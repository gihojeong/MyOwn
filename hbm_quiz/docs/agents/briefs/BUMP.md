# BUMP 분야 브리프 — Bump 와 계면 금속

- 소유 파일: `data/02_BUMP.json` · 기준: `docs/agents/STANDARDS.md` · 자동 검사: `python3 tools/validate.py --domain BUMP`
- 작성: EA (Phase 1, 2026-11-20) · 기준선 리포트: `docs/reviews/_auto_baseline.md`

## 0. 현황

| 난이도 | 문항 | stem 단일형 | ctx 조립형 | 정답 위치 ①/②/③/④ |
|---|---|---|---|---|
| 초급 | 80 | 14 | 66 | 30 / 18 / 18 / 14 |
| 중급 | 160 | 102 | 58 | 45 / 34 / 38 / 43 |
| 고급 | 165 | 144 | 21 | 49 / 38 / 44 / 34 |
| 합계 | 405 | 260 | 145 | |

- k=1 상황도 260 · k=0 주제도 145 · 그림 사용: f_bump 394, f_plot 11
- **차단 E 이슈가 있는 문항: 349 / 405** (E_JOSA_CIRC 는 EA Phase 2 일괄 처리라 제외)

## 1. 자동 검사 요약 (기준선)

| 코드 | 건수 | 예시 id |
|---|---|---|
| `E_FAMILY_OVER` | 164 | BUMP-A-0006, BUMP-A-0007, BUMP-A-0008, BUMP-A-0009 |
| `E_META_METRICS` | 145 | BUMP-A-0145, BUMP-A-0146, BUMP-A-0147, BUMP-A-0148 |
| `E_JOSA_CIRC` | 136 | BUMP-A-0145, BUMP-A-0146, BUMP-A-0147, BUMP-A-0148 |
| `E_STYLE_PLAIN` | 117 | BUMP-A-0145, BUMP-A-0146, BUMP-A-0147, BUMP-A-0148 |
| `E_EXP_SHORT` | 98 | BUMP-A-0158, BUMP-A-0159, BUMP-A-0160, BUMP-A-0163 |
| `E_TITLE_TRUNC` | 92 | BUMP-A-0145, BUMP-A-0146, BUMP-A-0147, BUMP-A-0148 |
| `E_EXP_ONLY_REFS` | 66 | BUMP-A-0160, BUMP-A-0163, BUMP-A-0164, BUMP-A-0165 |
| `E_FIG_ANSWER_LEAK` | 44 | BUMP-A-0123, BUMP-A-0124, BUMP-A-0125, BUMP-A-0126 |
| `E_K1_FIG_NUM` | 23 | BUMP-A-0137, BUMP-A-0138, BUMP-A-0142, BUMP-A-0143 |
| `E_JOSA_EN` | 17 | BUMP-A-0151, BUMP-A-0152, BUMP-B-0019, BUMP-B-0027 |
| `E_DOUBLE_Q` | 6 | BUMP-B-0024, BUMP-B-0025, BUMP-B-0032, BUMP-B-0037 |
| `E_TEXT_DUP_PAREN` | 2 | BUMP-B-0020 |
| `E_CALC_NO_WORK` | 2 | BUMP-B-0032, BUMP-B-0080 |
| `W_K1_FIG_EXTRA` | 249 | BUMP-A-0001, BUMP-A-0003, BUMP-A-0004, BUMP-A-0005 |
| `W_EXP_DISTRACTORS` | 172 | BUMP-A-0001, BUMP-A-0002, BUMP-A-0003, BUMP-A-0004 |
| `W_TITLE_COPY` | 145 | BUMP-A-0145, BUMP-A-0146, BUMP-A-0147, BUMP-A-0148 |
| `W_META_METRICS` | 138 | BUMP-A-0043, BUMP-A-0044, BUMP-A-0045, BUMP-A-0046 |
| `W_NEAR_DUP` | 124 | BUMP-A-0102, BUMP-A-0105, BUMP-A-0106, BUMP-A-0107 |
| `W_K1_METRIC_NUM` | 89 | BUMP-A-0002, BUMP-A-0003, BUMP-A-0004, BUMP-A-0005 |
| `W_OPT_ODD_END` | 87 | BUMP-A-0152, BUMP-A-0153, BUMP-A-0159, BUMP-A-0161 |
| `W_TITLE_LEN` | 60 | BUMP-A-0101, BUMP-A-0102, BUMP-A-0103, BUMP-A-0104 |
| `W_TITLE_QUESTION` | 51 | BUMP-A-0163, BUMP-A-0164, BUMP-A-0165, BUMP-B-0019 |
| `W_OPT_WEAK` | 19 | BUMP-A-0158, BUMP-A-0159, BUMP-A-0164, BUMP-B-0028 |
| `W_OPT_ABSOLUTE` | 15 | BUMP-A-0002, BUMP-A-0033, BUMP-A-0034, BUMP-A-0035 |
| `W_OPT_LONGEST` | 13 | BUMP-A-0146, BUMP-B-0017, BUMP-B-0024, BUMP-B-0027 |
| `W_EXP_OFFTOPIC` | 4 | BUMP-A-0146, BUMP-A-0150, BUMP-B-0040, BUMP-I-0116 |
| `W_FIG_LEAK` | 1 | BUMP-B-0047 |
| `W_EXP_REF_MISMATCH` | 1 | BUMP-I-0108 |
| `W_OPT_STEM_ECHO` | 1 | BUMP-A-0160 |
| `I_EXP_SRC_TAG` | 108 | BUMP-A-0101, BUMP-A-0102, BUMP-A-0103, BUMP-A-0104 |

(참고: `I_JOSA_SPACE` 399 · `I_TEMPLATE_JOIN` 145 — 새로 쓰는 문장은 조사를 붙여 쓰고, ctx 조립형은 STANDARDS 3.1 에 따라 정리)

## 2. 표본 조사로 확인한 대표 결함 (EA 직접 판독: 난이도별 10문항 이상)

- **템플릿 가족 164문항 초과**: IMC √t 추정 30+28(BUMP-A-0003~, -0073~), 전류 밀도 30(BUMP-A-0043~), Kirkendall 판정 20(BUMP-I-0003~), current crowding 16(BUMP-I-0023~). 고급에 단순 대입 계산이 많음.
- **비현실적 설정**: pillar 1개에 0.15–0.35 A → 47–118 kA/cm²(BUMP-I-0055, -0062, BUMP-A-0102). µbump EM 시험은 10⁴ A/cm² 급. "IMC 8 µm 를 넘지 않을 것" 규격은 solder 두께 10–15 µm 급 µbump 에서 의미가 약함(오히려 full-IMC 전환이 쟁점).
- **해설 혼입**: BUMP-A-0150 해설 첫 문장이 Smile/Cry 명명 설명(다른 문항 해설) — W_EXP_OFFTOPIC.
- **치환 흔적**: "IMC(IMC)"(BUMP-B-0020), 제목 36자 초과 60건.
- **그림**: Ni barrier 조건에서도 IMC 라벨이 Cu₆Sn₅/Cu₃Sn 로 표시(DA 요청). 계산 문항에서 `imc_um` 에 정답 값을 넣어 그림이 답을 노출(E_FIG_ANSWER_LEAK 44, 예 BUMP-A-0124).
- ctx 조립형의 오답이 빈약("규정에 함께 있기 때문", "측정 장비가 하나이기 때문" — BUMP-B-0051).

## 3. 핵심 개념 체크리스트와 현재 커버리지

키워드 기반 근사치(지문·보기·해설에서 해당 주제가 다뤄진 문항 수). 0–4 = **공백**, 5–14 = 부족, 15+ = 있음(질은 별도 판단).

| 주제 | 초급 | 중급 | 고급 | 판정 |
|---|---|---|---|---|
| Cu pillar/µbump 구조·도금 | 14 | 102 | 74 | 있음 |
| SnAg solder·리플로 | 14 | 102 | 44 | 있음 |
| UBM·Ni barrier | 11 | 28 | 1 | 있음 |
| IMC(Cu6Sn5/Cu3Sn/Ni3Sn4)·성장 kinetics | 20 | 76 | 84 | 있음 |
| Kirkendall void | 1 | 22 | 0 | 고급 없음 |
| EM·current crowding·Black 식 | 0 | 51 | 52 | 있음 |
| full-IMC joint(미세 피치) | 0 | 0 | 0 | **공백** |
| bump 높이 coplanarity | 2 | 2 | 1 | 부족 |
| flux/fluxless·formic acid | 5 | 8 | 0 | 부족 |
| bridge·short·non-wet | 4 | 23 | 5 | 있음 |
| pitch 축소 한계(µbump → HCB) | 7 | 4 | 13 | 있음 |
| thermal/dummy bump | 0 | 0 | 0 | **공백** |

**우선 보강 공백**: full-IMC joint(미세 피치에서 solder 전량 IMC화)와 그 기계적 영향, bump 높이 coplanarity 와 접합 불량 분포, fluxless/formic acid 환원, dummy·thermal bump, Ni 존재 시 IMC 상(Ni₃Sn₄, (Cu,Ni)₆Sn₅), Black 식 기반 EM 수명 비교(n, Ea), µbump → HCB 전환 피치 경계

## 4. 작업 지시 (우선순위 순)

0. **[최우선] 메타 지표 제거 — 283건** (`E_META_METRICS` 145, `W_META_METRICS` 138). 화면 '제시 조건' 띠에 "난이도: 고급", "묻는 것: 해당 항목", "세부 주제", "핵심어" 가 그대로 보인다(DA 스크린샷 확인). 지문 조건 2–4개로 바꾸거나, 요약할 조건이 없으면 `"metrics": []`(키는 유지). 정답 오류 수정과 같은 1순위로 처리한다.
1. **사실 오류·정답 오류 먼저**: §2 의 기술 정정 후보, `E_EXP_REF_ANSWER`(정답 키 재검증), NUM·FACT 에이전트 결과(`docs/reviews/num/BUMP.md`, `docs/reviews/_facts.md`)를 반영한다.
2. **템플릿 가족 정리**: `E_FAMILY_OVER` 대상은 가족당 3개(가능하면 난이도별 1개)만 남기고 삭제하거나 다른 판단을 묻도록 재작성. 근중복(`W_NEAR_DUP`)도 정리.
3. **ctx 조립형 정리**: ctx 가 qt 풀이에 필요 없으면 stem 단일형으로 변환. 기술 외 사유 오답·타 분야 오답(`W_OPT_WEAK`) 교체, 형식 단서(`W_OPT_ODD_END`, `W_OPT_LONGEST`, `W_OPT_ABSOLUTE`) 제거.
4. **해설 재작성**: `E_EXP_SHORT`·`E_EXP_ONLY_REFS`·`E_STYLE_PLAIN`·`W_EXP_DISTRACTORS` — 정답 근거 + 오답 3개 각각의 오류 + (계산) 식·대입·결과. 일괄 `[근거]` 꼬리표는 고친 해설에서 뺀다.
5. **제목·지표·그림**: `E_TITLE_TRUNC`·`W_TITLE_*` 제목 재작성, `E_META_METRICS` 지표를 지문 조건으로 교체, `E_K1_FIG_NUM`·`E_FIG_ANSWER_LEAK`·`E_FIG_INTERNAL`·`W_FIG_*` 그림 params 정정.
6. **난이도 재배치**: 단순 대입 계산·용어 문항이 고급이면 lv 를 내린다. lv 가 바뀌면 id 의 LV 도 달라져야 하므로 **새 id(`CODE-LV-9xxx`)를 발급하고 `"prev": "옛 id"` 필드를 남긴다**(보고서에 old→new 기록). 고급은 STANDARDS §1 기준으로 채운다.
7. **신규 출제**(§5) — 공백 주제 위주. 새 id 는 `BUMP-LV-9001` 부터.
8. 타 분야 문항은 고쳐서 `"mv": "CODE"` 로 이관 제안(EA 가 Phase 2 에서 이동) 하거나 자기 분야 관점으로 재작성.

## 4A. DA Phase 1 템플릿 변경으로 손봐야 할 기존 문항

- 해당 문항 없음(검사기 기준). 새 문항은 STANDARDS 부록 A 를 따른다.

## 5. 추가 출제 목표

| | 초급 | 중급 | 고급 | 합계 |
|---|---|---|---|---|
| 신규 최소 | 15 | 25 | 30 | 70 |

- 가족 초과로 정리될 문항 약 164 건은 위 신규로 대체한다(수량 유지보다 질 우선, 최종 분야 규모는 ±10 % 허용).
- 최종 난이도 비율 권장: 초급 25–30 % · 중급 35–40 % · 고급 30–35 %.

- 고급: Black 식(j⁻ⁿ·exp(Ea/kT))으로 두 조건 수명 비 추정, full-IMC 전환 시점(√t 성장 + solder 두께) 추정과 신뢰성 함의, coplanarity 분포 + NCF 유동으로 non-wet/short 위치 예측, Ni 두께·Sn 소모·IMC 상 전환 판단
- 중급: Ni barrier 유무에 따른 IMC 상 차이, flux 잔사와 NCF, dummy bump 역할(열·기계)

## 6. 사용할 그림 템플릿과 params

| 템플릿 | params | 제약 · 주의 |
|---|---|---|
| `f_bump` | `pillar_um`, `solder_um`, `imc_um`, `niBarrier`(라벨 Ni₃Sn₄/(Cu,Ni)₆Sn₅), `kirkendall`, `em`+`j_kA`, `temp`, `k`, `hours`, `tmax`, `ymax`, `bullet` | 계산 결과를 `imc_um` 에 넣지 말 것(측정값만) |
| `f_plot` | `title`, `x`/`y`{min,max,ticks ≤ 6,lab}, `series` ≤ 4, `marks` ≤ 3, `bullets` ≤ 3 | 데이터 해석형 고급의 주력 |
| `f_note` | `title` ≤ 22자, `points` ≤ 4(각 ≤ 50자), `ask` ≤ 12자 | points 는 **판단 관점** — 정답 문장 금지 |


- `em: true` 문항의 `j_kA` 는 지문 전류밀도와 같게, 현실 범위(수~수십 kA/cm²) 안으로. 계산 결과를 `imc_um` 에 넣지 말 것(측정값만).
- 데이터 해석형 고급에는 `f_table`(표)·`f_wafermap`(맵)·`f_plot`(그래프)을 쓴다(DA Phase 1 신설, 예시는 LAYOUT_RULES §4). 결과를 그림이 계산하는 템플릿은 `hideResult` 의무(STANDARDS 부록 A.1).

## 7. 완료 조건

- `python3 tools/validate.py --domain BUMP --gate` 통과(차단 E 0). 남는 W 는 수정 또는 `vx` + 사유.
- `python3 tools/build.py` · `node tools/smoke.js dist/HBM_quiz.html` 오류 없음.
- 보고서 `docs/reviews/BUMP.md` (형식: ROSTER §4).
