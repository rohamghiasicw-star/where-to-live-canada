"""build_ski.py - distance from every place to the nearest real ski hill.

Doug asked for "outdoor activities (hiking bicycling proximity to skiing etc)".
Skiing is the one of the three with a clean, current, both-country source.

Source: OpenSkiMap ski_areas.csv, rebuilt daily from OpenStreetMap, ODbL.
Filtered to status=operating AND has_downhill=yes AND lift_count>=1, which
gives 526 US and 236 Canadian areas. The lift filter is what removes tubing
hills and abandoned rope tows; the National Ski Areas Association's own count
is 492 US, so 526 is 7% above a figure that excludes the smallest hills - the
right direction and the right order of magnitude.

DISTANCE IS STRAIGHT LINE, not drive time, and the app says so. A mountain
range between you and the hill makes straight-line optimistic, and the routing
this repo uses elsewhere is a public demo server that should not be asked for
4,197 places. Same honesty the water dimension already uses.

Writes data/us/ski.json and data/ski.json, keyed by name+prov.
"""
import csv, json, math, os, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = "https://tiles.openskimap.org/csv/ski_areas.csv"
CACHE = "/tmp/openskimap_ski_areas.csv"
MIN_VERT = 150      # metres. Below this it is a bump, not a day out.


def hav(a1, o1, a2, o2):
    R = 6371.0
    p1, p2 = math.radians(a1), math.radians(a2)
    dp, dl = math.radians(a2 - a1), math.radians(o2 - o1)
    h = math.sin(dp/2)**2 + math.cos(p1)*math.cos(p2)*math.sin(dl/2)**2
    return 2 * R * math.asin(math.sqrt(h))


def load_areas():
    if not os.path.exists(CACHE):
        # the host 403s a bare urllib request; it wants a User-Agent
        req = urllib.request.Request(SRC, headers={"User-Agent": "where-u-belong/1.0"})
        with urllib.request.urlopen(req, timeout=120) as r, open(CACHE, "wb") as f:
            f.write(r.read())
    rows = list(csv.DictReader(open(CACHE, encoding="utf-8")))
    out = {"US": [], "CA": []}
    for x in rows:
        if x["status"] != "operating" or x["has_downhill"] != "yes":
            continue
        try:
            if int(x["lift_count"] or 0) < 1:
                continue
            lat, lon = float(x["lat"]), float(x["lng"])
        except (ValueError, TypeError):
            continue
        cc = "US" if "United States" in x["countries"] else (
             "CA" if "Canada" in x["countries"] else None)
        if not cc:
            continue
        try:
            vert = int(x["vertical_m"] or 0)
        except ValueError:
            vert = 0
        out[cc].append({"name": x["name"] or "unnamed", "lat": lat, "lon": lon,
                        "vert": vert, "lifts": int(x["lift_count"] or 0)})
    print("operating lift-served downhill areas: US %d, CA %d"
          % (len(out["US"]), len(out["CA"])))
    return out


def build(places, areas, key_prov, dest):
    big = [a for a in areas if a["vert"] >= MIN_VERT]
    rows = []
    for p in places:
        lat, lon = p.get("lat"), p.get("lon")
        if lat is None or lon is None:
            continue
        best = min(areas, key=lambda a: hav(lat, lon, a["lat"], a["lon"]), default=None)
        if not best:
            continue
        d = hav(lat, lon, best["lat"], best["lon"])
        bb = min(big, key=lambda a: hav(lat, lon, a["lat"], a["lon"]), default=None)
        rows.append({
            "name": p["name"], "prov": p[key_prov],
            "km_to_ski": round(d, 1),
            "nearest_ski": best["name"],
            "nearest_ski_vert": best["vert"] or None,
            "km_to_big_ski": round(hav(lat, lon, bb["lat"], bb["lon"]), 1) if bb else None,
        })
    with open(dest, "w") as f:
        json.dump(rows, f)
    near = sum(1 for r in rows if r["km_to_ski"] <= 100)
    print("wrote %s  (%d places, %d within 100km of a hill)" % (dest, len(rows), near))
    for r in sorted(rows, key=lambda r: r["km_to_ski"])[:3]:
        print("   closest: %-22s %5.1f km to %s" % (r["name"], r["km_to_ski"], r["nearest_ski"]))
    for r in sorted(rows, key=lambda r: -r["km_to_ski"])[:2]:
        print("   furthest: %-21s %5.1f km" % (r["name"], r["km_to_ski"]))
    return rows


if __name__ == "__main__":
    A = load_areas()
    us = json.load(open(os.path.join(ROOT, "data", "us", "places.json")))
    build(us, A["US"], "state", os.path.join(ROOT, "data", "us", "ski.json"))
    ca = json.load(open(os.path.join(ROOT, "data", "climate.json")))
    build(ca, A["CA"], "prov", os.path.join(ROOT, "data", "ski.json"))
