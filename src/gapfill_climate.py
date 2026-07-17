import json,math,urllib.request,time
coords={ (p['name'],p['prov']):p for p in json.load(open('data/coords.json'))}
elev=json.load(open('data/elevation.json'))
clim=json.load(open('data/climate.json'))
allst=json.load(open('https://' and 'data/stations_all.json')) if False else None
def hav(a,b,c,d):
    R=6371;p=math.radians
    x=math.sin(p(d-b)/2)**2+math.cos(p(b))*math.cos(p(d))*math.sin(p(c-a)/2)**2
    return 2*R*math.asin(math.sqrt(x))
def stations_near(lat,lon,box=0.9):
    u=(f"https://api.weather.gc.ca/collections/climate-stations/items?limit=200&f=json"
       f"&bbox={lon-box*1.4},{lat-box},{lon+box*1.4},{lat+box}")
    d=json.load(urllib.request.urlopen(u,timeout=90))
    out=[]
    for f in d['features']:
        p=f['properties']
        if p.get('HAS_MONTHLY_SUMMARY')!='Y': continue
        g=f['geometry']['coordinates']
        out.append({"stn":p['STN_ID'],"name":p['STATION_NAME'],"lat":g[1],"lon":g[0],
                    "elev":p.get('ELEVATION'),"first":str(p.get('MLY_FIRST_DATE'))[:4],
                    "last":str(p.get('MLY_LAST_DATE'))[:4],"km":hav(lon,lat,g[0],g[1])})
    return out
def monthly(stn):
    rows=[];off=0
    while True:
        u=(f"https://api.weather.gc.ca/collections/climate-monthly/items?f=json&limit=10000&offset={off}"
           f"&STN_ID={stn}&datetime=1981-01/2020-12")
        d=json.load(urllib.request.urlopen(u,timeout=120))
        rows+=d['features']
        if len(d['features'])<10000: break
        off+=10000
    return rows
FIELDS={"tmean":"MEAN_TEMPERATURE","snow":"TOTAL_SNOWFALL","precip":"TOTAL_PRECIPITATION"}
targets=[r for r in clim if r['climate'].get('tmean') is None]
# Revelstoke: has data but from a 1890m/1330m alpine station. force a redo.
for r in clim:
    su=r['stations_used'].get('snow') or {}
    if (su.get('delev') or 0)>500: targets.append(r)
print("gap-fill targets:",[f"{r['name']},{r['prov']}" for r in targets])
report=[]
for r in targets:
    pe=elev.get(r['name']+"|"+r['prov'])
    try: cs=stations_near(r['lat'],r['lon'])
    except Exception as e: print(r['name'],"bbox err",e); continue
    def ok(s):
        try: se=float(s['elev'])
        except: return False
        if pe is not None and abs(se-pe)>350: return False
        return s['km']<=55 and s['first'].isdigit() and s['last'].isdigit() and int(s['last'])>=1985
    cs=[s for s in cs if ok(s)]
    cs.sort(key=lambda s:(s['km']))
    best=None
    for s in cs[:6]:
        try: rows=monthly(s['stn'])
        except Exception as e: continue
        acc={}
        for f in rows:
            p=f['properties']; m=p.get('LOCAL_MONTH')
            for key,col in FIELDS.items():
                v=p.get(col)
                if v is None: continue
                if col=="MEAN_TEMPERATURE" and (p.get('DAYS_WITH_VALID_MEAN_TEMP') or 0)<25: continue
                acc.setdefault(key,{}).setdefault(m,[]).append(v)
        yrs=min((len(v) for v in acc.get('tmean',{}).values()), default=0)
        if yrs>=12:
            best=(s,acc,yrs); break
    if not best:
        print(f"  {r['name']:16s} NO usable monthly station"); report.append((r['name'],None,None,0)); continue
    s,acc,yrs=best
    for key,per in acc.items():
        if len(per)<12: continue
        mv={str(m):round(sum(v)/len(v),2) for m,v in per.items()}
        if key in ("snow","precip"): mv["13"]=round(sum(mv[str(m)] for m in range(1,13) if str(m) in mv),2)
        else: mv["13"]=round(sum(mv[str(m)] for m in range(1,13) if str(m) in mv)/12,2)
        r['climate'][key]=mv
        r['stations_used'][key]={"stn":str(s['stn']),"name":s['name'],"km":round(s['km'],1),
            "elev":s['elev'],"delev":round(abs(float(s['elev'])-pe)) if pe else None,
            "code":"COMPUTED","note":f"mean of {yrs}+ years of ECCC monthly observations 1981-2020"}
    print(f"  {r['name']:16s} <- {s['name']:26s} {s['km']:4.1f}km elev={s['elev']} yrs={yrs}  Jan={r['climate']['tmean'].get('1')}C")
    report.append((r['name'],s['name'],round(s['km'],1),yrs))
    time.sleep(0.3)
json.dump(clim,open('data/climate.json','w'),separators=(',',':'))
json.dump(report,open('research/gapfill-report.json','w'),indent=1)
print("\nstill missing tmean:",sum(1 for r in clim if r['climate'].get('tmean') is None))
