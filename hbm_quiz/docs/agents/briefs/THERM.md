# THERM 분야 브리프 — 열 설계와 방열

- 소유 파일: `data/13_THERM.json` · 기준: `docs/agents/STANDARDS.md` · 자동 검사: `python3 tools/validate.py --domain THERM`
- 작성: EA (Phase 1, 2026-11-20) · 기준선 리포트: `docs/reviews/_auto_baseline.md`

## 0. 현황

| 난이도 | 문항 | stem 단일형 | ctx 조립형 | 정답 위치 ①/②/③/④ |
|---|---|---|---|---|
| 초급 | 84 | 44 | 40 | 24 / 20 / 12 / 28 |
| 중급 | 234 | 209 | 25 | 56 / 63 / 56 / 59 |
| 고급 | 219 | 166 | 53 | 66 / 55 / 52 / 46 |
| 합계 | 537 | 419 | 118 | |

- k=1 상황도 419 · k=0 주제도 118 · 그림 사용: f_therm 468, f_sip 55, f_bond 10, f_hcb 2, f_stack 1, f_note 1
- **차단 E 이슈가 있는 문항: 489 / 537** (E_JOSA_CIRC 는 EA Phase 2 일괄 처리라 제외)

## 1. 자동 검사 요약 (기준선)

| 코드 | 건수 | 예시 id |
|---|---|---|
| `E_FIG_HIDE_RESULT` | 251 | WARP-A-0002, WARP-A-0003, WARP-A-0004, WARP-A-0005 |
| `E_K1_FIG_NUM` | 242 | WARP-A-0002, WARP-A-0033, WARP-A-0034, WARP-A-0035 |
| `E_FAMILY_OVER` | 189 | WARP-A-0006, WARP-A-0007, WARP-A-0008, WARP-A-0009 |
| `E_META_METRICS` | 118 | WARP-A-0178, WARP-A-0179, WARP-A-0181, WARP-A-0194 |
| `E_JOSA_CIRC` | 94 | WARP-A-0178, WARP-A-0179, WARP-A-0181, WARP-A-0194 |
| `E_TITLE_TRUNC` | 88 | WARP-A-0178, WARP-A-0179, WARP-A-0181, WARP-A-0194 |
| `E_EXP_SHORT` | 88 | WARP-A-0208, WARP-A-0209, WARP-A-0210, WARP-A-0211 |
| `E_STYLE_PLAIN` | 84 | WARP-A-0178, WARP-A-0179, WARP-A-0181, WARP-A-0194 |
| `E_EXP_ONLY_REFS` | 64 | WARP-A-0209, WARP-A-0210, WARP-A-0212, WARP-A-0213 |
| `E_JOSA_EN` | 15 | WARP-A-0002, WARP-A-0198, WARP-A-0207, WARP-A-0278 |
| `E_EXP_REF_ANSWER` | 3 | WARP-A-0267, WARP-I-0284, WARP-I-0285 |
| `E_FIG_ANSWER_LEAK` | 2 | WARP-A-0039, WARP-I-0207 |
| `E_TEXT_DUP_PAREN` | 2 | WARP-B-0074 |
| `E_CALC_NO_WORK` | 1 | WARP-A-0057 |
| `E_DOUBLE_Q` | 1 | WARP-B-0121 |
| `W_EXP_DISTRACTORS` | 353 | WARP-A-0001, WARP-A-0003, WARP-A-0004, WARP-A-0005 |
| `W_K1_FIG_EXTRA` | 343 | WARP-A-0001, WARP-A-0002, WARP-A-0050, WARP-A-0051 |
| `W_META_METRICS` | 310 | WARP-A-0050, WARP-A-0052, WARP-A-0053, WARP-A-0054 |
| `W_NEAR_DUP` | 271 | WARP-A-0060, WARP-A-0061, WARP-A-0062, WARP-A-0063 |
| `W_K1_METRIC_NUM` | 179 | WARP-A-0001, WARP-A-0002, WARP-A-0003, WARP-A-0004 |
| `W_TITLE_COPY` | 118 | WARP-A-0178, WARP-A-0179, WARP-A-0181, WARP-A-0194 |
| `W_OPT_ODD_END` | 49 | WARP-A-0196, WARP-A-0207, WARP-A-0208, WARP-A-0217 |
| `W_TITLE_QUESTION` | 30 | WARP-A-0210, WARP-A-0261, WARP-A-0275, WARP-B-0080 |
| `W_OPT_LONGEST` | 20 | WARP-A-0050, WARP-A-0052, WARP-A-0053, WARP-A-0054 |
| `W_OPT_WEAK` | 15 | WARP-A-0179, WARP-A-0195, WARP-A-0220, WARP-A-0232 |
| `W_OPT_ABSOLUTE` | 9 | WARP-A-0057, WARP-A-0220, WARP-A-0221, WARP-A-0249 |
| `W_FIG_LEAK` | 5 | WARP-A-0002, WARP-I-0027, WARP-I-0028, WARP-I-0029 |
| `W_OPT_LEN` | 4 | WARP-A-0055, WARP-A-0057, WARP-A-0058, WARP-I-0055 |
| `W_EXP_OFFTOPIC` | 3 | WARP-A-0181, WARP-A-0195, WARP-B-0085 |
| `W_FIG_TOPIC` | 1 | WARP-B-0139 |
| `W_OPT_PUNCT` | 1 | WARP-A-0220 |
| `W_QT_LONG` | 1 | WARP-A-0220 |
| `I_EXP_SRC_TAG` | 341 | WARP-A-0050, WARP-A-0051, WARP-A-0052, WARP-A-0053 |

(참고: `I_JOSA_SPACE` 483 · `I_TEMPLATE_JOIN` 118 — 새로 쓰는 문장은 조사를 붙여 쓰고, ctx 조립형은 STANDARDS 3.1 에 따라 정리)

## 1A. W1 입력 (지원 에이전트 결과 — 작업 1순위)

- **NUM** `docs/reviews/num/THERM.md`: 검증 401 · 산술 일치 401 · **정답 오류 확정 0** · **비현실 설정 45** · 그림·지표 정답 노출 45 · 간극 규약 위반 47 · 근접 오답(<3 %) 6 · 회상형(FACT 이관) 2. 문항별 올바른 값·식은 해당 파일. solver: `tools/num/`.
- **FACT** `docs/reviews/_facts.md` — 이 분야 관련 주장 3건 (판정은 §1–7 표, 문항 id 는 §8):
  - **F15** [정정] 해설 꼬리표 "Hot Chips 2026 SK hynix 발표 정리 (775 µm 한계 — 3문항: WARP-A-0055, WARP-A-0056, WARP-I-0059
  - **F25** [확인] SK hynix iHBM: ICE(전기 절연·고열전도 Si 계 소재)를 D2D PHY  — 7문항: WARP-A-0056, WARP-B-0149, WARP-B-0150, WARP-B-0151, WARP-B-0152, WARP-B-0153, WARP-B-0154
  - **F44** [사용 금지] "보고된 HBM 스택의 열유속 범위 15–25 W/cm²" — 55문항: WARP-A-0103, WARP-A-0104, WARP-A-0105, WARP-A-0106, WARP-A-0107, WARP-A-0108, WARP-A-0109, WARP-A-0110, WARP-A-0111, WARP-A-0112, WARP-B-0019, WARP-B-0020 …
- **XD** `docs/reviews/xd/THERM.md` — 용어 규약 위반·교차 중복(보유/삭제)·이관(mv)·사실 충돌 지시. 요약은 `docs/reviews/xd/_index.md`.
- 처리 원칙: NUM 정답 오류·FACT '정정'/'사용 금지' 판정 → 해당 문항을 **가장 먼저** 고치거나 삭제. FACT '조건부' 는 지문 표현을 고치면 유지(예: "JEDEC 규격 상한 775 µm" → "높이 상한(설계 조건) 775 µm"). 판정과 다르게 처리하면 보고서에 근거.

## 2. 표본 조사로 확인한 대표 결함 (EA 직접 판독: 난이도별 10문항 이상)

- **W0.5 분할로 신설**: `data/05_WARP.json` 에서 537문항 이관(id 는 `WARP-LV-NNNN` 그대로 유지, 파일의 `legacy_prefix: ["WARP"]`). **새 문항은 `THERM-LV-9001` 부터.**
- **가족 초과가 분야의 대부분**: 1D 열저항 누적(WARP-A-0003 계열 30, -0033 계열 17), 열유속→총 발열(WARP-I-0031 계열 24), W/cm² 환산, TIM 두께, 열 전용 TSV 저항 감소, 냉각수 예산, 면적 열저항 계면 ΔT. 대부분 단일 대입인데 고급에 배치.
- **비현실적 결과**: 최하단 die 154 / 236 / 397 °C 보기를 정답으로 둔 문항(WARP-A-0031, -0032). 원인은 "균일 열유속이 모든 간극을 통과" 모델 + 과대 열유속 + 과대 bond 열저항. **"최상단 95 °C 유지, 상한 85 °C"(WARP-A-0031)처럼 조건 자체가 이미 상한 초과**인 문항도 있다. STANDARDS 2.4 범위로 재설계(결과 ≈ 110 °C 이하).
- **용어 위반**: "12단 → 간극은 die 수보다 하나 적은 11개"(WARP-A-0003 계열) — 확정 규약은 **N단 = core N + base 1, 간극 N**. `f_therm.n` 은 base 포함 총 die 수이므로 N단이면 n = N+1.
- **검증 안 된 주장**: 열유속 가족 해설의 "보고된 HBM 스택 열유속 15~25 W/cm²"(WARP-B-0039 등), iHBM ICE(WARP-B-0150), 13 × 12.8 mm 스택 면적·0.35 W/mm²(→ 58 W/스택) 같은 설정값 — FACT 판정 전 사용 금지, 현실 범위로.
- **그림**: 열 계산 문항 다수가 `f_therm` 기본 층 구성(Si 30 / BEOL 6 / bond 9)을 지문과 다르게 그림(E_K1_FIG_NUM 다수). TIM·냉각수·계면 ΔT 문항처럼 적층 온도 분포와 무관한 문항에도 f_therm 을 붙임 → `f_plot`/`f_note` 로 교체하거나 지문 조건으로 그림.
- `f_sip` 55문항이 함께 이관됨(패키지 열 관점 문항) — SIP 와 중복 여부는 XD 판정.
- 타 분야 혼재: "HBM 공급 확대가 어려운 이유"(WARP-B-0088), "전류가 흐르면 열이 나는 이유"(WARP-B-0118) 등 → 삭제 또는 `mv`.

## 3. 핵심 개념 체크리스트와 현재 커버리지

키워드 기반 근사치(지문·보기·해설에서 해당 주제가 다뤄진 문항 수). 0–4 = **공백**, 5–14 = 부족, 15+ = 있음(질은 별도 판단).

| 주제 | 초급 | 중급 | 고급 | 판정 |
|---|---|---|---|---|
| 1D 열저항·층별 ΔT | 3 | 162 | 158 | 있음 |
| TIM·lid·cold plate | 48 | 139 | 73 | 있음 |
| 열유속·전력 밀도 | 22 | 80 | 80 | 있음 |
| N단↔간극 수 규약(base 포함) | 0 | 6 | 51 | 있음 |
| base die hotspot·로직 발열 분포 | 0 | 1 | 2 | **공백** |
| DRAM 온도와 refresh(85/95 °C) | 2 | 3 | 50 | 있음 |
| thermal TSV/dummy bump | 0 | 32 | 23 | 있음 |
| 접합층(NCF/MUF/HCB) 열전도 비교 | 2 | 3 | 2 | 부족 |
| 직렬·병렬 저항 네트워크 | 1 | 32 | 31 | 있음 |
| 냉각 방식(액냉·cold plate) 예산 | 44 | 79 | 46 | 있음 |
| 2.5D 패키지 내 HBM–SoC 열 간섭 | 0 | 0 | 3 | **공백** |

**우선 보강 공백**: base die(로직) 발열 분포·hotspot 과 1D 균일 열유속 모델의 한계, 각 die 발열이 누적되는 모델(아래쪽일수록 통과 열량 증가), 접합 방식별(TC-NCF / MR-MUF / HCB) 계면 열저항 비교, 2.5D 에서 SoC 발열이 HBM 에 주는 열 간섭, 85/95 °C 와 refresh 배수·성능 영향, 액냉·cold plate 열저항 예산, thermal dummy bump/TSV 의 면적 대비 효과

## 4. 작업 지시 (우선순위 순)

0. **[최우선] 메타 지표 제거 — 428건** (`E_META_METRICS` 118, `W_META_METRICS` 310). 화면 '제시 조건' 띠에 "난이도: 고급", "묻는 것: 해당 항목", "세부 주제", "핵심어" 가 그대로 보인다(DA 스크린샷 확인). 지문 조건 2–4개로 바꾸거나, 요약할 조건이 없으면 `"metrics": []`(키는 유지). 정답 오류 수정과 같은 1순위로 처리한다.
1. **정답 오류·사실 정정 (W1 입력 §1A)**: NUM 정답 오류 확정·비현실 설정·그림 노출(`docs/reviews/num/THERM.md`), FACT 정정·사용 금지·조건부 주장(§1A 의 F 번호), XD 용어·중복·이관 지시(`docs/reviews/xd/THERM.md`), §2 의 기술 정정 후보, `E_EXP_REF_ANSWER`(정답 키 재검증). 메타 지표 제거(0번)와 함께 가장 먼저.
2. **템플릿 가족 정리**: `E_FAMILY_OVER` 대상은 가족당 3개(가능하면 난이도별 1개)만 남기고 삭제하거나 다른 판단을 묻도록 재작성. 근중복(`W_NEAR_DUP`)도 정리.
3. **ctx 조립형 정리**: ctx 가 qt 풀이에 필요 없으면 stem 단일형으로 변환. 기술 외 사유 오답·타 분야 오답(`W_OPT_WEAK`) 교체, 형식 단서(`W_OPT_ODD_END`, `W_OPT_LONGEST`, `W_OPT_ABSOLUTE`) 제거.
4. **해설 재작성**: `E_EXP_SHORT`·`E_EXP_ONLY_REFS`·`E_STYLE_PLAIN`·`W_EXP_DISTRACTORS` — 정답 근거 + 오답 3개 각각의 오류 + (계산) 식·대입·결과. 일괄 `[근거]` 꼬리표는 고친 해설에서 뺀다.
5. **제목·지표·그림**: `E_TITLE_TRUNC`·`W_TITLE_*` 제목 재작성, `E_META_METRICS` 지표를 지문 조건으로 교체, `E_K1_FIG_NUM`·`E_FIG_ANSWER_LEAK`·`E_FIG_INTERNAL`·`W_FIG_*` 그림 params 정정.
6. **난이도 재배치**: 단순 대입 계산·용어 문항이 고급이면 lv 를 내린다. lv 가 바뀌면 id 의 LV 도 달라져야 하므로 **새 id(`CODE-LV-9xxx`)를 발급하고 `"prev": "옛 id"` 필드를 남긴다**(보고서에 old→new 기록). 고급은 STANDARDS §1 기준으로 채운다.
7. **신규 출제**(§5) — 공백 주제 위주. 새 id 는 `THERM-LV-9001` 부터.
8. 타 분야 문항은 고쳐서 `"mv": "CODE"` 로 이관 제안(EA 가 Phase 2 에서 이동) 하거나 자기 분야 관점으로 재작성.

## 4A. DA Phase 1 템플릿 변경으로 손봐야 할 기존 문항

템플릿 기본값·규약이 바뀌어(LAYOUT_RULES §3–4, STANDARDS 부록 A) 아래 문항은 params 를 고치지 않으면 그림이 지문과 어긋나거나 답을 보여 준다.

- `E_FIG_HIDE_RESULT` **251건** — `hideResult: true` 추가 (그림이 계산·판정 결과를 표시). 입력 params 자체가 답이면(예: f_stack.n = 최대 단수) k=0 으로: WARP-A-0002, WARP-A-0003, WARP-A-0004, WARP-A-0005, WARP-A-0006, WARP-A-0007, WARP-A-0008, WARP-A-0009, WARP-A-0010, WARP-A-0011, WARP-A-0012, WARP-A-0013, WARP-A-0014, WARP-A-0015, WARP-A-0016, WARP-A-0017, WARP-A-0018, WARP-A-0019, WARP-A-0020, WARP-A-0021, WARP-A-0022, WARP-A-0023, WARP-A-0024, WARP-A-0025, WARP-A-0026, WARP-A-0027, WARP-A-0028, WARP-A-0029, WARP-A-0030, WARP-A-0031, WARP-A-0032, WARP-A-0051, WARP-A-0052, WARP-A-0057, WARP-A-0059, WARP-A-0060, WARP-A-0061, WARP-A-0062, WARP-A-0063, WARP-A-0064, WARP-A-0065, WARP-A-0066, WARP-A-0067, WARP-A-0068, WARP-A-0069, WARP-A-0070, WARP-A-0071, WARP-A-0072, WARP-A-0073, WARP-A-0074, WARP-A-0075, WARP-A-0076, WARP-A-0077, WARP-A-0078, WARP-A-0079, WARP-A-0080, WARP-A-0081, WARP-A-0082, WARP-A-0083, WARP-A-0084, WARP-A-0085, WARP-A-0086, WARP-A-0087, WARP-A-0088, WARP-A-0089, WARP-A-0090, WARP-A-0091, WARP-A-0092, WARP-A-0093, WARP-A-0094, WARP-A-0095, WARP-A-0096, WARP-A-0097, WARP-A-0098, WARP-A-0099, WARP-A-0100, WARP-A-0101, WARP-A-0102, WARP-A-0113, WARP-A-0114, WARP-A-0115, WARP-A-0116, WARP-A-0117, WARP-A-0118, WARP-A-0119, WARP-A-0120, WARP-A-0121, WARP-A-0122, WARP-A-0123, WARP-A-0124, WARP-A-0125, WARP-A-0126, WARP-A-0127, WARP-A-0128, WARP-A-0129, WARP-A-0130, WARP-A-0131, WARP-A-0132, WARP-A-0133, WARP-A-0134, WARP-A-0145, WARP-A-0146, WARP-A-0147, WARP-A-0148, WARP-A-0149, WARP-A-0150, WARP-A-0151, WARP-A-0152, WARP-A-0153, WARP-A-0154, WARP-A-0155, WARP-A-0156, WARP-A-0157, WARP-A-0158, WARP-A-0159, WARP-A-0160, WARP-A-0161, WARP-A-0162, WARP-A-0163, WARP-A-0164, WARP-A-0165, WARP-A-0166, WARP-I-0057, WARP-I-0063, WARP-I-0064, WARP-I-0065, WARP-I-0066, WARP-I-0067, WARP-I-0068, WARP-I-0069, WARP-I-0070, WARP-I-0071, WARP-I-0072, WARP-I-0073, WARP-I-0074, WARP-I-0075, WARP-I-0076, WARP-I-0077, WARP-I-0078, WARP-I-0079, WARP-I-0080, WARP-I-0081, WARP-I-0082, WARP-I-0083, WARP-I-0084, WARP-I-0085, WARP-I-0086, WARP-I-0087, WARP-I-0088, WARP-I-0089, WARP-I-0090, WARP-I-0091, WARP-I-0092, WARP-I-0093, WARP-I-0094, WARP-I-0095, WARP-I-0096, WARP-I-0097, WARP-I-0098, WARP-I-0099, WARP-I-0100, WARP-I-0101, WARP-I-0102, WARP-I-0103, WARP-I-0104, WARP-I-0105, WARP-I-0106, WARP-I-0107, WARP-I-0108, WARP-I-0109, WARP-I-0110, WARP-I-0111, WARP-I-0112, WARP-I-0113, WARP-I-0114, WARP-I-0115, WARP-I-0116, WARP-I-0117, WARP-I-0118, WARP-I-0119, WARP-I-0120, WARP-I-0121, WARP-I-0122, WARP-I-0123, WARP-I-0124, WARP-I-0125, WARP-I-0126, WARP-I-0149, WARP-I-0150, WARP-I-0151, WARP-I-0152, WARP-I-0153, WARP-I-0154, WARP-I-0155, WARP-I-0156, WARP-I-0157, WARP-I-0158, WARP-I-0159, WARP-I-0160, WARP-I-0161, WARP-I-0162, WARP-I-0163, WARP-I-0164, WARP-I-0165, WARP-I-0166, WARP-I-0167, WARP-I-0168, WARP-I-0169, WARP-I-0170, WARP-I-0171, WARP-I-0172, WARP-I-0173, WARP-I-0174, WARP-I-0175, WARP-I-0176, WARP-I-0177, WARP-I-0178, WARP-I-0179, WARP-I-0180, WARP-I-0203, WARP-I-0204, WARP-I-0205, WARP-I-0206, WARP-I-0207, WARP-I-0208, WARP-I-0209, WARP-I-0210, WARP-I-0211, WARP-I-0212, WARP-I-0213, WARP-I-0214, WARP-I-0215, WARP-I-0216, WARP-I-0217, WARP-I-0218, WARP-I-0219, WARP-I-0220, WARP-I-0221, WARP-I-0222, WARP-I-0223, WARP-I-0224, WARP-I-0225, WARP-I-0226, WARP-I-0227, WARP-I-0228, WARP-I-0229, WARP-I-0230, WARP-I-0231, WARP-I-0232, WARP-I-0233, WARP-I-0234
- `W_QT_LONG` **1건** — 질문 마지막 문장 90자 이하로: WARP-A-0220
- `W_OPT_LEN` **4건** — 보기 60자 이하로: WARP-A-0055, WARP-A-0057, WARP-A-0058, WARP-I-0055

## 5. 추가 출제 목표

| | 초급 | 중급 | 고급 | 합계 |
|---|---|---|---|---|
| 신규 최소 | 10 | 25 | 40 | 75 |

- 가족 초과로 정리될 문항 약 189 건은 위 신규로 대체한다(수량 유지보다 질 우선, 최종 분야 규모는 ±10 % 허용).
- 최종 난이도 비율 권장: 초급 25–30 % · 중급 35–40 % · 고급 30–35 %.

- 고급: die 별 발열이 누적되는 열 모델로 최하단 온도 추정(균일 q 모델과 비교 판단), HCB 전환 시 계면 열저항 감소 → 허용 단수·전력 추정, SoC 인접 거리·전력에 따른 HBM 온도 상승과 refresh 구간 진입 판단, TIM–lid–cold plate 직렬 예산 배분(3개 이상 저항), thermal dummy bump 밀도 증가의 열 이득 vs 접합·응력 비용
- 중급: 면적 열저항 단위 환산(m²·K/W ↔ mm²·K/W), 85/95 °C 구간과 refresh 2배, 접합층이 병목인 이유(열전도율 비교)

## 6. 사용할 그림 템플릿과 params

| 템플릿 | params | 제약 · 주의 |
|---|---|---|
| `f_therm` | **`core`**(권장, n = core+1) 또는 `n`(base 포함 총 die 수), `q_Wmm2`, `tTop`, `limit`, `layers` ≤ 5행, `hideResult` | 새 문항은 `core` 로. N단 → `core: N`. 결과 온도는 현실 범위(≈ 110 °C 이하) |
| `f_sip` | `type`: cowos-s·cowos-r·cowos-l·emib·emib-t, `nHBM` 1–8, **`lines`**, `bullet` | **`lines` 생략 시 숫자 없는 "HBM I/O 배선"**. 지문이 1,024 / 2,048 배선을 말하면 `lines` 를 그 값으로(E_FIG_SIP_LINES). HBM3E = 1024, HBM4 = 2048 |
| `f_plot` | `title`, `x`/`y`{min,max,ticks ≤ 6,lab}, `series` ≤ 4, `marks` ≤ 3, `bullets` ≤ 3 | 데이터 해석형 고급의 주력 |
| `f_note` | `title` ≤ 22자, `points` ≤ 4(각 ≤ 50자), `ask` ≤ 12자 | points 는 **판단 관점** — 정답 문장 금지 |
| `f_stack` | `n`(core die 수), `highlight`, `gap_um`, `h_um`, `limit_um`, `bullet`, `hideResult` | 계산 답을 `n`/`h_um` 에 넣지 말 것 |



- `f_therm.n` = base 포함 총 die 수(N단 → n = N+1), `layers` 는 지문의 층 두께·열전도율과 정확히 일치. 결과 온도(base die)는 그림이 계산해 표시하므로 그 온도를 묻는 문항은 `hideResult: true` 필수(§4A). 새 문항은 `n` 대신 `core`(= N단의 N).
- 가족은 유형별 3개(1D 누적 / 총 발열 / 단위 환산 / TIM / 계면 ΔT / 냉각 예산 …), 나머지는 위 공백 주제로 대체.
- 데이터 해석형 고급에는 `f_table`(표)·`f_wafermap`(맵)·`f_plot`(그래프)을 쓴다(DA Phase 1 신설, 예시는 LAYOUT_RULES §4). 결과를 그림이 계산하는 템플릿은 `hideResult` 의무(STANDARDS 부록 A.1).

## 7. 완료 조건

- `python3 tools/validate.py --domain THERM --gate` 통과(차단 E 0). 남는 W 는 수정 또는 `vx` + 사유.
- `python3 tools/build.py` · `node tools/smoke.js dist/HBM_quiz.html` 오류 없음.
- 보고서 `docs/reviews/THERM.md` (형식: ROSTER §4).
