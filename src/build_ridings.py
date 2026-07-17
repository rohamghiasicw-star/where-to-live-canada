import json,re
from xml.etree import ElementTree as ET
KML='/tmp/fed23/kml/doc.kml'
NS='{http://www.opengis.net/kml/2.2}'
places=json.load(open('data/coords.json'))
def rings_of(pm):
    out=[]
    for poly in pm.iter(NS+'Polygon'):
        ob=poly.find(f'{NS}outerBoundaryIs/{NS}LinearRing/{NS}coordinates')
        if ob is None or not ob.text: continue
        pts=[]
        for tok in ob.text.split():
            a=tok.split(',')
            if len(a)>=2: pts.append((float(a[0]),float(a[1])))
        if len(pts)>3: out.append(pts)
    return out
def inside(x,y,ring):
    c=False; n=len(ring)
    for i in range(n):
        x1,y1=ring[i]; x2,y2=ring[(i+1)%n]
        if ((y1>y)!=(y2>y)) and (x < (x2-x1)*(y-y1)/(y2-y1+1e-18)+x1): c=not c
    return c
found={}
n=0
for ev,el in ET.iterparse(KML,events=('end',)):
    if el.tag!=NS+'Placemark': continue
    nm=el.find(NS+'name')
    name=nm.text if nm is not None else None
    if name:
        n+=1
        rs=rings_of(el)
        if rs:
            xs=[p[0] for r in rs for p in r]; ys=[p[1] for r in rs for p in r]
            bb=(min(xs),min(ys),max(xs),max(ys))
            for p in places:
                k=(p['name'],p['prov'])
                if k in found: continue
                if not (bb[0]<=p['lon']<=bb[2] and bb[1]<=p['lat']<=bb[3]): continue
                if any(inside(p['lon'],p['lat'],r) for r in rs):
                    found[k]=name
    el.clear()
print(f"placemarks scanned: {n}")
print(f"places located in a riding: {len(found)}/129")
miss=[f"{a},{b}" for (a,b) in [(p['name'],p['prov']) for p in places] if (a,b) not in found]
if miss: print("NOT IN ANY RIDING:", ", ".join(miss))
json.dump({f"{k[0]}|{k[1]}":v for k,v in found.items()},open('data/place_riding.json','w'),indent=1)
for k in [('Goderich','ON'),('Halifax','NS'),('Calgary','AB'),('Vancouver','BC'),('Iqaluit','NU'),('Toronto','ON')]:
    print(f"  {k[0]:12s} -> {found.get(k)}")
