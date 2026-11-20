import sys,re,collections,json; sys.path.insert(0,'.')
from load import load
Q=load()
NRE=r'(\d+)\s?단(?!계|위|면|열|차|자|순|독|점|일|어|락|속|가|품|층)|(\d+)-Hi'
GRE=r'(?:간극|접합층|접합 ?계면|bond ?층|본딩층|bondline|접합부 층)\s?(?:은|는|이|가|수는|수가|의 수는|수)?\s?(?:총\s?)?(\d+)\s?(?:개|층|곳)|(\d+)\s?개의\s?(?:간극|접합층|접합 계면|계면)'
out=[]
fewer=re.compile(r'하나 적|1개 적|한 개 적|n\s?[-−–]\s?1|N\s?[-−–]\s?1|die 수보다 하나|장수보다 하나')
for q in Q:
    txt={'S':(q.get('ctx') or '')+' '+q['_core'],'A':q['opts'][q['a']],'E':q['exp']}
    full=' '.join(txt.values())
    Ns=[int(a or b) for a,b in re.findall(NRE,txt['S'])]
    flags=[]
    for part,t in txt.items():
        for m in re.finditer(GRE,t):
            g=int(m.group(1) or m.group(2))
            if Ns and g==Ns[0]-1: flags.append(f'{part}:gap{g}=N{Ns[0]}-1 «{t[max(0,m.start()-40):m.end()+10]}»')
        for m in fewer.finditer(t):
            flags.append(f'{part}:FEWER «{t[max(0,m.start()-60):m.end()+30]}»')
    # figure checks
    f=q.get('fig') or ['',{}]
    if Ns and f[0]=='f_therm' and isinstance(f[1],dict) and 'n' in f[1]:
        if f[1]['n']!=Ns[0]+1: flags.append(f"FIG f_therm n={f[1]['n']} vs {Ns[0]}단 (should {Ns[0]+1})")
    if Ns and f[0]=='f_stack' and isinstance(f[1],dict) and 'n' in f[1]:
        if f[1]['n']!=Ns[0] and f[1]['n']!=Ns[0]: flags.append(f"FIG f_stack n={f[1]['n']} vs {Ns[0]}단")
    if flags: out.append((q['_d'],q['id'],Ns[:3],flags))
c=collections.Counter(o[0] for o in out); print(c, len(out))
for o in out: print(o[0],o[1],o[2]); [print('   ',x[:260]) for x in o[3]]
