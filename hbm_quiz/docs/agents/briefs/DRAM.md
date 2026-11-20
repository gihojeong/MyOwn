# DRAM 분야 브리프 — DRAM 동작과 설계

- 소유 파일: `data/09_DRAM.json` · 기준: `docs/agents/STANDARDS.md` · 자동 검사: `python3 tools/validate.py --domain DRAM`
- 작성: EA (Phase 1, 2026-11-20) · 기준선 리포트: `docs/reviews/_auto_baseline.md`

## 0. 현황

| 난이도 | 문항 | stem 단일형 | ctx 조립형 | 정답 위치 ①/②/③/④ |
|---|---|---|---|---|
| 초급 | 165 | 66 | 99 | 39 / 41 / 38 / 47 |
| 중급 | 165 | 99 | 66 | 55 / 32 / 35 / 43 |
| 고급 | 83 | 55 | 28 | 29 / 20 / 23 / 11 |
| 합계 | 413 | 220 | 193 | |

- k=1 상황도 220 · k=0 주제도 193 · 그림 사용: f_plot 244, f_note 115, f_therm 54
- **차단 E 이슈가 있는 문항: 257 / 413** (E_JOSA_CIRC 는 EA Phase 2 일괄 처리라 제외)

## 1. 자동 검사 요약 (기준선)

| 코드 | 건수 | 예시 id |
|---|---|---|
| `E_META_METRICS` | 193 | DRAM-A-0056, DRAM-A-0057, DRAM-A-0058, DRAM-A-0059 |
| `E_EXP_SHORT` | 160 | DRAM-A-0059, DRAM-A-0060, DRAM-A-0061, DRAM-A-0062 |
| `E_JOSA_CIRC` | 151 | DRAM-A-0056, DRAM-A-0058, DRAM-A-0059, DRAM-A-0060 |
| `E_EXP_ONLY_REFS` | 129 | DRAM-A-0059, DRAM-A-0060, DRAM-A-0061, DRAM-A-0062 |
| `E_STYLE_PLAIN` | 127 | DRAM-A-0056, DRAM-A-0058, DRAM-A-0060, DRAM-A-0062 |
| `E_TITLE_TRUNC` | 98 | DRAM-A-0056, DRAM-A-0057, DRAM-A-0058, DRAM-A-0059 |
| `E_FAMILY_OVER` | 64 | DRAM-A-0019, DRAM-A-0020, DRAM-A-0021, DRAM-A-0022 |
| `E_JOSA_EN` | 45 | DRAM-A-0069, DRAM-A-0070, DRAM-A-0071, DRAM-A-0072 |
| `E_DOUBLE_Q` | 13 | DRAM-B-0103, DRAM-B-0106, DRAM-B-0108, DRAM-B-0109 |
| `E_K1_FIG_NUM` | 9 | DRAM-A-0052, DRAM-A-0053, DRAM-A-0054, DRAM-A-0055 |
| `E_FIG_ANSWER_LEAK` | 1 | DRAM-I-0095 |
| `E_CALC_NO_WORK` | 1 | DRAM-B-0083 |
| `E_EXP_REF_ANSWER` | 1 | DRAM-I-0143 |
| `W_TITLE_COPY` | 193 | DRAM-A-0056, DRAM-A-0057, DRAM-A-0058, DRAM-A-0059 |
| `W_NEAR_DUP` | 190 | DRAM-A-0004, DRAM-A-0005, DRAM-A-0006, DRAM-A-0007 |
| `W_EXP_DISTRACTORS` | 118 | DRAM-A-0001, DRAM-A-0002, DRAM-A-0003, DRAM-A-0004 |
| `W_META_METRICS` | 111 | DRAM-A-0001, DRAM-A-0013, DRAM-A-0014, DRAM-A-0015 |
| `W_TITLE_QUESTION` | 92 | DRAM-A-0060, DRAM-A-0062, DRAM-A-0063, DRAM-A-0064 |
| `W_OPT_ODD_END` | 88 | DRAM-A-0058, DRAM-A-0059, DRAM-A-0062, DRAM-A-0064 |
| `W_K1_FIG_EXTRA` | 54 | DRAM-A-0034, DRAM-A-0035, DRAM-A-0036, DRAM-A-0037 |
| `W_K1_METRIC_NUM` | 49 | DRAM-A-0002, DRAM-A-0004, DRAM-A-0005, DRAM-A-0006 |
| `W_FIG_LEAK` | 22 | DRAM-A-0013, DRAM-A-0015, DRAM-A-0016, DRAM-A-0017 |
| `W_OPT_WEAK` | 14 | DRAM-A-0060, DRAM-A-0061, DRAM-A-0069, DRAM-A-0070 |
| `W_OPT_LONGEST` | 4 | DRAM-A-0001, DRAM-B-0080, DRAM-B-0164, DRAM-I-0001 |
| `W_OPT_ABSOLUTE` | 3 | DRAM-A-0080, DRAM-B-0139, DRAM-I-0125 |
| `W_EXP_OFFTOPIC` | 2 | DRAM-B-0085, DRAM-I-0100 |
| `W_OPT_PUNCT` | 2 | DRAM-A-0057, DRAM-I-0101 |
| `W_QT_LONG` | 2 | DRAM-A-0057, DRAM-I-0101 |
| `I_EXP_SRC_TAG` | 220 | DRAM-A-0001, DRAM-A-0002, DRAM-A-0003, DRAM-A-0004 |
| `I_FACT_WATCH` | 57 | DRAM-A-0002, DRAM-A-0003, DRAM-A-0004, DRAM-A-0005 |

(참고: `I_JOSA_SPACE` 346 · `I_TEMPLATE_JOIN` 193 — 새로 쓰는 문장은 조사를 붙여 쓰고, ctx 조립형은 STANDARDS 3.1 에 따라 정리)

## 2. 표본 조사로 확인한 대표 결함 (EA 직접 판독: 난이도별 10문항 이상)

- **비실재 구성으로 'HBM' 계산**: "512 bit · 4 채널"(DRAM-B-0043), "4,096 bit · 32 채널"(DRAM-B-0039), "256 bit · 16 채널 · PC 4개"(DRAM-B-0025), "1,024 bit · 16 채널 · PC 4개"(DRAM-A-0016), "1,024 bit × 11.2 Gb/s"(DRAM-I-0010) — 실제 세대 구성을 쓰거나 가상 인터페이스임을 밝힐 것(STANDARDS 2.2).
- **고급이 단순 대입**: 대역폭 계산(DRAM-A-0008), 보호 비트 비율(DRAM-A-0029) — 중급 이하로.
- **무의미 오답 템플릿**: "조건만으로는 계산할 수 없다", "단위가 맞지 않아 비교할 수 없다"가 계산 문항 보기에 반복.
- **DRAM 핵심 동작이 거의 없음**: sense amp·charge sharing 3건, row hammer 1건, tRCD/tRP 등 타이밍 0건, on-die ECC 1건, DRAM 공정(BCAT·HKMG·EUV) 0건.
- 정전기(ESD) 문항이 DRAM 에 다수(DRAM-B-0150, DRAM-I-0142) → FA 와 중복 여부 XD 판정.
- retention 온도 의존 모델 "12 °C 마다 반감"(DRAM-A-0055 계열)은 교재식 근사 — '가정' 임을 지문에 이미 명시하고 있어 유지 가능하나 가족 3개 제한.

## 3. 핵심 개념 체크리스트와 현재 커버리지

키워드 기반 근사치(지문·보기·해설에서 해당 주제가 다뤄진 문항 수). 0–4 = **공백**, 5–14 = 부족, 15+ = 있음(질은 별도 판단).

| 주제 | 초급 | 중급 | 고급 | 판정 |
|---|---|---|---|---|
| 1T1C 셀·storage capacitor | 7 | 1 | 1 | 부족 |
| sense amp·bitline·charge sharing | 3 | 0 | 0 | **공백** |
| refresh·retention·tREFI | 11 | 32 | 24 | 있음 |
| row hammer·RFM/PRAC | 0 | 0 | 1 | **공백** |
| timing tRCD/tRP/tRAS/tCCD | 0 | 0 | 0 | **공백** |
| bank/bank group·pseudo channel | 24 | 22 | 11 | 있음 |
| on-die ECC·link ECC | 1 | 0 | 0 | **공백** |
| DBI·신호 무결성·training | 4 | 1 | 0 | 부족 |
| PHY·TSV I/O 구조 | 4 | 3 | 2 | 부족 |
| VPP/VDD/VDDQ 전원 | 0 | 0 | 1 | **공백** |
| 온도 보상 refresh(85/95/105 °C) | 0 | 32 | 22 | 있음 |
| DRAM 공정(BCAT·HKMG·EUV 1b/1c) | 0 | 0 | 0 | **공백** |
| 대역폭 계산 | 28 | 58 | 38 | 있음 |

**우선 보강 공백**: 1T1C 셀 동작·charge sharing 신호량 계산, sense amp, 타이밍 파라미터(tRCD·tRP·tRAS·tRC·tCCD)와 대역폭 효율, bank/bank group 과 pseudo channel 동시 동작, refresh 오버헤드(tRFC/tREFI) 계산, row hammer 와 RFM/DRFM, on-die ECC vs link ECC, DBI·training, 온도 구간별 refresh 배수(85/95 °C), DRAM 공정(BCAT, 고종횡비 캐패시터, HKMG 주변회로, EUV 층)

## 4. 작업 지시 (우선순위 순)

0. **[최우선] 메타 지표 제거 — 304건** (`E_META_METRICS` 193, `W_META_METRICS` 111). 화면 '제시 조건' 띠에 "난이도: 고급", "묻는 것: 해당 항목", "세부 주제", "핵심어" 가 그대로 보인다(DA 스크린샷 확인). 지문 조건 2–4개로 바꾸거나, 요약할 조건이 없으면 `"metrics": []`(키는 유지). 정답 오류 수정과 같은 1순위로 처리한다.
1. **사실 오류·정답 오류 먼저**: §2 의 기술 정정 후보, `E_EXP_REF_ANSWER`(정답 키 재검증), NUM·FACT 에이전트 결과(`docs/reviews/num/DRAM.md`, `docs/reviews/_facts.md`)를 반영한다.
2. **템플릿 가족 정리**: `E_FAMILY_OVER` 대상은 가족당 3개(가능하면 난이도별 1개)만 남기고 삭제하거나 다른 판단을 묻도록 재작성. 근중복(`W_NEAR_DUP`)도 정리.
3. **ctx 조립형 정리**: ctx 가 qt 풀이에 필요 없으면 stem 단일형으로 변환. 기술 외 사유 오답·타 분야 오답(`W_OPT_WEAK`) 교체, 형식 단서(`W_OPT_ODD_END`, `W_OPT_LONGEST`, `W_OPT_ABSOLUTE`) 제거.
4. **해설 재작성**: `E_EXP_SHORT`·`E_EXP_ONLY_REFS`·`E_STYLE_PLAIN`·`W_EXP_DISTRACTORS` — 정답 근거 + 오답 3개 각각의 오류 + (계산) 식·대입·결과. 일괄 `[근거]` 꼬리표는 고친 해설에서 뺀다.
5. **제목·지표·그림**: `E_TITLE_TRUNC`·`W_TITLE_*` 제목 재작성, `E_META_METRICS` 지표를 지문 조건으로 교체, `E_K1_FIG_NUM`·`E_FIG_ANSWER_LEAK`·`E_FIG_INTERNAL`·`W_FIG_*` 그림 params 정정.
6. **난이도 재배치**: 단순 대입 계산·용어 문항이 고급이면 lv 를 내린다. lv 가 바뀌면 id 의 LV 도 달라져야 하므로 **새 id(`CODE-LV-9xxx`)를 발급하고 `"prev": "옛 id"` 필드를 남긴다**(보고서에 old→new 기록). 고급은 STANDARDS §1 기준으로 채운다.
7. **신규 출제**(§5) — 공백 주제 위주. 새 id 는 `DRAM-LV-9001` 부터.
8. 타 분야 문항은 고쳐서 `"mv": "CODE"` 로 이관 제안(EA 가 Phase 2 에서 이동) 하거나 자기 분야 관점으로 재작성.

## 4A. DA Phase 1 템플릿 변경으로 손봐야 할 기존 문항

템플릿 기본값·규약이 바뀌어(LAYOUT_RULES §3–4, STANDARDS 부록 A) 아래 문항은 params 를 고치지 않으면 그림이 지문과 어긋나거나 답을 보여 준다.

- `W_QT_LONG` **2건** — 질문 마지막 문장 90자 이하로: DRAM-A-0057, DRAM-I-0101

## 5. 추가 출제 목표

| | 초급 | 중급 | 고급 | 합계 |
|---|---|---|---|---|
| 신규 최소 | 10 | 30 | 50 | 90 |

- 가족 초과로 정리될 문항 약 64 건은 위 신규로 대체한다(수량 유지보다 질 우선, 최종 분야 규모는 ±10 % 허용).
- 최종 난이도 비율 권장: 초급 25–30 % · 중급 35–40 % · 고급 30–35 %.

- 고급(최우선, 83 → 130 이상): charge sharing 으로 비트라인 신호 ΔV 계산 후 센싱 여유 판단, tREFI·tRFC 로 refresh 시간 점유율 계산과 95 °C 확장 구간 영향, row hammer 임계와 RFM/DRFM 정책 비교, 타이밍 파라미터로 랜덤 액세스 실효 대역폭 추정, on-die ECC 와 시스템 ECC 의 역할 분담 판단
- 중급: 1T1C 읽기 과정(파괴적 읽기·restore), bank group 과 tCCD_S/L, DBI 효과

## 6. 사용할 그림 템플릿과 params

| 템플릿 | params | 제약 · 주의 |
|---|---|---|
| `f_plot` | `title`, `x`/`y`{min,max,ticks ≤ 6,lab}, `series` ≤ 4, `marks` ≤ 3, `bullets` ≤ 3 | 데이터 해석형 고급의 주력 |
| `f_note` | `title` ≤ 22자, `points` ≤ 4(각 ≤ 50자), `ask` ≤ 12자 | points 는 **판단 관점** — 정답 문장 금지 |
| `f_therm` | **`core`**(권장, n = core+1) 또는 `n`(base 포함 총 die 수), `q_Wmm2`, `tTop`, `limit`, `layers` ≤ 5행, `hideResult` | 새 문항은 `core` 로. N단 → `core: N`. 결과 온도는 현실 범위(≈ 110 °C 이하) |


- 대역폭·채널 가족은 실제 세대(HBM3/3E/4) 구성으로 각 1개만 유지.
- 데이터 해석형 고급에는 `f_table`(표)·`f_wafermap`(맵)·`f_plot`(그래프)을 쓴다(DA Phase 1 신설, 예시는 LAYOUT_RULES §4). 결과를 그림이 계산하는 템플릿은 `hideResult` 의무(STANDARDS 부록 A.1).

## 7. 완료 조건

- `python3 tools/validate.py --domain DRAM --gate` 통과(차단 E 0). 남는 W 는 수정 또는 `vx` + 사유.
- `python3 tools/build.py` · `node tools/smoke.js dist/HBM_quiz.html` 오류 없음.
- 보고서 `docs/reviews/DRAM.md` (형식: ROSTER §4).
