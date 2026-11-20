# COW 분야 브리프 — CoW 적층 접합

- 소유 파일: `data/04_COW.json` · 기준: `docs/agents/STANDARDS.md` · 자동 검사: `python3 tools/validate.py --domain COW`
- 작성: EA (Phase 1, 2026-11-20) · 기준선 리포트: `docs/reviews/_auto_baseline.md`

## 0. 현황

| 난이도 | 문항 | stem 단일형 | ctx 조립형 | 정답 위치 ①/②/③/④ |
|---|---|---|---|---|
| 초급 | 117 | 48 | 69 | 29 / 25 / 26 / 37 |
| 중급 | 245 | 140 | 105 | 51 / 61 / 68 / 65 |
| 고급 | 193 | 151 | 42 | 47 / 52 / 51 / 43 |
| 합계 | 555 | 339 | 216 | |

- k=1 상황도 339 · k=0 주제도 216 · 그림 사용: f_hcb 306, f_bond 247, f_note 1, f_saw 1
- **차단 E 이슈가 있는 문항: 415 / 555** (E_JOSA_CIRC 는 EA Phase 2 일괄 처리라 제외)

## 1. 자동 검사 요약 (기준선)

| 코드 | 건수 | 예시 id |
|---|---|---|
| `E_META_METRICS` | 216 | COW-A-0152, COW-A-0153, COW-A-0154, COW-A-0155 |
| `E_JOSA_CIRC` | 192 | COW-A-0152, COW-A-0153, COW-A-0154, COW-A-0155 |
| `E_STYLE_PLAIN` | 176 | COW-A-0152, COW-A-0153, COW-A-0154, COW-A-0155 |
| `E_EXP_SHORT` | 149 | COW-A-0164, COW-A-0169, COW-A-0175, COW-A-0178 |
| `E_FAMILY_OVER` | 146 | COW-A-0006, COW-A-0007, COW-A-0008, COW-A-0009 |
| `E_TITLE_TRUNC` | 129 | COW-A-0152, COW-A-0153, COW-A-0154, COW-A-0155 |
| `E_K1_FIG_NUM` | 104 | COW-A-0001, COW-A-0043, COW-A-0044, COW-A-0045 |
| `E_EXP_ONLY_REFS` | 98 | COW-A-0178, COW-A-0180, COW-A-0181, COW-A-0183 |
| `E_JOSA_EN` | 28 | COW-A-0077, COW-A-0155, COW-A-0164, COW-A-0174 |
| `E_CALC_NO_WORK` | 5 | COW-B-0072, COW-B-0076, COW-I-0212, COW-I-0241 |
| `E_FIG_ANSWER_LEAK` | 4 | COW-A-0082, COW-A-0085, COW-I-0036, COW-I-0044 |
| `E_EXP_REF_ANSWER` | 4 | COW-B-0079, COW-I-0197, COW-I-0205, COW-I-0211 |
| `E_DOUBLE_Q` | 3 | COW-B-0081, COW-B-0095, COW-B-0101 |
| `W_EXP_DISTRACTORS` | 324 | COW-A-0001, COW-A-0002, COW-A-0003, COW-A-0004 |
| `W_K1_FIG_EXTRA` | 296 | COW-A-0001, COW-A-0002, COW-A-0003, COW-A-0004 |
| `W_META_METRICS` | 221 | COW-A-0043, COW-A-0044, COW-A-0045, COW-A-0046 |
| `W_TITLE_COPY` | 216 | COW-A-0152, COW-A-0153, COW-A-0154, COW-A-0155 |
| `W_NEAR_DUP` | 191 | COW-A-0080, COW-A-0081, COW-A-0082, COW-A-0083 |
| `W_TITLE_QUESTION` | 86 | COW-A-0170, COW-A-0178, COW-A-0180, COW-A-0181 |
| `W_OPT_ODD_END` | 61 | COW-A-0172, COW-A-0173, COW-A-0177, COW-A-0178 |
| `W_K1_METRIC_NUM` | 47 | COW-A-0001, COW-A-0111, COW-A-0114, COW-A-0115 |
| `W_OPT_LONGEST` | 31 | COW-A-0074, COW-A-0076, COW-A-0077, COW-A-0078 |
| `W_TITLE_LEN` | 19 | COW-A-0001, COW-A-0027, COW-A-0028, COW-A-0029 |
| `W_FIG_LEAK` | 17 | COW-A-0001, COW-A-0027, COW-A-0028, COW-A-0029 |
| `W_OPT_ABSOLUTE` | 12 | COW-A-0074, COW-A-0076, COW-A-0174, COW-A-0175 |
| `W_OPT_WEAK` | 11 | COW-A-0076, COW-B-0062, COW-B-0078, COW-B-0085 |
| `W_EXP_OFFTOPIC` | 9 | COW-B-0052, COW-B-0062, COW-B-0063, COW-I-0141 |
| `W_FIG_TOPIC` | 5 | COW-A-0184, COW-A-0189, COW-B-0090, COW-B-0095 |
| `W_OPT_PUNCT` | 2 | COW-A-0174, COW-I-0187 |
| `W_OPT_STEM_ECHO` | 1 | COW-A-0077 |
| `W_NEAR_DUP_X` | 1 | COW-A-0160 |
| `I_EXP_SRC_TAG` | 223 | COW-A-0071, COW-A-0072, COW-A-0073, COW-A-0074 |

(참고: `I_JOSA_SPACE` 548 · `I_TEMPLATE_JOIN` 216 — 새로 쓰는 문장은 조사를 붙여 쓰고, ctx 조립형은 STANDARDS 3.1 에 따라 정리)

## 2. 표본 조사로 확인한 대표 결함 (EA 직접 판독: 난이도별 10문항 이상)

- **치명적 계산 오류 28문항 (COW-A-0043 ~ -0070)**: "배율 오차 × 반지름" 변위를 1,000배 크게 계산. 1 ppm × 125 mm = **125 nm** 인데 정답이 "125000 nm 로 허용치를 벗어난다". 정답 값과 '허용치 초과' 판정이 모두 틀린 경우가 다수(0.5 ppm × 100 mm = 50 nm 는 ±150 nm 이내). 전부 재계산·재작성.
- **공법 설정 오류**: hybrid copper bonding 인데 "bump pitch 40 µm, die 간극 9 µm"(COW-B-0007 계열) — HCB 는 bump 간극이 없고 pitch 가 수 µm. `f_bond` hcb 분기에 gap 수치 표시.
- **그림 불일치**: 접점 밀도 문항(pitch 30→9 µm)에 `f_hcb pitch_um: 2`(COW-B-0042), 겹침 면적 문항(pad 1500 nm·오차 250 nm)에 `off_nm 190`(COW-A-0094). E_K1_FIG_NUM 104.
- **사실 검증 필요**: COW-I-0023 "HCB 는 die 휨 100 nm 미만 요구" — D2W 접합에서 die bow 허용치는 통상 µm 급으로 보고되므로 출처 확인(나노토포그래피·국부 평탄도와 혼동 가능). COW-B-0106 MR-MUF 방열 우위의 근거(EMC 열전도·더 많은 thermal bump)를 해설에 명시.
- **명명 규약 충돌**: COW-I-0141 해설 "Bump 면 아래에서 중앙이 솟은 형상 = Cry" 는 `f_warp` 표(Smile)와 반대 → STANDARDS 2.5 로 통일.
- 가족 초과 146(ppm 28, overlay 판정 24, dishing 16, 접점 수 등).

## 3. 핵심 개념 체크리스트와 현재 커버리지

키워드 기반 근사치(지문·보기·해설에서 해당 주제가 다뤄진 문항 수). 0–4 = **공백**, 5–14 = 부족, 15+ = 있음(질은 별도 판단).

| 주제 | 초급 | 중급 | 고급 | 판정 |
|---|---|---|---|---|
| TC-NCF(열압착·NCF) | 60 | 47 | 11 | 있음 |
| MR-MUF(mass reflow·molded underfill) | 43 | 51 | 25 | 있음 |
| Advanced MR-MUF·warpage 제어 | 2 | 1 | 0 | **공백** |
| hybrid bonding(D2W) 공정 흐름 | 29 | 46 | 100 | 있음 |
| SiCN/SiO2 유전막·plasma activation | 9 | 4 | 19 | 있음 |
| Cu recess/dishing·anneal 팽창 | 8 | 7 | 45 | 있음 |
| overlay·배율(run-out) | 0 | 0 | 55 | 있음 |
| particle·void(접합 wave) | 2 | 13 | 27 | 있음 |
| gap·fillet·flow void | 32 | 70 | 45 | 있음 |
| filler entrapment | 9 | 10 | 5 | 있음 |
| collective(gang) bonding·throughput | 5 | 9 | 6 | 있음 |
| fluxless TCB | 0 | 1 | 1 | **공백** |
| 접점 밀도·pitch 계산 | 23 | 57 | 31 | 있음 |

**우선 보강 공백**: fluxless TCB, Advanced MR-MUF(웨이퍼 휨 제어·고열전도 EMC), D2W HCB 공정 흐름(CMP→세정→plasma 활성화→정렬→상온 접합→anneal)과 대기 시간, 접합 wave·void 전파, collective(gang) bonding 처리량, NCF 경화도·유동과 filler, 고단 적층에서 하단 die 의 누적 열이력

## 4. 작업 지시 (우선순위 순)

1. **사실 오류·정답 오류 먼저**: §2 의 기술 정정 후보, `E_EXP_REF_ANSWER`(정답 키 재검증), NUM·FACT 에이전트 결과(`docs/reviews/num/COW.md`, `docs/reviews/_facts.md`)를 반영한다.
2. **템플릿 가족 정리**: `E_FAMILY_OVER` 대상은 가족당 3개(가능하면 난이도별 1개)만 남기고 삭제하거나 다른 판단을 묻도록 재작성. 근중복(`W_NEAR_DUP`)도 정리.
3. **ctx 조립형 정리**: ctx 가 qt 풀이에 필요 없으면 stem 단일형으로 변환. 기술 외 사유 오답·타 분야 오답(`W_OPT_WEAK`) 교체, 형식 단서(`W_OPT_ODD_END`, `W_OPT_LONGEST`, `W_OPT_ABSOLUTE`) 제거.
4. **해설 재작성**: `E_EXP_SHORT`·`E_EXP_ONLY_REFS`·`E_STYLE_PLAIN`·`W_EXP_DISTRACTORS` — 정답 근거 + 오답 3개 각각의 오류 + (계산) 식·대입·결과. 일괄 `[근거]` 꼬리표는 고친 해설에서 뺀다.
5. **제목·지표·그림**: `E_TITLE_TRUNC`·`W_TITLE_*` 제목 재작성, `E_META_METRICS` 지표를 지문 조건으로 교체, `E_K1_FIG_NUM`·`E_FIG_ANSWER_LEAK`·`E_FIG_INTERNAL`·`W_FIG_*` 그림 params 정정.
6. **난이도 재배치**: 단순 대입 계산·용어 문항이 고급이면 lv 를 내린다. lv 가 바뀌면 id 의 LV 도 달라져야 하므로 **새 id(`CODE-LV-9xxx`)를 발급하고 `"prev": "옛 id"` 필드를 남긴다**(보고서에 old→new 기록). 고급은 STANDARDS §1 기준으로 채운다.
7. **신규 출제**(§5) — 공백 주제 위주. 새 id 는 `COW-LV-9001` 부터.
8. 타 분야 문항은 고쳐서 `"mv": "CODE"` 로 이관 제안(EA 가 Phase 2 에서 이동) 하거나 자기 분야 관점으로 재작성.

## 5. 추가 출제 목표

| | 초급 | 중급 | 고급 | 합계 |
|---|---|---|---|---|
| 신규 최소 | 10 | 30 | 40 | 80 |

- 가족 초과로 정리될 문항 약 146 건은 위 신규로 대체한다(수량 유지보다 질 우선, 최종 분야 규모는 ±10 % 허용).
- 최종 난이도 비율 권장: 초급 25–30 % · 중급 35–40 % · 고급 30–35 %.

- 고급: 16-Hi 에서 TC-NCF / MR-MUF / HCB 선택(높이 예산·열저항·수율·처리량 4변수 표), HCB 접합 후 SAT·전기 데이터로 void 원인(입자 vs dishing vs 배율) 규명, anneal 온도 vs Cu 팽창 vs dishing 허용치 정량, gang bonding 의 정렬·열이력 트레이드오프, MR-MUF 유동 void 와 간극·거리 의존(모세관 충전 시간 ∝ L²/(gap) 류 근사)
- 중급: plasma 활성화 후 대기 시간 영향, fluxless 의 이유, NCF 의 최저 점도 온도와 solder 융점 순서

## 6. 사용할 그림 템플릿과 params

| 템플릿 | params | 제약 · 주의 |
|---|---|---|
| `f_bond` | `method`: ncf·mrmuf·hcb, `pitch_um`, `gap_um`, `voids` 0–3, `filler_trap`(ncf), `nonwet`, `bullet` | hcb 분기는 항상 dishing 미접합 pad 를 그리고 "gap" 치수를 표시(DA 요청 중) → hcb 에 bump 간극 수치를 주지 말 것 |
| `f_hcb` | `pitch_um`, `tol_nm`, `off_nm`, `dish_nm`, `bullet` | 허용치 대비 초과/이내를 그림이 판정해 표시 → 판정이 답이면 정답 노출 |
| `f_plot` | `title`, `x`{min,max,ticks,lab}, `y`{…}, `series`[{name, color(“RRGGBB”), pts[[x,y]], dash}], `marks`[[x, 라벨]], `bullets`[…] | 데이터 해석형 고급 문항의 주력 템플릿 |
| `f_note` | `title`, `points`(≤ 4), `ask` | 정답 문장 금지 |


- `f_bond` hcb 분기는 bump 간극을 그리므로 HCB 상황도에는 `f_hcb` 를 쓴다. `f_hcb` 의 허용 초과/이내 표시는 판정형 문항의 답을 노출하므로 그 경우 k=0 으로.
- 데이터 해석형 고급에 표가 필요하면 `f_plot`(그래프)으로 우선 해결하고, 표 템플릿(`f_table`)은 DA 에 요청 중(`EA_to_DA.md`). 확정 전에는 표 데이터를 지문 안 문장으로 쓴다.

## 7. 완료 조건

- `python3 tools/validate.py --domain COW --gate` 통과(차단 E 0). 남는 W 는 수정 또는 `vx` + 사유.
- `python3 tools/build.py` · `node tools/smoke.js dist/HBM_quiz.html` 오류 없음.
- 보고서 `docs/reviews/COW.md` (형식: ROSTER §4).
