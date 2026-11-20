# WARP 분야 브리프 — Warpage 와 열 설계

- 소유 파일: `data/05_WARP.json` · 기준: `docs/agents/STANDARDS.md` · 자동 검사: `python3 tools/validate.py --domain WARP`
- 작성: EA (Phase 1, 2026-11-20) · 기준선 리포트: `docs/reviews/_auto_baseline.md`

## 0. 현황

| 난이도 | 문항 | stem 단일형 | ctx 조립형 | 정답 위치 ①/②/③/④ |
|---|---|---|---|---|
| 초급 | 154 | 62 | 92 | 41 / 41 / 29 / 43 |
| 중급 | 326 | 234 | 92 | 91 / 74 / 76 / 85 |
| 고급 | 283 | 166 | 117 | 82 / 71 / 71 / 59 |
| 합계 | 763 | 462 | 301 | |

- k=1 상황도 462 · k=0 주제도 301 · 그림 사용: f_therm 477, f_bond 130, f_warp 97, f_sip 55, f_hcb 2, f_stack 1, f_note 1
- **차단 E 이슈가 있는 문항: 662 / 763** (E_JOSA_CIRC 는 EA Phase 2 일괄 처리라 제외)

## 1. 자동 검사 요약 (기준선)

| 코드 | 건수 | 예시 id |
|---|---|---|
| `E_META_METRICS` | 301 | WARP-A-0167, WARP-A-0168, WARP-A-0169, WARP-A-0170 |
| `E_JOSA_CIRC` | 265 | WARP-A-0167, WARP-A-0168, WARP-A-0169, WARP-A-0170 |
| `E_K1_FIG_NUM` | 255 | WARP-A-0002, WARP-A-0033, WARP-A-0034, WARP-A-0035 |
| `E_STYLE_PLAIN` | 232 | WARP-A-0167, WARP-A-0168, WARP-A-0169, WARP-A-0170 |
| `E_TITLE_TRUNC` | 228 | WARP-A-0167, WARP-A-0168, WARP-A-0169, WARP-A-0170 |
| `E_FAMILY_OVER` | 211 | WARP-A-0006, WARP-A-0007, WARP-A-0008, WARP-A-0009 |
| `E_EXP_SHORT` | 206 | WARP-A-0183, WARP-A-0184, WARP-A-0208, WARP-A-0209 |
| `E_EXP_ONLY_REFS` | 146 | WARP-A-0209, WARP-A-0210, WARP-A-0212, WARP-A-0213 |
| `E_JOSA_EN` | 100 | WARP-A-0002, WARP-A-0175, WARP-A-0182, WARP-A-0184 |
| `E_EXP_REF_ANSWER` | 5 | WARP-A-0267, WARP-B-0100, WARP-I-0284, WARP-I-0285 |
| `E_FIG_ANSWER_LEAK` | 2 | WARP-A-0039, WARP-I-0207 |
| `E_TEXT_DUP_PAREN` | 2 | WARP-B-0074 |
| `E_DOUBLE_Q` | 2 | WARP-B-0121, WARP-B-0132 |
| `E_CALC_NO_WORK` | 1 | WARP-A-0057 |
| `W_EXP_DISTRACTORS` | 409 | WARP-A-0001, WARP-A-0003, WARP-A-0004, WARP-A-0005 |
| `W_K1_FIG_EXTRA` | 369 | WARP-A-0001, WARP-A-0002, WARP-A-0050, WARP-A-0051 |
| `W_META_METRICS` | 334 | WARP-A-0050, WARP-A-0052, WARP-A-0053, WARP-A-0054 |
| `W_NEAR_DUP` | 305 | WARP-A-0060, WARP-A-0061, WARP-A-0062, WARP-A-0063 |
| `W_TITLE_COPY` | 301 | WARP-A-0167, WARP-A-0168, WARP-A-0169, WARP-A-0170 |
| `W_K1_METRIC_NUM` | 180 | WARP-A-0001, WARP-A-0002, WARP-A-0003, WARP-A-0004 |
| `W_OPT_ODD_END` | 109 | WARP-A-0190, WARP-A-0196, WARP-A-0207, WARP-A-0208 |
| `W_TITLE_QUESTION` | 73 | WARP-A-0210, WARP-A-0233, WARP-A-0252, WARP-A-0261 |
| `W_OPT_WEAK` | 67 | WARP-A-0179, WARP-A-0190, WARP-A-0195, WARP-A-0199 |
| `W_OPT_LONGEST` | 32 | WARP-A-0050, WARP-A-0052, WARP-A-0053, WARP-A-0054 |
| `W_OPT_ABSOLUTE` | 18 | WARP-A-0057, WARP-A-0180, WARP-A-0220, WARP-A-0221 |
| `W_EXP_OFFTOPIC` | 8 | WARP-A-0181, WARP-A-0195, WARP-B-0070, WARP-B-0073 |
| `W_FIG_LEAK` | 5 | WARP-A-0002, WARP-I-0027, WARP-I-0028, WARP-I-0029 |
| `W_FIG_TOPIC` | 2 | WARP-A-0235, WARP-B-0139 |
| `W_EXP_REF_MISMATCH` | 2 | WARP-A-0173, WARP-A-0192 |
| `W_OPT_PUNCT` | 2 | WARP-A-0219, WARP-A-0220 |
| `W_NEAR_DUP_X` | 1 | WARP-B-0147 |
| `I_EXP_SRC_TAG` | 341 | WARP-A-0050, WARP-A-0051, WARP-A-0052, WARP-A-0053 |

(참고: `I_JOSA_SPACE` 666 · `I_TEMPLATE_JOIN` 301 — 새로 쓰는 문장은 조사를 붙여 쓰고, ctx 조립형은 STANDARDS 3.1 에 따라 정리)

## 2. 표본 조사로 확인한 대표 결함 (EA 직접 판독: 난이도별 10문항 이상)

- **규모 최대(763) · 가족 초과 211**: 1D 열저항 누적(WARP-A-0003 계열 30, -0033 계열 17), 열유속→총 발열(WARP-I-0031 계열 24), 열유속 W/cm² 환산, TIM 두께, 열 전용 TSV, 냉각수 예산, Tg 거동, Smile/Cry 명명.
- **비현실적 결과**: 최하단 die 154 °C, 236 °C, 397 °C 같은 보기를 정답으로 둔 문항(WARP-A-0031, -0032) — 균일 열유속이 모든 간극을 통과한다는 모델 + 과대 열유속. 또 "최상단 95 °C 로 유지, 상한 85 °C"(WARP-A-0031)처럼 **조건 자체가 이미 상한 초과**.
- **용어 충돌**: "12단 → 간극은 die 수보다 하나 적은 11개"(WARP-A-0003) — SIP 분야는 "core die 12장 → 간극 12개". STANDARDS 2.5 로 통일(N단 → 간극 N).
- **Smile/Cry 규약**: `f_warp` 표와 COW/BUMP 해설이 서로 반대 → STANDARDS 2.5 결정(위에서 본 형상: ∩ Cry, ∪ Smile)으로 정리. DA 가 표를 고치기 전에는 명칭 판정 문항에 f_warp 표를 근거로 쓰지 말 것.
- **검증 안 된 주장**: "보고된 HBM 스택의 열유속 범위 15~25 W/cm²"(WARP-B-0039 등 열유속 가족 해설), "iHBM 의 ICE"(WARP-B-0150, 업체 보도 기반) — 출처 [V] 확인 전 사용 금지.
- **타 분야 문항 혼재**: 연삭 냉각수(WARP-I-0283 → BSP), 낱개 접합 과제(WARP-B-0138 → COW), 접합층 두께(WARP-B-0102 → COW/PROD). `mv` 로 이관 제안.
- 열 계산 문항 다수가 `f_therm` 기본 층 구성(Si 30/BEOL 6/bond 9)을 지문과 다르게 그림(E_K1_FIG_NUM 255).

## 3. 핵심 개념 체크리스트와 현재 커버리지

키워드 기반 근사치(지문·보기·해설에서 해당 주제가 다뤄진 문항 수). 0–4 = **공백**, 5–14 = 부족, 15+ = 있음(질은 별도 판단).

| 주제 | 초급 | 중급 | 고급 | 판정 |
|---|---|---|---|---|
| CTE mismatch·bimetal(Stoney) | 22 | 3 | 5 | 있음 |
| EMC Tg·탄성률·cure shrinkage | 20 | 3 | 4 | 있음 |
| shadow moiré·DIC 측정 | 0 | 1 | 3 | **공백** |
| smile/cry 정의·부호 | 1 | 25 | 2 | 있음 |
| reflow 중 동적 warpage | 0 | 0 | 0 | **공백** |
| die/wafer warpage와 접합 불량 | 0 | 0 | 5 | 부족 |
| 1D 열저항·층별 ΔT | 3 | 162 | 161 | 있음 |
| TIM·lid·cold plate | 50 | 140 | 74 | 있음 |
| 열유속·전력 밀도 | 22 | 80 | 80 | 있음 |
| base die hotspot·logic 발열 | 0 | 1 | 2 | **공백** |
| DRAM 온도와 refresh(85/95 °C) | 2 | 5 | 50 | 있음 |
| thermal TSV/dummy bump | 0 | 32 | 23 | 있음 |
| 저항 네트워크·병렬/직렬 | 1 | 32 | 31 | 있음 |

**우선 보강 공백**: shadow moiré·DIC 측정 원리와 데이터 해석, reflow 중 동적 warpage(온도-휨 곡선)와 접합 불량, Stoney/bimetal 식 기반 휨 추정, EMC 조성(filler·Tg·CTE₁/CTE₂)과 휨 제어, die/wafer warpage → non-wet/short 분포, base die hotspot(로직 발열 분포)과 1D 모델 한계, 85/95 °C refresh 영역과 열 설계 연결

## 4. 작업 지시 (우선순위 순)

1. **사실 오류·정답 오류 먼저**: §2 의 기술 정정 후보, `E_EXP_REF_ANSWER`(정답 키 재검증), NUM·FACT 에이전트 결과(`docs/reviews/num/WARP.md`, `docs/reviews/_facts.md`)를 반영한다.
2. **템플릿 가족 정리**: `E_FAMILY_OVER` 대상은 가족당 3개(가능하면 난이도별 1개)만 남기고 삭제하거나 다른 판단을 묻도록 재작성. 근중복(`W_NEAR_DUP`)도 정리.
3. **ctx 조립형 정리**: ctx 가 qt 풀이에 필요 없으면 stem 단일형으로 변환. 기술 외 사유 오답·타 분야 오답(`W_OPT_WEAK`) 교체, 형식 단서(`W_OPT_ODD_END`, `W_OPT_LONGEST`, `W_OPT_ABSOLUTE`) 제거.
4. **해설 재작성**: `E_EXP_SHORT`·`E_EXP_ONLY_REFS`·`E_STYLE_PLAIN`·`W_EXP_DISTRACTORS` — 정답 근거 + 오답 3개 각각의 오류 + (계산) 식·대입·결과. 일괄 `[근거]` 꼬리표는 고친 해설에서 뺀다.
5. **제목·지표·그림**: `E_TITLE_TRUNC`·`W_TITLE_*` 제목 재작성, `E_META_METRICS` 지표를 지문 조건으로 교체, `E_K1_FIG_NUM`·`E_FIG_ANSWER_LEAK`·`E_FIG_INTERNAL`·`W_FIG_*` 그림 params 정정.
6. **난이도 재배치**: 단순 대입 계산·용어 문항이 고급이면 lv 를 내린다. lv 가 바뀌면 id 의 LV 도 달라져야 하므로 **새 id(`CODE-LV-9xxx`)를 발급하고 `"prev": "옛 id"` 필드를 남긴다**(보고서에 old→new 기록). 고급은 STANDARDS §1 기준으로 채운다.
7. **신규 출제**(§5) — 공백 주제 위주. 새 id 는 `WARP-LV-9001` 부터.
8. 타 분야 문항은 고쳐서 `"mv": "CODE"` 로 이관 제안(EA 가 Phase 2 에서 이동) 하거나 자기 분야 관점으로 재작성.

## 5. 추가 출제 목표

| | 초급 | 중급 | 고급 | 합계 |
|---|---|---|---|---|
| 신규 최소 | 15 | 35 | 45 | 95 |

- 가족 초과로 정리될 문항 약 211 건은 위 신규로 대체한다(수량 유지보다 질 우선, 최종 분야 규모는 ±10 % 허용).
- 최종 난이도 비율 권장: 초급 25–30 % · 중급 35–40 % · 고급 30–35 %.

- 고급: shadow moiré 온도 이력 데이터(승온·냉각 곡선, Tg 전후 기울기)로 실장 조건 판단, CTE·두께·모듈러스 3변수 bimetal 근사로 휨 방향·크기 추정, 열 모델에서 '발열이 각 die 에 분포' 할 때와 균일 열유속 가정의 차이 판단, TIM·lid·cold plate 예산 분배(직렬 열저항 3개 이상)
- 중급: Tg 전후 CTE 변화와 휨 방향, 측정 자세와 명칭(새 규약), thermal TSV/dummy bump 효과

## 6. 사용할 그림 템플릿과 params

| 템플릿 | params | 제약 · 주의 |
|---|---|---|
| `f_warp` | `ref`: bump-down·beol-up, `sign`: 1(중앙이 기준면에서 멂)·−1(가까움), `mag_um`, `tg`, `temp` | 명명 표가 본 기준서 2.5 와 다름 → 수정 전 Smile/Cry 명칭 판정 문항에 쓰지 말 것 |
| `f_therm` | `n`(**base 포함 총 die 수**), `q_Wmm2`, `tTop`(°C), `limit`(°C), `layers`: [[이름, 두께 µm, k W/m·K], …] (간극 1개를 지나는 층) | 그림이 ΔT = q·ΣR, base = tTop + ΔT·(n−1) 을 계산해 표시 → 지문의 N단(core 수)과 n 관계 주의: N단이면 n = N+1 |
| `f_bond` | `method`: ncf·mrmuf·hcb, `pitch_um`, `gap_um`, `voids` 0–3, `filler_trap`(ncf), `nonwet`, `bullet` | hcb 분기는 항상 dishing 미접합 pad 를 그리고 "gap" 치수를 표시(DA 요청 중) → hcb 에 bump 간극 수치를 주지 말 것 |
| `f_sip` | `type`: cowos-s·cowos-r·cowos-l·emib·emib-t, `nHBM` 1–4, `bullet` | "2,048선" 라벨 고정(HBM3E 문항과 모순 주의) |
| `f_plot` | `title`, `x`{min,max,ticks,lab}, `y`{…}, `series`[{name, color(“RRGGBB”), pts[[x,y]], dash}], `marks`[[x, 라벨]], `bullets`[…] | 데이터 해석형 고급 문항의 주력 템플릿 |
| `f_note` | `title`, `points`(≤ 4), `ask` | 정답 문장 금지 |



- `f_therm.n` 은 base 포함 총 die 수 → 지문이 "12단" 이면 n=13, 간극 12. 결과 온도를 지문 조건보다 현실 범위(대략 ≤ 110 °C)로 설계.
- 분할 편성 시(ROSTER §2) 열 설계 문항은 THERM 에이전트 소유.
- 데이터 해석형 고급에 표가 필요하면 `f_plot`(그래프)으로 우선 해결하고, 표 템플릿(`f_table`)은 DA 에 요청 중(`EA_to_DA.md`). 확정 전에는 표 데이터를 지문 안 문장으로 쓴다.

## 7. 완료 조건

- `python3 tools/validate.py --domain WARP --gate` 통과(차단 E 0). 남는 W 는 수정 또는 `vx` + 사유.
- `python3 tools/build.py` · `node tools/smoke.js dist/HBM_quiz.html` 오류 없음.
- 보고서 `docs/reviews/WARP.md` (형식: ROSTER §4).
