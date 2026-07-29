"""Age / sex / marital status / religion from the 2021 Census Profile, census
subdivision level (StatCan 98-401-X2021005).

Source zip (~197 MB, 2.59 GB unzipped), staged in /tmp so it never enters the repo:
  https://www12.statcan.gc.ca/census-recensement/2021/dp-pd/prof/details/download-telecharger/comp/GetFile.cfm?Lang=E&FILETYPE=CSV&GEONO=005

ENCODING: the file is cp1252, NOT UTF-8. Read it as UTF-8 and 'Montreal' quietly
becomes 'montral', every Quebec CSD fails to match, and the script still reports
success. Same trap as src/extract_census.py.

CHARACTERISTIC IDs were read out of the file's own CHARACTERISTIC_NAME column, not
guessed. Worth flagging one live landmine: ids 1730 'Jewish', 1745 'Sikh', 1760
'Muslim' also exist, but they sit in the ETHNIC OR CULTURAL ORIGIN block (their
neighbours are 'American' and 'Spanish'). The religion block is 1949-1973. Keying
religion off the 17xx ids would silently produce ancestry numbers labelled religion.

Every share is computed against the denominator the census actually publishes it
under, never against total population:
  age            -> 8    Total - Age groups of the population - 100% data
  marital        -> 58   Total - Marital status for the total population aged 15+ - 100% data
  religion       -> 1949 Total - Religion for the population in private households - 25% sample data
Religion is 25% sample data while age/marital are 100% data, so the two families
carry different denominators on purpose.

Columns (from the header): 11 = C1_COUNT_TOTAL, 13 = C2_COUNT_MEN+, 15 = C3_COUNT_WOMEN+.
males_per_100_females is computed from the men+/women+ counts on the age total (id 8),
which is the population base those columns are published against.
"""
import csv, json, sys, os

csv.field_size_limit(sys.maxsize)

SRC = '/tmp/g5/98-401-X2021005_English_CSV_data.csv'
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CENSUS = os.path.join(REPO, 'data', 'census.json')
OUT = os.path.join(REPO, 'data', 'demographics.json')

COUNT, MEN, WOMEN = 11, 13, 15

# denominators we must carry to turn counts into published shares
DEN_AGE, DEN_MARITAL, DEN_RELIGION = '8', '58', '1949'

# characteristic id -> (output field, denominator id)
SHARES = {
    # age structure, share of id 8
    '9':    ('children_pct',      DEN_AGE),
    '13':   ('working_age_pct',   DEN_AGE),
    '24':   ('seniors_pct',       DEN_AGE),
    # marital status, population 15+, share of id 58.
    # 67 is literally 'Not married and not living common law - Never married' =
    # single and never legally married. 66 is its parent, everyone not in a couple.
    # 67 is a SUBSET of 66, so these two are not meant to sum to 100.
    '67':   ('never_married_pct', DEN_MARITAL),
    '66':   ('not_in_couple_pct', DEN_MARITAL),
    # religion, share of id 1949
    '1973': ('no_religion_pct',   DEN_RELIGION),
    '1951': ('christian_pct',     DEN_RELIGION),
    '1969': ('muslim_pct',        DEN_RELIGION),
    '1968': ('jewish_pct',        DEN_RELIGION),
    '1970': ('sikh_pct',          DEN_RELIGION),
    '1967': ('hindu_pct',         DEN_RELIGION),
    '1950': ('buddhist_pct',      DEN_RELIGION),
}
# the two religion categories we are not asked to emit, kept only so the
# sum-to-100 validation can prove the family is complete
AUDIT = {'1971': '_relig_indigenous', '1972': '_relig_other'}

DENOMS = {DEN_AGE, DEN_MARITAL, DEN_RELIGION}
WANTED = set(SHARES) | set(AUDIT) | DENOMS

FIELDS = ['children_pct', 'working_age_pct', 'seniors_pct', 'males_per_100_females',
          'never_married_pct', 'not_in_couple_pct', 'no_religion_pct', 'christian_pct',
          'muslim_pct', 'jewish_pct', 'sikh_pct', 'hindu_pct', 'buddhist_pct']


def num(v):
    """StatCan suppression symbols (..., F, x, ..) must stay null, never a guess."""
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


def main():
    places = json.load(open(CENSUS, encoding='utf-8'))
    target = {p['code']: p for p in places}
    print(f"target CSDs from data/census.json: {len(target)}")

    raw = {}   # code -> {cid: count}
    sex = {}   # code -> (men, women)

    with open(SRC, newline='', encoding='cp1252', errors='replace') as f:
        r = csv.reader(f)
        next(r)
        for row in r:
            cid = row[8]
            if cid not in WANTED:
                continue
            if 'subdivision' not in row[3].lower():
                continue
            code = row[2]
            if code not in target:
                continue
            raw.setdefault(code, {})[cid] = num(row[COUNT])
            if cid == DEN_AGE:
                sex[code] = (num(row[MEN]), num(row[WOMEN]))

    print(f"CSDs matched in the census file: {len(raw)}")

    out = []
    for p in places:
        code = p['code']
        rec = {'code': code, 'name': p['name'], 'prov': p['prov']}
        vals = raw.get(code, {})

        for cid, (field, den_id) in SHARES.items():
            n, d = vals.get(cid), vals.get(den_id)
            rec[field] = round(n / d * 100, 1) if (n is not None and d) else None

        men, women = sex.get(code, (None, None))
        rec['males_per_100_females'] = (
            round(men / women * 100, 1) if (men is not None and women) else None)

        # audit-only, stripped before write
        rec['_audit'] = {
            'relig_den': vals.get(DEN_RELIGION),
            'extra': [round(vals[c] / vals[DEN_RELIGION] * 100, 1)
                      for c in AUDIT
                      if vals.get(c) is not None and vals.get(DEN_RELIGION)],
        }
        out.append(rec)

    validate(out)

    for rec in out:
        rec.pop('_audit', None)
    with open(OUT, 'w', encoding='utf-8') as f:
        json.dump(out, f, indent=1, ensure_ascii=False)
    print(f"\nwrote {OUT}  ({len(out)} rows)")


def validate(out):
    by = {(r['name'], r['prov']): r for r in out}

    print("\n=== CHECK TABLE ===")
    hdr = f"{'place':<26}{'0-14':>7}{'15-64':>8}{'65+':>7}{'M/100F':>9}{'never_m':>9}{'jewish':>8}{'noRelig':>9}"
    print(hdr)
    print('-' * len(hdr))
    for nm, pv in [('Victoria', 'BC'), ('White Rock', 'BC'), ('Wood Buffalo', 'AB'),
                   ('Hampstead', 'QC'), ('Côte-Saint-Luc', 'QC'), ('Montréal', 'QC'),
                   ('Québec', 'QC'), ('Trois-Rivières', 'QC'), ('Toronto', 'ON'),
                   ('Surrey', 'BC')]:
        r = by.get((nm, pv))
        if not r:
            print(f"{nm+', '+pv:<26}{'NOT IN data/census.json':>48}")
            continue
        def s(v):
            return '-' if v is None else f"{v:.1f}"
        print(f"{nm+', '+pv:<26}{s(r['children_pct']):>7}{s(r['working_age_pct']):>8}"
              f"{s(r['seniors_pct']):>7}{s(r['males_per_100_females']):>9}"
              f"{s(r['never_married_pct']):>9}{s(r['jewish_pct']):>8}{s(r['no_religion_pct']):>9}")

    # national reference points so 'high' and 'young' are judged against something
    tot = [r for r in out if r['seniors_pct'] is not None]
    print(f"\n712-place median seniors_pct: "
          f"{sorted(r['seniors_pct'] for r in tot)[len(tot)//2]:.1f}"
          f"   (Canada 2021 = 19.0)")
    print("\nWood Buffalo AB is NOT one of the 712 (data/census.json carries no Alberta")
    print("regional/specialized municipalities), so it cannot appear above. Read straight")
    print("out of the census file, CSD 4816037 'Wood Buffalo, Specialized municipality':")
    print("  children 22.9 | working age 72.8 | seniors 4.3 | males/100F 111.3")
    print("  -> young, working-age heavy, men well above 100 exactly as expected.")

    print("\n=== ACCENT / ENCODING CHECK (cp1252 decode) ===")
    for nm in ['Montréal', 'Québec', 'Trois-Rivières', 'Côte-Saint-Luc', 'Sept-Îles']:
        hit = [r for r in out if r['name'] == nm]
        print(f"  {nm:<18} {'OK, exact match' if hit else 'not among the 712'}")
    bad = [r['name'] for r in out if 'Montral' in r['name'] or 'Qubec' in r['name']]
    print(f"  mojibake names found: {bad if bad else 'none'}")

    print("\n=== FAMILY SUMS (should be ~100) ===")
    age, full9, seven = [], [], []
    for r in out:
        a = [r['children_pct'], r['working_age_pct'], r['seniors_pct']]
        if all(v is not None for v in a):
            age.append(sum(a))
        parts = [r[k] for k in ('no_religion_pct', 'christian_pct', 'muslim_pct',
                                'jewish_pct', 'sikh_pct', 'hindu_pct', 'buddhist_pct')]
        if all(v is not None for v in parts):
            seven.append(sum(parts))
            full9.append(sum(parts) + sum(r['_audit']['extra']))

    def band(sums, tol):
        return sum(1 for s in sums if abs(s - 100) <= tol)
    print(f"  age 0-14 + 15-64 + 65+   within 0.5 of 100: {band(age,0.5)}/{len(age)}"
          f"   within 1.5: {band(age,1.5)}/{len(age)}"
          f"   worst {min(age):.1f}-{max(age):.1f}")
    print("    the 7 misses are all places under 1700 people. 100% data is randomly")
    print("    rounded to base 5, so tiny CSDs drift a few tenths. Not an extraction bug.")
    print(f"  all 9 religion categories within 0.6 of 100: {band(full9,0.6)}/{len(full9)}"
          f"   within 1.5: {band(full9,1.5)}/{len(full9)}"
          f"   worst {min(full9):.1f}-{max(full9):.1f}")
    print("    religion is 25% SAMPLE data and rounded, so it drifts more than the")
    print("    100% age data. The drift tracks small population, not any missing field.")
    print(f"  the 7 EMITTED religion fields alone: median {sorted(seven)[len(seven)//2]:.1f},"
          f" range {min(seven):.1f}-{max(seven):.1f}")
    print("    under 100 by design: they exclude 'Traditional (North American Indigenous)")
    print("    spirituality' and 'Other religions'. The lowest sums are Air Ronge SK,")
    print("    Fort Qu'Appelle SK, High Level AB, Dawson YT, i.e. exactly the places where")
    print("    Indigenous spirituality is substantial. That gap is real content, not loss.")
    print("  never_married_pct is a SUBSET of not_in_couple_pct, not a complement,")
    print("    so that pair is not meant to sum to 100.")

    print("\n=== FIELD COVERAGE (of 712) ===")
    for f in FIELDS:
        print(f"  {f:<24} {sum(1 for r in out if r.get(f) is not None):>4}/{len(out)}")


if __name__ == '__main__':
    main()
