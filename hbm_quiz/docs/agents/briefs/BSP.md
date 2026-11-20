# BSP 분야 브리프 — Backside pad 형성

- 소유 파일: `data/01_BSP.json` · 기준: `docs/agents/STANDARDS.md` · 자동 검사: `python3 tools/validate.py --domain BSP`
- 작성: EA (Phase 1, 2026-11-20) · 기준선 리포트: `docs/reviews/_auto_baseline.md`

## 0. 현황

| 난이도 | 문항 | stem 단일형 | ctx 조립형 | 정답 위치 ①/②/③/④ |
|---|---|---|---|---|
| 초급 | 113 | 72 | 41 | 33 / 27 / 26 / 27 |
| 중급 | 114 | 54 | 60 | 26 / 32 / 32 / 24 |
| 고급 | 27 | 6 | 21 | 7 / 4 / 8 / 8 |
| 합계 | 254 | 132 | 122 | |

- k=1 상황도 132 · k=0 주제도 122 · 그림 사용: f_bs 254
- **차단 E 이슈가 있는 문항: 198 / 254** (E_JOSA_CIRC 는 EA Phase 2 일괄 처리라 제외)

## 1. 자동 검사 요약 (기준선)

| 코드 | 건수 | 예시 id |
|---|---|---|
| `E_META_METRICS` | 122 | BSP-A-0007, BSP-A-0008, BSP-A-0009, BSP-A-0010 |
| `E_JOSA_CIRC` | 114 | BSP-A-0007, BSP-A-0009, BSP-A-0010, BSP-A-0012 |
| `E_STYLE_PLAIN` | 110 | BSP-A-0007, BSP-A-0008, BSP-A-0009, BSP-A-0010 |
| `E_TITLE_TRUNC` | 91 | BSP-A-0007, BSP-A-0008, BSP-A-0009, BSP-A-0010 |
| `E_EXP_SHORT` | 64 | BSP-A-0017, BSP-A-0021, BSP-A-0022, BSP-A-0025 |
| `E_FAMILY_OVER` | 62 | BSP-B-0022, BSP-B-0023, BSP-B-0024, BSP-B-0025 |
| `E_EXP_ONLY_REFS` | 44 | BSP-A-0026, BSP-B-0080, BSP-B-0084, BSP-B-0097 |
| `E_K1_FIG_NUM` | 11 | BSP-A-0002, BSP-B-0001, BSP-B-0003, BSP-B-0004 |
| `E_JOSA_EN` | 6 | BSP-A-0023, BSP-I-0107, BSP-I-0110 |
| `E_GRAMMAR_TRUNC` | 5 | BSP-I-0015, BSP-I-0030, BSP-I-0031, BSP-I-0039 |
| `E_DOUBLE_Q` | 3 | BSP-B-0078, BSP-B-0084, BSP-B-0092 |
| `W_META_METRICS` | 126 | BSP-A-0003, BSP-A-0004, BSP-A-0005, BSP-A-0006 |
| `W_TITLE_COPY` | 122 | BSP-A-0007, BSP-A-0008, BSP-A-0009, BSP-A-0010 |
| `W_EXP_DISTRACTORS` | 118 | BSP-A-0001, BSP-A-0002, BSP-A-0003, BSP-A-0004 |
| `W_OPT_ODD_END` | 36 | BSP-A-0022, BSP-B-0073, BSP-B-0074, BSP-B-0079 |
| `W_TITLE_QUESTION` | 31 | BSP-A-0026, BSP-B-0073, BSP-B-0076, BSP-B-0080 |
| `W_FIG_LEAK` | 15 | BSP-B-0010, BSP-B-0013, BSP-B-0018, BSP-B-0022 |
| `W_OPT_LONGEST` | 13 | BSP-B-0028, BSP-B-0037, BSP-B-0065, BSP-B-0075 |
| `W_OPT_WEAK` | 11 | BSP-B-0089, BSP-B-0090, BSP-B-0100, BSP-B-0101 |
| `W_K1_METRIC_NUM` | 9 | BSP-B-0003, BSP-B-0004, BSP-B-0005, BSP-B-0006 |
| `W_OPT_STEM_ECHO` | 9 | BSP-B-0028, BSP-B-0037, BSP-B-0065, BSP-I-0016 |
| `W_NEAR_DUP` | 6 | BSP-A-0004, BSP-A-0005, BSP-A-0006, BSP-I-0007 |
| `W_EXP_OFFTOPIC` | 3 | BSP-I-0056, BSP-I-0063, BSP-I-0101 |
| `W_OPT_ABSOLUTE` | 1 | BSP-B-0091 |

(참고: `I_JOSA_SPACE` 254 · `I_TEMPLATE_JOIN` 122 — 새로 쓰는 문장은 조사를 붙여 쓰고, ctx 조립형은 STANDARDS 3.1 에 따라 정리)

## 2. 표본 조사로 확인한 대표 결함 (EA 직접 판독: 난이도별 10문항 이상)

- **8단계 공정 판정 템플릿 가족이 대부분**: "전체 8단계 중 'X' 를 막 끝낸 상태 → 남은 절연막 구성/다음 공정/의도" (BSP-B-0010 계열 15, -0009 계열 9, -0008·-0021 계열 8 …). 초·중급 113+114 의 상당수가 이 가족이다. **가족당 3개 제한**에 걸리는 문항 62개.
- **조립 문장 절단 흔적**: "'seed etching' 의 목적은 pad 바깥 금속을 제거해 분입니다", "SiN 을 stop 층으로 희생막만 걷어입니다", "CMP 의 stop 층을입니다"(BSP-I-0012, -0028, -0031 등, E_GRAMMAR_TRUNC). 조사 오류 "'SiO2 증착' 를", "설계 의도으로".
- **고급 27문항뿐이고 그중 21개가 ctx 조립형** — 일반론("상관 분석이 유효한 이유", BSP-A-0014) 위주.
- **기술 정정 후보**: BSP-A-0008 해설 "Glue가 두꺼우면 Si가 더 남고" — carrier 기준 연삭(두께 게이지가 상면 기준)에서는 glue 가 두꺼운 곳이 더 많이 깎여 **Si 가 얇아진다**. 정답(부분 상쇄)은 맞을 수 있으나 해설 논리가 반대. BSP-I-0065 "연삭량을 늘리면 상단 손상" 은 표현 모호.
- 이 분야의 공정 흐름(SiO₂/SiN/희생 SiO₂ + SiN-stop CMP)은 **한 가지 통합 방식**이다. 문항에서 "일반적 HBM 공정" 처럼 단정하지 말고 "이 공정 흐름에서는" 으로 한정한다.

## 3. 핵심 개념 체크리스트와 현재 커버리지

키워드 기반 근사치(지문·보기·해설에서 해당 주제가 다뤄진 문항 수). 0–4 = **공백**, 5–14 = 부족, 15+ = 있음(질은 별도 판단).

| 주제 | 초급 | 중급 | 고급 | 판정 |
|---|---|---|---|---|
| carrier(WSS) 접착·debond | 15 | 19 | 8 | 있음 |
| back grinding·TTV·stress relief | 9 | 13 | 6 | 있음 |
| edge trimming | 0 | 0 | 0 | **공백** |
| TSV reveal(Si recess 식각·선택비) | 78 | 62 | 11 | 있음 |
| Cu 노출 높이·돌출 산포 | 37 | 20 | 13 | 있음 |
| 저온 passivation(SiN/SiO2, glue 내열) | 71 | 53 | 6 | 있음 |
| CMP(SiN stop) 개구 | 73 | 55 | 1 | 있음 |
| backside pad 금속(Ni/Au, Cu/Ni)·seed etch | 74 | 68 | 9 | 있음 |
| undercut·residue | 0 | 6 | 6 | 부족 |
| Cu 오염/확산(뒷면 Si) | 2 | 7 | 0 | 부족 |
| 뒷면 probe/KGD test pad | 2 | 0 | 0 | **공백** |
| HCB용 뒷면 평탄도(hybrid bonding 대응) | 0 | 0 | 0 | **공백** |

**우선 보강 공백**: edge trimming, HCB 대응 뒷면 평탄도(뒷면도 접합면이 되는 경우), 뒷면 probe/KGD pad, Cu 오염·확산(reveal 중 노출 Cu), carrier 접착·debond 방식(laser/thermal slide/mechanical)과 내열 한계, Si recess 식각 선택비·종점, TTV 누적과 reveal 산포

## 4. 작업 지시 (우선순위 순)

1. **사실 오류·정답 오류 먼저**: §2 의 기술 정정 후보, `E_EXP_REF_ANSWER`(정답 키 재검증), NUM·FACT 에이전트 결과(`docs/reviews/num/BSP.md`, `docs/reviews/_facts.md`)를 반영한다.
2. **템플릿 가족 정리**: `E_FAMILY_OVER` 대상은 가족당 3개(가능하면 난이도별 1개)만 남기고 삭제하거나 다른 판단을 묻도록 재작성. 근중복(`W_NEAR_DUP`)도 정리.
3. **ctx 조립형 정리**: ctx 가 qt 풀이에 필요 없으면 stem 단일형으로 변환. 기술 외 사유 오답·타 분야 오답(`W_OPT_WEAK`) 교체, 형식 단서(`W_OPT_ODD_END`, `W_OPT_LONGEST`, `W_OPT_ABSOLUTE`) 제거.
4. **해설 재작성**: `E_EXP_SHORT`·`E_EXP_ONLY_REFS`·`E_STYLE_PLAIN`·`W_EXP_DISTRACTORS` — 정답 근거 + 오답 3개 각각의 오류 + (계산) 식·대입·결과. 일괄 `[근거]` 꼬리표는 고친 해설에서 뺀다.
5. **제목·지표·그림**: `E_TITLE_TRUNC`·`W_TITLE_*` 제목 재작성, `E_META_METRICS` 지표를 지문 조건으로 교체, `E_K1_FIG_NUM`·`E_FIG_ANSWER_LEAK`·`E_FIG_INTERNAL`·`W_FIG_*` 그림 params 정정.
6. **난이도 재배치**: 단순 대입 계산·용어 문항이 고급이면 lv 를 내린다. lv 가 바뀌면 id 의 LV 도 달라져야 하므로 **새 id(`CODE-LV-9xxx`)를 발급하고 `"prev": "옛 id"` 필드를 남긴다**(보고서에 old→new 기록). 고급은 STANDARDS §1 기준으로 채운다.
7. **신규 출제**(§5) — 공백 주제 위주. 새 id 는 `BSP-LV-9001` 부터.
8. 타 분야 문항은 고쳐서 `"mv": "CODE"` 로 이관 제안(EA 가 Phase 2 에서 이동) 하거나 자기 분야 관점으로 재작성.

## 5. 추가 출제 목표

| | 초급 | 중급 | 고급 | 합계 |
|---|---|---|---|---|
| 신규 최소 | 10 | 25 | 55 | 90 |

- 가족 초과로 정리될 문항 약 62 건은 위 신규로 대체한다(수량 유지보다 질 우선, 최종 분야 규모는 ±10 % 허용).
- 최종 난이도 비율 권장: 초급 25–30 % · 중급 35–40 % · 고급 30–35 %.

- 고급 목표를 27 → 80 이상으로. 데이터 해석형 중심: wafer 맵(TTV·glue 두께·TSV 깊이)으로 미노출/과돌출 위치 예측, 돌출 높이 분포에서 CMP 조건 결정, seed etch 시간 vs undercut vs residue 트레이드오프(데이터 표), 저온 passivation 막질(습식 식각률·누설) 데이터 해석, carrier debond 후 휨·crack 원인 규명
- 중급: TTV 합성(산포의 부호·크기), recess 깊이 계산, Cu 오염 방지 순서, 뒷면 pad 금속 스택(Ni/Au 등) 선택 이유

## 6. 사용할 그림 템플릿과 params

| 템플릿 | params | 제약 · 주의 |
|---|---|---|
| `f_bs` | `step` 0–7 (0 reveal, 1 SiO₂, 2 SiN, 3 희생 SiO₂, 4 CMP(SiN stop), 5 Ti/Cu seed, 6 Ni plating, 7 seed etching), `defect`: none·undercut·residue(step 7 에서만), `ox1`, `sin`, `ox2`(nm), `ni_um` | 공정 흐름은 고정 8단계 |
| `f_plot` | `title`, `x`{min,max,ticks,lab}, `y`{…}, `series`[{name, color(“RRGGBB”), pts[[x,y]], dash}], `marks`[[x, 라벨]], `bullets`[…] | 데이터 해석형 고급 문항의 주력 템플릿 |
| `f_note` | `title`, `points`(≤ 4), `ask` | 정답 문장 금지 |
| `f_film` | `layers`[[이름, 상대두께, 색]], `roles`[[층, 두께, 역할]], `bullets`, `flags`[[층 index, 표시]] | |


- 8단계 가족은 단계별 1문항씩(최대 8개가 아니라 **질문 유형별 3개**) 남기고 나머지는 위 공백 주제로 대체.
- 데이터 해석형 고급에 표가 필요하면 `f_plot`(그래프)으로 우선 해결하고, 표 템플릿(`f_table`)은 DA 에 요청 중(`EA_to_DA.md`). 확정 전에는 표 데이터를 지문 안 문장으로 쓴다.

## 7. 완료 조건

- `python3 tools/validate.py --domain BSP --gate` 통과(차단 E 0). 남는 W 는 수정 또는 `vx` + 사유.
- `python3 tools/build.py` · `node tools/smoke.js dist/HBM_quiz.html` 오류 없음.
- 보고서 `docs/reviews/BSP.md` (형식: ROSTER §4).
