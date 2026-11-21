import sys, re, json, collections, itertools, os
sys.path.insert(0, os.path.dirname(__file__))
from load import load

Q = {q['id']: q for q in load()}
D = {i: q['_d'] for i, q in Q.items()}
L = json.load(open(os.path.join(os.path.dirname(__file__), 'lists.json')))
NG = json.load(open(os.path.join(os.path.dirname(__file__), 'ngap_viol.json')))
PROC = json.load(open(os.path.join(os.path.dirname(__file__), 'proc.json')))
OUT = '/home/user/MyOwn/hbm_quiz/docs/reviews/xd'
CODES = ['TSV', 'BSP', 'BUMP', 'SAW', 'COW', 'WARP', 'THERM', 'SIP', 'FA', 'PROD', 'DRAM', 'MET', 'MIX', 'FEOL']
NAMES = {'TSV': 'TSV 형성과 충전', 'BSP': 'Backside pad 형성', 'BUMP': 'Bump 와 계면 금속', 'SAW': 'Sawing 과 개별화',
         'COW': 'CoW 적층 접합', 'WARP': 'Warpage 와 기계적 응력', 'THERM': '열 설계와 방열', 'SIP': 'SiP 조립 구조',
         'FA': '고장분석과 신뢰성', 'PROD': 'HBM 제품과 구조', 'DRAM': 'DRAM 동작과 설계', 'MET': '검사 · 계측과 품질',
         'MIX': '복합 판단', 'FEOL': '전공정과 배선 재료'}


def rng(l):
    out = []
    for k, g in itertools.groupby(sorted(l), key=lambda x: x[:-4]):
        nums = sorted(int(x[-4:]) for x in g)
        s = p = nums[0]
        for n in nums[1:] + [None]:
            if n is not None and n == p + 1:
                p = n
                continue
            out.append(f'{k}{s:04d}' if s == p else f'{k}{s:04d}~{p:04d}')
            if n is not None:
                s = p = n
    return ', '.join(out)


def chk(*ids):
    for i in ids:
        assert i in Q, i


term = collections.defaultdict(list)   # code -> rows (id, sev, problem, instruction)
dup = collections.defaultdict(list)    # code -> rows (id, problem, instruction)
mv = collections.defaultdict(list)     # code -> rows (id, to, reason)
conf = collections.defaultdict(list)   # code -> rows (id, problem, instruction)
notes = collections.defaultdict(list)


def T(i, sev, prob, ins):
    chk(i); term[D[i]].append((i, sev, prob, ins))


# ───────────────────── 1. 용어 규약 ─────────────────────
# 1a. N단 ↔ 간극 수
for d, i, lv, n, why in NG:
    if d == 'THERM':
        pb = []
        if 'text gap' in why: pb.append(f'{n}단인데 간극을 {n-1}개로 계산(“간극은 die 수보다 하나 적은 {n-1}개”)')
        if 'f_therm' in why: pb.append(f'f_therm.n={n} (core 수를 넣음 → 그림이 base 를 빼고 간극 {n-1}개로 계산)')
        T(i, 'E', ' · '.join(pb),
          f'STANDARDS 2.5: {n}단 = core {n} + base 1, 간극 {n}. 최하단이 base 면 간극 {n}개로 재계산(정답·오답 값·해설 식 모두), f_therm.n={n+1}. 최하단 core 까지를 묻는 설정이면 지문에 “최상단 core 에서 최하단 core 까지 {n-1}개 간극” 이라고 명시')
    elif d == 'MET':
        T(i, 'E', '12단 스택 수율 계산에서 “접합 간극 11곳” (0.995¹¹)',
          '12단은 접합 계면 12곳(base–core1 포함). 0.98¹² × 0.995¹² ≈ 0.739 → 정답 보기를 “약 74 %” 로(현재 “약 72 %” 는 어느 계산과도 맞지 않음). 오답도 재설계. NUM 에 재확인 요청')
T('WARP-I-0002', 'E', '12단 열저항 문항에 f_therm.n=12 (base 포함 총 die 수여야 함)', 'f_therm.n=13 (core 12 + base 1)') if 'WARP-I-0002' not in [r[1] for r in NG] else None
notes['THERM'].append(f'**f_therm.n 일괄 점검(W)**: k=1 인데 지문에 단수가 없는 f_therm 문항 {len(L["tk"])}개는 그림이 기본 n(대개 12)을 “die 12장” 으로 그려 지문에 없는 단수를 보여 준다(E_K1_FIG_NUM 성격). 단수가 풀이에 필요 없으면 k=0 주제도로, 필요하면 지문에 “N단(core N + base 1)” 을 쓰고 n=N+1.')
notes['THERM'].append('**20단 설정**: THERM 의 20단 문항은 JEDEC HBM4 단수(4/8/12/16-Hi) 밖이다. 유지하려면 지문에 “가정” 임을 밝힌다(STANDARDS 2.2).')
notes['SIP'].append(f'**표현 권고(W, 수치는 규약과 일치)**: SIP 문항 {len(L["sh"])}개가 “접합 간극은 die 수보다 하나 적습니다” 라고 쓴다. die 수에 base 를 넣으면 값은 맞지만 THERM 의 오류(“12단 → 간극 11”)와 같은 문장이라 학습자가 혼동한다. 공유 ctx 를 “간극 수 = core die 수(N)” 로 바꿀 것. 대상: {rng(L["sh"])}')

# 1b. Smile / Cry
bd_wrong = ['WARP-I-0003', 'WARP-I-0005', 'WARP-I-0007', 'WARP-I-0008', 'WARP-I-0009', 'WARP-I-0010', 'WARP-I-0011',
            'WARP-I-0013', 'WARP-I-0021', 'WARP-I-0022', 'WARP-I-0024', 'WARP-I-0025']
for i in bd_wrong:
    f = Q[i]['fig'][1]
    shape = '중앙이 기준면에서 멂(∩)' if f['sign'] == 1 else '중앙이 기준면에 가까움(∪)'
    right = 'Cry' if f['sign'] == 1 else 'Smile'
    wrong = Q[i]['opts'][Q[i]['a']]
    T(i, 'E', f'bump 면 아래 + {shape} 를 “{wrong}” 로 정답 처리 — f_warp 현행 표(active 면 기준) 를 따른 것으로 STANDARDS 2.5 와 반대',
      f'2.5 기준 정답은 **{right}**. 정답 키·해설 교정. 이 24문항(WARP-I-0003~0026)은 한 가족이므로 3개 이하만 남기고(자세 2종 × 형상 2종 중 대표), 지문의 “그림은 … 기준면별 명명 규칙표” 문장 삭제(DA 표 교체 전 근거로 쓰지 말 것)')
bu_ok = ['WARP-I-0004', 'WARP-I-0006', 'WARP-I-0012', 'WARP-I-0014', 'WARP-I-0015', 'WARP-I-0016', 'WARP-I-0017',
         'WARP-I-0018', 'WARP-I-0019', 'WARP-I-0020', 'WARP-I-0023', 'WARP-I-0026']
T('WARP-I-0004', 'W', f'BEOL 면 위 자세 12문항({rng(bu_ok)})은 정답이 2.5 와 일치하나 f_warp 명명 규칙표를 풀이 근거로 지칭하고, 위 12문항과 같은 가족(24개)',
  '가족 3개 제한으로 삭제 우선 대상. 남기는 문항은 “명명 규칙표” 지칭 삭제, 이름이 “위에서 본 형상” 으로 정해진다는 해설로 교체')
T('WARP-I-0001', 'E', '“bump 면 아래 + 중앙이 기준면에서 멂 → Smile 로 기록” 을 전제로 뒤집은 뒤 “Cry” 를 정답 처리. 2.5 기준으로는 첫 기록이 Cry, 뒤집은 뒤(중앙이 기준면에 가까움 ∪)가 Smile',
  '지문 전제와 정답을 2.5 로 교정(첫 기록 Cry → 뒤집으면 Smile, “die 자체는 변하지 않았고 위에서 본 형상이 반대가 되었기 때문”). 해설 비어 있음 → 작성')
T('WARP-B-0001', 'E', '“두 사람이 본 형상 자체는 같았습니다” — 한 사람은 bump 면 아래, 다른 사람은 BEOL 면 위(뒤집힘)로 놓았으므로 위에서 본 형상은 반대(∩/∪)다. 지문이 자기모순',
  '“die 의 실제 휨은 같았지만 놓은 자세가 달라 위에서 본 형상이 반대였다” 로 수정. 해설의 “기준면에 대한 중앙의 상대 위치로 정의” → “측정 자세 그대로 위에서 본 형상(∩ Cry / ∪ Smile)” 으로')
T('WARP-A-0185', 'E', '“가운데가 볼록하게 휜(Cry) die” — 측정 자세 없이 이름을 붙임(2.5: 자세를 지문에 반드시 적음). 또 COW-I-0141·BUMP-A-0146 과 같은 내용',
  '교차 중복으로 삭제(COW-I-0141 보유). 유지 시 “bump 면을 아래로 두고 위에서 본 형상이 ∩(Cry)” 로 자세 명시')
T('BUMP-A-0150', 'E', '해설 첫 문장이 Smile/Cry 명명 설명(다른 문항 해설 혼입). 명명 내용 자체는 2.5 와 일치',
  '해당 문장 삭제(교차 중복 판정으로 문항 자체도 삭제 대상 — §2)')
T('BUMP-A-0146', 'W', '해설에 Smile/Cry 명명 설명이 들어 있음(2.5 와 일치). 문항 주제(하중 상향 결과)와 무관한 문장', '교차 중복으로 삭제(COW-I-0141 보유) — §2')
T('COW-I-0141', 'W', '해설의 명명(“bump 면 아래에서 중앙이 솟은 형상 = Cry”)은 **2.5 와 일치**. 문제는 f_warp 현행 표·WARP-I 가족과 반대라는 점(→ §4 사실 충돌 F1)',
  '명명은 유지. 해설에서 명명 설명은 1문장으로 줄이고 하중 상향 결과(가장자리 미접합↓·중앙 과압축↑)의 근거와 오답 3개 해설로 채울 것')
for i in L['tw']:
    pass
term['TSV'].append(('(f_warp 사용 54문항)', 'W', f'열팽창 차·응력 계산 문항이 f_warp 그림을 써서 Smile/Cry 명명표(현행 표는 2.5 와 반대)를 노출: {rng([x for x in L["tw"] if x.startswith("TSV")])}',
                    'f_plot(CTE·온도–변위) 또는 f_note 로 교체. 명명 판정 문항이 아니므로 f_warp 금지'))
T('SIP-I-0014', 'W', 'f_warp 그림 사용(명명표 노출)', '문항이 명명 판정이 아니면 f_sip/f_plot 으로 교체')

# 1c. 공법 명칭
p1 = {x[1]: x[2] for x in PROC['P1_TCB_as_process']}
p1note = {
    'BUMP-B-0061': ('“die를 하나씩 열과 압력으로 붙이는 방식” 의 정답이 “TCB”, 오답 “MR-MUF”·“Hybrid Bonding” — TCB 를 공법명으로 MR-MUF 와 대비', '정답을 “TC-NCF” 로(또는 발문을 “장비 방식” 으로 바꿔 TCB 유지). 보기 “Hybrid Bonding” → “HCB”. 이 문항은 COW 와 중복이라 삭제 우선(§2)'),
    'BUMP-B-0062': ('보기에 “TCB” 를 MR-MUF 의 대립 공법으로 사용, “Hybrid Bonding” 표기', '“TCB” → “TC-NCF”, “Hybrid Bonding” → “HCB”. COW 중복으로 삭제 우선(§2)'),
    'COW-B-0090': ('“TCB와 MR-MUF” — TCB 를 공법명으로 사용', '“TC-NCF와 MR-MUF” 로. TCB 는 “TC-NCF 의 열압착(TCB) 장비” 처럼 장비 문맥에서만'),
    'COW-I-0203': ('“TCB와 MR-MUF” 대비', '“TC-NCF와 MR-MUF” 로'),
    'COW-A-0184': ('“TCB와 MR-MUF” 대비', '“TC-NCF와 MR-MUF” 로'),
    'COW-I-0200': ('“TCB 방식” 을 공법명으로 사용', '문맥에 따라 “TC-NCF” 또는 “열압착(TCB) 장비”'),
    'COW-B-0053': ('“TCB 적층” 을 공법명으로 사용', '“TC-NCF 적층” 또는 “열압착(TCB) 적층” — NCF/NCP/MUF 중 무엇과 결합했는지 명시'),
    'SIP-I-0129': ('보기 “TCB 적층” 을 공법명으로 사용', '교차 중복으로 삭제(§2). 유지 시 “TC-NCF 적층”'),
    'PROD-B-0050': ('보기 “TCB 적층”', '“적층(TC-NCF/MR-MUF)” 처럼 공법 중립 표현으로'),
}
for i, (pb, ins) in p1note.items():
    T(i, 'E', pb, ins)
p2 = collections.defaultdict(list)
for d, i, ms in PROC['P2_hybrid_noncanon']:
    p2[d].append((i, ms))
for d, lst in p2.items():
    if d == 'COW':
        term['COW'].append((f'({len(lst)}문항)', 'E', f'HCB 를 “Hybrid Bonding / hybrid bonding / 하이브리드 본딩 / Hybrid Copper Bonding” 으로 혼용: {rng([x[0] for x in lst])}',
                            '공법명은 **HCB** 로 통일(첫 언급만 “HCB(Cu–Cu hybrid bonding)”). 같은 문항 안 영문/한글 혼용 금지(3.8). 보기에서 공법을 고르는 문항은 반드시 “HCB”'))
    else:
        for i, ms in lst:
            if i in p1note:
                continue
            T(i, 'E', f'HCB 비표준 표기 {", ".join(sorted(set(ms)))}', '“HCB” 로 통일(첫 언급 “HCB(Cu–Cu hybrid bonding)”)')
p3 = [x[1] for x in PROC['P3_hcb_fullname_only'] if x[1] not in {y[0] for y in p2['COW']}]
term['COW'].append((f'({len(p3)}문항)', 'W', f'약어 없이 “hybrid copper bonding” 만 반복(HCB 미사용): {rng(p3)}', '첫 언급 “HCB(hybrid copper bonding)”, 이후 “HCB”'))
T('COW-B-0108', 'W', '“MUF” 단독 표기', 'MR-MUF 를 뜻하면 “MR-MUF”, 일반 molded underfill 이면 “MUF(molded underfill)” 로 풀어 씀')
T('COW-B-0079', 'W', '“Mass Reflow” 를 공법명처럼 사용', '공법명은 “MR-MUF”, 접합 단계만 가리킬 때 “mass reflow(일괄 리플로)”')
T('BUMP-B-0029', 'E', '“범프 없이 금속끼리 직접 붙이는 방식” 정답 “Hybrid Bonding”, 오답 “Mass Reflow”', '정답 “HCB”, 오답 “MR-MUF”. COW 의 공법 명칭 문항과 중복이라 삭제 우선(§2)')
for d, i, ms in PROC['P5_microbump_variants']:
    T(i, 'W', f'µbump 표기 변형 {", ".join(sorted(set(ms)))}', '“µbump”(U+00B5, 하이픈 없음) 로 통일 — STANDARDS 2.4 표기')
T('BUMP-B-0080', 'E', '“하이브리드 본딩 적용 시 … 범프 피치” — HCB 에는 bump 가 없다(2.4). 표기도 비표준', '교차 중복으로 삭제(§2). 사실 충돌 F3 참조')
T('TSV-I-0194', 'E', 'Bosch 측벽 식각을 “Erosion” 이라 부름 — 이 문항집에서 Erosion 은 CMP 결함(TSV-B-0076) 용어', '“측면 식각(lateral etch)” 또는 “scallop 깊이” 로. FEOL-I-0013 동일(§4 F7)')
T('FEOL-I-0013', 'E', '측벽 보호 성분 증가 결과를 “Erosion 감소” 로 표기 — CMP 용어와 충돌', '교차 중복으로 삭제(TSV-I-0194 보유). 유지 시 “측면 식각 감소”')

# ───────────────────── 2. 교차 중복 ─────────────────────
G = [
    # (concept, owner_id, [(id, action)], note)
    ('HBM 구조 발전 방향 요약 (완전 동일 문항)', 'PROD-B-0061', [('SIP-I-0130', '삭제')], '5-gram 1.00 — 보기만 순서 다름'),
    ('경화 온도·수지 점도·filler 함량 높/낮 짝짓기 (보기 구조 동일)', 'WARP-B-0147', [('MIX-B-0017', '삭제')], 'W_NEAR_DUP_X 0.90. WARP-B-0146 과도 같은 틀 — WARP 안에서 1개로 통합'),
    ('미세 피치에서 solder 접합 공정 창이 좁아지는 인자', 'COW-A-0160', [('BUMP-A-0147', '삭제'), ('BUMP-A-0150', '삭제')], 'W_NEAR_DUP_X 0.83. TCB 공정 창은 COW 학습 목표'),
    ('공정 조건 불변인데 결과가 서서히 변함 → 마모·축적', 'MET-I-0119', [('MET-B-0058', 'MET 내 통합(삭제)'), ('MIX-I-0013', '삭제'), ('MIX-I-0009', '삭제')], 'W_NEAR_DUP_X 0.82. SPC 추세(drift) 는 MET 본연 주제 — 관리도 데이터로 재작성 권고'),
    ('NCF 필름 두께 편차 → 배출량 편차', 'BUMP-I-0134', [('BUMP-I-0134', 'mv → COW'), ('WARP-I-0275', '삭제')], '0.81. NCF 는 COW 학습 목표 — BUMP-I-0134 를 다듬어 COW 로'),
    ('적층 후 die 교체 불가 이유', 'PROD-B-0051', [('MET-B-0023', '삭제')], '0.76'),
    ('시험 온도를 실사용보다 높이는 이유 / 지나치게 높이면 안 되는 이유', 'FA-I-0064', [('WARP-I-0298', '삭제'), ('WARP-I-0299', '삭제(FA-I-0065 보유)')], '0.75 / 0.56 — 가속 시험은 FA'),
    ('고단 적층에서 구조·공정·시스템이 한 문제로 수렴', 'MIX-A-0051', [('DRAM-A-0074', '삭제'), ('PROD-A-0023', '삭제')], '0.74 — 일반론. MIX 도 사례형으로 재작성 못 하면 삭제'),
    ('낱개(개별화) 후 최종 검사를 다시 하는 이유', 'MET-B-0074', [('SAW-I-0044', '삭제')], '0.71'),
    ('wafer 단위 작업이 유지되는 마지막 공정', 'PROD-B-0050', [('SIP-I-0129', '삭제')], '0.68 — 정답 표기도 “wafer 검사” vs “전기검사” 로 다름. PROD 하나로'),
    ('접합층 두께 축소의 이유(높이·열)', 'PROD-I-0036', [('SIP-I-0131', '삭제'), ('WARP-B-0102', '삭제'), ('FA-I-0043', '삭제'), ('WARP-B-0081', 'THERM 보유(열 관점 1개)')], '0.66/0.58/0.52 — 높이 예산은 PROD, 열저항은 THERM 이 1개씩'),
    ('스택 구성 수(die·간극·pad 보유 die) 환산 가족', 'SIP-A-0003', [('SIP-A-0003', 'mv → PROD (대표 1개)'), ('SIP-A-0004', '삭제'), ('SIP-A-0005', '삭제'), ('SIP-A-0006', '삭제'), ('SIP-A-0007', '삭제'), ('SIP-A-0008', '삭제'), ('SIP-A-0009', '삭제'), ('SIP-A-0010', '삭제'), ('SIP-A-0011', '삭제'), ('SIP-A-0012', '삭제'), ('WARP-A-0002', '삭제')], '0.63 — 단수 구성은 PROD(제품 구조) 소관. 6/10/14/18/24단은 JEDEC 단수가 아님'),
    ('구조·공법 변경 시 검사 체계도 바꿔야 하는 이유(일반론)', 'COW-A-0078', [('SIP-B-0148', '삭제'), ('SIP-A-0160', '삭제'), ('MIX-B-0006', 'MIX 내 1개로 통합'), ('MIX-A-0049', 'MIX 내 1개로 통합'), ('MIX-A-0039', 'MIX 내 1개로 통합'), ('COW-I-0229', '삭제'), ('SAW-I-0041', '재작성(구체화) 또는 삭제')], '0.62/0.45 — COW-A-0078 만 구체 조건 보유. SAW 는 “stealth dicing 내부 균열은 외관 AOI 로 안 보임 → IR 검사” 처럼 구체화'),
    ('EM 자기 가속 되먹임을 끊는 접근', 'FA-A-0037', [('MIX-A-0001', '삭제'), ('MIX-A-0042', '삭제')], '0.62'),
    ('일괄(gang) 접합 방식의 과제', 'COW-I-0167', [('SIP-B-0094', '삭제')], '0.62'),
    ('인터포저 면적↑ → 수율↓', 'SIP-B-0150', [('SIP-B-0086', 'SIP 내 통합(삭제)'), ('MET-I-0105', '삭제')], '0.62/0.59 — 인터포저는 SIP'),
    ('ESD 손상 vs 통전(EM) 열화 감별', 'DRAM-A-0061', [('DRAM-A-0061', 'mv → FA (재작성)'), ('DRAM-I-0149', '삭제'), ('BUMP-A-0164', '삭제')], '0.61/0.43 — 고장 감별은 FA'),
    ('적층 단마다 정렬 마크 재인식', 'COW-B-0057', [('SIP-B-0091', '삭제')], '0.58'),
    ('dicing 방식 이름 고르기', 'SAW-B-0037', [('FEOL-B-0044', '삭제')], '0.58 — SAW 에 동형 50문항'),
    ('상온 warpage 규격 내인데 실장 불량 → 승온 궤적 / 상온 값 하나로 관리하는 한계', 'WARP-A-0190', [('SIP-A-0144', 'BGA·interposer 데이터(f_plot)로 재작성 또는 삭제'), ('PROD-A-0027', '삭제'), ('SIP-A-0148', '삭제(WARP-A-0191 승온/냉각 이력과 중복)')], '0.57/0.51'),
    ('조건 변경 후 관찰 기간이 필요한 이유', 'MET-A-0108', [('MIX-I-0065', '삭제')], '0.56'),
    ('절단 전 wafer 상태 검사의 이점(KGD)', 'MET', [('SAW-I-0006', 'SAW 1개만 보유(절단 손상 관점으로)'), ('SAW-I-0008', '삭제'), ('SAW-B-0060', '삭제'), ('PROD-B-0084', '삭제'), ('PROD-B-0090', '삭제')], '0.56/0.42/0.39 — KGD 시험 흐름은 MET 학습 목표. SAW 는 dicing 관점 1개'),
    ('새 접합 방식을 단계적으로 도입하는 이유', 'COW-A-0181', [('COW-I-0178', 'COW 내 통합(삭제)'), ('WARP-A-0217', '삭제')], '0.55/0.45 — THERM 파일에 있는 비열(非熱) 문항'),
    ('최고온 die 가 refresh 정책을 결정', 'DRAM-A-0056', [('FA-A-0040', '삭제')], '0.53'),
    ('신뢰성 시험 규격 번호 고르기', 'FA-B-0092', [('PROD-B-0115', '삭제'), ('PROD-B-0116', '삭제'), ('PROD-B-0117', '삭제'), ('PROD-B-0118', '삭제')], '0.53/0.51 — 신뢰성 규격은 FA. PROD 는 JESD238/JESD270-4 제품 규격으로'),
    ('Open 이 여러 원인에서 수렴', 'FA-I-0027', [('MIX-A-0002', '삭제')], '0.53'),
    ('적층 후 물리적 수리 불가 → 선별 앞단 배치', 'PROD-I-0033', [('SIP-B-0100', '삭제')], '0.52'),
    ('조립 지표와 신뢰성 지표를 함께 봐야 하는 이유', 'FA-I-0081', [('MET-I-0171', '삭제')], '0.51'),
    ('접합 직전 대기(queue) 시간 관리', 'COW-I-0180', [('BSP-B-0106', '삭제'), ('BUMP-B-0028', '삭제')], '0.51/0.36'),
    ('불량 위치 패턴(대칭·반복 좌표)으로 원인 계층 판정', 'MET-I-0102', [('MET-B-0037', 'MET 내 통합(삭제)'), ('MIX-B-0001', '삭제'), ('MIX-I-0031', '삭제'), ('MIX-B-0002', '삭제'), ('SAW-I-0042', '재작성(blade·chuck 고유 패턴) 또는 삭제')], '0.50/0.48 — wafer map 해석은 MET(브리프 공백 주제)'),
    ('고단에서 접합 방식 전환이 검토되는 이유', 'PROD-I-0037', [('MIX-A-0044', '삭제')], '0.50'),
    ('절단 측면 미세 crack 이 문제인 이유', 'SAW-B-0031', [('FA-B-0059', '삭제')], '0.49'),
    ('제품 내장 온도 센서의 이유', 'DRAM-B-0098', [('WARP-B-0125', '삭제')], '0.49'),
    ('TSV 수를 늘려도 방열 효과가 제한적인 이유', 'WARP-A-0197', [('TSV-I-0140', '삭제'), ('TSV-A-0105', '삭제')], '0.48/0.46 — 열 경로 판단은 THERM. TSV 는 공정 관점(liner·KOZ 비용)의 thermal TSV 문항을 새로 쓸 것'),
    ('작은 단면 = 전류 밀도↑ 로 불리', 'BUMP-I-0119', [('FA-I-0080', '삭제'), ('FA-I-0062', '삭제'), ('WARP-B-0117', '삭제'), ('WARP-A-0258', '삭제')], '0.46/0.40 — µbump EM 은 BUMP'),
    ('통전 중 특정 접점 저항 지속 상승 → crowding 부 void 성장', 'BUMP-A-0152', [('WARP-A-0259', '삭제')], '0.37'),
    ('TCB 저온·장시간 조정의 부작용', 'COW-I-0155', [('MIX-A-0004', '삭제')], '0.45'),
    ('bond head 기울기 vs die warpage 의 불량 맵 분리', 'COW-A-0155', [('WARP-A-0184', '삭제')], '0.45'),
    ('복합 결함 분석 순서(비파괴 → 파괴)', 'FA-A-0090', [('MIX-A-0036', '삭제')], '0.45'),
    ('단수↑ → TCB 압착 사이클 누적', 'COW-B-0056', [('SIP-B-0090', '삭제')], '0.45'),
    ('12→16단 확장 시 TC-NCF 제약 조합', 'COW-A-0165', [('SIP-A-0143', '삭제')], '0.44'),
    ('Shadow moiré 이름 고르기', 'MET-B-0036', [('TSV-B-0097', '삭제')], '0.43'),
    ('chain 저항: 평균 이동 vs 상위 이탈값 해석', 'TSV-A-0102', [('MET-A-0064', '삭제')], '0.43 — TSV 고유 데이터'),
    ('온도 변화에 따른 형상 측정이 필요한 이유', 'MET-B-0057', [('WARP-I-0316', '삭제')], '0.43 — THERM 파일의 비열 문항'),
    ('가장 흔한 판단 실패(한 지표만 봄) — 일반론', 'MIX-A-0052', [('MIX-A-0089', 'MIX 내 통합(삭제)'), ('FEOL-A-0015', '삭제')], '0.43'),
    ('여러 막 응력의 중립면 기준 합성', 'WARP-A-0254', [('FEOL-A-0029', '삭제')], '0.43'),
    ('몰드 wafer 연삭 시 EMC/Si 경계 단차', 'BSP-B-0091', [('WARP-A-0174', 'mv → BSP (A 대표)'), ('WARP-I-0240', '삭제'), ('WARP-I-0262', '삭제'), ('WARP-A-0194', '삭제'), ('WARP-A-0231', '삭제')], '0.43/0.39 — 연삭은 BSP'),
    ('차세대 검토에 설계·공정·열을 함께 / 경쟁사 도입만으로 전환 금지 / 학회 수치 적용 전제', 'MIX-A-0100', [('PROD-A-0053', '삭제'), ('PROD-A-0036', '삭제'), ('PROD-A-0037', '삭제'), ('MIX-A-0050', 'MIX 내 통합'), ('MIX-A-0091', 'MIX 내 통합'), ('MIX-A-0057', 'MIX 내 통합')], '0.41–0.42 — PROD 브리프가 일반론 고급으로 지목. MIX 도 사례형으로 재작성 못 하면 삭제'),
    ('미세 피치 capillary underfill 충전 난이도', 'COW-B-0050', [('COW-I-0188', 'mv → SIP (SiP 단계 underfill)'), ('SIP-I-0134', '삭제(이관 문항으로 대체)')], '0.40'),
    ('HCB 에서 CMP 요구가 극단적으로 높은 이유', 'COW-I-0237', [('COW-A-0158', 'COW 내 통합'), ('TSV-A-0136', '삭제'), ('TSV-A-0124', '삭제')], '0.36/0.35 — HCB 접합면 CMP 는 COW'),
    ('warpage 가 있는 die 에 하중만 올린 결과', 'COW-I-0141', [('BUMP-A-0146', '삭제'), ('WARP-A-0185', '삭제')], '0.39 — Smile/Cry 표기도 정리(§1)'),
    ('NCF 유동 온도와 solder 용융 구간 불일치', 'COW-I-0161', [('BUMP-I-0135', '삭제')], '0.35'),
    ('fillet 형상 관리 이유', 'COW-I-0165', [('BUMP-B-0064', '삭제')], '0.41'),
    ('방열 개선이 성능·수명 모두에 이로운 이유', 'WARP-B-0127', [('FA-I-0034', 'Arrhenius 가속계수 정량 문항으로 재작성 또는 삭제')], '0.37 — FA 공백 주제(가속계수)로 전환 권고'),
    ('core wafer 를 잘라 base wafer 에 올리는 이유(KGD)', 'PROD-B-0049', [('SIP-B-0098', '삭제')], '0.37'),
    ('몰딩·연삭을 절단보다 먼저 하는 이유', 'SAW-B-0036', [('PROD-B-0088', '삭제'), ('WARP-B-0145', '삭제')], '0.36'),
    ('연삭 후 stress relief 생략 + 박화 → 취급 crack', 'TSV-A-0123', [('TSV-A-0123', 'mv → BSP'), ('TSV-I-0161', 'mv → BSP 또는 삭제'), ('SIP-A-0142', '삭제')], '0.36 — 연삭·stress relief 는 BSP'),
    ('Bosch 보호 단계↑ → 측면 식각↓·속도↓', 'TSV-I-0194', [('FEOL-I-0013', '삭제')], '0.35 — 용어도 정정(§1)'),
    ('압착 온도↑ → 초기 강도↑ · TC 수명↓', 'COW-A-0153', [('MET-A-0070', '삭제'), ('FA-A-0031', '삭제')], '0.36'),
    ('온도↑ → refresh 주기↓', 'DRAM-B-0094', [('MET-B-0028', '삭제')], '0.35'),
    ('진공 몰딩 이유', 'WARP-B-0068', [('MET-B-0049', '삭제')], '0.40'),
    ('두 공법을 모두 보유하는 이유', 'COW-A-0192', [('MIX-A-0102', '삭제')], '0.36'),
    ('앞 공정 관리가 강조되는 이유(산포 전파) — 일반론', 'MET-B-0078', [('MET-I-0155', 'MET 내 통합(삭제)'), ('PROD-I-0035', '삭제')], '0.39'),
    ('스택 수직 열 경로의 병목(접합층)', 'WARP-A-0196', [('WARP-A-0177', '삭제(05 WARP 파일에 남은 열 문항)')], '0.36 — 분할 시 05 에 남은 열 문항'),
    ('IR 이 Si 를 투과해 내부 관찰', 'MET-B-0066', [('FA-I-0077', '삭제 또는 backside LIT/IR-OBIRCH 판단으로 재작성')], '0.40'),
    ('HCB 의 pitch 축소(“18 µm”)', 'COW-A-0073', [('BUMP-B-0080', '삭제')], '개념 중복 + 사실 충돌 F3'),
    ('강성↑ → 형상↓·접합부 crack↑ 상충', 'WARP-I-0238', [('FA-A-0049', '삭제')], '개념 중복(WARP-I-0280 과도 WARP 내 통합)'),
    ('warped wafer 를 흡착 연삭 후 해제 → 두께 편차', 'WARP-A-0204', [('WARP-A-0204', 'mv → BSP (대표)'), ('WARP-A-0173', '삭제'), ('WARP-A-0192', '삭제'), ('WARP-I-0263', '삭제')], 'WARP 내 4중 중복 + 연삭/TTV 는 BSP'),
    ('공법 명칭 고르기(TCB/MR-MUF/HCB)', 'COW', [('BUMP-B-0061', '삭제'), ('BUMP-B-0062', '삭제'), ('BUMP-B-0029', '삭제')], 'COW 에 같은 정의 문항 다수(COW-B-0104 등). 공법명 표기도 위반(§1)'),
    ('ESD 일반(정의·대책·잠재 손상·시험 모델) 15문항', 'FA', [('DRAM-B-0141', 'mv → FA'), ('DRAM-I-0143', 'mv → FA'), ('DRAM-I-0148', 'mv → FA'), ('DRAM-A-0060', 'mv → FA'), ('DRAM-B-0142', '삭제'), ('DRAM-B-0146', '삭제'), ('DRAM-B-0147', '삭제'), ('DRAM-B-0148', '삭제'), ('DRAM-B-0150', '삭제'), ('DRAM-I-0142', '삭제'), ('DRAM-I-0147', '삭제'), ('DRAM-A-0064', '삭제'), ('DRAM-A-0065', '삭제')], 'FA 에는 ESD 문항이 사실상 없음(JS-001/JS-002 는 FA 범위). DRAM 내부에서도 B/I/A 동형 중복(I-0147≈A-0064, I-0148≈A-0065, B-0148≈I-0142≈A-0060). 설계 관점(on-die ESD 보호·CDM 목표) 1–2문항은 DRAM 이 새로 써서 보유 가능'),
]

pairs = 0
xgroups = 0
for concept, owner, members, note in G:
    for i, a in members:
        chk(i)
    od = D[owner] if owner in Q else owner
    xm = [m for m, _ in members if m != owner and D[m] != od]
    pairs += len(xm)
    if xm: xgroups += 1
    if owner in Q:
        others = [m for m, _ in members if m != owner]
        own_act = next((a for m, a in members if m == owner), None)
        if own_act is None:
            dup[D[owner]].append((owner, f'[보유] {concept} — 타 분야 근중복: {", ".join(others)}', f'보유 분야. 상대 문항은 해당 분야에서 삭제/이관. 남긴 문항은 STANDARDS 기준으로 다듬을 것 ({note})'))
    for i, a in members:
        oa = next((a for m, a in members if m == owner), '')
        tgt = (owner + (f' ({oa})' if oa.startswith('mv') else '')) if owner in Q else f'{owner} 분야'
        if i == owner:
            dup[D[i]].append((i, f'{concept} — 근중복 상대: {", ".join(m for m, _ in members if m != owner)}', f'{a} ({note})'))
        else:
            dup[D[i]].append((i, f'{concept} — 보유: {tgt}', f'{a} ({note})'))

for concept, owner, members, note in G:
    if owner not in Q:
        notes[owner].append(f'**보유 개념(타 분야에서 정리됨)**: “{concept}” — 상대: ' + ', '.join(f'{m}({a})' for m, a in members) + f'. 이관 문항을 받으면 이 분야 기존 문항과 다시 중복되지 않게 정리하고, 필요하면 이 분야 관점으로 새로 출제.')
inbound = collections.defaultdict(list)
# ───────────────────── 3. 이관 제안 (중복과 무관한 오분류) ─────────────────────
M = [
    ('WARP-I-0244', 'BSP', 'Post-fab wafer warpage 원인 후보(glue 경화·뒷면 절연막) — 뒷면 공정 관리 목표'),
    ('WARP-A-0182', 'BSP', '뒷면 공정 후 warpage → pad 노광 위치 이탈 — BSP 의 pad 형성 학습 목표'),
    ('WARP-A-0218', 'COW', 'HCB 청정도·평탄도 요구 — HCB 는 COW'),
    ('WARP-A-0235', 'COW', 'pad 산화 + NCF 유동 지연 → 결함 조합 — TC-NCF 접합 불량 판정'),
    ('WARP-B-0138', 'COW', '낱개 단위 접합의 과제 — 적층 공법'),
    ('WARP-A-0256', 'MET', 'XRD 로 박막 잔류 응력 측정 원리 — 계측 기법'),
    ('WARP-A-0243', 'FA', 'EMC 계면 delamination 조기 검출 전략(SAT) — 고장분석'),
    ('WARP-I-0320', 'THERM', 'TIM 두께 편차·lid 평탄도·스택 높이 산포 → 특정 스택 고온 — 분할 때 05 에 남은 열 문항'),
    ('WARP-A-0246', 'THERM', '상면 높이 산포·TIM 압축·lid 평탄도 → 국부 열저항 — 분할 때 05 에 남은 열 문항(WARP-I-0320 과 중복이므로 THERM 에서 1개로)'),
    ('WARP-I-0284', 'WARP', '냉각 속도 → 강도·잔류 응력 — 열 설계가 아니라 기계 물성(13 THERM → 05 WARP)'),
    ('WARP-I-0321', 'WARP', '몰딩 수축 편차 → 형상 → 실장 불량 — 기계(13 THERM → 05 WARP)'),
    ('WARP-I-0283', 'BSP', '연삭 냉각수 공급 이유 — 연삭 공정(13 THERM → BSP)'),
    ('WARP-B-0121', 'FA', '결함 부위의 자기 가속 열화 구조 — 신뢰성 일반(13 THERM → FA). FA 에 동형이 있으면 삭제'),
    ('BUMP-I-0156', 'COW', 'NCF filler 입경 → 미접합 경로 — NCF 재료/공정'),
    ('BUMP-I-0158', 'COW', '압착 하중↑ 의 새 문제 — TCB 공정 조건'),
    ('BUMP-A-0145', 'COW', 'height offset + bond force 상향의 한계 — TCB 공정 조건'),
    ('TSV-A-0155', 'COW', 'underfill void 위치 예측 — 적층 충전'),
    ('SIP-B-0165', 'COW', 'MR-MUF 에서 단수↑ 시 어려워지는 것 — 적층 공법'),
    ('SIP-A-0187', 'COW', '저단·후막 die 조건의 두 공법 우열 — 적층 공법 비교'),
    ('SIP-A-0075', 'COW', 'HCB CMP 목표(거칠기·dishing) — HCB 접합면'),
    ('SIP-B-0069', 'PROD', '8-Hi 24 GB 와 12-Hi 36 GB 의 동일 대역폭 — 제품 구성'),
    ('SIP-I-0158', 'MET', 'SiP 전 HBM 최종 검사 강화 근거 — 시험 흐름'),
    ('FA-A-0058', 'DRAM', '정정 가능 오류(ECC) 증가 추세 대응 — DRAM ECC (FA 브리프 지목)'),
    ('FA-A-0032', 'BSP', '뒷면 절연막 저온화 vs glue 열 한계 — BSP (FA 브리프 지목)'),
    ('FA-A-0024', 'THERM', 'HBM cube height 와 SoC 높이 정합 → 접촉 열저항 편차 — 열 설계 (FA 브리프 지목)'),
    ('DRAM-I-0165', 'PROD', 'HBM4 I/O 2배의 조립 측 부담 — 제품 구조/세대 비교'),
    ('PROD-A-0016', 'WARP', '극박 mid core 16-Hi 의 stack warpage 지배 요소 — 기계'),
    ('PROD-A-0033', 'MET', '스택 간격이 좁을 때 결함 검사 난이도 — 검사'),
    ('MET-B-0050', 'SAW', 'dicing 냉각수 공급 이유 — 절단 장비'),
    ('MET-I-0116', 'SAW', 'dicing 이송 속도↑ 결과 — 절단 조건'),
    ('MET-B-0033', 'FA', 'FIB 로 원하는 지점 단면 가공 — 고장분석 기법'),
    ('FEOL-A-0003', 'BSP', 'reveal 식각 선택비 저하 → Cu 돌출 산포 → 접합 불량 분포 (FEOL 브리프 지목)'),
    ('FEOL-A-0010', 'FA', '흡습 후 급속 가열 계면 박리(popcorn) — MSL/preconditioning (FEOL 브리프 지목)'),
    ('FEOL-B-0047', 'FA', '뒷면 광 방출에 InGaAs 검출기 — FA 기법 (FEOL 브리프 지목)'),
    ('FEOL-A-0018', 'SIP', '전원망 재분배 상충 — PDN (SIP 공백 주제, FEOL 브리프 지목)'),
    ('FEOL-B-0042', 'SIP', '용량이 다른 decap 병용 이유 — PDN (SIP 공백 주제)'),
    ('FEOL-B-0035', 'SIP', '신호선 끝 반사 — SI (SIP 공백 주제)'),
    ('FEOL-I-0009', 'MET', 'probe 접촉 압력 — 시험 (FEOL 브리프 지목)'),
    ('FEOL-B-0012', 'MET', 'wafer 상태 칩 양불 판정(EDS/KGD) — 시험'),
    ('FEOL-A-0019', 'COW', '극박 core die + 액상 충전 복합 현상 — MR-MUF. FEOL-A-0037 은 동일 문항이므로 삭제'),
]
for i, to, why in M:
    chk(i)
    mv[D[i]].append((i, to, why))
for i, to, why in M:
    inbound[to].append(i)
for concept, owner, members, note in G:
    for m, a in members:
        mm = re.match(r'mv → (\w+)', a)
        if mm: inbound[mm.group(1)].append(m)
for k, v in inbound.items():
    notes[k].append(f'**받을 이관 문항(Phase 2 에 EA 가 이동)**: {", ".join(sorted(set(v)))} — 도착 후 W3 에서 이 분야 문항과의 중복을 다시 본다. W2 신규 출제 때 같은 개념을 또 쓰지 말 것.')
dup['FEOL'].append(('FEOL-A-0037', 'FEOL-A-0019 와 동일 내용(극박 die + 액상 충전)', '삭제(FEOL-A-0019 를 COW 로 이관)'))
dup['THERM'].append(('WARP-A-0232', 'WARP-A-0195 와 동일(연삭 잔여 두께 축소 시 검증 항목)', '하나만 보유(THERM 열-기계 상충 문항으로 유효)'))
dup['WARP'].append(('WARP-A-0276', 'WARP-A-0269 와 동일(Advanced MR-MUF 저하중 기구) + 사실 충돌 F5', '하나만 남기고, FACT 판정 후 표현 확정'))

# ───────────────────── 4. 사실 충돌 ─────────────────────
F = [
    ('F1', 'Smile/Cry 정의가 반대', {
        'WARP': ['WARP-I-0001', 'WARP-I-0003~0026', 'WARP-B-0001'],
        'COW': ['COW-I-0141'], 'BUMP': ['BUMP-A-0146', 'BUMP-A-0150'], 'TSV': ['TSV-A-0049~0070, TSV-I-0058~0089 (f_warp 그림)']},
     'f_warp 현행 표와 WARP-I 가족은 “bump 면 아래 + 중앙이 기준면에서 멂 = Smile”(active 면 기준), COW-I-0141·BUMP-A-0146/0150 해설은 같은 형상을 “Cry” 라 부른다. STANDARDS 2.5(위에서 본 형상: ∩ = Cry, ∪ = Smile)는 **COW·BUMP 쪽과 일치**하고 f_warp 표·WARP-I 가족이 틀렸다. bump 면 아래 자세 12문항은 정답 키가 반대.',
     'WARP: 정답 키 교정 + 가족 3개로 축소(§1). DA: EA_to_DA §1 표 교체 전까지 f_warp 명명표를 근거로 쓰지 않음. TSV: f_warp 사용 54문항 그림 교체.'),
    ('F2', 'N단의 간극 수가 분야마다 다름', {
        'THERM': [f'{len([x for x in NG if x[0]=="THERM"])}문항 (WARP-I-0002, WARP-A-0003~0049)'], 'MET': ['MET-I-0001'], 'SIP': ['SIP-I-0016, SIP-A-0044 등(규약 일치 — 기준 예시)']},
     'THERM 열저항 가족은 “12단 → 간극은 die 수보다 하나 적은 11개” 로 계산하고 f_therm.n 에 core 수를 넣어(그림이 base 를 빼고 n−1 간극으로 계산) 결과를 맞춘다. SIP 는 “core n 장이면 간극 n 개”, MET-I-0001 은 “접합 간극 11곳”. STANDARDS 2.5: N단 → 간극 N.',
     'THERM: 간극 N 으로 재계산·f_therm.n=N+1(최하단 core 까지를 묻는 경우만 N−1 을 명시). MET-I-0001: 0.995¹² 로 재계산(≈ 74 %). DA: f_therm 고정 pill “간극 수는 die 수보다 하나 적다” → “간극 수 = core die 수” (EA_to_DA §7).'),
    ('F3', 'HCB 의 pitch·bump 표현', {
        'BUMP': ['BUMP-B-0080'], 'COW': ['COW-A-0073', 'COW-I-0245', 'COW-B-0003~0026 (HCB 분기에 bump pitch·간극)'], 'BUMP ': ['BUMP-A-0002, BUMP-A-0033~0042']},
     'BUMP-B-0080·COW-A-0073 은 HCB 를 “bump pitch 18 µm 이하/미만” 으로 서술(업체 보도 [R]). STANDARDS 2.4 는 HCB pad pitch ≤ 10 µm·bump 간극 없음, COW-I-0245 는 “D2W HCB 2 µm 급 시연”. 한편 BUMP-A-0002·A-0033~0042 는 solder µbump 를 pitch 6–20 µm 로 설정(2.4 의 µbump 25–55 µm 밖, HCB 영역과 겹침).',
     'COW: “18 µm” 는 [V] 출처 확인 전 정답 근거 금지(FACT) — 쓰더라도 “접합 pitch(pad pitch)” 로. BUMP: B-0080 삭제, A-0033~0042 의 pitch 는 µbump 현실 범위로 바꾸거나 “가정” 명시(NUM 과 함께).'),
    ('F4', 'preconditioning 규격 번호', {'FA': ['FA-B-0002', 'FA-B-0043~0046', 'FA-A-0033', '↔ FA-B-0094'], 'PROD': ['PROD-B-0115(보기)']},
     'FA-B-0002·B-0043~0046·A-0033 은 “preconditioning = J-STD-020”, FA-B-0094 는 “preconditioning = JESD22-A113”. STANDARDS 2.3: 절차는 JESD22-A113, J-STD-020 은 MSL 분류·리플로 프로파일.',
     'FA: “JESD22-A113 (J-STD-020 프로파일)” 로 통일. f_rel 기본 seq 첫 행도 같은 문제(EA_to_DA §8).'),
    ('F5', 'MR-MUF 의 가압 여부 / Advanced MR-MUF 의 개량점', {'COW': ['COW-I-0021', 'COW-B-0095', 'COW-B-0114', 'COW-I-0214', 'COW-A-0189'], 'BUMP': ['BUMP-I-0159'], 'WARP': ['WARP-A-0269', 'WARP-A-0276']},
     'COW-I-0021·BUMP-I-0159 는 MR-MUF 를 “die 마다 가압하지 않는 일괄 reflow(층별 하중 제약 없음)” 로, COW-B-0095/B-0114/I-0214/A-0189·WARP-A-0269/0276 은 Advanced MR-MUF 를 “압착(적층) 하중을 낮춘 개량형” 으로 정의한다. 가압이 없다는 방식의 “하중을 낮췄다” 는 서로 맞지 않는다.',
     'FACT 판정 요청: SK hynix [V] 발표 기준으로 Advanced MR-MUF 의 개량점(신규 EMC·칩 휨 제어/가접합 조건 등)을 확정하고, “가접합(pre-bond) 하중” 처럼 무엇의 하중인지 특정. 확정 전에는 COW 가 보유하고 WARP 는 WARP-A-0269/0276 중 1개만, 판정 후 표현 통일.'),
    ('F6', 'MR-MUF 방열 우위의 근거', {'COW': ['COW-B-0087', 'COW-B-0106', 'COW-I-0215'], 'BUMP': ['BUMP-I-0159'], 'THERM': ['WARP-I-0055']},
     '근거가 “고열전도 충전재(EMC)”(COW-B-0087/B-0106), “간극을 채워 경로가 연속”(COW-I-0215), “thermal dummy bump 를 더 많이 배치”(BUMP-I-0159), “filler 를 쓰기 쉬운 구조”(WARP-I-0055)로 제각각이다. 각자 정답으로 두면 다른 분야 문항에서 오답 근거가 된다.',
     'COW 가 [V] 출처로 근거를 확정(EMC 열전도 + dummy bump 밀도)해 해설에 명시하고, BUMP·THERM 은 같은 표현을 쓴다.'),
    ('F7', '“Erosion” 의 두 가지 뜻', {'TSV': ['TSV-I-0194', '↔ TSV-B-0076, TSV-A-0099'], 'FEOL': ['FEOL-I-0013']},
     'TSV-B-0076·A-0099 는 Erosion = CMP 에서 조밀 패턴 영역 전체가 낮아짐, TSV-I-0194·FEOL-I-0013 은 Bosch 측벽 식각을 “Erosion” 이라 부른다.',
     '식각 문항을 “측면 식각(lateral etch)/scallop” 으로 바꿈.'),
    ('F8', '도금 전류밀도 과다의 결과', {'TSV': ['TSV-I-0151', 'TSV-B-0106'], 'BUMP': ['BUMP-I-0144']},
     'TSV-I-0151 정답 “결정립이 거칠어진다”, BUMP-I-0144 정답 “거칠어지고 편차가 커진다”(표면 거칠기). TSV 브리프는 TSV-B-0106 에 대해 “고전류밀도는 핵생성 증가로 결정립이 미세해지는 경향, 주 문제는 pinch-off/void” 로 판정.',
     'FACT 판정 후 통일: 한계 전류밀도 초과 시 “표면 거칠어짐(수지상·burnt)”과 “결정립 크기” 를 구분해 서술.'),
    ('F9', 'HBM4 12단 용량', {'PROD': ['PROD-B-0103']},
     '정답 “HBM3E 12단과 36 GB 로 동일”. STANDARDS 2.2: HBM4 는 24 Gb·32 Gb die → 12-Hi 36 GB 또는 48 GB. “동일” 은 유일 정답이 아니다(DRAM·PROD 용량 계산 문항의 32 Gb die 설정과도 충돌 가능).',
     'die 밀도를 지문에 주고 계산형으로 바꾸거나, “24 Gb die 기준” 을 명시.'),
]
for code, title, per, what, ins in F:
    for d, ids in per.items():
        conf[d.strip()].append((code, title, ', '.join(ids), what, ins))

# ───────────────────── 출력 ─────────────────────
os.makedirs(OUT, exist_ok=True)
stats = {}
for c in CODES:
    t = term.get(c, []); du = dup.get(c, []); m = mv.get(c, []); cf = conf.get(c, [])
    nE = sum(1 for r in t if r[1] == 'E')
    lines = [f'# XD 교차분야 지시 — {c} ({NAMES[c]})', '',
             '- 작성: XD (교차분야 일관성) · W1 사전 점검 · 2026-11-20 · 기준: `docs/agents/STANDARDS.md` 2.5 · 3.10',
             f'- 대상 파일: `data/{["TSV","BSP","BUMP","SAW","COW","WARP","SIP","FA","PROD","DRAM","MET","MIX","FEOL"].index(c) if c!="THERM" else 13:02d}_{c}.json`' + (' (WARP 분할 후 열 문항, id 는 `WARP-` 유지)' if c == 'THERM' else ''),
             '- 지시 종류: **수정** · **삭제**(보고서 삭제 표에 “타 분야 중복: 보유 id” 로 기록) · **mv → CODE**(레코드에 `"mv": "CODE"`, 직접 옮기지 말 것) · **보유**(상대 분야가 지우므로 이 문항을 품질 기준으로 다듬을 것)',
             '- XD 판정과 다르게 처리하려면 리뷰 보고서에 근거를 적는다(EA 최종 판정).', '',
             '## 요약', '', '| 항목 | 건수 |', '|---|---|',
             f'| 1. 용어 규약 위반 (E / W) | {nE} / {len(t)-nE} 행 |',
             f'| 2. 교차 중복 관련 문항 | {len(du)} |', f'| 3. 이관 제안 (mv) | {len(m)} |', f'| 4. 사실 충돌 관여 | {len(cf)} 건 |', '']
    lines += ['## 1. 용어 규약 위반 (STANDARDS 2.5)', '']
    if t:
        lines += ['| id | 등급 | 문제 | 지시 |', '|---|---|---|---|']
        for i, sev, p, ins in t:
            lines.append(f'| {i} | {sev} | {p} | {ins} |')
    else:
        lines.append('- 해당 없음.')
    if notes.get(c):
        lines += ['', '### 참고']
        for n in notes.get(c, []):
            lines += ['', f'- {n}']
    lines += ['', '## 2. 교차 중복 · 근중복 (보유 분야 판정)', '',
              '판정 기준: 그 개념이 어느 분야 학습 목표의 핵심인가(ROSTER §3). 숫자는 핵심 텍스트+보기 char 4-gram Jaccard(참고값, 0.35 이상 판독).', '']
    if du:
        lines += ['| id | 문제 | 지시 |', '|---|---|---|']
        for i, p, ins in du:
            lines.append(f'| {i} | {p} | {ins} |')
    else:
        lines.append('- 해당 없음.')
    lines += ['', '## 3. 이관 제안 (오분류)', '']
    if m:
        lines += ['| id | 지시 | 이유 |', '|---|---|---|']
        for i, to, why in m:
            lines.append(f'| {i} | mv → {to} (`"mv": "{to}"`, 다듬은 뒤) | {why} |')
    else:
        lines.append('- 해당 없음.')
    lines += ['', '## 4. 분야 간 사실 충돌', '']
    if cf:
        lines += ['| 충돌 | 이 분야 관련 id | 무엇이 다른가 | 지시 |', '|---|---|---|---|']
        for code, title, ids, what, ins in cf:
            lines.append(f'| {code} {title} | {ids} | {what} | {ins} |')
    else:
        lines.append('- 해당 없음.')
    lines.append('')
    open(f'{OUT}/{c}.md', 'w').write('\n'.join(lines))
    stats[c] = (nE, len(t) - nE, len(du), len(m), len(cf))

json.dump({'stats': stats, 'pairs': pairs, 'groups': len(G), 'xgroups': xgroups, 'F': [(f[0], f[1]) for f in F], 'mv': len(M)}, open(os.path.join(os.path.dirname(__file__), 'stats.json'), 'w'), ensure_ascii=False)
print(stats, pairs, len(G), len(M))
