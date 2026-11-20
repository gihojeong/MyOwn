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
- **차단 E 이슈가 있는 문항: 437 / 537** (E_JOSA_CIRC 는 EA Phase 2 일괄 처리라 제외)

## 1. 자동 검사 요약 (기준선)

| 코드 | 건수 | 예시 id |
|---|---|---|
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
| `W_OPT_ABSOLUTE` | 7 | SIP-A-0150, SIP-A-0151, SIP-A-0163, SIP-A-0178 |
| `W_TITLE_LEN` | 6 | SIP-I-0007, SIP-I-0008, SIP-I-0009, SIP-I-0010 |
| `W_FIG_TOPIC` | 4 | SIP-A-0174, SIP-B-0135, SIP-I-0143, SIP-I-0146 |
| `W_OPT_STEM_ECHO` | 3 | SIP-I-0002, SIP-I-0005, SIP-I-0006 |
| `W_K1_METRIC_NUM` | 2 | SIP-A-0002, SIP-I-0014 |
| `W_EXP_OFFTOPIC` | 2 | SIP-B-0094, SIP-B-0095 |
| `W_STEM_NO_QMARK` | 1 | SIP-B-0132 |
| `W_EXP_REF_MISMATCH` | 1 | SIP-B-0141 |
| `I_FACT_WATCH` | 230 | SIP-A-0002, SIP-A-0013, SIP-A-0014, SIP-A-0015 |
| `I_EXP_SRC_TAG` | 226 | SIP-A-0073, SIP-A-0074, SIP-A-0075, SIP-A-0076 |

(참고: `I_JOSA_SPACE` 514 · `I_TEMPLATE_JOIN` 205 — 새로 쓰는 문장은 조사를 붙여 쓰고, ctx 조립형은 STANDARDS 3.1 에 따라 정리)

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

1. **사실 오류·정답 오류 먼저**: §2 의 기술 정정 후보, `E_EXP_REF_ANSWER`(정답 키 재검증), NUM·FACT 에이전트 결과(`docs/reviews/num/SIP.md`, `docs/reviews/_facts.md`)를 반영한다.
2. **템플릿 가족 정리**: `E_FAMILY_OVER` 대상은 가족당 3개(가능하면 난이도별 1개)만 남기고 삭제하거나 다른 판단을 묻도록 재작성. 근중복(`W_NEAR_DUP`)도 정리.
3. **ctx 조립형 정리**: ctx 가 qt 풀이에 필요 없으면 stem 단일형으로 변환. 기술 외 사유 오답·타 분야 오답(`W_OPT_WEAK`) 교체, 형식 단서(`W_OPT_ODD_END`, `W_OPT_LONGEST`, `W_OPT_ABSOLUTE`) 제거.
4. **해설 재작성**: `E_EXP_SHORT`·`E_EXP_ONLY_REFS`·`E_STYLE_PLAIN`·`W_EXP_DISTRACTORS` — 정답 근거 + 오답 3개 각각의 오류 + (계산) 식·대입·결과. 일괄 `[근거]` 꼬리표는 고친 해설에서 뺀다.
5. **제목·지표·그림**: `E_TITLE_TRUNC`·`W_TITLE_*` 제목 재작성, `E_META_METRICS` 지표를 지문 조건으로 교체, `E_K1_FIG_NUM`·`E_FIG_ANSWER_LEAK`·`E_FIG_INTERNAL`·`W_FIG_*` 그림 params 정정.
6. **난이도 재배치**: 단순 대입 계산·용어 문항이 고급이면 lv 를 내린다. lv 가 바뀌면 id 의 LV 도 달라져야 하므로 **새 id(`CODE-LV-9xxx`)를 발급하고 `"prev": "옛 id"` 필드를 남긴다**(보고서에 old→new 기록). 고급은 STANDARDS §1 기준으로 채운다.
7. **신규 출제**(§5) — 공백 주제 위주. 새 id 는 `SIP-LV-9001` 부터.
8. 타 분야 문항은 고쳐서 `"mv": "CODE"` 로 이관 제안(EA 가 Phase 2 에서 이동) 하거나 자기 분야 관점으로 재작성.

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
| `f_sip` | `type`: cowos-s·cowos-r·cowos-l·emib·emib-t, `nHBM` 1–4, `bullet` | "2,048선" 라벨 고정(HBM3E 문항과 모순 주의) |
| `f_stack` | `n`(**core die 수**), `highlight`: null·height·midcore·base·gap·topcore, `gap_um`, `h_um`, `limit_um`, `bullet` | 표에 die n+1, 간극 n, 높이 h_um 표시 → 계산 답을 h_um/n 에 넣지 말 것 |
| `f_plot` | `title`, `x`{min,max,ticks,lab}, `y`{…}, `series`[{name, color(“RRGGBB”), pts[[x,y]], dash}], `marks`[[x, 라벨]], `bullets`[…] | 데이터 해석형 고급 문항의 주력 템플릿 |
| `f_note` | `title`, `points`(≤ 4), `ask` | 정답 문장 금지 |


- 높이 계산은 **입력 조건만 그림에** (n·h_um 에 답 금지). 높이 가족은 3개만 유지하고 나머지는 위 공백 주제로 대체.
- 데이터 해석형 고급에 표가 필요하면 `f_plot`(그래프)으로 우선 해결하고, 표 템플릿(`f_table`)은 DA 에 요청 중(`EA_to_DA.md`). 확정 전에는 표 데이터를 지문 안 문장으로 쓴다.

## 7. 완료 조건

- `python3 tools/validate.py --domain SIP --gate` 통과(차단 E 0). 남는 W 는 수정 또는 `vx` + 사유.
- `python3 tools/build.py` · `node tools/smoke.js dist/HBM_quiz.html` 오류 없음.
- 보고서 `docs/reviews/SIP.md` (형식: ROSTER §4).
