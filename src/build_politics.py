import csv,json,re,unicodedata
# Elections Canada, 45th General Election (28 April 2025), official validated results,
# Table 12: votes by candidate by electoral district.
SRC='/tmp/t12.csv'
# Party positions on a single left-right axis. This is a judgement call, so it is
# stated openly and shown in the app rather than buried.
AXIS={'Liberal':-18,'Conservative':60,'NDP-New Democratic Party':-68,
      'Bloc Québécois':-8,'Green Party':-52,"People's Party":82}
PAT=[('Liberal',r'\bLiberal/'),('Conservative',r'\bConservative/'),
     ('NDP-New Democratic Party',r'\bNDP-New Democratic Party/'),
     ('Bloc Québécois',r'Bloc Qu'),('Green Party',r'Green Party/'),
     ("People's Party",r"People's Party")]
def rnorm(s):
    s=unicodedata.normalize('NFC',s)
    s=s.split('/')[0]                              # EC names are bilingual: 'Hamilton Centre/Hamilton-Centre'
    s=re.sub(r'[\u2010-\u2015\-]+','-',s)          # em/en dash and -- all collapse to one hyphen
    s=s.replace('\u2019',"'").replace('\u02bc',"'")
    return re.sub(r'\s+',' ',s).strip().lower()

def party(s):
    for name,p in PAT:
        if re.search(p,s): return name
    return None
rid={}
with open(SRC,encoding='utf-8-sig',errors='replace',newline='') as f:
    r=csv.reader(f); next(r)
    for row in r:
        if len(row)<8: continue
        ed=rnorm(row[1])
        ed_disp=row[1].split('/')[0].strip()
        pa=party(row[3])
        try: v=int(row[6].strip().replace(',',''))
        except: continue
        d=rid.setdefault(ed,{'total':0,'parties':{},'disp':ed_disp})
        d['total']+=v
        if pa: d['parties'][pa]=d['parties'].get(pa,0)+v
print("ridings parsed:",len(rid))
out={}
for ed,d in rid.items():
    if not d['total']: continue
    shares={p:round(v/d['total']*100,1) for p,v in d['parties'].items()}
    axis_votes=sum(d['parties'].get(p,0) for p in AXIS)
    if not axis_votes: continue
    lean=sum(AXIS[p]*d['parties'].get(p,0) for p in AXIS)/axis_votes
    win=max(d['parties'],key=d['parties'].get) if d['parties'] else None
    lab=('solid left' if lean<-40 else 'leans left' if lean<-12 else 'swing' if lean<12
         else 'leans right' if lean<40 else 'solid right')
    out[ed]={'disp':d['disp'],'lean':round(lean,1),'lean_label':lab,'winner':win,'shares':shares,
             'total_votes':d['total']}
pr=json.load(open('data/place_riding.json'))
res=[];miss=[]
for k,ed in pr.items():
    n,p=k.rsplit('|',1)
    e=out.get(rnorm(ed))
    if not e: miss.append(f"{n} ({ed})"); continue
    rec={'name':n,'prov':p,'riding':e.pop('disp',ed) if False else e['disp'],**{k2:v for k2,v in e.items() if k2!='disp'}}
    res.append(rec)
json.dump(res,open('data/politics.json','w'),indent=1,ensure_ascii=False)
json.dump({'axis':AXIS,'election':'45th Canadian General Election, 28 April 2025',
           'source':'Elections Canada official validated results, Table 12',
           'method':'vote-weighted mean of party axis positions, majors only'},
          open('research/politics-method.json','w'),indent=1,ensure_ascii=False)
print(f"places with politics: {len(res)}/129")
if miss: print("unmatched ridings:",miss[:6])
sm=sorted(res,key=lambda r:r['lean'])
print("\nmost left:")
for r in sm[:4]: print(f"  {r['name']:16s} {r['riding'][:26]:28s} {r['lean']:6.1f} {r['lean_label']:12s} {r['winner']}")
print("most right:")
for r in sm[-4:]: print(f"  {r['name']:16s} {r['riding'][:26]:28s} {r['lean']:6.1f} {r['lean_label']:12s} {r['winner']}")
