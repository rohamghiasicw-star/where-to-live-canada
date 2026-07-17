"""2021 Census Profile, census subdivision level. StatCan ships this file as
cp1252, not UTF-8: read it as UTF-8 with error replacement and Montreal silently
becomes 'montral' while the script reports success."""
import csv,json,re,unicodedata,sys
csv.field_size_limit(sys.maxsize)
SRC='/tmp/g5/98-401-X2021005_English_CSV_data.csv'
# id -> (key, denominator id or None). None means the value is already a count/rate.
CH={
 '1':('pop',None), '3':('pop_change',None), '6':('density',None), '7':('area_km2',None),
 '40':('median_age',None),
 '243':('median_hh_income',None),
 '1488':('dwell_median',None), '1489':('dwell_avg',None), '1494':('rent_median',None),
 '2230':('unemployment',None),
 # living factors, each as a share of its own published denominator
 '386':('_bilingual','383'), '390':('_french','388'),
 '1451':('_major_repairs','1449'),
 '1484':('owner_burden',None), '1492':('tenant_burden',None),
 '1529':('_immigrants','1527'),
 '1684':('_visible_minority','1683'),
 '2604':('_commute_car','2603'), '2607':('_commute_transit','2603'),
 '2608':('_commute_walk','2603'), '2609':('_commute_bike','2603'),
 '2612':('_commute_short','2611'), '2616':('_commute_long','2611'),
}
DENOMS={'383','388','1449','1527','1683','2603','2611'}
PROV={'10':'NL','11':'PE','12':'NS','13':'NB','24':'QC','35':'ON','46':'MB','47':'SK',
      '48':'AB','59':'BC','60':'YT','61':'NT','62':'NU'}
def norm(s):
    s=unicodedata.normalize('NFKD',s).encode('ascii','ignore').decode().lower()
    s=re.sub(r'\s*\(.*?\)\s*',' ',s); s=re.sub(r'[^a-z0-9]+',' ',s)
    return re.sub(r'\s+',' ',s).strip()
rows={}
with open(SRC,newline='',encoding='cp1252',errors='replace') as f:
    r=csv.reader(f); next(r)
    for row in r:
        cid=row[8]
        if cid not in CH and cid not in DENOMS: continue
        if 'subdivision' not in row[3].lower(): continue
        code=row[2]; prov=PROV.get(str(code)[:2])
        if not prov: continue
        try: val=float(row[11])
        except: val=None
        d=rows.setdefault((code,prov),{'geo':row[4],'code':code,'prov':prov,'_d':{}})
        if cid in DENOMS: d['_d'][cid]=val
        if cid in CH: d[CH[cid][0]]=val
# turn the counts into shares of their published denominator
for k,v in rows.items():
    for cid,(key,den) in CH.items():
        if not den or not key.startswith('_'): continue
        n=v.get(key); D=v['_d'].get(den)
        v.pop(key,None)
        v[key[1:]+'_pct']=round(n/D*100,1) if (n is not None and D) else None
    v.pop('_d',None)
print("CSDs parsed:",len(rows))
idx={}
for k,v in rows.items():
    idx.setdefault((norm(re.split(r',',v['geo'])[0]),v['prov']),[]).append(v)
json.dump({f"{a}|{b}":v for (a,b),v in idx.items()},open('data/_census_index.json','w'))
print("name|prov keys:",len(idx))
g=idx.get(('goderich','ON'))[0]
print("\nGoderich sample of the living factors:")
for f in ['pop','pop_change','median_age','commute_short_pct','commute_car_pct','commute_transit_pct',
          'immigrants_pct','french_pct','major_repairs_pct','tenant_burden','unemployment']:
    print(f"  {f:22s} {g.get(f)}")
