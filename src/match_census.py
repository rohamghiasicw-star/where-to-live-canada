import json,re,unicodedata
idx=json.load(open('data/_census_index.json'))
places=json.load(open('data/coords.json'))
def norm(s):
    s=unicodedata.normalize('NFKD',s).encode('ascii','ignore').decode().lower()
    s=re.sub(r'\s*\(.*?\)\s*',' ',s); s=re.sub(r'[^a-z0-9]+',' ',s)
    return re.sub(r'\s+',' ',s).strip()
# name in our list -> census subdivision name(s). multiple = merge (one place, two CSDs).
ALIAS={
 ('Quebec City','QC'):['quebec'], ('Montreal','QC'):['montreal'], ('Trois-Rivieres','QC'):['trois rivieres'],
 ('Gaspe','QC'):['gaspe'], ('Sept-Iles','QC'):['sept iles'], ("Val-d'Or",'QC'):['val d or'],
 ('Saguenay','QC'):['saguenay'], ('Dawson City','YT'):['dawson'],
 ('Kitchener-Waterloo','ON'):['kitchener','waterloo'],
 ('Greater Sudbury','ON'):['greater sudbury grand sudbury','greater sudbury'],
 ('Picton','ON'):['prince edward county'], ('Elora','ON'):['centre wellington'],
 ('Bayfield','ON'):['bluewater'], ('Tobermory','ON'):['northern bruce peninsula'],
 ('Almonte','ON'):['mississippi mills'], ('Salt Spring Island','BC'):['saltspring island'], ('Sydney','NS'):['cape breton'],
 ('Courtenay','BC'):['courtenay'], ('Sechelt','BC'):['sechelt'],
 ('Chester','NS'):['chester'], ('Charlottetown','PE'):['charlottetown'],
 ("St. John's",'NL'):['st john s'], ('Saint John','NB'):['saint john'],
 ('Sault Ste. Marie','ON'):['sault ste marie'], ('Niagara-on-the-Lake','ON'):['niagara on the lake'],
 ('St. Catharines','ON'):['st catharines'], ('St. Andrews','NB'):['saint andrews','st andrews'],
 ('Mont-Tremblant','QC'):['mont tremblant'], ('Saint-Sauveur','QC'):['saint sauveur'],
 ('North Hatley','QC'):['north hatley'], ('Baie-Saint-Paul','QC'):['baie saint paul'],
 ('Rouyn-Noranda','QC'):['rouyn noranda'], ('Grand Falls-Windsor','NL'):['grand falls windsor'],
 ('Prince Albert','SK'):['prince albert'], ('Powell River','BC'):['powell river'],
 ('Annapolis Royal','NS'):['annapolis royal'], ('Mahone Bay','NS'):['mahone bay'],
 ('Port Hope','ON'):['port hope'], ('Owen Sound','ON'):['owen sound'],
 ('North Bay','ON'):['north bay'], ('Thunder Bay','ON'):['thunder bay'],
 ('Red Deer','AB'):['red deer'], ('Medicine Hat','AB'):['medicine hat'],
 ('Grande Prairie','AB'):['grande prairie'], ('Moose Jaw','SK'):['moose jaw'],
 ('Swift Current','SK'):['swift current'], ('Corner Brook','NL'):['corner brook'],
 ('Prince George','BC'):['prince george'], ('Salt Spring','BC'):['capital f'],
}
def pick(cands):
    """prefer the real municipality over same-named parishes/reserves; biggest pop wins"""
    live=[c for c in cands if c.get('pop')]
    return max(live,key=lambda c:c['pop']) if live else (cands[0] if cands else None)
out=[];miss=[]
for p in places:
    n,pr=p['name'],p['prov']
    keys=ALIAS.get((n,pr)) or [norm(n)]
    hits=[]
    for k in keys:
        c=idx.get(f"{k}|{pr}")
        if c: hits.append(pick(c))
    if not hits:
        miss.append(f"{n},{pr}"); out.append({"name":n,"prov":pr}); continue
    if len(hits)==1:
        h=hits[0]
        rec={"name":n,"prov":pr,"csd":h["geo"]}
        for f in ['pop','density','area_km2','median_hh_income','dwell_avg','dwell_median','rent_median','unemployment','pop_change','median_age','owner_burden','tenant_burden','bilingual_pct','french_pct','major_repairs_pct','immigrants_pct','visible_minority_pct','commute_car_pct','commute_transit_pct','commute_walk_pct','commute_bike_pct','commute_short_pct','commute_long_pct']: rec[f]=h.get(f)
    else:  # merge two CSDs into one place (Kitchener-Waterloo)
        tp=sum(h.get('pop') or 0 for h in hits)
        def wavg(f):
            vals=[(h.get(f),h.get('pop') or 0) for h in hits if h.get(f) is not None]
            tot=sum(w for _,w in vals)
            return round(sum(v*w for v,w in vals)/tot,1) if tot else None
        rec={"name":n,"prov":pr,"csd":" + ".join(h['geo'] for h in hits),"pop":tp,
             "area_km2":sum(h.get('area_km2') or 0 for h in hits)}
        for f in ['pop','density','area_km2','median_hh_income','dwell_avg','dwell_median','rent_median','unemployment','pop_change','median_age','owner_burden','tenant_burden','bilingual_pct','french_pct','major_repairs_pct','immigrants_pct','visible_minority_pct','commute_car_pct','commute_transit_pct','commute_walk_pct','commute_bike_pct','commute_short_pct','commute_long_pct']:
            if f in ("pop","area_km2"): continue
            rec[f]=wavg(f)
    pp=rec.get('pop') or 0
    rec['settlement_type']=('big city' if pp>=500000 else 'mid city' if pp>=100000 else
        'small city' if pp>=25000 else 'town' if pp>=5000 else 'village')
    out.append(rec)
json.dump(out,open('data/census.json','w'),indent=1)
print(f"matched {len(places)-len(miss)}/129")
if miss: print("UNMATCHED:", ", ".join(miss))
for f in ['pop','median_hh_income','dwell_avg','rent_median','unemployment']:
    print(f"  {f:18s} {sum(1 for r in out if r.get(f) is not None):3d}/129")
