# TSV 분야 브리프 — TSV 형성과 충전

- 소유 파일: `data/00_TSV.json` · 기준: `docs/agents/STANDARDS.md` · 자동 검사: `python3 tools/validate.py --domain TSV`
- 작성: EA (Phase 1, 2026-11-20) · 기준선 리포트: `docs/reviews/_auto_baseline.md`

## 0. 현황

| 난이도 | 문항 | stem 단일형 | ctx 조립형 | 정답 위치 ①/②/③/④ |
|---|---|---|---|---|
| 초급 | 109 | 52 | 57 | 24 / 29 / 30 / 26 |
| 중급 | 212 | 121 | 91 | 58 / 47 / 58 / 49 |
| 고급 | 171 | 92 | 79 | 45 / 43 / 40 / 43 |
| 합계 | 492 | 265 | 227 | |

- k=1 상황도 265 · k=0 주제도 227 · 그림 사용: f_tsv 354, f_cmp 82, f_warp 54, f_plot 1, f_bump 1
- **차단 E 이슈가 있는 문항: 360 / 492** (E_JOSA_CIRC 는 EA Phase 2 일괄 처리라 제외)

## 1. 자동 검사 요약 (기준선)

| 코드 | 건수 | 예시 id |
|---|---|---|
| `E_META_METRICS` | 227 | TSV-A-0093, TSV-A-0094, TSV-A-0095, TSV-A-0096 |
| `E_JOSA_CIRC` | 210 | TSV-A-0093, TSV-A-0094, TSV-A-0095, TSV-A-0096 |
| `E_STYLE_PLAIN` | 199 | TSV-A-0093, TSV-A-0094, TSV-A-0095, TSV-A-0096 |
| `E_TITLE_TRUNC` | 189 | TSV-A-0093, TSV-A-0094, TSV-A-0095, TSV-A-0096 |
| `E_FIG_INTERNAL` | 169 | TSV-A-0093, TSV-A-0094, TSV-A-0095, TSV-A-0096 |
| `E_FAMILY_OVER` | 124 | TSV-A-0006, TSV-A-0007, TSV-A-0008, TSV-A-0009 |
| `E_EXP_SHORT` | 117 | TSV-A-0118, TSV-A-0121, TSV-A-0122, TSV-A-0136 |
| `E_EXP_ONLY_REFS` | 76 | TSV-A-0136, TSV-A-0141, TSV-A-0147, TSV-A-0148 |
| `E_JOSA_EN` | 42 | TSV-A-0094, TSV-A-0095, TSV-A-0112, TSV-A-0114 |
| `E_K1_FIG_NUM` | 15 | TSV-I-0013, TSV-I-0015, TSV-I-0016, TSV-I-0017 |
| `E_DOUBLE_Q` | 5 | TSV-B-0061, TSV-B-0075, TSV-B-0076, TSV-B-0077 |
| `E_OPT_DUP` | 3 | TSV-A-0021, TSV-A-0031, TSV-A-0044 |
| `E_EXP_REF_ANSWER` | 3 | TSV-A-0155, TSV-I-0172, TSV-I-0204 |
| `E_CALC_NO_WORK` | 1 | TSV-B-0097 |
| `W_TITLE_COPY` | 227 | TSV-A-0093, TSV-A-0094, TSV-A-0095, TSV-A-0096 |
| `W_EXP_DISTRACTORS` | 225 | TSV-A-0001, TSV-A-0002, TSV-A-0003, TSV-A-0004 |
| `W_NEAR_DUP` | 115 | TSV-A-0051, TSV-A-0053, TSV-A-0055, TSV-A-0059 |
| `W_K1_METRIC_NUM` | 106 | TSV-A-0002, TSV-A-0015, TSV-A-0017, TSV-A-0018 |
| `W_K1_FIG_EXTRA` | 92 | TSV-A-0001, TSV-A-0003, TSV-A-0004, TSV-A-0005 |
| `W_META_METRICS` | 91 | TSV-A-0015, TSV-A-0016, TSV-A-0017, TSV-A-0018 |
| `W_OPT_ODD_END` | 58 | TSV-A-0101, TSV-A-0102, TSV-A-0103, TSV-A-0123 |
| `W_TITLE_QUESTION` | 35 | TSV-A-0170, TSV-B-0054, TSV-B-0055, TSV-B-0056 |
| `W_TITLE_LEN` | 32 | TSV-A-0048, TSV-A-0055, TSV-A-0056, TSV-A-0057 |
| `W_OPT_LONGEST` | 21 | TSV-A-0045, TSV-A-0046, TSV-A-0047, TSV-A-0121 |
| `W_FIG_K0_DEFECT` | 14 | TSV-A-0102, TSV-A-0110, TSV-A-0125, TSV-A-0153 |
| `W_OPT_ABSOLUTE` | 11 | TSV-A-0100, TSV-A-0108, TSV-A-0115, TSV-A-0122 |
| `W_OPT_WEAK` | 10 | TSV-A-0046, TSV-A-0101, TSV-A-0106, TSV-A-0135 |
| `W_EXP_OFFTOPIC` | 3 | TSV-B-0062, TSV-B-0082, TSV-I-0156 |
| `W_EXP_REF_MISMATCH` | 2 | TSV-A-0128, TSV-I-0125 |
| `W_OPT_STEM_ECHO` | 1 | TSV-A-0114 |
| `W_OPT_PUNCT` | 1 | TSV-A-0132 |
| `I_EXP_SRC_TAG` | 115 | TSV-A-0045, TSV-A-0046, TSV-A-0047, TSV-A-0048 |

(참고: `I_JOSA_SPACE` 485 · `I_TEMPLATE_JOIN` 227 — 새로 쓰는 문장은 조사를 붙여 쓰고, ctx 조립형은 STANDARDS 3.1 에 따라 정리)

## 2. 표본 조사로 확인한 대표 결함 (EA 직접 판독: 난이도별 10문항 이상)

- **수치 템플릿 가족 과다**: 직류 저항(ρL/A) 30개(TSV-A-0015~), aspect ratio 계산 15+15개(TSV-B-0003~, -0004~), Bosch scallop 인과 18개(TSV-I-0013~), CMP dishing/erosion 짝짓기 24개(TSV-I-0031~), barrier 생략 12개(TSV-A-0003~). 같은 식에 숫자만 바꾼 문항이 고급(A)에 배치되어 있음 — **ρL/A 단일 대입은 중급 이하**.
- **그림 내부 모순 169건(E_FIG_INTERNAL)**: k=0 주제도에서 `ar` 과 depth/dia 가 다름(예: TSV-B-0088 ar 13, 80/4=20). 주제도에 무관한 void/pinch 결함을 그림(W_FIG_K0_DEFECT).
- **ctx 조립형(227문항)의 질 저하**: 공유 ctx(도금·CMP 서술)가 qt 와 무관(TSV-B-0088 "TSV가 열을 빼는 통로…"), 오답이 기술 외 사유("규정으로 정해져 있기 때문", TSV-B-0089), 해설이 번호 나열("②①④은 기술적 근거가 아니다").
- **기술 정정 후보**: TSV-B-0106 "도금 전류밀도가 높으면 결정립 조대" — 고전류밀도는 핵생성 증가로 결정립이 미세해지는 경향이며 주된 문제는 conformal 성장에 따른 pinch-off/void 다. 정답·해설 재검토. TSV-A-0142 "KOZ 축소 → 셀 리텐션 산포 확대" 는 근거 약함(KOZ 의 1차 영향은 주변 트랜지스터 이동도·Vt 변동). TSV-A-0058 SAC305 는 HBM µbump 재료(SnAg)와 맞지 않음.
- **조사·표기**: "void 은", "pinch-off 은"(TSV-B-0042 등 해설 템플릿), "형태이 반복적으로"(TSV-I-0010), "Void이", "Unfilled이".
- **f_warp 를 열팽창 차 계산(TSV-I-0062, TSV-A-0058)에 사용** — 그림이 warpage 명명표를 보여 주어 문항과 무관. f_plot 또는 f_note 로 교체.

## 3. 핵심 개념 체크리스트와 현재 커버리지

키워드 기반 근사치(지문·보기·해설에서 해당 주제가 다뤄진 문항 수). 0–4 = **공백**, 5–14 = 부족, 15+ = 있음(질은 별도 판단).

| 주제 | 초급 | 중급 | 고급 | 판정 |
|---|---|---|---|---|
| via-middle/first/last 통합 순서 | 1 | 3 | 2 | 부족 |
| Bosch DRIE·scallop | 22 | 31 | 4 | 있음 |
| liner 증착(SACVD/PECVD TEOS·피복률) | 37 | 62 | 35 | 있음 |
| barrier/seed PVD·ALD | 38 | 62 | 37 | 있음 |
| ECD 첨가제(accelerator/suppressor/leveler) | 16 | 5 | 24 | 있음 |
| bottom-up/superfill·void·seam·pinch-off | 21 | 29 | 0 | 고급 없음 |
| anneal·Cu pumping/protrusion | 1 | 42 | 32 | 있음 |
| CMP overburden·dishing/erosion | 1 | 25 | 1 | 있음 |
| KOZ·TSV 응력(이동도·Vt 변동) | 1 | 6 | 5 | 부족 |
| TSV RC·MOS 커패시턴스 | 0 | 0 | 0 | **공백** |
| TSV 밀도·pitch·HBM당 TSV 수 | 1 | 6 | 6 | 부족 |
| thermal TSV·dummy | 0 | 0 | 0 | **공백** |
| TSV 저항 계산 | 30 | 86 | 100 | 있음 |

**우선 보강 공백**: TSV RC·MOS 커패시턴스, thermal/dummy TSV, KOZ 와 응력에 의한 소자 특성 변화, via-middle 통합 순서와 열예산, HBM 세대별 TSV 수·pitch, ECD 첨가제 기구(accelerator/suppressor/leveler 의 역할 분담), 측벽 피복률 계측

## 4. 작업 지시 (우선순위 순)

1. **사실 오류·정답 오류 먼저**: §2 의 기술 정정 후보, `E_EXP_REF_ANSWER`(정답 키 재검증), NUM·FACT 에이전트 결과(`docs/reviews/num/TSV.md`, `docs/reviews/_facts.md`)를 반영한다.
2. **템플릿 가족 정리**: `E_FAMILY_OVER` 대상은 가족당 3개(가능하면 난이도별 1개)만 남기고 삭제하거나 다른 판단을 묻도록 재작성. 근중복(`W_NEAR_DUP`)도 정리.
3. **ctx 조립형 정리**: ctx 가 qt 풀이에 필요 없으면 stem 단일형으로 변환. 기술 외 사유 오답·타 분야 오답(`W_OPT_WEAK`) 교체, 형식 단서(`W_OPT_ODD_END`, `W_OPT_LONGEST`, `W_OPT_ABSOLUTE`) 제거.
4. **해설 재작성**: `E_EXP_SHORT`·`E_EXP_ONLY_REFS`·`E_STYLE_PLAIN`·`W_EXP_DISTRACTORS` — 정답 근거 + 오답 3개 각각의 오류 + (계산) 식·대입·결과. 일괄 `[근거]` 꼬리표는 고친 해설에서 뺀다.
5. **제목·지표·그림**: `E_TITLE_TRUNC`·`W_TITLE_*` 제목 재작성, `E_META_METRICS` 지표를 지문 조건으로 교체, `E_K1_FIG_NUM`·`E_FIG_ANSWER_LEAK`·`E_FIG_INTERNAL`·`W_FIG_*` 그림 params 정정.
6. **난이도 재배치**: 단순 대입 계산·용어 문항이 고급이면 lv 를 내린다. lv 가 바뀌면 id 의 LV 도 달라져야 하므로 **새 id(`CODE-LV-9xxx`)를 발급하고 `"prev": "옛 id"` 필드를 남긴다**(보고서에 old→new 기록). 고급은 STANDARDS §1 기준으로 채운다.
7. **신규 출제**(§5) — 공백 주제 위주. 새 id 는 `TSV-LV-9001` 부터.
8. 타 분야 문항은 고쳐서 `"mv": "CODE"` 로 이관 제안(EA 가 Phase 2 에서 이동) 하거나 자기 분야 관점으로 재작성.

## 5. 추가 출제 목표

| | 초급 | 중급 | 고급 | 합계 |
|---|---|---|---|---|
| 신규 최소 | 10 | 25 | 25 | 60 |

- 가족 초과로 정리될 문항 약 124 건은 위 신규로 대체한다(수량 유지보다 질 우선, 최종 분야 규모는 ±10 % 허용).
- 최종 난이도 비율 권장: 초급 25–30 % · 중급 35–40 % · 고급 30–35 %.

- 중급: 첨가제 3종의 역할과 bottom-up 충전 조건, liner 두께와 TSV 커패시턴스(동축 커패시터 식), Cu pumping 의 ΔαΔT 추정, via-middle 에서 TSV 를 contact 이후·BEOL 이전에 두는 열예산 근거, KOZ 정의
- 고급: TSV 커패시턴스 + 저항으로 RC 지연·신호 부담 추정(2식 연결), anneal 조건 vs protrusion vs BEOL crack 트레이드오프(3변수), 단면 SEM·저항 산포·열이력 후 변화 3개 관측으로 결함 기구 특정, HBM4 (I/O 2배)에서 TSV 수·pitch 증가가 KOZ·die 면적에 주는 영향 추정, thermal TSV 추가 시 열저항 감소와 면적 비용

## 6. 사용할 그림 템플릿과 params

| 템플릿 | params | 제약 · 주의 |
|---|---|---|
| `f_tsv` | `dia_um`, `depth_um`, `ar`, `fill`: good·void·seam·pinch, `scallop`: 0·1, `scallopPitch`(µm), `scallopDepth`(nm), `barrier`: bool, `overburden`: bool, `taper`(하단/상단 폭 비, 기본 0.82) | `ar` = depth/dia (소수 1자리). scallop 수치는 scallop=0 이어도 오른쪽에 표시됨(DA 수정 요청 중) → k=1 이면 지문과 맞추거나 생략 시 기본 0.35 µm·60 nm 가 그려짐 |
| `f_cmp` | `densA`, `densB`(%), `dish_nm`, `erosion_nm`, `nA`, `nB`(격자 수, 시각용) | 오른쪽 그래프는 고정 경향선(x축 0–60 %) |
| `f_warp` | `ref`: bump-down·beol-up, `sign`: 1(중앙이 기준면에서 멂)·−1(가까움), `mag_um`, `tg`, `temp` | 명명 표가 본 기준서 2.5 와 다름 → 수정 전 Smile/Cry 명칭 판정 문항에 쓰지 말 것 |
| `f_plot` | `title`, `x`{min,max,ticks,lab}, `y`{…}, `series`[{name, color(“RRGGBB”), pts[[x,y]], dash}], `marks`[[x, 라벨]], `bullets`[…] | 데이터 해석형 고급 문항의 주력 템플릿 |
| `f_note` | `title`, `points`(≤ 4), `ask` | 정답 문장 금지 |

- 비고: f_warp(열팽창 계산 문항 — 부적합, 교체 권장)

- `f_tsv` 의 `ar` 은 반드시 depth/dia (소수 1자리)로 맞춘다. k=0 주제도는 `fill: "good"`, `scallop: 0` 으로 중립화.
- 저항 가족은 3개만 남기고(초·중·고 각 1, 고급은 barrier·계면 저항까지 포함한 다단 추정으로 재작성), 나머지 삭제.
- 데이터 해석형 고급에 표가 필요하면 `f_plot`(그래프)으로 우선 해결하고, 표 템플릿(`f_table`)은 DA 에 요청 중(`EA_to_DA.md`). 확정 전에는 표 데이터를 지문 안 문장으로 쓴다.

## 7. 완료 조건

- `python3 tools/validate.py --domain TSV --gate` 통과(차단 E 0). 남는 W 는 수정 또는 `vx` + 사유.
- `python3 tools/build.py` · `node tools/smoke.js dist/HBM_quiz.html` 오류 없음.
- 보고서 `docs/reviews/TSV.md` (형식: ROSTER §4).
