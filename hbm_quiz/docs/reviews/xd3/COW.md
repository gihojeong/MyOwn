# XD W3 사후 점검 — COW 분야 지시

- 작성: XD · 2026-11-21 · 기준: 현재 data(2,448문항) · 요약: `docs/reviews/_xd_post.md`
- 지시 종류: **수정** / **삭제** / **보유** / **재작성** / **mv 판정** / **보강**. "보유" 는 상대 분야가 지우는 쪽이므로 그대로 두되 해설 근거를 유지합니다.
- EA 감사 W3 항목(`docs/reviews/EA_audit/_status.md`)과 충돌하지 않게 반영했습니다(입자 Poisson 예산 COW·MIX 보유, KOZ TSV 보유, MIX 일반론 손실 의도, FEOL-A-0003 이관, refresh 판정 die = 최하단 core die).

## 1. 조치 문항

| id | 구분 | 문제 | 지시 |
|---|---|---|---|
| COW-A-0044 | 사실 충돌 | D2W HCB overlay 허용치 ±50 nm(선형 합) — MIX-A-9013 은 ±0.5 µm(RSS)로 10배 차이, 둘 다 pad pitch 미기재 | pad pitch 를 지문에 넣고(예: 3 µm pitch → ±50 nm 가 타당) "설계 조건" 명시 |
| COW-I-9024 | 사실 충돌 | "MR-MUF 는 die 를 올릴 때 짧게 가열·가압해 가접합" — 가압 여부는 FACT X-F5 에서 공식 자료 미확인. 다른 분야(WARP-I-9025·I-0245·A-0276, MIX-A-9035, COW-I-0146)는 "가압 없이 쌓고 일괄 reflow" 로 서술 | 수정: "짧게 가열해 가접합(tack)" 으로 쓰고 가압 단정 삭제(가압을 쓰려면 "이 문항에서는 미소 하중을 가정" 으로 명시) |
| COW-A-9023 | 용어 W | "TC 본딩" 공법명 사용 | 수정: 공법명을 TC-NCF 로(발표 표현 "TC 본딩" 은 괄호) |
| COW-B-0117 | 용어 W | "TC 본딩" 을 공법명으로 사용(TCB 는 장비 방식 — STANDARDS 2.5). Samsung 비교 대상은 TC-NCF | 수정: "TC-NCF(Samsung 발표의 TC 본딩)" 처럼 공법명을 TC-NCF 로 두고 발표 표현은 괄호로 |
| COW-A-0072 | 중복 | 근중복: PROD-I-0037(PROD) 와 간극 제거 → die 두께 여유(공식 1개 대입) — 고급 금지 ①에도 해당 | I 로 내리고 새 id 발급 또는 삭제 (PROD-I-0037 보유). COW 는 COW-A-0071(충전 하한 판정)로 HCB 필요성 보유 |
| COW-A-9018 | 중복 | 근중복: BUMP-A-9014(BUMP) 와 하부 joint IMC 의 √t 누적 계산 동일(MIX-I-9016 은 사례 세트라 보유) | 삭제 (BUMP-A-9014 보유) |
| COW-A-9024 | 중복 | 근중복: MET-A-0008(MET) 와 die 시험 누락(test escape)의 스택 영향 — KGD 시험은 MET 보유 | 삭제 (MET-A-0008 보유) |
| COW-B-0053 | 중복 | 근중복: PROD-B-0031(PROD) 와 최상단 core die 에 뒷면 pad 불필요 | 삭제 또는 적층 순서 고유 판단(먼저 붙은 하부의 하중·열 이력 등)으로 재작성 |
| COW-B-9003 | 중복 | 근중복: THERM-B-9002(THERM) 와 12단 → 접합 계면 12개 세기 동일(PROD 로 오는 SIP-B-9001 도 같은 개념) | 삭제 (THERM-B-9002 보유) |
| COW-B-9007 | 중복 | 근중복: MET-B-0065(MET) 와 SAM 장비 이름 동일 | 삭제 (MET-B-0065 보유) |
| COW-I-9003 | 중복 | 근중복: WARP-I-9011(WARP) 와 underfill 이 bump 피로 수명을 늘리는 기구 동일 | 삭제 (WARP-I-9011 보유) |
| COW-I-9007 | 중복 | 근중복: WARP-I-0260(WARP) 와 Stoney 곡률 ∝ 1/t² 배율 계산 동일 | 삭제 (WARP-I-0260 보유) |
| COW-I-9016 | 중복 | 근중복: THERM-I-9009(THERM) 와 bump/수지 병렬 혼합 유효 열전도율 동일 | 삭제 (THERM-I-9009 보유) |
| COW-I-9025 | 중복 | 근중복: THERM-I-9023(THERM) 와 상부 냉각에서 가장 많은 열이 지나는 계면 동일 | 삭제 (THERM-I-9023 보유) |

## 2. 이 분야에서 나가는 mv 문항 판정

| id | → | 판정 | 근거 |
|---|---|---|---|
| COW-B-0080 «2.5D 조립 뒤 underfill을 채우는 이유» | SIP | **이관 후 삭제** | SIP-B-0084 와 중복 |
| COW-I-0188 «미세 pitch capillary underfill의 난점» | SIP | **이관 수용** | SiP 단계 capillary underfill — SIP-B-9011(이름)·I-9043(충전 시간)과 판단이 다름(COW-B-0050 과 같은 물리는 단계가 달라 허용) |

- "이관 후 삭제" 문항은 이 분야에서 더 다듬지 말고 EA Phase 2 에서 삭제 처리(삭제 사유: 근중복 — 도착 분야 대상 id). "이관 수용" 문항은 mv 필드 유지.

## 3. 이 분야로 들어오는 mv 문항 판정

| id | ← | 판정 | 근거 |
|---|---|---|---|
| BUMP-A-0145 «높이 편차가 큰 die 에 압착 하중만 올린 결과» | BUMP | **이관 수용** | 수치 높이 예산형 고급, COW-I-0149·I-0141 과 판단이 다름 |
| BUMP-I-0134 «NCF 두께 편차가 접합에 주는 영향» | BUMP | **이관 수용** | COW-I-0151(NCF 두께↑)과 달리 두께 편차 |
| BUMP-I-0156 «NCF filler 입경 상한이 미접합으로 이어지는 경로» | BUMP | **이관 수용** | COW-I-0022(대책)와 같은 관측이지만 묻는 것이 경로 — 지문 관측 문장을 다르게 다듬을 것 |
| BUMP-I-0158 «압착 하중을 올려 미접합을 줄인 뒤 새로 생기는 문제» | BUMP | **이관 후 삭제** | COW-I-0149 와 중복 |
| FEOL-A-0019 «극박 core die와 액상 충전이 겹칠 때의 현상» | FEOL | **이관 후 삭제** | COW-I-0213 와 중복 |
| SIP-B-0165 «MR-MUF 에서 단수가 높을 때의 충전 난도» | SIP | **이관 수용** | COW-B-0050(간극 축소 원인)과 묻는 것이 다름(단수 증가 결과) |
| SIP-I-9001 «HCB 전 CMP 기준이 nm 급인 이유» | SIP | **이관 후 삭제** | COW-I-0237 (COW-I-0169 도 인접) 와 중복 |
| TSV-A-0155 «underfill void 위치를 예측하는 인자» | TSV | **이관 수용** | COW 의 EMC 유동 문항과 판단이 다름(예측 인자 조합) |
| WARP-A-0218 «HCB 에서 작은 입자가 넓은 미접합을 만드는 이유» | WARP | **이관 후 삭제** | COW-B-0065 와 중복 |
| WARP-A-0235 «pad 산화와 NCF 유동 지연이 겹친 접합면» | WARP | **이관 수용** | COW-I-0228(공법별 대표 결함)과 다른 복합 조건 |
| WARP-B-0138 «die 를 하나씩 붙이는 적층의 대표 과제» | WARP | **이관 후 삭제** | COW-I-0220 와 중복 |

- 수용 문항은 도착 후 이 분야 문체·지표·그림 규칙으로 판독(EA Phase 2 이동 뒤).

## 4. 이 분야가 보유하는 교차 중복(상대 쪽 삭제)

- COW-A-0153 — 상대 FA-A-0126(FA) 와 접합 온도↑ → 초기 강도↑·IMC 계면 파단·TC 수명↓ 동일(W1 #59 와 같은 개념이 재출현)
- COW-A-0153 — 상대 FA-I-0055(FA) 와 접합 온도 상향 → IMC 과성장 동일
- COW-A-0164 — 상대 BUMP-A-0158(BUMP) 와 단별 IMC 두께 분포의 원인(누적 열이력) 동일 — MIX-A-9038 사례도 같은 데이터
- COW-A-0187 — 상대 MET-I-0138(MET) 와 W2W 에서 수율이 곱해지는 구조 동일(COW 가 W2W/D2W 비교로 포함)
- COW-A-9001 — HCB 입자 Poisson 예산 4분야 중 보유
- COW-B-0058 — 상대 BUMP-I-0138(BUMP) 와 순차 TC 적층에서 하부 joint 가 반복 열이력으로 IMC 성장 동일
- COW-B-0065 — 상대 SAW-B-9016(SAW) 와 HCB 접합면 입자 하나가 넓은 미접합을 만드는 이유 동일
- COW-B-0106 — 상대 WARP-I-0311(THERM) 와 MR-MUF 방열 우위의 공식 근거(dummy bump + EMC) 동일
- COW-B-0117 — 상대 THERM-I-9032(THERM) 와 Samsung HCB 열저항 20 % 개선 발표 회상 동일
- COW-I-0148 — 상대 MIX-B-0016(MIX) 와 Cu recess 과다/돌출 결함 짝 동일
- COW-I-0181 — 상대 BUMP-I-0109(BUMP) 와 formic acid fluxless 접합의 이점 동일(BUMP-B-9009 는 B 기본으로 보유)
- COW-I-0215 — 상대 BUMP-I-0159(BUMP) 와 MR-MUF 가 dummy bump 를 더 둘 수 있는 이유(무가압) 동일
- COW-I-9001 — 상대 SIP-I-9030(SIP) 와 µbump → HCB pitch 축소의 접점 수 배율(pitch² 반비례) 동일

## 5. 개념 공백 · 보강

- 전 분야 합산 기준 이 분야 소관의 신규 공백 없음.
