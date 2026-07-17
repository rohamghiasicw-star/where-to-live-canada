"""Deterministic synthesis of salvaged resident research. No model calls:
the claims and quotes were already written and sourced by the research agents,
this only organises them and refuses to invent anything they did not say."""
import json,re
from urllib.parse import urlparse
raw=json.load(open('data/lived_raw.json'))
SENT={'positive':1.0,'negative':-1.0,'mixed':0.0,'neutral':0.0}
def host(u):
    try: return urlparse(u).hostname.replace('www.','')
    except Exception: return None
out=[];rowsum=[]
for name,d in raw.items():
    F=[f for f in d['findings'] if f.get('claim') and f.get('source_url')]
    if not F: continue
    # topic sentiment: mean of labelled sentiment, scaled to -2..+2, needs >=2 data points
    bytopic={}
    for f in F: bytopic.setdefault(f.get('topic') or 'other',[]).append(SENT.get(f.get('sentiment'),0.0))
    ts={t:round(sum(v)/len(v)*2,2) for t,v in bytopic.items() if len(v)>=2}
    keep=['weather','cost','housing','jobs','healthcare','transit','community','culture','outdoors','safety','isolation']
    ts={k:ts.get(k) for k in keep}
    pos=[f for f in F if f.get('sentiment')=='positive']
    neg=[f for f in F if f.get('sentiment')=='negative']
    # spread across topics so we don't get four claims about rent
    def pick(lst,n):
        seen=set(); res=[]
        for f in sorted(lst,key=lambda f:-len(f.get('quote') or '')):
            t=f.get('topic')
            if t in seen: continue
            seen.add(t); res.append(f['claim'])
            if len(res)>=n: break
        for f in lst:
            if len(res)>=n: break
            if f['claim'] not in res: res.append(f['claim'])
        return res[:n]
    loved=pick(pos,4); hated=pick(neg,4)
    # quotes: verbatim only, one per source, longest first, negatives first (they get sanitised away otherwise)
    qs=[];seen=set()
    for f in sorted(F,key=lambda f:(f.get('sentiment')!='negative',-len(f.get('quote') or ''))):
        q=(f.get('quote') or '').strip()
        if len(q)<40: continue
        h=host(f['source_url'])
        if not h or h in seen: continue
        seen.add(h); qs.append({'quote':q,'source_url':f['source_url'],'context':f.get('topic')})
        if len(qs)>=3: break
    worst=min(((v,k) for k,v in ts.items() if v is not None),default=(None,None))
    downside=None
    if neg:
        cand=[f for f in neg if f.get('topic')==worst[1]] or neg
        downside=max(cand,key=lambda f:len(f['claim']))['claim']
    confs=[c for _,c,_ in d['lenses'] if c]
    conf='high' if confs.count('high')>=2 else 'low' if confs.count('low')>=2 else 'medium'
    out.append({'name':name,'loved':loved,'hated':hated,'honest_downside':downside,
                'quotes':qs,'topic_sentiment':ts,'confidence':conf,
                'evidence_count':len(F),'source_count':len(d['sources'])})
    rowsum.append((name,len(F),len(qs),conf))
json.dump(out,open('data/lived.json','w'),indent=1,ensure_ascii=False)
print(f"synthesised {len(out)} places")
print(f"  with >=1 verbatim quote: {sum(1 for r in out if r['quotes'])}")
print(f"  with an honest downside: {sum(1 for r in out if r['honest_downside'])}")
r=next(x for x in out if x['name']=='Tofino')
print("\n--- Tofino sample ---")
print(" downside:",r['honest_downside'][:150])
print(" quote:   ",r['quotes'][0]['quote'][:130],"\n           ->",r['quotes'][0]['source_url'][:70])
print(" sentiment:",{k:v for k,v in r['topic_sentiment'].items() if v is not None})
