import sys,os,collections
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import gen
from gen import G,M,F,stats,CODES,NAMES,D,Q,pairs,xgroups
L=[]
L+=['# XD 교차분야 일관성 점검 — W1 사전 점검 요약','',
'- 작성: XD · 2026-11-20 · 입력: `data/*.json` 14개 파일(5,000문항, WARP 분할 후 상태 — 05_WARP 226 · 13_THERM 537) · 기준: STANDARDS 2.5(용어 규약) · 3.10(중복)',
'- 분야별 지시: `docs/reviews/xd/CODE.md` (id · 문제 · 지시). 이 문서는 집계와 판정 원칙, 다른 에이전트에 넘길 사항만 담는다.',
'- 읽기 전용으로 수행(data/·template.html·tools/ 미수정). 스냅샷 시점 이후 분야 에이전트가 고친 문항은 W3 사후 점검(`_xd_post.md`)에서 다시 본다.','',
'## 1. 한눈에','',
'| 분야 | 용어 E | 용어 W | 교차 중복 관련 | mv 제안 | 사실 충돌 관여 |','|---|---|---|---|---|---|']
for c in CODES:
    e,w,du,m,cf=stats[c]
    L.append(f'| [{c}]({c}.md) | {e} | {w} | {du} | {m} | {cf} |')
L+=['','- “용어 E/W” 는 표의 행 수다. COW 의 HCB 표기는 한 행에 여러 문항을 묶었다(아래 §2 의 문항 수 참고).','',
'## 2. 용어 규약 위반 (문항 수)','',
'| 규약 | 등급 | 문항 수 | 분포 | 요지 |','|---|---|---|---|---|',
'| N단 ↔ 간극 수 | E | 49 | THERM 48 · MET 1 | THERM 열저항 가족이 “12단 → 간극은 die 수보다 하나 적은 11개”, f_therm.n 에 core 수 입력. MET-I-0001 “접합 간극 11곳”. SIP 는 규약대로 “core n 장 → 간극 n 개” |',
'| N단 ↔ 간극 수 (표현) | W | 71 | SIP 71 | 값은 규약과 일치하나 “접합 간극은 die 수보다 하나 적습니다” — THERM 오류와 같은 문장이라 “간극 수 = core die 수(N)” 로 |',
'| Smile / Cry | E | 16 | WARP 15 · BUMP 1 | bump 면 아래 자세 12문항(WARP-I-0003~0025 중) 정답 키가 2.5 와 반대, WARP-I-0001 전제·정답 반대, WARP-B-0001 지문 자기모순, WARP-A-0185 자세 미기재, BUMP-A-0150 해설 혼입 |',
'| Smile / Cry | W | 69 | WARP 12 · TSV 54 · SIP 1 · COW 1 · BUMP 1 | BEOL 면 위 12문항(정답은 맞으나 f_warp 명명표 근거 + 24문항 가족), f_warp 를 CTE 계산에 쓴 TSV 54·SIP 1(명명표 노출), 해설 명명 설명 |',
'| 공법명: TCB 를 공법명으로 | E | 9 | COW 5 · BUMP 2 · SIP 1 · PROD 1 | “TCB와 MR-MUF”, “TCB 방식/적층” → TC-NCF (TCB 는 장비 방식) |',
'| 공법명: HCB 비표준 표기 | E | 123 | COW 109 · BUMP 4 · TSV 2 · SIP 2 · THERM 2 · FA·PROD·MET·MIX 각 1 | Hybrid Bonding / hybrid bonding / 하이브리드 본딩 / Hybrid Copper Bonding 혼용 → “HCB” |',
'| 공법명: 약어 없는 full name | W | 99 | COW 99 | “hybrid copper bonding” 만 반복 → 첫 언급 “HCB(hybrid copper bonding)” |',
'| 공법명: MUF 단독·Mass Reflow | W | 2 (+BUMP-B-0029 E) | COW 2 | MR-MUF 로 |',
'| µbump 표기 | W | 10 | COW 5 · MET 2 · BUMP·PROD·THERM 각 1 | micro-bump / Microbump / 마이크로(범프) → µbump |',
'| 용어 충돌: Erosion | E | 2 | TSV 1 · FEOL 1 | Bosch 측벽 식각을 “Erosion” — CMP Erosion 과 충돌 |',
'| **합계** | **E** | **199** | | (TCB·HCB 중복 문항 2개 제외 시 고유 197) |',
'| | **W** | **251** | | f_therm 단수 미기재 311(THERM 노트) 은 별도 |','',
'- 단위 표기(µ/μ, um)는 위반 0건: 전 문항 U+00B5, “um” 단위 없음.',
'- MR-MUF·TC-NCF 표기는 변형(MR MUF, TCNCF 등) 0건 — 문제는 TCB 대용과 HCB 쪽뿐.','',
'## 3. 교차 중복 · 근중복','',
f'- 방법: ① `validate.py --codes W_NEAR_DUP_X`(5-gram ≥ 0.80) → 3쌍(WARP-B-0147↔MIX-B-0017, COW-A-0160↔BUMP-A-0147, MIX-I-0013↔MET-B-0058) + `E_DUP_EXACT` 1쌍(PROD-B-0061↔SIP-I-0130). ② 핵심 텍스트+보기의 char 4-gram Jaccard(숫자 정규화) 0.35 이상 143쌍 전수 판독. ③ 주제 키워드 군집(ESD, KGD, 연삭, 공법 명칭, thermal TSV 등) 판독.',
f'- 결과: **개념 중복 군 {len(G)}개(교차분야 {xgroups}개), 교차 분야 문항 쌍 {pairs}개** 를 판정했다. 동형 템플릿 우연 일치(예: “A 와 B 를 가르는 결정적 단서는” 틀만 같은 문항)는 중복이 아니라고 판정해 제외.',
'- 보유 원칙(“그 개념이 어느 분야 학습 목표의 핵심인가”): 접합 공정·NCF·MUF·HCB → COW · 연삭/stress relief/몰드 연삭 → BSP · 신뢰성 시험 규격·가속 시험·ESD·고장 감별 → FA · KGD/시험 흐름·wafer map·SPC → MET · 단수·높이 예산·die 구성 → PROD · 열 경로 판단 → THERM · warpage 거동 → WARP · µbump EM → BUMP · refresh·온도 센서 → DRAM · 인터포저 → SIP · dicing → SAW · 일반론(판단 태도)은 MIX 1개 이하(사례형 재작성 조건).','',
'| # | 개념 | 보유 | 삭제·이관 측 |','|---|---|---|---|']
for k,(concept,owner,members,note) in enumerate(G,1):
    own = f'{owner} ({D[owner]})' if owner in Q else f'{owner} 분야'
    oth = ', '.join(f'{m}({D[m]}) {a}' for m,a in members if m!=owner)
    oa = next((a for m,a in members if m==owner),None)
    if oa: own += f' — {oa}'
    L.append(f'| {k} | {concept} | {own} | {oth} |')
cnt=collections.Counter()
for _,owner,members,_ in G:
    for m,a in members:
        if m==owner: 
            if a.startswith('mv'): cnt['mv']+=1
            continue
        cnt['mv' if a.startswith('mv') else ('삭제' if a.startswith('삭제') else '재작성/통합')]+=1
L+=['',f'- 집계(보유 측 제외 문항): 삭제 {cnt["삭제"]} · mv {cnt["mv"]} · 재작성/분야 내 통합 {cnt["재작성/통합"]}.','',
'## 4. 오분류 이관 제안 (중복과 무관)','',
f'- **{len(M)}건** (+ 중복 판정 안에서의 mv {cnt["mv"]}건 = 총 {len(M)+cnt["mv"]}건).','',
'| id | 현재 | → | 이유 |','|---|---|---|---|']
for i,to,why in M: L.append(f'| {i} | {D[i]} | {to} | {why} |')
L+=['','- WARP 분할 경계 정리: 05 에 남은 열 문항(WARP-I-0320, WARP-A-0246 → THERM, WARP-A-0177 은 THERM 의 WARP-A-0196 과 중복이라 삭제), 13 으로 간 비열 문항(WARP-I-0284·I-0321 → WARP, WARP-I-0283 → BSP, WARP-B-0121 → FA, 그리고 중복 삭제 대상 WARP-A-0194·A-0231·A-0217·I-0298·I-0299·I-0316·B-0117·A-0258·A-0259·B-0125·A-0002). 분할 스크립트(`_w05_split_moved_ids.json`)의 기준을 EA 가 확인해 주길.','',
'## 5. 분야 간 사실 충돌','',
'| # | 충돌 | 관련 분야 | 무엇이 다른가 | 판정·처리 |','|---|---|---|---|---|']
for code,title,per,what,ins in F:
    L.append(f'| {code} | {title} | {", ".join(k.strip() for k in per)} | {what} | {ins} |')
L+=['','## 6. 다른 에이전트에 넘길 사항','',
'- **DA**: ① f_warp 명명표 교체(EA_to_DA §1) — F1 의 근원. 교체 전에는 WARP·TSV 가 표를 근거로 쓰지 못한다. ② f_therm 고정 pill “간극 수는 die 수보다 하나 적다” 와 n(=base 포함) 의미 — F2 의 근원(§7, `core` param 제안 지지). ③ f_bond hcb 분기의 gap 치수(§5) — COW-B-0003 계열.',
'- **FACT**: F5(Advanced MR-MUF 개량점·MR-MUF 가압 여부), F6(MR-MUF 방열 근거), F3(“HCB 18 µm” 의 등급), F8(도금 전류밀도와 결정립), F9(HBM4 12단 용량). THERM 의 iHBM/ICE 문항(WARP-B-0150·B-0154·A-0277)은 브리프대로 [V] 확인 전 사용 금지.',
'- **NUM**: F2 재계산 대상 THERM 48문항(간극 N 으로 바꾸면 정답·오답 값이 모두 바뀜)과 MET-I-0001(정답 “약 72 %” → 0.98¹²×0.995¹² ≈ 73.9 %).',
'- **EA**: ① 5-gram 0.80 검사기는 교차 중복을 3쌍만 잡는다. 판독으로 확인한 쌍의 실제 유사도는 0.35–0.75 — `W_NEAR_DUP_X` 임계를 낮추거나 char 4-gram 보조 검사를 W3 에 쓰겠다. ② Phase 2 이관 시 같은 개념의 mv 문항이 대상 분야 기존 문항과 다시 중복되지 않는지 W3 에서 재검사.','',
'## 7. 방법과 한계','',
'- 기계 탐색: 정규식(용어·수치), char 4-gram 역색인 Jaccard(교차 분야 쌍만), 분야별 어휘 점수(오분류 후보) → 판독. 스크립트는 scratchpad(`xd/s/`).',
'- 오분류는 어휘 점수로 후보 354건을 뽑아 판독했고, SIP↔PROD(높이 계산 231건)처럼 소관이 중첩된 군은 개별 이관 대신 §3 보유 원칙으로 처리했다.',
'- 사실 충돌은 “같은 물리량·정의를 분야마다 다르게 쓰는 경우” 만 다뤘다. 분야 내부의 단독 사실 오류는 FACT·NUM 소관이며 여기서는 충돌에 걸린 것만 적었다.','']
open('/home/user/MyOwn/hbm_quiz/docs/reviews/xd/_index.md','w').write('\n'.join(L))
print(cnt, len(M))
