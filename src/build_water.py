#!/usr/bin/env python3
"""
build_water.py - water proximity for every place in data/climate.json

Computes, per place, the true great-circle distance from the place's
coordinates to the BOUNDARY of

  * salt water (any ocean / sea / bay / strait) -> km_to_ocean
  * large freshwater lakes (>= 50 km2)          -> km_to_lake

and writes data/water.json.

DATA SOURCES
------------
Coastline geometry - GSHHG 2.3.7, FULL resolution (Wessel & Smith, "A Global
Self-consistent, Hierarchical, High-resolution Geography Database"):
    https://www.soest.hawaii.edu/pwessel/gshhg/gshhg-shp-2.3.7.zip
  GSHHS_f_L1 = the land / ocean boundary, i.e. the coastline. One consistent
  salt-water layer, so the Atlantic, Pacific, Arctic, Hudson Bay, James Bay,
  the Gulf of St. Lawrence and the Salish Sea are all covered, and the Great
  Lakes are correctly excluded from it (they are the separate L2 layer).

Lake geometry - HydroLAKES v1.0 (Messager et al. 2016, HydroSHEDS):
    https://data.hydrosheds.org/file/hydrolakes/HydroLAKES_polys_v10_shp.zip
  1.4 M lake polygons with a Lake_area km2 attribute. Filtered to >= 50 km2.
  Chosen over the coarser lake layers because it actually resolves the bays
  cities sit on - Hamilton Harbour, the Bay of Quinte, Kempenfelt Bay - which
  Natural Earth 10m and GSHHG L2 both flatten out of Lake Ontario / Simcoe.

Names - Natural Earth 10m physical vectors (public domain):
    https://naciscdn.org/naturalearth/10m/physical/ne_10m_geography_marine_polys.zip
    https://naciscdn.org/naturalearth/10m/physical/ne_10m_lakes.zip
    https://naciscdn.org/naturalearth/10m/physical/ne_10m_lakes_north_america.zip
  GSHHG carries no names and HydroLAKES stores bare ones ("Ontario"), so the
  label is looked up from whichever Natural Earth feature sits at the point on
  the shoreline that turned out to be closest. Natural Earth's "Alkaline Lake"
  class is also used to drop salt/soda lakes, which are not freshwater.

Names, fallback - GeoNames Canada gazetteer (CC BY 4.0):
    https://download.geonames.org/export/dump/CA.zip
  105 k named Canadian lakes as points. Natural Earth 10m has no name for the
  smaller water bodies a lot of towns actually sit on (Lac Saint-Louis, Lac des
  Deux Montagnes, Allumette Lake), so any lake polygon Natural Earth cannot
  name is labelled from the gazetteer point lying inside it.

METHOD
------
1. Every polygon ring inside a North-America window is densified so no segment
   is longer than MAX_SEG_KM, then stored as a flat array of 2-point segments.
2. A 3-D unit-sphere KD-tree over segment midpoints finds, for each place, the
   small set of segments that can possibly hold the closest point: any segment
   able to beat the best midpoint must have its own midpoint within
   best + MAX_SEG_KM/2.
3. Those candidate segments are projected into an azimuthal-equidistant CRS
   centred on the place. AEQD reproduces true geodesic distance from its centre
   exactly, so the analytic point-to-segment distance in that plane is the real
   distance in metres.
4. A point inside a lake, or outside every land polygon (i.e. standing in the
   sea), gets distance 0.

Nothing here is estimated or recalled - every number falls out of the
downloaded geometry.

Usage:  python3 src/build_water.py
Env:    WATER_CACHE  where to download/unpack the source data
                     (default: <tmpdir>/water_cache; needs ~3 GB)
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
from pyproj import CRS, Transformer
from scipy.spatial import cKDTree
from shapely.geometry import Point, shape
from shapely.prepared import prep
from shapely.strtree import STRtree

# --------------------------------------------------------------------------
# config
# --------------------------------------------------------------------------

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PLACES_PATH = os.path.join(REPO, "data", "climate.json")
OUT_PATH = os.path.join(REPO, "data", "water.json")

CACHE = os.environ.get("WATER_CACHE") or os.path.join(
    tempfile.gettempdir(), "water_cache"
)

GSHHG_URL = "https://www.soest.hawaii.edu/pwessel/gshhg/gshhg-shp-2.3.7.zip"
HYDROLAKES_URL = (
    "https://data.hydrosheds.org/file/hydrolakes/HydroLAKES_polys_v10_shp.zip"
)
GEONAMES_URL = "https://download.geonames.org/export/dump/CA.zip"
# gazetteer feature codes that name a standing body of water, best first
GEONAMES_CODES = {"LK": 0, "LKS": 0, "RSV": 0, "LGN": 1, "POOL": 1, "BAY": 2}
NE_BASE = "https://naciscdn.org/naturalearth/10m/physical"
NE_LAYERS = [
    "ne_10m_lakes",
    "ne_10m_lakes_north_america",
    "ne_10m_geography_marine_polys",
]

# North-America window. Every Canadian place sits well inside it, and so does
# the nearest salt water / large lake to any of them.
WIN_LON = (-180.0, -20.0)
WIN_LAT = (15.0, 90.0)

MAX_SEG_KM = 10.0        # densification target
PAD_KM = MAX_SEG_KM / 2 + 1.0
MIN_LAKE_KM2 = 50.0      # "roughly >50 km2"
R_EARTH_KM = 6371.0088   # sphere radius, used only to pick candidates
ON_WATER_KM = 5.0

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

    gdir = os.path.join(CACHE, "gshhg")
    if not os.path.exists(os.path.join(gdir, "GSHHS_shp", "f", "GSHHS_f_L1.shp")):
        z = os.path.join(CACHE, "gshhg-shp-2.3.7.zip")
        if not os.path.exists(z) or os.path.getsize(z) < 1_000_000:
            _download(GSHHG_URL, z, "(149 MB)")
        with zipfile.ZipFile(z) as zf:
            for n in zf.namelist():
                if n.startswith("GSHHS_shp/f/"):
                    zf.extract(n, gdir)

    hdir = os.path.join(CACHE, "hydrolakes")
    if not os.path.exists(hydrolakes_path()):
        z = os.path.join(CACHE, "HydroLAKES_polys_v10_shp.zip")
        if not os.path.exists(z) or os.path.getsize(z) < 1_000_000:
            _download(HYDROLAKES_URL, z, "(820 MB)")
        with zipfile.ZipFile(z) as zf:
            zf.extractall(hdir)

    for name in NE_LAYERS:
        d = os.path.join(CACHE, name)
        if os.path.exists(os.path.join(d, name + ".shp")):
            continue
        z = os.path.join(CACHE, name + ".zip")
        _download("%s/%s.zip" % (NE_BASE, name), z)
        with zipfile.ZipFile(z) as zf:
            zf.extractall(d)

    if not os.path.exists(geonames_path()):
        z = os.path.join(CACHE, "geonames_CA.zip")
        _download(GEONAMES_URL, z, "(8 MB)")
        with zipfile.ZipFile(z) as zf:
            zf.extractall(os.path.join(CACHE, "geonames_CA"))


def gshhg_path(layer):
    return os.path.join(CACHE, "gshhg", "GSHHS_shp", "f", layer + ".shp")


def hydrolakes_path():
    return os.path.join(CACHE, "hydrolakes", "HydroLAKES_polys_v10_shp",
                        "HydroLAKES_polys_v10.shp")


def geonames_path():
    return os.path.join(CACHE, "geonames_CA", "CA.txt")


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
                pts.append(Point(float(col[5]), float(col[4])))
            except ValueError:
                continue
            meta.append((pri, col[1]))
    sys.stderr.write("GeoNames water features: %d\n" % len(pts))
    return pts, meta


def read_ne(name):
    """-> list of (attribute dict, shapely geometry)."""
    r = shapefile.Reader(os.path.join(CACHE, name, name + ".shp"))
    fields = [f[0] for f in r.fields[1:]]
    out = []
    for sr in r.shapeRecords():
        g = shape(sr.shape.__geo_interface__)
        if not g.is_valid:
            g = g.buffer(0)
        out.append((dict(zip(fields, sr.record)), g))
    return out


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


def ring_segments(pts, owner_id):
    """coords -> (segments (n,4), owner ids (n,)) inside the window."""
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
    if not keep.any():
        return None
    s = np.concatenate([a[keep], b[keep]], axis=1)
    return s, np.full(len(s), owner_id, dtype=np.int32)


def shape_segments(sh, owner_id, segs, owners):
    parts = list(sh.parts) + [len(sh.points)]
    for k in range(len(parts) - 1):
        got = ring_segments(sh.points[parts[k]:parts[k + 1]], owner_id)
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

def load_coast(place_pts):
    """GSHHS_f_L1, the land/ocean boundary.

    Returns (WaterLayer, land polygons that could contain a place). Distance
    from a land point to this boundary is its distance to salt water; a place
    outside every land polygon is standing in the sea.
    """
    cache = os.path.join(CACHE, "coast_segments.npz")
    if os.path.exists(cache):
        z = np.load(cache)
        seg, owner = z["seg"], z["owner"]
    else:
        segs, owners = [], []
        n = 0
        for i, sh in enumerate(shapefile.Reader(gshhg_path("GSHHS_f_L1")).iterShapes()):
            if not bbox_hits_window(sh.bbox):
                continue
            shape_segments(sh, i, segs, owners)
            n += 1
            if n % 20000 == 0:
                sys.stderr.write("  L1 %d polygons in window\n" % n)
        seg = np.vstack(segs)
        owner = np.concatenate(owners)
        np.savez_compressed(cache, seg=seg, owner=owner)
        sys.stderr.write("L1 polygons in window: %d\n" % n)

    land = []
    for sh in shapefile.Reader(gshhg_path("GSHHS_f_L1")).iterShapes():
        if not bbox_hits_window(sh.bbox):
            continue
        lo0, la0, lo1, la1 = sh.bbox
        if any(lo0 <= lon <= lo1 and la0 <= lat <= la1 for lat, lon in place_pts):
            g = shape(sh.__geo_interface__)
            if not g.is_valid:
                g = g.buffer(0)
            land.append(g)
    sys.stderr.write("land polygons covering places: %d\n" % len(land))
    return WaterLayer("coast GSHHG-L1", seg, owner), land


def load_lakes(alkaline, ne_lakes):
    """HydroLAKES polygons >= MIN_LAKE_KM2 in the window.

    `alkaline` is the list of Natural Earth "Alkaline Lake" polygons; any
    HydroLAKES polygon centred on one of them is a salt/soda lake, not
    freshwater, and is dropped.

    `ne_lakes` supplies the proper spelling of each lake's name: HydroLAKES
    stores bare ones ("Ontario", "Winnipeg"), Natural Earth stores the ones
    people actually use ("Lake Ontario", "Okanagan Lake").
    """
    r = shapefile.Reader(hydrolakes_path(), encoding="latin-1")
    fields = [f[0] for f in r.fields[1:]]
    i_area = fields.index("Lake_area")
    i_lon = fields.index("Pour_long")
    i_lat = fields.index("Pour_lat")
    i_name = fields.index("Lake_name")

    wanted = []
    for i, rec in enumerate(r.iterRecords()):
        lon, lat = rec[i_lon], rec[i_lat]
        if (WIN_LON[0] <= lon <= WIN_LON[1] and WIN_LAT[0] <= lat <= WIN_LAT[1]
                and float(rec[i_area]) >= MIN_LAKE_KM2):
            wanted.append((i, (rec[i_name] or "").strip()))
    sys.stderr.write("HydroLAKES >= %.0f km2 in window: %d\n"
                     % (MIN_LAKE_KM2, len(wanted)))

    alk_index = STRtree(alkaline) if alkaline else None

    # Natural Earth lakes, prepared for point-in-polygon name lookups
    ne_named = [(nm, g) for nm, g in
                ((ne_lake_name(a), g) for a, g in ne_lakes) if nm]
    ne_index = STRtree([g for _, g in ne_named])
    ne_prep = [prep(g) for _, g in ne_named]
    ne_pts = [g.representative_point() for _, g in ne_named]
    ne_pt_index = STRtree(ne_pts)

    gaz_pts, gaz_meta = read_geonames_water()
    gaz_index = STRtree(gaz_pts)

    polys, names = [], []
    segs, owners = [], []
    dropped = 0
    for i, hydro_name in wanted:
        sh = r.shape(i)
        g = shape(sh.__geo_interface__)
        if not g.is_valid:
            g = g.buffer(0)
        rp = g.representative_point()
        if alk_index is not None:
            if any(alkaline[k].covers(rp) for k in alk_index.query(rp)):
                dropped += 1
                continue

        # name it: the Natural Earth lake this polygon sits inside, else the
        # Natural Earth lake sitting inside this polygon, else the gazetteer
        # point inside it, else HydroLAKES' own bare name
        name = None
        for k in ne_index.query(rp):
            if ne_prep[k].covers(rp):
                name = ne_named[k][0]
                break
        gp = prep(g)
        if name is None:
            best = None
            for k in ne_pt_index.query(g):
                if gp.covers(ne_pts[k]):
                    a = ne_named[k][1].area
                    if best is None or a > best[0]:
                        best = (a, ne_named[k][0])
            if best:
                name = best[1]
        if name is None:
            best = None
            for k in gaz_index.query(g):
                if gp.covers(gaz_pts[k]):
                    pri, nm = gaz_meta[k]
                    key = (pri, gaz_pts[k].distance(rp))
                    if best is None or key < best[0]:
                        best = (key, nm)
            if best:
                name = best[1]
        names.append(name or hydro_name or "Unnamed lake")

        fid = len(polys)
        polys.append(g)
        shape_segments(sh, fid, segs, owners)
    sys.stderr.write("lakes kept: %d  [alkaline dropped: %d]\n"
                     % (len(polys), dropped))
    return (WaterLayer("lakes HydroLAKES", np.vstack(segs),
                       np.concatenate(owners)), polys, names)


# --------------------------------------------------------------------------
# naming (Natural Earth)
# --------------------------------------------------------------------------

NE_LAKE_NAME_KEYS = ("name", "name_en", "namealt", "name_alt", "label")


def ne_lake_name(attrs):
    for k in NE_LAKE_NAME_KEYS:
        v = (attrs.get(k) or "").strip()
        if v:
            return v
    return ""


class Namer(object):
    """Names the water body that owns a given point on a shoreline."""

    def __init__(self, feats, name_keys):
        self.feats = []
        for a, g in feats:
            nm = ""
            for k in name_keys:
                v = (a.get(k) or "").strip()
                if v:
                    nm = v
                    break
            if nm:
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
            # highest scalerank == most specific named body, so Salish Sea wins
            # over North Pacific Ocean and Hudson Bay over Arctic Ocean
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

CHECKS = [
    ("Vancouver", "BC"), ("Victoria", "BC"), ("Halifax", "NS"),
    ("St. John's", "NL"), ("Toronto", "ON"), ("Hamilton", "ON"),
    ("Thunder Bay", "ON"), ("Regina", "SK"), ("Saskatoon", "SK"),
    ("Winnipeg", "MB"), ("Kelowna", "BC"), ("Calgary", "AB"),
]


def main():
    fetch()

    with open(PLACES_PATH) as f:
        places = json.load(f)
    sys.stderr.write("places: %d\n" % len(places))
    pts = [(p["lat"], p["lon"]) for p in places
           if p.get("lat") is not None and p.get("lon") is not None]

    ne_lakes = read_ne("ne_10m_lakes") + read_ne("ne_10m_lakes_north_america")
    alkaline = [g for a, g in ne_lakes
                if (a.get("featurecla") or "") == "Alkaline Lake"]

    coast, land = load_coast(pts)
    lakes, lake_polys, lake_names = load_lakes(alkaline, ne_lakes)

    land_prep = [prep(g) for g in land]
    land_index = STRtree(land)
    lake_prep = [prep(g) for g in lake_polys]
    lake_index = STRtree(lake_polys)

    marine_namer = Namer(read_ne("ne_10m_geography_marine_polys"),
                         ("name", "name_en"))
    lake_namer = Namer(ne_lakes, NE_LAKE_NAME_KEYS)

    out = []
    for n, p in enumerate(places):
        lat, lon = p.get("lat"), p.get("lon")
        rec = {
            "name": p["name"],
            "prov": p["prov"],
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

        o_km, _, o_pt = coast.distance(lat, lon)
        if o_km is not None and not any(
                land_prep[i].covers(pt) for i in land_index.query(pt)):
            o_km, o_pt = 0.0, (lon, lat)

        l_km, l_fid, l_pt = lakes.distance(lat, lon)
        if l_km is not None:
            for i in lake_index.query(pt):
                if lake_prep[i].covers(pt):
                    l_km, l_fid, l_pt = 0.0, int(i), (lon, lat)
                    break

        rec["km_to_ocean"] = None if o_km is None else round(o_km, 1)
        rec["km_to_lake"] = None if l_km is None else round(l_km, 1)

        cands = []
        if o_km is not None:
            nm = marine_namer.nearest_name(o_pt[0], o_pt[1],
                                           (0.35, 1.0, 3.0, 8.0)) or "Ocean"
            cands.append((o_km, "ocean", nm))
        if l_km is not None:
            # the Natural Earth lake sitting at the closest point is the most
            # local answer; otherwise the name resolved for the whole polygon
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
        if (n + 1) % 100 == 0:
            sys.stderr.write("  %d/%d\n" % (n + 1, len(places)))

    with open(OUT_PATH, "w") as f:
        json.dump(out, f, indent=1)
        f.write("\n")

    # ---- check table -----------------------------------------------------
    by = {(r["name"], r["prov"]): r for r in out}
    hdr = "%-16s %-4s %12s %11s %-24s %-6s %8s %9s"
    print("")
    print(hdr % ("PLACE", "PROV", "KM_TO_OCEAN", "KM_TO_LAKE", "NEAREST_WATER",
                 "TYPE", "KM", "ON_WATER"))
    print("-" * 100)
    for key in CHECKS:
        r = by.get(key)
        if not r:
            print("%-16s %-4s   MISSING" % key)
            continue
        print(hdr % (r["name"], r["prov"], r["km_to_ocean"], r["km_to_lake"],
                     r["nearest_water_name"], r["nearest_water_type"],
                     r["km_to_water"], r["on_water"]))
    print("")
    got = sum(1 for r in out if r["km_to_water"] is not None)
    print("places with values: %d / %d" % (got, len(out)))
    print("nearest is ocean: %d | nearest is lake: %d"
          % (sum(1 for r in out if r["nearest_water_type"] == "ocean"),
             sum(1 for r in out if r["nearest_water_type"] == "lake")))
    print("on_water (<= %.0f km): %d"
          % (ON_WATER_KM, sum(1 for r in out if r["on_water"])))
    print("unnamed: %d"
          % sum(1 for r in out if r["nearest_water_name"] in
                (None, "Unnamed lake", "Ocean")))
    print("wrote %s" % OUT_PATH)


if __name__ == "__main__":
    main()
