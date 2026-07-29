"""US station-side climate index: NOAA/NCEI 1991-2020 US Climate Normals, monthly.

Writes data/us/noaa_stations.json. Station side only. This script does NOT match
stations to places; it publishes every station with its own full record so the
matching step can choose.

WHY THE BULK ARCHIVE AND NOT THE ACCESS DATA SERVICE
  The NCEI Access Data Service (https://www.ncei.noaa.gov/access/services/data/v1
  ?dataset=normals-monthly-1991-2020) works, but for the normals datasets it
  requires an explicit station list: `bbox=` and `locations=FIPS:xx` both come
  back 400 {"field":"stations","message":"A station is required."}. So it cannot
  enumerate "all US stations" on its own, and pulling 15,616 stations from it is
  15,616 round trips against a list you had to source elsewhere anyway.
  The bulk archive is one 30MB tarball holding all 15,616 by-station monthly CSVs
  with the flags and the station metadata in the same rows, and it is more
  complete than NCEI's own published station inventory (inventory_30yr.txt is
  missing USW00023119 MARCH AFB, CA). The Access service is used here only as an
  independent spot check (--apicheck), and it agrees value for value.

UNIT CONVERSIONS (NCEI publishes US customary; this file is metric)
  temperature  degF -> degC   (F - 32) * 5/9      MLY/ANN-TAVG,-TMAX,-TMIN
  precip       inch -> mm     * 25.4              MLY/ANN-PRCP-NORMAL
  snow         inch -> cm     * 2.54              MLY/ANN-SNOW-NORMAL
  elevation    already metres in GHCN-D metadata (Denver-Stapleton reads 1611.2,
               which is 5286 ft, so the field is metres, not feet). Not converted.
  Do NOT ask the Access service for units=metric: it converts TMAX/TMIN/PRCP/SNOW
  but hands back MLY-TAVG-NORMAL still in Fahrenheit (Miami January comes out
  "68.6" beside TMAX "24.6"). All conversion here is done locally, from the
  as-published US customary values, so one silently-unconverted element cannot
  slip through.

MISSING vs REAL ZERO  (the one that would ruin the dataset)
  In this dataset absence is structural, not a sentinel. A station that never
  measured snow has no MLY-SNOW-NORMAL column at all: header widths run from 13
  to 413 columns depending on what the station reports. There is not one -9999
  and not one M measurement flag anywhere in the five elements we read.
    element absent from the station's file  -> null           (never measured)
    value present                           -> real value, including 0.0
  So Miami snow is 0.0 twelve times over (the column exists, comp flag P, ~12
  years) and Honolulu snow is null (no column). Phoenix snow is null too.
  Belt and braces for a future republish, we also null on: blank value, any
  sentinel <= -999, and measurement flags M (missing), Y (insufficient values),
  V (too cold to compute), Z (logical inconsistency).
  Measurement flag X means "nonzero value has rounded to zero" - that is a real
  measurement of almost-no-snow, so it is KEPT as 0.0, not nulled.
  Completeness flags S/R/P/E (and C/Q from older vintages) all describe how much
  record went into a value that does exist. None of them means missing, so none
  of them nulls a value; they are reported per element in `quality` instead.
  Every month is read from its own row. Nothing is ever carried across months and
  nothing is ever filled in, so a gap cannot be papered over with a neighbour.

WHAT IS NOT HERE
  Bright sunshine hours. The Canadian normals publish it; the US 1991-2020
  normals do not publish any sunshine element (the monthly variable list is
  TMIN TMAX TAVG DUTR CLDD HTDD GRDD PRCP SNOW SNWD). It is left out entirely
  rather than approximated from cloud cover.

SOURCES
  https://www.ncei.noaa.gov/data/normals-monthly/1991-2020/archive/us-climate-normals_1991-2020_v1.0.1_monthly_multivariate_by-station_c20230404.tar.gz
  https://www.ncei.noaa.gov/data/normals-annualseasonal/1991-2020/archive/us-climate-normals_1991-2020_v1.0.1_annualseasonal_multivariate_by-station_c20230404.tar.gz
  https://www.ncei.noaa.gov/data/normals-monthly/1991-2020/doc/Readme_By-Variable_By-Station_Normals_Files.txt   (flag definitions)
  https://www.ncei.noaa.gov/data/normals-monthly/1991-2020/doc/inventory_30yr.txt (state cross-check)
  https://www.ncei.noaa.gov/data/normals-monthly/1991-2020/access/                (per-station CSVs, same content)
  https://www.ncei.noaa.gov/access/services/data/v1                              (spot check)

usage: python3 src/us/build_climate.py [--cache DIR] [--apicheck]
"""
import csv, json, math, os, re, sys, tarfile, urllib.request, tempfile, collections

BASE_MLY = "https://www.ncei.noaa.gov/data/normals-monthly/1991-2020"
BASE_ANN = "https://www.ncei.noaa.gov/data/normals-annualseasonal/1991-2020"
TAR_MLY = "us-climate-normals_1991-2020_v1.0.1_monthly_multivariate_by-station_c20230404.tar.gz"
TAR_ANN = "us-climate-normals_1991-2020_v1.0.1_annualseasonal_multivariate_by-station_c20230404.tar.gz"
INVENTORY = BASE_MLY + "/doc/inventory_30yr.txt"

OUT = "data/us/noaa_stations.json"

# 50 states + DC. Everything else NCEI ships (PR VI GU AS MP FM MH PW UM, and one
# Ontario station) is dropped: this index is for the 50 states + DC.
STATES = ("AL AK AZ AR CA CO CT DE DC FL GA HI ID IL IN IA KS KY LA ME MD MA MI "
          "MN MS MO MT NE NV NH NJ NM NY NC ND OH OK OR PA RI SC SD TN TX UT VT "
          "VA WA WV WI WY").split()

# our five elements -> (monthly NCEI variable, annual NCEI variable, converter)
F2C = lambda v: (v - 32.0) * 5.0 / 9.0
IN2MM = lambda v: v * 25.4
IN2CM = lambda v: v * 2.54
ELEMENTS = {
    "tmean":  ("MLY-TAVG-NORMAL", "ANN-TAVG-NORMAL", F2C,   "degF->degC"),
    "tmax":   ("MLY-TMAX-NORMAL", "ANN-TMAX-NORMAL", F2C,   "degF->degC"),
    "tmin":   ("MLY-TMIN-NORMAL", "ANN-TMIN-NORMAL", F2C,   "degF->degC"),
    "precip": ("MLY-PRCP-NORMAL", "ANN-PRCP-NORMAL", IN2MM, "inch->mm"),
    "snow":   ("MLY-SNOW-NORMAL", "ANN-SNOW-NORMAL", IN2CM, "inch->cm"),
}
ANNUAL_OP = {"tmean": "mean", "tmax": "mean", "tmin": "mean",
             "precip": "sum", "snow": "sum"}
# measurement flags that mean "there is no value here"
MEAS_MISSING = {"M", "Y", "V", "Z"}
# completeness flags, best record first. S/R/P/E are the 1991-2020 set; C and Q
# turn up in older normals vintages, kept so a republish does not read as unknown.
QUALITY_ORDER = ["C", "S", "R", "P", "Q", "E"]


def log(*a):
    print(*a, flush=True)


def fetch(url, path):
    if os.path.exists(path) and os.path.getsize(path) > 0:
        log(f"  cached {os.path.basename(path)} ({os.path.getsize(path)/1e6:.1f} MB)")
        return path
    log(f"  GET {url}")
    req = urllib.request.Request(url, headers={"User-Agent": "livable-climate-build/1.0"})
    with urllib.request.urlopen(req, timeout=900) as r, open(path, "wb") as fh:
        fh.write(r.read())
    log(f"       -> {os.path.basename(path)} ({os.path.getsize(path)/1e6:.1f} MB)")
    return path


def untar(tgz, dest):
    if os.path.isdir(dest) and len(os.listdir(dest)) > 1000:
        log(f"  cached {dest}/ ({len(os.listdir(dest))} files)")
        return dest
    os.makedirs(dest, exist_ok=True)
    with tarfile.open(tgz) as t:
        t.extractall(dest)
    log(f"  extracted {len(os.listdir(dest))} files -> {dest}/")
    return dest


def value(row, idx, var):
    """One cell -> (float|None, meas_flag, comp_flag, years). None means missing.

    Three separate ways a value can be absent, all collapsing to None:
    the station has no such column, the cell is blank/sentinel, or the
    measurement flag says the value could not be computed."""
    if var not in idx:
        return None, "", "", None                       # station never reports it
    raw = row[idx[var]].strip()
    mf = row[idx["meas_flag_" + var]].strip() if "meas_flag_" + var in idx else ""
    cf = row[idx["comp_flag_" + var]].strip() if "comp_flag_" + var in idx else ""
    yr = row[idx["years_" + var]].strip() if "years_" + var in idx else ""
    yr = int(yr) if yr.isdigit() else None
    if mf in MEAS_MISSING:
        return None, mf, cf, yr
    if raw == "":
        return None, mf, cf, yr
    try:
        v = float(raw)
    except ValueError:
        return None, mf, cf, yr
    if v <= -999:                                        # -9999 / -8888 sentinels
        return None, mf, cf, yr
    return v, mf, cf, yr                                 # 0.0 arrives here intact


def read_csv(path):
    with open(path, newline="", encoding="utf-8", errors="replace") as fh:
        rows = list(csv.reader(fh))
    if not rows:
        return None, []
    return {n: j for j, n in enumerate(rows[0])}, rows[1:]


def load_inventory(path):
    """id -> state, for cross-checking the state parsed out of the station name."""
    inv = {}
    for line in open(path, encoding="utf-8", errors="replace"):
        if len(line) < 41:
            continue
        inv[line[0:11].strip()] = line[38:40].strip()
    return inv


NAME_RE = re.compile(r"^(?P<name>.*?),\s*(?P<st>[A-Z]{2})\s+(?P<cc>[A-Z]{2})$")


def build(cache):
    os.makedirs(cache, exist_ok=True)
    log("1. sources")
    mly_tgz = fetch(f"{BASE_MLY}/archive/{TAR_MLY}", os.path.join(cache, TAR_MLY))
    ann_tgz = fetch(f"{BASE_ANN}/archive/{TAR_ANN}", os.path.join(cache, TAR_ANN))
    inv_txt = fetch(INVENTORY, os.path.join(cache, "inventory_30yr.txt"))
    mly = untar(mly_tgz, os.path.join(cache, "mly"))
    ann = untar(ann_tgz, os.path.join(cache, "ann"))
    inv = load_inventory(inv_txt)
    log(f"  inventory: {len(inv)} stations listed")

    files = sorted(f for f in os.listdir(mly) if f.endswith(".csv"))
    log(f"\n2. parsing {len(files)} by-station monthly files")

    stations, dropped = [], collections.Counter()
    state_mismatch, unparsed_name, no_annual_col, computed_annual = [], [], collections.Counter(), collections.Counter()
    widths = collections.Counter()
    meas_census, comp_census = collections.Counter(), collections.Counter()

    for n, fn in enumerate(files):
        sid = fn[:-4]
        midx, mrows = read_csv(os.path.join(mly, fn))
        if not midx or len(mrows) != 12:
            dropped["monthly file not 12 rows"] += 1
            continue
        widths[len(midx)] += 1
        head = mrows[0]

        nm_raw = head[midx["NAME"]].strip()
        m = NAME_RE.match(nm_raw)
        if m:
            name, state = m.group("name").strip(), m.group("st")
        else:
            name, state = nm_raw, inv.get(sid, "")
            unparsed_name.append((sid, nm_raw))
        if sid in inv and inv[sid] != state:
            state_mismatch.append((sid, state, inv[sid]))
        if state not in STATES:
            dropped[f"outside 50 states + DC ({state})"] += 1
            continue

        try:
            lat = round(float(head[midx["LATITUDE"]]), 5)
            lon = round(float(head[midx["LONGITUDE"]]), 5)
        except (ValueError, KeyError):
            dropped["no coordinates"] += 1
            continue
        try:
            elev = round(float(head[midx["ELEVATION"]]), 1)      # already metres
            if elev <= -999:
                elev = None
        except (ValueError, KeyError):
            elev = None

        # months, keyed by the month column in each row, never by row order
        by_month = {}
        for row in mrows:
            mo = row[midx["month"]].strip().lstrip("0") or "0"
            by_month[mo] = row
        if sorted(int(k) for k in by_month) != list(range(1, 13)):
            dropped["monthly file month set != 1..12"] += 1
            continue

        aidx, arows = read_csv(os.path.join(ann, fn))
        arow = arows[0] if arows else None

        rec = {"id": sid, "name": name, "state": state,
               "lat": lat, "lon": lon, "elev_m": elev}
        completeness, quality, years, annual_src = {}, {}, {}, {}

        for key, (mvar, avar, conv, _u) in ELEMENTS.items():
            vals, flags, yrs = {}, [], []
            for mo in range(1, 13):
                v, mf, cf, yr = value(by_month[str(mo)], midx, mvar)
                # an absent column is the dataset's own way of saying "this
                # station does not measure this", and must not read as an
                # unflagged value in the census
                meas_census[(key, mf if mvar in midx else "no column")] += 1
                comp_census[(key, cf)] += 1
                if v is None:
                    vals[str(mo)] = None
                else:
                    vals[str(mo)] = round(conv(v), 2)
                    if cf:
                        flags.append(cf)
                    if yr:
                        yrs.append(yr)
            got = sum(1 for mo in range(1, 13) if vals[str(mo)] is not None)
            completeness[key] = got

            # annual: prefer NCEI's own published annual normal. Only compute one
            # when all 12 months are real, so a partial year cannot masquerade as
            # an annual total.
            av = None
            if arow is not None and aidx:
                av, amf, acf, ayr = value(arow, aidx, avar)
                if av is not None:
                    vals["13"] = round(conv(av), 2)
                    annual_src[key] = "published"
                    if acf:
                        flags.append(acf)
                elif avar in aidx:
                    no_annual_col[key] += 1
            if av is None:
                if got == 12:
                    mv = [vals[str(mo)] for mo in range(1, 13)]
                    tot = sum(mv)
                    vals["13"] = round(tot / 12 if ANNUAL_OP[key] == "mean" else tot, 2)
                    annual_src[key] = "computed from 12 monthly normals"
                    computed_annual[key] += 1
                else:
                    vals["13"] = None
                    annual_src[key] = None

            if got == 0:
                rec[key] = None                          # element not in the record
                quality[key] = None
                years[key] = None
            else:
                rec[key] = vals
                quality[key] = max(flags, key=lambda f: QUALITY_ORDER.index(f)
                                   if f in QUALITY_ORDER else len(QUALITY_ORDER)) if flags else None
                years[key] = min(yrs) if yrs else None

        rec["completeness"] = completeness
        rec["quality"] = quality          # worst completeness flag over the record
        rec["years"] = years              # fewest years behind any month
        rec["annual_src"] = annual_src
        # how many of the five elements carry a full 12 months. The matcher wants
        # one home station holding the whole set, not temperature from the airport
        # and snow from across the harbour.
        rec["elements_full"] = sum(1 for k in ELEMENTS if completeness[k] == 12)
        stations.append(rec)
        if (n + 1) % 4000 == 0:
            log(f"  ...{n+1} files read, {len(stations)} kept")

    log(f"  kept {len(stations)} stations")
    for k, v in dropped.most_common():
        log(f"  dropped {v:5d}  {k}")
    log(f"  station-file header widths (columns present vary by station): "
        f"{dict(sorted(widths.items()))}")
    if unparsed_name:
        log(f"  station names that did not parse as 'NAME, ST US': {len(unparsed_name)} {unparsed_name[:5]}")
    if state_mismatch:
        log(f"  state disagreements name-vs-inventory: {len(state_mismatch)} {state_mismatch[:5]}")

    log("\n3. flag census over the five elements (all months, all kept stations)")
    log("  measurement flags  ('' = none, X = nonzero rounded to zero, kept):")
    for (el, f), c in sorted(meas_census.items()):
        if f:
            log(f"    {el:7s} {f}  {c}")
    log("  completeness flags (none of these mean missing):")
    seen = collections.Counter()
    for (el, f), c in sorted(comp_census.items()):
        if f:
            seen[f] += c
    log("    " + "  ".join(f"{f}={c}" for f, c in seen.most_common()))
    if computed_annual:
        log(f"  annual computed from 12 months (no published annual): {dict(computed_annual)}")

    return stations


def meta(stations):
    bys = collections.Counter(s["state"] for s in stations)
    empty = [st for st in STATES if not bys.get(st)]
    return {
        "source": "NOAA/NCEI 1991-2020 U.S. Climate Normals, monthly (v1.0.1)",
        "route": ("bulk by-station archive; the Access Data Service cannot "
                  "enumerate stations for this dataset (bbox and locations=FIPS "
                  "are rejected with 'A station is required'), and its "
                  "units=metric leaves MLY-TAVG-NORMAL in Fahrenheit"),
        "urls": [
            f"{BASE_MLY}/archive/{TAR_MLY}",
            f"{BASE_ANN}/archive/{TAR_ANN}",
            f"{BASE_MLY}/doc/Readme_By-Variable_By-Station_Normals_Files.txt",
            f"{BASE_MLY}/doc/inventory_30yr.txt",
            f"{BASE_MLY}/access/",
            "https://www.ncei.noaa.gov/access/services/data/v1?dataset=normals-monthly-1991-2020",
        ],
        "scope": "50 states + DC",
        "months": "'1'..'12' monthly normals, '13' annual, matching data/climate.json",
        "units": {"tmean": "degC (converted from degF)",
                  "tmax": "degC (converted from degF)",
                  "tmin": "degC (converted from degF)",
                  "precip": "mm (converted from inches)",
                  "snow": "cm (converted from inches)",
                  "elev_m": "metres as published in GHCN-D metadata, not converted"},
        "conversions": {"temperature": "(F - 32) * 5/9",
                        "precip": "inches * 25.4", "snow": "inches * 2.54"},
        "missing_policy": ("null = the element is absent from that station's record "
                           "(NCEI omits the columns entirely), or the cell is blank, "
                           "a <=-999 sentinel, or carries measurement flag M/Y/V/Z. "
                           "0.0 = a measured zero and is kept, including measurement "
                           "flag X (nonzero rounded to zero). Completeness flags "
                           "S/R/P/E/C/Q never null a value; they are reported in "
                           "'quality'. No month is ever filled from another month."),
        "completeness": "per element, how many of the 12 months carry a real value (0-12)",
        "quality": "per element, worst completeness flag over the record: S standard (24+ yr), R representative (10+ yr, gaps infilled from neighbours), P provisional (10+ yr, not infilled), E estimated statistically from nearby stations",
        "years": "per element, fewest years of record behind any single month",
        "sunshine": ("not available: the US 1991-2020 normals publish no bright "
                     "sunshine element, so there is no counterpart to the Canadian "
                     "'sun' field and none is invented"),
        "station_count": len(stations),
        "states_with_no_station": empty,
        "gaps": {
            "dc": ("the District of Columbia has no 1991-2020 normals station at "
                   "all. GHCN-Daily has 21 DC stations, including THE WHITE HOUSE, "
                   "but every one is a short-record volunteer gauge that does not "
                   "qualify for a normal, so none is published. Washington DC has "
                   "to draw on MD and VA stations, and should be labelled as doing so."),
            "no_elevation": sorted(s["id"] for s in stations if s["elev_m"] is None),
            "no_elevation_note": ("elev_m is null for these; the matcher should "
                                  "distrust them rather than treat them as sea level"),
        },
    }


# ---------------------------------------------------------------- validation ---
CHECKS = [
    ("Miami FL",              25.7617,  -80.1918),
    ("International Falls MN", 48.6023,  -93.4109),
    ("Phoenix AZ",            33.4484, -112.0740),
    ("Seattle WA",            47.6062, -122.3321),
    ("Buffalo NY",            42.8864,  -78.8784),
    ("Denver CO",             39.7392, -104.9903),
    ("Anchorage AK",          61.2181, -149.9003),
    ("Honolulu HI",           21.3069, -157.8583),
]
SANITY = {
    "Miami FL": ("jan tmean > 15", lambda j, u, s: j is not None and j > 15),
    "International Falls MN": ("jan tmean < -14", lambda j, u, s: j is not None and j < -14),
    "Phoenix AZ": ("jul tmean > 33", lambda j, u, s: u is not None and u > 33),
    "Buffalo NY": ("annual snow > 200", lambda j, u, s: s is not None and s > 200),
    "Honolulu HI": ("snow 0 or null, not a number", lambda j, u, s: s is None or s == 0),
}


def km(a, b, c, d):
    R = 6371.0088
    p = math.radians
    x = (math.sin(p(c - a) / 2) ** 2
         + math.cos(p(a)) * math.cos(p(c)) * math.sin(p(d - b) / 2) ** 2)
    return 2 * R * math.asin(math.sqrt(x))


# Ranking the check-table pick, in kilometres, the way src/match_climate.py prices
# a thin record. Nearest-with-the-most-elements is not good enough: it handed
# Phoenix to SOUTH PHOENIX (a 16-year R-flagged co-op reading 32.1C in July,
# which happens to also log snow) over SKY HARBOR (27 years, S-flagged, 35.3C)
# purely because the airport does not report snow.
QUAL_KM = {"C": 0, "S": 0, "R": 6, "P": 10, "Q": 14, "E": 25, None: 30}


def pick_cost(d, s):
    q = QUAL_KM.get(s["quality"]["tmean"], 30)
    yr = s["years"]["tmean"] or 0
    return d + q + max(0, 25 - yr)          # short record costs a km per missing year


def validate(stations):
    log("\n4. check table")
    log("   Pick = station within 40 km with a full 12-month tmean, ranked by")
    log("   distance + a kilometre price on a thin or infilled record. A sanity")
    log("   print only: matching places to stations is a later step.")
    hdr = (f"{'city':23s} {'station':30s} {'id':12s} {'km':>5s} {'elev_m':>7s} "
           f"{'jan tmean':>9s} {'jul tmean':>9s} {'ann snow':>9s} {'q':>4s} {'yr':>3s}")
    log("   " + hdr)
    log("   " + "-" * len(hdr))
    ok = True
    for city, lat, lon in CHECKS:
        near = [(km(lat, lon, s["lat"], s["lon"]), s) for s in stations]
        near = [t for t in near if t[0] <= 40]
        full = [t for t in near if t[1]["completeness"]["tmean"] == 12]
        pool = full or near
        pool.sort(key=lambda t: pick_cost(*t))
        if not pool:
            log(f"   {city:23s} NO STATION WITHIN 40 km")
            ok = False
            continue
        d, s = pool[0]
        jan = (s["tmean"] or {}).get("1")
        jul = (s["tmean"] or {}).get("7")
        sn = (s["snow"] or {}).get("13")
        f = lambda v: "null" if v is None else f"{v:.1f}"
        log(f"   {city:23s} {s['name'][:30]:30s} {s['id']:12s} {d:5.1f} "
            f"{'' if s['elev_m'] is None else s['elev_m']:>7} {f(jan):>9s} {f(jul):>9s} "
            f"{f(sn):>9s} {str(s['quality']['tmean'] or '-'):>4s} "
            f"{str(s['years']['tmean'] or '-'):>3s}")
        if city in SANITY:
            label, test = SANITY[city]
            good = test(jan, jul, sn)
            ok &= good
            log(f"   {'':23s}   sanity: {label:32s} {'PASS' if good else 'FAIL'}")

    log("\n4b. elevation is carried for every station, because the matcher needs it")
    log("    (Revelstoke took its snow from a station 1,431 m up a mountain and read")
    log("    1,388 cm of alpine snowpack instead of the town's 425 cm). Elevation")
    log("    spread among stations within 40 km of each check city:")
    have = sum(1 for s in stations if s["elev_m"] is not None)
    log(f"    stations carrying elev_m: {have} of {len(stations)}"
        f"  ({len(stations)-have} without)")
    for city, lat, lon in CHECKS:
        near = [s for s in stations if km(lat, lon, s["lat"], s["lon"]) <= 40
                and s["elev_m"] is not None]
        if not near:
            continue
        lo = min(near, key=lambda s: s["elev_m"])
        hi = max(near, key=lambda s: s["elev_m"])
        log(f"    {city:23s} {len(near):4d} stations, {lo['elev_m']:7.1f} m to "
            f"{hi['elev_m']:7.1f} m  (spread {hi['elev_m']-lo['elev_m']:6.1f} m, "
            f"highest = {hi['name'][:26]})")

    log("\n5. stations by state")
    bys = collections.Counter(s["state"] for s in stations)
    missing = [st for st in STATES if st not in bys]
    line = []
    for st in STATES:
        line.append(f"{st}={bys.get(st,0)}")
    for i in range(0, len(line), 12):
        log("   " + "  ".join(line[i:i + 12]))
    log(f"   states+DC with at least one station: {len(bys)} of {len(STATES)}")
    if missing:
        log(f"   NO STATIONS AT ALL: {', '.join(missing)}")

    log("\n6. completeness")
    full = collections.Counter()
    dist = {k: collections.Counter() for k in ELEMENTS}
    for s in stations:
        for k in ELEMENTS:
            c = s["completeness"][k]
            dist[k][c] += 1
            if c == 12:
                full[k] += 1
    n = len(stations)
    log(f"   {'element':8s} {'12 of 12':>9s} {'partial':>8s} {'0 (absent)':>11s}   {'% full':>7s}")
    for k in ELEMENTS:
        part = sum(v for c, v in dist[k].items() if 0 < c < 12)
        log(f"   {k:8s} {full[k]:9d} {part:8d} {dist[k][0]:11d}   {100*full[k]/n:6.1f}%")
    log(f"   stations with a complete 12-month tmean: {full['tmean']} of {n}")
    ef = collections.Counter(s["elements_full"] for s in stations)
    log("   elements fully present per station (of 5): "
        + "  ".join(f"{k}->{ef[k]}" for k in sorted(ef, reverse=True)))
    q = {k: collections.Counter(s["quality"][k] for s in stations if s["quality"][k]) for k in ELEMENTS}
    log("   worst completeness flag per element:")
    for k in ELEMENTS:
        log(f"     {k:8s} " + "  ".join(f"{f}={c}" for f, c in q[k].most_common()))
    return ok


def apicheck(stations):
    """Independent read of the same numbers through the Access Data Service."""
    log("\n7. spot check against the Access Data Service (independent route)")
    ids = ["USW00012839", "USW00023183", "USW00014733", "USW00022521"]
    dts = "MLY-TAVG-NORMAL,MLY-SNOW-NORMAL"
    url = ("https://www.ncei.noaa.gov/access/services/data/v1?"
           "dataset=normals-monthly-1991-2020&stations=" + ",".join(ids) +
           "&dataTypes=" + dts + "&format=json&startDate=1991-01-01&endDate=2020-12-31"
           "&includeStationName=true")
    log(f"   {url}")
    try:
        rows = json.load(urllib.request.urlopen(
            urllib.request.Request(url, headers={"User-Agent": "livable-climate-build/1.0"}),
            timeout=180))
    except Exception as e:
        log(f"   API unavailable, skipping: {e}")
        return
    idx = {s["id"]: s for s in stations}
    for r in rows:
        if r.get("DATE") != "01":
            continue
        s = idx.get(r["STATION"])
        if not s:
            continue
        api_t = r.get("MLY-TAVG-NORMAL")
        api_s = r.get("MLY-SNOW-NORMAL")
        mine_t = (s["tmean"] or {}).get("1")
        mine_s = (s["snow"] or {}).get("1")
        exp_t = None if api_t in (None, "") else round(F2C(float(api_t)), 2)
        exp_s = None if api_s in (None, "") else round(IN2CM(float(api_s)), 2)
        log(f"   {s['id']} {s['name'][:24]:24s} jan tmean api {str(api_t).strip() or 'None':>6s}F"
            f" -> {str(exp_t):>7s}C  ours {str(mine_t):>7s}  "
            f"{'MATCH' if exp_t == mine_t else 'MISMATCH'}"
            f" | jan snow api {str(api_s).strip() or 'None':>5s}in -> {str(exp_s):>6s}cm"
            f" ours {str(mine_s):>6s} {'MATCH' if exp_s == mine_s else 'MISMATCH'}")


def main():
    cache = os.path.join(tempfile.gettempdir(), "ncei-normals-1991-2020")
    if "--cache" in sys.argv:
        cache = sys.argv[sys.argv.index("--cache") + 1]
    stations = build(cache)
    stations.sort(key=lambda s: (s["state"], s["id"]))
    ok = validate(stations)
    if "--apicheck" in sys.argv:
        apicheck(stations)
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w") as fh:
        json.dump({"meta": meta(stations), "stations": stations}, fh, separators=(",", ":"))
    log(f"\nwrote {OUT}  ({os.path.getsize(OUT)/1e6:.1f} MB, {len(stations)} stations)")
    log("sanity checks: " + ("ALL PASS" if ok else "SOMETHING FAILED, see above"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
