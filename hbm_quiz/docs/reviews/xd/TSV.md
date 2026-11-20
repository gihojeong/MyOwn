# XD 교차분야 지시 — TSV (TSV 형성과 충전)

- 작성: XD (교차분야 일관성) · W1 사전 점검 · 2026-11-20 · 기준: `docs/agents/STANDARDS.md` 2.5 · 3.10
- 대상 파일: `data/00_TSV.json`
- 지시 종류: **수정** · **삭제**(보고서 삭제 표에 “타 분야 중복: 보유 id” 로 기록) · **mv → CODE**(레코드에 `"mv": "CODE"`, 직접 옮기지 말 것) · **보유**(상대 분야가 지우므로 이 문항을 품질 기준으로 다듬을 것)
- XD 판정과 다르게 처리하려면 리뷰 보고서에 근거를 적는다(EA 최종 판정).

## 요약

| 항목 | 건수 |
|---|---|
| 1. 용어 규약 위반 (E / W) | 3 / 1 행 |
| 2. 교차 중복 관련 문항 | 9 |
| 3. 이관 제안 (mv) | 1 |
| 4. 사실 충돌 관여 | 3 건 |

## 1. 용어 규약 위반 (STANDARDS 2.5)

| id | 등급 | 문제 | 지시 |
|---|---|---|---|
| (f_warp 사용 54문항) | W | 열팽창 차·응력 계산 문항이 f_warp 그림을 써서 Smile/Cry 명명표(현행 표는 2.5 와 반대)를 노출: TSV-A-0049~0070, TSV-I-0058~0089 | f_plot(CTE·온도–변위) 또는 f_note 로 교체. 명명 판정 문항이 아니므로 f_warp 금지 |
| TSV-I-0189 | E | HCB 비표준 표기 Hybrid Bonding | “HCB” 로 통일(첫 언급 “HCB(Cu–Cu hybrid bonding)”) |
| TSV-A-0150 | E | HCB 비표준 표기 Hybrid Bonding | “HCB” 로 통일(첫 언급 “HCB(Cu–Cu hybrid bonding)”) |
| TSV-I-0194 | E | Bosch 측벽 식각을 “Erosion” 이라 부름 — 이 문항집에서 Erosion 은 CMP 결함(TSV-B-0076) 용어 | “측면 식각(lateral etch)” 또는 “scallop 깊이” 로. FEOL-I-0013 동일(§4 F7) |

## 2. 교차 중복 · 근중복 (보유 분야 판정)

판정 기준: 그 개념이 어느 분야 학습 목표의 핵심인가(ROSTER §3). 숫자는 핵심 텍스트+보기 char 4-gram Jaccard(참고값, 0.35 이상 판독).

| id | 문제 | 지시 |
|---|---|---|
| TSV-I-0140 | TSV 수를 늘려도 방열 효과가 제한적인 이유 — 보유: WARP-A-0197 | 삭제 (0.48/0.46 — 열 경로 판단은 THERM. TSV 는 공정 관점(liner·KOZ 비용)의 thermal TSV 문항을 새로 쓸 것) |
| TSV-A-0105 | TSV 수를 늘려도 방열 효과가 제한적인 이유 — 보유: WARP-A-0197 | 삭제 (0.48/0.46 — 열 경로 판단은 THERM. TSV 는 공정 관점(liner·KOZ 비용)의 thermal TSV 문항을 새로 쓸 것) |
| TSV-B-0097 | Shadow moiré 이름 고르기 — 보유: MET-B-0036 | 삭제 (0.43) |
| TSV-A-0102 | [보유] chain 저항: 평균 이동 vs 상위 이탈값 해석 — 타 분야 근중복: MET-A-0064 | 보유 분야. 상대 문항은 해당 분야에서 삭제/이관. 남긴 문항은 STANDARDS 기준으로 다듬을 것 (0.43 — TSV 고유 데이터) |
| TSV-A-0136 | HCB 에서 CMP 요구가 극단적으로 높은 이유 — 보유: COW-I-0237 | 삭제 (0.36/0.35 — HCB 접합면 CMP 는 COW) |
| TSV-A-0124 | HCB 에서 CMP 요구가 극단적으로 높은 이유 — 보유: COW-I-0237 | 삭제 (0.36/0.35 — HCB 접합면 CMP 는 COW) |
| TSV-A-0123 | 연삭 후 stress relief 생략 + 박화 → 취급 crack — 근중복 상대: TSV-I-0161, SIP-A-0142 | mv → BSP (0.36 — 연삭·stress relief 는 BSP) |
| TSV-I-0161 | 연삭 후 stress relief 생략 + 박화 → 취급 crack — 보유: TSV-A-0123 (mv → BSP) | mv → BSP 또는 삭제 (0.36 — 연삭·stress relief 는 BSP) |
| TSV-I-0194 | [보유] Bosch 보호 단계↑ → 측면 식각↓·속도↓ — 타 분야 근중복: FEOL-I-0013 | 보유 분야. 상대 문항은 해당 분야에서 삭제/이관. 남긴 문항은 STANDARDS 기준으로 다듬을 것 (0.35 — 용어도 정정(§1)) |

## 3. 이관 제안 (오분류)

| id | 지시 | 이유 |
|---|---|---|
| TSV-A-0155 | mv → COW (`"mv": "COW"`, 다듬은 뒤) | underfill void 위치 예측 — 적층 충전 |

## 4. 분야 간 사실 충돌

| 충돌 | 이 분야 관련 id | 무엇이 다른가 | 지시 |
|---|---|---|---|
| F1 Smile/Cry 정의가 반대 | TSV-A-0049~0070, TSV-I-0058~0089 (f_warp 그림) | f_warp 현행 표와 WARP-I 가족은 “bump 면 아래 + 중앙이 기준면에서 멂 = Smile”(active 면 기준), COW-I-0141·BUMP-A-0146/0150 해설은 같은 형상을 “Cry” 라 부른다. STANDARDS 2.5(위에서 본 형상: ∩ = Cry, ∪ = Smile)는 **COW·BUMP 쪽과 일치**하고 f_warp 표·WARP-I 가족이 틀렸다. bump 면 아래 자세 12문항은 정답 키가 반대. | WARP: 정답 키 교정 + 가족 3개로 축소(§1). DA: EA_to_DA §1 표 교체 전까지 f_warp 명명표를 근거로 쓰지 않음. TSV: f_warp 사용 54문항 그림 교체. |
| F7 “Erosion” 의 두 가지 뜻 | TSV-I-0194, ↔ TSV-B-0076, TSV-A-0099 | TSV-B-0076·A-0099 는 Erosion = CMP 에서 조밀 패턴 영역 전체가 낮아짐, TSV-I-0194·FEOL-I-0013 은 Bosch 측벽 식각을 “Erosion” 이라 부른다. | 식각 문항을 “측면 식각(lateral etch)/scallop” 으로 바꿈. |
| F8 도금 전류밀도 과다의 결과 | TSV-I-0151, TSV-B-0106 | TSV-I-0151 정답 “결정립이 거칠어진다”, BUMP-I-0144 정답 “거칠어지고 편차가 커진다”(표면 거칠기). TSV 브리프는 TSV-B-0106 에 대해 “고전류밀도는 핵생성 증가로 결정립이 미세해지는 경향, 주 문제는 pinch-off/void” 로 판정. | FACT 판정 후 통일: 한계 전류밀도 초과 시 “표면 거칠어짐(수지상·burnt)”과 “결정립 크기” 를 구분해 서술. |
