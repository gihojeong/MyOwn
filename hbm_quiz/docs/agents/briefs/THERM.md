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
- **차단 E 이슈가 있는 문항: 452 / 537** (E_JOSA_CIRC 는 EA Phase 2 일괄 처리라 제외)

## 1. 자동 검사 요약 (기준선)

| 코드 | 건수 | 예시 id |
|---|---|---|
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
| `W_EXP_OFFTOPIC` | 3 | WARP-A-0181, WARP-A-0195, WARP-B-0085 |
| `W_FIG_TOPIC` | 1 | WARP-B-0139 |
| `W_OPT_PUNCT` | 1 | WARP-A-0220 |
| `I_EXP_SRC_TAG` | 341 | WARP-A-0050, WARP-A-0051, WARP-A-0052, WARP-A-0053 |

(참고: `I_JOSA_SPACE` 483 · `I_TEMPLATE_JOIN` 118 — 새로 쓰는 문장은 조사를 붙여 쓰고, ctx 조립형은 STANDARDS 3.1 에 따라 정리)

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

1. **사실 오류·정답 오류 먼저**: §2 의 기술 정정 후보, `E_EXP_REF_ANSWER`(정답 키 재검증), NUM·FACT 에이전트 결과(`docs/reviews/num/THERM.md`, `docs/reviews/_facts.md`)를 반영한다.
2. **템플릿 가족 정리**: `E_FAMILY_OVER` 대상은 가족당 3개(가능하면 난이도별 1개)만 남기고 삭제하거나 다른 판단을 묻도록 재작성. 근중복(`W_NEAR_DUP`)도 정리.
3. **ctx 조립형 정리**: ctx 가 qt 풀이에 필요 없으면 stem 단일형으로 변환. 기술 외 사유 오답·타 분야 오답(`W_OPT_WEAK`) 교체, 형식 단서(`W_OPT_ODD_END`, `W_OPT_LONGEST`, `W_OPT_ABSOLUTE`) 제거.
4. **해설 재작성**: `E_EXP_SHORT`·`E_EXP_ONLY_REFS`·`E_STYLE_PLAIN`·`W_EXP_DISTRACTORS` — 정답 근거 + 오답 3개 각각의 오류 + (계산) 식·대입·결과. 일괄 `[근거]` 꼬리표는 고친 해설에서 뺀다.
5. **제목·지표·그림**: `E_TITLE_TRUNC`·`W_TITLE_*` 제목 재작성, `E_META_METRICS` 지표를 지문 조건으로 교체, `E_K1_FIG_NUM`·`E_FIG_ANSWER_LEAK`·`E_FIG_INTERNAL`·`W_FIG_*` 그림 params 정정.
6. **난이도 재배치**: 단순 대입 계산·용어 문항이 고급이면 lv 를 내린다. lv 가 바뀌면 id 의 LV 도 달라져야 하므로 **새 id(`CODE-LV-9xxx`)를 발급하고 `"prev": "옛 id"` 필드를 남긴다**(보고서에 old→new 기록). 고급은 STANDARDS §1 기준으로 채운다.
7. **신규 출제**(§5) — 공백 주제 위주. 새 id 는 `THERM-LV-9001` 부터.
8. 타 분야 문항은 고쳐서 `"mv": "CODE"` 로 이관 제안(EA 가 Phase 2 에서 이동) 하거나 자기 분야 관점으로 재작성.

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
| `f_therm` | `n`(**base 포함 총 die 수**), `q_Wmm2`, `tTop`(°C), `limit`(°C), `layers`: [[이름, 두께 µm, k W/m·K], …] (간극 1개를 지나는 층) | 그림이 ΔT = q·ΣR, base = tTop + ΔT·(n−1) 을 계산해 표시 → 지문의 N단(core 수)과 n 관계 주의: N단이면 n = N+1 |
| `f_sip` | `type`: cowos-s·cowos-r·cowos-l·emib·emib-t, `nHBM` 1–4, `bullet` | "2,048선" 라벨 고정(HBM3E 문항과 모순 주의) |
| `f_plot` | `title`, `x`{min,max,ticks,lab}, `y`{…}, `series`[{name, color(“RRGGBB”), pts[[x,y]], dash}], `marks`[[x, 라벨]], `bullets`[…] | 데이터 해석형 고급 문항의 주력 템플릿 |
| `f_note` | `title`, `points`(≤ 4), `ask` | 정답 문장 금지 |
| `f_stack` | `n`(**core die 수**), `highlight`: null·height·midcore·base·gap·topcore, `gap_um`, `h_um`, `limit_um`, `bullet` | 표에 die n+1, 간극 n, 높이 h_um 표시 → 계산 답을 h_um/n 에 넣지 말 것 |



- `f_therm.n` = base 포함 총 die 수(N단 → n = N+1), `layers` 는 지문의 층 두께·열전도율과 정확히 일치. 결과 온도(base die)는 그림이 계산해 표시하므로 그 온도를 묻는 문항은 DA 의 결과 숨김 옵션 도입 전까지 k=0 으로.
- 가족은 유형별 3개(1D 누적 / 총 발열 / 단위 환산 / TIM / 계면 ΔT / 냉각 예산 …), 나머지는 위 공백 주제로 대체.
- 데이터 해석형 고급에 표가 필요하면 `f_plot`(그래프)으로 우선 해결하고, 표 템플릿(`f_table`)은 DA 에 요청 중(`EA_to_DA.md`). 확정 전에는 표 데이터를 지문 안 문장으로 쓴다.

## 7. 완료 조건

- `python3 tools/validate.py --domain THERM --gate` 통과(차단 E 0). 남는 W 는 수정 또는 `vx` + 사유.
- `python3 tools/build.py` · `node tools/smoke.js dist/HBM_quiz.html` 오류 없음.
- 보고서 `docs/reviews/THERM.md` (형식: ROSTER §4).
