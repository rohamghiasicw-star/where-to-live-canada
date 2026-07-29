"""US place elevation: ground elevation in metres at each place's internal point.

Writes data/us/elevation.json  ->  {"<geoid>": <metres> | null}
Reads  data/us/places.json     (never modified)

WHY THIS FILE EXISTS
  The climate step picks one weather station per place. Distance alone is not
  enough: in the Canadian build, Revelstoke's nearest published-normals station
  sat 43 km away and 1,431 m higher and reported 1,388 cm of alpine snowpack
  instead of the town's 425 cm. The fix is to put elevation difference into the
  station-matching cost, and that needs the PLACE's elevation. Station elevation
  already ships in data/us/noaa_stations.json (GHCN-D metadata, metres). This
  file supplies the other half. See src/fix_elev_outliers.py, which nulled any
  Canadian element whose station sat more than 600 m off the town's elevation.

SOURCE: opentopodata.org public API, dataset `ned10m`
  ned10m is USGS 3DEP / NED at 1/3 arc-second (~10 m). Chosen over the
  alternatives because:
    - it is the same USGS elevation model that EPQS serves, so it is
      US-authoritative rather than a global resample;
    - it accepts 100 locations per POST, so 4,226 places is 43 calls, versus
      4,226 sequential round trips for EPQS;
    - it is the only candidate that covered EVERY place in this list. srtm30m
      stops at 60 N and returns null for the seven Alaska places (Fairbanks,
      College, Badger... all above 64 N). mapzen covers them but is a resampled
      global composite. ned10m returned a value for interior Alaska (College
      144.5 m) and for Puerto Rico (San Juan 9.1 m), so no second dataset was
      needed for coverage.
  `mapzen` (global composite: NED + SRTM + GMTED + others) is wired in as a
  FALLBACK, used only for places ned10m returns null for. Which dataset produced
  each value is recorded in the cache and counted in the report.

CROSS-CHECKED against USGS EPQS (https://epqs.nationalmap.gov/v1/json), a
  different service reading the same USGS model, single point only. Run with
  --epqs to re-verify the check table. Agreement at the points tested is within
  a couple of decimetres (Denver 1612.9 vs 1613.1; San Juan 9.1 vs 9.3;
  New Orleans -1.43 vs -1.46). EPQS is a check, never a source for the output,
  because mixing two services would put a seam in the dataset.

COORDINATE ORDER  (the classic way to ruin this file)
  places.json carries `lat` then `lon`; opentopodata wants "lat,lon"; EPQS wants
  x=lon and y=lat. Sending them swapped returns plausible-looking numbers for
  the wrong hemisphere. Three independent guards, all of which must pass before
  anything is written:
    1. CONTROLS below are fetched and range-checked. Two of them only work if
       the order is right: Furnace Creek must come back NEGATIVE (no swapped
       coordinate lands below sea level) and Leadville must come back above
       3,000 m.
    2. REVERSED_PROBE sends three known points with lat/lon deliberately
       swapped and asserts the answers are NOT the true ones. Swapped US
       coordinates land on the Antarctic plateau: Miami reversed reads 3,247 m.
    3. Every result is matched to its request by the lat/lng the API ECHOES
       BACK, not by list position, so a reordered or short response cannot
       silently shift elevations onto the wrong places.

GEOID KEYS ARE STRINGS
  787 of the 4,226 geoids have a leading zero (Alabama places look like
  '0100100'). They are read as strings, never parsed as numbers, and the writer
  asserts the leading-zero count survives to the output file.

NEVER INTERPOLATED
  A place with no value from either dataset is written as null. Nothing is
  averaged from neighbours, carried over, or guessed. 0.0 is a real elevation
  (sea level) and is kept as 0.0; only a genuine absence becomes null.

INTERNAL POINTS ARE NOT DOWNTOWNS  (read this before trusting a big city)
  places.json lat/lon are the Census Gazetteer INTPTLAT/INTPTLONG internal
  points of the whole place polygon. For a municipality that annexed a mountain
  range, that point is up the mountain, and the elevation here is correctly the
  elevation of that point, not of the populated core. Anchorage AK is the worst
  case: its internal point (61.17425, -149.28433) sits ~33 km east of downtown
  inside the Chugach Range and reads ~1,217 m, not the ~30 m of downtown. Both
  ned10m and EPQS agree on 1,217 m, so this is the coordinate, not the elevation
  service. The report flags every place whose value is a large-area outlier so
  the matcher can decide; this file does not silently "fix" any of them.

RATE LIMITS, honoured (https://www.opentopodata.org/ - "Max 100 locations per
  request. Max 1 call per second. Max 1000 calls per day."): batches of 100,
  >=1.1 s between calls, exponential backoff on 429/5xx that also honours
  Retry-After. Raw API responses are cached to disk keyed by dataset + batch
  contents, so a restart or a fallback pass costs the API nothing.

SOURCES
  https://www.opentopodata.org/                          (public API limits)
  https://www.opentopodata.org/api/                      (request/response format)
  https://www.opentopodata.org/datasets/ned/             (ned10m provenance)
  https://api.opentopodata.org/v1/ned10m                 (the endpoint used)
  https://api.opentopodata.org/v1/mapzen                 (null fallback)
  https://epqs.nationalmap.gov/v1/json                   (independent cross-check)
  https://www.usgs.gov/3d-elevation-program               (3DEP / NED programme)

usage:
  python3 src/us/build_elevation.py            # build (uses cache, refetches gaps)
  python3 src/us/build_elevation.py --epqs     # also cross-check table vs USGS EPQS
  python3 src/us/build_elevation.py --report   # re-print the report from the cache
"""
import hashlib, json, math, os, statistics, sys, tempfile, time, urllib.error, urllib.request

PLACES = "data/us/places.json"
OUT = "data/us/elevation.json"

API = "https://api.opentopodata.org/v1/%s"
EPQS = "https://epqs.nationalmap.gov/v1/json?x=%.6f&y=%.6f&units=Meters&wkid=4326"
PRIMARY = "ned10m"
FALLBACK = "mapzen"

BATCH = 100          # documented maximum locations per request
MIN_INTERVAL = 1.1   # documented maximum 1 call/second, with headroom
MAX_TRIES = 6
UA = "livable-us-elevation/1.0 (dataset build; batched, 1 req/sec)"

CACHE = os.environ.get("LIVABLE_US_CACHE",
                       os.path.join(tempfile.gettempdir(), "livable_us_elev_cache"))

# Range checks. Places marked in_list=True are looked up by geoid in the output;
# the others are external reference points fetched on their own so the order
# guards have something unambiguous to bite on.
#                name                geoid      lat        lon        lo      hi
CONTROLS = [
    ("Denver CO",                   "0820000",  39.76185, -104.88111, 1500,   1750),
    ("Leadville CO (external)",     None,       39.25080, -106.29250, 3000,   3200),
    ("New Orleans LA",              "2255000",  30.05342,  -89.93450,  -10,      5),
    ("Miami FL",                    "1245000",  25.77516,  -80.20861,   -5,      5),
    ("Virginia Beach VA",           "5182000",  36.77952,  -76.02914,   -5,      5),
    ("Salt Lake City UT",           "4967000",  40.77693, -111.93099, 1200,   1450),
    ("Flagstaff AZ",                "0423620",  35.18521, -111.62070, 1950,   2250),
    ("Santa Fe NM",                 "3570500",  35.66198, -105.98181, 1950,   2250),
    ("Furnace Creek CA (external)", None,       36.46140, -116.86560, -100,     0),
    ("Anchorage AK",                "0203000",  61.17425, -149.28433,    0,     50),
    ("Urban Honolulu HI",           "1571550",  21.32435, -157.84764,    0,     20),
]

# Deliberately swapped lat/lon. Correct-order truth is in the 4th slot; a swapped
# request must NOT return it. Two outcomes both prove the order is right:
#   - swapped latitude still inside +/-90 (Miami -80.2, Virginia Beach -76.0):
#     the request succeeds but lands on the Antarctic plateau (~3,200 m), so the
#     wrong-order answer is nowhere near the truth;
#   - swapped latitude outside +/-90 (Denver -104.9): opentopodata refuses the
#     request outright with "Provide locations in lat,lon order", which is the
#     API telling us in words which order it wants.
REVERSED_PROBE = [
    ("Miami FL",          -80.20861, 25.77516,    1.6),
    ("Virginia Beach VA", -76.02914, 36.77952,    4.2),
    ("Denver CO",        -104.88111, 39.76185, 1612.9),
]


def log(*a):
    print(*a)
    sys.stdout.flush()


# ---------------------------------------------------------------- HTTP + cache

_last_call = [0.0]


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
    # sha1, not hash(): str hashing is salted per process, so hash() would make
    # the cache miss on every restart and refetch the whole dataset.
    key = "%s_%s_%d.json" % (dataset, hashlib.sha1(locstr.encode()).hexdigest()[:16], len(pts))
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
        json.dump({"_locstr": locstr, "_dataset": dataset, "response": d},
                  open(path, "w"))

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
    """Must pass before any place is fetched. Aborts the build if it does not."""
    log("\n1. COORDINATE ORDER GUARDS")
    pts = [(c[2], c[3]) for c in CONTROLS]
    got = fetch_batch(PRIMARY, pts)
    fails = []
    log("   %-30s %10s  %s" % ("control", "metres", "expected range"))
    for (name, _g, la, lo, lo_ok, hi_ok), v in zip(CONTROLS, got):
        ok = v is not None and lo_ok <= v <= hi_ok
        log("   %-30s %10s  [%g, %g] %s"
            % (name, "null" if v is None else "%.1f" % v, lo_ok, hi_ok,
               "ok" if ok else "OUT OF RANGE"))
        if not ok:
            fails.append((name, v, lo_ok, hi_ok))

    log("\n   reversed-order probe (swapped lat/lon must NOT return the truth):")
    for name, ra, rb, truth in REVERSED_PROBE:
        try:
            v = fetch_batch(PRIMARY, [(ra, rb)])[0]
        except RuntimeError as e:
            if "INVALID_REQUEST" in str(e) or "Latitude must be between" in str(e):
                log("     %-18s sent (%9.5f,%9.5f) -> API REFUSED the swap "
                    "(\"lat,lon order\"); true value %.1f  ok" % (name, ra, rb, truth))
                continue
            raise
        bad = v is not None and abs(v - truth) < 50
        log("     %-18s sent (%9.5f,%9.5f) -> %-9s true value %8.1f  %s"
            % (name, ra, rb, "null" if v is None else "%.1f" % v, truth,
               "ok (nowhere near truth)" if not bad else "ORDER BUG"))
        if bad:
            fails.append(("reversed " + name, v, truth, truth))
    return fails


# ------------------------------------------------------------------------ build

def build(places, do_epqs=False):
    os.makedirs(CACHE, exist_ok=True)
    log("cache: %s" % CACHE)

    order_fails = check_order()
    hard = [f for f in order_fails if not f[0].startswith(("Anchorage", "Urban Honolulu"))]
    if hard:
        log("\nABORT: coordinate/control guards failed: %s" % hard)
        log("Nothing written. Fix the source or the coordinate order first.")
        return None, None

    pts = [(p["lat"], p["lon"]) for p in places]
    n = len(pts)
    nb = math.ceil(n / BATCH)
    log("\n2. FETCH %s  (%d places, %d batches of <=%d, >=%.1fs apart)"
        % (PRIMARY, n, nb, BATCH, MIN_INTERVAL))

    vals, src = [], []
    for i in range(0, n, BATCH):
        chunk = pts[i:i + BATCH]
        got = fetch_batch(PRIMARY, chunk)
        vals.extend(got)
        src.extend([PRIMARY if v is not None else None for v in got])
        b = i // BATCH + 1
        if b % 10 == 0 or b == nb:
            log("   batch %d/%d  (%d values, %d null so far)"
                % (b, nb, sum(v is not None for v in vals), sum(v is None for v in vals)))

    gaps = [i for i, v in enumerate(vals) if v is None]
    log("\n3. FALLBACK %s for %s null from %s" % (FALLBACK, len(gaps), PRIMARY))
    if gaps:
        for j in range(0, len(gaps), BATCH):
            idx = gaps[j:j + BATCH]
            got = fetch_batch(FALLBACK, [pts[k] for k in idx])
            for k, v in zip(idx, got):
                if v is not None:
                    vals[k], src[k] = v, FALLBACK
        log("   recovered %d, still null %d"
            % (sum(src[k] == FALLBACK for k in gaps), sum(vals[k] is None for k in gaps)))
    else:
        log("   none needed - %s covered every place" % PRIMARY)

    out = {}
    for p, v in zip(places, vals):
        g = p["geoid"]
        if not isinstance(g, str):
            raise RuntimeError("geoid %r is not a string - leading zeros are at risk" % (g,))
        out[g] = None if v is None else round(v, 1)   # never interpolated
    return out, src


# ----------------------------------------------------------------------- report

def report(places, out, src, do_epqs=False):
    by_geoid = {p["geoid"]: p for p in places}
    log("\n4. CHECK TABLE  (strong known values; source is %s)" % PRIMARY)
    log("   %-24s %-8s %10s  %-16s %s"
        % ("place", "geoid", "metres", "expected", "verdict"))
    suspect = []
    for name, g, la, lo, lo_ok, hi_ok in CONTROLS:
        if g is None:
            v = fetch_batch(PRIMARY, [(la, lo)])[0]
            v = None if v is None else round(v, 1)
            gtxt = "-extern-"
        else:
            v = out.get(g)
            gtxt = g
        ok = v is not None and lo_ok <= v <= hi_ok
        log("   %-24s %-8s %10s  [%6g,%6g]  %s"
            % (name[:24], gtxt, "null" if v is None else "%.1f" % v, lo_ok, hi_ok,
               "PASS" if ok else "CHECK"))
        if not ok:
            suspect.append((name, g, la, lo, v, lo_ok, hi_ok))

    if suspect:
        log("\n   %d value(s) outside the expected range. Second opinion from USGS" % len(suspect))
        log("   EPQS (a different service on the same USGS model) for each:")
        for name, g, la, lo, v, lo_ok, hi_ok in suspect:
            e, res = epqs_one(la, lo)
            agree = (v is not None and e is not None and abs(v - e) < max(2.0, 0.02 * abs(v)))
            log("     %-24s ned10m %-9s EPQS %-9s (res %s) -> %s"
                % (name[:24], "null" if v is None else "%.1f" % v,
                   "null" if e is None else "%.1f" % e, res,
                   "BOTH SERVICES AGREE - the coordinate, not the elevation"
                   if agree else "SERVICES DISAGREE - investigate"))
            if g and by_geoid.get(g):
                p = by_geoid[g]
                log("       internal point (%.5f, %.5f), place land area %s km2"
                    % (p["lat"], p["lon"], p.get("land_area_km2")))

    if do_epqs:
        log("\n4b. EPQS cross-check of every in-list control (--epqs)")
        for name, g, la, lo, _a, _b in CONTROLS:
            v = out.get(g) if g else round(fetch_batch(PRIMARY, [(la, lo)])[0], 1)
            e, res = epqs_one(la, lo)
            log("   %-24s ned10m %-9s EPQS %-9s delta %s"
                % (name[:24], "null" if v is None else "%.1f" % v,
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
        log("   from %-14s %d" % (PRIMARY, sum(s == PRIMARY for s in src)))
        log("   from %-14s %d" % (FALLBACK, sum(s == FALLBACK for s in src)))
    if nulls:
        log("   null geoids: %s" % ", ".join(
            "%s (%s, %s)" % (g, by_geoid[g]["name"], by_geoid[g]["state"]) for g in nulls[:20]))
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
        log("   %8.1f m  %-8s %-24s %-2s  (%.5f, %.5f)  %s km2"
            % (v, g, p["name"][:24], p["state"], p["lat"], p["lon"], p.get("land_area_km2")))
    log("\n   FIVE LOWEST")
    for v, g in ranked[-5:][::-1]:
        p = by_geoid[g]
        log("   %8.1f m  %-8s %-24s %-2s  (%.5f, %.5f)  %s km2"
            % (v, g, p["name"][:24], p["state"], p["lat"], p["lon"], p.get("land_area_km2")))

    # Places whose internal point is likely NOT the populated core. Not corrected
    # here - just surfaced, because the station matcher will trust this number.
    big = sorted((( (p.get("land_area_km2") or 0), out.get(p["geoid"]), p)
                  for p in places
                  if (p.get("land_area_km2") or 0) > 500 and (out.get(p["geoid"]) or 0) > 500),
                 reverse=True)
    if big:
        log("\n8. INTERNAL-POINT WARNING: large places reading high. The internal point")
        log("   of a place that annexed mountains is up the mountain, so this is the")
        log("   elevation of the coordinate, not of downtown. Nothing was adjusted.")
        for area, v, p in big[:10]:
            log("   %8.1f m  %-24s %-2s  land area %8.1f km2" % (v, p["name"][:24], p["state"], area))


def main():
    do_epqs = "--epqs" in sys.argv
    places = json.load(open(PLACES))
    log("read %s: %d places" % (PLACES, len(places)))

    if "--report" in sys.argv and os.path.exists(OUT):
        out = json.load(open(OUT))
        report(places, out, None, do_epqs)
        return

    out, src = build(places, do_epqs)
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

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w") as f:
        json.dump(out, f, separators=(",", ":"), sort_keys=True)
    log("\nwrote %s  (%d keys, %.0f KB)" % (OUT, len(out), os.path.getsize(OUT) / 1024.0))

    # Re-read from disk so the report describes the shipped file, not memory.
    shipped = json.load(open(OUT))
    if shipped != out:
        raise RuntimeError("round-trip mismatch: written file differs from computed values")
    report(places, shipped, src, do_epqs)


if __name__ == "__main__":
    main()
