#!/usr/bin/env python3
"""
src/us/build_water.py - water proximity for every place in data/us/places.json

Same job as src/build_water.py does for Canada, re-cut for the United States and
re-sourced onto Natural Earth 10m physical vectors. Writes data/us/water.json.

Per place:
  km_to_ocean          distance to salt water: Pacific, Atlantic, Arctic,
                       Gulf of Mexico and the bays / sounds / straits that open
                       onto them. The Great Lakes are NOT in this layer.
  km_to_lake           distance to a lake >= MIN_LAKE_KM2 (50 km2). That band
                       takes in all five Great Lakes, the Great Salt Lake,
                       Lake Champlain, Tahoe, Okeechobee and Pontchartrain.
  nearest_water_name   name of whichever of the two is closer
  nearest_water_type   "ocean" | "lake"
  km_to_water          min(km_to_ocean, km_to_lake)
  on_water             km_to_water <= 5

The 29 Puerto Rico rows in places.json are skipped, as briefed. Every other row
is emitted, in places.json order, carrying geoid + name + state so a row is
still addressable when name+state repeats (it does, 4 times: University FL,
Kailua HI, Fairwood WA, El Sobrante CA).

DATA SOURCES - Natural Earth 10m physical vectors, public domain
---------------------------------------------------------------
  https://naciscdn.org/naturalearth/10m/physical/ne_10m_ocean.zip
      One global salt-water polygon. Continents and islands are its holes, so
      its boundary IS the coastline, and the Great Lakes / Great Salt Lake /
      Champlain / Tahoe / Okeechobee are correctly outside it (verified by
      point-in-polygon on all five). The Gulf of Mexico, Chesapeake Bay, Puget
      Sound and Cook Inlet are inside it, which is what we want.
  https://naciscdn.org/naturalearth/10m/physical/ne_10m_lakes.zip
  https://naciscdn.org/naturalearth/10m/physical/ne_10m_lakes_north_america.zip
      Lake polygons with names. featurecla is one of Lake / Reservoir /
      Alkaline Lake. Unlike the Canadian build, Alkaline Lake is KEPT here:
      the brief names the Great Salt Lake, which is exactly that class.
  https://naciscdn.org/naturalearth/10m/physical/ne_10m_geography_marine_polys.zip
      Named marine bodies, used to label the salt water at the shoreline point
      that turned out to be closest. scalerank orders them, and the most
      specific name wins, so a Seattle answer reads "Puget Sound" and not
      "North Pacific Ocean".

  Lake Pontchartrain is a special case, handled by geometry rather than by
  hand. Natural Earth has no lake polygon for it - it sits inside ne_10m_ocean,
  because it connects to the Gulf through the Rigolets. It IS in
  ne_10m_geography_marine_polys, as featurecla "lagoon", name "Lake
  Pontchartrain". So any stretch of ocean-polygon shoreline whose midpoint
  falls inside a marine "lagoon" polygon named "Lake ..." is moved out of the
  salt-water segment pool and into the lake pool under that name. That yields a
  true Pontchartrain shoreline distance for New Orleans and keeps km_to_ocean
  meaning open salt water. Only 4 such lagoons exist in the window; the other
  three (Husky Lakes NT, Bras d'Or Lake NS, Lago de Maracaibo VE) are outside
  the US and change nothing.

NAMES, FALLBACK - GeoNames US gazetteer (CC BY 4.0)
    https://download.geonames.org/export/dump/US.zip
  349 of the 1,210 qualifying lake polygons in the window carry no Natural
  Earth name (nearly all of them remote Canadian ones). Any such polygon is
  labelled from the gazetteer water-feature point lying inside it.

METHOD - unchanged from the validated Canadian build
----------------------------------------------------
1. Every polygon ring in the window is densified so no segment exceeds
   MAX_SEG_KM, then flattened into an array of 2-point segments.
2. A 3-D unit-sphere KD-tree over segment midpoints narrows each place to the
   segments that could hold the closest point: to beat the best midpoint a
   segment's own midpoint must lie within best + MAX_SEG_KM/2.
3. Those candidates are projected into an azimuthal-equidistant CRS centred on
   the place. AEQD reproduces true geodesic distance from its own centre, so the
   analytic point-to-segment distance in that plane is the real distance in
   metres. Distance is to the polygon BOUNDARY, never to a centroid.
4. A place inside a lake polygon, or inside the ocean polygon, is distance 0.

Nothing is estimated. Every number falls out of the downloaded geometry.

Usage:  /tmp/uswater_venv/bin/python src/us/build_water.py
Env:    US_WATER_CACHE  where to download/unpack the sources
                        (default: <tmpdir>/us_water_cache; needs ~1.5 GB)
"""

import json
import math
import os
import sys
import tempfile
import urllib.request
import zipfile

import numpy as np
import shapefile  # pyshp
from pyproj import CRS, Geod, Transformer
from scipy.spatial import cKDTree
from shapely import wkb
from shapely.geometry import Point, box, shape
from shapely.prepared import prep
from shapely.strtree import STRtree

# --------------------------------------------------------------------------
# config
# --------------------------------------------------------------------------

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PLACES_PATH = os.path.join(REPO, "data", "us", "places.json")
OUT_PATH = os.path.join(REPO, "data", "us", "water.json")

CACHE = os.environ.get("US_WATER_CACHE") or os.path.join(
    tempfile.gettempdir(), "us_water_cache"
)

NE_BASE = "https://naciscdn.org/naturalearth/10m/physical"
NE_LAYERS = [
    "ne_10m_ocean",
    "ne_10m_lakes",
    "ne_10m_lakes_north_america",
    "ne_10m_geography_marine_polys",
]
GEONAMES_URL = "https://download.geonames.org/export/dump/US.zip"
# gazetteer feature codes that name a standing body of water, best first
GEONAMES_CODES = {"LK": 0, "LKS": 0, "RSV": 0, "LGN": 1, "POOL": 1, "BAY": 2}

TERRITORIES = {"PR", "VI", "GU", "AS", "MP"}

# Window around the 50 states. places.json spans lon -159.4 .. -68.7,
# lat 19.6 .. 64.9, so this leaves room for the nearest water to any of them.
WIN_LON = (-180.0, -50.0)
WIN_LAT = (10.0, 75.0)

MAX_SEG_KM = 10.0          # densification target
PAD_KM = MAX_SEG_KM / 2 + 1.0
MIN_LAKE_KM2 = 50.0        # "roughly >50 km2"
LAKE_CLASSES = {"Lake", "Reservoir", "Alkaline Lake"}
R_EARTH_KM = 6371.0088     # sphere radius, used only to pick candidates
ON_WATER_KM = 5.0

GEOD = Geod(ellps="WGS84")

# Natural Earth names the two big oceans hemisphere-wise; the app wants the
# plain name. Display-only relabelling, no geometry involved.
OCEAN_RENAME = {
    "North Pacific Ocean": "Pacific Ocean",
    "South Pacific Ocean": "Pacific Ocean",
    "North Atlantic Ocean": "Atlantic Ocean",
    "South Atlantic Ocean": "Atlantic Ocean",
}


# --------------------------------------------------------------------------
# download
# --------------------------------------------------------------------------

def _download(url, dest, note=""):
    sys.stderr.write("downloading %s %s\n" % (url, note))
    urllib.request.urlretrieve(url, dest)


def fetch():
    os.makedirs(CACHE, exist_ok=True)
    for name in NE_LAYERS:
        d = os.path.join(CACHE, name)
        if os.path.exists(os.path.join(d, name + ".shp")):
            continue
        z = os.path.join(CACHE, name + ".zip")
        _download("%s/%s.zip" % (NE_BASE, name), z)
        with zipfile.ZipFile(z) as zf:
            zf.extractall(d)
    if not os.path.exists(geonames_path()):
        z = os.path.join(CACHE, "US.zip")
        if not os.path.exists(z) or os.path.getsize(z) < 1_000_000:
            _download(GEONAMES_URL, z, "(71 MB)")
        with zipfile.ZipFile(z) as zf:
            zf.extractall(os.path.join(CACHE, "geonames_US"))


def ne_path(name):
    return os.path.join(CACHE, name, name + ".shp")


def geonames_path():
    return os.path.join(CACHE, "geonames_US", "US.txt")


def read_ne(name):
    """-> list of (attribute dict, shapely geometry)."""
    r = shapefile.Reader(ne_path(name))
    fields = [f[0] for f in r.fields[1:]]
    out = []
    for sr in r.shapeRecords():
        g = shape(sr.shape.__geo_interface__)
        if not g.is_valid:
            g = g.buffer(0)
        out.append((dict(zip(fields, sr.record)), g))
    return out


def read_geonames_water():
    """-> (list of shapely points, list of (priority, name))."""
    pts, meta = [], []
    with open(geonames_path(), encoding="utf-8") as f:
        for line in f:
            col = line.rstrip("\n").split("\t")
            if len(col) < 9 or col[6] != "H":
                continue
            pri = GEONAMES_CODES.get(col[7])
            if pri is None or not col[1]:
                continue
            try:
                lat, lon = float(col[4]), float(col[5])
            except ValueError:
                continue
            if not (WIN_LON[0] <= lon <= WIN_LON[1]
                    and WIN_LAT[0] <= lat <= WIN_LAT[1]):
                continue
            pts.append(Point(lon, lat))
            meta.append((pri, col[1]))
    sys.stderr.write("GeoNames US water features in window: %d\n" % len(pts))
    return pts, meta


# --------------------------------------------------------------------------
# geometry helpers
# --------------------------------------------------------------------------

def ll_to_xyz(lat, lon):
    la = np.radians(np.asarray(lat, dtype=float))
    lo = np.radians(np.asarray(lon, dtype=float))
    c = np.cos(la)
    return np.stack([c * np.cos(lo), c * np.sin(lo), np.sin(la)], axis=-1)


def chord_to_km(ch):
    return 2.0 * R_EARTH_KM * math.asin(min(max(ch, 0.0), 2.0) / 2.0)


def km_to_chord(km):
    return 2.0 * math.sin(min(km / R_EARTH_KM, math.pi) / 2.0)


def bbox_hits_window(bbox):
    lo0, la0, lo1, la1 = bbox
    return not (
        lo1 < WIN_LON[0] - 1 or lo0 > WIN_LON[1] + 1
        or la1 < WIN_LAT[0] - 1 or la0 > WIN_LAT[1] + 1
    )


def geodesic_area_km2(g):
    return abs(GEOD.geometry_area_perimeter(g)[0]) / 1e6


def densify(pts):
    """Split any segment longer than MAX_SEG_KM. Linear in lon/lat, which over
    <= 10 km differs from the geodesic by centimetres."""
    a = pts[:-1]
    b = pts[1:]
    midlat = np.radians((a[:, 1] + b[:, 1]) * 0.5)
    dx = (b[:, 0] - a[:, 0]) * np.cos(midlat) * 111.32
    dy = (b[:, 1] - a[:, 1]) * 110.574
    n = np.maximum(1, np.ceil(np.hypot(dx, dy) / MAX_SEG_KM).astype(int))
    if n.max() == 1:
        return pts
    out = []
    for i in range(len(a)):
        k = n[i]
        if k == 1:
            out.append(a[i][None, :])
        else:
            t = np.linspace(0.0, 1.0, k, endpoint=False)[:, None]
            out.append(a[i] + t * (b[i] - a[i]))
    out.append(b[-1][None, :])
    return np.vstack(out)


def ring_segments(pts, owner_id, drop_clip_edges=False):
    """coords -> (segments (n,4), owner ids (n,)) inside the window.

    drop_clip_edges kills the artificial ring edges Natural Earth leaves where
    it cuts the global ocean polygon at the antimeridian and the poles - those
    are not coastline.
    """
    if len(pts) < 2:
        return None
    pts = densify(np.asarray(pts, dtype=float))
    a = pts[:-1]
    b = pts[1:]
    mlon = (a[:, 0] + b[:, 0]) * 0.5
    mlat = (a[:, 1] + b[:, 1]) * 0.5
    keep = (
        (mlon >= WIN_LON[0]) & (mlon <= WIN_LON[1])
        & (mlat >= WIN_LAT[0]) & (mlat <= WIN_LAT[1])
    )
    if drop_clip_edges:
        edge = (
            ((np.abs(a[:, 0]) >= 179.99) & (np.abs(b[:, 0]) >= 179.99))
            | ((a[:, 1] >= 89.99) & (b[:, 1] >= 89.99))
            | ((a[:, 1] <= -89.99) & (b[:, 1] <= -89.99))
        )
        keep &= ~edge
    if not keep.any():
        return None
    s = np.concatenate([a[keep], b[keep]], axis=1)
    return s, np.full(len(s), owner_id, dtype=np.int32)


def shape_segments(sh, owner_id, segs, owners, drop_clip_edges=False):
    parts = list(sh.parts) + [len(sh.points)]
    for k in range(len(parts) - 1):
        got = ring_segments(sh.points[parts[k]:parts[k + 1]], owner_id,
                            drop_clip_edges)
        if got:
            segs.append(got[0])
            owners.append(got[1])


class WaterLayer(object):
    """Segment set + KD-tree, plus the exact per-place distance solver."""

    def __init__(self, label, seg, owner):
        self.label = label
        self.seg = seg
        self.owner = owner
        mid_lon = (seg[:, 0] + seg[:, 2]) * 0.5
        mid_lat = (seg[:, 1] + seg[:, 3]) * 0.5
        self.tree = cKDTree(ll_to_xyz(mid_lat, mid_lon))
        sys.stderr.write("%s: %d segments\n" % (label, len(seg)))

    def distance(self, lat, lon):
        """-> (km, owner_id, (nearest_lon, nearest_lat)) or (None, None, None)"""
        p3 = ll_to_xyz(lat, lon)
        d_chord, _ = self.tree.query(p3)
        best_mid_km = chord_to_km(float(d_chord))
        idx = self.tree.query_ball_point(p3, km_to_chord(best_mid_km + PAD_KM))
        if not idx:
            return None, None, None
        idx = np.asarray(idx)
        cand = self.seg[idx]

        proj = CRS.from_proj4(
            "+proj=aeqd +lat_0=%.10f +lon_0=%.10f +datum=WGS84 +units=m +no_defs"
            % (lat, lon)
        )
        fwd = Transformer.from_crs("EPSG:4326", proj, always_xy=True)
        ax, ay = fwd.transform(cand[:, 0], cand[:, 1])
        bx, by = fwd.transform(cand[:, 2], cand[:, 3])
        A = np.stack([ax, ay], axis=1)
        B = np.stack([bx, by], axis=1)
        AB = B - A
        denom = (AB * AB).sum(1)
        safe = denom > 0
        t = np.zeros(len(A))
        t[safe] = -(A[safe] * AB[safe]).sum(1) / denom[safe]
        t = np.clip(t, 0.0, 1.0)
        C = A + t[:, None] * AB
        d = np.hypot(C[:, 0], C[:, 1])
        d = np.where(np.isfinite(d), d, np.inf)
        if not np.isfinite(d).any():
            return None, None, None
        j = int(np.argmin(d))
        inv = Transformer.from_crs(proj, "EPSG:4326", always_xy=True)
        nlon, nlat = inv.transform(float(C[j, 0]), float(C[j, 1]))
        return float(d[j]) / 1000.0, int(self.owner[idx[j]]), (nlon, nlat)


# --------------------------------------------------------------------------
# layers
# --------------------------------------------------------------------------

def lagoon_lakes():
    """Marine 'lagoon' polygons named 'Lake ...' -> [(name, polygon)].

    Natural Earth files these inside ne_10m_ocean, so without this they would
    read as salt water. Lake Pontchartrain is the one that matters in the US.
    """
    out = []
    for a, g in read_ne("ne_10m_geography_marine_polys"):
        if (a.get("featurecla") or "") != "lagoon":
            continue
        nm = (a.get("name") or "").strip()
        if nm.lower().startswith("lake") or nm.lower().endswith("lake") \
                or " lake" in nm.lower():
            if bbox_hits_window(g.bounds):
                out.append((nm, g))
    sys.stderr.write("marine lagoons treated as lakes: %s\n"
                     % ", ".join(n for n, _ in out))
    return out


def load_ocean(lagoons):
    """ne_10m_ocean -> (salt WaterLayer, lagoon segment pool, ocean parts).

    The boundary of the global ocean polygon is the coastline. Segments whose
    midpoint falls inside one of `lagoons` are handed back separately so they
    can join the lake pool instead.
    """
    r = shapefile.Reader(ne_path("ne_10m_ocean"))
    segs, owners = [], []
    for i, sh in enumerate(r.iterShapes()):
        shape_segments(sh, i, segs, owners, drop_clip_edges=True)
    seg = np.vstack(segs)
    sys.stderr.write("ocean boundary segments in window: %d\n" % len(seg))

    mid = np.stack([(seg[:, 0] + seg[:, 2]) * 0.5,
                    (seg[:, 1] + seg[:, 3]) * 0.5], axis=1)
    in_lagoon = np.full(len(seg), -1, dtype=np.int32)
    for li, (nm, g) in enumerate(lagoons):
        lo0, la0, lo1, la1 = g.bounds
        cand = np.nonzero((mid[:, 0] >= lo0) & (mid[:, 0] <= lo1)
                          & (mid[:, 1] >= la0) & (mid[:, 1] <= la1)
                          & (in_lagoon < 0))[0]
        pg = prep(g)
        hit = [k for k in cand if pg.covers(Point(mid[k, 0], mid[k, 1]))]
        in_lagoon[hit] = li
        sys.stderr.write("  %s: %d shoreline segments reassigned\n"
                         % (nm, len(hit)))

    salt = seg[in_lagoon < 0]
    lagoon_pool = [(li, seg[in_lagoon == li]) for li in range(len(lagoons))]

    # the ocean polygon itself, clipped to the window, for the inside test
    cache = os.path.join(CACHE, "ocean_clip.wkb")
    if os.path.exists(cache):
        with open(cache, "rb") as f:
            clipped = wkb.loads(f.read())
    else:
        g = shape(r.shape(0).__geo_interface__)
        if not g.is_valid:
            g = g.buffer(0)
        clipped = g.intersection(box(WIN_LON[0], WIN_LAT[0],
                                     WIN_LON[1], WIN_LAT[1]))
        with open(cache, "wb") as f:
            f.write(wkb.dumps(clipped))
    parts = list(clipped.geoms) if clipped.geom_type.startswith("Multi") \
        else [clipped]
    sys.stderr.write("ocean polygon parts in window: %d\n" % len(parts))
    return (WaterLayer("salt water NE-10m-ocean", salt,
                       np.zeros(len(salt), dtype=np.int32)),
            lagoon_pool, parts)


def load_lakes(lagoons, lagoon_pool):
    """NE lake polygons >= MIN_LAKE_KM2 -> (WaterLayer, polygons, names).

    Lagoon shoreline handed over by load_ocean() is appended as extra lake
    entries whose polygon is the marine lagoon outline (used only for the
    inside test; the distance comes from the real ocean-polygon shoreline).
    """
    gaz_pts, gaz_meta = read_geonames_water()
    gaz_index = STRtree(gaz_pts) if gaz_pts else None

    raw = []
    for layer in ("ne_10m_lakes", "ne_10m_lakes_north_america"):
        r = shapefile.Reader(ne_path(layer))
        fields = [f[0] for f in r.fields[1:]]
        for sr in r.shapeRecords():
            a = dict(zip(fields, sr.record))
            if (a.get("featurecla") or "") not in LAKE_CLASSES:
                continue
            if not bbox_hits_window(sr.shape.bbox):
                continue
            g = shape(sr.shape.__geo_interface__)
            if not g.is_valid:
                g = g.buffer(0)
            if geodesic_area_km2(g) < MIN_LAKE_KM2:
                continue
            raw.append((a, g, sr.shape))

    polys, names, segs, owners = [], [], [], []
    unnamed = 0
    for a, g, sh in raw:
        nm = ne_name(a)
        if not nm and gaz_index is not None:
            pg = prep(g)
            best = None
            for k in gaz_index.query(g):
                if pg.covers(gaz_pts[k]):
                    pri, gnm = gaz_meta[k]
                    key = (pri, gaz_pts[k].distance(g.representative_point()))
                    if best is None or key < best[0]:
                        best = (key, gnm)
            if best:
                nm = best[1]
        if not nm:
            unnamed += 1
        fid = len(polys)
        polys.append(g)
        names.append(nm or "Unnamed lake")
        shape_segments(sh, fid, segs, owners)

    for li, seg in lagoon_pool:
        if not len(seg):
            continue
        fid = len(polys)
        polys.append(lagoons[li][1])
        names.append(lagoons[li][0])
        segs.append(seg)
        owners.append(np.full(len(seg), fid, dtype=np.int32))

    sys.stderr.write("lake polygons >= %.0f km2: %d  [still unnamed: %d]\n"
                     % (MIN_LAKE_KM2, len(polys), unnamed))
    return (WaterLayer("lakes NE-10m", np.vstack(segs),
                       np.concatenate(owners)), polys, names)


# --------------------------------------------------------------------------
# naming (Natural Earth)
# --------------------------------------------------------------------------

NE_NAME_KEYS = ("name", "name_en", "namealt", "name_alt", "label")


def ne_name(attrs):
    for k in NE_NAME_KEYS:
        v = attrs.get(k)
        v = v.strip() if isinstance(v, str) else ""
        if v:
            return v
    return ""


class Namer(object):
    """Names the water body that owns a given point on a shoreline."""

    def __init__(self, feats, skip=()):
        self.feats = []
        for a, g in feats:
            nm = ne_name(a)
            if not nm or nm in skip:
                continue
            self.feats.append((nm, float(a.get("scalerank") or 0), g))
        self.index = STRtree([g for _, _, g in self.feats])

    def name_for(self, lon, lat, near_deg):
        pt = Point(lon, lat)
        inside = []
        for i in self.index.query(pt):
            nm, rank, g = self.feats[i]
            if g.covers(pt):
                inside.append((rank, nm))
        if inside:
            # highest scalerank == most specific named body, so Puget Sound
            # wins over North Pacific Ocean and Cook Inlet over Gulf of Alaska
            inside.sort(key=lambda x: -x[0])
            return OCEAN_RENAME.get(inside[0][1], inside[0][1])
        best = None
        for i in self.index.query(pt.buffer(near_deg)):
            nm, _, g = self.feats[i]
            d = g.distance(pt)
            if d <= near_deg and (best is None or d < best[0]):
                best = (d, nm)
        if best:
            return OCEAN_RENAME.get(best[1], best[1])
        return None

    def nearest_name(self, lon, lat, radii):
        """name_for with a widening search - used for salt water, where the
        named marine polygons tile the sea and something must always match."""
        for r in radii:
            nm = self.name_for(lon, lat, r)
            if nm:
                return nm
        return None


# --------------------------------------------------------------------------
# main
# --------------------------------------------------------------------------

OCEAN_CHECKS = [("Santa Monica", "CA"), ("Miami Beach", "FL"),
                ("Virginia Beach", "VA"), ("Urban Honolulu", "HI")]
LAKE_CHECKS = [("Chicago", "IL"), ("Cleveland", "OH"), ("Buffalo", "NY"),
               ("Duluth", "MN")]
INLAND_CHECKS = [("Denver", "CO"), ("Wichita", "KS"), ("Lubbock", "TX")]
OTHER_CHECKS = [("Salt Lake City", "UT"), ("New Orleans", "LA"),
                ("Seattle", "WA"), ("Detroit", "MI"), ("Reno", "NV"),
                ("Burlington", "VT"), ("Anchorage", "AK"), ("Boston", "MA")]


def main():
    fetch()

    with open(PLACES_PATH) as f:
        raw_places = json.load(f)
    places = [p for p in raw_places if p["state"] not in TERRITORIES]
    sys.stderr.write("places: %d of %d rows (%d territory rows skipped)\n"
                     % (len(places), len(raw_places),
                        len(raw_places) - len(places)))

    lag = lagoon_lakes()
    salt, lagoon_pool, ocean_parts = load_ocean(lag)
    lakes, lake_polys, lake_names = load_lakes(lag, lagoon_pool)

    ocean_prep = [prep(g) for g in ocean_parts]
    ocean_index = STRtree(ocean_parts)
    lake_prep = [prep(g) for g in lake_polys]
    lake_index = STRtree(lake_polys)

    marine = read_ne("ne_10m_geography_marine_polys")
    lagoon_names = set(n for n, _ in lag)
    marine_namer = Namer(marine, skip=lagoon_names)
    lake_namer = Namer(read_ne("ne_10m_lakes")
                       + read_ne("ne_10m_lakes_north_america"))

    out = []
    for n, p in enumerate(places):
        lat, lon = p["lat"], p["lon"]
        rec = {
            "geoid": p["geoid"],
            "name": p["name"],
            "state": p["state"],
            "km_to_ocean": None,
            "km_to_lake": None,
            "nearest_water_name": None,
            "nearest_water_type": None,
            "km_to_water": None,
            "on_water": None,
        }
        if lat is None or lon is None:
            out.append(rec)
            continue
        pt = Point(lon, lat)

        o_km, _, o_pt = salt.distance(lat, lon)
        in_ocean = any(ocean_prep[i].covers(pt) for i in ocean_index.query(pt))

        l_km, l_fid, l_pt = lakes.distance(lat, lon)
        for i in lake_index.query(pt):
            if lake_prep[i].covers(pt):
                # a marine lagoon outline only counts as water where the ocean
                # polygon agrees; elsewhere inside it is dry land
                if lake_names[i] in lagoon_names and not in_ocean:
                    continue
                l_km, l_fid, l_pt = 0.0, int(i), (lon, lat)
                break
        if in_ocean and l_km != 0.0 and o_km is not None:
            o_km, o_pt = 0.0, (lon, lat)

        rec["km_to_ocean"] = None if o_km is None else round(o_km, 1)
        rec["km_to_lake"] = None if l_km is None else round(l_km, 1)

        cands = []
        if o_km is not None:
            nm = marine_namer.nearest_name(o_pt[0], o_pt[1],
                                           (0.35, 1.0, 3.0, 8.0)) or "Ocean"
            cands.append((o_km, "ocean", nm))
        if l_km is not None:
            nm = None
            if lake_names[l_fid] not in lagoon_names:
                nm = lake_namer.name_for(l_pt[0], l_pt[1], 0.03)
            cands.append((l_km, "lake", nm or lake_names[l_fid]))
        if cands:
            cands.sort(key=lambda x: x[0])
            km, typ, nm = cands[0]
            rec["nearest_water_name"] = nm
            rec["nearest_water_type"] = typ
            rec["km_to_water"] = round(km, 1)
            rec["on_water"] = bool(km <= ON_WATER_KM)
        out.append(rec)
        if (n + 1) % 250 == 0:
            sys.stderr.write("  %d/%d\n" % (n + 1, len(places)))

    with open(OUT_PATH, "w") as f:
        json.dump(out, f, indent=1)
        f.write("\n")

    # ---- check tables ----------------------------------------------------
    by = {}
    for r in out:
        by.setdefault((r["name"], r["state"]), r)
    hdr = "%-22s %-3s %12s %11s  %-24s %-6s %8s %9s"

    def block(title, keys):
        print("")
        print(title)
        print(hdr % ("PLACE", "ST", "KM_TO_OCEAN", "KM_TO_LAKE",
                     "NEAREST_WATER", "TYPE", "KM", "ON_WATER"))
        print("-" * 104)
        for key in keys:
            r = by.get(key)
            if not r:
                print("%-22s %-3s   MISSING" % key)
                continue
            print(hdr % (r["name"], r["state"], r["km_to_ocean"],
                         r["km_to_lake"], r["nearest_water_name"],
                         r["nearest_water_type"], r["km_to_water"],
                         r["on_water"]))

    block("OCEAN CHECKS - expect type=ocean, km 0-3", OCEAN_CHECKS)
    block("GREAT LAKES CHECKS - expect type=lake, correct lake, km 0-3",
          LAKE_CHECKS)
    block("INLAND CHECKS - expect km_to_ocean > 800", INLAND_CHECKS)
    block("OTHER CHECKS", OTHER_CHECKS)

    print("")
    got = sum(1 for r in out if r["km_to_water"] is not None)
    print("rows written: %d   with a value: %d" % (len(out), got))
    print("nearest is ocean: %d | nearest is lake: %d"
          % (sum(1 for r in out if r["nearest_water_type"] == "ocean"),
             sum(1 for r in out if r["nearest_water_type"] == "lake")))
    print("on_water (<= %.0f km): %d"
          % (ON_WATER_KM, sum(1 for r in out if r["on_water"])))
    print("km_to_ocean missing: %d | km_to_lake missing: %d"
          % (sum(1 for r in out if r["km_to_ocean"] is None),
             sum(1 for r in out if r["km_to_lake"] is None)))
    print("unnamed nearest water: %d"
          % sum(1 for r in out if r["nearest_water_name"] in
                (None, "Unnamed lake", "Ocean")))
    print("wrote %s (%.0f KB)"
          % (OUT_PATH, os.path.getsize(OUT_PATH) / 1024.0))


if __name__ == "__main__":
    main()
