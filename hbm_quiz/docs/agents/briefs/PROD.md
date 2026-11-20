# PROD 분야 브리프 — HBM 제품과 구조

- 소유 파일: `data/08_PROD.json` · 기준: `docs/agents/STANDARDS.md` · 자동 검사: `python3 tools/validate.py --domain PROD`
- 작성: EA (Phase 1, 2026-11-20) · 기준선 리포트: `docs/reviews/_auto_baseline.md`

## 0. 현황

| 난이도 | 문항 | stem 단일형 | ctx 조립형 | 정답 위치 ①/②/③/④ |
|---|---|---|---|---|
| 초급 | 135 | 26 | 109 | 39 / 31 / 31 / 34 |
| 중급 | 61 | 27 | 34 | 19 / 13 / 15 / 14 |
| 고급 | 54 | 15 | 39 | 18 / 14 / 15 / 7 |
| 합계 | 250 | 68 | 182 | |

- k=1 상황도 68 · k=0 주제도 182 · 그림 사용: f_stack 129, f_plot 98, f_note 22, f_sip 1
- **차단 E 이슈가 있는 문항: 209 / 250** (E_JOSA_CIRC 는 EA Phase 2 일괄 처리라 제외)

## 1. 자동 검사 요약 (기준선)

| 코드 | 건수 | 예시 id |
|---|---|---|
| `E_META_METRICS` | 182 | PROD-A-0016, PROD-A-0017, PROD-A-0018, PROD-A-0019 |
| `E_JOSA_CIRC` | 167 | PROD-A-0016, PROD-A-0017, PROD-A-0018, PROD-A-0021 |
| `E_STYLE_PLAIN` | 149 | PROD-A-0016, PROD-A-0017, PROD-A-0018, PROD-A-0019 |
| `E_TITLE_TRUNC` | 130 | PROD-A-0016, PROD-A-0017, PROD-A-0018, PROD-A-0019 |
| `E_EXP_SHORT` | 127 | PROD-A-0022, PROD-A-0023, PROD-A-0025, PROD-A-0026 |
| `E_JOSA_EN` | 85 | PROD-A-0018, PROD-A-0022, PROD-A-0026, PROD-A-0028 |
| `E_EXP_ONLY_REFS` | 82 | PROD-A-0022, PROD-A-0023, PROD-A-0025, PROD-A-0026 |
| `E_FAMILY_OVER` | 22 | PROD-A-0011, PROD-A-0012, PROD-A-0013, PROD-A-0014 |
| `E_CALC_NO_WORK` | 14 | PROD-B-0099, PROD-B-0100, PROD-B-0101, PROD-B-0110 |
| `E_DOUBLE_Q` | 7 | PROD-B-0042, PROD-B-0076, PROD-B-0095, PROD-B-0097 |
| `E_FIG_HIDE_RESULT` | 2 | PROD-B-0003, PROD-I-0001 |
| `E_DUP_EXACT` | 2 | PROD-B-0061, PROD-I-0044 |
| `E_K1_FIG_NUM` | 1 | PROD-A-0002 |
| `W_TITLE_COPY` | 182 | PROD-A-0016, PROD-A-0017, PROD-A-0018, PROD-A-0019 |
| `W_K1_FIG_EXTRA` | 61 | PROD-A-0001, PROD-A-0002, PROD-A-0004, PROD-A-0005 |
| `W_OPT_ODD_END` | 60 | PROD-A-0021, PROD-A-0023, PROD-A-0025, PROD-A-0033 |
| `W_TITLE_QUESTION` | 47 | PROD-A-0026, PROD-A-0027, PROD-A-0038, PROD-A-0046 |
| `W_NEAR_DUP` | 47 | PROD-A-0008, PROD-A-0011, PROD-A-0012, PROD-A-0013 |
| `W_OPT_WEAK` | 38 | PROD-A-0022, PROD-A-0023, PROD-A-0025, PROD-A-0026 |
| `W_EXP_DISTRACTORS` | 35 | PROD-A-0001, PROD-A-0002, PROD-A-0003, PROD-A-0004 |
| `W_META_METRICS` | 12 | PROD-A-0001, PROD-A-0003, PROD-A-0004, PROD-B-0001 |
| `W_OPT_LONGEST` | 11 | PROD-A-0001, PROD-A-0004, PROD-A-0019, PROD-A-0041 |
| `W_TITLE_LEAK` | 8 | PROD-B-0006, PROD-B-0012, PROD-B-0018, PROD-B-0024 |
| `W_OPT_ABSOLUTE` | 4 | PROD-A-0036, PROD-A-0039, PROD-A-0040, PROD-I-0005 |
| `W_METRIC_LEN` | 3 | PROD-B-0001, PROD-I-0003, PROD-I-0004 |
| `W_K1_METRIC_NUM` | 3 | PROD-B-0003, PROD-I-0003, PROD-I-0004 |
| `W_OPT_LEN` | 3 | PROD-A-0004, PROD-I-0004, PROD-I-0005 |
| `W_OPT_STEM_ECHO` | 2 | PROD-A-0003, PROD-B-0094 |
| `W_EXP_OFFTOPIC` | 2 | PROD-B-0062, PROD-B-0107 |
| `W_FIG_LEAK` | 1 | PROD-I-0001 |
| `W_EXP_REF_MISMATCH` | 1 | PROD-I-0030 |
| `I_EXP_SRC_TAG` | 68 | PROD-A-0001, PROD-A-0002, PROD-A-0003, PROD-A-0004 |
| `I_FACT_WATCH` | 14 | PROD-A-0001, PROD-A-0002, PROD-B-0001, PROD-B-0002 |

(참고: `I_JOSA_SPACE` 224 · `I_TEMPLATE_JOIN` 182 — 새로 쓰는 문장은 조사를 붙여 쓰고, ctx 조립형은 STANDARDS 3.1 에 따라 정리)

## 1A. W1 입력 (지원 에이전트 결과 — 작업 1순위)

- **NUM** `docs/reviews/num/PROD.md`: 검증 58 · 산술 일치 58 · **정답 오류 확정 0** · **비현실 설정 9** · 그림·지표 정답 노출 0 · 간극 규약 위반 0 · 근접 오답(<3 %) 0 · 회상형(FACT 이관) 19. 문항별 올바른 값·식은 해당 파일. solver: `tools/num/`.
- **FACT** `docs/reviews/_facts.md` — 이 분야 관련 주장 24건 (판정은 §1–7 표, 문항 id 는 §8):
  - **F01** [확인] HBM4 = 2,048 bit/스택, 독립 채널 32 × 64 bit, 채널당 pseu — 5문항: PROD-B-0001, PROD-B-0002, PROD-B-0095, PROD-B-0099, PROD-I-0003
  - **F02** [확인] HBM4 JEDEC 최대 8 Gb/s, 스택 ≈ 2 TB/s — 2문항: PROD-B-0002, PROD-B-0124
  - **F03** [확인] HBM4 4/8/12/16-Hi, 24·32 Gb die, 최대 64 GB(32 Gb× — 4문항: PROD-B-0003, PROD-B-0102, PROD-I-0001, PROD-I-0002
  - **F04** [정정] HBM4 는 HBM3 컨트롤러와 호환되지 않는다 — 1문항: PROD-I-0003
  - **F05** [확인] HBM3(JESD238, 2022-01): 6.4 Gb/s, 819 GB/s, 16 채 — 2문항: PROD-B-0099, PROD-I-0003
  - **F07** [확인] HBM3E 는 별도 JEDEC 세대가 아님; 업체 핀 속도 9.2(Micron)·9.6 — 2문항: PROD-I-0003, PROD-I-0004
  - **F12** [조건부] 720 µm = HBM 패키지 높이(8/12-Hi) — 2문항: PROD-A-0001, PROD-B-0107
  - **F13** [조건부] 775 µm = HBM4 패키지 높이 규격 상한(12·16-Hi), HBM3E 720  — 3문항: PROD-A-0001, PROD-A-0002, PROD-B-0107
  - **F14** [사용 금지] HBM4E 세대에서 패키지 높이를 약 900 µm 로 추가 완화 검토 — 1문항: PROD-B-0135
  - **F15** [정정] 해설 꼬리표 "Hot Chips 2026 SK hynix 발표 정리 (775 µm 한계 — 3문항: PROD-A-0001, PROD-A-0002, PROD-A-0003
  - **F16** [확인] SK hynix HBM4: I/O 2,048, 전력 효율 40 % 이상 개선, 10 G — 4문항: PROD-B-0122, PROD-B-0123, PROD-B-0125, PROD-B-0132
  - **F17** [정정] PROD-B-0124 해설 "JEDEC 규격 핀 속도는 하한선" — 1문항: PROD-B-0124
  - **F18** [확인] Samsung HBM4: core 1c(10 nm급 6세대), base die 자사 파 — 2문항: PROD-B-0126, PROD-B-0127
  - **F19** [확인] ISSCC 2026 공개 12단 HBM4 스택 대역폭 3 TB/s 급 — 1문항: PROD-B-0101
  - **F20** [확인] HBM4 12단 제품 용량 = HBM3E 12단과 같은 36 GB — 1문항: PROD-B-0103
  - **F21** [확인] Samsung HBM4E(GTC 2026 최초 공개): 16 Gb/s, 4.0 TB/s — 2문항: PROD-B-0128, PROD-B-0129
  - **F22** [확인] SK hynix HBM4E 12단 샘플: 최대 16 Gb/s, 48 GB, Advanc — 1문항: PROD-B-0130
  - **F24** [확인] Samsung HBM3E 12H: TC NCF 박막화로 칩 간 간격 7 µm, 8H 와 — 2문항: PROD-B-0133, PROD-B-0134
  - **F27** [조건부] HBM4 base die 를 로직 공정으로: 한 회사는 외부 파운드리 12 nm, 다른 — 1문항: PROD-A-0004
  - **F28** [확인] HBM4 세대 양산 주력은 µbump 기반 기존 공법, HCB 는 차세대 후보 — 2문항: PROD-B-0108, PROD-B-0109
  - **F29** [확인] MR-MUF = SK hynix, TC-NCF = Samsung·Micron — 1문항: PROD-B-0132
  - **F31** [확인] TC-NCF = die 별 하중·온도 정밀 제어, MR-MUF = 일괄 리플로로 생산성 — 1문항: PROD-B-0111
  - **F33** [판정 참조] 현행 HBM die 간 접속 피치 "20 µm 안팎"(자릿수 문항) — 1문항: PROD-B-0110
  - **F39** [확인] 시험 번호 대응: A101 THB · A103 HTS(HTSL) · A104 TC ·  — 4문항: PROD-B-0115, PROD-B-0116, PROD-B-0117, PROD-B-0118
- **XD** `docs/reviews/xd/PROD.md` — 용어 규약 위반·교차 중복(보유/삭제)·이관(mv)·사실 충돌 지시. 요약은 `docs/reviews/xd/_index.md`.
- 처리 원칙: NUM 정답 오류·FACT '정정'/'사용 금지' 판정 → 해당 문항을 **가장 먼저** 고치거나 삭제. FACT '조건부' 는 지문 표현을 고치면 유지(예: "JEDEC 규격 상한 775 µm" → "높이 상한(설계 조건) 775 µm"). 판정과 다르게 처리하면 보고서에 근거.

## 2. 표본 조사로 확인한 대표 결함 (EA 직접 판독: 난이도별 10문항 이상)

- **업체 소문형 사실**: "SK하이닉스가 샘플을 공급한 HBM4E 의 핀당 최대 속도 16 Gbps"(PROD-B-0130) — [R] 등급 이하, 정답 근거 불가. 업체 고유 수치 문항 전수 재검증(FACT 에이전트 결과 반영).
- **고급이 기술 내용 없음**: "학회 발표 수치를 자사 조건에 적용할 때 확인할 전제"(PROD-A-0037, -0050 중복), "차세대 구조를 검토할 때 설계·공정·열을 함께 보아야 하는 이유"(PROD-A-0053) — 일반론. 고급 54 중 39가 ctx 조립형.
- **용량 계산 가족**(PROD-B-0013 계열): 초·중·고급에 같은 식이 반복(16 Gb × 8 ÷ 8). 고급에 단순 용량 계산(PROD-A-0008, -0015) 배치.
- **터무니없는 오답**: "패키지 전체 두께를 10 mm 이상으로"(PROD-B-0094), "셀 용량 10배".
- **정정(FACT F04)**: PROD-I-0003 "HBM4 는 HBM3 컨트롤러와 비호환" 은 JESD270-4 발표문(하위 호환 명시)과 **정반대** — Phase 1 브리프에서 유지 가치로 적은 것을 철회한다.
- 맞는 내용(유지 가치): HBM3E 1,024 bit·16 채널·32 PC(PROD-I-0004), base die 로직 공정 이전(PROD-A-0004 — 업체별 공정은 [V] 출처로 확인).

## 3. 핵심 개념 체크리스트와 현재 커버리지

키워드 기반 근사치(지문·보기·해설에서 해당 주제가 다뤄진 문항 수). 0–4 = **공백**, 5–14 = 부족, 15+ = 있음(질은 별도 판단).

| 주제 | 초급 | 중급 | 고급 | 판정 |
|---|---|---|---|---|
| HBM 세대별 I/O 폭·채널(HBM2E→HBM4) | 10 | 6 | 1 | 있음 |
| 핀 속도·대역폭 | 9 | 2 | 0 | 부족 |
| 용량·die 밀도(24/32 Gb) | 42 | 33 | 12 | 있음 |
| stack height 4/8/12/16-Hi | 60 | 39 | 35 | 있음 |
| 패키지 높이 720/775 µm | 1 | 0 | 2 | **공백** |
| base die(로직 공정·custom HBM) | 40 | 24 | 16 | 있음 |
| 전압 VDD/VDDQ·전력 효율 pJ/bit | 6 | 2 | 3 | 부족 |
| footprint·ball map | 0 | 0 | 0 | **공백** |
| HBM vs GDDR/LPDDR 비교 | 0 | 0 | 0 | **공백** |
| RAS·ECC·repair | 0 | 1 | 0 | **공백** |
| JEDEC 표준 문서(JESD238/270-4) | 1 | 0 | 0 | **공백** |
| 제품 로드맵(HBM3E 12H, HBM4 16H) | 29 | 6 | 5 | 있음 |

**우선 보강 공백**: JEDEC 세대별 핵심 사양 비교(STANDARDS 2.2 표 범위), 패키지 높이 720 → 775 µm 의 의미, footprint/ball map, HBM vs GDDR7/LPDDR5X(대역폭·전력·비용) 비교, RAS(ECC·repair·DRFM), 전력 효율(pJ/bit) 계산, 단수·die 밀도·용량 조합 설계, custom HBM(cHBM) 의 base die 기능 분담

## 4. 작업 지시 (우선순위 순)

0. **[최우선] 메타 지표 제거 — 194건** (`E_META_METRICS` 182, `W_META_METRICS` 12). 화면 '제시 조건' 띠에 "난이도: 고급", "묻는 것: 해당 항목", "세부 주제", "핵심어" 가 그대로 보인다(DA 스크린샷 확인). 지문 조건 2–4개로 바꾸거나, 요약할 조건이 없으면 `"metrics": []`(키는 유지). 정답 오류 수정과 같은 1순위로 처리한다.
1. **정답 오류·사실 정정 (W1 입력 §1A)**: NUM 정답 오류 확정·비현실 설정·그림 노출(`docs/reviews/num/PROD.md`), FACT 정정·사용 금지·조건부 주장(§1A 의 F 번호), XD 용어·중복·이관 지시(`docs/reviews/xd/PROD.md`), §2 의 기술 정정 후보, `E_EXP_REF_ANSWER`(정답 키 재검증). 메타 지표 제거(0번)와 함께 가장 먼저.
2. **템플릿 가족 정리**: `E_FAMILY_OVER` 대상은 가족당 3개(가능하면 난이도별 1개)만 남기고 삭제하거나 다른 판단을 묻도록 재작성. 근중복(`W_NEAR_DUP`)도 정리.
3. **ctx 조립형 정리**: ctx 가 qt 풀이에 필요 없으면 stem 단일형으로 변환. 기술 외 사유 오답·타 분야 오답(`W_OPT_WEAK`) 교체, 형식 단서(`W_OPT_ODD_END`, `W_OPT_LONGEST`, `W_OPT_ABSOLUTE`) 제거.
4. **해설 재작성**: `E_EXP_SHORT`·`E_EXP_ONLY_REFS`·`E_STYLE_PLAIN`·`W_EXP_DISTRACTORS` — 정답 근거 + 오답 3개 각각의 오류 + (계산) 식·대입·결과. 일괄 `[근거]` 꼬리표는 고친 해설에서 뺀다.
5. **제목·지표·그림**: `E_TITLE_TRUNC`·`W_TITLE_*` 제목 재작성, `E_META_METRICS` 지표를 지문 조건으로 교체, `E_K1_FIG_NUM`·`E_FIG_ANSWER_LEAK`·`E_FIG_INTERNAL`·`W_FIG_*` 그림 params 정정.
6. **난이도 재배치**: 단순 대입 계산·용어 문항이 고급이면 lv 를 내린다. lv 가 바뀌면 id 의 LV 도 달라져야 하므로 **새 id(`CODE-LV-9xxx`)를 발급하고 `"prev": "옛 id"` 필드를 남긴다**(보고서에 old→new 기록). 고급은 STANDARDS §1 기준으로 채운다.
7. **신규 출제**(§5) — 공백 주제 위주. 새 id 는 `PROD-LV-9001` 부터.
8. 타 분야 문항은 고쳐서 `"mv": "CODE"` 로 이관 제안(EA 가 Phase 2 에서 이동) 하거나 자기 분야 관점으로 재작성.

## 4A. DA Phase 1 템플릿 변경으로 손봐야 할 기존 문항

템플릿 기본값·규약이 바뀌어(LAYOUT_RULES §3–4, STANDARDS 부록 A) 아래 문항은 params 를 고치지 않으면 그림이 지문과 어긋나거나 답을 보여 준다.

- `E_FIG_HIDE_RESULT` **2건** — `hideResult: true` 추가 (그림이 계산·판정 결과를 표시). 입력 params 자체가 답이면(예: f_stack.n = 최대 단수) k=0 으로: PROD-B-0003, PROD-I-0001
- `W_METRIC_LEN` **3건** — 지표 label ≤ 12자 · value ≤ 16자: PROD-B-0001, PROD-I-0003, PROD-I-0004
- `W_OPT_LEN` **3건** — 보기 60자 이하로: PROD-A-0004, PROD-I-0004, PROD-I-0005

## 5. 추가 출제 목표

| | 초급 | 중급 | 고급 | 합계 |
|---|---|---|---|---|
| 신규 최소 | 10 | 35 | 45 | 90 |

- 가족 초과로 정리될 문항 약 22 건은 위 신규로 대체한다(수량 유지보다 질 우선, 최종 분야 규모는 ±10 % 허용).
- 최종 난이도 비율 권장: 초급 25–30 % · 중급 35–40 % · 고급 30–35 %.

- 고급: 목표 용량·대역폭·전력 예산을 동시에 만족하는 세대·단수·스택 수 선택(4변수), pJ/bit 와 대역폭으로 I/O 전력 추정 후 열 예산과 대조, 16-Hi 를 775 µm 에 넣는 두께 예산과 접합 방식 선택, base die 로직 공정 이전에 따른 기능·비용·열 트레이드오프
- 중급: 세대 간 채널·PC 구조 변화와 컨트롤러 영향, 용량 단위 환산, 패키지 높이 규격 변화의 공정 함의

## 6. 사용할 그림 템플릿과 params

| 템플릿 | params | 제약 · 주의 |
|---|---|---|
| `f_stack` | `n`(core die 수), `highlight`, `gap_um`, `h_um`, `limit_um`, `bullet`, `hideResult` | 계산 답을 `n`/`h_um` 에 넣지 말 것 |
| `f_plot` | `title`, `x`/`y`{min,max,ticks ≤ 6,lab}, `series` ≤ 4, `marks` ≤ 3, `bullets` ≤ 3 | 데이터 해석형 고급의 주력 |
| `f_note` | `title` ≤ 22자, `points` ≤ 4(각 ≤ 50자), `ask` ≤ 12자 | points 는 **판단 관점** — 정답 문장 금지 |
| `f_sip` | `type`: cowos-s·cowos-r·cowos-l·emib·emib-t, `nHBM` 1–8, **`lines`**, `bullet` | **`lines` 생략 시 숫자 없는 "HBM I/O 배선"**. 지문이 1,024 / 2,048 배선을 말하면 `lines` 를 그 값으로(E_FIG_SIP_LINES). HBM3E = 1024, HBM4 = 2048 |


- 수치는 STANDARDS 2.2 표 범위 안에서만 '확정 사실'로 쓴다. 업체 값은 `src` 에 [V] 출처를 남긴다.
- 데이터 해석형 고급에는 `f_table`(표)·`f_wafermap`(맵)·`f_plot`(그래프)을 쓴다(DA Phase 1 신설, 예시는 LAYOUT_RULES §4). 결과를 그림이 계산하는 템플릿은 `hideResult` 의무(STANDARDS 부록 A.1).

## 7. 완료 조건

- `python3 tools/validate.py --domain PROD --gate` 통과(차단 E 0). 남는 W 는 수정 또는 `vx` + 사유.
- `python3 tools/build.py` · `node tools/smoke.js dist/HBM_quiz.html` 오류 없음.
- 보고서 `docs/reviews/PROD.md` (형식: ROSTER §4).
