# MET 분야 브리프 — 검사 · 계측과 품질

- 소유 파일: `data/10_MET.json` · 기준: `docs/agents/STANDARDS.md` · 자동 검사: `python3 tools/validate.py --domain MET`
- 작성: EA (Phase 1, 2026-11-20) · 기준선 리포트: `docs/reviews/_auto_baseline.md`

## 0. 현황

| 난이도 | 문항 | stem 단일형 | ctx 조립형 | 정답 위치 ①/②/③/④ |
|---|---|---|---|---|
| 초급 | 86 | 22 | 64 | 22 / 17 / 29 / 18 |
| 중급 | 172 | 91 | 81 | 49 / 39 / 38 / 46 |
| 고급 | 119 | 60 | 59 | 32 / 31 / 28 / 28 |
| 합계 | 377 | 173 | 204 | |

- k=1 상황도 173 · k=0 주제도 204 · 그림 사용: f_note 141, f_plot 121, f_stack 111, f_rel 3, f_bs 1
- **차단 E 이슈가 있는 문항: 302 / 377** (E_JOSA_CIRC 는 EA Phase 2 일괄 처리라 제외)

## 1. 자동 검사 요약 (기준선)

| 코드 | 건수 | 예시 id |
|---|---|---|
| `E_META_METRICS` | 204 | MET-A-0061, MET-A-0062, MET-A-0063, MET-A-0064 |
| `E_STYLE_PLAIN` | 174 | MET-A-0061, MET-A-0062, MET-A-0063, MET-A-0064 |
| `E_JOSA_CIRC` | 161 | MET-A-0061, MET-A-0062, MET-A-0063, MET-A-0064 |
| `E_EXP_SHORT` | 152 | MET-A-0071, MET-A-0077, MET-A-0080, MET-A-0082 |
| `E_TITLE_TRUNC` | 142 | MET-A-0061, MET-A-0062, MET-A-0063, MET-A-0064 |
| `E_EXP_ONLY_REFS` | 116 | MET-A-0071, MET-A-0080, MET-A-0082, MET-A-0090 |
| `E_FAMILY_OVER` | 64 | MET-A-0020, MET-A-0021, MET-A-0022, MET-A-0023 |
| `E_FIG_HIDE_RESULT` | 55 | MET-A-0039, MET-A-0040, MET-A-0041, MET-A-0042 |
| `E_JOSA_EN` | 6 | MET-B-0026, MET-B-0049, MET-B-0064, MET-I-0095 |
| `E_CALC_NO_WORK` | 3 | MET-A-0104, MET-B-0036, MET-I-0123 |
| `E_DOUBLE_Q` | 2 | MET-B-0065, MET-B-0068 |
| `E_DUP_EXACT` | 1 | MET-I-0102 |
| `W_TITLE_COPY` | 204 | MET-A-0061, MET-A-0062, MET-A-0063, MET-A-0064 |
| `W_EXP_DISTRACTORS` | 174 | MET-A-0001, MET-A-0002, MET-A-0003, MET-A-0004 |
| `W_META_METRICS` | 173 | MET-A-0001, MET-A-0002, MET-A-0003, MET-A-0004 |
| `W_NEAR_DUP` | 130 | MET-A-0009, MET-A-0010, MET-A-0011, MET-A-0012 |
| `W_K1_FIG_EXTRA` | 114 | MET-A-0001, MET-A-0002, MET-A-0005, MET-A-0007 |
| `W_TITLE_QUESTION` | 60 | MET-A-0099, MET-A-0102, MET-A-0107, MET-A-0108 |
| `W_OPT_ODD_END` | 55 | MET-A-0004, MET-A-0073, MET-A-0079, MET-A-0087 |
| `W_OPT_WEAK` | 30 | MET-A-0004, MET-A-0071, MET-A-0081, MET-A-0091 |
| `W_OPT_LONGEST` | 12 | MET-A-0002, MET-A-0003, MET-A-0004, MET-A-0005 |
| `W_OPT_ABSOLUTE` | 9 | MET-A-0003, MET-A-0093, MET-A-0104, MET-B-0030 |
| `W_OPT_LEN` | 3 | MET-A-0001, MET-A-0002, MET-I-0002 |
| `W_METRIC_LEN` | 2 | MET-A-0002, MET-A-0003 |
| `W_EXP_OFFTOPIC` | 2 | MET-B-0038, MET-B-0040 |
| `W_EXP_REF_MISMATCH` | 1 | MET-A-0081 |
| `I_EXP_SRC_TAG` | 173 | MET-A-0001, MET-A-0002, MET-A-0003, MET-A-0004 |

(참고: `I_JOSA_SPACE` 223 · `I_TEMPLATE_JOIN` 204 — 새로 쓰는 문장은 조사를 붙여 쓰고, ctx 조립형은 STANDARDS 3.1 에 따라 정리)

## 1A. W1 입력 (지원 에이전트 결과 — 작업 1순위)

- **NUM** `docs/reviews/num/MET.md`: 검증 165 · 산술 일치 152 · **정답 오류 확정 13** · **비현실 설정 12** · 그림·지표 정답 노출 0 · 간극 규약 위반 1 · 근접 오답(<3 %) 28 · 회상형(FACT 이관) 3. 문항별 올바른 값·식은 해당 파일. solver: `tools/num/`.
- **FACT** `docs/reviews/_facts.md` — 이 분야 관련 주장 1건 (판정은 §1–7 표, 문항 id 는 §8):
  - **F42** [정정] `f_rel` 그림 기본 seq 의 "JESD22-A104 · −55 / +125 °C — 3문항: MET-A-0005, MET-I-0002, MET-I-0003
- **XD** `docs/reviews/xd/MET.md` — 용어 규약 위반·교차 중복(보유/삭제)·이관(mv)·사실 충돌 지시. 요약은 `docs/reviews/xd/_index.md`.
- 처리 원칙: NUM 정답 오류·FACT '정정'/'사용 금지' 판정 → 해당 문항을 **가장 먼저** 고치거나 삭제. FACT '조건부' 는 지문 표현을 고치면 유지(예: "JEDEC 규격 상한 775 µm" → "높이 상한(설계 조건) 775 µm"). 판정과 다르게 처리하면 보고서에 근거.

## 2. 표본 조사로 확인한 대표 결함 (EA 직접 판독: 난이도별 10문항 이상)

- **'검사·계측' 분야인데 계측 문항이 거의 없음**: bump coplanarity·TTV(IR 간섭)·overlay·AFM/profiler·AOI·SPC·Gauge R&R 이 0–2 건. 대신 테스터 병렬 시간 계산(MET-B-0007 계열), 직렬 수율 곱(MET-I-0015 계열), 장비 일반 상식(진공 척·도금액 순환·플라즈마 압력 — FEOL 성격) 위주.
- **가족 초과 64**: 병렬 시험 시간, 스택 수율, 검사 주기별 헛적층 die.
- 수율 곱 문항은 계산이 맞음(검증: 0.96¹²×0.995¹² = 0.577). 다만 "선별 없이 쌓았을 때" 와 KGD 선별 후 비교로 바꾸면 고급 가치가 생김.
- 일반론 고급("복합 인자 문제에서도 단일 인자 실험이 필요한 이유", MET-A-0106; "수율 지표와 신뢰성 지표가 반대로 움직일 때", MET-A-0074)은 HBM 데이터 없이 상식으로 풀림.

## 3. 핵심 개념 체크리스트와 현재 커버리지

키워드 기반 근사치(지문·보기·해설에서 해당 주제가 다뤄진 문항 수). 0–4 = **공백**, 5–14 = 부족, 15+ = 있음(질은 별도 판단).

| 주제 | 초급 | 중급 | 고급 | 판정 |
|---|---|---|---|---|
| KGD·wafer probe test | 7 | 39 | 25 | 있음 |
| burn-in·test time·parallelism | 22 | 24 | 10 | 있음 |
| bump 높이/coplanarity 계측 | 0 | 0 | 1 | **공백** |
| Si 두께·TTV(IR 간섭) | 0 | 0 | 0 | **공백** |
| overlay 계측 | 0 | 0 | 0 | **공백** |
| AFM·profilometer(dishing nm) | 0 | 0 | 0 | **공백** |
| SAM·X-ray inline 검사 | 1 | 0 | 0 | **공백** |
| AOI·defect inspection·review | 0 | 0 | 1 | **공백** |
| warpage 계측(shadow moiré) | 1 | 0 | 0 | **공백** |
| SPC·Cpk·관리도 | 0 | 1 | 0 | **공백** |
| Gauge R&R·측정 불확도 | 0 | 2 | 2 | **공백** |
| 수율 모델(직렬 수율·Poisson) | 5 | 46 | 30 | 있음 |
| 샘플링·검출력 | 0 | 2 | 4 | 부족 |

**우선 보강 공백**: bump 높이·coplanarity 계측(공초점·백색광 간섭), Si 두께·TTV(IR 간섭계), HCB overlay 계측과 배율·회전 성분 분해, CMP dishing nm 계측(AFM/프로파일러) 분해능, inline X-ray/SAT 검사 감도, AOI·입자 검사(HCB), SPC(관리도·Cpk), Gauge R&R, KGD 테스트 커버리지와 escape, 샘플링 검출력

## 4. 작업 지시 (우선순위 순)

0. **[최우선] 메타 지표 제거 — 377건** (`E_META_METRICS` 204, `W_META_METRICS` 173). 화면 '제시 조건' 띠에 "난이도: 고급", "묻는 것: 해당 항목", "세부 주제", "핵심어" 가 그대로 보인다(DA 스크린샷 확인). 지문 조건 2–4개로 바꾸거나, 요약할 조건이 없으면 `"metrics": []`(키는 유지). 정답 오류 수정과 같은 1순위로 처리한다.
1. **정답 오류·사실 정정 (W1 입력 §1A)**: NUM 정답 오류 확정·비현실 설정·그림 노출(`docs/reviews/num/MET.md`), FACT 정정·사용 금지·조건부 주장(§1A 의 F 번호), XD 용어·중복·이관 지시(`docs/reviews/xd/MET.md`), §2 의 기술 정정 후보, `E_EXP_REF_ANSWER`(정답 키 재검증). 메타 지표 제거(0번)와 함께 가장 먼저.
2. **템플릿 가족 정리**: `E_FAMILY_OVER` 대상은 가족당 3개(가능하면 난이도별 1개)만 남기고 삭제하거나 다른 판단을 묻도록 재작성. 근중복(`W_NEAR_DUP`)도 정리.
3. **ctx 조립형 정리**: ctx 가 qt 풀이에 필요 없으면 stem 단일형으로 변환. 기술 외 사유 오답·타 분야 오답(`W_OPT_WEAK`) 교체, 형식 단서(`W_OPT_ODD_END`, `W_OPT_LONGEST`, `W_OPT_ABSOLUTE`) 제거.
4. **해설 재작성**: `E_EXP_SHORT`·`E_EXP_ONLY_REFS`·`E_STYLE_PLAIN`·`W_EXP_DISTRACTORS` — 정답 근거 + 오답 3개 각각의 오류 + (계산) 식·대입·결과. 일괄 `[근거]` 꼬리표는 고친 해설에서 뺀다.
5. **제목·지표·그림**: `E_TITLE_TRUNC`·`W_TITLE_*` 제목 재작성, `E_META_METRICS` 지표를 지문 조건으로 교체, `E_K1_FIG_NUM`·`E_FIG_ANSWER_LEAK`·`E_FIG_INTERNAL`·`W_FIG_*` 그림 params 정정.
6. **난이도 재배치**: 단순 대입 계산·용어 문항이 고급이면 lv 를 내린다. lv 가 바뀌면 id 의 LV 도 달라져야 하므로 **새 id(`CODE-LV-9xxx`)를 발급하고 `"prev": "옛 id"` 필드를 남긴다**(보고서에 old→new 기록). 고급은 STANDARDS §1 기준으로 채운다.
7. **신규 출제**(§5) — 공백 주제 위주. 새 id 는 `MET-LV-9001` 부터.
8. 타 분야 문항은 고쳐서 `"mv": "CODE"` 로 이관 제안(EA 가 Phase 2 에서 이동) 하거나 자기 분야 관점으로 재작성.

## 4A. DA Phase 1 템플릿 변경으로 손봐야 할 기존 문항

템플릿 기본값·규약이 바뀌어(LAYOUT_RULES §3–4, STANDARDS 부록 A) 아래 문항은 params 를 고치지 않으면 그림이 지문과 어긋나거나 답을 보여 준다.

- `E_FIG_HIDE_RESULT` **55건** — `hideResult: true` 추가 (그림이 계산·판정 결과를 표시). 입력 params 자체가 답이면(예: f_stack.n = 최대 단수) k=0 으로: MET-A-0039, MET-A-0040, MET-A-0041, MET-A-0042, MET-A-0043, MET-A-0044, MET-A-0045, MET-A-0046, MET-A-0047, MET-A-0048, MET-A-0049, MET-A-0050, MET-A-0051, MET-A-0052, MET-A-0053, MET-A-0054, MET-A-0055, MET-A-0056, MET-A-0057, MET-A-0058, MET-A-0059, MET-A-0060, MET-I-0001, MET-I-0060, MET-I-0061, MET-I-0062, MET-I-0063, MET-I-0064, MET-I-0065, MET-I-0066, MET-I-0067, MET-I-0068, MET-I-0069, MET-I-0070, MET-I-0071, MET-I-0072, MET-I-0073, MET-I-0074, MET-I-0075, MET-I-0076, MET-I-0077, MET-I-0078, MET-I-0079, MET-I-0080, MET-I-0081, MET-I-0082, MET-I-0083, MET-I-0084, MET-I-0085, MET-I-0086, MET-I-0087, MET-I-0088, MET-I-0089, MET-I-0090, MET-I-0091
- `W_METRIC_LEN` **2건** — 지표 label ≤ 12자 · value ≤ 16자: MET-A-0002, MET-A-0003
- `W_OPT_LEN` **3건** — 보기 60자 이하로: MET-A-0001, MET-A-0002, MET-I-0002

## 5. 추가 출제 목표

| | 초급 | 중급 | 고급 | 합계 |
|---|---|---|---|---|
| 신규 최소 | 10 | 30 | 40 | 80 |

- 가족 초과로 정리될 문항 약 64 건은 위 신규로 대체한다(수량 유지보다 질 우선, 최종 분야 규모는 ±10 % 허용).
- 최종 난이도 비율 권장: 초급 25–30 % · 중급 35–40 % · 고급 30–35 %.

- 고급: overlay 측정 벡터에서 평행 이동·회전·배율 성분 분리 후 원인 판정, Cpk 계산 → 규격·공정 중심 조정 판단, Gauge R&R 결과로 측정계 적합성 판정, KGD 커버리지·escape 율로 스택 수율 추정(선별 위치 최적화), 입자 밀도(Poisson)로 HCB 수율 추정
- 중급: 계측 기법별 분해능·측정 대상 매칭, 관리도 이상 패턴 해석

## 6. 사용할 그림 템플릿과 params

| 템플릿 | params | 제약 · 주의 |
|---|---|---|
| `f_plot` | `title`, `x`/`y`{min,max,ticks ≤ 6,lab}, `series` ≤ 4, `marks` ≤ 3, `bullets` ≤ 3 | 데이터 해석형 고급의 주력 |
| `f_note` | `title` ≤ 22자, `points` ≤ 4(각 ≤ 50자), `ask` ≤ 12자 | points 는 **판단 관점** — 정답 문장 금지 |
| `f_stack` | `n`(core die 수), `highlight`, `gap_um`, `h_um`, `limit_um`, `bullet`, `hideResult` | 계산 답을 `n`/`h_um` 에 넣지 말 것 |
| `f_rel` | `seq` ≤ 4행, `cur`, `fails` ≤ 5점, `xlab`, `xmax`, `ymax`, `crit`, `hint`, `bullet` | 기본 seq 첫 행은 JESD22-A113 preconditioning. 기본 seq 의 TC "1000 cycle" 은 JESD47(condition B 700 cycle)과 다르다 — JEDEC 자격 시험을 묻는 문항은 `seq` 를 직접 준다(DA 수정 요청 중). HTOL·HTS 는 `xlab`/`xmax` 를 시간 축으로 |


- 장비 일반 상식 문항(진공·도금 교반·식각 압력)은 FEOL 로 `mv` 제안하거나 계측 관점으로 재작성.
- 데이터 해석형 고급에는 `f_table`(표)·`f_wafermap`(맵)·`f_plot`(그래프)을 쓴다(DA Phase 1 신설, 예시는 LAYOUT_RULES §4). 결과를 그림이 계산하는 템플릿은 `hideResult` 의무(STANDARDS 부록 A.1).

## 7. 완료 조건

- `python3 tools/validate.py --domain MET --gate` 통과(차단 E 0). 남는 W 는 수정 또는 `vx` + 사유.
- `python3 tools/build.py` · `node tools/smoke.js dist/HBM_quiz.html` 오류 없음.
- 보고서 `docs/reviews/MET.md` (형식: ROSTER §4).
