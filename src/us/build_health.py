"""build_health.py - physical inactivity per US place, from CDC PLACES.

Doug asked for a "healthier lifestyle" dimension and named his own test:
San Diego versus Kansas City. This is the measure that answers it.

ONE measure, named, not a blended health score. That is CDC's own instruction:
"the data should not be used for ranking the overall health of counties,
cities, or census tracts" but individual measures "can be compared". So the app
ranks on Physical Inactivity (LPA) alone and says so on the question.

These are MODELLED estimates - multilevel regression with poststratification off
BRFSS 2023. Nobody surveyed Priceville, Alabama; CDC predicts its prevalence
from its demographics. The hint says so, because a modelled number presented as
a measured one is the kind of thing this app exists not to do.

Pennsylvania and Kentucky are entirely absent from the 2025 release - KY and PA
"were unable to collect enough data to meet the minimum requirements" for BRFSS
2023 - so both states are backfilled from the 2024 release and the year is
recorded per place rather than assumed.

Writes data/us/health.json. Public domain, no key.
"""
import csv, json, os, sys, urllib.parse, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BASE = "https://data.cdc.gov/resource/%s.csv"
CUR, PRIOR = "eav7-hnsx", "sd8v-uq83"      # 2025 release, 2024 release
UA = "where-u-belong/1.0 (research build)"


def pull(ds, where):
    q = urllib.parse.urlencode({
        "$select": "locationid,stateabbr,locationname,measureid,data_value",
        "$where": where, "$limit": "50000"})
    url = (BASE % ds) + "?" + q
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=180) as r:
        rows = list(csv.DictReader(line.decode("utf-8") for line in r))
    print("  %s: %d rows" % (ds, len(rows)))
    return rows


def main():
    print("CDC PLACES, physical inactivity (LPA), crude prevalence")
    cur = pull(CUR, "datavaluetypeid='CrdPrv' AND measureid='LPA'")
    back = pull(PRIOR, "datavaluetypeid='CrdPrv' AND measureid='LPA' "
                       "AND stateabbr in('PA','KY')")

    out = {}
    for r in cur:
        v = (r.get("data_value") or "").strip()
        if v:
            out[r["locationid"]] = {"inactive_pct": float(v), "release": 2025}
    n_cur = len(out)
    filled = 0
    for r in back:
        gid, v = r["locationid"], (r.get("data_value") or "").strip()
        if v and gid not in out:
            out[gid] = {"inactive_pct": float(v), "release": 2024}
            filled += 1
    print("  2025 release: %d places" % n_cur)
    print("  PA/KY backfilled from 2024: %d places" % filled)

    # Report the join against the app's own place list rather than assuming it.
    pl = json.load(open(os.path.join(ROOT, "data", "us", "places.json")))
    hit = sum(1 for p in pl if p["geoid"] in out)
    print("  joins %d/%d of the app's places (%.1f%%)" % (hit, len(pl), 100 * hit / len(pl)))
    miss_states = {}
    for p in pl:
        if p["geoid"] not in out:
            miss_states[p["state"]] = miss_states.get(p["state"], 0) + 1
    if miss_states:
        print("  unmatched by state: %s" % dict(sorted(
            miss_states.items(), key=lambda kv: -kv[1])[:8]))

    dest = os.path.join(ROOT, "data", "us", "health.json")
    with open(dest, "w") as f:
        json.dump(out, f)
    print("wrote %s  (%d places)" % (dest, len(out)))


if __name__ == "__main__":
    main()
