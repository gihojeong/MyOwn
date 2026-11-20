# MIX 분야 브리프 — 복합 판단

- 소유 파일: `data/11_MIX.json` · 기준: `docs/agents/STANDARDS.md` · 자동 검사: `python3 tools/validate.py --domain MIX`
- 작성: EA (Phase 1, 2026-11-20) · 기준선 리포트: `docs/reviews/_auto_baseline.md`

## 0. 현황

| 난이도 | 문항 | stem 단일형 | ctx 조립형 | 정답 위치 ①/②/③/④ |
|---|---|---|---|---|
| 초급 | 44 | 0 | 44 | 12 / 5 / 12 / 15 |
| 중급 | 70 | 0 | 70 | 20 / 20 / 15 / 15 |
| 고급 | 103 | 0 | 103 | 21 / 28 / 30 / 24 |
| 합계 | 217 | 0 | 217 | |

- k=1 상황도 0 · k=0 주제도 217 · 그림 사용: f_note 217
- **차단 E 이슈가 있는 문항: 217 / 217** (E_JOSA_CIRC 는 EA Phase 2 일괄 처리라 제외)

## 1. 자동 검사 요약 (기준선)

| 코드 | 건수 | 예시 id |
|---|---|---|
| `E_META_METRICS` | 217 | MIX-A-0001, MIX-A-0002, MIX-A-0003, MIX-A-0004 |
| `E_EXP_SHORT` | 188 | MIX-A-0012, MIX-A-0014, MIX-A-0016, MIX-A-0018 |
| `E_JOSA_CIRC` | 179 | MIX-A-0001, MIX-A-0002, MIX-A-0003, MIX-A-0004 |
| `E_STYLE_PLAIN` | 172 | MIX-A-0001, MIX-A-0002, MIX-A-0003, MIX-A-0004 |
| `E_TITLE_TRUNC` | 152 | MIX-A-0001, MIX-A-0002, MIX-A-0003, MIX-A-0004 |
| `E_EXP_ONLY_REFS` | 151 | MIX-A-0021, MIX-A-0022, MIX-A-0023, MIX-A-0024 |
| `E_JOSA_EN` | 6 | MIX-A-0004, MIX-I-0014, MIX-I-0016 |
| `E_EXP_REF_ANSWER` | 5 | MIX-A-0025, MIX-B-0007, MIX-B-0008, MIX-I-0016 |
| `E_DOUBLE_Q` | 1 | MIX-A-0005 |
| `W_TITLE_COPY` | 217 | MIX-A-0001, MIX-A-0002, MIX-A-0003, MIX-A-0004 |
| `W_TITLE_QUESTION` | 61 | MIX-A-0008, MIX-A-0024, MIX-A-0028, MIX-A-0033 |
| `W_OPT_ODD_END` | 45 | MIX-A-0020, MIX-A-0022, MIX-A-0023, MIX-A-0029 |
| `W_OPT_WEAK` | 28 | MIX-A-0003, MIX-A-0029, MIX-A-0043, MIX-A-0048 |
| `W_OPT_LONGEST` | 19 | MIX-A-0002, MIX-A-0003, MIX-A-0004, MIX-A-0011 |
| `W_EXP_DISTRACTORS` | 12 | MIX-A-0025, MIX-A-0058, MIX-B-0007, MIX-B-0008 |
| `W_OPT_ABSOLUTE` | 11 | MIX-A-0007, MIX-A-0041, MIX-A-0054, MIX-A-0060 |
| `W_EXP_OFFTOPIC` | 1 | MIX-I-0019 |
| `W_OPT_STEM_ECHO` | 1 | MIX-A-0037 |
| `W_NEAR_DUP_X` | 1 | MIX-I-0013 |
| `W_NEAR_DUP` | 1 | MIX-I-0007 |

(참고: `I_JOSA_SPACE` 0 · `I_TEMPLATE_JOIN` 217 — 새로 쓰는 문장은 조사를 붙여 쓰고, ctx 조립형은 STANDARDS 3.1 에 따라 정리)

## 2. 표본 조사로 확인한 대표 결함 (EA 직접 판독: 난이도별 10문항 이상)

- **217문항 전부 ctx 조립형 + f_note, 전부 E 이슈 보유.** 대부분 HBM 고유 내용이 없는 일반론("불량이 같은 좌표에서 반복되면 위치 고정 요인", MIX-B-0021 ≈ MIX-I-0005 ≈ MIX-I-0031 근중복).
- **지시 대상 없는 지시어**: "이 상충을 근본적으로 우회하는 기술 방향"(MIX-A-0008) — 앞 문항을 전제로 한 문장.
- **해설이 정답을 오답으로 5건**(MIX-I-0028 "④①③은 기술 항목이 아니다" a=④, MIX-B-0007 등).
- 무의미·타 분야 오답("색상, 무게, 크기, 포장", "가격, 납기, 재고, 수요", MIX-B-0004).
- `f_note.points` 가 정답 문장을 거의 그대로 제시(그림이 답을 알려 줌).

## 3. 핵심 개념 체크리스트와 현재 커버리지

키워드 기반 근사치(지문·보기·해설에서 해당 주제가 다뤄진 문항 수). 0–4 = **공백**, 5–14 = 부족, 15+ = 있음(질은 별도 판단).

| 주제 | 초급 | 중급 | 고급 | 판정 |
|---|---|---|---|---|
| 두께 예산(die+gap+mold) × 열 × 수율 통합 판단 | 8 | 15 | 15 | 있음 |
| 공법 선택(TC-NCF/MR-MUF/HCB) 다변수 비교 | 0 | 2 | 0 | **공백** |
| 불량 원인 규명(다중 데이터) | 7 | 7 | 17 | 있음 |
| 수치 추정(Fermi) | 0 | 0 | 1 | **공백** |
| 데이터 해석(분포·맵·추세) | 2 | 4 | 8 | 부족 |
| 비용·수율 트레이드오프 | 3 | 8 | 24 | 있음 |

**우선 보강 공백**: '복합 판단' 의 본래 목적 — 여러 분야 지식을 동시에 써야 하는 **사례 기반 문항** — 이 사실상 없음. 두께 예산 × 열 × 수율, 공법 선택 다변수 비교, 다중 데이터 원인 규명, Fermi 추정이 각각 0–24건.

## 4. 작업 지시 (우선순위 순)

1. **사실 오류·정답 오류 먼저**: §2 의 기술 정정 후보, `E_EXP_REF_ANSWER`(정답 키 재검증), NUM·FACT 에이전트 결과(`docs/reviews/num/MIX.md`, `docs/reviews/_facts.md`)를 반영한다.
2. **템플릿 가족 정리**: `E_FAMILY_OVER` 대상은 가족당 3개(가능하면 난이도별 1개)만 남기고 삭제하거나 다른 판단을 묻도록 재작성. 근중복(`W_NEAR_DUP`)도 정리.
3. **ctx 조립형 정리**: ctx 가 qt 풀이에 필요 없으면 stem 단일형으로 변환. 기술 외 사유 오답·타 분야 오답(`W_OPT_WEAK`) 교체, 형식 단서(`W_OPT_ODD_END`, `W_OPT_LONGEST`, `W_OPT_ABSOLUTE`) 제거.
4. **해설 재작성**: `E_EXP_SHORT`·`E_EXP_ONLY_REFS`·`E_STYLE_PLAIN`·`W_EXP_DISTRACTORS` — 정답 근거 + 오답 3개 각각의 오류 + (계산) 식·대입·결과. 일괄 `[근거]` 꼬리표는 고친 해설에서 뺀다.
5. **제목·지표·그림**: `E_TITLE_TRUNC`·`W_TITLE_*` 제목 재작성, `E_META_METRICS` 지표를 지문 조건으로 교체, `E_K1_FIG_NUM`·`E_FIG_ANSWER_LEAK`·`E_FIG_INTERNAL`·`W_FIG_*` 그림 params 정정.
6. **난이도 재배치**: 단순 대입 계산·용어 문항이 고급이면 lv 를 내린다. lv 가 바뀌면 id 의 LV 도 달라져야 하므로 **새 id(`CODE-LV-9xxx`)를 발급하고 `"prev": "옛 id"` 필드를 남긴다**(보고서에 old→new 기록). 고급은 STANDARDS §1 기준으로 채운다.
7. **신규 출제**(§5) — 공백 주제 위주. 새 id 는 `MIX-LV-9001` 부터.
8. 타 분야 문항은 고쳐서 `"mv": "CODE"` 로 이관 제안(EA 가 Phase 2 에서 이동) 하거나 자기 분야 관점으로 재작성.

## 5. 추가 출제 목표

| | 초급 | 중급 | 고급 | 합계 |
|---|---|---|---|---|
| 신규 최소 | 15 | 40 | 80 | 135 |

- 기존 문항 정리(삭제·재작성) 규모는 §2 에 따른다. 최종 분야 규모는 질 우선으로 정한다.
- 최종 난이도 비율 권장: 초급 25–30 % · 중급 35–40 % · 고급 30–35 %.

- **분야 재구축**: 기존 217 중 HBM 고유성이 있는 것만 재작성(목표 ≤ 60), 나머지 삭제. 신규는 **사례 세트**(공유 ctx 1개 + 3–5개 문항) 방식 권장 — ctx 조립형을 '제대로' 쓰는 유일한 분야.
- 사례 예: ① HBM4 16-Hi 를 775 µm 에 넣는 계획(die 두께·간극·접합 방식·열저항·KGD 수율), ② 신뢰성 시험 후 저항 상승 lot 의 원인 규명(TC 데이터 + SAT + 단면), ③ HCB 전환 시 CMP·세정·dicing·검사 변경점 연쇄, ④ 2.5D 패키지에서 HBM 수 증가 시 interposer 면적·warpage·수율, ⑤ 고온 동작(95 °C) 에서 refresh·열·신뢰성 트레이드오프.
- 고급 80 중 최소 30은 표·그래프 데이터 해석(`f_plot`, 신규 `f_table`).

## 6. 사용할 그림 템플릿과 params

| 템플릿 | params | 제약 · 주의 |
|---|---|---|
| `f_note` | `title`, `points`(≤ 4), `ask` | 정답 문장 금지 |
| `f_plot` | `title`, `x`{min,max,ticks,lab}, `y`{…}, `series`[{name, color(“RRGGBB”), pts[[x,y]], dash}], `marks`[[x, 라벨]], `bullets`[…] | 데이터 해석형 고급 문항의 주력 템플릿 |
| `f_stack` | `n`(**core die 수**), `highlight`: null·height·midcore·base·gap·topcore, `gap_um`, `h_um`, `limit_um`, `bullet` | 표에 die n+1, 간극 n, 높이 h_um 표시 → 계산 답을 h_um/n 에 넣지 말 것 |
| `f_therm` | `n`(**base 포함 총 die 수**), `q_Wmm2`, `tTop`(°C), `limit`(°C), `layers`: [[이름, 두께 µm, k W/m·K], …] (간극 1개를 지나는 층) | 그림이 ΔT = q·ΣR, base = tTop + ΔT·(n−1) 을 계산해 표시 → 지문의 N단(core 수)과 n 관계 주의: N단이면 n = N+1 |
| `f_bond` | `method`: ncf·mrmuf·hcb, `pitch_um`, `gap_um`, `voids` 0–3, `filler_trap`(ncf), `nonwet`, `bullet` | hcb 분기는 항상 dishing 미접합 pad 를 그리고 "gap" 치수를 표시(DA 요청 중) → hcb 에 bump 간극 수치를 주지 말 것 |
| `f_hcb` | `pitch_um`, `tol_nm`, `off_nm`, `dish_nm`, `bullet` | 허용치 대비 초과/이내를 그림이 판정해 표시 → 판정이 답이면 정답 노출 |

- 비고: f_note(현재 전부)
- 비고: (신규 요청) f_table
- 사례 세트는 ctx 를 공유하고 각 문항 qt 가 서로 다른 판단을 묻는다. `j` 연결구는 0(기본)만 쓰거나 ctx 끝을 자연스럽게 맺는다.
- 데이터 해석형 고급에 표가 필요하면 `f_plot`(그래프)으로 우선 해결하고, 표 템플릿(`f_table`)은 DA 에 요청 중(`EA_to_DA.md`). 확정 전에는 표 데이터를 지문 안 문장으로 쓴다.

## 7. 완료 조건

- `python3 tools/validate.py --domain MIX --gate` 통과(차단 E 0). 남는 W 는 수정 또는 `vx` + 사유.
- `python3 tools/build.py` · `node tools/smoke.js dist/HBM_quiz.html` 오류 없음.
- 보고서 `docs/reviews/MIX.md` (형식: ROSTER §4).
