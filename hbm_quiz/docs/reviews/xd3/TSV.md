# XD W3 사후 점검 — TSV 분야 지시

- 작성: XD · 2026-11-21 · 기준: 현재 data(2,448문항) · 요약: `docs/reviews/_xd_post.md`
- 지시 종류: **수정** / **삭제** / **보유** / **재작성** / **mv 판정** / **보강**. "보유" 는 상대 분야가 지우는 쪽이므로 그대로 두되 해설 근거를 유지합니다.
- EA 감사 W3 항목(`docs/reviews/EA_audit/_status.md`)과 충돌하지 않게 반영했습니다(입자 Poisson 예산 COW·MIX 보유, KOZ TSV 보유, MIX 일반론 손실 의도, FEOL-A-0003 이관, refresh 판정 die = 최하단 core die).

## 1. 조치 문항

- 없음

## 2. 이 분야에서 나가는 mv 문항 판정

| id | → | 판정 | 근거 |
|---|---|---|---|
| TSV-A-0123 «stress relief 생략과 추가 박화가 겹친 lot» | BSP | **이관 수용** | BSP-B-0079(목적)·A-9055(휨)와 묻는 판단(crack 원인 분리)이 다름 |
| TSV-A-0155 «underfill void 위치를 예측하는 인자» | COW | **이관 수용** | COW 의 EMC 유동 문항과 판단이 다름(예측 인자 조합) |
| TSV-B-0096 «backside pad 의 접착·차단 금속층» | BSP | **이관 후 삭제** | BSP-I-0095 와 중복 |
| TSV-I-0134 «reveal CMP 후 Cu tip 상면 dishing 의 영향» | BSP | **이관 수용** | BSP 에 reveal CMP dishing → pad 접촉 문항 없음 |
| TSV-I-0139 «reveal 시 뒷면을 너무 많이 깎았을 때» | BSP | **이관 후 삭제** | BSP-I-9018 (BSP-I-0113 도 같은 계열) 와 중복 |

- "이관 후 삭제" 문항은 이 분야에서 더 다듬지 말고 EA Phase 2 에서 삭제 처리(삭제 사유: 근중복 — 도착 분야 대상 id). "이관 수용" 문항은 mv 필드 유지.

## 3. 이 분야로 들어오는 mv 문항 판정

- 없음

## 4. 이 분야가 보유하는 교차 중복(상대 쪽 삭제)

- TSV-A-9007 — 상대 FEOL-A-9037(FEOL) 와 거리별 ΔId 표로 KOZ 판정 동일(KOZ 는 TSV 보유 — EA 항목 2 와 같은 원칙)
- TSV-A-9020 — 상대 FEOL-A-9027(FEOL) 와 via-middle liner 표에서 SACVD O₃-TEOS 선택 동일
- TSV-A-9029 — 상대 FEOL-A-9001(FEOL) 와 TSV 응력 (a/r)² 감쇠로 pMOS KOZ 역산 — 같은 식·같은 설정(EA 감사 W3 항목 2: TSV 보유)
- TSV-A-9041 — 상대 FEOL-A-0028(FEOL) 와 KOZ 면적 계산(EA 감사 W3 항목 2: TSV 보유)
- TSV-B-0060 — 상대 FEOL-B-9011(FEOL) 와 KOZ 정의·이유 동일
- TSV-B-0061 — 상대 FEOL-B-9010(FEOL) 와 via-middle 이름 고르기 동일
- TSV-B-0076 — 상대 FEOL-B-9006(FEOL) 와 erosion 명칭 동일
- TSV-B-9004 — 상대 FEOL-I-9020(FEOL) 와 via-middle liner 저온 증착 이유 동일
- TSV-B-9006 — 상대 FEOL-B-0068(FEOL) 와 Cu pumping 명칭 동일

## 5. 개념 공백 · 보강

- 전 분야 합산 기준 이 분야 소관의 신규 공백 없음.
