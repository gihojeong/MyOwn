import re
def ctx(name,p,win=90,lim=30):
    print('=====',name); n=0
    for q in Q:
        t=(q.get('ctx') or '')+' '+q['_core']+' ⟪'+q['opts'][q['a']]+'⟫ '+q['exp']
        m=re.search(p,t)
        if m:
            n+=1
            if n<=lim: print(f"  {q['_d']}:{q['id']} …{t[max(0,m.start()-win):m.end()+win]}…")
    print('  total',n)
ctx('J-STD-020/A113',r'J-STD-020|JESD22-A113|J-STD-033')
ctx('MR-MUF 압력/하중',r'MR-MUF[^.]{0,80}(압력|하중|가압|압착)|(압력|하중|가압|압착)[^.]{0,40}MR-MUF')
ctx('MR-MUF vs NCF 열',r'(MR-MUF|MUF)[^.]{0,120}(방열|열전도|열 ?저항|열 측면)|(방열|열전도)[^.]{0,80}MR-MUF')
