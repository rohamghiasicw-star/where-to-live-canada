import json,urllib.request,urllib.parse,time,sys
PROVN={"BC":"British Columbia","AB":"Alberta","SK":"Saskatchewan","MB":"Manitoba","ON":"Ontario",
"QC":"Quebec","NB":"New Brunswick","NS":"Nova Scotia","PE":"Prince Edward Island",
"NL":"Newfoundland and Labrador","YT":"Yukon","NT":"Northwest Territories","NU":"Nunavut"}
ALIAS={"Kitchener-Waterloo":"Kitchener","Picton":"Picton, Prince Edward County","Elora":"Elora, Centre Wellington",
"Salt Spring Island":"Salt Spring Island","Courtenay":"Courtenay","Quebec City":"Quebec City",
"Dawson City":"Dawson City","Gaspe":"Gaspé","Trois-Rivieres":"Trois-Rivières","Val-d'Or":"Val-d'Or",
"Sept-Iles":"Sept-Îles","Montreal":"Montreal","Saint-Sauveur":"Saint-Sauveur, Laurentides"}
places=json.load(open('data/places.json'))
out=[]
for i,pl in enumerate(places):
    q=ALIAS.get(pl['name'],pl['name'])
    url="https://nominatim.openstreetmap.org/search?"+urllib.parse.urlencode({
        "q":f"{q}, {PROVN[pl['prov']]}, Canada","format":"json","limit":1,"addressdetails":0})
    req=urllib.request.Request(url,headers={"User-Agent":"livable-canada-research/1.0 (contact: rohamghiasicw@gmail.com)"})
    try:
        r=json.load(urllib.request.urlopen(req,timeout=30))
        if r:
            out.append({**pl,"lat":float(r[0]['lat']),"lon":float(r[0]['lon']),"osm_display":r[0].get('display_name')})
            print(f"{i+1}/129 OK  {pl['name']:24s} {float(r[0]['lat']):.4f},{float(r[0]['lon']):.4f}",flush=True)
        else:
            out.append({**pl,"lat":None,"lon":None}); print(f"{i+1}/129 MISS {pl['name']}",flush=True)
    except Exception as e:
        out.append({**pl,"lat":None,"lon":None}); print(f"{i+1}/129 ERR  {pl['name']} {e}",flush=True)
    time.sleep(1.1)
json.dump(out,open('data/coords.json','w'),indent=1)
print("done. missing:",sum(1 for o in out if o['lat'] is None))
