# XD W3 사후 점검 — PROD 분야 지시

- 작성: XD · 2026-11-21 · 기준: 현재 data(2,448문항) · 요약: `docs/reviews/_xd_post.md`
- 지시 종류: **수정** / **삭제** / **보유** / **재작성** / **mv 판정** / **보강**. "보유" 는 상대 분야가 지우는 쪽이므로 그대로 두되 해설 근거를 유지합니다.
- EA 감사 W3 항목(`docs/reviews/EA_audit/_status.md`)과 충돌하지 않게 반영했습니다(입자 Poisson 예산 COW·MIX 보유, KOZ TSV 보유, MIX 일반론 손실 의도, FEOL-A-0003 이관, refresh 판정 die = 최하단 core die).

## 1. 조치 문항

| id | 구분 | 문제 | 지시 |
|---|---|---|---|
| PROD-A-9032 | 사실 충돌 | HBM PHY 가장자리 폭 10 mm 가정 → 변당 3개. SIP-I-9027(11 mm → 2개)과 결론 반대 | 스택 폭을 SIP 와 같은 값으로 맞추거나 "가상의 스택 폭" 임을 명시 |
| PROD-A-9028 | 사실 충돌(경미) | HBM4 접속 수 2배 → 피치 약 39 µm "기존 접합으로 대응 가능" — 이관 예정 DRAM-I-0165 는 같은 변화를 "정렬·수율 요구 증가" 로 서술 | DRAM-I-0165 는 이관 후 삭제로 판정. PROD-A-9028 해설에 "범위 안이지만 정렬 여유는 줄어든다" 한 문장 추가 권장 |
| PROD-A-9016 | 중복 | 근중복: MIX-A-9036(MIX) 와 dummy bump 면적비 증가 → 12 접합층 ΔT 감소 동일 계산 | 삭제 (MIX-A-9036 보유) |
| PROD-A-9036 | 중복 | 근중복: MET-I-9001(MET) 와 base wafer KGD map 미사용 시 낭비 core die 수 동일 | 삭제 (MET-I-9001 보유) |
| PROD-B-0032 | 중복 | PROD-B-0031 과 같은 개념(top core 에 backside 접속 불필요) — 분야 내부 근중복 | 삭제 (PROD-B-0031 보유) |
| PROD-B-0110 | 중복 | 근중복: BUMP-B-9003(BUMP) 와 µbump pitch 자릿수(수십 µm) 동일 | 삭제 (BUMP-B-9003 보유) |
| PROD-B-9011 | 중복 | 근중복: WARP-I-0056(THERM) 와 상부 냉각 스택에서 가장 뜨거운 위치 동일(DRAM-I-9025 는 core die 를 묻는 refresh 관점이라 보유) | 삭제 (WARP-I-0056 보유) |
| PROD-I-9021 | 중복 | 근중복: SIP-B-9001(PROD) 와 backside pad 보유 die 수 세기 — 이관 문항 SIP-B-9001(die·간극·pad 3종)이 포함 | 삭제 (이관 수용 SIP-B-9001 보유) |

## 2. 이 분야에서 나가는 mv 문항 판정

| id | → | 판정 | 근거 |
|---|---|---|---|
| PROD-A-0016 «극박 16-Hi 의 stack warpage 지배 요소» | WARP | **이관 수용** | WARP 에 극박 16-Hi stack warpage 지배 요소 문항 없음 |
| PROD-A-0033 «간극이 좁은 스택에서 결함 검출이 어려운 이유» | MET | **이관 수용** | MET-I-9036(2D X-ray 층 구분)과 다름 |

- "이관 후 삭제" 문항은 이 분야에서 더 다듬지 말고 EA Phase 2 에서 삭제 처리(삭제 사유: 근중복 — 도착 분야 대상 id). "이관 수용" 문항은 mv 필드 유지.

## 3. 이 분야로 들어오는 mv 문항 판정

| id | ← | 판정 | 근거 |
|---|---|---|---|
| DRAM-I-0165 «HBM4 I/O 확대가 조립에 주는 부담» | DRAM | **이관 후 삭제** | PROD-A-9028·PROD-I-0003 와 중복 |
| SIP-B-0069 «8-Hi 24 GB 와 12-Hi 36 GB 의 같은 대역폭» | SIP | **이관 수용** | PROD-B-0029(스택 수)와 달리 단수 ↔ 대역폭 |
| SIP-B-9001 «8단 스택의 die·간극·pad 보유 die 수» | SIP | **이관 수용** | PROD 의 스택 구성 세기 대표(PROD-I-9021 은 삭제) |

- 수용 문항은 도착 후 이 분야 문체·지표·그림 규칙으로 판독(EA Phase 2 이동 뒤).

## 4. 이 분야가 보유하는 교차 중복(상대 쪽 삭제)

- PROD-B-0031 — 상대 BSP-B-0104(BSP) 와 최상단 core die 에 backside pad 가 없는 이유(PROD-B-0032 도 같은 개념 — PROD 내부 정리)
- PROD-B-0031 — 상대 COW-B-0053(COW) 와 최상단 core die 에 뒷면 pad 불필요
- PROD-B-0037 — 상대 FEOL-I-9027(FEOL) 와 base die 를 로직 공정으로 옮기는 이유 동일
- PROD-B-0103 — 상대 DRAM-B-9011(DRAM) 와 24 Gb × 12단 = 36 GB 용량 환산 동일
- PROD-B-9001 — 상대 DRAM-B-0029(DRAM) 와 HBM3 채널 16 × 64 bit 회상 동일
- PROD-I-0033 — 상대 BSP-I-9052(BSP) 와 die 수율 98 %^12 ≈ 79 % 동일(숫자까지 같음)
- PROD-I-0033 — 상대 DRAM-I-9024(DRAM) 와 die 수율^12 곱 동일 절차
- PROD-I-0037 — 상대 COW-A-0072(COW) 와 간극 제거 → die 두께 여유(공식 1개 대입) — 고급 금지 ①에도 해당
- PROD-I-0037 — 상대 MIX-I-0069(MIX) 와 HCB 전환 시 간극만큼 core die 두께가 늘어남 동일
- PROD-I-9005 — 상대 MIX-I-9001(MIX) 와 16-Hi core die 두께 상한 역산 동일
- PROD-I-9005 — 상대 SIP-I-0063(SIP) 와 16단 높이 상한에서 core die 최대 두께 역산 동일
- PROD-I-9009 — 상대 MIX-I-9010(MIX) 와 HBM3E 9.6 Gb/s 로 8 TB/s 에 필요한 스택 수 7개 동일
- PROD-I-9011 — 상대 DRAM-I-0035(DRAM) 와 HBM4 pseudo channel 64 × 32 bit 구성 동일(세대 사양은 PROD 보유)
- PROD-I-9019 — 상대 SIP-I-0104(SIP) 와 12단 스택 높이 계산 동일
- PROD-I-9032 — 상대 MIX-B-9004(MIX) 와 계면 수율 99.5 %^16 ≈ 92 % 동일
- SIP-B-9001 — 상대 PROD-I-9021(PROD) 와 backside pad 보유 die 수 세기 — 이관 문항 SIP-B-9001(die·간극·pad 3종)이 포함

## 5. 개념 공백 · 보강

- **저단 제품의 비동작(dummy) die·spacer 로 높이 맞춤** — SIP-B-0071·B-0087 삭제 후 0. 높이·평탄도 이유 1개(업체 [V] 근거 확인 후, 없으면 "가정")
