import re,json,urllib.request,base64,os
UA="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36"
def get(u,binary=False):
    r=urllib.request.urlopen(urllib.request.Request(u,headers={"User-Agent":UA}),timeout=60)
    return r.read() if binary else r.read().decode()
FAMS=[("League Gothic","League+Gothic",[400]),
      ("IBM Plex Sans","IBM+Plex+Sans",[400,500,600]),
      ("IBM Plex Mono","IBM+Plex+Mono",[400,500])]
out={};total=0
for disp,slug,wts in FAMS:
    css=get(f"https://fonts.googleapis.com/css2?family={slug}:wght@{';'.join(map(str,wts))}&display=swap")
    # split into @font-face blocks, keep only the 'latin' subset (covers French accents via Latin-1)
    blocks=re.split(r'/\*\s*([a-z\-]+)\s*\*/',css)
    for i in range(1,len(blocks)-1,2):
        subset,body=blocks[i],blocks[i+1]
        if subset!='latin': continue
        m=re.search(r'font-weight:\s*(\d+)',body); u=re.search(r'url\((https://[^)]+\.woff2)\)',body)
        ur=re.search(r'unicode-range:\s*([^;]+);',body)
        if not(m and u): continue
        w=int(m.group(1))
        if w not in wts: continue
        data=get(u.group(1),binary=True); total+=len(data)
        out[f"{disp}|{w}"]={"b64":base64.b64encode(data).decode(),"bytes":len(data),
                            "range":ur.group(1).strip() if ur else None}
        print(f"{disp:16s} {w}  {len(data):6d}B  latin")
json.dump(out,open('fonts/faces.json','w'))
print(f"\ntotal woff2: {total/1024:.1f}KB  -> base64 ~{total*1.34/1024:.1f}KB")
