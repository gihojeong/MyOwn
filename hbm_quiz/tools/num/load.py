import json,glob,re,sys,collections
sys.path.insert(0,'/home/user/MyOwn/hbm_quiz/tools')
import validate as V
ROOT='/home/user/MyOwn/hbm_quiz/'
meta=json.load(open(ROOT+'data/_meta.json'))
JOIN=meta.get('join',' ')
ALL=[]
for f in sorted(glob.glob(ROOT+'data/[0-9]*.json')):
    d=json.load(open(f))
    for q in d['questions']:
        ALL.append((d['code'],q))
def text(q):
    if q.get('stem') is not None: return q['stem']
    return (q.get('ctx') or '')+' '+(q.get('qt') or '')
NUMOPT=re.compile(r"^[\s약~≈]*[-+]?[\d,]*\.?\d")
def is_calc(q):
    core=text(q)
    return bool(V.CALC_Q.search(core)) or all(NUMOPT.match(o) for o in q['opts'])
def allnum(q): return all(NUMOPT.match(o) for o in q['opts'])
def fam(q): return V.fam_key(V.core_of(q))
UNITNUM=re.compile(r"\d\s*(µm|nm|mm|°C|%|W|mΩ|Ω|kA|mA|A\b|h\b|시간|개|장|단|배|GB|Gb|TB|ppm|cycle|MPa|GPa|ns|ps|mV|V\b|K\b)")
def numopts(q): return sum(bool(UNITNUM.search(o)) for o in q['opts'])
def is_calc2(q): return is_calc(q) or numopts(q)>=3
PREFIXES=["현장에서 다음 조건으로 작업이 진행되고 있습니다.","다음 조건으로 설계안을 검토하고 있습니다.","양산 라인에서 확인된 조건은 다음과 같습니다.","분석 의뢰서에 적힌 조건은 다음과 같습니다.","기술 검토 자료에 다음 수치가 적혀 있습니다.","품질 회의 자료에 다음 조건이 정리되어 있습니다.","설계 검토 회의에서 다음 조건이 제시되었습니다.","제품 기획 자료의 조건은 다음과 같습니다.","공정 변경 심의에 올라온 조건은 다음과 같습니다.","고객 사양 검토 중 다음 조건이 확인되었습니다."]
def strip(t):
    t=t.strip()
    for p in PREFIXES:
        if t.startswith(p): t=t[len(p):].strip()
    return t
def sig(q):
    t=strip(text(q)); t=re.sub(r"[\d.,]+","#",t)
    return t[:70]
def qsent(q):
    t=text(q).strip()
    parts=re.split(r"(?<=[.?])\s+",t)
    qs=[p for p in parts if '?' in p]
    return qs[-1] if qs else parts[-1]
def is_calc3(q):
    return bool(V.CALC_Q.search(qsent(q))) or allnum(q) or numopts(q)>=3
