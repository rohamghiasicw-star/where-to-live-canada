"""build_quake_ca.py - earthquake risk per Canadian CSD, from NRCan's PSRA.

Canada has no FEMA-style all-hazard index. What it does have, keyed directly to
the census subdivision, is the Probabilistic Seismic Risk Assessment: NRCan's
earthquake risk indicator per CSD. So Canada gets an earthquake question and the
US gets a pick-your-hazard question. Different, because the data is different,
rather than one forced onto the other.

eqri_norm_score_b0 is the normalised baseline risk index. Higher is worse.

Source: NRCan CanadaSRM, psra_indicators_csd.gpkg (a GeoPackage, read here as
plain SQLite - only the attribute table is needed, no geometry).
Writes data/quake_ca.json keyed by name+prov.
"""
import json, os, sqlite3

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(os.environ.get("WUB_SCRATCH", "/tmp"), "psra_indicators_csd.gpkg")
FIELD = "eqri_norm_score_b0"


def main():
    con = sqlite3.connect(SRC)
    raw = {}
    for csduid, score in con.execute(
            'SELECT csduid, %s FROM psra_indicators_csd WHERE %s IS NOT NULL'
            % (FIELD, FIELD)):
        raw[str(csduid)] = float(score)
    print("CSDs with a seismic score: %d" % len(raw))

    code2place = {r["code"]: (r["name"], r["prov"])
                  for r in json.load(open(os.path.join(ROOT, "data", "census.json")))}
    out = []
    for code, (nm, prov) in code2place.items():
        if code in raw:
            out.append({"name": nm, "prov": prov, "quake": round(raw[code], 4)})
    dest = os.path.join(ROOT, "data", "quake_ca.json")
    with open(dest, "w") as f:
        json.dump(out, f)

    places = json.load(open(os.path.join(ROOT, "data", "climate.json")))
    print("wrote %s (%d places)" % (dest, len(out)))
    print("joins %d/%d (%.1f%%)" % (len(out), len(places), 100 * len(out) / len(places)))
    xs = sorted(r["quake"] for r in out)
    if xs:
        q = lambda f: xs[int((len(xs) - 1) * f)]
        print("  score spread: min %.3f  p25 %.3f  median %.3f  p90 %.3f  max %.3f"
              % (xs[0], q(.25), q(.50), q(.90), xs[-1]))
        for r in sorted(out, key=lambda r: -r["quake"])[:3]:
            print("    riskiest: %-20s %s  %.3f" % (r["name"], r["prov"], r["quake"]))
        for r in sorted(out, key=lambda r: r["quake"])[:2]:
            print("    safest:   %-20s %s  %.3f" % (r["name"], r["prov"], r["quake"]))


if __name__ == "__main__":
    main()
