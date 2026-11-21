# SAW 분야 브리프 — Sawing 과 개별화

- 소유 파일: `data/03_SAW.json` · 기준: `docs/agents/STANDARDS.md` · 자동 검사: `python3 tools/validate.py --domain SAW`
- 작성: EA (Phase 1, 2026-11-20) · 기준선 리포트: `docs/reviews/_auto_baseline.md`

## 0. 현황

| 난이도 | 문항 | stem 단일형 | ctx 조립형 | 정답 위치 ①/②/③/④ |
|---|---|---|---|---|
| 초급 | 69 | 28 | 41 | 17 / 18 / 18 / 16 |
| 중급 | 52 | 2 | 50 | 11 / 19 / 11 / 11 |
| 고급 | 59 | 46 | 13 | 18 / 17 / 15 / 9 |
| 합계 | 180 | 76 | 104 | |

- k=1 상황도 76 · k=0 주제도 104 · 그림 사용: f_saw 180
- **차단 E 이슈가 있는 문항: 141 / 180** (E_JOSA_CIRC 는 EA Phase 2 일괄 처리라 제외)

## 1. 자동 검사 요약 (기준선)

| 코드 | 건수 | 예시 id |
|---|---|---|
| `E_META_METRICS` | 104 | SAW-A-0047, SAW-A-0048, SAW-A-0049, SAW-A-0050 |
| `E_EXP_SHORT` | 92 | SAW-A-0049, SAW-A-0051, SAW-A-0052, SAW-A-0053 |
| `E_STYLE_PLAIN` | 80 | SAW-A-0047, SAW-A-0048, SAW-A-0049, SAW-A-0050 |
| `E_EXP_ONLY_REFS` | 75 | SAW-A-0049, SAW-A-0051, SAW-A-0052, SAW-A-0053 |
| `E_JOSA_CIRC` | 73 | SAW-A-0048, SAW-A-0050, SAW-A-0056, SAW-A-0059 |
| `E_TITLE_TRUNC` | 57 | SAW-A-0047, SAW-A-0048, SAW-A-0049, SAW-A-0050 |
| `E_FAMILY_OVER` | 32 | SAW-A-0024, SAW-A-0025, SAW-A-0026, SAW-A-0027 |
| `E_JOSA_EN` | 26 | SAW-A-0047, SAW-A-0054, SAW-B-0030, SAW-B-0032 |
| `E_EXP_REF_ANSWER` | 6 | SAW-A-0047, SAW-B-0030, SAW-B-0052, SAW-B-0054 |
| `E_DOUBLE_Q` | 3 | SAW-B-0035, SAW-B-0039, SAW-B-0041 |
| `E_K1_FIG_NUM` | 2 | SAW-B-0001, SAW-I-0001 |
| `E_DUP_EXACT` | 2 | SAW-B-0008, SAW-B-0027 |
| `E_FIG_TOPIC` | 1 | SAW-I-0002 |
| `W_TITLE_COPY` | 104 | SAW-A-0047, SAW-A-0048, SAW-A-0049, SAW-A-0050 |
| `W_EXP_DISTRACTORS` | 84 | SAW-A-0001, SAW-A-0002, SAW-A-0003, SAW-A-0004 |
| `W_META_METRICS` | 52 | SAW-A-0021, SAW-A-0022, SAW-A-0023, SAW-A-0024 |
| `W_TITLE_QUESTION` | 44 | SAW-B-0029, SAW-B-0031, SAW-B-0034, SAW-B-0036 |
| `W_OPT_ODD_END` | 39 | SAW-A-0001, SAW-A-0009, SAW-A-0010, SAW-A-0011 |
| `W_OPT_WEAK` | 15 | SAW-A-0058, SAW-B-0030, SAW-B-0031, SAW-B-0036 |
| `W_OPT_LONGEST` | 9 | SAW-A-0049, SAW-B-0043, SAW-B-0048, SAW-B-0054 |
| `W_FIG_TOPIC` | 6 | SAW-A-0049, SAW-B-0032, SAW-B-0038, SAW-I-0017 |
| `W_OPT_STEM_ECHO` | 5 | SAW-A-0002, SAW-A-0003, SAW-A-0004, SAW-A-0005 |
| `W_K1_FIG_EXTRA` | 4 | SAW-A-0001, SAW-A-0002, SAW-B-0002, SAW-I-0002 |
| `W_EXP_OFFTOPIC` | 3 | SAW-B-0029, SAW-B-0034, SAW-I-0003 |
| `W_K1_METRIC_NUM` | 2 | SAW-A-0001, SAW-B-0001 |
| `W_OPT_ABSOLUTE` | 1 | SAW-A-0053 |

(참고: `I_JOSA_SPACE` 180 · `I_TEMPLATE_JOIN` 104 — 새로 쓰는 문장은 조사를 붙여 쓰고, ctx 조립형은 STANDARDS 3.1 에 따라 정리)

## 1A. W1 입력 (지원 에이전트 결과 — 작업 1순위)

- **NUM** `docs/reviews/num/SAW.md`: 검증 26 · 산술 일치 25 · **정답 오류 확정 1** · **비현실 설정 0** · 그림·지표 정답 노출 0 · 간극 규약 위반 0 · 근접 오답(<3 %) 0 · 회상형(FACT 이관) 0. 문항별 올바른 값·식은 해당 파일. solver: `tools/num/`.
- **FACT** `docs/reviews/_facts.md` — 이 분야를 직접 가리키는 주장 없음(§2.2–2.4 기준표 변경은 STANDARDS 부록 B 참고).
- **XD** `docs/reviews/xd/SAW.md` — 용어 규약 위반·교차 중복(보유/삭제)·이관(mv)·사실 충돌 지시. 요약은 `docs/reviews/xd/_index.md`.
- 처리 원칙: NUM 정답 오류·FACT '정정'/'사용 금지' 판정 → 해당 문항을 **가장 먼저** 고치거나 삭제. FACT '조건부' 는 지문 표현을 고치면 유지(예: "JEDEC 규격 상한 775 µm" → "높이 상한(설계 조건) 775 µm"). 판정과 다르게 처리하면 보고서에 근거.

## 2. 표본 조사로 확인한 대표 결함 (EA 직접 판독: 난이도별 10문항 이상)

- **ctx 조립형 104문항의 질이 특히 낮음**: 같은 질문 반복(SAW-B-0059 ≈ SAW-I-0016 ≈ SAW-I-0005 "절단 손상이 즉시 드러나지 않는 이유"), 무의미 오답("색상이 같기 때문", "장비 선택지가 하나뿐이기 때문"), 타 분야 오답("리프레시 주기와 채널 수", SAW-I-0033).
- **해설이 정답을 오답으로 서술 6건**(SAW-A-0047 "②④③은 무관하다" a=③, SAW-B-0030, -0052, -0054, -0058) — 정답 키 재검증 필요.
- **방식 판정 가족**: "설명에 해당하는 개별화 방식 고르기"(SAW-B-0003 계열) — 그림 표와 지문 설명이 같아 그림만 보고 풀림.
- 그림-지문 불일치: plasma 인데 `kerf_um` 30–40(비교표는 5–15 µm, SAW-A-0028), deep laser 질문에 dbg 그림(SAW-B-0051), deep laser 지문에 blade 키워드로 E_FIG_TOPIC(SAW-I-0002).
- 중급 52 문항 중 stem 형은 2개뿐 — 중급이 사실상 비어 있음.

## 3. 핵심 개념 체크리스트와 현재 커버리지

키워드 기반 근사치(지문·보기·해설에서 해당 주제가 다뤄진 문항 수). 0–4 = **공백**, 5–14 = 부족, 15+ = 있음(질은 별도 판단).

| 주제 | 초급 | 중급 | 고급 | 판정 |
|---|---|---|---|---|
| blade dicing·chipping | 28 | 2 | 20 | 있음 |
| laser grooving(low-k) | 22 | 0 | 1 | 있음 |
| stealth dicing·SDBG | 18 | 1 | 0 | 고급 없음 |
| DBG(dicing before grinding) | 20 | 3 | 1 | 있음 |
| plasma dicing | 21 | 4 | 3 | 있음 |
| die strength(3점 굽힘) | 27 | 3 | 23 | 있음 |
| scribe lane 금속·TEG | 27 | 1 | 44 | 있음 |
| seal ring·crack stop | 0 | 0 | 0 | **공백** |
| HCB 입자 청정도와 dicing | 0 | 1 | 0 | **공백** |
| 몰딩 cube/wafer 절단(MUF 포함) | 5 | 5 | 2 | 부족 |
| tape/expansion·pick-up | 5 | 1 | 10 | 있음 |
| gross die 계산 | 2 | 1 | 35 | 있음 |

**우선 보강 공백**: seal ring·crack stop 과 chipping 허용 기준, SDBG(stealth dicing before grinding), HCB 용 dicing 청정도(입자·잔사가 접합 void 로), MR-MUF 후 molded cube/wafer 절단(EMC+Si 동시 절단), die strength(3점 굽힘·Weibull) 측정과 측벽 손상, 얇은 die(30–50 µm) 취급·pick-up, tape/UV 경화

## 4. 작업 지시 (우선순위 순)

0. **[최우선] 메타 지표 제거 — 156건** (`E_META_METRICS` 104, `W_META_METRICS` 52). 화면 '제시 조건' 띠에 "난이도: 고급", "묻는 것: 해당 항목", "세부 주제", "핵심어" 가 그대로 보인다(DA 스크린샷 확인). 지문 조건 2–4개로 바꾸거나, 요약할 조건이 없으면 `"metrics": []`(키는 유지). 정답 오류 수정과 같은 1순위로 처리한다.
1. **정답 오류·사실 정정 (W1 입력 §1A)**: NUM 정답 오류 확정·비현실 설정·그림 노출(`docs/reviews/num/SAW.md`), FACT 정정·사용 금지·조건부 주장(§1A 의 F 번호), XD 용어·중복·이관 지시(`docs/reviews/xd/SAW.md`), §2 의 기술 정정 후보, `E_EXP_REF_ANSWER`(정답 키 재검증). 메타 지표 제거(0번)와 함께 가장 먼저.
2. **템플릿 가족 정리**: `E_FAMILY_OVER` 대상은 가족당 3개(가능하면 난이도별 1개)만 남기고 삭제하거나 다른 판단을 묻도록 재작성. 근중복(`W_NEAR_DUP`)도 정리.
3. **ctx 조립형 정리**: ctx 가 qt 풀이에 필요 없으면 stem 단일형으로 변환. 기술 외 사유 오답·타 분야 오답(`W_OPT_WEAK`) 교체, 형식 단서(`W_OPT_ODD_END`, `W_OPT_LONGEST`, `W_OPT_ABSOLUTE`) 제거.
4. **해설 재작성**: `E_EXP_SHORT`·`E_EXP_ONLY_REFS`·`E_STYLE_PLAIN`·`W_EXP_DISTRACTORS` — 정답 근거 + 오답 3개 각각의 오류 + (계산) 식·대입·결과. 일괄 `[근거]` 꼬리표는 고친 해설에서 뺀다.
5. **제목·지표·그림**: `E_TITLE_TRUNC`·`W_TITLE_*` 제목 재작성, `E_META_METRICS` 지표를 지문 조건으로 교체, `E_K1_FIG_NUM`·`E_FIG_ANSWER_LEAK`·`E_FIG_INTERNAL`·`W_FIG_*` 그림 params 정정.
6. **난이도 재배치**: 단순 대입 계산·용어 문항이 고급이면 lv 를 내린다. lv 가 바뀌면 id 의 LV 도 달라져야 하므로 **새 id(`CODE-LV-9xxx`)를 발급하고 `"prev": "옛 id"` 필드를 남긴다**(보고서에 old→new 기록). 고급은 STANDARDS §1 기준으로 채운다.
7. **신규 출제**(§5) — 공백 주제 위주. 새 id 는 `SAW-LV-9001` 부터.
8. 타 분야 문항은 고쳐서 `"mv": "CODE"` 로 이관 제안(EA 가 Phase 2 에서 이동) 하거나 자기 분야 관점으로 재작성.

## 4A. DA Phase 1 템플릿 변경으로 손봐야 할 기존 문항

- 해당 문항 없음(검사기 기준). 새 문항은 STANDARDS 부록 A 를 따른다.

## 5. 추가 출제 목표

| | 초급 | 중급 | 고급 | 합계 |
|---|---|---|---|---|
| 신규 최소 | 15 | 35 | 30 | 80 |

- 가족 초과로 정리될 문항 약 32 건은 위 신규로 대체한다(수량 유지보다 질 우선, 최종 분야 규모는 ±10 % 허용).
- 최종 난이도 비율 권장: 초급 25–30 % · 중급 35–40 % · 고급 30–35 %.

- 중급(최우선): 방식별 kerf·HAZ·chipping·측벽 강도 비교(조건 2개), low-k 박리와 laser grooving 의 이유, SDBG 순서와 장점, plasma dicing 에서 scribe 금속/TEG 처리
- 고급: chipping 분포 데이터 + seal ring 거리로 신뢰성 판정, die strength Weibull 데이터 해석, HCB 적용 제품의 dicing 방식 선택(입자·측벽·처리량 3변수), molded cube 절단에서 EMC/Si 동시 절단 조건 충돌, gross die 계산은 1개만

## 6. 사용할 그림 템플릿과 params

| 템플릿 | params | 제약 · 주의 |
|---|---|---|
| `f_saw` | `method`: blade·lg·stealth·plasma·deeplaser·dbg, `kerf_um`, `haz_um`, `chip_um`, `bullet` | 표는 "대표 범위" — kerf 는 방식별 범위 안으로 |
| `f_plot` | `title`, `x`/`y`{min,max,ticks ≤ 6,lab}, `series` ≤ 4, `marks` ≤ 3, `bullets` ≤ 3 | 데이터 해석형 고급의 주력 |
| `f_note` | `title` ≤ 22자, `points` ≤ 4(각 ≤ 50자), `ask` ≤ 12자 | points 는 **판단 관점** — 정답 문장 금지 |


- `f_saw` 비교표는 고정값이므로 params(kerf)와 모순 금지: plasma 는 kerf 5–15 µm, blade 30–60 µm 범위로.
- 데이터 해석형 고급에는 `f_table`(표)·`f_wafermap`(맵)·`f_plot`(그래프)을 쓴다(DA Phase 1 신설, 예시는 LAYOUT_RULES §4). 결과를 그림이 계산하는 템플릿은 `hideResult` 의무(STANDARDS 부록 A.1).

## 7. 완료 조건

- `python3 tools/validate.py --domain SAW --gate` 통과(차단 E 0). 남는 W 는 수정 또는 `vx` + 사유.
- `python3 tools/build.py` · `node tools/smoke.js dist/HBM_quiz.html` 오류 없음.
- 보고서 `docs/reviews/SAW.md` (형식: ROSTER §4).
