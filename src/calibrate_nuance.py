"""calibrate_nuance.py - pick the saturation point for each new OSM dimension
from the real distribution instead of guessing it.

A question like "somewhere good for a dog" scores sqrt(n / SAT). Set SAT too low
and every mid-size town ties at 1.0, which answers "is there one" but cannot
tell you where the best one is. Set it too high and only the largest metro ever
clears 0.5. The 90th percentile of places that have ANY of the thing is the
point where the curve still grades the top decile apart.

Run after build_osm.py / us/build_osm.py. Prints a table; the constants go into
app/app.js by hand so the numbers in the file stay readable and reviewable.
"""
import json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIELDS = ["dog_parks", "vets", "arts_venues", "local_food", "learning",
          "health_facilities", "volunteer_orgs"]


def pct(xs, q):
    if not xs:
        return None
    xs = sorted(xs)
    i = (len(xs) - 1) * q
    lo, hi = int(i), min(int(i) + 1, len(xs) - 1)
    return xs[lo] + (xs[hi] - xs[lo]) * (i - lo)


def report(path, label):
    if not os.path.exists(path):
        print("%s: MISSING (%s)" % (label, path))
        return
    rows = json.load(open(path))
    print("\n== %s  (%d places) ==" % (label, len(rows)))
    print("%-18s %6s %6s %6s %6s %6s %6s" % ("field", "have", "p50", "p75", "p90", "p99", "max"))
    for f in FIELDS:
        vals = [r[f] for r in rows if r.get(f) is not None]
        if not vals:
            print("%-18s %6s  -- NO DATA, dimension must be cut --" % (f, 0))
            continue
        nz = [v for v in vals if v > 0]
        print("%-18s %5d%% %6.0f %6.0f %6.0f %6.0f %6d" % (
            f, round(100 * len(nz) / len(vals)), pct(vals, .50), pct(vals, .75),
            pct(vals, .90), pct(vals, .99), max(vals)))
    print("  'have' = share of places with at least one. Under ~40%% the question")
    print("  mostly returns zero and is not worth offering as a tile.")


if __name__ == "__main__":
    report(os.path.join(ROOT, "data", "osm.json"), "CANADA")
    report(os.path.join(ROOT, "data", "us", "osm.json"), "USA")
