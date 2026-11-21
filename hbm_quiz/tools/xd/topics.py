import sys,re,collections,json; sys.path.insert(0,'.')
from load import load
Q=load()
T={
'스택높이·die/간극수 계산':r'(높이|두께 예산|간극 수|간극은|간극 \d+ ?개).{0,200}(단|Hi)|(\d+단|\d+-Hi).{0,200}(높이|간극)',
'대역폭 GB/s 계산':r'GB/s|TB/s',
'용량 GB 계산':r'\d+ ?Gb.{0,80}(GB|용량)|용량.{0,40}GB',
'JEDEC 시험 규격 ID':r'JESD22|J-STD-020|JESD47',
'ESD/정전기':r'ESD|정전기|HBM 모델|CDM',
'Shadow moiré/형상측정':r'[Mm]oir|모아레',
'언더필/MUF 충전 미세피치':r'언더필|[Uu]nderfill|미충전|[Uu]nfilled',
'EM/전류밀도':r'EM\b|전류 ?밀도|일렉트로마이그레이션|[Ee]lectromigration',
'thermal TSV/더미 bump 방열':r'(TSV|관통 배선|dummy|더미).{0,40}(열|방열)',
'refresh-온도':r'(리프레시|[Rr]efresh).{0,60}(온도|°C)|(온도|°C).{0,60}(리프레시|[Rr]efresh)',
'KGD/절단 전 검사':r'KGD|양품.{0,20}(골라|선별)|절단 전.{0,20}검사|wafer 상태.{0,20}검사',
'HCB CMP/dishing/recess':r'(HCB|[Hh]ybrid|직접 접합|하이브리드).{0,120}(CMP|연마|[Dd]ishing|리세스|recess)',
'MR-MUF vs TC-NCF 비교':r'MR-MUF.{0,200}TC-NCF|TC-NCF.{0,200}MR-MUF',
'몰드 연삭/stress relief':r'(연삭|[Gg]rinding).{0,80}(수지|EMC|몰드|[Mm]old|[Ss]tress [Rr]elief|손상층)',
'dicing 방식 판정':r'[Ss]tealth|[Pp]lasma dicing|[Bb]lade dicing|[Ll]aser [Gg]rooving',
'수율 곱 계산':r'수율.{0,80}(\^|제곱|곱)|\d\.\d+ ?\^|\d\.\d+¹',
'FA 기법(LIT/OBIRCH/SAT/X-ray)':r'LIT|OBIRCH|Lock-in|SAT\b|SAM\b|초음파|X-ray|CT\b|EOTPR|TDR',
'IMC/Kirkendall':r'IMC|Kirkendall|커켄달|반응층',
'Smile/Cry 명명':r'[Ss]mile|\bCry\b',
'Tg/유리전이':r'Tg\b|유리전이',
}
cnt={k:collections.Counter() for k in T}; ids={k:collections.defaultdict(list) for k in T}
for q in Q:
    t=' '.join([q['_core'],' '.join(q['opts'])])
    for k,p in T.items():
        if re.search(p,t): cnt[k][q['_d']]+=1; ids[k][q['_d']].append(q['id'])
for k in T: print(f'{k:28s}', dict(cnt[k].most_common()))
json.dump(ids,open('topics.json','w'),ensure_ascii=False)
