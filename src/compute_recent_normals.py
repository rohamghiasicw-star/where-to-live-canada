"""Compute 1991-2020 climate normals per town from ECCC monthly observations.
Per-town bbox query to climate-monthly returns every nearby station's records;
compute the normal from the nearest station with real coverage, and fall back to
the official 1981-2010 normal where recent coverage is too thin. Every town is
labelled with the period and station it actually got."""
import urllib.request,urllib.parse,json,math,collections,time,sys
coords=json.load(open('data/coords.json'))
elev=json.load(open('data/elevation.json'))
base=json.load(open('data/climate.json'))          # current official 1981-2010, the fallback
byname={(r['name'],r['prov']):r for r in base}
def hav(a,b,c,d):
    R=6371;p=math.radians
    x=math.sin(p(d-b)/2)**2+math.cos(p(b))*math.cos(p(d))*math.sin(p(c-a)/2)**2
    return 2*R*math.asin(math.sqrt(x))
FIELDS={'tmean':'MEAN_TEMPERATURE','tmax':'MAX_TEMPERATURE','tmin':'MIN_TEMPERATURE',
        'snow':'TOTAL_SNOWFALL','precip':'TOTAL_PRECIPITATION'}
def fetch(lat,lon,box=0.55):
    u=("https://api.weather.gc.ca/collections/climate-monthly/items?f=json&limit=25000"
       f"&datetime=1991-01/2020-12&bbox={lon-box*1.4},{lat-box},{lon+box*1.4},{lat+box}")
    for _ in range(3):
        try: return json.load(urllib.request.urlopen(u,timeout=120))['features']
        except Exception: time.sleep(2)
    return []
def station_normal(recs):
    acc=collections.defaultdict(lambda: collections.defaultdict(list)); meta={}
    for f in recs:
        p=f['properties']; m=p.get('LOCAL_MONTH')
        meta.setdefault('name',p.get('STATION_NAME')); meta['lat']=p.get('LATITUDE'); meta['lon']=p.get('LONGITUDE')
        for k,col in FIELDS.items():
            v=p.get(col)
            if v is None: continue
            if col=='MEAN_TEMPERATURE' and (p.get('DAYS_WITH_VALID_MEAN_TEMP') or 0)<20: continue
            acc[k][m].append(v)
    out={}
    for k,per in acc.items():
        if len(per)<12: continue
        if k=='tmean' and min(len(per[m]) for m in per)<15: continue    # >=15 years each month
        mv={str(m):round(sum(vs)/len(vs),2) for m,vs in per.items()}
        mv['13']=round(sum(mv[str(m)] for m in range(1,13) if str(m) in mv),2) if k in ('snow','precip') \
                 else round(sum(mv[str(m)] for m in range(1,13) if str(m) in mv)/12,2)
        out[k]=mv
    yrs=min((len(acc['tmean'][m]) for m in acc.get('tmean',{})),default=0)
    return out,meta,yrs
res=[];up=0;kept=0
for i,pl in enumerate(coords):
    lat,lon=pl['lat'],pl['lon']; pe=elev.get(pl['name']+'|'+pl['prov'])
    recs=fetch(lat,lon)
    bystn=collections.defaultdict(list)
    for f in recs: bystn[f['properties'].get('STN_ID')].append(f)
    cand=[]
    for stn,rs in bystn.items():
        norm,meta,yrs=station_normal(rs)
        if 'tmean' not in norm or meta.get('lat') is None: continue
        try: la,lo=float(meta['lat']),float(meta['lon'])
        except: continue
        km=hav(lon,lat,lo,la)
        if km>60: continue
        cand.append((km,stn,norm,meta,yrs))
    cand.sort(key=lambda t:t[0])
    b=byname[(pl['name'],pl['prov'])]
    if cand:
        km,stn,norm,meta,yrs=cand[0]
        rec={'name':pl['name'],'prov':pl['prov'],'climate':dict(b['climate']),'stations_used':dict(b['stations_used']),
             'smoke':b.get('smoke'),'elev_m':b.get('elev_m')}
        for k,mv in norm.items():                       # upgrade temp/snow/precip to recent
            rec['climate'][k]=mv
            rec['stations_used'][k]={'stn':stn,'name':meta['name'],'km':round(km,1),
                'elev':None,'delev':None,'code':'RECENT','note':f'1991-2020 mean of {yrs}+ years of ECCC monthly observations'}
        rec['period']='1991-2020'
        up+=1
    else:
        rec=dict(b); rec['period']='1981-2010'; kept+=1
    res.append(rec)
    if (i+1)%60==0:
        json.dump(res,open('data/climate_recent.json','w'),separators=(',',':'))
        print(f"  {i+1}/{len(coords)}  upgraded={up} kept-official={kept}",flush=True)
    time.sleep(0.3)
json.dump(res,open('data/climate_recent.json','w'),separators=(',',':'))
print(f"DONE. upgraded to 1991-2020: {up}, kept official 1981-2010: {kept}",flush=True)
