import json,math
coords=json.load(open('data/coords.json'))
elev=json.load(open('data/elevation.json'))
stations={str(s['stn']):s for s in json.load(open('data/stations.json'))}
norm=json.load(open('data/normals_by_station.json'))
smoke={(s['name'],s['prov']):s for s in json.load(open('data/smoke.json'))}
def hav(a,b,c,d):
    R=6371;p=math.radians
    x=math.sin(p(d-b)/2)**2+math.cos(p(b))*math.cos(p(d))*math.sin(p(c-a)/2)**2
    return 2*R*math.asin(math.sqrt(x))
MAXD={"tmean":60,"tmax":60,"tmin":60,"snow":60,"precip":60,"days_rain":60,
      "days_lt_m20":60,"days_gt30":60,"sun":300,"humidex30":300}
ELEV_TOL=150      # free elevation difference (m)
ELEV_PENALTY=20   # metres of extra elevation diff that cost 1 km of penalty
ELEV_HARD=700     # reject outright beyond this, if anything else exists
def cands(lat,lon,pe):
    out=[]
    for sid,s in stations.items():
        if sid not in norm: continue
        km=hav(lon,lat,s['lon'],s['lat'])
        if km>320: continue
        try: se=float(s['elev'])
        except (TypeError,ValueError): se=None
        if se is None or pe is None:
            cost,ed=km+25,None                      # unknown elevation: mild distrust
        else:
            ed=abs(se-pe)
            cost=km+max(0,ed-ELEV_TOL)/ELEV_PENALTY
        out.append({"km":km,"cost":cost,"ed":ed,"sid":sid,"s":s})
    out.sort(key=lambda t:t['cost'])
    return out
res=[];gaps={}
for pl in coords:
    pe=elev.get(pl['name']+"|"+pl['prov'])
    cs=cands(pl['lat'],pl['lon'],pe)
    rec={"name":pl['name'],"prov":pl['prov'],"lat":pl['lat'],"lon":pl['lon'],
         "elev_m":pe,"climate":{},"stations_used":{}}
    for el,maxd in MAXD.items():
        pick=None
        for tier in (ELEV_HARD,99999):            # try elevation-sane stations first
            for c in cs:
                if el not in norm[c['sid']]: continue
                if c['km']>maxd: continue
                if c['ed'] is not None and c['ed']>tier: continue
                pick=c; break
            if pick: break
        if pick:
            rec['climate'][el]=norm[pick['sid']][el]
            rec['stations_used'][el]={"stn":pick['sid'],"name":pick['s']['name'],
                "km":round(pick['km'],1),"elev":pick['s']['elev'],
                "delev":round(pick['ed']) if pick['ed'] is not None else None,"code":pick['s']['ncode']}
        else:
            rec['climate'][el]=None; gaps[el]=gaps.get(el,0)+1
    sm=smoke.get((pl['name'],pl['prov']))
    rec['smoke']={"mean_ugm3":round(sm['mean_2013_2024'],3),
                  "by_year":{y:round(v,2) for y,v in sm['by_year'].items()},
                  "source":"ECCC RAQDPS-FW.CE wildfire contribution to surface PM2.5, 2013-2024 mean"} if sm else None
    res.append(rec)
json.dump(res,open('data/climate.json','w'),separators=(',',':'))
print("places:",len(res),"| missing:",{k:v for k,v in gaps.items()})
print("\nmountain-town station check (was pulling alpine stations):")
for n in ["Revelstoke","Banff","Canmore","Jasper","Nelson","Whistler","Fernie","Goderich"]:
    r=next((x for x in res if x['name']==n),None)
    su=r['stations_used'].get('snow') or {}
    sn=(r['climate'].get('snow') or {}).get('13')
    print(f"  {n:11s} elev={str(r['elev_m']):>6s}m  snow={str(sn):>8s}cm  <- {su.get('name','?'):24s} {str(su.get('km')):>5s}km  delev={su.get('delev')}m")
