#!/usr/bin/env python3
"""US map geometry for the app sheet: state rings plus the one point transform.

Mirrors src/build_map.py (Canada). That script projects Natural Earth admin-1
boundaries into the projection the country is conventionally drawn in, simplifies
them, and emits raw projected rings as flat coordinate arrays; src/build_app.py
fits and scales them into the canvas. Nothing here is normalised to a view box,
so the same drawing code consumes either country.

Canada needed one projection. The US needs three.

1. Lower 48 + DC: EPSG:5070, NAD83 / Conus Albers (equal-area conic, standard
   parallels 29.5N and 45.5N, central meridian 96W). This is the projection the
   US is conventionally drawn in, the USGS national default.

2. Alaska: EPSG:5070 is defined for the lower 48 and shears Alaska into a
   useless smear, so Alaska is projected on its own in EPSG:3338, NAD83 / Alaska
   Albers (parallels 55N and 65N, central meridian 154W), the official Alaska
   projection, then scaled and translated into an inset.

3. Hawaii: projected on its own in the Hawaii Albers Equal Area Conic
   (parallels 8N and 18N, latitude of origin 13N, central meridian 157W; the
   projection ESRI ships as Hawaii_Albers_Equal_Area_Conic, WKID 102007, and the
   same parameters d3.geoAlbersUsa uses for its Hawaii inset), then translated
   into an inset at true scale.

THE INSET TRANSFORMS, exactly. Both are a uniform scale about the origin of the
inset's own projected plane followed by a translation, in EPSG:5070 metres:

    Alaska   x_5070 = 0.35 * x_3338 + (-1_760_000)
             y_5070 = 0.35 * y_3338 +    175_000
    Hawaii   x_5070 = 1.00 * x_hiaea + (-760_000)
             y_5070 = 1.00 * y_hiaea + (-330_000)

0.35 for Alaska is the conventional inset scale (what d3.geoAlbersUsa uses);
Hawaii is drawn at true scale. The translations drop both insets into the empty
southwest corner of the lower-48 bounding box - the block of plate below
California and west of the Rio Grande that no land occupies - so the insets cost
nothing: the full extent of the output is still exactly the lower-48 extent, and
the app's fit is unchanged by their presence. Any point can be put on the sheet
with project() below, which is the same transform the rings were built with.

Resolution: ne_50m. The sheet is ~4,600 km wide, so at any plausible render
width it is a 1:40M-1:50M map, which is what Natural Earth generalised the 50m
series for. The 10m build was made and compared at these same settings: at this
scale it is visually indistinguishable (the extra vertices only add wiggle to the
Mississippi and Missouri river borders) and costs 137 KB against 78 KB, so 50m is
the honest choice. Switch with NE_LAYER / NE_URL if the sheet ever gets bigger.

Simplification is topology-preserving, not per-state. Simplifying each state on
its own tears shared borders apart, and these rings are drawn as separate filled
paths with a stroke, so a torn border shows up as a double hairline. Instead
every boundary is cut into arcs at the vertices where the set of states touching
it changes, each arc is simplified once with shapely (Douglas-Peucker), and the
rings are rebuilt from the shared arcs. Both sides of a border therefore get
byte-identical geometry. Tolerance scales with the drawn size of the state, so
Texas is generalised hard and Rhode Island, Delaware and DC keep their shape.

Output: data/us/us_rings.json, the same shape as data/canada_rings.json but keyed
        on postal code instead of province name:
            {"proj": "...", "state": {"CA": [[[x,y],...], ...], "TX": [...], ...}}
        x and y are EPSG:5070 metres rounded to the metre (the sheet renders at
        roughly 4.6 km per pixel, so the metre is ~4,000x more precision than the
        canvas can show). Rings are closed and ordered largest first.
        One caveat worth knowing when the dots go on: a coastal point can sit a
        kilometre or two outside its own simplified coastline (Miami is 3 km out).
        That is under a pixel. Places out on dropped islets are further out.

Usage:  python3 src/us/build_map.py
Needs:  pyproj, shapely, pyshp  (same three src/build_water.py uses)
Env:    US_MAP_CACHE  where to download/unpack Natural Earth
                      (default: <tmpdir>/us_map_cache, ~4 MB)

Source: https://naciscdn.org/naturalearth/50m/cultural/ne_50m_admin_1_states_provinces.zip
        Natural Earth 5.1.1, public domain.
"""

import json
import math
import os
import sys
import tempfile
import urllib.request
import zipfile

# --------------------------------------------------------------------------
# config
# --------------------------------------------------------------------------

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT_PATH = os.path.join(REPO, "data", "us", "us_rings.json")

CACHE = os.environ.get("US_MAP_CACHE") or os.path.join(
    tempfile.gettempdir(), "us_map_cache"
)
NE_LAYER = "ne_50m_admin_1_states_provinces"
NE_URL = "https://naciscdn.org/naturalearth/50m/cultural/%s.zip" % NE_LAYER

PROJ_NAME = "albers_conus5070_ak3338_hiaea_insets"

CONUS_EPSG = 5070          # NAD83 / Conus Albers
AK_EPSG = 3338             # NAD83 / Alaska Albers
HI_PROJ4 = ("+proj=aea +lat_0=13 +lon_0=-157 +lat_1=8 +lat_2=18 "
            "+x_0=0 +y_0=0 +datum=NAD83 +units=m +no_defs")

# the inset transforms. see the module docstring.
AK_SCALE, AK_DX, AK_DY = 0.35, -1_760_000.0, 175_000.0
HI_SCALE, HI_DX, HI_DY = 1.00, -760_000.0, -330_000.0

# lon/lat windows applied before projecting, so the insets stay compact:
#  - Alaska keeps everything east of the antimeridian. The far Aleutians past
#    Attu are uninhabited and the 50m series already stops at 178W.
#  - Hawaii keeps the main eight islands and drops the Northwestern Hawaiian
#    Islands, a 2,000 km chain of uninhabited atolls out to Kure. Drawing them
#    would triple the inset's width to show nobody.
AK_WINDOW = (-180.0, 50.0, -128.0, 72.5)
HI_WINDOW = (-161.0, 18.0, -154.0, 23.5)

# Simplification. TOL_K is metres of tolerance per sqrt(km2) of drawn area, so a
# state's generalisation matches its size on the plate; the clamp keeps the
# smallest units legible and stops the biggest from going polygonal.
TOL_K = 4.8
TOL_MIN, TOL_MAX = 200.0, 5000.0
# Drop islands smaller than this *as drawn*, i.e. after the inset scale, so the
# threshold means the same number of pixels everywhere. A state's largest ring is
# never dropped. 30 km2 is a ~5 km speck, about one pixel at the width this sheet
# renders at, and it is deliberately far finer than the Canadian sheet's cutoff
# (~2,400 km2) because the islands it buys back are inhabited and get ranked:
# Nantucket, Martha's Vineyard, the Florida Keys, the San Juans, Kodiak.
MIN_RING_KM2 = 30.0

# Excluded on purpose:
#  - Puerto Rico, Guam, the US Virgin Islands, American Samoa, the Northern
#    Marianas and the minor outlying islands. Natural Earth files them as their
#    own admin-0 units (iso_a2 PR/GU/VI/AS/MP/UM), not as US states, and none of
#    them are in the 50m admin-1 layer at all. Each would need a fourth and
#    fifth inset on the far side of two oceans.
#  - Nothing else. All 50 states and DC are in the output.
US_ISO = "US"


# --------------------------------------------------------------------------
# projection: the one transform the rings and the dots share
# --------------------------------------------------------------------------

_T = {}


def _tf(which):
    """lazily built pyproj transformers, so importing this module is cheap."""
    if not _T:
        from pyproj import CRS, Transformer
        wgs = CRS.from_epsg(4326)
        for k, crs in (("conus", CRS.from_epsg(CONUS_EPSG)),
                       ("AK", CRS.from_epsg(AK_EPSG)),
                       ("HI", CRS.from_proj4(HI_PROJ4))):
            _T[k] = Transformer.from_crs(wgs, crs, always_xy=True).transform
    return _T[which]


def _inside(win, lon, lat):
    return win[0] <= lon <= win[2] and win[1] <= lat <= win[3]


def zone(lon, lat, state=None):
    """'AK', 'HI' or 'conus'. `state` may be a postal code or a state name; when
    it is missing the point's own position decides, so callers without a state
    column still land in the right place."""
    if state:
        u = str(state).strip().upper()
        if u in ("AK", "ALASKA"):
            return "AK"
        if u in ("HI", "HAWAII"):
            return "HI"
        return "conus"
    if _inside(AK_WINDOW, lon, lat):
        return "AK"
    if _inside(HI_WINDOW, lon, lat):
        return "HI"
    return "conus"


def project(lon, lat, state=None):
    """(lon, lat) -> (x, y) in the sheet's EPSG:5070 metres, Alaska and Hawaii
    folded into their insets. This is the transform data/us/us_rings.json was
    built with; place dots must go through it so they land on the geometry."""
    z = zone(lon, lat, state)
    if z == "AK":
        x, y = _tf("AK")(lon, lat)
        return x * AK_SCALE + AK_DX, y * AK_SCALE + AK_DY
    if z == "HI":
        x, y = _tf("HI")(lon, lat)
        return x * HI_SCALE + HI_DX, y * HI_SCALE + HI_DY
    return _tf("conus")(lon, lat)


# --------------------------------------------------------------------------
# source data
# --------------------------------------------------------------------------

def fetch():
    d = os.path.join(CACHE, NE_LAYER)
    shp = os.path.join(d, NE_LAYER + ".shp")
    if os.path.exists(shp):
        return shp
    os.makedirs(CACHE, exist_ok=True)
    z = os.path.join(CACHE, NE_LAYER + ".zip")
    if not os.path.exists(z) or os.path.getsize(z) < 100_000:
        sys.stderr.write("downloading %s\n" % NE_URL)
        urllib.request.urlretrieve(NE_URL, z)
    with zipfile.ZipFile(z) as zf:
        zf.extractall(d)
    return shp


def read_states():
    """postal code -> shapely geometry, projected, windowed. AK and HI arrive
    already scaled and translated into their insets."""
    import shapefile  # pyshp
    from shapely.geometry import shape, box
    from shapely.ops import transform as sh_transform

    def move(g, s, dx, dy):
        return sh_transform(lambda xs, ys: (tuple(v * s + dx for v in xs),
                                            tuple(v * s + dy for v in ys)), g)

    out = {}
    for sr in shapefile.Reader(fetch()).iterShapeRecords():
        rec = sr.record
        if rec["iso_a2"] != US_ISO:
            continue
        st = rec["postal"]
        g = shape(sr.shape.__geo_interface__)
        if st == "AK":
            g = move(sh_transform(_tf("AK"), g.intersection(box(*AK_WINDOW))),
                     AK_SCALE, AK_DX, AK_DY)
        elif st == "HI":
            g = move(sh_transform(_tf("HI"), g.intersection(box(*HI_WINDOW))),
                     HI_SCALE, HI_DX, HI_DY)
        else:
            g = sh_transform(_tf("conus"), g)
        out[st] = (rec["name"], g)
    return out


def exterior_rings(g):
    """largest ring first, small islands dropped, holes ignored. The app draws
    every ring as its own filled path, so an interior ring would be painted over
    anyway; the 50m US states have none."""
    ps = list(g.geoms) if g.geom_type == "MultiPolygon" else [g]
    ps.sort(key=lambda p: -p.area)
    keep = []
    for i, p in enumerate(ps):
        if i and p.area / 1e6 < MIN_RING_KM2:
            continue
        keep.append([tuple(c) for c in p.exterior.coords])
    return keep


# --------------------------------------------------------------------------
# topology-preserving simplification
# --------------------------------------------------------------------------

_Q = 0.01                                   # metres, for vertex identity only
_k = lambda p: (round(p[0] / _Q), round(p[1] / _Q))


def arcs_and_plan(rings):
    """rings: {state: [ring, ...]}. Cut every ring into arcs at the vertices
    where the set of states touching it changes, so a shared border is one arc
    held by both states. -> (raw arcs, {state: [[(arc key, reversed), ...]]})"""
    owners = {}
    for st, rs in rings.items():
        for r in rs:
            for p in r[:-1]:
                owners.setdefault(_k(p), set()).add(st)

    def canon(pts):
        a = tuple(_k(p) for p in pts)
        b = a[::-1]
        return (a, False) if a <= b else (b, True)

    raw, plan = {}, {}
    for st, rs in rings.items():
        plan[st] = []
        for r in rs:
            v = r[:-1]                       # open the cycle
            n = len(v)
            own = [frozenset(owners[_k(p)]) for p in v]
            cuts = [i for i in range(n)
                    if own[i] != own[i - 1] or own[i] != own[(i + 1) % n]]
            segs = []
            if not cuts:                     # nothing shared: one closed arc
                segs.append(v + [v[0]])
            else:
                for a, b in zip(cuts, cuts[1:] + [cuts[0]]):
                    pts, i = [v[a]], a
                    while i != b:
                        i = (i + 1) % n
                        pts.append(v[i])
                    segs.append(pts)
            refs = []
            for pts in segs:
                key, rev = canon(pts)
                raw.setdefault(key, pts[::-1] if rev else pts)
                refs.append((key, rev))
            plan[st].append(refs)
    return raw, plan


def simplify_arc(pts, tol):
    from shapely.geometry import LineString, Polygon
    if len(pts) <= 2:
        return pts
    if _k(pts[0]) == _k(pts[-1]):            # closed arc: simplify as a ring so
        for t in (tol, tol / 3):             # it cannot collapse or cross itself
            p = Polygon(pts).simplify(t, preserve_topology=True)
            if p.geom_type == "Polygon" and not p.is_empty and len(p.exterior.coords) >= 4:
                return [tuple(c) for c in p.exterior.coords]
        return pts
    return [tuple(c) for c in LineString(pts).simplify(tol, preserve_topology=False).coords]


def build_rings():
    from shapely.geometry import Polygon
    states = read_states()
    rings = {st: exterior_rings(g) for st, (nm, g) in states.items()}
    rings = {st: rs for st, rs in rings.items() if rs}

    area = {st: sum(Polygon(r).area for r in rs) / 1e6 for st, rs in rings.items()}
    tol = {st: min(max(TOL_K * math.sqrt(a), TOL_MIN), TOL_MAX) for st, a in area.items()}

    raw, plan = arcs_and_plan(rings)
    # a shared arc takes the finer of its two states' tolerances, so a big state
    # cannot coarsen the border of a small one
    best = {}
    for st, rs in plan.items():
        for refs in rs:
            for key, rev in refs:
                best[key] = min(best.get(key, float("inf")), tol[st])
    arcs = {key: simplify_arc(pts, best[key]) for key, pts in raw.items()}

    out = {}
    for st, rs in plan.items():
        got = []
        for refs in rs:
            ring = []
            for key, rev in refs:
                seg = arcs[key]
                if rev:
                    seg = seg[::-1]
                ring += seg[1:] if ring else seg
            if ring[0] != ring[-1]:
                ring.append(ring[0])
            if len(ring) >= 4:
                got.append(ring)
        if got:
            out[st] = got
    return out, states, tol, arcs


# --------------------------------------------------------------------------
# validation + write
# --------------------------------------------------------------------------

CHECKS = [
    ("Seattle, WA",   -122.3321, 47.6062, "WA"),
    ("Chicago, IL",    -87.6298, 41.8781, "IL"),
    ("Portland, ME",   -70.2553, 43.6591, "ME"),
    ("San Diego, CA", -117.1611, 32.7157, "CA"),
    ("Miami, FL",      -80.1918, 25.7617, "FL"),
    ("Anchorage, AK", -149.9003, 61.2181, "AK"),
    ("Honolulu, HI",  -157.8583, 21.3069, "HI"),
]

def main():
    from shapely.geometry import Point, Polygon, MultiPolygon

    out, states, tol, arcs = build_rings()

    js = {"proj": PROJ_NAME,
          "state": {st: [[[round(x), round(y)] for x, y in r] for r in rs]
                    for st, rs in sorted(out.items())}}
    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    with open(OUT_PATH, "w") as f:
        json.dump(js, f, separators=(",", ":"))

    npts = sum(len(r) for rs in out.values() for r in rs)
    print("source     %s (Natural Earth 5.1.1)" % NE_LAYER)
    print("proj       %s" % PROJ_NAME)
    print("states     %d   rings %d   arcs %d   points %d"
          % (len(out), sum(len(rs) for rs in out.values()), len(arcs), npts))
    print("wrote      %s  %.1f KB" % (OUT_PATH, os.path.getsize(OUT_PATH) / 1024))

    # ---- bounding boxes
    def bbox(keys):
        pts = [p for st in keys for r in out[st] for p in r]
        xs, ys = [p[0] for p in pts], [p[1] for p in pts]
        return min(xs), min(ys), max(xs), max(ys)

    l48 = [st for st in out if st not in ("AK", "HI")]
    fb, cb = bbox(list(out)), bbox(l48)
    print("\nfull bbox  x[%.0f %.0f] y[%.0f %.0f]  %.0f x %.0f km"
          % (fb[0], fb[2], fb[1], fb[3], (fb[2]-fb[0])/1000, (fb[3]-fb[1])/1000))
    print("lower 48   x[%.0f %.0f] y[%.0f %.0f]  %.0f x %.0f km  aspect %.3f:1"
          % (cb[0], cb[2], cb[1], cb[3], (cb[2]-cb[0])/1000, (cb[3]-cb[1])/1000,
             (cb[2]-cb[0])/(cb[3]-cb[1])))
    print("           insets sit inside the lower-48 extent: %s"
          % ("yes" if (fb[0] >= cb[0] - 1 and fb[1] >= cb[1] - 1
                       and fb[2] <= cb[2] + 1 and fb[3] <= cb[3] + 1) else "NO"))
    for st in ("AK", "HI"):
        b = bbox([st])
        print("%s inset   x[%.0f %.0f] y[%.0f %.0f]  %.0f x %.0f km"
              % (st, b[0], b[2], b[1], b[3], (b[2]-b[0])/1000, (b[3]-b[1])/1000))

    # ---- insets must not run into the mainland
    geo = {st: MultiPolygon([Polygon(r) for r in rs]).buffer(0) for st, rs in out.items()}
    l48u = MultiPolygon([Polygon(r) for st in l48 for r in out[st]]).buffer(0)
    for st in ("AK", "HI"):
        print("%s clearance to the lower 48  %.0f km" % (st, geo[st].distance(l48u) / 1000))
    print("AK to HI clearance             %.0f km" % (geo["AK"].distance(geo["HI"]) / 1000))

    # ---- the cities, through project(), checked against the rings they should hit
    print("\nproject() check (metres, and the ring the point lands in)")
    for nm, lon, lat, st in CHECKS:
        x, y = project(lon, lat, st)
        d = geo[st].distance(Point(x, y)) / 1000
        hit = "inside %s" % st if d == 0 else "%.0f km off %s" % (d, st)
        print("  %-14s %9.0f %9.0f   %s" % (nm, x, y, hit))
    order = sorted(CHECKS, key=lambda c: project(c[1], c[2], c[3])[0])
    print("  west to east: %s" % " < ".join(c[0].split(",")[0] for c in order))
    order = sorted(CHECKS, key=lambda c: -project(c[1], c[2], c[3])[1])
    print("  north to south: %s" % " > ".join(c[0].split(",")[0] for c in order))

    # ---- every state's own label point must land in its own geometry: proof the
    # dots and the rings really are on one transform
    bad = []
    for st, (nm, g) in states.items():
        p = g.representative_point()
        if geo[st].distance(p) > 0:
            bad.append(st)
    print("\nrepresentative point inside own rings: %d/%d%s"
          % (len(states) - len(bad), len(states), (" missed " + ",".join(bad)) if bad else ""))
    print("shared borders: %d arcs for %d rings, each simplified once"
          % (len(arcs), sum(len(rs) for rs in out.values())))

    # ---- did simplification tear any border apart? a tear shows up as a hole in
    # the union of the lower 48. Overlap is the same test from the other side.
    holes = [Polygon(i).area / 1e6 for p in (l48u.geoms if l48u.geom_type == "MultiPolygon"
                                             else [l48u]) for i in p.interiors]
    summed = sum(Polygon(r).area for st in l48 for r in out[st])
    print("border weld: %d gaps totalling %.0f km2, overlap %.4f%% of %.0f km2"
          % (len(holes), sum(holes), 100 * (summed - l48u.area) / l48u.area, l48u.area / 1e6))
    print("included: 50 states + DC. excluded: PR, VI, GU, AS, MP, UM "
          "(not states, not in the 50m admin-1 layer, would need more insets)")


if __name__ == "__main__":
    main()
