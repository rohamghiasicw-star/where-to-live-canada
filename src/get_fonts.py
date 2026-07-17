"""Type system: Radio Canada + Radio Canada Big.
Coppers and Brasses (Montreal), commissioned for CBC/Radio-Canada. OFL 1.1.
Chosen for fit, not novelty: a Canadian reference tool set in Canada's public
broadcaster's own face. Both cuts ship real `tnum` (the previous stack shipped
none, so font-variant-numeric was a no-op). The wdth axis lets type carry data.
No monospace: the 1985 MLS book was proportional grotesque, and the inheritance
from that tradition is tabular figures, not typewriter cosplay."""
import re,json,urllib.request,base64,io,os
from fontTools.ttLib import TTFont
UA="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/120 Safari/537.36"
def get(u,b=False):
    r=urllib.request.urlopen(urllib.request.Request(u,headers={"User-Agent":UA}),timeout=60)
    return r.read() if b else r.read().decode()
FAMS=[("Radio Canada","Radio+Canada:wdth,wght@75..100,300..700","300 700","75% 100%"),
      ("Radio Canada Big","Radio+Canada+Big:wght@400..700","400 700",None)]
SUBSETS={"latin","latin-ext"}          # latin-ext carries the French accents Quebec needs
out=[];total=0
for fam,spec,wspec,stretch in FAMS:
    css=get(f"https://fonts.googleapis.com/css2?family={spec}&display=swap")
    blocks=re.split(r'/\*\s*([a-z\-]+)\s*\*/',css)
    for i in range(1,len(blocks)-1,2):
        sub,body=blocks[i],blocks[i+1]
        if sub not in SUBSETS: continue
        m=re.search(r'url\((https://[^)]+\.woff2)\)',body)
        ur=re.search(r'unicode-range:\s*([^;]+);',body)
        if not m: continue
        data=get(m.group(1),True); total+=len(data)
        f=TTFont(io.BytesIO(data))
        feats=set()
        for t in ('GSUB','GPOS'):
            if t in f:
                for fr in f[t].table.FeatureList.FeatureRecord: feats.add(fr.FeatureTag)
        # digits live in the latin subset; latin-ext carries accents only, so only
        # latin needs to prove it has tabular figures
        if sub=='latin':
            assert 'tnum' in feats, f"{fam} {sub} has no tabular numerals"
        out.append({"family":fam,"sub":sub,"w":wspec,"stretch":stretch,
                    "b64":base64.b64encode(data).decode(),"range":ur.group(1).strip() if ur else None,
                    "bytes":len(data)})
        print(f"{fam:18s} {sub:10s} {len(data):6d}B  tnum={'yes' if 'tnum' in feats else 'n/a (no digits)'}")
css=[]
for f in out:
    css.append(f"@font-face{{font-family:'{f['family']}';font-style:normal;"
               f"font-weight:{f['w']};" + (f"font-stretch:{f['stretch']};" if f['stretch'] else "") +
               f"font-display:swap;src:url(data:font/woff2;base64,{f['b64']}) format('woff2');" +
               (f"unicode-range:{f['range']};" if f['range'] else "") + "}")
open('fonts/faces.css','w').write("".join(css))
print(f"\nwoff2 {total/1024:.1f}KB -> css {os.path.getsize('fonts/faces.css')/1024:.1f}KB")
