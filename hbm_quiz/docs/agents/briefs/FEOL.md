# FEOL 분야 브리프 — 전공정과 배선 재료

- 소유 파일: `data/12_FEOL.json` · 기준: `docs/agents/STANDARDS.md` · 자동 검사: `python3 tools/validate.py --domain FEOL`
- 작성: EA (Phase 1, 2026-11-20) · 기준선 리포트: `docs/reviews/_auto_baseline.md`

## 0. 현황

| 난이도 | 문항 | stem 단일형 | ctx 조립형 | 정답 위치 ①/②/③/④ |
|---|---|---|---|---|
| 초급 | 72 | 0 | 72 | 22 / 22 / 14 / 14 |
| 중급 | 74 | 0 | 74 | 18 / 20 / 13 / 23 |
| 고급 | 37 | 0 | 37 | 11 / 8 / 6 / 12 |
| 합계 | 183 | 0 | 183 | |

- k=1 상황도 0 · k=0 주제도 183 · 그림 사용: f_film 147, f_note 36
- **차단 E 이슈가 있는 문항: 183 / 183** (E_JOSA_CIRC 는 EA Phase 2 일괄 처리라 제외)

## 1. 자동 검사 요약 (기준선)

| 코드 | 건수 | 예시 id |
|---|---|---|
| `E_META_METRICS` | 183 | FEOL-A-0001, FEOL-A-0002, FEOL-A-0003, FEOL-A-0004 |
| `E_STYLE_PLAIN` | 151 | FEOL-A-0001, FEOL-A-0002, FEOL-A-0003, FEOL-A-0004 |
| `E_JOSA_CIRC` | 148 | FEOL-A-0001, FEOL-A-0002, FEOL-A-0003, FEOL-A-0004 |
| `E_EXP_SHORT` | 144 | FEOL-A-0006, FEOL-A-0007, FEOL-A-0011, FEOL-A-0013 |
| `E_TITLE_TRUNC` | 118 | FEOL-A-0001, FEOL-A-0002, FEOL-A-0003, FEOL-A-0004 |
| `E_EXP_ONLY_REFS` | 109 | FEOL-A-0013, FEOL-A-0014, FEOL-A-0016, FEOL-A-0018 |
| `E_JOSA_EN` | 21 | FEOL-A-0001, FEOL-A-0003, FEOL-A-0005, FEOL-A-0012 |
| `E_DOUBLE_Q` | 10 | FEOL-B-0004, FEOL-B-0033, FEOL-B-0035, FEOL-B-0037 |
| `E_CALC_NO_WORK` | 2 | FEOL-B-0026, FEOL-I-0012 |
| `E_EXP_REF_ANSWER` | 2 | FEOL-A-0018, FEOL-I-0068 |
| `W_TITLE_COPY` | 183 | FEOL-A-0001, FEOL-A-0002, FEOL-A-0003, FEOL-A-0004 |
| `W_TITLE_QUESTION` | 63 | FEOL-A-0023, FEOL-B-0003, FEOL-B-0004, FEOL-B-0006 |
| `W_OPT_ODD_END` | 58 | FEOL-A-0006, FEOL-A-0007, FEOL-A-0014, FEOL-A-0017 |
| `W_OPT_WEAK` | 17 | FEOL-A-0013, FEOL-A-0014, FEOL-A-0023, FEOL-B-0012 |
| `W_OPT_LONGEST` | 16 | FEOL-A-0001, FEOL-A-0026, FEOL-A-0028, FEOL-B-0002 |
| `W_EXP_DISTRACTORS` | 9 | FEOL-A-0018, FEOL-B-0005, FEOL-B-0017, FEOL-B-0031 |
| `W_EXP_OFFTOPIC` | 7 | FEOL-B-0014, FEOL-B-0020, FEOL-I-0008, FEOL-I-0018 |
| `W_OPT_ABSOLUTE` | 6 | FEOL-A-0029, FEOL-A-0036, FEOL-B-0015, FEOL-I-0015 |

(참고: `I_JOSA_SPACE` 67 · `I_TEMPLATE_JOIN` 183 — 새로 쓰는 문장은 조사를 붙여 쓰고, ctx 조립형은 STANDARDS 3.1 에 따라 정리)

## 2. 표본 조사로 확인한 대표 결함 (EA 직접 판독: 난이도별 10문항 이상)

- **183문항 전부 ctx 조립형**, 일반 반도체 공정 상식(포토리소그래피 정의, ALD 원리, 클린룸) 위주로 HBM·DRAM 맥락이 약함. 고급 37 중 상당수가 타 분야 주제(Reveal 선택비 FEOL-A-0003 → BSP, 흡습 급속가열 FEOL-A-0010 → FA/WARP, 전원망 FEOL-A-0018 → SIP).
- **해설이 정답을 오답으로 2건**(FEOL-A-0018 "④①③은 기술 판단 항목이 아니다" a=④).
- 타 분야 기법이 섞임: InGaAs 검출기(FEOL-B-0047 → FA), 프로브 압력(FEOL-I-0009 → MET).
- 이중 의문형 10건(분야 최다 수준), 해설 해라체.

## 3. 핵심 개념 체크리스트와 현재 커버리지

키워드 기반 근사치(지문·보기·해설에서 해당 주제가 다뤄진 문항 수). 0–4 = **공백**, 5–14 = 부족, 15+ = 있음(질은 별도 판단).

| 주제 | 초급 | 중급 | 고급 | 판정 |
|---|---|---|---|---|
| DRAM 셀 공정(BCAT·capacitor high-k) | 6 | 3 | 0 | 부족 |
| 주변회로 HKMG·FinFET(base die 로직) | 2 | 2 | 4 | 부족 |
| EUV·multi-patterning | 2 | 4 | 3 | 부족 |
| ALD/CVD/PVD 증착 | 4 | 1 | 1 | 부족 |
| 식각(이방성·선택비) | 12 | 15 | 4 | 있음 |
| Cu damascene·barrier | 0 | 2 | 3 | 부족 |
| low-k·기계 강도 | 0 | 2 | 1 | **공백** |
| contact·silicide | 3 | 1 | 0 | **공백** |
| 열예산(TSV via-middle과의 정합) | 0 | 1 | 3 | **공백** |
| CMP(FEOL/BEOL) | 2 | 2 | 0 | **공백** |
| passivation·pad(Al/Cu) | 7 | 5 | 2 | 부족 |
| wafer bow·응력 막 | 7 | 12 | 2 | 있음 |

**우선 보강 공백**: DRAM 셀 공정(BCAT 매립 채널 트랜지스터, 고종횡비 캐패시터와 high-k 유전막), 주변회로 HKMG, EUV 적용 층과 확률적 결함, base die 로직 공정(FinFET/GAA) 과 TSV 통합, via-middle 의 열예산 정합, Cu/low-k BEOL 의 기계적 취약성과 패키지 응력(CPI), passivation·pad 구조와 probe/접합, wafer bow 와 응력막

## 4. 작업 지시 (우선순위 순)

0. **[최우선] 메타 지표 제거 — 183건** (`E_META_METRICS` 183, `W_META_METRICS` 0). 화면 '제시 조건' 띠에 "난이도: 고급", "묻는 것: 해당 항목", "세부 주제", "핵심어" 가 그대로 보인다(DA 스크린샷 확인). 지문 조건 2–4개로 바꾸거나, 요약할 조건이 없으면 `"metrics": []`(키는 유지). 정답 오류 수정과 같은 1순위로 처리한다.
1. **사실 오류·정답 오류 먼저**: §2 의 기술 정정 후보, `E_EXP_REF_ANSWER`(정답 키 재검증), NUM·FACT 에이전트 결과(`docs/reviews/num/FEOL.md`, `docs/reviews/_facts.md`)를 반영한다.
2. **템플릿 가족 정리**: `E_FAMILY_OVER` 대상은 가족당 3개(가능하면 난이도별 1개)만 남기고 삭제하거나 다른 판단을 묻도록 재작성. 근중복(`W_NEAR_DUP`)도 정리.
3. **ctx 조립형 정리**: ctx 가 qt 풀이에 필요 없으면 stem 단일형으로 변환. 기술 외 사유 오답·타 분야 오답(`W_OPT_WEAK`) 교체, 형식 단서(`W_OPT_ODD_END`, `W_OPT_LONGEST`, `W_OPT_ABSOLUTE`) 제거.
4. **해설 재작성**: `E_EXP_SHORT`·`E_EXP_ONLY_REFS`·`E_STYLE_PLAIN`·`W_EXP_DISTRACTORS` — 정답 근거 + 오답 3개 각각의 오류 + (계산) 식·대입·결과. 일괄 `[근거]` 꼬리표는 고친 해설에서 뺀다.
5. **제목·지표·그림**: `E_TITLE_TRUNC`·`W_TITLE_*` 제목 재작성, `E_META_METRICS` 지표를 지문 조건으로 교체, `E_K1_FIG_NUM`·`E_FIG_ANSWER_LEAK`·`E_FIG_INTERNAL`·`W_FIG_*` 그림 params 정정.
6. **난이도 재배치**: 단순 대입 계산·용어 문항이 고급이면 lv 를 내린다. lv 가 바뀌면 id 의 LV 도 달라져야 하므로 **새 id(`CODE-LV-9xxx`)를 발급하고 `"prev": "옛 id"` 필드를 남긴다**(보고서에 old→new 기록). 고급은 STANDARDS §1 기준으로 채운다.
7. **신규 출제**(§5) — 공백 주제 위주. 새 id 는 `FEOL-LV-9001` 부터.
8. 타 분야 문항은 고쳐서 `"mv": "CODE"` 로 이관 제안(EA 가 Phase 2 에서 이동) 하거나 자기 분야 관점으로 재작성.

## 4A. DA Phase 1 템플릿 변경으로 손봐야 할 기존 문항

- 해당 문항 없음(검사기 기준). 새 문항은 STANDARDS 부록 A 를 따른다.

## 5. 추가 출제 목표

| | 초급 | 중급 | 고급 | 합계 |
|---|---|---|---|---|
| 신규 최소 | 15 | 35 | 45 | 95 |

- 기존 문항 정리(삭제·재작성) 규모는 §2 에 따른다. 최종 분야 규모는 질 우선으로 정한다.
- 최종 난이도 비율 권장: 초급 25–30 % · 중급 35–40 % · 고급 30–35 %.

- 고급(37 → 80 이상): via-middle TSV 가 FEOL 열예산·소자 특성에 주는 영향(3변수), low-k BEOL 의 CPI(chip-package interaction) crack 원인 규명, DRAM 캐패시터 종횡비·유전막·누설 트레이드오프 정량, EUV 확률 결함과 수율(Poisson) 추정, base die 로직 공정 노드 선택(성능·비용·TSV 통합)
- 중급: BCAT 구조와 이점, 캐패시터 C = εA/d 기반 비교, damascene 순서와 barrier 의 이유

## 6. 사용할 그림 템플릿과 params

| 템플릿 | params | 제약 · 주의 |
|---|---|---|
| `f_film` | `layers` ≤ 9, `roles` ≤ 5, `bullets` ≤ 3, `flags` ≤ 2 | |
| `f_note` | `title` ≤ 22자, `points` ≤ 4(각 ≤ 50자), `ask` ≤ 12자 | points 는 **판단 관점** — 정답 문장 금지 |
| `f_plot` | `title`, `x`/`y`{min,max,ticks ≤ 6,lab}, `series` ≤ 4, `marks` ≤ 3, `bullets` ≤ 3 | 데이터 해석형 고급의 주력 |


- 순수 일반 상식 초급(포토 정의 등)은 1/3 이하로 줄이고 DRAM·HBM 맥락으로 재작성.
- 데이터 해석형 고급에는 `f_table`(표)·`f_wafermap`(맵)·`f_plot`(그래프)을 쓴다(DA Phase 1 신설, 예시는 LAYOUT_RULES §4). 결과를 그림이 계산하는 템플릿은 `hideResult` 의무(STANDARDS 부록 A.1).

## 7. 완료 조건

- `python3 tools/validate.py --domain FEOL --gate` 통과(차단 E 0). 남는 W 는 수정 또는 `vx` + 사유.
- `python3 tools/build.py` · `node tools/smoke.js dist/HBM_quiz.html` 오류 없음.
- 보고서 `docs/reviews/FEOL.md` (형식: ROSTER §4).
