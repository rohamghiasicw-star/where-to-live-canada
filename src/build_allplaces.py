"""Expand from 129 hand-picked places to every real Canadian community:
population >= 1000 living at density >= 100/km2, plus the original 129.

Coordinates come from two independent sources that check each other:
  1. Nominatim, which returns the town centre but can resolve a name to a
     region (it put Kenora at 54.0N, in the middle of Kenora District).
  2. The CSD polygon centroid, which is exact for the subdivision but lands
     in the bush for huge municipalities (Gaspe's is 118km from the town).
Where they disagree, the compactness of the CSD decides which to believe."""
import json,math,re,unicodedata,urllib.request,urllib.parse,time,sys
PROVN={"BC":"British Columbia","AB":"Alberta","SK":"Saskatchewan","MB":"Manitoba","ON":"Ontario",
"QC":"Quebec","NB":"New Brunswick","NS":"Nova Scotia","PE":"Prince Edward Island",
"NL":"Newfoundland and Labrador","YT":"Yukon","NT":"Northwest Territories","NU":"Nunavut"}
BB={"BC":(48.2,60.1,-139.1,-114.0),"AB":(48.9,60.1,-120.1,-109.9),"SK":(48.9,60.1,-110.1,-101.3),
"MB":(48.9,60.1,-102.1,-88.9),"ON":(41.6,56.9,-95.2,-74.3),"QC":(44.9,62.7,-79.8,-57.0),
"NB":(44.5,48.1,-69.1,-63.7),"NS":(43.3,47.1,-66.4,-59.7),"PE":(45.9,47.1,-64.5,-61.9),
"NL":(46.6,60.4,-59.5,-52.5),"YT":(60.0,69.7,-141.1,-123.7),"NT":(60.0,78.8,-136.5,-102.0),
"NU":(60.0,83.2,-120.0,-61.0)}
def hav(a,b,c,d):
    R=6371;p=math.radians
    x=math.sin(p(d-b)/2)**2+math.cos(p(b))*math.cos(p(d))*math.sin(p(c-a)/2)**2
    return 2*R*math.asin(math.sqrt(x))
cd=json.load(open('data/csd_coords.json'))
idx=json.load(open('data/_census_index.json'))
rows={}
for k,v in idx.items():
    for r in v: rows[r['code']]=r
old=json.load(open('data/coords.json'))
oldcen={r['csd'].split(',')[0]:r for r in json.load(open('data/census.json'))}
oldc={p['name']:p for p in old}
sel=[]
for code,r in rows.items():
    pop=r.get('pop') or 0; den=r.get('density') or 0
    if not (pop>=1000 and den>=100): continue
    sel.append(code)
# always keep the original 129 whatever the filter says
keepgeo={r['csd'].split(',')[0] for r in json.load(open('data/census.json'))}
for code,r in rows.items():
    if code in sel: continue
    if r['geo'].split(',')[0] in keepgeo: sel.append(code)
print("target places:",len(sel))
def short(geo):   # 'Goderich, Town (T)' -> 'Goderich'
    return re.split(r',',geo)[0].strip()
UA={"User-Agent":"where-to-live-canada/1.0 (rohamghiasicw@gmail.com)"}
def geocode(name,prov):
    u="https://nominatim.openstreetmap.org/search?"+urllib.parse.urlencode(
        {"q":f"{name}, {PROVN[prov]}, Canada","format":"json","limit":1})
    try:
        r=json.load(urllib.request.urlopen(urllib.request.Request(u,headers=UA),timeout=30))
        if not r: return None
        return float(r[0]['lat']),float(r[0]['lon']),r[0].get('display_name','')
    except Exception:
        return None
out=[];stats={'reused':0,'centroid':0,'nominatim':0,'centroid_fallback':0,'failed':0}
for i,code in enumerate(sorted(sel)):
    r=rows[code]; nm=short(r['geo']); prov=r['prov']
    cc=cd.get(code)
    rec={"name":nm,"prov":prov,"code":code,"csd":r['geo'],
         "pop":r.get('pop'),"density":r.get('density'),
         "land_km2":cc['land_km2'] if cc else None}
    if nm in oldc and oldc[nm]['prov']==prov:      # already audited, do not touch
        rec.update(lat=oldc[nm]['lat'],lon=oldc[nm]['lon'],coord_src='audited')
        stats['reused']+=1; out.append(rec); continue
    if not cc: stats['failed']+=1; continue
    land=cc['land_km2'] or 0
    if land<=60:                                   # compact: the centroid IS the town
        rec.update(lat=cc['lat'],lon=cc['lon'],coord_src='csd centroid')
        stats['centroid']+=1; out.append(rec); continue
    g=geocode(nm,prov); time.sleep(1.05)
    if not g:
        rec.update(lat=cc['lat'],lon=cc['lon'],coord_src='csd centroid (geocode failed)')
        stats['centroid_fallback']+=1; out.append(rec); continue
    la,lo,disp=g
    lo_,hi,wl,wr=BB[prov]
    inprov = lo_<=la<=hi and wl<=lo<=wr
    isregion = re.search(r'^(District|County|Region|Regional|Territory|Census)',disp.split(',')[0].strip(),re.I)
    far = hav(lo,la,cc['lon'],cc['lat'])
    # trust the geocode unless it left the province, named a region, or ran far
    # from a CSD compact enough that it should not have
    if (not inprov) or isregion or (far>40 and land<400):
        rec.update(lat=cc['lat'],lon=cc['lon'],coord_src=f'csd centroid (geocode rejected, {far:.0f}km off)')
        stats['centroid_fallback']+=1
    else:
        rec.update(lat=la,lon=lo,coord_src='nominatim',osm=disp[:90])
        stats['nominatim']+=1
    out.append(rec)
    if (i+1)%75==0: print(f"  {i+1}/{len(sel)}  {stats}",flush=True)
json.dump(out,open('data/allplaces.json','w'),indent=1,ensure_ascii=False)
print("\nplaces:",len(out),stats)
