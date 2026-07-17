"""StatCan 17-10-0155: population estimates by census subdivision, July 1 2025
(released 2026-01-14). Four years newer than the 2021 Census, captures shifts
the census can't (Surrey 568k -> 704k). Modelled estimates, not a count, so only
population updates; density/income/dwellings stay on the 2021 Census."""
import csv,json
SRC='/tmp/pop2025/17100155.csv'
# DGUID like 2021A00051207011 -> trailing 7 digits after the type block = CSD code.
# our codes are 7 digits (e.g. Toronto 3520005). extract the last 7 of the DGUID.
est={}
with open(SRC,encoding='utf-8-sig') as f:
    for row in csv.DictReader(f):
        if row['REF_DATE']!='2025': continue
        dg=row['DGUID']
        if 'A0005' not in dg: continue            # A0005 = census subdivision vintage tag
        code=dg.split('A0005')[-1]
        if len(code)!=7: continue
        try: est[code]=int(float(row['VALUE']))
        except: pass
print("2025 CSD estimates:",len(est))
cen=json.load(open('data/census.json'))
hit=0; big=[]
for r in cen:
    e=est.get(r.get('code'))
    if e is not None:
        old=r.get('pop')
        r['pop_2025']=e
        if old and abs(e-old)/old>0.12: big.append((r['name'],int(old),e,round((e-old)/old*100)))
        hit+=1
json.dump(cen,open('data/census.json','w'),indent=1,ensure_ascii=False)
print(f"joined 2025 pop to {hit}/{len(cen)} places")
print("biggest shifts since 2021:")
for n,o,e,p in sorted(big,key=lambda t:-t[3])[:8]: print(f"   {n:22s} {o:>8,} -> {e:>8,}  {p:+d}%")
