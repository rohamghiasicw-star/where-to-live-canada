import json,urllib.request,time,os
# ECCC Canadian Climate Normals 1981-2010. Trimmed to what the app scores on.
ELEMENTS={1:"tmean",5:"tmax",8:"tmin",54:"snow",56:"precip",102:"sun",
          44:"days_lt_m20",37:"days_gt30",46:"humidex30",61:"days_rain"}
MONTHLY={"tmean","tmax","tmin","snow","precip","sun"}   # keep 12 months + annual
def fetch(nid):
    rows=[];off=0
    while True:
        u=("https://api.weather.gc.ca/collections/climate-normals/items?f=json"
           f"&limit=10000&offset={off}&NORMAL_ID={nid}")
        d=json.load(urllib.request.urlopen(u,timeout=180))
        fs=d['features']; rows+=fs
        if len(fs)<10000 or len(rows)>=d.get('numberMatched',0): break
        off+=10000
    return rows
data={}
for nid,key in ELEMENTS.items():
    try:
        rows=fetch(nid); kept=0
        for f in rows:
            p=f['properties']
            if p.get('VALUE') is None: continue
            m=p['MONTH']
            if key not in MONTHLY and m!=13: continue   # annual only for the rest
            data.setdefault(str(p['STN_ID']),{}).setdefault(key,{})[m]=round(p['VALUE'],2); kept+=1
        print(f"{key:12s} nid={nid:3d} rows={len(rows):6d} kept={kept:6d} stns={sum(1 for s in data if key in data[s]):4d}",flush=True)
    except Exception as e:
        print(f"{key:12s} nid={nid} FAILED {e}",flush=True)
    time.sleep(0.4)
json.dump(data,open('data/normals_by_station.json','w'),separators=(',',':'))
print("stations:",len(data),"| KB:",round(os.path.getsize('data/normals_by_station.json')/1024))
