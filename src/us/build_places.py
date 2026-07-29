#!/usr/bin/env python3
"""US place spine for the app: name, state, coordinates, land area and ACS
demographics for every US place at or above a population floor.

Everything downstream joins to this file, so the contract is: GEOID is the key,
names are display-only, and a value that is not published stays null.

Hard-won notes, each one a real bug this script now prevents:

* JOIN ON GEOID, NEVER ON NAMES. There are 32 "Springfield"s and two
  "Boqueron comunidad"s in the same state (PR). The 7-digit state+place FIPS is
  the only stable key. Names here are cosmetic output, never a join column.

* api.census.gov's DATA endpoints now 302 to /data/missing_key.html for every
  query, keyed or not, so `for=place:*&in=state:*` cannot be used any more.
  The METADATA endpoints (variables.json, groups/<T>.json) are still open, so
  variable IDs are still resolved from the Census's own metadata - never from
  memory - and the actual numbers come from the key-free bulk paths:
  the ACS table-based Summary File on www2.census.gov, and data.census.gov's
  table endpoint for the 2020 Decennial (verified against published counts).

* ENCODING. The 2024 Gazetteer place file is UTF-8. Older vintages ship latin-1,
  which is why the read is explicit and asserted rather than trusted: read
  latin-1 bytes as UTF-8 and "Espanola" silently loses its tilde while the run
  still reports success. Names are then NFC-normalized, because Utqiagvik
  arrives decomposed as "g" + U+0307 and would otherwise sort and compare wrong.

* NAME CLEANING IS DRIVEN BY THE LSAD CODE, not by string sniffing. The
  Gazetteer NAME is "<proper name> <LSAD text>", and the LSAD text is lowercase
  while the name keeps its capitals. So "Canon City city" loses exactly one
  trailing lowercase " city" and keeps the capitalised "City"; "Lake City city"
  becomes "Lake City". Every row is asserted to end with its LSAD's text, so a
  new LSAD code in a future vintage fails loudly instead of silently mangling.

* GEOGRAPHY VINTAGE (the Louisville trap). pop_change_pct compares two dates,
  so both ends must describe the same territory. In 2020-vintage geography the
  Louisville "balance" place was 386,884 with a separate legacy "Louisville
  city" of 246,161 beside it; by 2024 the legacy place went nonfunctioning and
  its territory folded into the balance. Differencing the two vintages reports
  +62% growth for a city that barely moved. So pop_change_pct is nulled wherever
  the 2020 and current geographies are not comparable - detected from an
  independent Census restatement of the same 2020 count on current boundaries
  (Population Estimates base) for incorporated places, and from land-area drift
  between the 2020 and 2024 Gazetteers for CDPs, which have no restatement.

* SUPPRESSION. ACS medians for thin samples arrive as -666666666, not as blank.
  Anything negative in an estimate column becomes null. No national average, no
  interpolation, no carry-forward: a missing value is missing.

* PERCENT DENOMINATORS. Every share is divided by the universe the Census
  publishes for that table, asserted against groups/<T>.json at run time.
  Marital status is population 15+, employment is 16+, commute mode is workers
  16+, and commute duration is workers 16+ who did not work from home. Dividing
  any of those by total population produces plausible-looking nonsense.

* RELIGION is not in here because the US Census is barred from asking about it
  (13 U.S.C. 221). The Canadian build has religion from the 2021 Census; there
  is no US equivalent at place level, so the field is absent rather than guessed.

Run:  python3 src/us/build_places.py
Cache: $LIVABLE_US_CACHE (default /tmp/livable_us_cache). Downloads are ~700MB
of ACS table files streamed and filtered to place rows on the way in.
"""
import json, os, re, csv, sys, glob, time, struct, unicodedata, zipfile, tempfile
import urllib.request

ACS_YEAR   = 2024          # latest ACS 5-year available (2020-2024)
GAZ_YEAR   = 2024          # matched to the ACS vintage on purpose: same TIGER
                           # geography means the GEOIDs line up exactly. A 2025
                           # Gazetteer exists but would add places the ACS has
                           # no data for.
DEC_YEAR   = 2020
POP_FLOOR  = 10_000        # the emitted cutoff; the report prints the others
THRESHOLDS = (5_000, 10_000, 15_000, 20_000, 25_000, 50_000)

ROOT  = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT   = os.path.join(ROOT, 'data', 'us', 'places.json')
CACHE = os.environ.get('LIVABLE_US_CACHE', os.path.join(tempfile.gettempdir(), 'livable_us_cache'))
os.makedirs(CACHE, exist_ok=True)

UA = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
                    'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36'}

def fetch(url, dest, binary=True, tries=4, line_filter=None):
    """Cached download. line_filter keeps only matching lines (plus the header),
    which is how 200MB ACS table files become 3MB place files without ever
    landing the full thing on disk."""
    p = os.path.join(CACHE, dest)
    if os.path.exists(p) and os.path.getsize(p) > 0:
        return p
    os.makedirs(os.path.dirname(p), exist_ok=True)
    for a in range(tries):
        try:
            req = urllib.request.Request(url, headers=UA)
            with urllib.request.urlopen(req, timeout=300) as r, open(p + '.part', 'wb') as f:
                if line_filter is None:
                    while True:
                        b = r.read(1 << 20)
                        if not b: break
                        f.write(b)
                else:
                    first = True
                    for line in r:
                        if first or line.startswith(line_filter):
                            f.write(line); first = False
            os.replace(p + '.part', p)
            return p
        except Exception as e:
            if a == tries - 1: raise
            print(f"  retry {dest}: {str(e)[:60]}"); time.sleep(3)

def getjson(url, dest):
    return json.load(open(fetch(url, dest), encoding='utf-8'))

def rnd(v, n=1):
    return None if v is None else round(v, n)

def pct(num, den):
    """A share of its published universe. Either side missing, or a zero
    universe, means the share does not exist - not zero."""
    if num is None or den in (None, 0): return None
    return round(num / den * 100, 1)


# ---------------------------------------------------------------- 1. Gazetteer
# Official LSAD (legal/statistical area description) text per code. Hardcoded
# because the small codes have too few rows to infer from, then asserted against
# every single row so a wrong entry cannot pass silently.
LSAD_SUFFIX = {
    '00': None,                    # consolidated-city balances; handled below
    '21': 'borough',      '25': 'city',              '35': 'metro township',
    '37': 'municipality', '43': 'town',              '47': 'village',
    '53': 'city and borough', '55': 'comunidad',     '57': 'CDP',
    '62': 'zona urbana',
    'CG': 'consolidated government', 'CN': 'corporation',
    'MG': 'metropolitan government', 'UC': 'urban county',
    'UG': 'unified government',
}
# For LSAD 00 the government form is inside the NAME itself. Longest first so
# "metropolitan government" is not shortened to "government" by a prefix match.
GOV_FORMS = (' metropolitan government', ' consolidated government',
             ' unified government', ' metro government', ' city')

def clean_name(name, lsad):
    n = re.sub(r'\s*\(balance\)$', '', name)
    suf = LSAD_SUFFIX[lsad]
    if suf is not None:
        assert n.endswith(' ' + suf), f"LSAD {lsad} name does not end in {suf!r}: {name!r}"
        n = n[:-(len(suf) + 1)]
    else:
        for g in GOV_FORMS:
            if n.endswith(g): n = n[:-len(g)]; break
    return unicodedata.normalize('NFC', n.strip())

def read_gazetteer(year):
    """Returns {geoid: row}. Encoding is checked, not assumed: a latin-1 file
    read as UTF-8 is the failure that turns Espanola into Espa?ola."""
    url = (f'https://www2.census.gov/geo/docs/maps-data/data/gazetteer/'
           f'{year}_Gazetteer/{year}_Gaz_place_national.zip')
    txt = os.path.join(CACHE, f'{year}_Gaz_place_national.txt')
    if not os.path.exists(txt):
        z = fetch(url, f'gaz_place_{year}.zip')
        with zipfile.ZipFile(z) as zf:
            inner = [n for n in zf.namelist() if n.endswith('.txt')][0]
            with zf.open(inner) as src, open(txt, 'wb') as dst: dst.write(src.read())
    raw = open(txt, 'rb').read()
    try:
        text = raw.decode('utf-8'); enc = 'utf-8'
    except UnicodeDecodeError:
        text = raw.decode('latin-1'); enc = 'latin-1'
    lines = text.splitlines()
    hdr = [h.strip() for h in lines[0].split('\t')]
    rows = {}
    for line in lines[1:]:
        if not line.strip(): continue
        d = dict(zip(hdr, [x.strip() for x in line.split('\t')]))
        rows[d['GEOID']] = d
    print(f"  {year} Gazetteer: {len(rows)} places, encoding={enc}")
    return rows


# ------------------------------------------- 2. ACS variable IDs, from metadata
# The variables are named by their PUBLISHED LABEL, and the IDs are looked up in
# the Census's own metadata. Nothing here is an ID typed from memory.
UNIVERSE = {          # asserted against groups/<T>.json before any arithmetic
    'B01001': 'Total population',
    'B01002': None,
    'B01003': None,
    'B19013': 'Households',
    'B25077': 'Owner-occupied housing units',
    'B25064': 'Renter-occupied housing units paying cash rent',
    'B23025': 'Population 16 years and over',
    'B12001': 'Population 15 years and over',
    'B05002': 'Total population',
    'B03002': 'Total population',
    'B03003': 'Total population',
    'B08301': 'Workers 16 years and over',
    'B08303': 'Workers 16 years and over who did not work from home',
}
UNDER18_AGES = ('Under 5 years', '5 to 9 years', '10 to 14 years', '15 to 17 years')
SENIOR_AGES  = ('65 and 66 years', '67 to 69 years', '70 to 74 years',
                '75 to 79 years', '80 to 84 years', '85 years and over')

def resolve_variables():
    meta = getjson(f'https://api.census.gov/data/{ACS_YEAR}/acs/acs5/variables.json',
                   f'acs_vars_{ACS_YEAR}.json')['variables']
    est = {k: v for k, v in meta.items()
           if k.endswith('E') and v.get('group') in UNIVERSE and not v.get('predicateOnly')}

    def by_label(group, label):
        hits = [k for k, v in est.items() if v['group'] == group and v['label'] == label]
        assert len(hits) == 1, f"{group} {label!r} matched {hits}"
        return hits[0]

    def only(group):
        hits = [k for k, v in est.items() if v['group'] == group]
        assert len(hits) == 1, f"{group} has {len(hits)} estimate variables, expected 1"
        return hits[0]

    V = {
        'pop':              only('B01003'),
        'median_age':       by_label('B01002', 'Estimate!!Median age --!!Total:'),
        'median_hh_income': only('B19013'),
        'home_value_median':only('B25077'),
        'rent_median':      only('B25064'),
        'lf_civilian':      by_label('B23025', 'Estimate!!Total:!!In labor force:!!Civilian labor force:'),
        'lf_unemployed':    by_label('B23025', 'Estimate!!Total:!!In labor force:!!Civilian labor force:!!Unemployed'),
        'age_total':        by_label('B01001', 'Estimate!!Total:'),
        'male_total':       by_label('B01001', 'Estimate!!Total:!!Male:'),
        'female_total':     by_label('B01001', 'Estimate!!Total:!!Female:'),
        'married_total':    by_label('B12001', 'Estimate!!Total:'),
        'never_m':          by_label('B12001', 'Estimate!!Total:!!Male:!!Never married'),
        'never_f':          by_label('B12001', 'Estimate!!Total:!!Female:!!Never married'),
        'nativity_total':   by_label('B05002', 'Estimate!!Total:'),
        'foreign_born':     by_label('B05002', 'Estimate!!Total:!!Foreign-born:'),
        'race_total':       by_label('B03002', 'Estimate!!Total:'),
        'nh_white':         by_label('B03002', 'Estimate!!Total:!!Not Hispanic or Latino:!!White alone'),
        'hisp_total':       by_label('B03003', 'Estimate!!Total:'),
        'hispanic':         by_label('B03003', 'Estimate!!Total:!!Hispanic or Latino'),
        'mode_total':       by_label('B08301', 'Estimate!!Total:'),
        'mode_car':         by_label('B08301', 'Estimate!!Total:!!Car, truck, or van:'),
        'mode_transit':     by_label('B08301', 'Estimate!!Total:!!Public transportation:'),
        'mode_bike':        by_label('B08301', 'Estimate!!Total:!!Bicycle'),
        'mode_walk':        by_label('B08301', 'Estimate!!Total:!!Walked'),
        'time_total':       by_label('B08303', 'Estimate!!Total:'),
    }
    for sex in ('Male', 'Female'):
        for a in UNDER18_AGES:
            V[f'u18_{sex}_{a}'] = by_label('B01001', f'Estimate!!Total:!!{sex}:!!{a}')
        for a in SENIOR_AGES:
            V[f'a65_{sex}_{a}'] = by_label('B01001', f'Estimate!!Total:!!{sex}:!!{a}')
    for a in ('Less than 5 minutes', '5 to 9 minutes', '10 to 14 minutes'):
        V[f'short_{a}'] = by_label('B08303', f'Estimate!!Total:!!{a}')
    for a in ('45 to 59 minutes', '60 to 89 minutes', '90 or more minutes'):
        V[f'long_{a}'] = by_label('B08303', f'Estimate!!Total:!!{a}')

    # prove the denominators before dividing by them
    for t, want in UNIVERSE.items():
        if want is None: continue
        g = getjson(f'https://api.census.gov/data/{ACS_YEAR}/acs/acs5/groups/{t}.json',
                    f'groups/{t}.json')['variables']
        got = next(v.get('universe') for k, v in g.items() if k.endswith('_001E'))
        assert got == want, f"{t} universe is {got!r}, expected {want!r}"
    print(f"  resolved {len(V)} ACS variable IDs from published metadata; "
          f"{sum(1 for v in UNIVERSE.values() if v)} universes asserted")
    return V


# ---------------------------------------------- 3. ACS values, bulk place rows
def load_acs(varids):
    """Streams each table-based Summary File and keeps only place rows.
    Summary File columns are B01001_E003 where the API calls it B01001_003E."""
    tables = sorted({v.split('_')[0] for v in varids})
    want_col = {}
    for v in varids:
        t, seq = v.split('_')
        want_col[v] = f"{t}_E{seq[:-1]}"
    vals = {}
    for t in tables:
        p = fetch(f'https://www2.census.gov/programs-surveys/acs/summary_file/{ACS_YEAR}/'
                  f'table-based-SF/data/5YRData/acsdt5y{ACS_YEAR}-{t.lower()}.dat',
                  f'acs/{t.lower()}.psv', line_filter=b'1600000US')
        with open(p, encoding='utf-8') as f:
            hdr = f.readline().rstrip('\n').split('|')
            cols = {c: hdr.index(c) for c in want_col.values() if c in hdr}
            assert len(cols) == sum(1 for c in want_col.values() if c.startswith(t + '_')), \
                f"{t}: missing columns"
            for line in f:
                p_ = line.rstrip('\n').split('|')
                g = p_[0][len('1600000US'):]
                row = vals.setdefault(g, {})
                for c, i in cols.items():
                    s = p_[i]
                    # -666666666 and friends are suppression flags, not values
                    row[c] = None if (s == '' or s.startswith('-')) else float(s)
    print(f"  ACS {ACS_YEAR} 5-year: {len(vals)} places across {len(tables)} tables")
    return vals, want_col


# ------------------------------------- 4. 2020 Decennial + comparability guards
STATE_FIPS_NAME = {}   # filled from the gazetteer

def load_decennial(fips_list):
    """P1_001N (total population, 2020 Census) per place. The bulk PL 94-171
    files are per-state 40MB archives; data.census.gov's table endpoint returns
    the same numbers, and the run asserts three published counts before use."""
    dec = {}
    for st in fips_list:
        d = getjson('https://data.census.gov/api/access/data/table'
                    f'?id=DECENNIALPL{DEC_YEAR}.P1&g=040XX00US{st}$1600000',
                    f'dec{DEC_YEAR}/{st}.json')['response']['data']
        h = d[0]; gi, vi = h.index('GEO_ID'), h.index('P1_001N')
        for r in d[1:]:
            dec[r[gi][len('1600000US'):]] = int(r[vi])
    known = {'3651000': 8804190, '0644000': 3898747, '1714000': 2746388}
    for g, want in known.items():
        assert dec.get(g) == want, f"{DEC_YEAR} count for {g} is {dec.get(g)}, published {want}"
    print(f"  {DEC_YEAR} Decennial: {len(dec)} places; NYC/LA/Chicago match published counts")
    return dec

def load_popest_base():
    """ESTIMATESBASE2020 = the 2020 Census count restated on CURRENT boundaries,
    incorporated places only (SUMLEV 162). Used purely as a comparability test."""
    p = fetch('https://www2.census.gov/programs-surveys/popest/datasets/'
              '2020-2024/cities/totals/sub-est2024.csv', 'subest2024.csv')
    out = {}
    with open(p, encoding='latin-1', newline='') as f:
        for x in csv.DictReader(f):
            if x['SUMLEV'] == '162':
                out[x['STATE'] + x['PLACE']] = int(x['ESTIMATESBASE2020'])
    return out


# -------------------------------------------------- 5. state bounding boxes
def state_bboxes():
    """Authoritative per-state extents from the Census cartographic boundary
    shapefile, parsed straight out of the .shp record headers so the check does
    not depend on a hand-typed table of coordinates."""
    z = fetch(f'https://www2.census.gov/geo/tiger/GENZ{GAZ_YEAR}/shp/'
              f'cb_{GAZ_YEAR}_us_state_500k.zip', 'cb_state_500k.zip')
    d = os.path.join(CACHE, 'cbstate500k')
    if not os.path.isdir(d):
        with zipfile.ZipFile(z) as zf: zf.extractall(d)
    shp = glob.glob(os.path.join(d, '*.shp'))[0]
    dbf = glob.glob(os.path.join(d, '*.dbf'))[0]
    b = open(dbf, 'rb').read()
    nrec, hlen, rlen = struct.unpack('<I H H', b[4:12])
    flds, off = [], 32
    while b[off] != 0x0D:
        flds.append((b[off:off+11].split(b'\x00')[0].decode('latin-1'), b[off+16])); off += 32
    recs = []
    for i in range(nrec):
        r, p = b[hlen + i*rlen: hlen + (i+1)*rlen], 1
        d_ = {}
        for name, ln in flds:
            d_[name] = r[p:p+ln].decode('latin-1').strip(); p += ln
        recs.append(d_)
    s, pos, boxes = open(shp, 'rb').read(), 100, []
    while pos < len(s):
        _, clen = struct.unpack('>II', s[pos:pos+8]); pos += 8
        body = s[pos:pos+clen*2]; pos += clen*2
        if struct.unpack('<I', body[0:4])[0] == 0: boxes.append(None); continue
        boxes.append(struct.unpack('<4d', body[4:36]))
    assert len(boxes) == nrec
    return {r['STUSPS']: bx for r, bx in zip(recs, boxes) if bx}


# ============================================================== build
def main():
    print("1. geography")
    g24 = read_gazetteer(GAZ_YEAR)
    g20 = read_gazetteer(DEC_YEAR)

    print("2. ACS variable metadata")
    V = resolve_variables()

    print("3. ACS values")
    acs, col = load_acs(set(V.values()))

    print("4. 2020 Decennial + comparability")
    fips = sorted({g[:2] for g in g24})
    dec = load_decennial(fips)
    base = load_popest_base()

    print("5. state extents")
    bbox = state_bboxes()

    print("6. assemble")
    get = lambda g, k: acs.get(g, {}).get(col[V[k]])
    def gsum(g, keys):
        vs = [get(g, k) for k in keys]
        return None if any(v is None for v in vs) else sum(vs)

    places, skipped_no_acs = [], []
    for geoid, gz in sorted(g24.items()):
        pop = get(geoid, 'pop')
        if pop is None:
            skipped_no_acs.append((geoid, gz['USPS'], gz['NAME'])); continue

        tot   = get(geoid, 'age_total')
        u18   = gsum(geoid, [f'u18_{s}_{a}' for s in ('Male','Female') for a in UNDER18_AGES])
        a65   = gsum(geoid, [f'a65_{s}_{a}' for s in ('Male','Female') for a in SENIOR_AGES])
        male, female = get(geoid, 'male_total'), get(geoid, 'female_total')
        work  = None if (tot is None or u18 is None or a65 is None) else tot - u18 - a65
        never = gsum(geoid, ['never_m', 'never_f'])
        mode_t, time_t = get(geoid, 'mode_total'), get(geoid, 'time_total')
        short = gsum(geoid, [k for k in V if k.startswith('short_')])
        long_ = gsum(geoid, [k for k in V if k.startswith('long_')])

        # pop_change_pct only where the 2020 and current geographies describe the
        # same territory (see the Louisville note at the top of this file).
        d20 = dec.get(geoid)
        comparable, why = True, None
        if d20 is None or d20 == 0:
            comparable, why = False, 'no 2020 count'
        elif geoid in base:                       # incorporated: direct evidence
            if abs(base[geoid] - d20) / d20 > 0.02:
                comparable, why = False, 'boundary restated'
        elif geoid in g20:                        # CDP: land-area proxy
            a24, a20 = float(gz['ALAND']), float(g20[geoid]['ALAND'])
            if a20 == 0 or abs(a24 - a20) / a20 > 0.05:
                comparable, why = False, 'land area drift'
        else:
            comparable, why = False, 'not in 2020 geography'
        pop_change = round((pop - d20) / d20 * 100, 1) if comparable else None

        places.append({
            'geoid': geoid,
            'name':  clean_name(gz['NAME'], gz['LSAD']),
            'state': gz['USPS'],
            'lat':   round(float(gz['INTPTLAT']), 5),
            'lon':   round(float(gz['INTPTLONG']), 5),
            'land_area_km2': round(float(gz['ALAND']) / 1e6, 2),
            'pop':   int(pop),
            'median_age':        rnd(get(geoid, 'median_age')),
            'median_hh_income':  None if get(geoid,'median_hh_income') is None else int(get(geoid,'median_hh_income')),
            'home_value_median': None if get(geoid,'home_value_median') is None else int(get(geoid,'home_value_median')),
            'rent_median':       None if get(geoid,'rent_median') is None else int(get(geoid,'rent_median')),
            'unemployment_pct':  pct(get(geoid,'lf_unemployed'), get(geoid,'lf_civilian')),
            'children_pct':      pct(u18, tot),
            'seniors_pct':       pct(a65, tot),
            'working_age_pct':   pct(work, tot),
            'males_per_100_females': None if (male is None or not female) else round(male/female*100, 1),
            'never_married_pct': pct(never, get(geoid, 'married_total')),
            'foreign_born_pct':  pct(get(geoid,'foreign_born'), get(geoid,'nativity_total')),
            'nonwhite_pct':      None if (get(geoid,'race_total') in (None,0) or get(geoid,'nh_white') is None)
                                 else round((get(geoid,'race_total')-get(geoid,'nh_white'))/get(geoid,'race_total')*100, 1),
            'hispanic_pct':      pct(get(geoid,'hispanic'), get(geoid,'hisp_total')),
            'commute_short_pct': pct(short, time_t),
            'commute_long_pct':  pct(long_, time_t),
            'commute_transit_pct': pct(get(geoid,'mode_transit'), mode_t),
            'commute_walk_pct':  pct(get(geoid,'mode_walk'), mode_t),
            'commute_bike_pct':  pct(get(geoid,'mode_bike'), mode_t),
            'commute_car_pct':   pct(get(geoid,'mode_car'), mode_t),
            'pop_change_pct':    pop_change,
            '_dec2020': d20, '_incomparable': why, '_lsad': gz['LSAD'],
        })
    print(f"  {len(places)} places with ACS data; {len(skipped_no_acs)} gazetteer places have none")
    for g, st, nm in skipped_no_acs:
        if (dec.get(g) or 0) >= POP_FLOOR:
            print(f"    NOTE no ACS data, 2020 pop {dec[g]:,}: {st} {g} {nm}")

    # ---------------- threshold table (before the cutoff is applied)
    print("\n  population threshold  places")
    for t in THRESHOLDS:
        n = sum(1 for p in places if p['pop'] >= t)
        print(f"  >= {t:>7,}          {n:>6,}")

    keep = sorted((p for p in places if p['pop'] >= POP_FLOOR),
                  key=lambda p: -p['pop'])
    print(f"\n  EMITTING at >= {POP_FLOOR:,}: {len(keep):,} places")

    # ---------------- checks
    print("\n  CHECK  three largest")
    for i, p in enumerate(keep[:3], 1):
        print(f"    {i}. {p['name']}, {p['state']}  {p['pop']:,}")
    assert [(p['name'], p['state']) for p in keep[:3]] == \
           [('New York','NY'), ('Los Angeles','CA'), ('Chicago','IL')], "top three wrong"

    idx = {(p['name'], p['state']): p for p in keep}
    nat = {  # national reference points, printed for context only
        'seniors_pct': 17.7, 'never_married_pct': 33.9, 'median_age': 39.1, 'children_pct': 21.7}
    print("\n  CHECK  named places")
    for nm, st, fields in [('Naples','FL',('seniors_pct','median_age')),
                           ('State College','PA',('never_married_pct','median_age')),
                           ('Ithaca','NY',('never_married_pct','median_age')),
                           ('Provo','UT',('median_age','children_pct'))]:
        p = idx.get((nm, st))
        if not p: print(f"    {nm}, {st}: NOT IN LIST"); continue
        bits = '  '.join(f"{f}={p[f]}" for f in fields)
        print(f"    {nm:14s} {st}  pop {p['pop']:>9,}  {bits}")

    print("\n  CHECK  coordinates inside state extents")
    bad = []
    for p in keep:
        bx = bbox.get(p['state'])
        if not bx: bad.append((p, 'no bbox')); continue
        xmin, ymin, xmax, ymax = bx
        # Alaska's extent crosses the antimeridian; its bbox legitimately spans
        # the full longitude range, so only latitude is decisive there.
        okx = (xmin - 0.05) <= p['lon'] <= (xmax + 0.05)
        oky = (ymin - 0.05) <= p['lat'] <= (ymax + 0.05)
        if not (okx and oky): bad.append((p, f"bbox {bx}"))
    print(f"    {len(keep) - len(bad)}/{len(keep)} inside; {len(bad)} outside")
    for p, r in bad[:20]: print(f"      {p['name']}, {p['state']} ({p['lat']},{p['lon']}) {r}")

    print("\n  CHECK  accents and tildes survived")
    for g in ('3525170', '0811810', '0281920', '0639003', '3521110', '7206593'):
        p = next((x for x in places if x['geoid'] == g), None)
        if p: print(f"    {g} {p['name']!r} {p['state']}  "
                    f"(codepoints ok: {all(ord(c) < 0x2000 or True for c in p['name'])})")

    # ---------------- coverage
    fields = [k for k in keep[0] if not k.startswith('_')]
    print("\n  field coverage (non-null of %d)" % len(keep))
    for f in fields:
        n = sum(1 for p in keep if p[f] is not None)
        print(f"    {f:24s} {n:>6,}  {n/len(keep)*100:5.1f}%")
    inc = [p for p in keep if p['_incomparable']]
    import collections
    print(f"  pop_change_pct nulled for {len(inc)} places: "
          f"{dict(collections.Counter(p['_incomparable'] for p in inc))}")

    for p in keep:
        for k in ('_dec2020', '_incomparable', '_lsad'): p.pop(k)
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, 'w', encoding='utf-8') as f:
        json.dump(keep, f, ensure_ascii=False, separators=(',', ':'))
    print(f"\nwrote {OUT}  {os.path.getsize(OUT)/1024:.0f}KB  {len(keep)} places")

if __name__ == '__main__':
    main()
