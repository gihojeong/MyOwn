# FA 분야 브리프 — 고장분석과 신뢰성

- 소유 파일: `data/07_FA.json` · 기준: `docs/agents/STANDARDS.md` · 자동 검사: `python3 tools/validate.py --domain FA`
- 작성: EA (Phase 1, 2026-11-20) · 기준선 리포트: `docs/reviews/_auto_baseline.md`

## 0. 현황

| 난이도 | 문항 | stem 단일형 | ctx 조립형 | 정답 위치 ①/②/③/④ |
|---|---|---|---|---|
| 초급 | 120 | 46 | 74 | 26 / 32 / 35 / 27 |
| 중급 | 115 | 24 | 91 | 31 / 33 / 26 / 25 |
| 고급 | 139 | 23 | 116 | 30 / 35 / 38 / 36 |
| 합계 | 374 | 93 | 281 | |

- k=1 상황도 93 · k=0 주제도 281 · 그림 사용: f_fa 233, f_rel 137, f_note 4
- **차단 E 이슈가 있는 문항: 322 / 374** (E_JOSA_CIRC 는 EA Phase 2 일괄 처리라 제외)

## 1. 자동 검사 요약 (기준선)

| 코드 | 건수 | 예시 id |
|---|---|---|
| `E_META_METRICS` | 281 | FA-A-0024, FA-A-0025, FA-A-0026, FA-A-0027 |
| `E_JOSA_CIRC` | 252 | FA-A-0024, FA-A-0025, FA-A-0026, FA-A-0027 |
| `E_STYLE_PLAIN` | 235 | FA-A-0024, FA-A-0025, FA-A-0026, FA-A-0027 |
| `E_TITLE_TRUNC` | 202 | FA-A-0024, FA-A-0025, FA-A-0026, FA-A-0027 |
| `E_EXP_SHORT` | 194 | FA-A-0033, FA-A-0051, FA-A-0055, FA-A-0056 |
| `E_EXP_ONLY_REFS` | 131 | FA-A-0051, FA-A-0056, FA-A-0072, FA-A-0075 |
| `E_FAMILY_OVER` | 37 | FA-A-0006, FA-A-0007, FA-A-0008, FA-A-0009 |
| `E_JOSA_EN` | 19 | FA-A-0035, FA-A-0042, FA-A-0050, FA-A-0073 |
| `E_DOUBLE_Q` | 19 | FA-B-0067, FA-B-0068, FA-B-0069, FA-B-0070 |
| `E_CALC_NO_WORK` | 7 | FA-A-0059, FA-A-0120, FA-B-0012, FA-B-0014 |
| `E_DUP_EXACT` | 4 | FA-B-0026, FA-B-0028, FA-B-0030, FA-B-0034 |
| `E_EXP_REF_ANSWER` | 2 | FA-A-0083, FA-I-0091 |
| `W_TITLE_COPY` | 281 | FA-A-0024, FA-A-0025, FA-A-0026, FA-A-0027 |
| `W_OPT_ODD_END` | 80 | FA-A-0022, FA-A-0061, FA-A-0066, FA-A-0069 |
| `W_EXP_DISTRACTORS` | 76 | FA-A-0001, FA-A-0021, FA-A-0022, FA-A-0023 |
| `W_TITLE_QUESTION` | 75 | FA-A-0051, FA-A-0080, FA-A-0089, FA-A-0090 |
| `W_META_METRICS` | 69 | FA-A-0021, FA-A-0022, FA-A-0023, FA-B-0003 |
| `W_OPT_LONGEST` | 28 | FA-A-0021, FA-A-0022, FA-A-0023, FA-A-0035 |
| `W_NEAR_DUP` | 26 | FA-A-0003, FA-A-0004, FA-A-0005, FA-A-0006 |
| `W_OPT_WEAK` | 21 | FA-A-0057, FA-A-0059, FA-A-0072, FA-A-0075 |
| `W_OPT_ABSOLUTE` | 17 | FA-A-0001, FA-A-0045, FA-A-0048, FA-A-0055 |
| `W_TITLE_LEN` | 10 | FA-I-0003, FA-I-0004, FA-I-0005, FA-I-0006 |
| `W_FIG_TOPIC` | 5 | FA-A-0083, FA-A-0101, FA-A-0102, FA-A-0118 |
| `W_K1_METRIC_NUM` | 2 | FA-A-0001, FA-B-0002 |
| `W_K1_FIG_EXTRA` | 2 | FA-A-0022, FA-I-0023 |
| `W_EXP_OFFTOPIC` | 2 | FA-B-0059, FA-I-0071 |
| `I_FACT_WATCH` | 49 | FA-A-0002, FA-A-0003, FA-A-0004, FA-A-0005 |
| `I_EXP_SRC_TAG` | 5 | FA-A-0021, FA-A-0022, FA-A-0023, FA-I-0023 |

(참고: `I_JOSA_SPACE` 189 · `I_TEMPLATE_JOIN` 281 — 새로 쓰는 문장은 조사를 붙여 쓰고, ctx 조립형은 STANDARDS 3.1 에 따라 정리)

## 2. 표본 조사로 확인한 대표 결함 (EA 직접 판독: 난이도별 10문항 이상)

- **이중 사실 묶음 고급**: "기준을 만족했으며, 전압을 걸지 않는 고온 보관은 HTS 이다"(FA-A-0003 계열 18) — 고장률 판정과 용어 구분을 한 보기에 묶음. 또 "누적 고장률 5 % 이하" 판정은 JEDEC(JESD47: 3 lot × 77, 0 fail) 방식이 아님 → 사내 기준임을 명시하거나 재설계.
- **기법 판정 가족**: "설명에 해당하는 고장분석 기법 고르기"(FA-B-0007 계열), "신호가 나타나는 위치의 의미"(FA-I-0008 계열) — 그림이 기법명을 제목으로 보여 줌(W_FIG_LEAK 성격).
- **그림 분기 불일치**: LIT 질문에 `f_fa tech: obirch`(FA-A-0083), W_FIG_TOPIC 5.
- **해설이 정답을 오답으로**: FA-A-0083 "②③④는 위상 정보의 용도가 아니다"(a=③).
- 타 분야 혼재: ECC 정정 가능 오류 추세(FA-A-0058 → DRAM), glue 열 한계(FA-A-0032 → BSP), cube height(FA-A-0024 → SIP/WARP).
- `f_rel` 기본 시퀀스 첫 행이 "J-STD-020 · MSL preconditioning" — preconditioning 절차는 JESD22-A113(DA 요청).

## 3. 핵심 개념 체크리스트와 현재 커버리지

키워드 기반 근사치(지문·보기·해설에서 해당 주제가 다뤄진 문항 수). 0–4 = **공백**, 5–14 = 부족, 15+ = 있음(질은 별도 판단).

| 주제 | 초급 | 중급 | 고급 | 판정 |
|---|---|---|---|---|
| LIT(lock-in thermography) | 23 | 5 | 7 | 있음 |
| OBIRCH | 21 | 4 | 0 | 고급 없음 |
| EMMI/PEM | 6 | 2 | 1 | 부족 |
| EOTPR/TDR | 22 | 4 | 4 | 있음 |
| 3D X-ray(XRM/CT) | 32 | 14 | 12 | 있음 |
| SAT(C-SAM) 초음파 | 16 | 8 | 4 | 있음 |
| FIB·TEM·단면 | 5 | 10 | 11 | 있음 |
| nanoprobing | 0 | 0 | 0 | **공백** |
| JESD47 qual(77×3, LTPD) | 1 | 0 | 0 | **공백** |
| TC/HTOL/HTS/uHAST/THB | 30 | 12 | 36 | 있음 |
| MSL·preconditioning(J-STD-020/JESD22-A113) | 21 | 1 | 1 | 있음 |
| 가속계수(Arrhenius·Coffin-Manson·Peck) | 0 | 1 | 0 | **공백** |
| Weibull·FIT | 0 | 0 | 0 | **공백** |
| ESD(HBM/CDM) | 25 | 0 | 19 | 있음 |

**우선 보강 공백**: 가속 계수(Arrhenius·Coffin-Manson·Peck) 계산, Weibull·FIT, JESD47 표본 설계(LTPD), EMMI/PEM, nanoprobing, FIB/plasma FIB 단면 전략, SAT(C-SAM) 의 위상 반전·해상도, HBM 고유 고장 모드(µbump crack, TSV open, NCF void, die crack, EM)별 신호 특징

## 4. 작업 지시 (우선순위 순)

1. **사실 오류·정답 오류 먼저**: §2 의 기술 정정 후보, `E_EXP_REF_ANSWER`(정답 키 재검증), NUM·FACT 에이전트 결과(`docs/reviews/num/FA.md`, `docs/reviews/_facts.md`)를 반영한다.
2. **템플릿 가족 정리**: `E_FAMILY_OVER` 대상은 가족당 3개(가능하면 난이도별 1개)만 남기고 삭제하거나 다른 판단을 묻도록 재작성. 근중복(`W_NEAR_DUP`)도 정리.
3. **ctx 조립형 정리**: ctx 가 qt 풀이에 필요 없으면 stem 단일형으로 변환. 기술 외 사유 오답·타 분야 오답(`W_OPT_WEAK`) 교체, 형식 단서(`W_OPT_ODD_END`, `W_OPT_LONGEST`, `W_OPT_ABSOLUTE`) 제거.
4. **해설 재작성**: `E_EXP_SHORT`·`E_EXP_ONLY_REFS`·`E_STYLE_PLAIN`·`W_EXP_DISTRACTORS` — 정답 근거 + 오답 3개 각각의 오류 + (계산) 식·대입·결과. 일괄 `[근거]` 꼬리표는 고친 해설에서 뺀다.
5. **제목·지표·그림**: `E_TITLE_TRUNC`·`W_TITLE_*` 제목 재작성, `E_META_METRICS` 지표를 지문 조건으로 교체, `E_K1_FIG_NUM`·`E_FIG_ANSWER_LEAK`·`E_FIG_INTERNAL`·`W_FIG_*` 그림 params 정정.
6. **난이도 재배치**: 단순 대입 계산·용어 문항이 고급이면 lv 를 내린다. lv 가 바뀌면 id 의 LV 도 달라져야 하므로 **새 id(`CODE-LV-9xxx`)를 발급하고 `"prev": "옛 id"` 필드를 남긴다**(보고서에 old→new 기록). 고급은 STANDARDS §1 기준으로 채운다.
7. **신규 출제**(§5) — 공백 주제 위주. 새 id 는 `FA-LV-9001` 부터.
8. 타 분야 문항은 고쳐서 `"mv": "CODE"` 로 이관 제안(EA 가 Phase 2 에서 이동) 하거나 자기 분야 관점으로 재작성.

## 5. 추가 출제 목표

| | 초급 | 중급 | 고급 | 합계 |
|---|---|---|---|---|
| 신규 최소 | 10 | 30 | 40 | 80 |

- 가족 초과로 정리될 문항 약 37 건은 위 신규로 대체한다(수량 유지보다 질 우선, 최종 분야 규모는 ±10 % 허용).
- 최종 난이도 비율 권장: 초급 25–30 % · 중급 35–40 % · 고급 30–35 %.

- 고급(최우선): 두 시험 조건 간 가속 계수 계산 후 현장 수명 추정, Weibull 플롯 기울기로 고장 모드 판정(초기/마모), 복수 FA 결과(LIT 위치 + EOTPR 지연 + XRM slice)로 결함 위치·깊이 확정, 0-fail 표본 수와 신뢰수준 계산
- 중급: SAT 신호 위상 반전의 의미, EMMI vs OBIRCH 선택 조건, JEDEC 시험별 바이어스·습도 조건 비교

## 6. 사용할 그림 템플릿과 params

| 템플릿 | params | 제약 · 주의 |
|---|---|---|
| `f_fa` | `tech`: lit·obirch·eotpr·xrm · lit/obirch: `hot`[x,y](0–1), `fov_um`, `depth` · eotpr: `feats`[[ps, mV, 라벨], …] · xrm: `dz`, `zpeak`(µm) | 지문 기법과 tech 일치 |
| `f_rel` | `seq`[[문서, 시험명, 조건], …], `cur`(강조 행), `fails`[[cycle, %], …], `crit`(%), `hint`, `bullet` | x축 "TC cycle 수" 0–1000 고정, y 0–10 % |
| `f_plot` | `title`, `x`{min,max,ticks,lab}, `y`{…}, `series`[{name, color(“RRGGBB”), pts[[x,y]], dash}], `marks`[[x, 라벨]], `bullets`[…] | 데이터 해석형 고급 문항의 주력 템플릿 |
| `f_note` | `title`, `points`(≤ 4), `ask` | 정답 문장 금지 |


- `f_fa` 는 지문 기법과 tech 일치. 기법 이름을 묻는 문항은 그림 제목이 답을 보여 주므로 k=0 + 중립 주제도(`f_note`)를 쓴다.
- 데이터 해석형 고급에 표가 필요하면 `f_plot`(그래프)으로 우선 해결하고, 표 템플릿(`f_table`)은 DA 에 요청 중(`EA_to_DA.md`). 확정 전에는 표 데이터를 지문 안 문장으로 쓴다.

## 7. 완료 조건

- `python3 tools/validate.py --domain FA --gate` 통과(차단 E 0). 남는 W 는 수정 또는 `vx` + 사유.
- `python3 tools/build.py` · `node tools/smoke.js dist/HBM_quiz.html` 오류 없음.
- 보고서 `docs/reviews/FA.md` (형식: ROSTER §4).
