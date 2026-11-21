# SIP 분야 브리프 — SiP 조립 구조

- 소유 파일: `data/06_SIP.json` · 기준: `docs/agents/STANDARDS.md` · 자동 검사: `python3 tools/validate.py --domain SIP`
- 작성: EA (Phase 1, 2026-11-20) · 기준선 리포트: `docs/reviews/_auto_baseline.md`

## 0. 현황

| 난이도 | 문항 | stem 단일형 | ctx 조립형 | 정답 위치 ①/②/③/④ |
|---|---|---|---|---|
| 초급 | 175 | 66 | 109 | 50 / 40 / 40 / 45 |
| 중급 | 172 | 125 | 47 | 40 / 44 / 35 / 53 |
| 고급 | 190 | 141 | 49 | 52 / 48 / 48 / 42 |
| 합계 | 537 | 332 | 205 | |

- k=1 상황도 332 · k=0 주제도 205 · 그림 사용: f_stack 297, f_sip 236, f_warp 1, f_cmp 1, f_film 1, f_note 1
- **차단 E 이슈가 있는 문항: 494 / 537** (E_JOSA_CIRC 는 EA Phase 2 일괄 처리라 제외)

## 1. 자동 검사 요약 (기준선)

| 코드 | 건수 | 예시 id |
|---|---|---|
| `E_FIG_HIDE_RESULT` | 235 | SIP-A-0002, SIP-A-0003, SIP-A-0004, SIP-A-0005 |
| `E_META_METRICS` | 205 | SIP-A-0142, SIP-A-0143, SIP-A-0144, SIP-A-0145 |
| `E_FIG_ANSWER_LEAK` | 170 | SIP-A-0009, SIP-A-0013, SIP-A-0014, SIP-A-0015 |
| `E_STYLE_PLAIN` | 170 | SIP-A-0142, SIP-A-0143, SIP-A-0144, SIP-A-0145 |
| `E_EXP_SHORT` | 164 | SIP-A-0148, SIP-A-0149, SIP-A-0152, SIP-A-0153 |
| `E_JOSA_CIRC` | 161 | SIP-A-0142, SIP-A-0143, SIP-A-0144, SIP-A-0145 |
| `E_FAMILY_OVER` | 152 | SIP-A-0006, SIP-A-0007, SIP-A-0008, SIP-A-0009 |
| `E_TITLE_TRUNC` | 143 | SIP-A-0142, SIP-A-0143, SIP-A-0144, SIP-A-0145 |
| `E_EXP_ONLY_REFS` | 116 | SIP-A-0149, SIP-A-0153, SIP-A-0155, SIP-A-0156 |
| `E_K1_FIG_NUM` | 94 | SIP-A-0002, SIP-A-0003, SIP-A-0004, SIP-A-0005 |
| `E_JOSA_EN` | 38 | SIP-A-0003, SIP-A-0004, SIP-A-0005, SIP-A-0006 |
| `E_FIG_SIP_LINES` | 31 | SIP-B-0001, SIP-B-0003, SIP-B-0004, SIP-B-0005 |
| `E_DOUBLE_Q` | 8 | SIP-B-0067, SIP-B-0078, SIP-B-0129, SIP-B-0134 |
| `E_OPT_DUP` | 4 | SIP-A-0047, SIP-A-0064, SIP-A-0069, SIP-A-0070 |
| `E_EXP_REF_ANSWER` | 4 | SIP-A-0152, SIP-B-0133, SIP-I-0138, SIP-I-0161 |
| `E_CALC_NO_WORK` | 3 | SIP-B-0161, SIP-B-0163, SIP-B-0173 |
| `E_DUP_EXACT` | 2 | SIP-B-0019, SIP-B-0021 |
| `W_EXP_DISTRACTORS` | 290 | SIP-A-0002, SIP-A-0013, SIP-A-0014, SIP-A-0015 |
| `W_TITLE_COPY` | 205 | SIP-A-0142, SIP-A-0143, SIP-A-0144, SIP-A-0145 |
| `W_NEAR_DUP` | 204 | SIP-A-0080, SIP-A-0081, SIP-A-0082, SIP-A-0083 |
| `W_META_METRICS` | 112 | SIP-A-0043, SIP-A-0044, SIP-A-0045, SIP-A-0046 |
| `W_OPT_ODD_END` | 84 | SIP-A-0142, SIP-A-0144, SIP-A-0146, SIP-A-0157 |
| `W_K1_FIG_EXTRA` | 66 | SIP-A-0001, SIP-A-0003, SIP-A-0004, SIP-A-0005 |
| `W_TITLE_QUESTION` | 59 | SIP-A-0155, SIP-B-0068, SIP-B-0073, SIP-B-0075 |
| `W_OPT_WEAK` | 28 | SIP-A-0144, SIP-A-0146, SIP-A-0149, SIP-A-0156 |
| `W_OPT_LONGEST` | 16 | SIP-A-0073, SIP-A-0074, SIP-A-0075, SIP-A-0076 |
| `W_FIG_LEAK` | 10 | SIP-A-0003, SIP-A-0004, SIP-A-0005, SIP-A-0006 |
| `W_METRIC_LEN` | 8 | SIP-I-0003, SIP-I-0004, SIP-I-0007, SIP-I-0008 |
| `W_OPT_ABSOLUTE` | 7 | SIP-A-0150, SIP-A-0151, SIP-A-0163, SIP-A-0178 |
| `W_TITLE_LEN` | 6 | SIP-I-0007, SIP-I-0008, SIP-I-0009, SIP-I-0010 |
| `W_FIG_TOPIC` | 4 | SIP-A-0174, SIP-B-0135, SIP-I-0143, SIP-I-0146 |
| `W_OPT_STEM_ECHO` | 3 | SIP-I-0002, SIP-I-0005, SIP-I-0006 |
| `W_K1_METRIC_NUM` | 2 | SIP-A-0002, SIP-I-0014 |
| `W_OPT_LEN` | 2 | SIP-A-0073, SIP-A-0075 |
| `W_EXP_OFFTOPIC` | 2 | SIP-B-0094, SIP-B-0095 |
| `W_STEM_NO_QMARK` | 1 | SIP-B-0132 |
| `W_EXP_REF_MISMATCH` | 1 | SIP-B-0141 |
| `W_QT_LONG` | 1 | SIP-I-0136 |
| `I_FACT_WATCH` | 230 | SIP-A-0002, SIP-A-0013, SIP-A-0014, SIP-A-0015 |
| `I_EXP_SRC_TAG` | 226 | SIP-A-0073, SIP-A-0074, SIP-A-0075, SIP-A-0076 |

(참고: `I_JOSA_SPACE` 514 · `I_TEMPLATE_JOIN` 205 — 새로 쓰는 문장은 조사를 붙여 쓰고, ctx 조립형은 STANDARDS 3.1 에 따라 정리)

## 1A. W1 입력 (지원 에이전트 결과 — 작업 1순위)

- **NUM** `docs/reviews/num/SIP.md`: 검증 289 · 산술 일치 286 · **정답 오류 확정 7** · **비현실 설정 27** · 그림·지표 정답 노출 169 · 간극 규약 위반 0 · 근접 오답(<3 %) 30 · 회상형(FACT 이관) 6. 문항별 올바른 값·식은 해당 파일. solver: `tools/num/`.
- **FACT** `docs/reviews/_facts.md` — 이 분야 관련 주장 10건 (판정은 §1–7 표, 문항 id 는 §8):
  - **F11** [정정] SIP 문항의 "HBM 스택과 XPU 사이에는 2,048개의 데이터 선" (세대 미표기 — 31문항: SIP-B-0001, SIP-B-0003, SIP-B-0004, SIP-B-0005, SIP-B-0006, SIP-B-0007, SIP-B-0008, SIP-B-0009, SIP-B-0010, SIP-B-0011, SIP-B-0012, SIP-B-0013 …
  - **F12** [조건부] 720 µm = HBM 패키지 높이(8/12-Hi) — 56문항: SIP-A-0002, SIP-A-0013, SIP-A-0023, SIP-A-0044, SIP-A-0045, SIP-A-0047, SIP-A-0049, SIP-A-0050, SIP-A-0051, SIP-A-0052, SIP-A-0054, SIP-A-0055 …
  - **F13** [조건부] 775 µm = HBM4 패키지 높이 규격 상한(12·16-Hi), HBM3E 720  — 181문항: SIP-A-0002, SIP-A-0013, SIP-A-0014, SIP-A-0015, SIP-A-0016, SIP-A-0017, SIP-A-0018, SIP-A-0019, SIP-A-0020, SIP-A-0021, SIP-A-0022, SIP-A-0023 …
  - **F15** [정정] 해설 꼬리표 "Hot Chips 2026 SK hynix 발표 정리 (775 µm 한계 — 164문항: SIP-A-0078, SIP-A-0079, SIP-A-0080, SIP-A-0081, SIP-A-0082, SIP-A-0083, SIP-A-0084, SIP-A-0085, SIP-A-0086, SIP-A-0087, SIP-A-0088, SIP-A-0089 …
  - **F26** [조건부] SK hynix: 하이브리드 본딩은 20단 이상(≥20Hi) 에서 필요, HB 시 bu — 1문항: SIP-B-0173
  - **F34** [확인] reticle(1회 노광 면적) ≈ 26 × 33 mm = 858 mm²; CoWoS- — 59문항: SIP-A-0073, SIP-A-0074, SIP-A-0122, SIP-A-0123, SIP-A-0124, SIP-A-0125, SIP-A-0126, SIP-A-0127, SIP-A-0128, SIP-A-0129, SIP-A-0130, SIP-A-0131 …
  - **F35** [사용 금지] HBM 탑재 수: 전면 Si ≈ 8, 유기 RDL 4–6, 브리지 12개 이상 — 1문항: SIP-I-0015
  - **F36** [정정] CoWoS-R(유기 RDL 인터포저)은 die·기판과 팽창률 차이가 커서 접합 신뢰성이 — 4문항: SIP-A-0178, SIP-B-0138, SIP-I-0136, SIP-I-0145
  - **F37** [정정] 유기 RDL·브리지 구조는 "수직 통로가 없어" 전원이 기판을 돌아가거나 "기판이 담당 — 3문항: SIP-I-0013, SIP-I-0144, SIP-I-0146
  - **F38** [확인] CoWoS-S·-R·-L·EMIB·EMIB-T 구조 정의(Si 전면 인터포저+TSV / — 14문항: SIP-A-0074, SIP-B-0077, SIP-B-0134, SIP-B-0135, SIP-B-0136, SIP-B-0139, SIP-B-0140, SIP-B-0141, SIP-B-0142, SIP-B-0144, SIP-B-0155, SIP-I-0143 …
- **XD** `docs/reviews/xd/SIP.md` — 용어 규약 위반·교차 중복(보유/삭제)·이관(mv)·사실 충돌 지시. 요약은 `docs/reviews/xd/_index.md`.
- 처리 원칙: NUM 정답 오류·FACT '정정'/'사용 금지' 판정 → 해당 문항을 **가장 먼저** 고치거나 삭제. FACT '조건부' 는 지문 표현을 고치면 유지(예: "JEDEC 규격 상한 775 µm" → "높이 상한(설계 조건) 775 µm"). 판정과 다르게 처리하면 보고서에 근거.

## 2. 표본 조사로 확인한 대표 결함 (EA 직접 판독: 난이도별 10문항 이상)

- **스택 높이 계산 가족이 분야의 중심**(SIP-A-0013 계열 30, -0043 계열 30, 최대 단수·두께 역산 등): 높이 계산은 PROD/COW 와도 겹침. 가족 초과 152.
- **그림이 답을 노출(E_FIG_ANSWER_LEAK 170)**: 최대 단수 문항에서 `f_stack.n` 에 정답 단수, `h_um` 에 정답 높이(SIP-I-0028, -0042, -0021, SIP-A-0028, -0069). 그림 표가 die·간극·높이를 계산해 보여 준다.
- **보기 중복**: SIP-A-0069 "14장" 2회(정답 포함), SIP-A-0047, -0064, -0070.
- **2.5D 본연의 주제가 얕음**: CoWoS-S/R/L·EMIB 은 "설명에 해당하는 구조 고르기"(B) 위주, 중·고급은 거의 높이 계산. PDN·SI·interposer 배선·package warpage·underfill 0건.
- **사실 검증 필요**: SIP-I-0015 "전면 Si 8개, 유기 RDL 4~6개, 브리지 12개 이상" — 제품 사례(MI300X CoWoS-S 8 stack, B200 CoWoS-L 8 stack 등)와 대조 필요. '2,048선' 라벨이 HBM3E 문항에도 고정 표시.
- ctx 조립형 문항에 타 분야 주제 혼재(연삭 stress relief SIP-A-0142, warpage 측정 SIP-A-0148).

## 3. 핵심 개념 체크리스트와 현재 커버리지

키워드 기반 근사치(지문·보기·해설에서 해당 주제가 다뤄진 문항 수). 0–4 = **공백**, 5–14 = 부족, 15+ = 있음(질은 별도 판단).

| 주제 | 초급 | 중급 | 고급 | 판정 |
|---|---|---|---|---|
| CoWoS-S(Si interposer) | 36 | 4 | 2 | 있음 |
| CoWoS-R(RDL) | 29 | 8 | 3 | 있음 |
| CoWoS-L/LSI bridge | 24 | 3 | 2 | 있음 |
| EMIB/EMIB-T | 27 | 2 | 2 | 있음 |
| reticle 크기·stitching | 22 | 22 | 11 | 있음 |
| interposer 배선 L/S·PHY 거리 | 0 | 0 | 0 | **공백** |
| C4 bump·substrate | 66 | 44 | 22 | 있음 |
| PDN·decap(IR drop) | 0 | 0 | 1 | **공백** |
| SI(crosstalk·eye) | 0 | 0 | 0 | **공백** |
| CoW-oS vs CoC 조립 순서 | 13 | 8 | 3 | 있음 |
| package warpage·underfill | 0 | 0 | 0 | **공백** |
| 스택 높이·두께 예산 | 40 | 103 | 126 | 있음 |
| 3D(HBM-on-logic)·SoIC | 1 | 0 | 0 | **공백** |

**우선 보강 공백**: interposer 배선 L/S 와 PHY 간 거리(HBM–SoC 채널 길이), PDN(IR drop·decap·전원 TSV), SI(crosstalk·eye·채널 손실), package warpage 와 C4/BGA 접합, underfill, 조립 순서(CoW-first vs oS), 3D(HBM-on-logic, SoIC) 와 열 문제, HBM 탑재 수와 reticle 배수 관계의 실제 사례

## 4. 작업 지시 (우선순위 순)

0. **[최우선] 메타 지표 제거 — 317건** (`E_META_METRICS` 205, `W_META_METRICS` 112). 화면 '제시 조건' 띠에 "난이도: 고급", "묻는 것: 해당 항목", "세부 주제", "핵심어" 가 그대로 보인다(DA 스크린샷 확인). 지문 조건 2–4개로 바꾸거나, 요약할 조건이 없으면 `"metrics": []`(키는 유지). 정답 오류 수정과 같은 1순위로 처리한다.
1. **정답 오류·사실 정정 (W1 입력 §1A)**: NUM 정답 오류 확정·비현실 설정·그림 노출(`docs/reviews/num/SIP.md`), FACT 정정·사용 금지·조건부 주장(§1A 의 F 번호), XD 용어·중복·이관 지시(`docs/reviews/xd/SIP.md`), §2 의 기술 정정 후보, `E_EXP_REF_ANSWER`(정답 키 재검증). 메타 지표 제거(0번)와 함께 가장 먼저.
2. **템플릿 가족 정리**: `E_FAMILY_OVER` 대상은 가족당 3개(가능하면 난이도별 1개)만 남기고 삭제하거나 다른 판단을 묻도록 재작성. 근중복(`W_NEAR_DUP`)도 정리.
3. **ctx 조립형 정리**: ctx 가 qt 풀이에 필요 없으면 stem 단일형으로 변환. 기술 외 사유 오답·타 분야 오답(`W_OPT_WEAK`) 교체, 형식 단서(`W_OPT_ODD_END`, `W_OPT_LONGEST`, `W_OPT_ABSOLUTE`) 제거.
4. **해설 재작성**: `E_EXP_SHORT`·`E_EXP_ONLY_REFS`·`E_STYLE_PLAIN`·`W_EXP_DISTRACTORS` — 정답 근거 + 오답 3개 각각의 오류 + (계산) 식·대입·결과. 일괄 `[근거]` 꼬리표는 고친 해설에서 뺀다.
5. **제목·지표·그림**: `E_TITLE_TRUNC`·`W_TITLE_*` 제목 재작성, `E_META_METRICS` 지표를 지문 조건으로 교체, `E_K1_FIG_NUM`·`E_FIG_ANSWER_LEAK`·`E_FIG_INTERNAL`·`W_FIG_*` 그림 params 정정.
6. **난이도 재배치**: 단순 대입 계산·용어 문항이 고급이면 lv 를 내린다. lv 가 바뀌면 id 의 LV 도 달라져야 하므로 **새 id(`CODE-LV-9xxx`)를 발급하고 `"prev": "옛 id"` 필드를 남긴다**(보고서에 old→new 기록). 고급은 STANDARDS §1 기준으로 채운다.
7. **신규 출제**(§5) — 공백 주제 위주. 새 id 는 `SIP-LV-9001` 부터.
8. 타 분야 문항은 고쳐서 `"mv": "CODE"` 로 이관 제안(EA 가 Phase 2 에서 이동) 하거나 자기 분야 관점으로 재작성.

## 4A. DA Phase 1 템플릿 변경으로 손봐야 할 기존 문항

템플릿 기본값·규약이 바뀌어(LAYOUT_RULES §3–4, STANDARDS 부록 A) 아래 문항은 params 를 고치지 않으면 그림이 지문과 어긋나거나 답을 보여 준다.

- `E_FIG_HIDE_RESULT` **235건** — `hideResult: true` 추가 (그림이 계산·판정 결과를 표시). 입력 params 자체가 답이면(예: f_stack.n = 최대 단수) k=0 으로: SIP-A-0002, SIP-A-0003, SIP-A-0004, SIP-A-0005, SIP-A-0006, SIP-A-0007, SIP-A-0008, SIP-A-0009, SIP-A-0010, SIP-A-0011, SIP-A-0012, SIP-A-0013, SIP-A-0014, SIP-A-0015, SIP-A-0016, SIP-A-0017, SIP-A-0018, SIP-A-0019, SIP-A-0020, SIP-A-0021, SIP-A-0022, SIP-A-0023, SIP-A-0024, SIP-A-0025, SIP-A-0026, SIP-A-0027, SIP-A-0028, SIP-A-0029, SIP-A-0030, SIP-A-0031, SIP-A-0032, SIP-A-0033, SIP-A-0034, SIP-A-0035, SIP-A-0036, SIP-A-0037, SIP-A-0038, SIP-A-0039, SIP-A-0040, SIP-A-0041, SIP-A-0042, SIP-A-0043, SIP-A-0044, SIP-A-0045, SIP-A-0046, SIP-A-0047, SIP-A-0048, SIP-A-0049, SIP-A-0050, SIP-A-0051, SIP-A-0052, SIP-A-0053, SIP-A-0054, SIP-A-0055, SIP-A-0056, SIP-A-0057, SIP-A-0058, SIP-A-0059, SIP-A-0060, SIP-A-0061, SIP-A-0062, SIP-A-0063, SIP-A-0064, SIP-A-0065, SIP-A-0066, SIP-A-0067, SIP-A-0068, SIP-A-0069, SIP-A-0070, SIP-A-0071, SIP-A-0072, SIP-A-0078, SIP-A-0079, SIP-A-0080, SIP-A-0081, SIP-A-0082, SIP-A-0083, SIP-A-0084, SIP-A-0085, SIP-A-0086, SIP-A-0087, SIP-A-0088, SIP-A-0089, SIP-A-0090, SIP-A-0091, SIP-A-0092, SIP-A-0093, SIP-A-0094, SIP-A-0095, SIP-A-0096, SIP-A-0097, SIP-A-0098, SIP-A-0099, SIP-A-0100, SIP-A-0101, SIP-A-0102, SIP-A-0103, SIP-A-0104, SIP-A-0105, SIP-A-0106, SIP-A-0107, SIP-A-0108, SIP-A-0109, SIP-A-0110, SIP-A-0111, SIP-A-0112, SIP-A-0113, SIP-A-0114, SIP-A-0115, SIP-A-0116, SIP-A-0117, SIP-A-0118, SIP-A-0119, SIP-A-0120, SIP-A-0121, SIP-A-0132, SIP-A-0133, SIP-A-0134, SIP-A-0135, SIP-A-0136, SIP-A-0137, SIP-A-0138, SIP-A-0139, SIP-A-0140, SIP-A-0141, SIP-B-0045, SIP-B-0046, SIP-B-0047, SIP-B-0048, SIP-B-0049, SIP-B-0050, SIP-B-0051, SIP-B-0052, SIP-B-0053, SIP-B-0054, SIP-B-0055, SIP-B-0056, SIP-B-0057, SIP-B-0058, SIP-B-0059, SIP-B-0060, SIP-B-0061, SIP-B-0062, SIP-B-0063, SIP-B-0064, SIP-B-0065, SIP-B-0066, SIP-I-0016, SIP-I-0017, SIP-I-0018, SIP-I-0019, SIP-I-0020, SIP-I-0021, SIP-I-0022, SIP-I-0023, SIP-I-0024, SIP-I-0025, SIP-I-0026, SIP-I-0027, SIP-I-0028, SIP-I-0029, SIP-I-0030, SIP-I-0031, SIP-I-0032, SIP-I-0033, SIP-I-0034, SIP-I-0035, SIP-I-0036, SIP-I-0037, SIP-I-0038, SIP-I-0039, SIP-I-0040, SIP-I-0041, SIP-I-0042, SIP-I-0043, SIP-I-0044, SIP-I-0045, SIP-I-0046, SIP-I-0047, SIP-I-0048, SIP-I-0049, SIP-I-0050, SIP-I-0051, SIP-I-0052, SIP-I-0053, SIP-I-0054, SIP-I-0055, SIP-I-0056, SIP-I-0057, SIP-I-0058, SIP-I-0059, SIP-I-0060, SIP-I-0061, SIP-I-0062, SIP-I-0063, SIP-I-0064, SIP-I-0065, SIP-I-0066, SIP-I-0067, SIP-I-0068, SIP-I-0069, SIP-I-0070, SIP-I-0071, SIP-I-0072, SIP-I-0073, SIP-I-0074, SIP-I-0075, SIP-I-0076, SIP-I-0077, SIP-I-0078, SIP-I-0079, SIP-I-0080, SIP-I-0081, SIP-I-0104, SIP-I-0105, SIP-I-0106, SIP-I-0107, SIP-I-0108, SIP-I-0109, SIP-I-0110, SIP-I-0111, SIP-I-0112, SIP-I-0113, SIP-I-0114, SIP-I-0115, SIP-I-0116, SIP-I-0117, SIP-I-0118, SIP-I-0119, SIP-I-0120, SIP-I-0121, SIP-I-0122, SIP-I-0123, SIP-I-0124, SIP-I-0125
- `E_FIG_SIP_LINES` **31건** — `f_sip` 에 `lines` 추가 (기본값이 '숫자 없는 HBM I/O 배선' 으로 바뀜; 지문의 1,024/2,048 과 일치): SIP-B-0001, SIP-B-0003, SIP-B-0004, SIP-B-0005, SIP-B-0006, SIP-B-0007, SIP-B-0008, SIP-B-0009, SIP-B-0010, SIP-B-0011, SIP-B-0012, SIP-B-0013, SIP-B-0014, SIP-B-0015, SIP-B-0016, SIP-B-0017, SIP-B-0018, SIP-B-0019, SIP-B-0020, SIP-B-0021, SIP-B-0022, SIP-I-0003, SIP-I-0004, SIP-I-0005, SIP-I-0006, SIP-I-0007, SIP-I-0008, SIP-I-0009, SIP-I-0010, SIP-I-0011, SIP-I-0012
- `W_QT_LONG` **1건** — 질문 마지막 문장 90자 이하로: SIP-I-0136
- `W_METRIC_LEN` **8건** — 지표 label ≤ 12자 · value ≤ 16자: SIP-I-0003, SIP-I-0004, SIP-I-0007, SIP-I-0008, SIP-I-0009, SIP-I-0010, SIP-I-0011, SIP-I-0012
- `W_OPT_LEN` **2건** — 보기 60자 이하로: SIP-A-0073, SIP-A-0075

## 5. 추가 출제 목표

| | 초급 | 중급 | 고급 | 합계 |
|---|---|---|---|---|
| 신규 최소 | 10 | 30 | 30 | 70 |

- 가족 초과로 정리될 문항 약 152 건은 위 신규로 대체한다(수량 유지보다 질 우선, 최종 분야 규모는 ±10 % 허용).
- 최종 난이도 비율 권장: 초급 25–30 % · 중급 35–40 % · 고급 30–35 %.

- 고급: reticle 배수·HBM 수·SoC 면적 동시 만족 배치(면적·배선 길이·수율 3변수), interposer 배선 저항·커패시턴스로 신호 지연/전력 추정, PDN 경로(CoWoS-S TSV vs CoWoS-R substrate 경유) 비교 판단, package warpage 데이터로 C4 non-wet 위치 예측
- 중급: CoWoS-S/R/L/EMIB-T 의 전원 경로 차이, underfill 역할, 조립 순서별 위험

## 6. 사용할 그림 템플릿과 params

| 템플릿 | params | 제약 · 주의 |
|---|---|---|
| `f_sip` | `type`: cowos-s·cowos-r·cowos-l·emib·emib-t, `nHBM` 1–8, **`lines`**, `bullet` | **`lines` 생략 시 숫자 없는 "HBM I/O 배선"**. 지문이 1,024 / 2,048 배선을 말하면 `lines` 를 그 값으로(E_FIG_SIP_LINES). HBM3E = 1024, HBM4 = 2048 |
| `f_stack` | `n`(core die 수), `highlight`, `gap_um`, `h_um`, `limit_um`, `bullet`, `hideResult` | 계산 답을 `n`/`h_um` 에 넣지 말 것 |
| `f_plot` | `title`, `x`/`y`{min,max,ticks ≤ 6,lab}, `series` ≤ 4, `marks` ≤ 3, `bullets` ≤ 3 | 데이터 해석형 고급의 주력 |
| `f_note` | `title` ≤ 22자, `points` ≤ 4(각 ≤ 50자), `ask` ≤ 12자 | points 는 **판단 관점** — 정답 문장 금지 |


- 높이 계산은 **입력 조건만 그림에** (n·h_um 에 답 금지). 높이 가족은 3개만 유지하고 나머지는 위 공백 주제로 대체.
- 데이터 해석형 고급에는 `f_table`(표)·`f_wafermap`(맵)·`f_plot`(그래프)을 쓴다(DA Phase 1 신설, 예시는 LAYOUT_RULES §4). 결과를 그림이 계산하는 템플릿은 `hideResult` 의무(STANDARDS 부록 A.1).

## 7. 완료 조건

- `python3 tools/validate.py --domain SIP --gate` 통과(차단 E 0). 남는 W 는 수정 또는 `vx` + 사유.
- `python3 tools/build.py` · `node tools/smoke.js dist/HBM_quiz.html` 오류 없음.
- 보고서 `docs/reviews/SIP.md` (형식: ROSTER §4).
