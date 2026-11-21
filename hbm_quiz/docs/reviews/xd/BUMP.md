# XD 교차분야 지시 — BUMP (Bump 와 계면 금속)

- 작성: XD (교차분야 일관성) · W1 사전 점검 · 2026-11-20 · 기준: `docs/agents/STANDARDS.md` 2.5 · 3.10
- 대상 파일: `data/02_BUMP.json`
- 지시 종류: **수정** · **삭제**(보고서 삭제 표에 “타 분야 중복: 보유 id” 로 기록) · **mv → CODE**(레코드에 `"mv": "CODE"`, 직접 옮기지 말 것) · **보유**(상대 분야가 지우므로 이 문항을 품질 기준으로 다듬을 것)
- XD 판정과 다르게 처리하려면 리뷰 보고서에 근거를 적는다(EA 최종 판정).

## 요약

| 항목 | 건수 |
|---|---|
| 1. 용어 규약 위반 (E / W) | 7 / 2 행 |
| 2. 교차 중복 관련 문항 | 14 |
| 3. 이관 제안 (mv) | 3 |
| 4. 사실 충돌 관여 | 6 건 |

## 1. 용어 규약 위반 (STANDARDS 2.5)

| id | 등급 | 문제 | 지시 |
|---|---|---|---|
| BUMP-A-0150 | E | 해설 첫 문장이 Smile/Cry 명명 설명(다른 문항 해설 혼입). 명명 내용 자체는 2.5 와 일치 | 해당 문장 삭제(교차 중복 판정으로 문항 자체도 삭제 대상 — §2) |
| BUMP-A-0146 | W | 해설에 Smile/Cry 명명 설명이 들어 있음(2.5 와 일치). 문항 주제(하중 상향 결과)와 무관한 문장 | 교차 중복으로 삭제(COW-I-0141 보유) — §2 |
| BUMP-B-0061 | E | “die를 하나씩 열과 압력으로 붙이는 방식” 의 정답이 “TCB”, 오답 “MR-MUF”·“Hybrid Bonding” — TCB 를 공법명으로 MR-MUF 와 대비 | 정답을 “TC-NCF” 로(또는 발문을 “장비 방식” 으로 바꿔 TCB 유지). 보기 “Hybrid Bonding” → “HCB”. 이 문항은 COW 와 중복이라 삭제 우선(§2) |
| BUMP-B-0062 | E | 보기에 “TCB” 를 MR-MUF 의 대립 공법으로 사용, “Hybrid Bonding” 표기 | “TCB” → “TC-NCF”, “Hybrid Bonding” → “HCB”. COW 중복으로 삭제 우선(§2) |
| BUMP-B-0029 | E | HCB 비표준 표기 Hybrid Bonding | “HCB” 로 통일(첫 언급 “HCB(Cu–Cu hybrid bonding)”) |
| BUMP-B-0080 | E | HCB 비표준 표기 하이브리드 본딩 | “HCB” 로 통일(첫 언급 “HCB(Cu–Cu hybrid bonding)”) |
| BUMP-B-0029 | E | “범프 없이 금속끼리 직접 붙이는 방식” 정답 “Hybrid Bonding”, 오답 “Mass Reflow” | 정답 “HCB”, 오답 “MR-MUF”. COW 의 공법 명칭 문항과 중복이라 삭제 우선(§2) |
| BUMP-I-0105 | W | µbump 표기 변형 Microbump | “µbump”(U+00B5, 하이픈 없음) 로 통일 — STANDARDS 2.4 표기 |
| BUMP-B-0080 | E | “하이브리드 본딩 적용 시 … 범프 피치” — HCB 에는 bump 가 없다(2.4). 표기도 비표준 | 교차 중복으로 삭제(§2). 사실 충돌 F3 참조 |

## 2. 교차 중복 · 근중복 (보유 분야 판정)

판정 기준: 그 개념이 어느 분야 학습 목표의 핵심인가(ROSTER §3). 숫자는 핵심 텍스트+보기 char 4-gram Jaccard(참고값, 0.35 이상 판독).

| id | 문제 | 지시 |
|---|---|---|
| BUMP-A-0147 | 미세 피치에서 solder 접합 공정 창이 좁아지는 인자 — 보유: COW-A-0160 | 삭제 (W_NEAR_DUP_X 0.83. TCB 공정 창은 COW 학습 목표) |
| BUMP-A-0150 | 미세 피치에서 solder 접합 공정 창이 좁아지는 인자 — 보유: COW-A-0160 | 삭제 (W_NEAR_DUP_X 0.83. TCB 공정 창은 COW 학습 목표) |
| BUMP-I-0134 | NCF 필름 두께 편차 → 배출량 편차 — 근중복 상대: WARP-I-0275 | mv → COW (0.81. NCF 는 COW 학습 목표 — BUMP-I-0134 를 다듬어 COW 로) |
| BUMP-A-0164 | ESD 손상 vs 통전(EM) 열화 감별 — 보유: DRAM-A-0061 (mv → FA (재작성)) | 삭제 (0.61/0.43 — 고장 감별은 FA) |
| BUMP-B-0028 | 접합 직전 대기(queue) 시간 관리 — 보유: COW-I-0180 | 삭제 (0.51/0.36) |
| BUMP-I-0119 | [보유] 작은 단면 = 전류 밀도↑ 로 불리 — 타 분야 근중복: FA-I-0080, FA-I-0062, WARP-B-0117, WARP-A-0258 | 보유 분야. 상대 문항은 해당 분야에서 삭제/이관. 남긴 문항은 STANDARDS 기준으로 다듬을 것 (0.46/0.40 — µbump EM 은 BUMP) |
| BUMP-A-0152 | [보유] 통전 중 특정 접점 저항 지속 상승 → crowding 부 void 성장 — 타 분야 근중복: WARP-A-0259 | 보유 분야. 상대 문항은 해당 분야에서 삭제/이관. 남긴 문항은 STANDARDS 기준으로 다듬을 것 (0.37) |
| BUMP-A-0146 | warpage 가 있는 die 에 하중만 올린 결과 — 보유: COW-I-0141 | 삭제 (0.39 — Smile/Cry 표기도 정리(§1)) |
| BUMP-I-0135 | NCF 유동 온도와 solder 용융 구간 불일치 — 보유: COW-I-0161 | 삭제 (0.35) |
| BUMP-B-0064 | fillet 형상 관리 이유 — 보유: COW-I-0165 | 삭제 (0.41) |
| BUMP-B-0080 | HCB 의 pitch 축소(“18 µm”) — 보유: COW-A-0073 | 삭제 (개념 중복 + 사실 충돌 F3) |
| BUMP-B-0061 | 공법 명칭 고르기(TCB/MR-MUF/HCB) — 보유: COW 분야 | 삭제 (COW 에 같은 정의 문항 다수(COW-B-0104 등). 공법명 표기도 위반(§1)) |
| BUMP-B-0062 | 공법 명칭 고르기(TCB/MR-MUF/HCB) — 보유: COW 분야 | 삭제 (COW 에 같은 정의 문항 다수(COW-B-0104 등). 공법명 표기도 위반(§1)) |
| BUMP-B-0029 | 공법 명칭 고르기(TCB/MR-MUF/HCB) — 보유: COW 분야 | 삭제 (COW 에 같은 정의 문항 다수(COW-B-0104 등). 공법명 표기도 위반(§1)) |

## 3. 이관 제안 (오분류)

| id | 지시 | 이유 |
|---|---|---|
| BUMP-I-0156 | mv → COW (`"mv": "COW"`, 다듬은 뒤) | NCF filler 입경 → 미접합 경로 — NCF 재료/공정 |
| BUMP-I-0158 | mv → COW (`"mv": "COW"`, 다듬은 뒤) | 압착 하중↑ 의 새 문제 — TCB 공정 조건 |
| BUMP-A-0145 | mv → COW (`"mv": "COW"`, 다듬은 뒤) | height offset + bond force 상향의 한계 — TCB 공정 조건 |

## 4. 분야 간 사실 충돌

| 충돌 | 이 분야 관련 id | 무엇이 다른가 | 지시 |
|---|---|---|---|
| F1 Smile/Cry 정의가 반대 | BUMP-A-0146, BUMP-A-0150 | f_warp 현행 표와 WARP-I 가족은 “bump 면 아래 + 중앙이 기준면에서 멂 = Smile”(active 면 기준), COW-I-0141·BUMP-A-0146/0150 해설은 같은 형상을 “Cry” 라 부른다. STANDARDS 2.5(위에서 본 형상: ∩ = Cry, ∪ = Smile)는 **COW·BUMP 쪽과 일치**하고 f_warp 표·WARP-I 가족이 틀렸다. bump 면 아래 자세 12문항은 정답 키가 반대. | WARP: 정답 키 교정 + 가족 3개로 축소(§1). DA: EA_to_DA §1 표 교체 전까지 f_warp 명명표를 근거로 쓰지 않음. TSV: f_warp 사용 54문항 그림 교체. |
| F3 HCB 의 pitch·bump 표현 | BUMP-B-0080 | BUMP-B-0080·COW-A-0073 은 HCB 를 “bump pitch 18 µm 이하/미만” 으로 서술(업체 보도 [R]). STANDARDS 2.4 는 HCB pad pitch ≤ 10 µm·bump 간극 없음, COW-I-0245 는 “D2W HCB 2 µm 급 시연”. 한편 BUMP-A-0002·A-0033~0042 는 solder µbump 를 pitch 6–20 µm 로 설정(2.4 의 µbump 25–55 µm 밖, HCB 영역과 겹침). | COW: “18 µm” 는 [V] 출처 확인 전 정답 근거 금지(FACT) — 쓰더라도 “접합 pitch(pad pitch)” 로. BUMP: B-0080 삭제, A-0033~0042 의 pitch 는 µbump 현실 범위로 바꾸거나 “가정” 명시(NUM 과 함께). |
| F3 HCB 의 pitch·bump 표현 | BUMP-A-0002, BUMP-A-0033~0042 | BUMP-B-0080·COW-A-0073 은 HCB 를 “bump pitch 18 µm 이하/미만” 으로 서술(업체 보도 [R]). STANDARDS 2.4 는 HCB pad pitch ≤ 10 µm·bump 간극 없음, COW-I-0245 는 “D2W HCB 2 µm 급 시연”. 한편 BUMP-A-0002·A-0033~0042 는 solder µbump 를 pitch 6–20 µm 로 설정(2.4 의 µbump 25–55 µm 밖, HCB 영역과 겹침). | COW: “18 µm” 는 [V] 출처 확인 전 정답 근거 금지(FACT) — 쓰더라도 “접합 pitch(pad pitch)” 로. BUMP: B-0080 삭제, A-0033~0042 의 pitch 는 µbump 현실 범위로 바꾸거나 “가정” 명시(NUM 과 함께). |
| F5 MR-MUF 의 가압 여부 / Advanced MR-MUF 의 개량점 | BUMP-I-0159 | COW-I-0021·BUMP-I-0159 는 MR-MUF 를 “die 마다 가압하지 않는 일괄 reflow(층별 하중 제약 없음)” 로, COW-B-0095/B-0114/I-0214/A-0189·WARP-A-0269/0276 은 Advanced MR-MUF 를 “압착(적층) 하중을 낮춘 개량형” 으로 정의한다. 가압이 없다는 방식의 “하중을 낮췄다” 는 서로 맞지 않는다. | FACT 판정 요청: SK hynix [V] 발표 기준으로 Advanced MR-MUF 의 개량점(신규 EMC·칩 휨 제어/가접합 조건 등)을 확정하고, “가접합(pre-bond) 하중” 처럼 무엇의 하중인지 특정. 확정 전에는 COW 가 보유하고 WARP 는 WARP-A-0269/0276 중 1개만, 판정 후 표현 통일. |
| F6 MR-MUF 방열 우위의 근거 | BUMP-I-0159 | 근거가 “고열전도 충전재(EMC)”(COW-B-0087/B-0106), “간극을 채워 경로가 연속”(COW-I-0215), “thermal dummy bump 를 더 많이 배치”(BUMP-I-0159), “filler 를 쓰기 쉬운 구조”(WARP-I-0055)로 제각각이다. 각자 정답으로 두면 다른 분야 문항에서 오답 근거가 된다. | COW 가 [V] 출처로 근거를 확정(EMC 열전도 + dummy bump 밀도)해 해설에 명시하고, BUMP·THERM 은 같은 표현을 쓴다. |
| F8 도금 전류밀도 과다의 결과 | BUMP-I-0144 | TSV-I-0151 정답 “결정립이 거칠어진다”, BUMP-I-0144 정답 “거칠어지고 편차가 커진다”(표면 거칠기). TSV 브리프는 TSV-B-0106 에 대해 “고전류밀도는 핵생성 증가로 결정립이 미세해지는 경향, 주 문제는 pinch-off/void” 로 판정. | FACT 판정 후 통일: 한계 전류밀도 초과 시 “표면 거칠어짐(수지상·burnt)”과 “결정립 크기” 를 구분해 서술. |
