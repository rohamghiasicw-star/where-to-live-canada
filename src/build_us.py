#!/usr/bin/env python3
"""Assemble the US build: data/us/* -> us/index.html

Mirrors src/build_app.py, which does Canada. Agent data files are optional: whatever
has landed gets merged and the rest stays null, so this runs end to end from the
first day the place list exists.

The one piece of real logic here rather than in an agent is climate station
matching, because that is where the Canadian build went wrong twice and the fix
has to be identical:

  1. Stations are not where you live. Revelstoke's nearest published-normals
     station was 43 km away and 1,431 m up a mountain, and using it reported
     1,388 cm of alpine snowpack instead of the town's 425 cm. So elevation is
     part of the distance metric, not an afterthought.

  2. One home station per place. Vancouver briefly took its temperature from the
     airport and its snow from a different station, which is a climate that exists
     nowhere. So a place gets ONE station carrying every element together.
"""
import json, math, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'us'))
from countries import US as CFG, other as other_country
from albers import project

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = lambda *p: os.path.join(ROOT, *p)


def load(p, default=None):
    try:
        with open(D(p)) as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return default


places = load('data/us/places.json')
if not places:
    sys.exit("data/us/places.json has not landed yet; nothing to build.")

# Territories have no ring in the state geometry (Natural Earth files them as
# admin-0), so a place there would draw with nothing under it.
TERRITORIES = {'PR', 'VI', 'GU', 'AS', 'MP'}
dropped_terr = [p for p in places if p.get('state') in TERRITORIES]
places = [p for p in places if p.get('state') not in TERRITORIES]

# Two places carry a Census parenthetical that reads as a glitch on a result card.
# The Canadian build does the same thing for border-split "(Part)" names.
ALIAS = {'San Buenaventura (Ventura)': 'Ventura',
         'El Paso de Robles (Paso Robles)': 'Paso Robles',
         'Urban Honolulu': 'Honolulu',
         'Nashville-Davidson': 'Nashville',
         'Louisville/Jefferson County': 'Louisville',
         'Athens-Clarke County': 'Athens',
         'Boise City': 'Boise'}
for p in places:
    if p['name'] in ALIAS:
        p['name'] = ALIAS[p['name']]

# The app keys everything on `prov`; for the US that holds the two-letter state.
for p in places:
    p['prov'] = p['state']

# ---- project, then fit the sheet the same way the Canadian one does
for p in places:
    p['_x'], p['_y'] = project(p['lon'], p['lat'], p['state'])

rings = load(CFG['rings'])
key_rings = rings[CFG['rings_key']] if rings else {}
rx = [pt[0] for v in key_rings.values() for ring in v for pt in ring]
ry = [pt[1] for v in key_rings.values() for ring in v for pt in ring]
# fit to the GEOMETRY, not to the places: the outline is what the eye registers,
# and fitting to points would crop Maine and the Florida keys off the sheet.
padx = (max(rx) - min(rx)) * CFG['pad']['x']
pady = (max(ry) - min(ry)) * CFG['pad']['y']
vx0, vx1 = min(rx) - padx, max(rx) + padx
vy0, vy1 = min(ry) - pady * CFG['pad']['ybot'], max(ry) + pady
sc = 1000.0 / (vx1 - vx0)
view_h = round((vy1 - vy0) * sc, 1)
for p in places:
    p['x'] = round((p.pop('_x') - vx0) * sc, 1)
    p['y'] = round((vy1 - p.pop('_y')) * sc, 1)

mapgeo = {
    'height': view_h,
    'prov': {n: [[[round((x - vx0) * sc, 1), round((vy1 - y) * sc, 1)] for x, y in r] for r in rs]
             for n, rs in key_rings.items()},
}

key = lambda n, pr: (str(n).strip().lower(), str(pr).strip().upper())
by = {key(p['name'], p['prov']): p for p in places}
by_geoid = {str(p['geoid']): p for p in places}
stats = {}

# ---- demographics already live on the place records from the Census step
DEMO_FIELDS = ('children_pct', 'working_age_pct', 'seniors_pct',
               'males_per_100_females', 'never_married_pct')
for p in places:
    # pull the demographic fields out BEFORE the catch-all sweep below. That sweep
    # takes every key ending in _pct, which silently swallowed children_pct,
    # seniors_pct and never_married_pct, so the Kids and Single people questions
    # scored null for all 4,197 places and only showed up as a coverage penalty.
    demo = {k: p.pop(k) for k in DEMO_FIELDS if k in p and p[k] is not None}
    life = {k: p.pop(k) for k in list(p.keys()) if k.endswith('_pct')}
    if p.get('median_age') is not None:
        life['median_age'] = p['median_age']
    if life:
        cw = [life.get('commute_transit_pct'), life.get('commute_walk_pct'), life.get('commute_bike_pct')]
        life['carfree_pct'] = round(sum(x for x in cw if x is not None), 1) \
            if any(x is not None for x in cw) else None
        life['pop_change'] = life.pop('pop_change_pct', None)
        life['unemployment'] = life.pop('unemployment_pct', None)
        life['immigrants_pct'] = life.pop('foreign_born_pct', None)
        p['life'] = life
    cost = {'home_price': p.pop('home_value_median', None),
            'rent_2br': p.pop('rent_median', None),
            'median_hh_income': p.pop('median_hh_income', None),
            'source': 'American Community Survey 5-year'}
    if any(v is not None for k2, v in cost.items() if k2 != 'source'):
        p['cost'] = cost
    pp = p.get('pop')
    if pp:
        p['settlement_type'] = ('big city' if pp >= 500000 else 'mid city' if pp >= 100000 else
                                'small city' if pp >= 25000 else 'town' if pp >= 5000 else 'village')
    if demo:
        p['demo'] = demo
stats['census'] = sum(1 for p in places if p.get('pop') is not None)
stats['life'] = sum(1 for p in places if p.get('life'))
stats['demo'] = sum(1 for p in places if p.get('demo'))


# ---- climate: one home station per place, chosen on distance AND elevation
def hav(a, b, c, d):
    R = 6371.0
    dp, dl = math.radians(c - a), math.radians(d - b)
    x = (math.sin(dp / 2) ** 2
         + math.cos(math.radians(a)) * math.cos(math.radians(c)) * math.sin(dl / 2) ** 2)
    return 2 * R * math.asin(math.sqrt(x))


ELEMS = ('tmean', 'tmax', 'tmin', 'precip', 'snow')
_st = load('data/us/noaa_stations.json') or []
# the file is {meta, stations}; meta records the units, the missing-value policy and
# that the US normals publish no bright-sunshine element, so there is no `sun` column
stations = _st.get('stations', []) if isinstance(_st, dict) else _st
# true place elevations if that step has landed; otherwise the local-profile guard
# below carries the job on its own
_elev = load('data/us/elevation.json') or {}
for p in places:
    e = _elev.get(str(p.get('geoid')))
    if e is not None:
        p['elev_m'] = e
if stations:
    # bucket stations by rounded degree so this is not 3000 x 10000 comparisons
    grid = {}
    for s in stations:
        if s.get('lat') is None or s.get('lon') is None:
            continue
        grid.setdefault((round(s['lat']), round(s['lon'])), []).append(s)

    def near_stations(lat, lon, deg=1):
        out = []
        for dla in range(-deg, deg + 1):
            for dlo in range(-deg, deg + 1):
                out += grid.get((round(lat) + dla, round(lon) + dlo), [])
        return out

    matched = 0
    for p in places:
        cands = near_stations(p['lat'], p['lon'])
        if not cands:
            cands = near_stations(p['lat'], p['lon'], 3)
        # What elevation should this place's climate be at? If the true place
        # elevation is known, use it. Otherwise take the median of the nearby
        # stations, which is the whole point: a valley town surrounded by eight
        # stations at 200-400 m and one at 1,900 m should not take the outlier.
        # Without this the Revelstoke failure recurs, and it recurs silently,
        # because an alpine snowfall figure looks like a real number.
        # Local station elevation, computed either way, because it is also the
        # sanity check on the measured place elevation below.
        _wz = [(hav(p['lat'], p['lon'], c['lat'], c['lon']), c['elev_m'])
               for c in cands if c.get('elev_m') is not None]
        _wz.sort()
        _near = [z for km_, z in _wz[:5] if km_ <= 40] or [z for _, z in _wz[:3]]
        _local = sorted(_near)[len(_near) // 2] if _near else None

        if p.get('elev_m') is not None:
            ref_elev = p['elev_m']           # measured, and right for almost everywhere
            # But places.json carries the Census polygon's INTERNAL POINT, not the
            # populated core, and for a giant municipality that point can sit up a
            # mountain. Anchorage covers 4,421 km2 and its internal point reads
            # 1,216 m while the city is at about 30 m. Trusting that would invert
            # this whole guard: it would go looking for an alpine station. Weather
            # stations cluster where people are, so a sharp disagreement with the
            # local station profile means the internal point is not the town.
            if _local is not None and abs(ref_elev - _local) > 400:
                ref_elev = _local
        else:
            # Proxy, and a biased one in exactly the terrain that matters: in
            # mountains the median of nearby stations is dragged upward by the
            # mountain stations, so Indio (genuinely 6 m BELOW sea level) reads a
            # local profile of 602 m because San Jacinto rises 3,300 m beside it.
            # Taking the nearest handful rather than everything within 60 km keeps
            # the reference closer to the valley floor the town actually sits on.
            ref_elev = _local

        best, best_cost = None, None
        for s in cands:
            km = hav(p['lat'], p['lon'], s['lat'], s['lon'])
            if km > 120:
                continue
            comp = (s.get('completeness') or {}).get('tmean', 0)
            if comp < 6:              # a half-empty record is not a climate
                continue
            # 100 m of elevation costs the same as 8 km of ground distance
            dz = 0.0 if (ref_elev is None or s.get('elev_m') is None) \
                else abs(s['elev_m'] - ref_elev)
            cs = s.get('completeness') or {}
            # A missing precipitation record is a real loss, a missing snow record
            # less so. But weighting "has more elements" too heavily is itself a
            # trap: it hands Phoenix to a 16-year co-op gauge that happens to log
            # snow, over Sky Harbor's 27-year record 13 km closer that does not.
            # Snow is cheap here for that reason.
            # Whether a missing snow record matters depends on where you are. Phoenix
            # averages no snow, so preferring a gauge that happens to log snow is
            # actively wrong there: it took Phoenix to a station 2 km farther out and
            # cost it the 27-year Sky Harbor record. The station's own January mean
            # answers the question without needing the place's climate first.
            _jan = (s.get('tmean') or {}).get('1')
            snow_matters = _jan is not None and _jan <= 6.0
            gap = (0 if cs.get('precip', 0) >= 6 else 45) \
                + (6 if (snow_matters and cs.get('snow', 0) < 6) else 0)
            # A value that exists is not the same as a value measured here. NCEI
            # flags 5,714 stations' precipitation as E, statistically estimated from
            # neighbours, and treating that as equal to a 30-year measured record is
            # the Revelstoke mistake in a quieter form.
            QUAL = {'S': 0, 'R': 22, 'P': 14, 'E': 40, 'C': 8, 'Q': 8}
            q = s.get('quality') or {}
            qpen = QUAL.get(q.get('tmean'), 0) + QUAL.get(q.get('precip'), 0) * 0.4
            yrs = (s.get('years') or {}).get('tmean')
            ypen = 0 if yrs is None else max(0, 30 - yrs) * 1.5
            cost = km + dz / 100.0 * 8.0 + (12 - comp) * 4.0 + gap + qpen + ypen
            if best_cost is None or cost < best_cost:
                best, best_cost = s, cost
        if not best:
            continue
        p['climate'] = {e: best.get(e) for e in ELEMS if best.get(e)}
        # NCEI omits the snow column entirely for stations that do not measure snow,
        # which in the Sun Belt is because there is none. Leaving that as unknown made
        # the Snow question drop 653 places, so someone asking for as little snow as
        # possible was denied exactly the places that have none. Where the January
        # mean is comfortably above freezing, a missing snow record is read as zero
        # and flagged, rather than left as a hole or quietly filled.
        _j = (best.get('tmean') or {}).get('1')
        if p['climate'].get('snow') is None and _j is not None and _j > 8.0:
            p['climate']['snow'] = {'13': 0.0}
            p['climate']['snow_inferred'] = True
        p['stations_used'] = {'tmean': {
            'id': best.get('id'), 'name': best.get('name'),
            'km': round(hav(p['lat'], p['lon'], best['lat'], best['lon']), 1),
            'elev_m': best.get('elev_m'),
            'ref_elev_m': None if ref_elev is None else round(ref_elev, 1),
            'quality': (best.get('quality') or {}).get('tmean'),
            'years': (best.get('years') or {}).get('tmean'),
        }}
        matched += 1
    stats['climate'] = matched

# ---- smoke: sample the gridded fire-attributed surface
sg = load('data/us/smoke_grid.json')
if sg and sg.get('values'):
    def sample(lat, lon):
        i = int(round((lat - sg['lat0']) / sg['dlat']))
        j = int(round((lon - sg['lon0']) / sg['dlon']))
        if 0 <= i < sg['nlat'] and 0 <= j < sg['nlon']:
            return sg['values'][i][j]
        return None
    n = 0
    for p in places:
        v = sample(p['lat'], p['lon'])
        if v is not None:
            p['smoke'] = {'mean_ugm3': round(v, 2), 'units': sg.get('units'),
                          'years': sg.get('years')}
            n += 1
    stats['smoke'] = n

# ---- politics: place -> county -> lean
pc = load('data/us/place_county.json') or {}
_polraw = load('data/us/politics.json') or {}
# the county file is keyed by 5-digit FIPS with the leading zero intact ('01001').
# Losing that zero silently mismaps every Alabama and Alaska county, so keys are
# kept as strings throughout and never passed through int().
if isinstance(_polraw, dict):
    pol = {str(k).zfill(5): v for k, v in _polraw.items()}
else:
    pol = {str(r.get('fips', r.get('county_fips'))).zfill(5): r for r in _polraw}
if pc and pol:
    n = 0
    for p in places:
        ent = pc.get(str(p['geoid']))
        # a place straddling county lines carries every county it touches plus the
        # one holding the largest share of its population; take that one and record
        # that the lean is a partial picture.
        if isinstance(ent, dict):
            fips, multi = ent.get('county'), bool(ent.get('multi_county'))
        else:
            fips, multi = ent, False
        r = pol.get(str(fips).zfill(5)) if fips is not None else None
        if not r or r.get('lean') is None:
            continue
        p['politics'] = {'lean': r['lean'], 'riding': r.get('county_name'),
                         'winner': r.get('lean_label'), 'multi_county': multi or None}
        n += 1
    stats['politics'] = n

# ---- the country-agnostic joins, keyed on name+state
for fname, field, fields in (
    ('data/us/civic.json', 'civic', ('has_pro_team', 'pro_league_count', 'teams',
                                     'rapid_transit', 'transit_type', 'transit_name')),
    ('data/us/water.json', 'water', ('km_to_water', 'km_to_ocean', 'km_to_lake',
                                     'nearest_water_name', 'nearest_water_type', 'on_water')),
    ('data/us/osm.json', 'osm', ('soccer_pitches', 'churches', 'mosques', 'synagogues',
                                 'gurdwaras', 'temples_hindu', 'temples_buddhist',
                                 'worship_total', 'ice_rinks', 'radius_km')),
    ('data/us/proximity.json', 'prox', ('nearest_big_city', 'km_to_big_city',
                                        'drive_min_to_big_city', 'routed')),
):
    rows = load(fname) or []
    n = 0
    for r in rows:
        k = key(r.get('name', ''), r.get('state', r.get('prov', '')))
        if k not in by:
            continue
        v = {f: r.get(f) for f in fields if r.get(f) is not None}
        if v:
            by[k][field] = v
            n += 1
    stats[field] = n

# ---- trim the payload the same way the Canadian build does
for p in places:
    c = p.get('climate') or {}
    for el in ('precip', 'snow'):
        if isinstance(c.get(el), dict):
            c[el] = {'13': c[el].get('13')} if c[el].get('13') is not None else None
    for el in ('tmax', 'tmin'):
        if isinstance(c.get(el), dict):
            c[el] = {'13': c[el].get('13'), '1': c[el].get('1'), '7': c[el].get('7')}
    for junk in ('land_area_km2', 'median_age', 'geoid'):
        p.pop(junk, None)
    st = (p.get('stations_used') or {}).get('tmean')
    if st:
        st.pop('ref_elev_m', None)     # audit field, not something a reader sees

from politics_scale import calibrate as _cal
CFG['politics'] = _cal([v.get('lean') for v in pol.values()]) or \
    dict(left=-50.0, centre=42.0, right=80.0, tol=43.0)
print("  politics scale", CFG['politics'])

# ---- assemble, sharing the Canadian shell
html = open(D('app/index.html')).read()
N = len(places)
smallest = min(places, key=lambda p: p.get('pop') or 9e9)
html = html.replace('<!--__HEADNOTE__-->', open(D('app/head.us.html')).read())
html = html.replace('<!--__FOOT__-->', open(D('app/foot.us.html')).read())
html = re.sub(r'all <b>\d+ places in __COUNTRY__</b>', 'all <b>%d places in __COUNTRY__</b>' % N, html)
html = re.sub(r'<b>\d+</b> cities and towns', '<b>%d</b> cities and towns' % N, html)
html = re.sub(r'Residents have been researched for \d+ of \d+ places',
              'Residents have been researched for 0 of %d places' % N, html)
# same self-healing idea as the Canadian build: the headnote states facts about the
# list, so it is computed from the list rather than typed and left to drift.
_smallpop = int(smallest.get('pop') or 0)
html = re.sub(r'New York down to <b>[^<]*</b>',
              'New York down to <b>%s, %s</b>' % (smallest['name'], smallest['prov']), html)
html = re.sub(r'where [\d,]+ people live', 'where %s people live' % format(_smallpop, ','), html)
html = html.replace('__SOURCES__', CFG['meta_sources'])
html = html.replace('__FINDHINT__', CFG['find_hint'])
html = html.replace('__COUNTRY__', CFG['country'])
_o = other_country(CFG['cc'])
html = html.replace('<!--__SWITCH__-->',
    '  <a class="cswitch" href="%s">Looking at <b>%s</b>. Switch to <b>%s</b> &rsaquo;</a>'
    % (_o['href'], CFG['country'], _o['label']))

def put(marker, payload):
    global html
    i = html.index(marker)
    html = html[:i] + payload + html[i + len(marker):]

put('/*__CFG__*/', json.dumps({k: v for k, v in CFG.items()
    if k in ('cc', 'country', 'adjective', 'unit', 'riding_label', 'sources',
             'prov_line', 'detail_note', 'climate_period', 'pop_year', 'census_year',
             'vote_year', 'growth', 'politics')}, separators=(',', ':'), ensure_ascii=False))
put('/*__DATA__*/', json.dumps(places, separators=(',', ':'), ensure_ascii=False))
put('/*__MAP__*/', json.dumps(mapgeo, separators=(',', ':')))
put('/*__FONTS__*/', open(D('fonts/faces.css')).read())
put('/*__CSS__*/', open(D('app/style.css')).read())
put('/*__JS__*/', open(D('app/app.js')).read())

os.makedirs(D(os.path.dirname(CFG['out'])), exist_ok=True)
out = D(CFG['out'])
open(out, 'w').write(html)
print("built %s  %.0fKB" % (out, os.path.getsize(out) / 1024))

# staging copy, same banner treatment the Canadian build gets, so /us/ and
# /staging/us/ are never confused for each other
_banner = ('<div style="background:#B33A1E;color:#fff;font:600 12px/1.35 system-ui,sans-serif;'
           'padding:7px 14px;text-align:center;letter-spacing:.02em">'
           'STAGING &middot; work in progress, may be rough &middot; '
           '<a href="../" style="color:#fff">the stable version is here &rarr;</a></div>')
_m = re.search(r'<div class="sheet"[^>]*>', html)
if not _m:
    raise SystemExit("build_us: could not find the root div to anchor the staging banner")
_stg = html[:_m.start()] + _banner + html[_m.start():]
_stg = re.sub(r'<title>([^<]*)</title>', lambda t: '<title>[STAGING] ' + t.group(1) + '</title>',
              _stg, count=1)
# the country switch inside staging should stay inside staging
_stg = _stg.replace('<a class="cswitch" href="canada/"', '<a class="cswitch" href="canada/"')
os.makedirs(D(os.path.dirname(CFG['staging'])), exist_ok=True)
open(D(CFG['staging']), 'w').write(_stg)
print("staging %s  %.0fKB" % (CFG['staging'], os.path.getsize(D(CFG['staging'])) / 1024))
print("  places    %d   (%d territory places dropped: no map geometry)"
      % (len(places), len(dropped_terr)))
for k, v in sorted(stats.items()):
    bar = '#' * round(v / max(1, len(places)) * 24)
    print("  %-9s %4d/%d  %s" % (k, v, len(places), bar))
missing = [k for k in ('climate', 'smoke', 'politics', 'civic', 'water', 'osm', 'prox')
           if not stats.get(k)]
if missing:
    print("  NOT YET LANDED: " + ', '.join(missing))
