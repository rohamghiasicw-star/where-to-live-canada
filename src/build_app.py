#!/usr/bin/env python3
"""Assemble the single-file app: data + map + fonts + css + js -> livable.html
Agent data files are optional; whatever has landed gets merged, the rest stays null."""
import json, math, os, re, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # repo root, this file lives in src/
D = lambda *p: os.path.join(ROOT, *p)

def load(p, default=None):
    try:
        with open(D(p)) as f: return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return default

# ---- base: climate carries name/prov/lat/lon/elev/climate/stations_used/smoke
places = load('data/climate.json')

# Drop treaty settlement lands (CSDTYPE "TWL") the way reserves were dropped:
# Tsawwassen Lands is First Nation treaty land, not a normal move-to place, and
# its +176.5% growth on a missing home value was gaming the ranking.
_cd = load('data/csd_coords.json') or {}
_drop = {(r.get('name'), r.get('prov')) for r in (load('data/census.json') or [])
         if (_cd.get(r.get('code')) or {}).get('type') == 'TWL'}
places = [p for p in places if (p.get('name'), p.get('prov')) not in _drop]

# ---- same Lambert projection the map sheet was built in
P1, P2, LAT0, LON0 = map(math.radians, (49.0, 77.0, 63.390675, -91.866666666))
def lcc(lon, lat):
    phi, lam = math.radians(lat), math.radians(lon)
    t = lambda p: math.tan(math.pi/4 + p/2)
    n = math.log(math.cos(P1)/math.cos(P2)) / math.log(t(P2)/t(P1))
    F = math.cos(P1)*(t(P1)**n)/n
    rho, rho0 = F/(t(phi)**n), F/(t(LAT0)**n)
    th = n*(lam - LON0)
    return rho*math.sin(th), rho0 - rho*math.cos(th)

# Fit the sheet to the inhabited band, not the full national extent. Canada reaches
# 83N but nobody in this survey lives past 64N, so a full-extent map spends most of
# the plate on empty arctic. Pad generously; the provinces bleed off the sheet edge
# the way they do on a real map series.
proj = [lcc(p['lon'], p['lat']) for p in places]
px_, py_ = [q[0] for q in proj], [q[1] for q in proj]
padx = (max(px_) - min(px_)) * 0.045
pady = (max(py_) - min(py_)) * 0.10
vx0, vx1 = min(px_) - padx, max(px_) + padx
vy0, vy1 = min(py_) - pady * 0.7, max(py_) + pady
sc = 1000 / (vx1 - vx0)
view_h = round((vy1 - vy0) * sc, 1)
for p, (qx, qy) in zip(places, proj):
    p['x'] = round((qx - vx0) * sc, 1)
    p['y'] = round((vy1 - qy) * sc, 1)

rings = load('data/canada_rings.json')
mapgeo = {
    'height': view_h,
    'prov': {n: [[[round((x - vx0) * sc, 1), round((vy1 - y) * sc, 1)] for x, y in r] for r in rs]
             for n, rs in rings['prov'].items()},
}

key = lambda n, pr: (n.strip().lower(), pr.strip().upper())
by = {key(p['name'], p['prov']): p for p in places}

def merge(fname, field, pick):
    """Merge an agent's file into places under `field`. Returns hit count."""
    rows = load(fname)
    if not rows: return 0
    if isinstance(rows, dict): rows = list(rows.values())
    hit = 0
    for r in rows:
        if not isinstance(r, dict) or 'name' not in r: continue
        k = key(r['name'], r.get('prov', ''))
        if k not in by: continue
        v = pick(r)
        if v: by[k][field] = v; hit += 1
    return hit

stats = {}

# population, income, housing: 2021 Census profile, census subdivision level
for r in (load('data/census.json') or []):
    k = key(r.get('name',''), r.get('prov',''))
    if k not in by: continue
    for f in ('pop','density','settlement_type','area_km2'):
        if r.get(f) is not None: by[k][f] = r[f]
    by[k]['csd'] = r.get('csd')
    cost = {
        'home_price': r.get('dwell_avg'),
        'home_price_median': r.get('dwell_median'),
        'rent_2br': r.get('rent_median'),
        'median_hh_income': r.get('median_hh_income'),
        'source': '2021 Census, census subdivision',
    }
    if any(v is not None for k2, v in cost.items() if k2 != 'source'):
        by[k]['cost'] = cost
    # what living there is actually like, all from the same census profile
    life = {f: r.get(f) for f in (
        'pop_change','median_age','unemployment','tenant_burden','owner_burden',
        'major_repairs_pct','immigrants_pct','visible_minority_pct','french_pct','bilingual_pct',
        'commute_car_pct','commute_transit_pct','commute_walk_pct','commute_bike_pct',
        'commute_short_pct','commute_long_pct')}
    if any(v is not None for v in life.values()):
        # one derived field: everything that is not a car
        cw = [life.get('commute_transit_pct'), life.get('commute_walk_pct'), life.get('commute_bike_pct')]
        life['carfree_pct'] = round(sum(x for x in cw if x is not None), 1) if any(x is not None for x in cw) else None
        by[k]['life'] = life
stats['census'] = sum(1 for p in places if p.get('pop') is not None)
stats['life'] = sum(1 for p in places if p.get('life'))

stats['politics'] = merge('data/politics.json', 'politics', lambda r: {
    'lean': r.get('lean'), 'lean_label': r.get('lean_label'),
    'riding': r.get('riding'), 'winner': r.get('riding_2021_winner'),
} if r.get('lean') is not None else None)

stats['prox'] = merge('data/proximity.json', 'prox', lambda r: {
    'nearest_big_city': r.get('nearest_big_city'),
    'km_to_big_city': r.get('km_to_big_city'),
    'drive_min_to_big_city': r.get('drive_min_to_big_city'),
    'routed': r.get('routed'), 'note': r.get('note'),
} if r.get('nearest_big_city') else None)

stats['vibe'] = merge('data/vibe.json', 'vibe', lambda r: {
    'blurb': r.get('blurb'), 'tags': r.get('vibe_tags'), 'outdoors': r.get('outdoors'),
    'walkable': r.get('walkable_downtown'), 'nature': r.get('nature_access'),
    'arts': r.get('arts_culture'),
} if r.get('vibe_tags') or r.get('outdoors') else None)

# lived experience: what residents actually say, from forums / local news / blogs
lived = 0
# Match on name AND province. Windsor exists in Ontario and Quebec, Stratford in
# Ontario and PEI: on name alone the Ontario research attached to the Quebec and
# PEI towns, because those sort first.
byname = {}
for p in places: byname[(p['name'].strip().lower(), p['prov'])] = p
# the research was done under the names the 129-place list used; the expansion
# renamed places to their census names (Dawson City -> Dawson)
for p in load('data/allplaces.json') or []:
    if p.get('alias'):
        t = byname.get((p['name'].strip().lower(), p['prov']))
        if t: byname.setdefault((p['alias'].strip().lower(), p['prov']), t)
for r in (load('data/lived.json') or []):
    p = byname.get(((r.get('name') or '').strip().lower(), r.get('prov')))
    if not p: continue
    p['lived'] = {
        'loved': r.get('loved'), 'hated': r.get('hated'),
        'honest_downside': r.get('honest_downside'),
        'quotes': [q for q in (r.get('quotes') or []) if q.get('quote') and q.get('source_url')],
        'sentiment': {k2: v for k2, v in (r.get('topic_sentiment') or {}).items() if v is not None},
        'confidence': r.get('confidence'),
        'evidence_count': r.get('evidence_count'), 'source_count': r.get('source_count'),
    }
    lived += 1
stats['lived'] = lived

# ---- trim payload: drop the raw monthly cache for elements the app only uses annually
for p in places:
    for el in ('days_rain','days_lt_m20','days_gt30','humidex30','sun','precip','snow'):
        c = p['climate'].get(el)
        if isinstance(c, dict) and el not in ('tmean',):
            p['climate'][el] = {'13': c.get('13')} if c.get('13') is not None else None
    for el in ('tmax','tmin'):
        c = p['climate'].get(el)
        if isinstance(c, dict): p['climate'][el] = {'13': c.get('13'), '1': c.get('1'), '7': c.get('7')}
    if p.get('smoke'): p['smoke'].pop('by_year', None)
    p['stations_used'] = {k2: v for k2, v in p['stations_used'].items() if k2 == 'tmean'}

# ---- assemble
html = open(D('app/index.html')).read()
fonts = open(D('fonts/faces.css')).read()
css  = open(D('app/style.css')).read()
js   = open(D('app/app.js')).read()

def put(marker, payload):
    global html
    i = html.index(marker)
    html = html[:i] + payload + html[i+len(marker):]

put('/*__DATA__*/', json.dumps(places, separators=(',', ':'), ensure_ascii=False))
put('/*__MAP__*/',  json.dumps(mapgeo, separators=(',', ':')))
put('/*__FONTS__*/', fonts)
put('/*__CSS__*/', css)
put('/*__JS__*/', js)

# index.html so GitHub Pages serves it at the repo root; the file is fully self-contained
# (fonts, data and map all inlined) so it also works opened straight off disk.
out = D('index.html')
open(out, 'w').write(html)
kb = os.path.getsize(out) / 1024
print(f"built {out}  {kb:.0f}KB")
print(f"  places        {len(places)}")
for k, v in stats.items():
    bar = '#' * round(v / len(places) * 24)
    print(f"  {k:9s} {v:3d}/129  {bar}")
missing = [k for k, v in stats.items() if v == 0]
if missing: print(f"  NOT YET LANDED: {', '.join(missing)}")

# keep the staging copy in lockstep with every build
import subprocess
subprocess.run(['python3', os.path.join(os.path.dirname(__file__), 'make_staging.py')])
