# XD W3 사후 점검 — THERM 분야 지시

- 작성: XD · 2026-11-21 · 기준: 현재 data(2,448문항) · 요약: `docs/reviews/_xd_post.md`
- 지시 종류: **수정** / **삭제** / **보유** / **재작성** / **mv 판정** / **보강**. "보유" 는 상대 분야가 지우는 쪽이므로 그대로 두되 해설 근거를 유지합니다.
- EA 감사 W3 항목(`docs/reviews/EA_audit/_status.md`)과 충돌하지 않게 반영했습니다(입자 Poisson 예산 COW·MIX 보유, KOZ TSV 보유, MIX 일반론 손실 의도, FEOL-A-0003 이관, refresh 판정 die = 최하단 core die).

## 1. 조치 문항

| id | 구분 | 문제 | 지시 |
|---|---|---|---|
| THERM-A-9004 | 규약(EA 5) | "base die 온도로 판정한 refresh 점유율" — refresh/온도 구간은 셀이 있는 최하단 core die 로 판정(EA 감사 W3 항목 5) | 수정: 판정 대상을 "최하단 core die(core 1)" 로 바꾸고 base–core1 간극 ΔT 를 빼서 재계산(THERM-A-9026 의 방식). 정답·오답 값 재검(NUM) |
| THERM-A-9017 | 규약(EA 5) | base die 온도와 구간 판정 — refresh/온도 구간은 셀이 있는 최하단 core die 로 판정(EA 감사 W3 항목 5) | 수정: 판정 대상을 "최하단 core die(core 1)" 로 바꾸고 base–core1 간극 ΔT 를 빼서 재계산(THERM-A-9026 의 방식). 정답·오답 값 재검(NUM) |
| THERM-A-9021 | 규약(EA 5) | HBM 상한 85 °C 를 base die 에 적용 — refresh/온도 구간은 셀이 있는 최하단 core die 로 판정(EA 감사 W3 항목 5) | 수정: 판정 대상을 "최하단 core die(core 1)" 로 바꾸고 base–core1 간극 ΔT 를 빼서 재계산(THERM-A-9026 의 방식). 정답·오답 값 재검(NUM) |
| THERM-A-9024 | 규약(EA 5) | base die 온도로 정상/확장 구간 판정 — refresh/온도 구간은 셀이 있는 최하단 core die 로 판정(EA 감사 W3 항목 5) | 수정: 판정 대상을 "최하단 core die(core 1)" 로 바꾸고 base–core1 간극 ΔT 를 빼서 재계산(THERM-A-9026 의 방식). 정답·오답 값 재검(NUM) |
| THERM-A-9032 | 규약(EA 5) | base die 88 °C 로 확장 구간 판정 — refresh/온도 구간은 셀이 있는 최하단 core die 로 판정(EA 감사 W3 항목 5) | 수정: 판정 대상을 "최하단 core die(core 1)" 로 바꾸고 base–core1 간극 ΔT 를 빼서 재계산(THERM-A-9026 의 방식). 정답·오답 값 재검(NUM) |
| WARP-A-0003 | 규약(EA 5) | 제목·질문이 "base die 온도와 refresh 구간 판정" — refresh/온도 구간은 셀이 있는 최하단 core die 로 판정(EA 감사 W3 항목 5) | 수정: 판정 대상을 "최하단 core die(core 1)" 로 바꾸고 base–core1 간극 ΔT 를 빼서 재계산(THERM-A-9026 의 방식). 정답·오답 값 재검(NUM) |
| WARP-A-0004 | 규약(EA 5) | base die 온도로 95 °C 초과 판정 — refresh/온도 구간은 셀이 있는 최하단 core die 로 판정(EA 감사 W3 항목 5) | 수정: 판정 대상을 "최하단 core die(core 1)" 로 바꾸고 base–core1 간극 ΔT 를 빼서 재계산(THERM-A-9026 의 방식). 정답·오답 값 재검(NUM) |
| WARP-A-0033 | 규약(EA 5) | "base die 85 °C 를 지키는 허용 열유속" — 셀 없는 base die 에 DRAM 상한 적용 — refresh/온도 구간은 셀이 있는 최하단 core die 로 판정(EA 감사 W3 항목 5) | 수정: 판정 대상을 "최하단 core die(core 1)" 로 바꾸고 base–core1 간극 ΔT 를 빼서 재계산(THERM-A-9026 의 방식). 정답·오답 값 재검(NUM) |
| WARP-A-0208 | 규약(EA 5) | base die 86 °C 로 확장 구간 판정 — refresh/온도 구간은 셀이 있는 최하단 core die 로 판정(EA 감사 W3 항목 5) | 수정: 판정 대상을 "최하단 core die(core 1)" 로 바꾸고 base–core1 간극 ΔT 를 빼서 재계산(THERM-A-9026 의 방식). 정답·오답 값 재검(NUM) |
| THERM-I-9022 | 사실 충돌 | HCB 계면 유효 k ≈ 99 W/m·K(Cu 25 % 병렬) — 다른 문항의 HCB 계면 가정과 2 자릿수 차 | 해설에 "병렬 근사는 상한(구속 저항·계면 저항 무시)" 한 문장 추가, 위 기준 범위와 정합 |
| WARP-I-0029 | 사실 충돌 | HCB 접합 계면층 1 µm·유효 5 W/m·K(≈ 0.2 mm²·K/W) 가정 — 같은 분야 THERM-I-9022(유효 ≈ 99 W/m·K, ≈ 0.01), WARP-A-0059(간극당 2), WARP-I-0061(1.2 vs µbump 4.2), COW-A-9023(접합층 열저항의 30 % 잔존)와 자릿수가 다름 | THERM 이 HCB 계면·µbump 접합층의 면적 열저항 기준 범위를 한 줄로 정해(예: µbump 접합층 5–17, HCB 계면 ≲ 1 mm²·K/W, 모두 "문항 설정값") 해당 문항 지문에 범위 안 값과 "가정" 을 명시. THERM-I-9022 는 병렬 근사가 상한값임을 해설에 적기 |
| THERM-A-9036 | 용어 W | "TC 본딩" 공법명 사용 | 수정: TC-NCF 로(발표 표현은 괄호) |
| THERM-I-9014 | 중복 | 근중복: DRAM-I-9007(DRAM) 와 tRFC ÷ tREFI refresh 점유율 계산 동일(THERM-A-9004 가 열 연계 판단을 보유) | 삭제 (DRAM-I-9007 보유) |
| THERM-I-9032 | 중복 | 근중복: COW-B-0117(COW) 와 Samsung HCB 열저항 20 % 개선 발표 회상 동일 | 삭제 (COW-B-0117 보유) |
| WARP-I-0311 | 중복 | 근중복: COW-B-0106(COW) 와 MR-MUF 방열 우위의 공식 근거(dummy bump + EMC) 동일 | 삭제 (COW-B-0106 보유) |

## 2. 이 분야에서 나가는 mv 문항 판정

| id | → | 판정 | 근거 |
|---|---|---|---|
| WARP-A-0249 «열화상 발열점과 실제 결함 위치가 어긋나는 이유» | FA | **이관 후 삭제** | FA-I-0076 와 중복 |
| WARP-A-0260 «LIT 위상 지연으로 발열 깊이를 추정하는 원리» | FA | **이관 후 삭제** | FA-I-0003·FA-B-0001 와 중복 |
| WARP-B-0121 «결함 부위가 갈수록 빨리 나빠지는 되먹임» | FA | **이관 수용** | FA-A-0037(정량)과 B/A 짝 |
| WARP-B-0141 «주기 신호로 미세 발열 위치를 찾는 기법» | FA | **이관 후 삭제** | FA-B-0003 와 중복 |
| WARP-B-0142 «LIT 가 단순 열화상보다 미세 발열에 강한 이유» | FA | **이관 후 삭제** | FA-I-0075 와 중복 |
| WARP-I-0283 «연삭 중 냉각수를 충분히 공급하는 이유» | BSP | **이관 수용** | BSP 에 연삭 냉각수 문항 없음 |
| WARP-I-0284 «수지를 빠르게 냉각할 때 커지는 잔류 응력» | WARP | **이관 수용** | WARP 에 냉각 속도 → 잔류 응력 문항 없음 |
| WARP-I-0321 «몰딩 수축 편차가 실장 불량으로 이어지는 경로» | WARP | **이관 수용** | WARP-B-0094 와 다름(실장 경로) |

- "이관 후 삭제" 문항은 이 분야에서 더 다듬지 말고 EA Phase 2 에서 삭제 처리(삭제 사유: 근중복 — 도착 분야 대상 id). "이관 수용" 문항은 mv 필드 유지.

## 3. 이 분야로 들어오는 mv 문항 판정

| id | ← | 판정 | 근거 |
|---|---|---|---|
| FA-A-0024 «HBM 상면 높이와 SoC 높이의 정합» | FA | **이관 후 삭제** | THERM 의 WARP-A-0208(계산형)·WARP-A-0246 와 중복 |
| WARP-A-0246 «높이 산포·TIM 압축·lid 평탄도의 국부 열저항» | WARP | **이관 수용** | THERM 에 높이 산포·lid 평탄도 복합 기구 없음(WARP-A-0208 은 계산형) |
| WARP-B-0078 «패키지 재료의 열전도율 크기 순서» | WARP | **이관 후 삭제** | THERM-B-9003 와 중복 |
| WARP-I-0320 «여러 스택 가운데 한 곳만 뜨거워지는 원인» | WARP | **이관 후 삭제** | WARP-A-0246(같이 이관, 고급 보유) 와 중복 |

- 수용 문항은 도착 후 이 분야 문체·지표·그림 규칙으로 판독(EA Phase 2 이동 뒤).

## 4. 이 분야가 보유하는 교차 중복(상대 쪽 삭제)

- THERM-B-9002 — 상대 COW-B-9003(COW) 와 12단 → 접합 계면 12개 세기 동일(PROD 로 오는 SIP-B-9001 도 같은 개념)
- THERM-B-9009 — 상대 BUMP-B-9010(BUMP) 와 thermal dummy bump 의 역할 동일
- THERM-I-9009 — 상대 COW-I-9016(COW) 와 bump/수지 병렬 혼합 유효 열전도율 동일
- THERM-I-9023 — 상대 COW-I-9025(COW) 와 상부 냉각에서 가장 많은 열이 지나는 계면 동일
- WARP-I-0056 — 상대 MIX-B-9012(MIX) 와 상부 냉각 스택에서 가장 뜨거운 die(base die) 동일
- WARP-I-0056 — 상대 PROD-B-9011(PROD) 와 상부 냉각 스택에서 가장 뜨거운 위치 동일(DRAM-I-9025 는 core die 를 묻는 refresh 관점이라 보유)

## 5. 개념 공백 · 보강

- **JEDEC 패키지 열저항 지표(θJC·ψJT, JESD51 계열)** — 전 분야 0. 정의·측정 조건 차이를 묻는 초·중급 1–2개(수치 출처는 FACT 확인 후)
- **TIM 재료 선택(indium·liquid metal·graphite·solder TIM)** — 전 분야 0(펌프아웃 등 열화는 2문항 있음). 재료별 k·신뢰성 상충 1개
- **HCB 계면·µbump 접합층 열저항 기준 범위** — 사실 충돌 F2 참고 — 문항 설정값 범위를 분야 공통으로 정해 문서화
