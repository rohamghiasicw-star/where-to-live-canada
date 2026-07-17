import json,urllib.request,time,math
places=json.load(open('data/coords.json'))
cen={(r['name'],r['prov']):r for r in json.load(open('data/census.json'))}
# metro anchors over ~500k. Ottawa-Gatineau counted once.
# Every Canadian CMA over 300,000 (2021 Census). This is what "a real city" means:
# an airport, hospitals, jobs, a university. London is in here because it is exactly
# the drive the whole idea started from.
ANCHORS=[("Toronto","ON",43.6535,-79.3839),("Montreal","QC",45.5019,-73.5674),
 ("Vancouver","BC",49.2827,-123.1207),("Ottawa","ON",45.4209,-75.6901),
 ("Calgary","AB",51.0447,-114.0719),("Edmonton","AB",53.5461,-113.4938),
 ("Quebec City","QC",46.8139,-71.2080),("Winnipeg","MB",49.8951,-97.1384),
 ("Hamilton","ON",43.2557,-79.8711),("Kitchener-Waterloo","ON",43.4516,-80.4925),
 ("London","ON",42.9849,-81.2453),("Halifax","NS",44.6488,-63.5752),
 ("St. Catharines","ON",43.1594,-79.2469),("Windsor","ON",42.3149,-83.0364),
 ("Oshawa","ON",43.8971,-78.8658),("Victoria","BC",48.4284,-123.3656),
 ("Saskatoon","SK",52.1332,-106.6700)]

def hav(a,b,c,d):
    R=6371;p=math.radians
    x=math.sin(p(d-b)/2)**2+math.cos(p(b))*math.cos(p(d))*math.sin(p(c-a)/2)**2
    return 2*R*math.asin(math.sqrt(x))
def table(srcs,dsts):
    coords=";".join(f"{lo:.5f},{la:.5f}" for la,lo in srcs+dsts)
    si=";".join(str(i) for i in range(len(srcs)))
    di=";".join(str(i+len(srcs)) for i in range(len(dsts)))
    u=(f"http://router.project-osrm.org/table/v1/driving/{coords}"
       f"?sources={si}&destinations={di}&annotations=duration,distance")
    d=json.load(urllib.request.urlopen(u,timeout=120))
    return d.get('durations'),d.get('distances')
A=[(a[2],a[3]) for a in ANCHORS]
out=[];B=18
for i in range(0,len(places),B):
    chunk=places[i:i+B]
    S=[(p['lat'],p['lon']) for p in chunk]
    try:
        dur,dist=table(S,A)
    except Exception as e:
        print("batch",i,"FAILED",e); dur=dist=None
    for j,p in enumerate(chunk):
        rec={"name":p['name'],"prov":p['prov']}
        row=dur[j] if dur else None
        best=None
        if row:
            cand=[(row[k],dist[j][k],ANCHORS[k]) for k in range(len(A)) if row[k] is not None]
            if cand: best=min(cand,key=lambda t:t[0])
        if best:
            rec.update({"nearest_big_city":best[2][0],
                        "drive_min_to_big_city":round(best[0]/60,1),
                        "km_to_big_city":round(best[1]/1000,1),"routed":True})
        else:
            gc=min(((hav(p['lon'],p['lat'],a[3],a[2]),a) for a in ANCHORS),key=lambda t:t[0])
            rec.update({"nearest_big_city":gc[1][0],"km_to_big_city":round(gc[0]*1.25,1),
                        "drive_min_to_big_city":None,"routed":False,
                        "note":"no road route (fly-in); straight-line distance only"})
        # a place that IS an anchor is its own city
        if (p['name'],p['prov']) in [(a[0],a[1]) for a in ANCHORS]:
            rec.update({"nearest_big_city":p['name'],"drive_min_to_big_city":0.0,"km_to_big_city":0.0})
        out.append(rec)
    print(f"  routed {min(i+B,len(places))}/{len(places)}",flush=True)
    time.sleep(1.0)
json.dump(out,open('data/proximity.json','w'),indent=1)
ok=sum(1 for r in out if r.get('drive_min_to_big_city') is not None)
print(f"\nrouted {ok}/129")
for n in ["Goderich","Tofino","Iqaluit","Churchill","Toronto","Halifax","Dawson"]:
    r=next((x for x in out if x['name']==n),None)
    if not r: continue
    print(f"  {n:12s} -> {str(r['nearest_big_city']):18s} {str(r.get('drive_min_to_big_city')):>7s}min {str(r.get('km_to_big_city')):>7s}km routed={r.get('routed')}")
