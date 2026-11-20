import sys,re,collections; sys.path.insert(0,'.')
from load import load
Q=load()
def scan(name,p,win=70,limit=40,ans_only=True):
    print('=====',name)
    n=0; per=collections.Counter()
    for q in Q:
        t=(q.get('ctx') or '')+' '+q['_core']+' ⟪'+q['opts'][q['a']]+'⟫ '+q['exp'] if ans_only else q['_full']
        for m in re.finditer(p,t):
            per[q['_d']]+=1
            if n<limit: print(f"  {q['_d']}:{q['id']} …{t[max(0,m.start()-win):m.end()+win]}…".replace('\n',' '))
            n+=1
            break
    print('  total',n,dict(per))
import sys
exec(open(sys.argv[1]).read())
