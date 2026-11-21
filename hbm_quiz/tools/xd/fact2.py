import sys,re,collections; sys.path.insert(0,'.')
from load import load
Q=load()
def tab(name,p,grp=1,where='sae',show=2):
    vals=collections.defaultdict(lambda: collections.defaultdict(list))
    for q in Q:
        parts={'s':(q.get('ctx') or '')+' '+q['_core'],'a':q['opts'][q['a']],'e':q['exp'],'o':' '.join(o for i,o in enumerate(q['opts']) if i!=q['a'])}
        t=' '.join(parts[c] for c in where)
        for m in re.finditer(p,t):
            v=next((g for g in m.groups() if g),m.group(0)) if m.groups() else m.group(0)
            vals[v][q['_d']].append(q['id'])
    print('=====',name)
    for v,d in sorted(vals.items(),key=lambda x:-sum(len(l) for l in x[1].values())):
        print(f'  {v!r}: '+'; '.join(f"{k}{len(l)}({','.join(l[:show])})" for k,l in d.items()))
exec(open(sys.argv[1]).read())
