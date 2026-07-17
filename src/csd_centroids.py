"""Exact coordinates for every census subdivision, keyed by CSDUID.
Beats geocoding by name: no rate limit, no fuzzy match, and no chance of
resolving Kenora to Kenora District. The boundary file is NAD83 Statistics
Canada Lambert (EPSG:3347), the same projection the map is drawn in."""
import json,math,shapefile,pyproj
# StatCan ships this dbf as cp1252, like the census CSV. 'Cap-Pele' is Cap-Pele.
R=shapefile.Reader('/tmp/csdb/lcsd000b21a_e',encoding='cp1252')
inv=pyproj.Transformer.from_crs('EPSG:3347','EPSG:4326',always_xy=True)
def ring_centroid(pts):
    a=cx=cy=0.0
    for i in range(len(pts)-1):
        x0,y0=pts[i]; x1,y1=pts[i+1]
        cr=x0*y1-x1*y0; a+=cr; cx+=(x0+x1)*cr; cy+=(y0+y1)*cr
    if abs(a)<1e-9:
        xs=[p[0] for p in pts]; ys=[p[1] for p in pts]
        return sum(xs)/len(xs), sum(ys)/len(ys), 0.0
    a*=0.5
    return cx/(6*a), cy/(6*a), abs(a)
out={}
for sr in R.iterShapeRecords():
    s,rec=sr.shape,sr.record
    if not s.points: continue
    parts=list(s.parts)+[len(s.points)]
    best=None
    for i in range(len(parts)-1):
        ring=s.points[parts[i]:parts[i+1]]
        if len(ring)<4: continue
        x,y,a=ring_centroid(ring)
        if best is None or a>best[2]: best=(x,y,a)
    if not best: continue
    lon,lat=inv.transform(best[0],best[1])
    out[rec['CSDUID']]={'lat':round(lat,5),'lon':round(lon,5),
        'name':rec['CSDNAME'],'type':rec['CSDTYPE'],'land_km2':rec['LANDAREA']}
json.dump(out,open('data/csd_coords.json','w'))
print("centroids:",len(out))
# validate against the 129 coords we already trust (Nominatim, hand-audited)
cur=json.load(open('data/coords.json'))
cen={r['name']+'|'+r['prov']:r for r in json.load(open('data/census.json'))}
idx=json.load(open('data/_census_index.json'))
def hav(a,b,c,d):
    Rk=6371;p=math.radians
    x=math.sin(p(d-b)/2)**2+math.cos(p(b))*math.cos(p(d))*math.sin(p(c-a)/2)**2
    return 2*Rk*math.asin(math.sqrt(x))
# find each known place's CSDUID via its geo string
geo2uid={v['name']:k for k,v in out.items()}
d=[]
for p in cur:
    c=cen.get(p['name']+'|'+p['prov'])
    if not c: continue
    base=c['csd'].split(',')[0]
    uid=geo2uid.get(base)
    if not uid: continue
    o=out[uid]
    d.append((hav(p['lon'],p['lat'],o['lon'],o['lat']),p['name']))
d.sort()
import statistics as st
print(f"\nagreement with our 129 audited coords ({len(d)} matched):")
print(f"  median {st.median([x[0] for x in d]):.1f}km   p90 {d[int(len(d)*.9)][0]:.1f}km")
print("  worst (big or oddly-shaped municipalities, expected):")
for km,n in d[-5:]: print(f"     {n:20s} {km:6.1f}km")
