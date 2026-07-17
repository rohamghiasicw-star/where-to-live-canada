import json,urllib.request,collections
clim=json.load(open('data/climate.json'))
elev=json.load(open('data/elevation.json'))
FIELDS={"tmean":"MEAN_TEMPERATURE","tmax":"MAX_TEMPERATURE","tmin":"MIN_TEMPERATURE",
        "snow":"TOTAL_SNOWFALL","precip":"TOTAL_PRECIPITATION"}
def monthly(stn,since="1971-01"):
    rows=[];off=0
    while True:
        u=(f"https://api.weather.gc.ca/collections/climate-monthly/items?f=json&limit=10000&offset={off}"
           f"&STN_ID={stn}&datetime={since}/2020-12")
        d=json.load(urllib.request.urlopen(u,timeout=120)); rows+=d['features']
        if len(d['features'])<10000: break
        off+=10000
    return rows
def compute(stn,keys):
    rows=monthly(stn); acc={}
    for f in rows:
        p=f['properties']; m=p['LOCAL_MONTH']
        for k in keys:
            v=p.get(FIELDS[k])
            if v is None: continue
            acc.setdefault(k,{}).setdefault(m,[]).append(v)
    out={}
    for k,per in acc.items():
        if len(per)<12 or min(len(v) for v in per.values())<10: continue
        mv={str(m):round(sum(v)/len(v),2) for m,v in per.items()}
        mv["13"]=round(sum(mv[str(m)] for m in range(1,13)),2) if k in ("snow","precip") \
                 else round(sum(mv[str(m)] for m in range(1,13))/12,2)
        out[k]=(mv,min(len(v) for v in per.values()))
    return out
# Revelstoke: town-elevation station with a real 24-year snow record
r=next(x for x in clim if x['name']=='Revelstoke')
got=compute(1372,["snow","precip","tmax","tmin"])
for k,(mv,yrs) in got.items():
    r['climate'][k]=mv
    r['stations_used'][k]={"stn":"1372","name":"REVELSTOKE AIRPORT RD","km":4.0,"elev":"450.00",
        "delev":round(abs(450-elev['Revelstoke|BC'])),"code":"COMPUTED",
        "note":f"mean of {yrs}+ years of ECCC monthly observations"}
    print(f"Revelstoke {k:7s} -> {mv['13']} ({yrs} yrs, 450m)")
# sweep: null any element still sourced from a wildly wrong elevation
KILL=600
killed=collections.Counter()
for rec in clim:
    for el,su in list(rec['stations_used'].items()):
        if (su.get('delev') or 0)>KILL:
            rec['climate'][el]=None; rec['stations_used'].pop(el)
            killed[f"{rec['name']}/{el}"]+=1
json.dump(clim,open('data/climate.json','w'),separators=(',',':'))
print("\nnulled for elevation mismatch >600m:",dict(killed) or "none")
de=[ (x['stations_used'].get('tmean') or {}).get('delev') for x in clim]
de=[d for d in de if d is not None]
print(f"tmean elevation delta: median {sorted(de)[len(de)//2]}m, max {max(de)}m")
print("snowiest now:")
s=sorted([x for x in clim if (x['climate'].get('snow') or {}).get('13')],key=lambda x:-x['climate']['snow']['13'])[:5]
for x in s:
    su=x['stations_used']['snow']
    print(f"  {x['name']:14s} {x['climate']['snow']['13']:6.1f}cm <- {su['name']} (delev {su.get('delev')}m)")
