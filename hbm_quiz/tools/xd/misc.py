import sys,re,collections,json; sys.path.insert(0,'.')
from load import load
Q=load()
V={
'TSV':r'TSV|via|Bosch|scallop|liner|seed|도금 충전|bottom-up|KOZ|keep-out|pinch|seam',
'BSP':r'reveal|리빌|back ?grind|연삭|carrier|캐리어|debond|glue|접착제|TTV|뒷면|backside|passivation|stress relief|edge trim|recess',
'BUMP':r'IMC|Kirkendall|pillar|solder|SnAg|Ni barrier|EM\b|전류 ?밀도|current crowding|wetting|젖음|reflow',
'SAW':r'dicing|절단|kerf|blade|stealth|plasma dicing|laser groov|chipping|singulat|개별화|DBG|seal ring',
'COW':r'TC-NCF|MR-MUF|NCF|NCP|HCB|hybrid|직접 접합|bond head|본딩 헤드|정렬|overlay|적층 공정|압착|TCB|gang|underfill|fillet|squeeze',
'WARP':r'[Ww]arpage|휨|Smile|Cry|Tg|유리전이|CTE|열팽창|moir|강성|중립면|수축|잔류 응력',
'THERM':r'열저항|방열|W/mm²|W/cm²|TIM|접합부 온도|열유속|냉각|cold plate|열전도|lid|Lid|열점|hot ?spot',
'SIP':r'interposer|인터포저|CoWoS|EMIB|RDL|bridge|브리지|substrate|기판|BGA|SoC|PDN|신호 무결|SI\b|C4',
'FA':r'LIT|OBIRCH|EOTPR|TDR|X-ray|SAT|단면|FIB|SEM|TEM|HTOL|HTS|THB|HAST|JESD|신뢰성 시험|고장 ?분석|Weibull|가속',
'PROD':r'JEDEC|HBM3E|HBM4|HBM3\b|세대|패키지 높이|720|775|용량|GB\b|base die|로직 공정|custom',
'DRAM':r'refresh|리프레시|retention|sense amp|채널|pseudo|bank|tRCD|row hammer|ECC|셀|wordline|bitline|대역폭|Gb/s',
'MET':r'계측|측정 장비|AOI|SPC|Cpk|GR&R|gauge|수율|KGD|probe|프로브|테스터|검사|overlay 계측|coplanarity',
'FEOL':r'포토|노광|lithograph|ALD|CVD|PVD|식각|etch|CMP|BEOL|low-k|트랜지스터|게이트|HKMG|EUV|배선 재료',
}
res=[]
for q in Q:
    t=q['_core']+' '+' '.join(q['opts'])+' '+q.get('title','')
    sc={d:len(re.findall(p,t)) for d,p in V.items()}
    own=q['_d']
    if own=='MIX': continue
    best=max(sc,key=sc.get)
    if best!=own and sc[best]>=3 and sc[own]==0:
        res.append((own,q['id'],best,sc[best],q['_core'][:110]))
c=collections.Counter((r[0],r[2]) for r in res)
print(len(res)); print(c.most_common())
for r in res: print(*r)
