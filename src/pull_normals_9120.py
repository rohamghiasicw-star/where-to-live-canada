"""Pull Canadian Climate Normals 1991-2020, per station, from the legacy bulk
endpoint. Flow: station_select (per prov) -> climate_ids -> results page (has the
big stnID in its dl-data form) -> bulk CSV -> parse. Coordinates come from the
GeoMet climate-stations API, matched by climate_id (exact)."""
import urllib.request,urllib.parse,re,json,time,sys
UA={"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) Chrome/120 Safari/537.36","Cookie":"jsenabled=1"}
def get(u,timeout=45):
    for _ in range(3):
        try:
            return urllib.request.urlopen(urllib.request.Request(u,headers=UA),timeout=timeout).read().decode('utf-8','replace')
        except Exception:
            time.sleep(2)
    return ''
# 1) climate_id -> coords, from GeoMet (exact)
print("building climate_id -> coords from GeoMet...",flush=True)
coords={}
gm=json.load(urllib.request.urlopen("https://api.weather.gc.ca/collections/climate-stations/items?limit=15000&HAS_NORMALS_DATA=Y&COUNTRY=CAN&f=json",timeout=90))
for f in gm['features']:
    p=f['properties']; g=f['geometry']['coordinates'] if f.get('geometry') else None
    cid=str(p.get('CLIMATE_IDENTIFIER') or '').strip()
    if cid and g: coords[cid]={'lat':round(g[1],5),'lon':round(g[0],5),'elev':p.get('ELEVATION')}
print(f"  {len(coords)} station coords",flush=True)
PROVS=['BC','AB','SK','MB','ON','QC','NB','NS','PE','NL','YT','NT','NU']
BASE="https://climate.weather.gc.ca/climate_normals/"
COLS=['jan','feb','mar','apr','may','jun','jul','aug','sep','oct','nov','dec','year']
ELEM={'Daily Average (°C)':'tmean','Daily Maximum (°C)':'tmax','Daily Minimum (°C)':'tmin',
      'Snowfall (cm)':'snow','Precipitation (mm)':'precip','Rainfall (mm)':'rain'}
def parse_csv(txt):
    out={}
    for line in txt.splitlines():
        if not line.startswith('"') or 'NORMALS_ELEMENT' in line: continue
        parts=next(iter([list(re.findall(r'"((?:[^"]|"")*)"',line))]),None)
        if not parts or len(parts)<18: continue
        elem=parts[4]
        key=ELEM.get(elem)
        if not key: continue
        vals=parts[5:18]  # jan..dec + year
        mv={}
        for i,v in enumerate(vals):
            v=v.strip()
            if v=='' : continue
            try: mv[str(i+1) if i<12 else '13']=round(float(v),2)
            except: pass
        if mv: out[key]=mv
    return out
def stn_id_and_name(cid,prov):
    u=BASE+"results_1991_2020_e.html?"+urllib.parse.urlencode(
        {'searchType':'stnProv','lstProvince':prov,'selRowPerPage':100,'startRow':1,'climate_id':cid,'dispBack':0})
    h=get(u)
    i=h.find('id="dl-data"')
    if i<0: return None,None
    blk=h[i:i+1400]
    sid=re.search(r'name="stnID"\s*value="([0-9]+)"|value="([0-9]+)"\s*name="stnID"',blk)
    nm=re.search(r'name="stnname"\s*value="([^"]*)"|value="([^"]*)"\s*name="stnname"',blk)
    return (sid.group(1) or sid.group(2)) if sid else None, (nm.group(1) or nm.group(2)) if nm else None
data={}; total=0; fails=0
for prov in PROVS:
    cids=set(); start=1
    while True:   # selRowPerPage caps at 100, so page through startRow
        sel=get(BASE+"station_select_1991_2020_e.html?"+urllib.parse.urlencode(
            {'searchType':'stnProv','lstProvince':prov,'selRowPerPage':100,'startRow':start}))
        page=set(re.findall(r'climate_id=([0-9A-Z]+)',sel))
        new_ids=page-cids
        if not new_ids: break
        cids|=page; start+=100
        if start>2000: break
        time.sleep(0.4)
    cids=sorted(cids)
    print(f"{prov}: {len(cids)} stations",flush=True)
    for cid in cids:
        sid,nm=stn_id_and_name(cid,prov); time.sleep(0.5)
        if not sid: fails+=1; continue
        csv=get(BASE+"bulk_data_e.html?"+urllib.parse.urlencode(
            {'ffmt':'csv','lang':'e','prov':prov,'yr':1991,'stnID':sid,'climate_id':cid,'submit':'Download Data'}))
        el=parse_csv(csv); time.sleep(0.4)
        if not el.get('tmean') and not el.get('snow'): continue
        rec={'name':nm,'prov':prov,**el}
        c=coords.get(cid)
        if c: rec.update(c)
        data[cid]=rec; total+=1
        if total%50==0: print(f"  ...{total} pulled",flush=True)
    json.dump(data,open('data/normals_1991_2020_by_station.json','w'),separators=(',',':'))
print(f"DONE. stations={total} fails={fails}",flush=True)
tor=data.get('6158355')
if tor: print("Toronto City Jan tmean:",(tor.get('tmean') or {}).get('1'),"annual:",(tor.get('tmean') or {}).get('13'))
