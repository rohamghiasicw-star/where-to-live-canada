import json,math
# EPSG:3347 NAD83 / Statistics Canada Lambert (spherical approximation - fine for a stylized sheet)
P1,P2,LAT0,LON0 = map(math.radians,(49.0,77.0,63.390675,-91.866666666))
def lcc(lon,lat):
    phi,lam=math.radians(lat),math.radians(lon)
    phi=max(min(phi,math.radians(89.9)),math.radians(-89.9))
    t=lambda p: math.tan(math.pi/4+p/2)
    n=math.log(math.cos(P1)/math.cos(P2))/math.log(t(P2)/t(P1))
    F=math.cos(P1)*(t(P1)**n)/n
    rho=F/(t(phi)**n); rho0=F/(t(LAT0)**n)
    th=n*(lam-LON0)
    return rho*math.sin(th), rho0-rho*math.cos(th)
def dp(pts,tol):
    if len(pts)<3: return pts
    def d(p,a,b):
        if a==b: return math.hypot(p[0]-a[0],p[1]-a[1])
        t=((p[0]-a[0])*(b[0]-a[0])+(p[1]-a[1])*(b[1]-a[1]))/((b[0]-a[0])**2+(b[1]-a[1])**2)
        t=max(0,min(1,t)); return math.hypot(p[0]-(a[0]+t*(b[0]-a[0])),p[1]-(a[1]+t*(b[1]-a[1])))
    dm,idx=0,0
    for i in range(1,len(pts)-1):
        dd=d(pts[i],pts[0],pts[-1])
        if dd>dm: dm,idx=dd,i
    if dm>tol: return dp(pts[:idx+1],tol)[:-1]+dp(pts[idx:],tol)
    return [pts[0],pts[-1]]
def ring_area(r):
    return abs(sum(r[i][0]*r[i+1][1]-r[i+1][0]*r[i][1] for i in range(len(r)-1))/2)

d=json.load(open('/tmp/ne_prov.geojson'))
TOL=0.0014; MIN_AREA=0.00006
PROV_TOL={'Nunavut':0.0030,'Northwest Territories':0.0022,'Newfoundland and Labrador':0.0016}
MAX_RINGS=6
out={}
for f in d['features']:
    p=f['properties']
    if p.get('admin')!='Canada': continue
    name=p.get('name'); geom=f['geometry']
    polys=geom['coordinates'] if geom['type']=='MultiPolygon' else [geom['coordinates']]
    tol=PROV_TOL.get(name,TOL)
    cand=[]
    for poly in polys:
        pr=[lcc(x,y) for x,y in poly[0]]
        cand.append((ring_area(pr),pr))
    cand.sort(key=lambda t:-t[0])
    rings=[]
    for i,(a,pr) in enumerate(cand[:MAX_RINGS]):
        if i>0 and a<MIN_AREA: continue      # always keep each province's largest ring
        sr=dp(pr,tol if i==0 else tol*1.6)
        if len(sr)>3: rings.append(sr)
    out[name]=rings

# emit RAW projected rings. the view box is fitted to the places in build_app.py,
# because Canada is mostly empty arctic and a full-extent sheet wastes 60% of the plate.
raw={n:[[[round(px,5),round(py,5)] for px,py in r] for r in rs] for n,rs in out.items()}
allpts=[pt for rs in out.values() for r in rs for pt in r]
xs=[p[0] for p in allpts]; ys=[p[1] for p in allpts]
print(f"rings={sum(len(r) for r in out.values())} pts={len(allpts)}")
print(f"full extent x[{min(xs):.4f},{max(xs):.4f}] y[{min(ys):.4f},{max(ys):.4f}]")
json.dump({"proj":"lcc_statcan","prov":raw}, open('data/canada_rings.json','w'), separators=(',',':'))
import os; print("rings bytes:",os.path.getsize('data/canada_rings.json'))
