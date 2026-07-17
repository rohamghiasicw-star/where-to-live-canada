"""Join the census by CSDUID instead of by name. Name matching gave us a PEI
village of 87 people called Victoria standing in for Victoria BC."""
import json
ap=json.load(open('data/allplaces.json'))
idx=json.load(open('data/_census_index.json'))
bycode={}
for k,v in idx.items():
    for r in v: bycode[r['code']]=r
F=('pop','density','area_km2','median_hh_income','dwell_avg','dwell_median','rent_median',
   'unemployment','pop_change','median_age','owner_burden','tenant_burden','bilingual_pct',
   'french_pct','major_repairs_pct','immigrants_pct','visible_minority_pct','commute_car_pct',
   'commute_transit_pct','commute_walk_pct','commute_bike_pct','commute_short_pct','commute_long_pct')
out=[]
for p in ap:
    r=bycode.get(p['code'])
    if not r: continue
    rec={'name':p['name'],'prov':p['prov'],'code':p['code'],'csd':r['geo']}
    for f in F: rec[f]=r.get(f)
    pp=rec.get('pop') or 0
    rec['settlement_type']=('big city' if pp>=500000 else 'mid city' if pp>=100000 else
        'small city' if pp>=25000 else 'town' if pp>=5000 else 'village')
    out.append(rec)
json.dump(out,open('data/census.json','w'),indent=1,ensure_ascii=False)
print(f"census joined by code: {len(out)}/{len(ap)}")
for f in ['pop','median_hh_income','dwell_avg','median_age','pop_change','commute_short_pct']:
    print(f"  {f:20s} {sum(1 for r in out if r.get(f) is not None):3d}/{len(out)}")
