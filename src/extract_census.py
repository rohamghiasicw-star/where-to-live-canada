import csv,json,re,unicodedata
SRC='/tmp/g5/98-401-X2021005_English_CSV_data.csv'
CH={'1':'pop','6':'density','7':'area_km2','243':'median_hh_income','1488':'dwell_median',
    '1489':'dwell_avg','1494':'rent_median','2230':'unemployment'}
PROV={'10':'NL','11':'PE','12':'NS','13':'NB','24':'QC','35':'ON','46':'MB','47':'SK',
      '48':'AB','59':'BC','60':'YT','61':'NT','62':'NU'}
def norm(s):
    s=unicodedata.normalize('NFKD',s).encode('ascii','ignore').decode().lower()
    s=re.sub(r'\s*\(.*?\)\s*',' ',s)
    s=re.sub(r'[^a-z0-9]+',' ',s)
    return re.sub(r'\s+',' ',s).strip()
rows={}
with open(SRC,newline='',encoding='cp1252',errors='replace') as f:
    r=csv.reader(f); next(r)
    for row in r:
        cid=row[8]
        if cid not in CH: continue
        if 'subdivision' not in row[3].lower(): continue
        code=row[2]; prov=PROV.get(str(code)[:2])
        if not prov: continue
        val=row[11]
        try: val=float(val)
        except: val=None
        k=(code,prov)
        rows.setdefault(k,{'geo':row[4],'code':code,'prov':prov})[CH[cid]]=val
print("CSDs parsed:",len(rows))
# index by normalized bare name, per province
idx={}
for k,v in rows.items():
    base=norm(re.split(r',',v['geo'])[0])
    idx.setdefault((base,v['prov']),[]).append(v)
json.dump({f"{k[0]}|{k[1]}":v for k,v in idx.items()},open('data/_census_index.json','w'))
print("unique name|prov keys:",len(idx))
for probe in [('goderich','ON'),('halifax','NS'),('kitchener','ON'),('quebec','QC'),('dawson','YT')]:
    hits=idx.get(probe,[])
    for h in hits[:2]:
        print(f"  {probe} -> {h['geo']:44s} pop={h.get('pop')} inc={h.get('median_hh_income')} dwell={h.get('dwell_avg')}")
