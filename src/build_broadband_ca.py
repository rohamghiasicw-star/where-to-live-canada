"""build_broadband_ca.py - share of dwellings that can get real internet, per CSD.

Source: CRTC Communications Monitoring Report, Table 9 ("Broadband and mobile
service availability, by CSD and year"). Open Government Licence, free, no key.

Three traps, all paid for in the source verification:
  - The file is cp1252, and the header is on line 5. Lines 1-4 are a banner.
  - The table's own title says "by CSD and year" but the surrounding CRTC page
    says "by CMA". The geography really is CSD - the ID column is 7 digits and
    matches the census subdivision codes exactly.
  - Values are DWELLING COUNTS, not percentages, and each CSD is split across
    rural/urban and OLMC rows. Sum the splits, then divide by the CSD's own
    'AllDemographics' row for the same year.

Rank on Gigabit, not 50/10: 50/10 is saturated across Canada and separates
almost nothing, while Gigabit still reads 0% in Yellowknife, Whitehorse and
Dawson, which is the honest answer to "can I actually work from here".

Writes data/broadband_ca.json keyed by name+prov.
"""
import csv, io, json, os, sys, zipfile

csv.field_size_limit(sys.maxsize)
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ZIP = os.path.join(os.environ.get("WUB_SCRATCH", "/tmp"), "crtc.zip")
INNER = "C-T9.csv"
TIERS = ("Gigabit", "100+", "50/10/U", "AllDemographics")
I_CSD, I_TIER, I_YEAR, I_DWELL = 2, 6, 7, 8


def main():
    tot = {}          # (code, year, tier) -> dwellings
    years = set()
    with zipfile.ZipFile(ZIP) as z, z.open(INNER) as fh:
        txt = io.TextIOWrapper(fh, encoding="cp1252", errors="replace")
        for _ in range(4):
            txt.readline()          # banner
        r = csv.reader(txt)
        next(r)                     # header, line 5
        for row in r:
            if len(row) <= I_DWELL:
                continue
            tier = row[I_TIER]
            if tier not in TIERS:
                continue
            try:
                d = float(row[I_DWELL])
                yr = int(row[I_YEAR])
            except ValueError:
                continue
            years.add(yr)
            k = (row[I_CSD], yr, tier)
            tot[k] = tot.get(k, 0.0) + d      # sum the rural/urban/OLMC splits
    yr = max(years)
    print("years present: %d-%d, using %d" % (min(years), max(years), yr))

    code2place = {r["code"]: (r["name"], r["prov"])
                  for r in json.load(open(os.path.join(ROOT, "data", "census.json")))}
    out = []
    for code, (nm, prov) in code2place.items():
        base = tot.get((code, yr, "AllDemographics"))
        if not base:
            continue
        rec = {"name": nm, "prov": prov}
        for tier, key in (("Gigabit", "gigabit_pct"), ("100+", "fast_pct"),
                          ("50/10/U", "basic_pct")):
            v = tot.get((code, yr, tier))
            if v is not None:
                rec[key] = round(min(v / base, 1.0) * 100, 1)
        if "gigabit_pct" in rec:
            out.append(rec)

    dest = os.path.join(ROOT, "data", "broadband_ca.json")
    with open(dest, "w") as f:
        json.dump(out, f)
    print("wrote %s (%d places)" % (dest, len(out)))

    places = json.load(open(os.path.join(ROOT, "data", "climate.json")))
    have = {(r["name"], r["prov"]): r for r in out}
    hit = [p for p in places if (p["name"], p["prov"]) in have]
    print("joins %d/%d of the app's places (%.1f%%)" % (len(hit), len(places),
                                                        100 * len(hit) / len(places)))
    g = sorted(have[(p["name"], p["prov"])]["gigabit_pct"] for p in hit)
    if g:
        q = lambda f: g[int((len(g) - 1) * f)]
        print("  gigabit %% across the app's places: p10 %.1f  p25 %.1f  median %.1f  p90 %.1f"
              % (q(.10), q(.25), q(.50), q(.90)))
        print("  places at exactly 100%%: %d of %d" % (sum(1 for x in g if x >= 100), len(g)))
        worst = sorted(hit, key=lambda p: have[(p["name"], p["prov"])]["gigabit_pct"])[:5]
        for p in worst:
            print("    %-18s %s  gigabit %.1f%%" % (p["name"], p["prov"],
                  have[(p["name"], p["prov"])]["gigabit_pct"]))


if __name__ == "__main__":
    main()
