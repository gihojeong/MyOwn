# WARP 분야 브리프 — Warpage 와 기계적 응력

- 소유 파일: `data/05_WARP.json` · 기준: `docs/agents/STANDARDS.md` · 자동 검사: `python3 tools/validate.py --domain WARP`
- 작성: EA (Phase 1, 2026-11-20) · 기준선 리포트: `docs/reviews/_auto_baseline.md`

## 0. 현황

| 난이도 | 문항 | stem 단일형 | ctx 조립형 | 정답 위치 ①/②/③/④ |
|---|---|---|---|---|
| 초급 | 70 | 18 | 52 | 17 / 21 / 17 / 15 |
| 중급 | 92 | 25 | 67 | 35 / 11 / 20 / 26 |
| 고급 | 64 | 0 | 64 | 16 / 16 / 19 / 13 |
| 합계 | 226 | 43 | 183 | |

- k=1 상황도 43 · k=0 주제도 183 · 그림 사용: f_bond 120, f_warp 97, f_therm 9
- **차단 E 이슈가 있는 문항: 216 / 226** (E_JOSA_CIRC 는 EA Phase 2 일괄 처리라 제외)

## 1. 자동 검사 요약 (기준선)

| 코드 | 건수 | 예시 id |
|---|---|---|
| `E_META_METRICS` | 183 | WARP-A-0167, WARP-A-0168, WARP-A-0169, WARP-A-0170 |
| `E_JOSA_CIRC` | 171 | WARP-A-0167, WARP-A-0168, WARP-A-0169, WARP-A-0170 |
| `E_STYLE_PLAIN` | 148 | WARP-A-0167, WARP-A-0168, WARP-A-0169, WARP-A-0170 |
| `E_TITLE_TRUNC` | 140 | WARP-A-0167, WARP-A-0168, WARP-A-0169, WARP-A-0170 |
| `E_EXP_SHORT` | 118 | WARP-A-0183, WARP-A-0184, WARP-A-0218, WARP-A-0222 |
| `E_JOSA_EN` | 85 | WARP-A-0175, WARP-A-0182, WARP-A-0184, WARP-A-0185 |
| `E_EXP_ONLY_REFS` | 82 | WARP-A-0218, WARP-A-0222, WARP-A-0224, WARP-A-0225 |
| `E_FAMILY_OVER` | 22 | WARP-B-0006, WARP-B-0007, WARP-B-0011, WARP-B-0012 |
| `E_K1_FIG_NUM` | 13 | WARP-B-0002, WARP-B-0003, WARP-B-0004, WARP-B-0005 |
| `E_FIG_WARP_NAME` | 12 | WARP-I-0003, WARP-I-0005, WARP-I-0007, WARP-I-0008 |
| `E_EXP_REF_ANSWER` | 2 | WARP-B-0100, WARP-I-0289 |
| `E_DOUBLE_Q` | 1 | WARP-B-0132 |
| `W_TITLE_COPY` | 183 | WARP-A-0167, WARP-A-0168, WARP-A-0169, WARP-A-0170 |
| `W_OPT_ODD_END` | 60 | WARP-A-0190, WARP-A-0219, WARP-A-0226, WARP-A-0227 |
| `W_EXP_DISTRACTORS` | 56 | WARP-A-0183, WARP-A-0219, WARP-B-0001, WARP-B-0002 |
| `W_OPT_WEAK` | 52 | WARP-A-0190, WARP-A-0199, WARP-A-0228, WARP-A-0233 |
| `W_TITLE_QUESTION` | 43 | WARP-A-0233, WARP-A-0252, WARP-B-0066, WARP-B-0067 |
| `W_NEAR_DUP` | 34 | WARP-B-0008, WARP-B-0009, WARP-B-0010, WARP-B-0011 |
| `W_K1_FIG_EXTRA` | 26 | WARP-B-0001, WARP-I-0001, WARP-I-0003, WARP-I-0004 |
| `W_META_METRICS` | 24 | WARP-I-0003, WARP-I-0004, WARP-I-0005, WARP-I-0006 |
| `W_OPT_LONGEST` | 12 | WARP-A-0188, WARP-A-0218, WARP-A-0222, WARP-A-0224 |
| `W_OPT_ABSOLUTE` | 9 | WARP-A-0180, WARP-A-0254, WARP-A-0273, WARP-B-0114 |
| `W_EXP_OFFTOPIC` | 5 | WARP-B-0070, WARP-B-0073, WARP-I-0248, WARP-I-0252 |
| `W_EXP_REF_MISMATCH` | 2 | WARP-A-0173, WARP-A-0192 |
| `W_K1_METRIC_NUM` | 1 | WARP-B-0002 |
| `W_METRIC_LEN` | 1 | WARP-I-0001 |
| `W_OPT_PUNCT` | 1 | WARP-A-0219 |
| `W_QT_LONG` | 1 | WARP-A-0219 |
| `W_FIG_TOPIC` | 1 | WARP-A-0235 |
| `W_NEAR_DUP_X` | 1 | WARP-B-0147 |

(참고: `I_JOSA_SPACE` 183 · `I_TEMPLATE_JOIN` 183 — 새로 쓰는 문장은 조사를 붙여 쓰고, ctx 조립형은 STANDARDS 3.1 에 따라 정리)

## 2. 표본 조사로 확인한 대표 결함 (EA 직접 판독: 난이도별 10문항 이상)

- **W0.5 분할(2026-11-20)**: 원래 763문항 중 열 설계 537문항을 `data/13_THERM.json`(THERM 에이전트 소유)으로 옮겼다. 이 파일에는 warpage·몰딩·기계 응력 226문항이 남았다(이관 id 목록: `docs/reviews/_w05_split_moved_ids.json`). 열·warpage 가 섞인 경계 문항(TIM 두께 편차 + lid 평탄도 등 약 20)은 이 파일에 남겼다 — 열이 주제면 `"mv": "THERM"` 으로 제안.
- **Smile/Cry 규약 확정**(오케스트레이터 승인): 측정 자세 그대로 **위에서 본 형상 — ∩ = Cry(convex), ∪ = Smile(concave)**. DA 가 `f_warp` 표를 이 규약으로 교체했다(sign 1 = ∩ = Cry). 이 파일의 명명 판정 가족(WARP-I-0003~0006 등, "Bump 면이 아래 + 중앙이 멂 → Smile")은 **옛 규약으로 쓰여 있어 이제 그림과 정답이 반대** — 전부 재작성(§4A `E_FIG_WARP_NAME`). 지문에 측정 자세와 형상을 문장으로도 명시한다.
- 명명 판정 가족, Tg 거동 가족(WARP-B-0003 계열 10, -0008 계열 6)이 초·중급의 큰 비중 — 가족당 3개.
- **ctx 조립형(몰딩·EMC 일반 상식)**: "진공 상태에서 molding 하는 이유", "유동성이 중요한 이유" 등 일반론과 빈약 오답("수축이 힘을 만듦" vs "색상이 변하기 때문", WARP-B-0094).
- **타 분야 혼재**: 연삭 냉각수(WARP-I-0283 → BSP), 낱개 접합 과제(WARP-B-0138 → COW), 접합층 두께 축소 이유(WARP-B-0102 → COW/PROD), molded wafer 연삭 단차(WARP-I-0240 → BSP). `mv` 로 이관 제안.
- "실리콘, 구리, 몰딩 수지, 공기를 열이 잘 전달되는 순서"(WARP-B-0078) 같은 열 문항이 남아 있으면 `mv: THERM`.

## 3. 핵심 개념 체크리스트와 현재 커버리지

키워드 기반 근사치(지문·보기·해설에서 해당 주제가 다뤄진 문항 수). 0–4 = **공백**, 5–14 = 부족, 15+ = 있음(질은 별도 판단).

| 주제 | 초급 | 중급 | 고급 | 판정 |
|---|---|---|---|---|
| CTE mismatch·bimetal(Stoney) | 22 | 3 | 5 | 있음 |
| EMC Tg·탄성률·cure shrinkage | 20 | 3 | 4 | 있음 |
| EMC 조성(filler·점도·유동) | 15 | 23 | 22 | 있음 |
| shadow moiré·DIC 측정 | 0 | 1 | 1 | **공백** |
| smile/cry 정의·측정 자세 | 1 | 25 | 2 | 있음 |
| reflow 중 동적 warpage | 0 | 0 | 0 | **공백** |
| die/wafer warpage와 접합 불량 | 0 | 0 | 5 | 부족 |
| molding(진공·압축 성형·grinding) | 15 | 11 | 16 | 있음 |
| lid·stiffener·package 휨 | 4 | 1 | 1 | 부족 |
| 얇은 die/wafer 휨·carrier | 0 | 3 | 4 | 부족 |

**우선 보강 공백**: shadow moiré·DIC 측정 원리와 온도 이력 데이터 해석, reflow 중 동적 warpage 와 접합 불량(non-wet/short) 위치, Stoney/bimetal 식 기반 휨 크기·방향 추정, EMC 조성(filler·CTE₁/CTE₂·Tg·탄성률)과 휨 제어, 얇은 core die·wafer 의 휨과 carrier, lid/stiffener 와 2.5D 패키지 휨, Advanced MR-MUF 의 휨 제어 원리

## 4. 작업 지시 (우선순위 순)

0. **[최우선] 메타 지표 제거 — 207건** (`E_META_METRICS` 183, `W_META_METRICS` 24). 화면 '제시 조건' 띠에 "난이도: 고급", "묻는 것: 해당 항목", "세부 주제", "핵심어" 가 그대로 보인다(DA 스크린샷 확인). 지문 조건 2–4개로 바꾸거나, 요약할 조건이 없으면 `"metrics": []`(키는 유지). 정답 오류 수정과 같은 1순위로 처리한다.
1. **사실 오류·정답 오류 먼저**: §2 의 기술 정정 후보, `E_EXP_REF_ANSWER`(정답 키 재검증), NUM·FACT 에이전트 결과(`docs/reviews/num/WARP.md`, `docs/reviews/_facts.md`)를 반영한다.
2. **템플릿 가족 정리**: `E_FAMILY_OVER` 대상은 가족당 3개(가능하면 난이도별 1개)만 남기고 삭제하거나 다른 판단을 묻도록 재작성. 근중복(`W_NEAR_DUP`)도 정리.
3. **ctx 조립형 정리**: ctx 가 qt 풀이에 필요 없으면 stem 단일형으로 변환. 기술 외 사유 오답·타 분야 오답(`W_OPT_WEAK`) 교체, 형식 단서(`W_OPT_ODD_END`, `W_OPT_LONGEST`, `W_OPT_ABSOLUTE`) 제거.
4. **해설 재작성**: `E_EXP_SHORT`·`E_EXP_ONLY_REFS`·`E_STYLE_PLAIN`·`W_EXP_DISTRACTORS` — 정답 근거 + 오답 3개 각각의 오류 + (계산) 식·대입·결과. 일괄 `[근거]` 꼬리표는 고친 해설에서 뺀다.
5. **제목·지표·그림**: `E_TITLE_TRUNC`·`W_TITLE_*` 제목 재작성, `E_META_METRICS` 지표를 지문 조건으로 교체, `E_K1_FIG_NUM`·`E_FIG_ANSWER_LEAK`·`E_FIG_INTERNAL`·`W_FIG_*` 그림 params 정정.
6. **난이도 재배치**: 단순 대입 계산·용어 문항이 고급이면 lv 를 내린다. lv 가 바뀌면 id 의 LV 도 달라져야 하므로 **새 id(`CODE-LV-9xxx`)를 발급하고 `"prev": "옛 id"` 필드를 남긴다**(보고서에 old→new 기록). 고급은 STANDARDS §1 기준으로 채운다.
7. **신규 출제**(§5) — 공백 주제 위주. 새 id 는 `WARP-LV-9001` 부터.
8. 타 분야 문항은 고쳐서 `"mv": "CODE"` 로 이관 제안(EA 가 Phase 2 에서 이동) 하거나 자기 분야 관점으로 재작성.

## 4A. DA Phase 1 템플릿 변경으로 손봐야 할 기존 문항

템플릿 기본값·규약이 바뀌어(LAYOUT_RULES §3–4, STANDARDS 부록 A) 아래 문항은 params 를 고치지 않으면 그림이 지문과 어긋나거나 답을 보여 준다.

- `E_FIG_WARP_NAME` **12건** — `f_warp` 표가 확정 규약(sign 1 = ∩ = Cry)으로 바뀌어 정답 명칭과 그림이 반대 — 문항 재작성: WARP-I-0003, WARP-I-0005, WARP-I-0007, WARP-I-0008, WARP-I-0009, WARP-I-0010, WARP-I-0011, WARP-I-0013, WARP-I-0021, WARP-I-0022, WARP-I-0024, WARP-I-0025
- `W_QT_LONG` **1건** — 질문 마지막 문장 90자 이하로: WARP-A-0219
- `W_METRIC_LEN` **1건** — 지표 label ≤ 12자 · value ≤ 16자: WARP-I-0001

## 5. 추가 출제 목표

| | 초급 | 중급 | 고급 | 합계 |
|---|---|---|---|---|
| 신규 최소 | 15 | 30 | 40 | 85 |

- 가족 초과로 정리될 문항 약 22 건은 위 신규로 대체한다(수량 유지보다 질 우선, 최종 분야 규모는 ±10 % 허용).
- 최종 난이도 비율 권장: 초급 25–30 % · 중급 35–40 % · 고급 30–35 %.

- 고급: shadow moiré 승온·냉각 곡선(Tg 전후 기울기, hysteresis)으로 실장 조건과 위험 구간 판단, CTE·두께·모듈러스 3변수 bimetal 근사로 휨 방향·크기 추정, reflow 온도 구간별 die–substrate 상대 휨으로 non-wet/bridge 위치 예측, EMC filler 증량의 휨·유동·void 트레이드오프
- 중급: Tg 전후 CTE 변화와 휨 방향, 측정 자세와 명칭(확정 규약), 몰딩 방식(transfer/compression)과 휨

## 6. 사용할 그림 템플릿과 params

| 템플릿 | params | 제약 · 주의 |
|---|---|---|
| `f_warp` | `ref`: bump-down·beol-up, `sign` 1 = ∩ = **Cry** / −1 = ∪ = **Smile**, `mag_um`, `tg`, `temp` | 표가 확정 규약(2.5)으로 교체됨. 정답 명칭과 sign 일치(E_FIG_WARP_NAME) |
| `f_bond` | `method`: ncf·mrmuf·hcb, `pitch_um`, `gap_um`, `voids` 0–3, `filler_trap`, `nonwet`, **`dish`**, `bullet` | **hcb: dishing 미접합 pad 는 `dish: true` 일 때만 그려진다(기본 없음)** — dishing 을 근거로 쓰는 hcb 문항은 `dish: true` 필수(E_FIG_DISH_OPTIN). **hcb 에 `gap_um` 금지**(표시 안 됨, HCB 는 bump 간극 없음). 결함 표식(voids·filler_trap·nonwet·dish)은 동시에 2개 이하 |
| `f_plot` | `title`, `x`/`y`{min,max,ticks ≤ 6,lab}, `series` ≤ 4, `marks` ≤ 3, `bullets` ≤ 3 | 데이터 해석형 고급의 주력 |
| `f_note` | `title` ≤ 22자, `points` ≤ 4(각 ≤ 50자), `ask` ≤ 12자 | points 는 **판단 관점** — 정답 문장 금지 |



- `f_warp` 의 `ref`·`sign`·`mag_um`·`tg`·`temp` 는 지문과 일치. 명명 표는 확정 규약으로 교체 완료(sign 1 = Cry).
- 이 파일에 남은 `f_therm` 9문항은 주제를 확인해 `mv: THERM` 또는 그림 교체.
- 데이터 해석형 고급에는 `f_table`(표)·`f_wafermap`(맵)·`f_plot`(그래프)을 쓴다(DA Phase 1 신설, 예시는 LAYOUT_RULES §4). 결과를 그림이 계산하는 템플릿은 `hideResult` 의무(STANDARDS 부록 A.1).

## 7. 완료 조건

- `python3 tools/validate.py --domain WARP --gate` 통과(차단 E 0). 남는 W 는 수정 또는 `vx` + 사유.
- `python3 tools/build.py` · `node tools/smoke.js dist/HBM_quiz.html` 오류 없음.
- 보고서 `docs/reviews/WARP.md` (형식: ROSTER §4).
