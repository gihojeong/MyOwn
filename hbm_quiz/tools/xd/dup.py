import sys; sys.path.insert(0,'.')
from load import load
import re, collections, json
Q=load()
def norm(s):
    s=(s or '').lower(); s=re.sub(r'\d+(\.\d+)?','0',s); return re.sub(r'[\s\W_]+','',s)
def grams(t,n=4): return {t[i:i+n] for i in range(len(t)-n+1)}
G=[]
for q in Q:
    t=norm(q['_core'])+'|'+'|'.join(sorted(norm(o) for o in q['opts']))
    G.append(grams(t))
df=collections.Counter(g for s in G for g in s)
N=len(Q)
idx=collections.defaultdict(list)
for i,s in enumerate(G):
    for g in s:
        if df[g]<=60: idx[g].append(i)
res=[]
for i,s in enumerate(G):
    c=collections.Counter()
    for g in s:
        if df[g]<=60:
            for j in idx[g]:
                if j>i and Q[j]['_d']!=Q[i]['_d']: c[j]+=1
    for j,k in c.items():
        if k<8: continue
        jac=len(s&G[j])/len(s|G[j])
        if jac>=float(sys.argv[1]): res.append((jac,Q[i]['id'],Q[j]['id']))
res.sort(reverse=True)
json.dump(res,open('xdup.json','w'))
print(len(res))
for r in res: print(f'{r[0]:.2f} {r[1]} {r[2]}')
