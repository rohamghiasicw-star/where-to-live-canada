import json,urllib.request,os
from PIL import Image
import numpy as np
places=json.load(open('/Users/rohamghiasi/Desktop/Mover Files/livable/data/coords.json'))
YRS=list(range(2013,2025))
def get(y):
    f=f"/tmp/fw_{y}.tif"
    if not os.path.exists(f) or os.path.getsize(f)<1000:
        u=("https://geo.weather.gc.ca/geomet?SERVICE=WCS&VERSION=2.0.1&REQUEST=GetCoverage"
           "&COVERAGEID=RAQDPS-FW.CE_PM2.5-DIFF-YAvg&FORMAT=image/tiff"
           f"&TIME={y}-01-01T00:00:00Z&SUBSETTINGCRS=EPSG:4326&OUTPUTCRS=EPSG:4326"
           "&SUBSET=x(-141,-52)&SUBSET=y(41,84)")
        urllib.request.urlretrieve(u,f)
    im=Image.open(f); t=im.tag_v2
    sx,sy,_=t[33550]; _,_,_,ox,oy,_=t[33922]
    return np.array(im),ox,oy,sx,sy
data={}
for y in YRS:
    a,ox,oy,sx,sy=get(y); data[y]=(a,ox,oy,sx,sy)
    print(f"{y}: {a.shape} mean={a.mean():.2f} max={a.max():.1f}",flush=True)
def samp(y,lat,lon):
    a,ox,oy,sx,sy=data[y]
    c=int((lon-ox)/sx); r=int((oy-lat)/sy)
    if not(0<=r<a.shape[0] and 0<=c<a.shape[1]): return None
    w=a[max(0,r-1):r+2,max(0,c-1):c+2]
    return float(np.nanmean(w))
out=[]
for p in places:
    v={y:samp(y,p['lat'],p['lon']) for y in YRS}
    ok=[x for x in v.values() if x is not None]
    if not ok: out.append((None,p,v)); continue
    out.append((sum(ok)/len(ok),p,v))
json.dump([{ 'name':p['name'],'prov':p['prov'],'mean_2013_2024':m,
             'by_year':{str(k):val for k,val in v.items()}} for m,p,v in out],
          open('/tmp/fw_towns.json','w'),indent=1)
good=[(m,p,v) for m,p,v in out if m is not None]
good.sort(key=lambda t: t[0], reverse=True)
print(f"\n{len(good)}/{len(places)} towns resolved on the 10km grid")
print("\nTOP 12 smokiest (2013-2024 mean wildfire PM2.5 ug/m3):")
for m,p,v in good[:12]: print(f"  {p['name']:20} {p['prov']:3} {m:5.2f}   2023={v[2023]:.1f}  2018={v[2018]:.1f}")
print("\nCLEANEST 8:")
for m,p,v in good[-8:]: print(f"  {p['name']:20} {p['prov']:3} {m:5.2f}   2023={v[2023]:.1f}")
miss=[p['name'] for m,p,v in out if m is None]
print("\nOFF-GRID:",miss if miss else "none")
