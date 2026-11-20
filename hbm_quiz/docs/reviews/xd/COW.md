# XD 교차분야 지시 — COW (CoW 적층 접합)

- 작성: XD (교차분야 일관성) · W1 사전 점검 · 2026-11-20 · 기준: `docs/agents/STANDARDS.md` 2.5 · 3.10
- 대상 파일: `data/04_COW.json`
- 지시 종류: **수정** · **삭제**(보고서 삭제 표에 “타 분야 중복: 보유 id” 로 기록) · **mv → CODE**(레코드에 `"mv": "CODE"`, 직접 옮기지 말 것) · **보유**(상대 분야가 지우므로 이 문항을 품질 기준으로 다듬을 것)
- XD 판정과 다르게 처리하려면 리뷰 보고서에 근거를 적는다(EA 최종 판정).

## 요약

| 항목 | 건수 |
|---|---|
| 1. 용어 규약 위반 (E / W) | 6 / 9 행 |
| 2. 교차 중복 관련 문항 | 22 |
| 3. 이관 제안 (mv) | 0 |
| 4. 사실 충돌 관여 | 4 건 |

## 1. 용어 규약 위반 (STANDARDS 2.5)

| id | 등급 | 문제 | 지시 |
|---|---|---|---|
| COW-I-0141 | W | 해설의 명명(“bump 면 아래에서 중앙이 솟은 형상 = Cry”)은 **2.5 와 일치**. 문제는 f_warp 현행 표·WARP-I 가족과 반대라는 점(→ §4 사실 충돌 F1) | 명명은 유지. 해설에서 명명 설명은 1문장으로 줄이고 하중 상향 결과(가장자리 미접합↓·중앙 과압축↑)의 근거와 오답 3개 해설로 채울 것 |
| COW-B-0090 | E | “TCB와 MR-MUF” — TCB 를 공법명으로 사용 | “TC-NCF와 MR-MUF” 로. TCB 는 “TC-NCF 의 열압착(TCB) 장비” 처럼 장비 문맥에서만 |
| COW-I-0203 | E | “TCB와 MR-MUF” 대비 | “TC-NCF와 MR-MUF” 로 |
| COW-A-0184 | E | “TCB와 MR-MUF” 대비 | “TC-NCF와 MR-MUF” 로 |
| COW-I-0200 | E | “TCB 방식” 을 공법명으로 사용 | 문맥에 따라 “TC-NCF” 또는 “열압착(TCB) 장비” |
| COW-B-0053 | E | “TCB 적층” 을 공법명으로 사용 | “TC-NCF 적층” 또는 “열압착(TCB) 적층” — NCF/NCP/MUF 중 무엇과 결합했는지 명시 |
| (109문항) | E | HCB 를 “Hybrid Bonding / hybrid bonding / 하이브리드 본딩 / Hybrid Copper Bonding” 으로 혼용: COW-A-0002~0026, COW-A-0072~0078, COW-A-0089~0110, COW-A-0157~0159, COW-A-0161, COW-A-0163, COW-A-0174, COW-A-0185, COW-B-0059~0060, COW-B-0092~0093, COW-B-0095, COW-B-0116, COW-I-0021~0023, COW-I-0025, COW-I-0048~0079, COW-I-0148, COW-I-0187, COW-I-0206~0208, COW-I-0245 | 공법명은 **HCB** 로 통일(첫 언급만 “HCB(Cu–Cu hybrid bonding)”). 같은 문항 안 영문/한글 혼용 금지(3.8). 보기에서 공법을 고르는 문항은 반드시 “HCB” |
| (99문항) | W | 약어 없이 “hybrid copper bonding” 만 반복(HCB 미사용): COW-A-0001, COW-A-0027~0070, COW-A-0166, COW-A-0170, COW-A-0177~0178, COW-A-0186~0188, COW-B-0001~0026, COW-B-0065, COW-B-0071~0072, COW-B-0094, COW-B-0102, COW-I-0168~0172, COW-I-0177~0181, COW-I-0186, COW-I-0210~0212, COW-I-0218~0219 | 첫 언급 “HCB(hybrid copper bonding)”, 이후 “HCB” |
| COW-B-0108 | W | “MUF” 단독 표기 | MR-MUF 를 뜻하면 “MR-MUF”, 일반 molded underfill 이면 “MUF(molded underfill)” 로 풀어 씀 |
| COW-B-0079 | W | “Mass Reflow” 를 공법명처럼 사용 | 공법명은 “MR-MUF”, 접합 단계만 가리킬 때 “mass reflow(일괄 리플로)” |
| COW-A-0072 | W | µbump 표기 변형 micro-bump | “µbump”(U+00B5, 하이픈 없음) 로 통일 — STANDARDS 2.4 표기 |
| COW-A-0073 | W | µbump 표기 변형 micro-bump | “µbump”(U+00B5, 하이픈 없음) 로 통일 — STANDARDS 2.4 표기 |
| COW-I-0023 | W | µbump 표기 변형 micro-bump | “µbump”(U+00B5, 하이픈 없음) 로 통일 — STANDARDS 2.4 표기 |
| COW-B-0116 | W | µbump 표기 변형 마이크로 범프 | “µbump”(U+00B5, 하이픈 없음) 로 통일 — STANDARDS 2.4 표기 |
| COW-I-0187 | W | µbump 표기 변형 마이크로범프 | “µbump”(U+00B5, 하이픈 없음) 로 통일 — STANDARDS 2.4 표기 |

## 2. 교차 중복 · 근중복 (보유 분야 판정)

판정 기준: 그 개념이 어느 분야 학습 목표의 핵심인가(ROSTER §3). 숫자는 핵심 텍스트+보기 char 4-gram Jaccard(참고값, 0.35 이상 판독).

| id | 문제 | 지시 |
|---|---|---|
| COW-A-0160 | [보유] 미세 피치에서 solder 접합 공정 창이 좁아지는 인자 — 타 분야 근중복: BUMP-A-0147, BUMP-A-0150 | 보유 분야. 상대 문항은 해당 분야에서 삭제/이관. 남긴 문항은 STANDARDS 기준으로 다듬을 것 (W_NEAR_DUP_X 0.83. TCB 공정 창은 COW 학습 목표) |
| COW-A-0078 | [보유] 구조·공법 변경 시 검사 체계도 바꿔야 하는 이유(일반론) — 타 분야 근중복: SIP-B-0148, SIP-A-0160, MIX-B-0006, MIX-A-0049, MIX-A-0039, COW-I-0229, SAW-I-0041 | 보유 분야. 상대 문항은 해당 분야에서 삭제/이관. 남긴 문항은 STANDARDS 기준으로 다듬을 것 (0.62/0.45 — COW-A-0078 만 구체 조건 보유. SAW 는 “stealth dicing 내부 균열은 외관 AOI 로 안 보임 → IR 검사” 처럼 구체화) |
| COW-I-0229 | 구조·공법 변경 시 검사 체계도 바꿔야 하는 이유(일반론) — 보유: COW-A-0078 | 삭제 (0.62/0.45 — COW-A-0078 만 구체 조건 보유. SAW 는 “stealth dicing 내부 균열은 외관 AOI 로 안 보임 → IR 검사” 처럼 구체화) |
| COW-I-0167 | [보유] 일괄(gang) 접합 방식의 과제 — 타 분야 근중복: SIP-B-0094 | 보유 분야. 상대 문항은 해당 분야에서 삭제/이관. 남긴 문항은 STANDARDS 기준으로 다듬을 것 (0.62) |
| COW-B-0057 | [보유] 적층 단마다 정렬 마크 재인식 — 타 분야 근중복: SIP-B-0091 | 보유 분야. 상대 문항은 해당 분야에서 삭제/이관. 남긴 문항은 STANDARDS 기준으로 다듬을 것 (0.58) |
| COW-A-0181 | [보유] 새 접합 방식을 단계적으로 도입하는 이유 — 타 분야 근중복: COW-I-0178, WARP-A-0217 | 보유 분야. 상대 문항은 해당 분야에서 삭제/이관. 남긴 문항은 STANDARDS 기준으로 다듬을 것 (0.55/0.45 — THERM 파일에 있는 비열(非熱) 문항) |
| COW-I-0178 | 새 접합 방식을 단계적으로 도입하는 이유 — 보유: COW-A-0181 | COW 내 통합(삭제) (0.55/0.45 — THERM 파일에 있는 비열(非熱) 문항) |
| COW-I-0180 | [보유] 접합 직전 대기(queue) 시간 관리 — 타 분야 근중복: BSP-B-0106, BUMP-B-0028 | 보유 분야. 상대 문항은 해당 분야에서 삭제/이관. 남긴 문항은 STANDARDS 기준으로 다듬을 것 (0.51/0.36) |
| COW-I-0155 | [보유] TCB 저온·장시간 조정의 부작용 — 타 분야 근중복: MIX-A-0004 | 보유 분야. 상대 문항은 해당 분야에서 삭제/이관. 남긴 문항은 STANDARDS 기준으로 다듬을 것 (0.45) |
| COW-A-0155 | [보유] bond head 기울기 vs die warpage 의 불량 맵 분리 — 타 분야 근중복: WARP-A-0184 | 보유 분야. 상대 문항은 해당 분야에서 삭제/이관. 남긴 문항은 STANDARDS 기준으로 다듬을 것 (0.45) |
| COW-B-0056 | [보유] 단수↑ → TCB 압착 사이클 누적 — 타 분야 근중복: SIP-B-0090 | 보유 분야. 상대 문항은 해당 분야에서 삭제/이관. 남긴 문항은 STANDARDS 기준으로 다듬을 것 (0.45) |
| COW-A-0165 | [보유] 12→16단 확장 시 TC-NCF 제약 조합 — 타 분야 근중복: SIP-A-0143 | 보유 분야. 상대 문항은 해당 분야에서 삭제/이관. 남긴 문항은 STANDARDS 기준으로 다듬을 것 (0.44) |
| COW-B-0050 | [보유] 미세 피치 capillary underfill 충전 난이도 — 타 분야 근중복: COW-I-0188, SIP-I-0134 | 보유 분야. 상대 문항은 해당 분야에서 삭제/이관. 남긴 문항은 STANDARDS 기준으로 다듬을 것 (0.40) |
| COW-I-0188 | 미세 피치 capillary underfill 충전 난이도 — 보유: COW-B-0050 | mv → SIP (SiP 단계 underfill) (0.40) |
| COW-I-0237 | [보유] HCB 에서 CMP 요구가 극단적으로 높은 이유 — 타 분야 근중복: COW-A-0158, TSV-A-0136, TSV-A-0124 | 보유 분야. 상대 문항은 해당 분야에서 삭제/이관. 남긴 문항은 STANDARDS 기준으로 다듬을 것 (0.36/0.35 — HCB 접합면 CMP 는 COW) |
| COW-A-0158 | HCB 에서 CMP 요구가 극단적으로 높은 이유 — 보유: COW-I-0237 | COW 내 통합 (0.36/0.35 — HCB 접합면 CMP 는 COW) |
| COW-I-0141 | [보유] warpage 가 있는 die 에 하중만 올린 결과 — 타 분야 근중복: BUMP-A-0146, WARP-A-0185 | 보유 분야. 상대 문항은 해당 분야에서 삭제/이관. 남긴 문항은 STANDARDS 기준으로 다듬을 것 (0.39 — Smile/Cry 표기도 정리(§1)) |
| COW-I-0161 | [보유] NCF 유동 온도와 solder 용융 구간 불일치 — 타 분야 근중복: BUMP-I-0135 | 보유 분야. 상대 문항은 해당 분야에서 삭제/이관. 남긴 문항은 STANDARDS 기준으로 다듬을 것 (0.35) |
| COW-I-0165 | [보유] fillet 형상 관리 이유 — 타 분야 근중복: BUMP-B-0064 | 보유 분야. 상대 문항은 해당 분야에서 삭제/이관. 남긴 문항은 STANDARDS 기준으로 다듬을 것 (0.41) |
| COW-A-0153 | [보유] 압착 온도↑ → 초기 강도↑ · TC 수명↓ — 타 분야 근중복: MET-A-0070, FA-A-0031 | 보유 분야. 상대 문항은 해당 분야에서 삭제/이관. 남긴 문항은 STANDARDS 기준으로 다듬을 것 (0.36) |
| COW-A-0192 | [보유] 두 공법을 모두 보유하는 이유 — 타 분야 근중복: MIX-A-0102 | 보유 분야. 상대 문항은 해당 분야에서 삭제/이관. 남긴 문항은 STANDARDS 기준으로 다듬을 것 (0.36) |
| COW-A-0073 | [보유] HCB 의 pitch 축소(“18 µm”) — 타 분야 근중복: BUMP-B-0080 | 보유 분야. 상대 문항은 해당 분야에서 삭제/이관. 남긴 문항은 STANDARDS 기준으로 다듬을 것 (개념 중복 + 사실 충돌 F3) |

## 3. 이관 제안 (오분류)

- 해당 없음.

## 4. 분야 간 사실 충돌

| 충돌 | 이 분야 관련 id | 무엇이 다른가 | 지시 |
|---|---|---|---|
| F1 Smile/Cry 정의가 반대 | COW-I-0141 | f_warp 현행 표와 WARP-I 가족은 “bump 면 아래 + 중앙이 기준면에서 멂 = Smile”(active 면 기준), COW-I-0141·BUMP-A-0146/0150 해설은 같은 형상을 “Cry” 라 부른다. STANDARDS 2.5(위에서 본 형상: ∩ = Cry, ∪ = Smile)는 **COW·BUMP 쪽과 일치**하고 f_warp 표·WARP-I 가족이 틀렸다. bump 면 아래 자세 12문항은 정답 키가 반대. | WARP: 정답 키 교정 + 가족 3개로 축소(§1). DA: EA_to_DA §1 표 교체 전까지 f_warp 명명표를 근거로 쓰지 않음. TSV: f_warp 사용 54문항 그림 교체. |
| F3 HCB 의 pitch·bump 표현 | COW-A-0073, COW-I-0245, COW-B-0003~0026 (HCB 분기에 bump pitch·간극) | BUMP-B-0080·COW-A-0073 은 HCB 를 “bump pitch 18 µm 이하/미만” 으로 서술(업체 보도 [R]). STANDARDS 2.4 는 HCB pad pitch ≤ 10 µm·bump 간극 없음, COW-I-0245 는 “D2W HCB 2 µm 급 시연”. 한편 BUMP-A-0002·A-0033~0042 는 solder µbump 를 pitch 6–20 µm 로 설정(2.4 의 µbump 25–55 µm 밖, HCB 영역과 겹침). | COW: “18 µm” 는 [V] 출처 확인 전 정답 근거 금지(FACT) — 쓰더라도 “접합 pitch(pad pitch)” 로. BUMP: B-0080 삭제, A-0033~0042 의 pitch 는 µbump 현실 범위로 바꾸거나 “가정” 명시(NUM 과 함께). |
| F5 MR-MUF 의 가압 여부 / Advanced MR-MUF 의 개량점 | COW-I-0021, COW-B-0095, COW-B-0114, COW-I-0214, COW-A-0189 | COW-I-0021·BUMP-I-0159 는 MR-MUF 를 “die 마다 가압하지 않는 일괄 reflow(층별 하중 제약 없음)” 로, COW-B-0095/B-0114/I-0214/A-0189·WARP-A-0269/0276 은 Advanced MR-MUF 를 “압착(적층) 하중을 낮춘 개량형” 으로 정의한다. 가압이 없다는 방식의 “하중을 낮췄다” 는 서로 맞지 않는다. | FACT 판정 요청: SK hynix [V] 발표 기준으로 Advanced MR-MUF 의 개량점(신규 EMC·칩 휨 제어/가접합 조건 등)을 확정하고, “가접합(pre-bond) 하중” 처럼 무엇의 하중인지 특정. 확정 전에는 COW 가 보유하고 WARP 는 WARP-A-0269/0276 중 1개만, 판정 후 표현 통일. |
| F6 MR-MUF 방열 우위의 근거 | COW-B-0087, COW-B-0106, COW-I-0215 | 근거가 “고열전도 충전재(EMC)”(COW-B-0087/B-0106), “간극을 채워 경로가 연속”(COW-I-0215), “thermal dummy bump 를 더 많이 배치”(BUMP-I-0159), “filler 를 쓰기 쉬운 구조”(WARP-I-0055)로 제각각이다. 각자 정답으로 두면 다른 분야 문항에서 오답 근거가 된다. | COW 가 [V] 출처로 근거를 확정(EMC 열전도 + dummy bump 밀도)해 해설에 명시하고, BUMP·THERM 은 같은 표현을 쓴다. |
