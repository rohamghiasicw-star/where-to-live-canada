"""US place elevation: ground elevation in metres at each place's coordinate.

Writes data/us/elevation.json  ->  {"<geoid>": <metres> | null}
Reads  data/us/places.json     (never modified)

WHY THIS FILE EXISTS
  The climate step picks one weather station per place. Distance alone is not
  enough: in the Canadian build, Revelstoke's nearest published-normals station
  sat 43 km away and 1,431 m higher and reported 1,388 cm of alpine snowpack
  instead of the town's 425 cm. The fix is to put elevation difference into the
  station-matching cost, and that needs the PLACE's elevation.

  The interim guard used the MEDIAN ELEVATION OF NEARBY STATIONS as a stand-in,
  which is biased exactly where it matters. Indio CA sits on the Coachella
  Valley floor at or below sea level, but San Jacinto Peak rises 3,300 m beside
  it, so the local station profile reads 602 m. This file replaces that proxy
  with the real ground elevation under each place's coordinate: Indio's
  coordinate reads 1.2 m, a 600 m correction.

SOURCE: opentopodata.org public API, dataset `ned10m`
  ned10m is USGS 3DEP / NED at 1/3 arc-second (~10 m) - the same USGS model
  EPQS serves, so it is US-authoritative rather than a global resample, and it
  accepts 100 locations per POST (43 calls for 4,226 places instead of 4,226
  sequential round trips).

  FALLBACK CHAIN, used only where the previous dataset returns null:
    1. ned10m   USGS 3DEP/NED 1/3 arc-second, CONUS + AK + HI + PR
    2. srtm30m  NASA SRTM v3 1 arc-second - the specified fallback
    3. mapzen   global composite (NED + SRTM + GMTED + ...), last resort only
  srtm30m cannot be the only fallback: SRTM flies no higher than 60 N, so it is
  null for every Alaska place above that line. mapzen is the only remaining
  option there. Which dataset produced each value is recorded and counted in
  the report, so any seam in the data is visible rather than hidden.

CROSS-CHECKED against USGS EPQS (https://epqs.nationalmap.gov/v1/json), a
  different service reading the same USGS model, single point only. Run with
  --epqs to re-verify the whole check table. Agreement at the points tested is
  within a couple of decimetres (Denver 1612.9 vs 1613.1; New Orleans -1.43 vs
  -1.46; Indio 1.16 vs 1.05). EPQS is a check, never a source for the output:
  mixing two services would put a seam through the dataset.

COORDINATE ORDER  (the classic way to ruin this file)
  places.json carries `lat` then `lon`; opentopodata wants "lat,lon"; EPQS wants
  x=lon and y=lat. Sending them swapped returns plausible-looking numbers for
  the wrong place. Three independent guards, all of which must pass before
  anything is fetched in bulk:
    1. CONTROLS below are fetched and range-checked. Two of them only work if
       the order is right: Furnace Creek must come back NEGATIVE (no swapped US
       coordinate lands below sea level) and Leadville must clear 3,000 m.
    2. REVERSED_PROBE sends known points with lat/lon deliberately swapped and
       asserts the answers are NOT the true ones. Swapped US coordinates land
       in the southern ocean or outside NED, so ned10m returns null; when the
       swapped latitude is outside +/-90 the API refuses outright with
       "Latitude must be between -90 and 90. Provide locations in lat,lon
       order", which is the service naming the order in words.
    3. Every result is matched to its request by the lat/lng the API ECHOES
       BACK, not by list position, so a reordered or truncated response raises
       instead of silently shifting elevations onto the wrong places.

CHECKPOINTED
  data/us/elevation.json is rewritten (atomically, via a temp file + os.replace)
  after EVERY batch, so an interruption leaves a usable partial file instead of
  nothing. During a run in progress the not-yet-fetched places are null; on a
  completed run null means the services genuinely had no value. The run log
  prints "CHECKPOINT filled n/N" after each write, so a partial file is
  identifiable from the tail of the log.

RESUMABLE
  Raw API responses are cached to disk (sha1 of dataset + the exact request
  string), so a restart replays the fetch at zero API cost. An existing
  elevation.json is also read back as a warm start, so batches already fully
  valued are skipped even if the cache is wiped. Gaps (null) are always retried.

GEOID KEYS ARE STRINGS
  787 of the 4,226 geoids have a leading zero (Alabama places look like
  '0100100'). They are read as strings, never parsed as numbers, and the writer
  asserts the leading-zero count survives to the output file.

NEVER INTERPOLATED
  A place with no value from any dataset is written as null. Nothing is averaged
  from neighbours, carried over, or guessed. 0.0 is a real elevation (sea level)
  and is kept as 0.0; only a genuine absence becomes null.

INTERNAL POINTS ARE NOT DOWNTOWNS  (read this before trusting a big city)
  places.json lat/lon are Census Gazetteer internal points of the whole place
  polygon. For a municipality that annexed a mountain range, that point is up
  the mountain, and the elevation here is correctly the elevation of that point,
  not of the populated core. Confirmed by EPQS at three places:
      place              internal point        downtown
      Anchorage AK       1217.1 m              33.6 m
      Urban Honolulu HI    52.0 m               5.8 m
      Indio CA              1.0 m              -3.6 m
  Both services agree at the internal point in every case, so this is the
  coordinate, not the elevation service. Section 8 of the report lists every
  large-area place reading high so the station matcher can decide. This file
  does not silently "fix" any of them - correcting them means changing
  places.json, which is out of scope here.

RATE LIMITS, honoured (https://www.opentopodata.org/ - "Max 100 locations per
  request. Max 1 call per second. Max 1000 calls per day."): batches of 100,
  >=1.1 s between calls, exponential backoff on 429/5xx that also honours
  Retry-After.

SOURCES
  https://www.opentopodata.org/                 (public API rate limits)
  https://www.opentopodata.org/api/             (request/response format)
  https://www.opentopodata.org/datasets/ned/    (ned10m provenance)
  https://www.opentopodata.org/datasets/srtm/   (srtm30m provenance, 60 N limit)
  https://www.opentopodata.org/datasets/mapzen/ (mapzen composite)
  https://api.opentopodata.org/v1/ned10m        (the endpoint used)
  https://epqs.nationalmap.gov/v1/json          (independent cross-check)
  https://www.usgs.gov/3d-elevation-program     (3DEP / NED programme)

usage:
  python3 src/us/build_elevation.py            # build (uses cache, retries gaps)
  python3 src/us/build_elevation.py --epqs     # also cross-check table vs EPQS
  python3 src/us/build_elevation.py --report   # re-print the report from the file
"""
import hashlib, json, math, os, statistics, sys, tempfile, time, urllib.error, urllib.request

PLACES = "data/us/places.json"
OUT = "data/us/elevation.json"

API = "https://api.opentopodata.org/v1/%s"
EPQS = "https://epqs.nationalmap.gov/v1/json?x=%.6f&y=%.6f&units=Meters&wkid=4326"
PRIMARY = "ned10m"
FALLBACKS = ["srtm30m", "mapzen"]   # srtm30m is the specified fallback; mapzen
                                    # exists only because SRTM stops at 60 N

BATCH = 100          # documented maximum locations per request
MIN_INTERVAL = 1.1   # documented maximum 1 call/second, with headroom
MAX_TRIES = 6
UA = "livable-us-elevation/1.0 (dataset build; batched, 1 req/sec)"

CACHE = os.environ.get("LIVABLE_US_CACHE",
                       os.path.join(tempfile.gettempdir(), "livable_us_elev_cache"))

# Range checks.
#   guard=True   must pass or the build aborts before touching the output file.
#   guard=False  reported only. These are the places whose Gazetteer internal
#                point is demonstrably not the populated core (see the header);
#                their true downtown value is in DOWNTOWNS below and the
#                mismatch is explained in the report rather than papered over.
# geoid=None means the point is not in places.json and is fetched on its own so
# the order guards have an unambiguous reference to bite on.
#        name                        geoid      lat        lon        lo     hi   guard
CONTROLS = [
    ("Denver CO",                   "0820000",  39.76185, -104.88111, 1500,  1750, True),
    ("Leadville CO (external)",     None,       39.25080, -106.29250, 3000,  3200, True),
    ("Flagstaff AZ",                "0423620",  35.18521, -111.62070, 1950,  2250, True),
    ("Santa Fe NM",                 "3570500",  35.66198, -105.98181, 1950,  2250, True),
    ("Salt Lake City UT",           "4967000",  40.77693, -111.93099, 1200,  1450, True),
    ("New Orleans LA",              "2255000",  30.05342,  -89.93450,  -10,     0, True),
    ("Miami FL",                    "1245000",  25.77516,  -80.20861,   -5,     5, True),
    ("Virginia Beach VA",           "5182000",  36.77952,  -76.02914,   -5,     5, True),
    ("Furnace Creek CA (external)", None,       36.46140, -116.86560, -100,     0, True),
    ("Indio CA",                    "0636448",  33.73164, -116.23597,  -20,    20, True),
    ("Anchorage AK",                "0203000",  61.17425, -149.28433,    0,    50, False),
    ("Urban Honolulu HI",           "1571550",  21.32435, -157.84764,    0,    20, False),
]

# Populated-core coordinates for the places whose internal point sits elsewhere.
# Used ONLY to explain the mismatch in the report. Never written to the output.
DOWNTOWNS = {
    "0203000": ("Anchorage downtown",     61.21810, -149.89550),
    "1571550": ("Honolulu downtown",      21.30690, -157.85830),
    "0636448": ("Indio city hall",        33.72060, -116.21560),
}

# Deliberately swapped lat/lon. Correct-order truth is in the 4th slot; a
# swapped request must NOT return it. Two outcomes both prove the order is
# right: the request lands outside NED and returns null, or the swapped latitude
# falls outside +/-90 and the API refuses, naming the order it wants.
REVERSED_PROBE = [
    ("Miami FL",          -80.20861, 25.77516,    1.6),
    ("Virginia Beach VA", -76.02914, 36.77952,    4.2),
    ("Indio CA",         -116.23597, 33.73164,   -6.0),
    ("Denver CO",        -104.88111, 39.76185, 1612.9),
]


def log(*a):
    print(*a)
    sys.stdout.flush()


# ---------------------------------------------------------------- HTTP + cache

_last_call = [0.0]
_calls = [0]


def _throttle():
    wait = MIN_INTERVAL - (time.time() - _last_call[0])
    if wait > 0:
        time.sleep(wait)
    _last_call[0] = time.time()


def _post(dataset, locstr):
    """One POST. Retries 429/5xx with backoff, honouring Retry-After."""
    body = json.dumps({"locations": locstr}).encode()
    url = API % dataset
    for attempt in range(1, MAX_TRIES + 1):
        _throttle()
        req = urllib.request.Request(url, data=body, headers={
            "Content-Type": "application/json", "User-Agent": UA})
        try:
            with urllib.request.urlopen(req, timeout=120) as r:
                _calls[0] += 1
                return json.load(r)
        except urllib.error.HTTPError as e:
            retryable = e.code == 429 or 500 <= e.code < 600
            hdr = e.headers.get("Retry-After") if e.headers else None
            back = float(hdr) if (hdr or "").strip().isdigit() else 2.0 ** attempt
            detail = ""
            try:
                detail = e.read().decode("utf8", "replace")[:200]
            except Exception:
                pass
            if not retryable or attempt == MAX_TRIES:
                raise RuntimeError("HTTP %s from %s: %s" % (e.code, url, detail))
            log("    HTTP %s, retry %d/%d in %.0fs %s"
                % (e.code, attempt, MAX_TRIES - 1, back, detail))
            time.sleep(back)
        except (urllib.error.URLError, TimeoutError, OSError) as e:
            if attempt == MAX_TRIES:
                raise RuntimeError("network failure on %s: %s" % (url, e))
            back = 2.0 ** attempt
            log("    %s, retry %d/%d in %.0fs" % (e, attempt, MAX_TRIES - 1, back))
            time.sleep(back)
    raise RuntimeError("unreachable")


def fetch_batch(dataset, pts):
    """pts = [(lat, lon), ...] <= BATCH.  Returns [elev|None] aligned to pts.

    Results are matched to requests by the coordinates the API echoes back, so a
    reordered or truncated response raises instead of shifting values sideways.
    Responses are cached on disk keyed by dataset + the exact request string.
    """
    locstr = "|".join("%.6f,%.6f" % (la, lo) for la, lo in pts)
    # sha1, not hash(): str hashing is salted per process, so hash() would miss
    # the cache on every restart and refetch the whole dataset.
    key = "%s_%s_%d.json" % (dataset,
                             hashlib.sha1(locstr.encode()).hexdigest()[:16], len(pts))
    path = os.path.join(CACHE, key)

    d = None
    if os.path.exists(path):
        try:
            cached = json.load(open(path))
            if cached.get("_locstr") == locstr:   # guard against a hash collision
                d = cached["response"]
        except Exception:
            d = None
    if d is None:
        d = _post(dataset, locstr)
        tmp = path + ".tmp"
        with open(tmp, "w") as f:
            json.dump({"_locstr": locstr, "_dataset": dataset, "response": d}, f)
        os.replace(tmp, path)

    if d.get("status") != "OK":
        raise RuntimeError("%s status %s: %s" % (dataset, d.get("status"), d.get("error")))
    res = d.get("results") or []
    if len(res) != len(pts):
        raise RuntimeError("%s returned %d results for %d locations"
                           % (dataset, len(res), len(pts)))

    out = []
    for (la, lo), r in zip(pts, res):
        loc = r.get("location") or {}
        gla, glo = loc.get("lat"), loc.get("lng")
        if gla is None or glo is None:
            raise RuntimeError("%s result missing echoed location: %r" % (dataset, r))
        if abs(float(gla) - la) > 1e-4 or abs(float(glo) - lo) > 1e-4:
            raise RuntimeError(
                "%s echoed (%s,%s) for requested (%.6f,%.6f) - response is "
                "misaligned or the coordinate order is wrong; refusing to key "
                "elevations onto the wrong places" % (dataset, gla, glo, la, lo))
        e = r.get("elevation")
        out.append(None if e is None else float(e))
    return out


def epqs_one(lat, lon):
    """USGS EPQS single point, metres. Cross-check only, never a source."""
    for attempt in range(1, 4):
        try:
            req = urllib.request.Request(EPQS % (lon, lat), headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=60) as r:
                d = json.load(r)
            v = d.get("value")
            if v in (None, "", "-1000000"):
                return None, None
            return float(v), d.get("resolution")
        except Exception:
            if attempt == 3:
                return None, None
            time.sleep(2.0 ** attempt)
    return None, None


# ------------------------------------------------------------------ order guards

def check_order():
    """Must pass before the bulk fetch. Aborts the build if a guard fails."""
    log("\n1. COORDINATE ORDER GUARDS  (nothing is fetched in bulk until these pass)")
    pts = [(c[2], c[3]) for c in CONTROLS]
    got = fetch_batch(PRIMARY, pts)
    fails = []
    log("   %-30s %10s  %-16s %s" % ("control", "metres", "expected", "verdict"))
    for (name, _g, la, lo, lo_ok, hi_ok, guard), v in zip(CONTROLS, got):
        ok = v is not None and lo_ok <= v <= hi_ok
        log("   %-30s %10s  [%6g,%6g]  %s"
            % (name, "null" if v is None else "%.1f" % v, lo_ok, hi_ok,
               "ok" if ok else ("OUT OF RANGE" if guard else "out of range (not a guard)")))
        if not ok and guard:
            fails.append((name, v, lo_ok, hi_ok))

    log("\n   reversed-order probe (swapped lat/lon must NOT return the truth):")
    for name, ra, rb, truth in REVERSED_PROBE:
        try:
            v = fetch_batch(PRIMARY, [(ra, rb)])[0]
        except RuntimeError as e:
            if "Latitude must be between" in str(e) or "INVALID_REQUEST" in str(e):
                log("     %-18s sent (%10.5f,%9.5f) -> API REFUSED the swap "
                    "(\"provide locations in lat,lon order\"); true %.1f  ok"
                    % (name, ra, rb, truth))
                continue
            raise
        bad = v is not None and abs(v - truth) < 50
        log("     %-18s sent (%10.5f,%9.5f) -> %-9s true %8.1f  %s"
            % (name, ra, rb, "null" if v is None else "%.1f" % v, truth,
               "ok (not the truth)" if not bad else "ORDER BUG"))
        if bad:
            fails.append(("reversed " + name, v, truth, truth))
    return fails


# ------------------------------------------------------------------ checkpoint

def to_out(places, vals):
    out = {}
    for p, v in zip(places, vals):
        g = p["geoid"]
        if not isinstance(g, str):
            raise RuntimeError("geoid %r is not a string - leading zeros are at risk" % (g,))
        out[g] = None if v is None else round(v, 1)   # never interpolated
    return out


def checkpoint(places, vals, note=""):
    """Rewrite the output file atomically. Called after EVERY batch, so an
    interruption leaves a usable partial file rather than nothing."""
    out = to_out(places, vals)
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    tmp = OUT + ".tmp"
    with open(tmp, "w") as f:
        json.dump(out, f, separators=(",", ":"), sort_keys=True)
    os.replace(tmp, OUT)   # atomic: readers never see a half-written file
    filled = sum(1 for v in vals if v is not None)
    log("   CHECKPOINT wrote %s  filled %d/%d %s" % (OUT, filled, len(vals), note))
    return out


# ------------------------------------------------------------------------ build

def build(places):
    os.makedirs(CACHE, exist_ok=True)
    log("cache: %s  (%d files)"
        % (CACHE, len(os.listdir(CACHE)) if os.path.isdir(CACHE) else 0))

    fails = check_order()
    if fails:
        log("\nABORT: coordinate/control guards failed: %s" % fails)
        log("Nothing written. Fix the source or the coordinate order first.")
        return None, None

    pts = [(p["lat"], p["lon"]) for p in places]
    n = len(pts)
    vals = [None] * n
    src = [None] * n

    # Warm start: an earlier checkpointed file lets a wiped cache skip batches
    # that are already fully valued. Nulls are always retried.
    if os.path.exists(OUT):
        try:
            prev = json.load(open(OUT))
            for i, p in enumerate(places):
                v = prev.get(p["geoid"])
                if v is not None:
                    vals[i], src[i] = float(v), "resumed"
            log("warm start from %s: %d values already present"
                % (OUT, sum(1 for v in vals if v is not None)))
        except Exception as e:
            log("warm start skipped (%s)" % e)

    nb = math.ceil(n / BATCH)
    log("\n2. FETCH %s  (%d places, %d batches of <=%d, >=%.1fs apart)"
        % (PRIMARY, n, nb, BATCH, MIN_INTERVAL))
    for i in range(0, n, BATCH):
        b = i // BATCH + 1
        idx = list(range(i, min(i + BATCH, n)))
        if all(vals[k] is not None for k in idx):
            continue                                   # already valued, no call
        got = fetch_batch(PRIMARY, [pts[k] for k in idx])
        for k, v in zip(idx, got):
            vals[k] = v
            src[k] = PRIMARY if v is not None else None
        checkpoint(places, vals, "(batch %d/%d %s)" % (b, nb, PRIMARY))

    # Fallback chain for whatever the primary could not answer.
    for ds in FALLBACKS:
        gaps = [i for i, v in enumerate(vals) if v is None]
        log("\n3. FALLBACK %-8s for %d null" % (ds, len(gaps)))
        if not gaps:
            log("   none needed")
            continue
        for j in range(0, len(gaps), BATCH):
            idx = gaps[j:j + BATCH]
            got = fetch_batch(ds, [pts[k] for k in idx])
            for k, v in zip(idx, got):
                if v is not None:
                    vals[k], src[k] = v, ds
            checkpoint(places, vals, "(fallback %s)" % ds)
        log("   recovered %d, still null %d"
            % (sum(1 for k in gaps if src[k] == ds),
               sum(1 for k in gaps if vals[k] is None)))

    return to_out(places, vals), src


# ----------------------------------------------------------------------- report

def report(places, out, src, do_epqs=False):
    by_geoid = {p["geoid"]: p for p in places}

    log("\n4. CHECK TABLE")
    log("   %-26s %-8s %10s  %-16s %s"
        % ("place", "geoid", "metres", "expected", "verdict"))
    suspect = []
    for name, g, la, lo, lo_ok, hi_ok, guard in CONTROLS:
        if g is None:
            v = fetch_batch(PRIMARY, [(la, lo)])[0]
            v = None if v is None else round(v, 1)
            gtxt = "-extern-"
        else:
            v = out.get(g)
            gtxt = g
        ok = v is not None and lo_ok <= v <= hi_ok
        log("   %-26s %-8s %10s  [%6g,%6g]  %s"
            % (name[:26], gtxt, "null" if v is None else "%.1f" % v, lo_ok, hi_ok,
               "PASS" if ok else "CHECK - see 4b"))
        if not ok:
            suspect.append((name, g, la, lo, v, lo_ok, hi_ok))

    if suspect:
        log("\n4b. %d value(s) outside the expected range. Second opinion from USGS"
            % len(suspect))
        log("    EPQS - a different service reading the same USGS model - at the")
        log("    same coordinate, and at the populated core for comparison:")
        for name, g, la, lo, v, lo_ok, hi_ok in suspect:
            e, res = epqs_one(la, lo)
            agree = (v is not None and e is not None
                     and abs(v - e) < max(2.0, 0.02 * abs(v)))
            log("    %-24s %s %-9s EPQS %-9s (res %s) -> %s"
                % (name[:24], PRIMARY, "null" if v is None else "%.1f" % v,
                   "null" if e is None else "%.1f" % e, res,
                   "SERVICES AGREE: the coordinate, not the elevation"
                   if agree else "SERVICES DISAGREE - investigate"))
            p = by_geoid.get(g) if g else None
            if p:
                log("      internal point (%.5f, %.5f), place land area %s km2"
                    % (p["lat"], p["lon"], p.get("land_area_km2")))
            if g in DOWNTOWNS:
                dn, dla, dlo = DOWNTOWNS[g]
                de, dres = epqs_one(dla, dlo)
                log("      %-22s (%.5f, %.5f) EPQS %-9s <- the populated core, %s km away"
                    % (dn, dla, dlo, "null" if de is None else "%.1f m" % de,
                       "%.0f" % (111.0 * math.hypot(dla - p["lat"],
                                                    (dlo - p["lon"]) * math.cos(math.radians(dla)))
                                 ) if p else "?"))
                log("      places.json carries the polygon internal point, so the value")
                log("      above is right for that coordinate. NOT adjusted here.")

    if do_epqs:
        log("\n4c. EPQS cross-check of every control (--epqs)")
        for name, g, la, lo, _a, _b, _guard in CONTROLS:
            v = out.get(g) if g else round(fetch_batch(PRIMARY, [(la, lo)])[0], 1)
            e, res = epqs_one(la, lo)
            log("    %-26s %s %-9s EPQS %-9s delta %s"
                % (name[:26], PRIMARY, "null" if v is None else "%.1f" % v,
                   "null" if e is None else "%.1f" % e,
                   "n/a" if (v is None or e is None) else "%.2f m" % (v - e)))

    vv = [v for v in out.values() if v is not None]
    nulls = [g for g, v in out.items() if v is None]
    log("\n5. COVERAGE")
    log("   places in           %d" % len(places))
    log("   keys out            %d" % len(out))
    log("   with a value        %d  (%.2f%%)" % (len(vv), 100.0 * len(vv) / len(out)))
    log("   null                %d" % len(nulls))
    if src:
        for ds in [PRIMARY] + FALLBACKS + ["resumed"]:
            c = sum(1 for s in src if s == ds)
            if c:
                log("   from %-14s %d" % (ds, c))
        log("   API calls this run  %d" % _calls[0])
    if nulls:
        log("   null geoids: %s" % ", ".join(
            "%s (%s, %s)" % (g, by_geoid[g]["name"], by_geoid[g]["state"])
            for g in nulls[:20]))
    log("   leading-zero geoids %d in, %d out"
        % (sum(1 for p in places if p["geoid"].startswith("0")),
           sum(1 for g in out if g.startswith("0"))))

    log("\n6. DISTRIBUTION (metres)")
    log("   min    %.1f" % min(vv))
    log("   median %.1f" % statistics.median(vv))
    log("   mean   %.1f" % (sum(vv) / len(vv)))
    log("   max    %.1f" % max(vv))

    ranked = sorted(((v, g) for g, v in out.items() if v is not None), reverse=True)
    log("\n7. FIVE HIGHEST")
    for v, g in ranked[:5]:
        p = by_geoid[g]
        log("   %8.1f m  %-8s %-26s %-2s  (%.5f, %.5f)  %s km2"
            % (v, g, p["name"][:26], p["state"], p["lat"], p["lon"],
               p.get("land_area_km2")))
    log("\n   FIVE LOWEST")
    for v, g in ranked[-5:][::-1]:
        p = by_geoid[g]
        log("   %8.1f m  %-8s %-26s %-2s  (%.5f, %.5f)  %s km2"
            % (v, g, p["name"][:26], p["state"], p["lat"], p["lon"],
               p.get("land_area_km2")))

    # Places whose internal point is likely NOT the populated core. Surfaced,
    # never corrected - the station matcher will trust this number, so it needs
    # to know which ones describe a mountainside rather than a town.
    big = sorted((((p.get("land_area_km2") or 0), out.get(p["geoid"]), p)
                  for p in places
                  if (p.get("land_area_km2") or 0) > 400
                  and (out.get(p["geoid"]) or 0) > 900),
                 key=lambda t: -(t[1] or 0))
    if big:
        log("\n8. INTERNAL-POINT WARNING: %d large places reading high." % len(big))
        log("   The internal point of a place that annexed mountains is up the")
        log("   mountain, so this is the elevation of the coordinate, not of")
        log("   downtown. Nothing was adjusted. Top 10 by elevation:")
        for area, v, p in big[:10]:
            log("   %8.1f m  %-26s %-2s  land area %8.1f km2"
                % (v, p["name"][:26], p["state"], area))


def main():
    do_epqs = "--epqs" in sys.argv
    places = json.load(open(PLACES))
    log("read %s: %d places" % (PLACES, len(places)))

    if "--report" in sys.argv and os.path.exists(OUT):
        report(places, json.load(open(OUT)), None, do_epqs)
        return

    out, src = build(places)
    if out is None:
        sys.exit(1)

    if len(out) != len(places):
        raise RuntimeError("key count %d != place count %d (duplicate geoid?)"
                           % (len(out), len(places)))
    lz_in = sum(1 for p in places if p["geoid"].startswith("0"))
    lz_out = sum(1 for g in out if g.startswith("0"))
    if lz_in != lz_out:
        raise RuntimeError("leading-zero geoids %d in but %d out - keys corrupted"
                           % (lz_in, lz_out))

    # Final write is just the last checkpoint; re-read from disk so the report
    # describes the shipped file, not what is in memory.
    tmp = OUT + ".tmp"
    with open(tmp, "w") as f:
        json.dump(out, f, separators=(",", ":"), sort_keys=True)
    os.replace(tmp, OUT)
    log("\nwrote %s  (%d keys, %.0f KB)" % (OUT, len(out), os.path.getsize(OUT) / 1024.0))

    shipped = json.load(open(OUT))
    if shipped != out:
        raise RuntimeError("round-trip mismatch: written file differs from computed values")
    report(places, shipped, src, do_epqs)


if __name__ == "__main__":
    main()
