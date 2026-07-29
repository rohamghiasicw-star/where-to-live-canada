#!/usr/bin/env python3
"""
src/us/build_proximity.py - nearest big city, by road, for every place in
data/us/places.json. Writes data/us/proximity.json.

Same job as src/build_proximity.py does for Canada, re-cut for the US and
hardened for 4,197 places instead of 129: batched table requests, a disk cache
so a restart never redoes work, polite throttling, exponential backoff, and a
ferry audit.

Per place:
  nearest_big_city         name of the nearest place in places.json with
                           pop > 300,000 (69 of them). "Nearest" means shortest
                           real driving time; where nothing is drivable it means
                           shortest straight line, and the row is flagged.
  nearest_big_city_state   its state, because the name alone repeats
                           (Columbus, Kansas City, Portland, Arlington)
  km_to_big_city           STRAIGHT-LINE distance to that city, WGS84 geodesic
                           (pyproj Geod.inv). Not the road distance.
  drive_min_to_big_city    real routed driving time, minutes. null when no
                           road route exists.
  routed                   true only when the number came from an actual OSRM
                           routing response. false means no road route was
                           found and drive_min_to_big_city is null.
  note                     present only on rows where routed is false, saying
                           why.

A place that is itself over 300,000 gets itself: distance 0, drive 0, exactly
as the Canadian build does.

ROUTING - OSRM public demo server, OpenStreetMap road data
  http://router.project-osrm.org/table/v1/driving/...   (the batch pass)
  http://router.project-osrm.org/route/v1/driving/...   (the ferry audit)
  Attribution: OpenStreetMap contributors, ODbL. Project OSRM demo server.

PASS 1 - table
  One /table request per BATCH sources against all 69 anchors as destinations,
  annotations=duration,distance. The demo server accepts 189 coordinates in a
  request, verified. 42 requests covers the whole country. Each response is
  cached to disk under its own key, so re-running is free.

PASS 2 - ferry audit
  OSRM's car profile routes over vehicle ferries, and the demo server does not
  accept exclude=ferry ("Exclude flag combination is not supported"). So a
  Juneau -> Seattle "drive" comes back as 2,945 min because it rides the Alaska
  Marine Highway out of Juneau, and Nantucket -> Boston rides the Hyannis boat.
  That is not a drive. Every route the audit touches is re-requested through
  /route with steps=true, and any leg whose mode is "ferry" disqualifies that
  anchor; the next-nearest anchor is tried, up to FERRY_TRIES of them. If they
  all need a boat the row goes routed=false with drive_min_to_big_city null.

  The audit runs on every Alaska and Hawaii place, plus any place whose pass-1
  route is slow enough for a ferry hop to be hiding in it
  (implied speed < AUDIT_SPEED_KMH over at least AUDIT_MIN_KM of road).

Nothing is estimated. A drive time is either a real OSRM response or null.

Usage:  /tmp/uswater_venv/bin/python src/us/build_proximity.py
Env:    US_PROX_CACHE   request cache dir (default <tmpdir>/us_proximity_cache)
"""

import hashlib
import json
import os
import sys
import tempfile
import time
import urllib.error
import urllib.request

from pyproj import Geod

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PLACES_PATH = os.path.join(REPO, "data", "us", "places.json")
OUT_PATH = os.path.join(REPO, "data", "us", "proximity.json")

CACHE = os.environ.get("US_PROX_CACHE") or os.path.join(
    tempfile.gettempdir(), "us_proximity_cache"
)

OSRM = "http://router.project-osrm.org"
BIG_CITY_POP = 300000
TERRITORIES = {"PR", "VI", "GU", "AS", "MP"}

BATCH = 100          # sources per table request (+69 destinations = 169 coords)
SLEEP = 1.1          # polite gap between requests
RETRIES = 6
TIMEOUT = 240

FERRY_TRIES = 6      # anchors to try before giving up on a ferry-locked place
AUDIT_SPEED_KMH = 45.0
AUDIT_MIN_KM = 25.0

GEOD = Geod(ellps="WGS84")


# --------------------------------------------------------------------------
# cached, throttled, retrying GET
# --------------------------------------------------------------------------

_last = [0.0]


def get_json(url, label=""):
    os.makedirs(CACHE, exist_ok=True)
    key = hashlib.sha1(url.encode()).hexdigest()[:24]
    path = os.path.join(CACHE, key + ".json")
    if os.path.exists(path):
        with open(path) as f:
            return json.load(f), True

    delay = 2.0
    for attempt in range(RETRIES):
        gap = SLEEP - (time.time() - _last[0])
        if gap > 0:
            time.sleep(gap)
        _last[0] = time.time()
        try:
            with urllib.request.urlopen(url, timeout=TIMEOUT) as r:
                d = json.load(r)
        except urllib.error.HTTPError as e:
            body = {}
            try:
                body = json.load(e)
            except Exception:
                pass
            if e.code == 400 and body.get("code") in ("NoRoute", "NoSegment"):
                d = body                      # a real answer, cache it
            else:
                sys.stderr.write("  HTTP %d %s %s (attempt %d)\n"
                                 % (e.code, label, body.get("code", ""),
                                    attempt + 1))
                time.sleep(delay)
                delay = min(delay * 2, 90)
                continue
        except Exception as e:
            sys.stderr.write("  %s %s (attempt %d)\n"
                             % (type(e).__name__, label, attempt + 1))
            time.sleep(delay)
            delay = min(delay * 2, 90)
            continue
        with open(path, "w") as f:
            json.dump(d, f)
        return d, False
    return None, False


def table(srcs, dsts, label=""):
    coords = ";".join("%.5f,%.5f" % (lo, la) for la, lo in srcs + dsts)
    si = ";".join(str(i) for i in range(len(srcs)))
    di = ";".join(str(i + len(srcs)) for i in range(len(dsts)))
    url = ("%s/table/v1/driving/%s?sources=%s&destinations=%s"
           "&annotations=duration,distance" % (OSRM, coords, si, di))
    return get_json(url, label)


def route_steps(a, b, label=""):
    url = ("%s/route/v1/driving/%.5f,%.5f;%.5f,%.5f?steps=true&overview=false"
           % (OSRM, a[1], a[0], b[1], b[0]))
    return get_json(url, label)


def straight_km(a, b):
    return GEOD.inv(a[1], a[0], b[1], b[0])[2] / 1000.0


# --------------------------------------------------------------------------
# main
# --------------------------------------------------------------------------

CHECKS = [("Trenton", "NJ"), ("Riverside", "CA"), ("Anchorage", "AK"),
          ("Urban Honolulu", "HI"), ("Juneau", "AK"), ("Fairbanks", "AK"),
          ("Hilo", "HI"), ("Pearl City", "HI"), ("Nantucket", "MA"),
          ("Bainbridge Island", "WA"), ("Key West", "FL"),
          ("Bismarck", "ND"), ("Ely", "NV"), ("New York", "NY")]


def main():
    with open(PLACES_PATH) as f:
        raw = json.load(f)
    places = [p for p in raw if p["state"] not in TERRITORIES]
    anchors = [p for p in places if p["pop"] > BIG_CITY_POP]
    anchor_geoids = set(p["geoid"] for p in anchors)
    A = [(p["lat"], p["lon"]) for p in anchors]
    sys.stderr.write("places: %d of %d rows (%d territory rows skipped)\n"
                     % (len(places), len(raw), len(raw) - len(places)))
    sys.stderr.write("anchors (pop > %d): %d\n" % (BIG_CITY_POP, len(anchors)))

    # ---- pass 1: table batches -------------------------------------------
    rows = [None] * len(places)
    hits = 0
    for i in range(0, len(places), BATCH):
        chunk = places[i:i + BATCH]
        S = [(p["lat"], p["lon"]) for p in chunk]
        d, cached = table(S, A, "table %d" % i)
        hits += 1 if cached else 0
        dur = dis = None
        if d and d.get("code") == "Ok":
            dur, dis = d.get("durations"), d.get("distances")
        else:
            sys.stderr.write("  batch %d unusable: %s\n"
                             % (i, (d or {}).get("code")))
        for j, p in enumerate(chunk):
            cand = []
            if dur:
                for k in range(len(A)):
                    if dur[j][k] is not None:
                        cand.append((dur[j][k], dis[j][k], k))
                cand.sort()
            rows[i + j] = cand
        sys.stderr.write("  table %d/%d\n" % (min(i + BATCH, len(places)),
                                              len(places)))
    sys.stderr.write("table pass done (%d/%d batches from cache)\n"
                     % (hits, (len(places) + BATCH - 1) // BATCH))

    # ---- pass 2: who needs a ferry audit ---------------------------------
    audit = []
    for n, p in enumerate(places):
        if p["geoid"] in anchor_geoids:
            continue
        if p["state"] in ("AK", "HI"):
            audit.append(n)
            continue
        c = rows[n]
        if not c:
            continue
        sec, m, _ = c[0]
        km = m / 1000.0
        if sec > 0 and km >= AUDIT_MIN_KM and km / (sec / 3600.0) < AUDIT_SPEED_KMH:
            audit.append(n)
    sys.stderr.write("ferry audit candidates: %d\n" % len(audit))

    ferry_fix = {}
    for c, n in enumerate(audit):
        p = places[n]
        chosen = None
        for sec, m, k in rows[n][:FERRY_TRIES]:
            d, _ = route_steps((p["lat"], p["lon"]), A[k],
                               "route %s->%s" % (p["name"],
                                                 anchors[k]["name"]))
            if not d or d.get("code") != "Ok" or not d.get("routes"):
                continue
            r = d["routes"][0]
            modes = set(s.get("mode") for leg in r["legs"]
                        for s in leg["steps"])
            if "ferry" in modes:
                continue
            chosen = (k, r["duration"], r["distance"])
            break
        ferry_fix[n] = chosen
        if (c + 1) % 25 == 0:
            sys.stderr.write("  audit %d/%d\n" % (c + 1, len(audit)))

    # ---- assemble --------------------------------------------------------
    out = []
    n_self = n_routed = n_est = 0
    for n, p in enumerate(places):
        rec = {
            "geoid": p["geoid"],
            "name": p["name"],
            "state": p["state"],
            "nearest_big_city": None,
            "nearest_big_city_state": None,
            "km_to_big_city": None,
            "drive_min_to_big_city": None,
            "routed": False,
        }
        here = (p["lat"], p["lon"])

        if p["geoid"] in anchor_geoids:
            rec.update({"nearest_big_city": p["name"],
                        "nearest_big_city_state": p["state"],
                        "km_to_big_city": 0.0,
                        "drive_min_to_big_city": 0.0,
                        "routed": True})
            n_self += 1
            out.append(rec)
            continue

        pick = None
        if n in ferry_fix:
            if ferry_fix[n] is not None:
                k, sec, _m = ferry_fix[n]
                pick = (k, sec)
        elif rows[n]:
            sec, _m, k = rows[n][0]
            pick = (k, sec)

        if pick is not None:
            k, sec = pick
            a = anchors[k]
            rec.update({"nearest_big_city": a["name"],
                        "nearest_big_city_state": a["state"],
                        "km_to_big_city": round(straight_km(here, A[k]), 1),
                        "drive_min_to_big_city": round(sec / 60.0, 1),
                        "routed": True})
            n_routed += 1
        else:
            k = min(range(len(A)), key=lambda k: straight_km(here, A[k]))
            a = anchors[k]
            why = ("no road route to any US city over 300,000 (nearest one "
                   "reachable only by vehicle ferry or air); straight-line "
                   "distance only"
                   if n in ferry_fix else
                   "OSRM found no road route to any US city over 300,000; "
                   "straight-line distance only")
            rec.update({"nearest_big_city": a["name"],
                        "nearest_big_city_state": a["state"],
                        "km_to_big_city": round(straight_km(here, A[k]), 1),
                        "drive_min_to_big_city": None,
                        "routed": False,
                        "note": why})
            n_est += 1
        out.append(rec)

    with open(OUT_PATH, "w") as f:
        json.dump(out, f, indent=1)
        f.write("\n")

    # ---- report ----------------------------------------------------------
    by = {}
    for r in out:
        by.setdefault((r["name"], r["state"]), r)
    hdr = "%-20s %-3s  %-22s %10s %12s %8s"
    print("")
    print(hdr % ("PLACE", "ST", "NEAREST_BIG_CITY", "KM (line)",
                 "DRIVE_MIN", "ROUTED"))
    print("-" * 84)
    for key in CHECKS:
        r = by.get(key)
        if not r:
            print("%-20s %-3s   not in places.json" % key)
            continue
        print(hdr % (r["name"], r["state"],
                     "%s, %s" % (r["nearest_big_city"],
                                 r["nearest_big_city_state"]),
                     r["km_to_big_city"], r["drive_min_to_big_city"],
                     r["routed"]))
    print("")
    print("rows written:        %d" % len(out))
    print("is itself a big city: %d (distance 0, drive 0)" % n_self)
    print("routed on real roads: %d" % n_routed)
    print("no road route (drive null, straight-line km only): %d" % n_est)
    print("drive_min null:       %d"
          % sum(1 for r in out if r["drive_min_to_big_city"] is None))
    print("")
    print("rows with no road route, by state:")
    st = {}
    for r in out:
        if not r["routed"]:
            st[r["state"]] = st.get(r["state"], 0) + 1
    for k in sorted(st, key=lambda k: -st[k]):
        print("   %-3s %d" % (k, st[k]))
    print("")
    print("wrote %s (%.0f KB)"
          % (OUT_PATH, os.path.getsize(OUT_PATH) / 1024.0))


if __name__ == "__main__":
    main()
