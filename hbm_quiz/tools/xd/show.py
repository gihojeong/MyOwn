import sys,json; sys.path.insert(0,'.')
from load import load
Q={q['id']+'@'+q['_d']:q for q in load()}
byid={}
for k,q in Q.items(): byid.setdefault(q['id'],[]).append(q)
def sh(i,full=False):
    for q in byid.get(i,[]):
        print(f"  [{q['_d']}] {q['id']} lv={q['lv']} k={q['k']} fig={(q.get('fig') or [''])[0]} T:{q.get('title','')}")
        if q.get('ctx') and full: print('    C:',q['ctx'][:250])
        print('    S:',q['_core'][:420 if full else 260])
        print('    O:',' / '.join(('*' if n==q['a'] else '')+o[:70] for n,o in enumerate(q['opts'])))
        if full: print('    E:',q['exp'][:400])
if __name__=='__main__':
    full='-f' in sys.argv
    for a in sys.argv[1:]:
        if a!='-f': sh(a,full)
