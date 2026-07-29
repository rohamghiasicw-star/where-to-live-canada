#!/usr/bin/env python3
"""
US political lean by county, 2024 presidential election.

Sibling of src/build_politics.py (Canada, 45th federal general election by riding).
Same output scale: -100 = left, +100 = right, vote weighted. Same idea that the
party positions are written down in the script so they can be argued with instead
of hiding inside a formula.

  data/us/politics.json      county FIPS -> lean + the vote counts behind it
  data/us/place_county.json  7 digit Census place GEOID -> county FIPS

Sources, in the order they are trusted:

1. MIT Election Data and Science Lab, "2024-elections-official" (github.com/MEDSL).
   Official precinct level returns transcribed from each state's own canvass.
   Aggregated here to county. This is the academic source and it is preferred.
   The MEDSL county level file (County Presidential Election Returns 2000-2024,
   doi:10.7910/DVN/VOQCHQ) would have been the first choice but Harvard Dataverse
   puts it behind a required guestbook form, so it cannot be fetched by script.
2. MEDSL "2024-president-state.csv" official state totals. Used only as a referee,
   never as data: every state's aggregated county sum is checked against it.
3. tonmcg/US_County_Level_Election_Results_08-24, a long running public county
   results repository (AP / network feeds). Used only as a per county repair where
   source 1 fails the source 2 check, and every repaired row is labelled
   source="tonmcg_county" in the output so it can be filtered out.

Geography:
  Census place -> county from national_place_by_county2020.txt.
  Population weights for places that straddle counties from the Census Population
  Estimates sub-est2024.csv (SUMLEV 157 = place part within county).
  Places with no estimates coverage (mostly CDPs) are resolved with exact 2020
  Census block population inside the place boundary, via TIGERweb.

Run:  python3 src/us/build_politics.py            (from the repo root)
Cache dir: $LIVABLE_US_CACHE, default <tmp>/livable_us_cache  (~1.6 GB of raw data)
"""
import csv, io, json, os, sys, collections, tempfile, zipfile
import urllib.request, urllib.parse

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CACHE = os.environ.get('LIVABLE_US_CACHE', os.path.join(tempfile.gettempdir(), 'livable_us_cache'))
os.makedirs(CACHE, exist_ok=True)
OUT_POL = os.path.join(ROOT, 'data', 'us', 'politics.json')
OUT_PC  = os.path.join(ROOT, 'data', 'us', 'place_county.json')

# ---------------------------------------------------------------- the axis ----
# Where the two parties sit on one left-right axis. This is a judgement call, so
# it is stated openly (same as the Canadian script) instead of being buried.
#
# The Canadian file spreads six parties across the axis and takes a vote weighted
# mean. The US presidential race is effectively two parties, so the two of them
# are pinned to the ends of the scale and the vote weighted mean collapses to the
# two-party margin:
#
#     lean = ( AXIS[D]*dem + AXIS[R]*rep ) / (dem + rep)
#          = ( rep - dem ) / (dem + rep) * 100
#
#     -100  every two-party vote Democratic
#        0  an even two-party split
#     +100  every two-party vote Republican
#
# Consequence to be honest about: pinning the parties to +/-100 means the US
# numbers use the full width of the scale while the Canadian numbers do not
# (Canada's most right riding lands near +60). A US +45 and a Canadian +45 are
# NOT the same thing. Do not compare the two countries' leans directly.
AXIS = {'DEMOCRAT': -100.0, 'REPUBLICAN': 100.0}

# Third party votes are counted and reported (other_votes) but deliberately kept
# out of the lean. In 2024 they are ~1.9% of the national vote and they do not
# share an axis: Libertarian sits right of Republican on economics, Green sits
# left of Democratic, and the largest single bloc (Kennedy, where he stayed on
# the ballot) is not placeable at all. Guessing positions for them would add
# invented precision to every county for less than two points of vote. Stated
# here so the choice is arguable rather than silent.
THIRD_PARTY_AXIS_NOT_USED = True

# Same label bands as the Canadian script, so the wording is consistent in the app.
def lean_label(x):
    return ('solid left' if x < -40 else 'leans left' if x < -12 else
            'swing' if x < 12 else 'leans right' if x < 40 else 'solid right')

# ------------------------------------------------------------------ sources ---
MEDSL_RAW = 'https://raw.githubusercontent.com/MEDSL/2024-elections-official/main'
STATES = ['ak','al','ar','az','ca','co','ct','dc','de','fl','ga','hi','ia','id','il','in','ks',
          'ky','la','ma','md','me','mi','mn','mo','ms','mt','nc','nd','ne','nh','nj','nm','nv',
          'ny','oh','ok','or','pa','ri','sc','sd','tn','tx','ut','va','vt','wa','wi','wv','wy']
TONMCG = ('https://raw.githubusercontent.com/tonmcg/US_County_Level_Election_Results_08-24/'
          'master/2024_US_County_Level_Presidential_Results.csv')
PLACE_COUNTY = 'https://www2.census.gov/geo/docs/reference/codes2020/national_place_by_county2020.txt'
COUSUB = 'https://www2.census.gov/geo/docs/reference/codes2020/national_cousub2020.txt'
SUBEST = ('https://www2.census.gov/programs-surveys/popest/datasets/2020-2024/cities/totals/'
          'sub-est2024.csv')
TIGER = ('https://tigerweb.geo.census.gov/arcgis/rest/services/TIGERweb/'
         'tigerWMS_Census2020/MapServer')

def fetch(url, name, binary=True):
    p = os.path.join(CACHE, name)
    if not os.path.exists(p) or os.path.getsize(p) == 0:
        sys.stderr.write('  get %s\n' % name)
        req = urllib.request.Request(url, headers={'User-Agent': 'livable-build/1.0'})
        with urllib.request.urlopen(req, timeout=600) as r, open(p, 'wb') as f:
            while True:
                b = r.read(1 << 20)
                if not b: break
                f.write(b)
    return p

# ------------------------------------------------------- known source defects --
# Every item here is a defect found by checking the aggregation against the
# official state totals. Each one is applied openly and reported in the run log.
FIPS_RENAME = {'46113': '46102'}   # Shannon County SD renamed Oglala Lakota, 2015
# MEDSL parks Kansas City MO under a synthetic county code. '36' is New York's
# state FIPS, so left alone it lands 122k votes in New York.
KC_PSEUDO = '36000'
KC_COUNTIES = ['29037', '29047', '29095', '29165']   # Cass, Clay, Jackson, Platte
# Rows that are meta information, not a candidate.
NON_CAND = {'', 'OVERVOTES', 'UNDERVOTES', 'OVER VOTES', 'UNDER VOTES', 'BLANK', 'BLANKS',
            'BLANK VOTES', 'TOTAL', 'TOTALS', 'TOTAL VOTES', 'TOTAL VOTES CAST',
            'TOTAL BALLOTS CAST', 'TOTAL BALLOTS', 'BALLOTS CAST', 'CAST VOTES', 'TOTAL CAST',
            'REGISTERED VOTERS', 'TOTAL VOTERS', 'EXHAUSTED', 'NO CANDIDATE', 'VOID',
            'TIMES COUNTED', 'TIMES BLANK VOTED', 'CONTEST TOTALS', 'NOT VOTED'}
DEM, REP, OTH = 0, 1, 2
# Counties whose lean is not comparable to tonmcg's file, so they are never repaired:
#   AK  MEDSL gives real boroughs, tonmcg gives state house districts
#   CT  MEDSL and the 2020 place file use the old 8 counties, tonmcg uses the 9
#       post-2022 planning regions
#   DC  tonmcg splits DC into 8 ward rows, the real county FIPS is 11001
NO_REPAIR = {'AK', 'CT', 'DC'}

def slot(cand, party):
    if cand == 'KAMALA D HARRIS': return DEM
    if cand == 'DONALD J TRUMP':  return REP
    return OTH

# ------------------------------------------------------- 1. official totals ---
def official_state_totals():
    p = fetch(MEDSL_RAW + '/2024-president-state.csv', 'president_state.csv')
    off = collections.defaultdict(lambda: [0, 0, 0])
    fips2po = {}
    for r in csv.DictReader(open(p, encoding='utf-8-sig')):
        po = r['state_po']; fips2po[r['state_fips']] = po
        c = r['candidate'].upper(); v = int(r['votes'])
        if 'HARRIS' in c and 'KAMALA' in c: off[po][DEM] += v
        elif 'TRUMP' in c and 'DONALD' in c: off[po][REP] += v
        elif c in ('UNDERVOTES', 'OVERVOTES'): pass       # not votes for anyone
        else: off[po][OTH] += v
    return dict(off), fips2po

# ------------------------------- 2. MEDSL precinct returns -> county totals ---
def read_state(po):
    z = zipfile.ZipFile(fetch('%s/individual_states/%s24.zip' % (MEDSL_RAW, po.lower()),
                              '%s24.zip' % po.lower()))
    n = z.namelist()[0]
    with z.open(n) as fh:
        for r in csv.DictReader(io.TextIOWrapper(fh, encoding='utf-8', errors='replace')):
            if r.get('office') == 'US PRESIDENT' and r.get('stage') == 'GEN':
                yield r

def keep(r):
    cand = (r.get('candidate') or '').strip().upper()
    if cand in NON_CAND: return None
    v = (r.get('votes') or '').strip()
    if v in ('*', ''): return None            # '*' = jurisdiction suppressed the count
    try: return cand, int(float(v))
    except ValueError: return None

def dedup_modes(recs, extra_key=None):
    """States report either one TOTAL row per candidate or one row per voting mode,
    and some report both. Summing blindly double counts those. Group first, then
    take TOTAL if TOTAL is present alongside split modes."""
    g = collections.defaultdict(dict)
    for r, cand, v in recs:
        k = (r['county_fips'], r.get('jurisdiction_fips', ''), r['precinct'], cand,
             r.get('party_detailed', ''), r.get('district', ''))
        if extra_key: k = k + (r.get(extra_key, ''),)
        m = r.get('mode', '')
        g[k][m] = g[k].get(m, 0) + v
    out = []
    conflicts = 0
    for k, md in g.items():
        if 'TOTAL' in md and len(md) > 1:
            conflicts += 1; v = md['TOTAL']
        else:
            v = sum(md.values())
        out.append((k, v))
    return out, conflicts

def drop_nj_aggregates(recs):
    """New Jersey 2024 publishes election-district rows AND a municipal total row
    for the same municipality ("Allendale" alongside "Allendale 1".."Allendale 4").
    Drop any precinct label that is a strict prefix of another label in the same
    county, i.e. the roll-up rows."""
    byc = collections.defaultdict(set)
    for r, c, v in recs: byc[r['county_fips']].add(r['precinct'])
    drop = set()
    for cf, ps in byc.items():
        for p in ps:
            if any(q != p and q.startswith(p + ' ') for q in ps):
                drop.add((cf, p))
    kept = [(r, c, v) for r, c, v in recs if (r['county_fips'], r['precinct']) not in drop]
    return kept, len(recs) - len(kept)

def alaska_to_boroughs(recs):
    """Alaska is the one state that does not report everything by borough.
    Precinct rows carry a borough (county_fips), but absentee / early / question
    ballots are only published for the whole state house district and come through
    with an empty county_fips. About 49% of Alaska's presidential vote arrives that
    way. Boroughs are therefore built as:

        borough total = borough's own precinct votes
                      + that district's district-only votes, split across the
                        district's boroughs in proportion to the same candidate's
                        precinct votes in each borough

    So Alaska borough numbers are part measured, part allocated. They sum exactly
    to the official state totals, and every Alaska row is flagged imputed=True."""
    g = collections.defaultdict(dict)
    for r, cand, v in recs:
        k = (r['county_fips'], r.get('jurisdiction_name', ''), r['precinct'], cand,
             r.get('party_detailed', ''))
        m = r.get('mode', '')
        g[k][m] = g[k].get(m, 0) + v
    attr = collections.defaultdict(lambda: collections.defaultdict(collections.Counter))
    unattr = collections.defaultdict(collections.Counter)
    for k, md in g.items():
        v = md['TOTAL'] if ('TOTAL' in md and len(md) > 1) else sum(md.values())
        cf, dist, _pr, cand, party = k
        s = slot(cand, party)
        if len(cf) == 5 and cf.isdigit(): attr[dist][s][cf] += v
        else: unattr[dist][s] += v
    county = collections.defaultdict(lambda: [0.0, 0.0, 0.0])
    allocated = 0
    for dist, slots in attr.items():
        for s, per in slots.items():
            tot = sum(per.values()); un = unattr.get(dist, {}).get(s, 0)
            allocated += un
            for cf, v in per.items():
                county[cf][s] += v + (un * v / tot if tot else 0.0)
    stranded = sum(v for d, sl in unattr.items() for s, v in sl.items() if d not in attr)
    return county, allocated, stranded

def medsl_counties(fips2po):
    county = collections.defaultdict(lambda: [0.0, 0.0, 0.0])
    log = {}
    unallocated = collections.Counter()     # votes on rows with no usable county FIPS
    for po in STATES:
        po = po.upper()
        recs = []
        for r in read_state(po):
            k = keep(r)
            if k: recs.append((r, k[0], k[1]))
        note = {'rows': len(recs)}
        if po == 'NJ':
            recs, n = drop_nj_aggregates(recs)
            note['nj_rollup_rows_dropped'] = n
        if po == 'AK':
            sub, alloc, stranded = alaska_to_boroughs(recs)
            note['ak_district_only_votes_allocated'] = alloc
            note['ak_stranded'] = stranded
            for cf, v in sub.items():
                for i in range(3): county[cf][i] += v[i]
        else:
            rows, conflicts = dedup_modes(recs)
            note['mode_conflict_groups'] = conflicts
            for k, v in rows:
                cf = FIPS_RENAME.get(k[0], k[0])
                if len(cf) != 5 or not cf.isdigit():
                    unallocated[po] += v; continue
                county[cf][slot(k[3], k[4])] += v
        log[po] = note
        sys.stderr.write('  %s ok\n' % po)
    # Kansas City's synthetic code: fold it out of New York's number space. Its
    # votes are recovered by repairing the four Missouri counties from tonmcg.
    kc = county.pop(KC_PSEUDO, None)
    log['_kansas_city_pseudo_county'] = ([round(x) for x in kc] if kc else None)
    log['_unallocated_votes_by_state'] = dict(unallocated)
    return county, log

# ---------------------------------------------------------- 3. the referee ----
def tonmcg_counties():
    p = fetch(TONMCG, 'tonmcg_2024_county.csv')
    out = {}
    for r in csv.DictReader(open(p, encoding='utf-8-sig')):
        cf = r['county_fips'].zfill(5)
        d, g, t = int(r['votes_dem']), int(r['votes_gop']), int(r['total_votes'])
        out[cf] = [d, g, max(t - d - g, 0)]
    return out

def state_sums(county, fips2po):
    s = collections.defaultdict(lambda: [0.0, 0.0, 0.0])
    for cf, v in county.items():
        po = fips2po.get(cf[:2])
        if po:
            for i in range(3): s[po][i] += v[i]
    return s

def repair(county, off, ton, fips2po, tol_state=0.005, tol_county=0.02):
    """A state's county sum has to reproduce the official state total. Where it
    does not, the counties that disagree with the reference file by more than
    tol_county are swapped for the reference file's numbers and the state total is
    re-checked. Nothing is scaled or invented, whole county rows are swapped and
    labelled. Note the ordering matters: a state whose own sum already matches is
    left alone even if individual counties differ from tonmcg, because there the
    reference file is the one that is wrong (Oregon and Washington are examples)."""
    src = {cf: 'medsl_precinct' for cf in county}
    before = state_sums(county, fips2po)
    failing = []
    for po, o in off.items():
        m = before.get(po, [0, 0, 0])
        rd = (m[DEM] - o[DEM]) / o[DEM] if o[DEM] else 0
        rr = (m[REP] - o[REP]) / o[REP] if o[REP] else 0
        if max(abs(rd), abs(rr)) > tol_state: failing.append(po)
    # Missouri always needs the four Kansas City counties: the pseudo county cannot
    # be split back apart from the precinct file.
    forced = set(KC_COUNTIES) if 'MO' in failing else set()
    swapped = []
    for cf in sorted(set(county) | set(ton)):
        po = fips2po.get(cf[:2])
        if po is None or po in NO_REPAIR: continue
        if po not in failing: continue
        t = ton.get(cf)
        if not t: continue
        m = county.get(cf)
        need = cf in forced
        if m is not None and not need:
            dd = abs(m[DEM] - t[DEM]) / max(t[DEM], 1)
            dr = abs(m[REP] - t[REP]) / max(t[REP], 1)
            need = max(dd, dr) > tol_county
        if m is None: need = True
        if need:
            swapped.append((cf, po, [round(x) for x in (m or [0, 0, 0])], list(t)))
            county[cf] = [float(x) for x in t]
            src[cf] = 'tonmcg_county'
    return county, src, failing, swapped, before

# --------------------------------------------------- 4. county names + pop ----
def county_names_and_pop(fips2po):
    """Names and 2024 population per county. Connecticut needs care: the election
    data and the 2020 place file both use the old 8 CT counties, while every
    current Census estimate uses the 9 post-2022 planning regions. CT county
    population is therefore rebuilt by summing town estimates back into the old
    counties via the 2020 county subdivision file."""
    sp = fetch(SUBEST, 'sub-est2024.csv')
    name, pop = {}, {}
    ct_town_pop = {}
    for r in csv.DictReader(open(sp, encoding='latin-1')):
        if r['SUMLEV'] == '050':
            cf = r['STATE'] + r['COUNTY']
            name[cf] = r['NAME']; pop[cf] = int(r['POPESTIMATE2024'] or 0)
        elif r['SUMLEV'] == '061' and r['STATE'] == '09':
            ct_town_pop[r['COUSUB']] = int(r['POPESTIMATE2024'] or 0)
    cs = fetch(COUSUB, 'national_cousub2020.txt')
    ct = collections.Counter(); ctname = {}
    for r in csv.DictReader(open(cs, encoding='latin-1'), delimiter='|'):
        if r['STATEFP'] != '09': continue
        cf = r['STATEFP'] + r['COUNTYFP']
        ctname[cf] = r['COUNTYNAME']
        ct[cf] += ct_town_pop.get(r['COUSUBFP'], 0)
    for cf, p in ct.items():
        name[cf] = ctname[cf]; pop[cf] = p
    return name, pop

# ------------------------------------------------------- 5. place -> county ---
def tiger_query(layer, params):
    d = urllib.parse.urlencode(params).encode()
    req = urllib.request.Request('%s/%s/query' % (TIGER, layer), data=d,
                                 headers={'User-Agent': 'livable-build/1.0'})
    with urllib.request.urlopen(req, timeout=180) as r:
        return json.load(r)

def tiger_place_pop_by_county(geoid):
    """Exact 2020 Census block population of a place, split by county. Used for the
    ~200 straddling places (nearly all CDPs) that the population estimates file
    does not break out by county."""
    for layer in (26, 28):     # incorporated places, then CDPs
        g = tiger_query(layer, {'where': "GEOID='%s'" % geoid, 'outFields': 'GEOID',
                                'returnGeometry': 'true', 'outSR': '4269', 'f': 'json'})
        if g.get('features'): break
    else:
        return None
    geom = g['features'][0]['geometry']
    res = tiger_query(10, {
        'geometry': json.dumps({'rings': geom['rings'], 'spatialReference': {'wkid': 4269}}),
        'geometryType': 'esriGeometryPolygon', 'inSR': '4269',
        'spatialRel': 'esriSpatialRelContains', 'returnGeometry': 'false', 'f': 'json',
        'outStatistics': json.dumps([{'statisticType': 'sum', 'onStatisticField': 'POP100',
                                      'outStatisticFieldName': 'P'}]),
        'groupByFieldsForStatistics': 'STATE,COUNTY'})
    out = {}
    for f in res.get('features', []):
        a = f['attributes']
        out[a['STATE'] + a['COUNTY']] = int(a['P'] or 0)
    return out

def build_place_county(valid_counties, fips2po):
    pcp = fetch(PLACE_COUNTY, 'national_place_by_county2020.txt')
    places = collections.defaultdict(set); meta = {}
    for r in csv.DictReader(open(pcp, encoding='latin-1'), delimiter='|'):
        g = r['STATEFP'] + r['PLACEFP']
        places[g].add(r['STATEFP'] + r['COUNTYFP'])
        meta[g] = (r['PLACENAME'], r['STATE'], r['TYPE'])
    # place part populations, SUMLEV 157 of the estimates file
    w = collections.defaultdict(dict)
    for r in csv.DictReader(open(os.path.join(CACHE, 'sub-est2024.csv'), encoding='latin-1')):
        if r['SUMLEV'] == '157' and r['COUSUB'] == '00000' and r['PLACE'] not in ('00000', '99990'):
            w[r['STATE'] + r['PLACE']][r['STATE'] + r['COUNTY']] = int(r['POPESTIMATE2024'] or 0)
    cachef = os.path.join(CACHE, 'tiger_place_parts.json')
    tcache = json.load(open(cachef)) if os.path.exists(cachef) else {}
    out = {}
    stats = collections.Counter()
    skipped_terr = 0
    for g, cs in sorted(places.items()):
        if fips2po.get(g[:2]) is None:       # Puerto Rico and the island areas
            skipped_terr += 1; continue
        cs = sorted(cs)
        if len(cs) == 1:
            out[g] = {'county': cs[0], 'multi_county': False}
            stats['single'] += 1
            continue
        ww = {c: v for c, v in w.get(g, {}).items() if c in cs}
        src = 'subest2024_sumlev157'
        if not ww or sum(ww.values()) == 0:
            if g not in tcache:
                try:
                    tcache[g] = tiger_place_pop_by_county(g) or {}
                except Exception as e:
                    sys.stderr.write('  tiger fail %s %s\n' % (g, e)); tcache[g] = {}
                json.dump(tcache, open(cachef, 'w'))
            ww = {c: v for c, v in (tcache.get(g) or {}).items() if c in cs}
            src = 'census2020_blocks_tigerweb'
        if not ww or sum(ww.values()) == 0:
            # Nothing anywhere says which part holds the people. Fall back to the
            # lowest county FIPS so the result is at least deterministic, and say so.
            out[g] = {'county': cs[0], 'multi_county': True, 'counties': cs,
                      'share': None, 'weight_source': 'unresolved_lowest_fips'}
            stats['unresolved'] += 1
            continue
        # SUMLEV 157 omits county parts that hold no population, so a part missing
        # from the weights is treated as zero rather than unknown.
        best = max(ww.items(), key=lambda kv: (kv[1], kv[0] == cs[0]))
        tot = sum(ww.values())
        out[g] = {'county': best[0], 'multi_county': True, 'counties': cs,
                  'pop_by_county': {c: ww.get(c, 0) for c in cs},
                  'share': round(best[1] / tot, 4), 'weight_source': src}
        stats[src] += 1
        if best[0] not in valid_counties: stats['winner_not_in_politics'] += 1
    stats['territory_places_skipped'] = skipped_terr
    return out, stats, meta

# ----------------------------------------------------------------- 6. main ----
def main():
    sys.stderr.write('sources -> %s\n' % CACHE)
    off, fips2po = official_state_totals()
    county, log = medsl_counties(fips2po)
    ton = tonmcg_counties()
    county, src, failing, swapped, before = repair(county, off, ton, fips2po)
    name, pop = county_names_and_pop(fips2po)

    rows = {}
    for cf, v in sorted(county.items()):
        po = fips2po.get(cf[:2])
        if po is None: continue
        d, r, o = (round(x) for x in v)
        two = d + r
        tot = d + r + o
        if two == 0: continue
        lean = (AXIS['DEMOCRAT'] * d + AXIS['REPUBLICAN'] * r) / two
        rec = {
            'county_name': name.get(cf, ''), 'state': po,
            'dem_votes': d, 'rep_votes': r, 'other_votes': o, 'total_votes': tot,
            'dem_pct': round(d / tot * 100, 2), 'rep_pct': round(r / tot * 100, 2),
            'two_party_votes': two,
            'lean': round(lean, 1), 'lean_label': lean_label(lean),
            'winner': 'REPUBLICAN' if r > d else 'DEMOCRAT' if d > r else 'TIE',
            'source': src.get(cf, 'medsl_precinct'),
        }
        p = pop.get(cf)
        if p: rec['population_2024'] = p
        if po == 'AK': rec['imputed'] = 'ak_district_allocation'
        # A single lean over a county this big is close to meaningless. Flagged in
        # the data so the app can refuse to lean on it.
        if p and p >= 1_000_000: rec['coarse'] = True
        rows[cf] = rec
    json.dump(rows, open(OUT_POL, 'w'), indent=1, sort_keys=True)

    pc, pcstats, pmeta = build_place_county(set(rows), fips2po)
    json.dump(pc, open(OUT_PC, 'w'), indent=0, sort_keys=True)

    # ------------------------------------------------------------- report ----
    print('=' * 78)
    print('US COUNTY POLITICAL LEAN, 2024 PRESIDENTIAL')
    print('=' * 78)
    print('lean = (AXIS[DEM]*dem_votes + AXIS[REP]*rep_votes) / (dem_votes + rep_votes)')
    print('     = (rep_votes - dem_votes) / (dem_votes + rep_votes) * 100      AXIS %s' % AXIS)
    print()
    print('counties written : %d' % len(rows))
    print('  from MEDSL precinct returns : %d' % sum(1 for r in rows.values() if r['source'] == 'medsl_precinct'))
    print('  repaired from tonmcg        : %d' % sum(1 for r in rows.values() if r['source'] == 'tonmcg_county'))
    tot = sum(r['total_votes'] for r in rows.values())
    td = sum(r['dem_votes'] for r in rows.values()); tr = sum(r['rep_votes'] for r in rows.values())
    offtot = sum(sum(v) for v in off.values())
    print('national votes   : %d  (dem %d  rep %d  other %d)' % (tot, td, tr, tot - td - tr))
    print('official (MEDSL state file) : %d   difference %+d (%+.3f%%)'
          % (offtot, tot - offtot, (tot - offtot) / offtot * 100))
    print()
    print('states that failed the 0.5%% state-total check and were repaired: %s' % (failing or 'none'))
    print('county rows swapped: %d' % len(swapped))
    for cf, po, m, t in swapped[:8]:
        print('   %s %s  medsl D%-8d R%-8d -> ref D%-8d R%-8d' % (cf, po, m[0], m[1], t[0], t[1]))
    if len(swapped) > 8: print('   ... and %d more (all labelled source=tonmcg_county)' % (len(swapped) - 8))
    print()
    after = state_sums(county, fips2po)
    worst = []
    for po, o in off.items():
        m = after.get(po, [0, 0, 0])
        rd = (m[DEM] - o[DEM]) / o[DEM] * 100 if o[DEM] else 0
        rr = (m[REP] - o[REP]) / o[REP] * 100 if o[REP] else 0
        worst.append((max(abs(rd), abs(rr)), po, rd, rr))
    worst.sort(reverse=True)
    print('worst remaining state residuals vs official totals:')
    for _, po, rd, rr in worst[:6]:
        print('   %s  dem %+.2f%%  rep %+.2f%%' % (po, rd, rr))
    print()
    print('--- spot checks --------------------------------------------------------')
    print('%-7s %-26s %6s %-12s %10s %10s %10s %s' %
          ('FIPS', 'county', 'lean', 'label', 'dem', 'rep', 'total', 'source'))
    CHECKS = [('06075', 'expect strongly negative'), ('11001', 'expect strongly negative'),
              ('48393', 'expect strongly positive'), ('48431', 'expect strongly positive'),
              ('04013', 'expect near zero'), ('06037', 'biggest county in the country'),
              ('02020', 'Alaska, partly allocated'), ('09001', 'Connecticut, old county'),
              ('29095', 'Kansas City repair'), ('22071', 'Louisiana repair'),
              ('15005', 'Kalawao HI, no separate returns')]
    for cf, why in CHECKS:
        r = rows.get(cf)
        if not r:
            print('%-7s %-26s   ABSENT   %s' % (cf, '', why)); continue
        print('%-7s %-26s %6.1f %-12s %10d %10d %10d %s   %s' %
              (cf, (r['county_name'] + ', ' + r['state'])[:26], r['lean'], r['lean_label'],
               r['dem_votes'], r['rep_votes'], r['total_votes'], r['source'], why))
    print()
    sm = sorted(rows.items(), key=lambda kv: kv[1]['lean'])
    print('most left / most right:')
    for cf, r in sm[:3] + sm[-3:]:
        print('   %s %-30s %6.1f  %s' % (cf, r['county_name'] + ', ' + r['state'], r['lean'],
                                         r['lean_label']))
    print()
    print('--- coverage -----------------------------------------------------------')
    uni = {}
    for r in csv.DictReader(open(os.path.join(CACHE, 'sub-est2024.csv'), encoding='latin-1')):
        if r['SUMLEV'] == '050': uni[r['STATE'] + r['COUNTY']] = r['NAME'] + ', ' + r['STNAME']
    absent = [(c, n) for c, n in sorted(uni.items()) if c not in rows and not c.startswith('09')]
    print('Census county-equivalents (current vintage) : %d' % len(uni))
    print('counties with a lean                        : %d' % len(rows))
    print('absent (outside Connecticut)                : %s' % (absent or 'none'))
    print('Connecticut is keyed on the pre-2022 counties (%d rows), not the 9 planning'
          % sum(1 for c in rows if c.startswith('09')))
    print('  regions, because both the election returns and the 2020 place file use them.')
    print('unallocated votes (rows with no county code): %s' % dict(log['_unallocated_votes_by_state']))
    print()
    coarse = sorted((r for r in rows.values() if r.get('coarse')),
                    key=lambda r: -r['population_2024'])
    print('counties over 1M people, where one lean number is close to meaningless (%d):' % len(coarse))
    for r in coarse[:12]:
        print('   %-28s %9d people   lean %6.1f' %
              (r['county_name'] + ', ' + r['state'], r['population_2024'], r['lean']))
    print('   ... %d more' % max(0, len(coarse) - 12))
    print()
    print('--- place -> county ----------------------------------------------------')
    print('places written : %d' % len(pc))
    for k in sorted(pcstats): print('   %-32s %d' % (k, pcstats[k]))
    print()
    print('--- log ----------------------------------------------------------------')
    print(json.dumps({k: v for k, v in log.items() if k.startswith('_')}, indent=1))
    for po in ('AK', 'NJ'):
        print(po, json.dumps(log[po]))
    print()
    print('wrote %s' % OUT_POL)
    print('wrote %s' % OUT_PC)

if __name__ == '__main__':
    main()
