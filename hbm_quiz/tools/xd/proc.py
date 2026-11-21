import sys,re,collections,json; sys.path.insert(0,'.')
from load import load
Q=load()
R={
 'P1_TCB_as_process': r'TCB\s?(?:와|과|vs|대비|,)\s?(?:Advanced )?MR-MUF|MR-MUF\s?(?:와|과|vs|대비|,)\s?TCB|TCB\s?(?:와|과|vs|대비)\s?(?:[Hh]ybrid|HCB|하이브리드)|TCB\s?(?:방식|공법)|TCB MR-MUF|TCB 적층',
 'P2_hybrid_noncanon': r'[Hh]ybrid [Bb]onding|하이브리드\s?(?:본딩|접합)|Hybrid Copper Bonding',
 'P3_hcb_fullname_only': r'hybrid copper bonding',
 'P4_MUF_alone_or_massreflow': r'(?<![-\w])MUF\b|[Mm]ass [Rr]eflow',
 'P5_microbump_variants': r'[Mm]icro[- ]?[Bb]ump|마이크로\s?범프|[µμ]-?[Bb]ump|u-?bump',
}
out=collections.defaultdict(list)
for q in Q:
    t=q['_full']
    for k,p in R.items():
        ms=re.findall(p,t)
        if not ms: continue
        if k=='P3_hcb_fullname_only' and 'HCB' in t: continue
        out[k].append((q['_d'],q['id'],sorted(set(ms))))
for k,v in out.items():
    print('==',k,len(v),dict(collections.Counter(x[0] for x in v)))
    for x in v[:400]: print('  ',x[0],x[1],x[2])
json.dump(out,open('proc.json','w'),ensure_ascii=False)
