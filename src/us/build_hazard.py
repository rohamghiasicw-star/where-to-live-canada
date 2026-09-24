"""build_hazard.py - natural hazard risk per US place, from FEMA's National Risk Index.

Published at county level, so every place inherits its county's figure. That is
stated in the hint rather than hidden: a county is a big thing, and two towns at
opposite ends of one share a number.

The app asks WHICH hazard rather than using FEMA's composite. The composite is
expected annual loss weighted by social vulnerability and community resilience,
so it partly measures how much there is to lose - Los Angeles County scores 100
in large part because it is Los Angeles. The per-hazard scores answer the
question a person actually has, which is "I do not want to live where it burns".

Column note: riverine flood is RFLD_RISKS. Checked against the real header.

Source: FEMA NRI, via the ArcGIS Hub CSV (hazards.fema.gov was unreachable).
Writes data/us/hazard.json keyed by the 7-digit place GEOID.
"""
import csv, json, os, sys

csv.field_size_limit(sys.maxsize)
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SRC = os.path.join(os.environ.get("WUB_SCRATCH", "/tmp"), "fema_county.csv")

HAZ = {"wildfire": "WFIR_RISKS", "hurricane": "HRCN_RISKS", "tornado": "TRND_RISKS",
       "flood": "RFLD_RISKS", "coastal": "CFLD_RISKS", "quake": "ERQK_RISKS",
       "any": "RISK_SCORE"}


def main():
    rows = {}
    with open(SRC, newline="", encoding="utf-8-sig") as f:
        for r in csv.DictReader(f):
            fips = (r.get("STCOFIPS") or "").strip()
            if len(fips) != 5:
                continue
            rec = {}
            for k, col in HAZ.items():
                v = (r.get(col) or "").strip()
                if v:
                    try:
                        rec[k] = round(float(v), 1)
                    except ValueError:
                        pass
            if rec:
                rows[fips] = rec
    print("counties with risk scores: %d" % len(rows))

    xwalk = json.load(open(os.path.join(ROOT, "data", "us", "place_county.json")))
    places = json.load(open(os.path.join(ROOT, "data", "us", "places.json")))
    out, miss = {}, 0
    for p in places:
        c = xwalk.get(p["geoid"])
        rec = rows.get(c["county"]) if c else None
        if rec:
            out[p["geoid"]] = rec
        else:
            miss += 1
    dest = os.path.join(ROOT, "data", "us", "hazard.json")
    with open(dest, "w") as f:
        json.dump(out, f)
    print("wrote %s (%d places, %d unmatched)" % (dest, len(out), miss))
    print("joins %d/%d (%.1f%%)" % (len(out), len(places), 100 * len(out) / len(places)))

    by = {p["geoid"]: p for p in places}
    for k in ("wildfire", "hurricane", "tornado", "flood"):
        best = sorted((v[k], by[g]["name"], by[g]["state"]) for g, v in out.items()
                      if k in v and by[g].get("pop", 0) > 50000)[:2]
        worst = sorted(((v[k], by[g]["name"], by[g]["state"]) for g, v in out.items()
                        if k in v), reverse=True)[:2]
        print("  %-9s safest: %-22s worst: %s" % (
            k, "%s %s (%.0f)" % (best[0][1], best[0][2], best[0][0]) if best else "-",
            "%s %s (%.0f)" % (worst[0][1], worst[0][2], worst[0][0]) if worst else "-"))


if __name__ == "__main__":
    main()
