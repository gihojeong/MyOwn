import sys,re,json,collections; sys.path.insert(0,'.')
from load import load
Q=load()
res=[]
for q in Q:
    full=(q.get('ctx') or '')+' '+q['_core']+' '+q['opts'][q['a']]+' '+q['exp']
    Ns=[int(a or b) for a,b in re.findall(r'(\d+)\s?단(?!계)|(\d+)-Hi',q['_core']+(q.get('ctx') or ''))]
    f=q.get('fig') or ['',{}]
    why=[]
    for m in re.finditer(r'하나 적은 (\d+)\s?개|간극 (\d+)\s?(?:곳|개)',full):
        g=int(m.group(1) or m.group(2))
        if Ns and g==Ns[0]-1: why.append(f'text gap {g} for {Ns[0]}단')
    if Ns and f[0]=='f_therm' and f[1].get('n')==Ns[0]: why.append(f'f_therm n={Ns[0]} (base 누락)')
    if not Ns and f[0]=='f_therm' and q['k']==1 and re.search(r'die (\d+)\s?장',full): pass
    if why: res.append((q['_d'],q['id'],q['lv'],Ns[0],'; '.join(why)))
print(collections.Counter(r[0] for r in res), len(res))
for r in res: print(*r)
json.dump(res,open('ngap_viol.json','w'),ensure_ascii=False)
