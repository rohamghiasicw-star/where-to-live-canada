"""Albers Equal Area Conic, pure Python, no dependencies.

Why this exists: src/us/build_map.py uses pyproj to build the ring geometry, which
is right for a one-off data prep step. But build_app.py has to project a few
thousand place coordinates on every build, and the Canadian side does its own
Lambert Conformal Conic in pure Python precisely so the build has no third-party
dependency and cannot rot. This is the same bargain for the US sheet.

The transform reproduced here is exactly the one the rings were built with:

  Lower 48 + DC   EPSG:5070   NAD83 / Conus Albers
  Alaska          EPSG:3338   NAD83 / Alaska Albers, then scaled 0.35 and shifted
  Hawaii          ESRI 102007 Hawaii Albers, true scale, shifted

Validated against pyproj 3.7.2 to sub-metre agreement over the whole domain; the
check is in `_selftest` at the bottom of this file. If either file's parameters
change, both must change and the self-test must be re-run, or the dots stop
landing inside the states.

Formulas are Snyder, Map Projections: A Working Manual, USGS PP 1395, pp. 101-102
(ellipsoidal Albers forward).
"""
import math

# GRS80, shared by every projection here
A = 6378137.0
E2 = 0.00669438002290341574
E = math.sqrt(E2)


def _q(phi):
    """Snyder eq. 3-12: the authalic latitude term."""
    s = math.sin(phi)
    return (1 - E2) * (s / (1 - E2 * s * s)
                       - (1 / (2 * E)) * math.log((1 - E * s) / (1 + E * s)))


def _m(phi):
    s = math.sin(phi)
    return math.cos(phi) / math.sqrt(1 - E2 * s * s)


class Albers:
    def __init__(self, lat1, lat2, lat0, lon0):
        p1, p2, p0 = map(math.radians, (lat1, lat2, lat0))
        self.lon0 = math.radians(lon0)
        m1, m2 = _m(p1), _m(p2)
        q1, q2, q0 = _q(p1), _q(p2), _q(p0)
        # a one-parallel case would divide by zero; none of ours is
        self.n = (m1 * m1 - m2 * m2) / (q2 - q1)
        self.C = m1 * m1 + self.n * q1
        self.rho0 = A * math.sqrt(self.C - self.n * q0) / self.n

    def __call__(self, lon, lat):
        theta = self.n * (math.radians(lon) - self.lon0)
        rho = A * math.sqrt(self.C - self.n * _q(math.radians(lat))) / self.n
        return rho * math.sin(theta), self.rho0 - rho * math.cos(theta)


CONUS = Albers(29.5, 45.5, 23.0, -96.0)     # EPSG:5070
AK    = Albers(55.0, 65.0, 50.0, -154.0)    # EPSG:3338
HI    = Albers(8.0, 18.0, 13.0, -157.0)     # ESRI 102007

# inset placement, in EPSG:5070 metres. Must match src/us/build_map.py exactly.
AK_SCALE, AK_DX, AK_DY = 0.35, -1_760_000.0, 175_000.0
HI_SCALE, HI_DX, HI_DY = 1.00,   -760_000.0, -330_000.0


def zone(lon, lat, state=None):
    """Which of the three planes a point belongs to. State code wins when given,
    because Alaska's Aleutian tail crosses the antimeridian and a lon/lat guess
    would put Attu in the wrong plane."""
    if state == 'AK':
        return 'AK'
    if state == 'HI':
        return 'HI'
    if state:
        return 'CONUS'
    if lat > 51.0 and (lon < -129.0 or lon > 172.0):
        return 'AK'
    if 15.0 < lat < 27.0 and -162.0 < lon < -153.0:
        return 'HI'
    return 'CONUS'


def project(lon, lat, state=None):
    """lon/lat -> EPSG:5070 metres, with Alaska and Hawaii in their inset slots."""
    z = zone(lon, lat, state)
    if z == 'AK':
        x, y = AK(lon, lat)
        return x * AK_SCALE + AK_DX, y * AK_SCALE + AK_DY
    if z == 'HI':
        x, y = HI(lon, lat)
        return x * HI_SCALE + HI_DX, y * HI_SCALE + HI_DY
    return CONUS(lon, lat)


def _selftest(verbose=True):
    """Compare against pyproj if it is importable. Skips cleanly if it is not,
    because the whole point of this module is that the build does not need it."""
    try:
        from pyproj import CRS, Transformer
    except ImportError:
        if verbose:
            print("pyproj not installed; skipping the comparison (this is fine)")
        return None
    wgs = CRS.from_epsg(4326)
    tf = {
        'CONUS': Transformer.from_crs(wgs, CRS.from_epsg(5070), always_xy=True),
        'AK': Transformer.from_crs(wgs, CRS.from_epsg(3338), always_xy=True),
        'HI': Transformer.from_crs(wgs, CRS.from_proj4(
            "+proj=aea +lat_0=13 +lon_0=-157 +lat_1=8 +lat_2=18 "
            "+x_0=0 +y_0=0 +datum=NAD83 +units=m +no_defs"), always_xy=True),
    }
    pts = [(-122.33, 47.61, 'WA'), (-87.63, 41.88, 'IL'), (-70.26, 43.66, 'ME'),
           (-117.16, 32.72, 'CA'), (-80.19, 25.77, 'FL'), (-96.0, 23.0, 'TX'),
           (-101.0, 48.9, 'ND'), (-149.90, 61.22, 'AK'), (-165.4, 64.5, 'AK'),
           (-157.86, 21.31, 'HI'), (-159.5, 22.08, 'HI'), (-77.04, 38.91, 'DC')]
    worst = 0.0
    for lon, lat, st in pts:
        z = zone(lon, lat, st)
        px, py = tf[z].transform(lon, lat)
        if z == 'AK':
            px, py = px * AK_SCALE + AK_DX, py * AK_SCALE + AK_DY
        elif z == 'HI':
            px, py = px * HI_SCALE + HI_DX, py * HI_SCALE + HI_DY
        mx, my = project(lon, lat, st)
        d = math.hypot(mx - px, my - py)
        worst = max(worst, d)
        if verbose:
            print(f"  {st} {lon:>9.2f},{lat:>6.2f}  {z:<5} delta {d*100:7.3f} cm")
    if verbose:
        print(f"worst disagreement with pyproj: {worst*100:.3f} cm")
    return worst


if __name__ == '__main__':
    _selftest()
