# XD 교차분야 일관성 점검 — W1 사전 점검 요약

- 작성: XD · 2026-11-20 · 입력: `data/*.json` 14개 파일(5,000문항, WARP 분할 후 상태 — 05_WARP 226 · 13_THERM 537) · 기준: STANDARDS 2.5(용어 규약) · 3.10(중복)
- 분야별 지시: `docs/reviews/xd/CODE.md` (id · 문제 · 지시). 이 문서는 집계와 판정 원칙, 다른 에이전트에 넘길 사항만 담는다.
- 읽기 전용으로 수행(data/·template.html·tools/ 미수정). 스냅샷 시점 이후 분야 에이전트가 고친 문항은 W3 사후 점검(`_xd_post.md`)에서 다시 본다.

## 1. 한눈에

| 분야 | 용어 E | 용어 W | 교차 중복 관련 | mv 제안 | 사실 충돌 관여 |
|---|---|---|---|---|---|
| [TSV](TSV.md) | 3 | 1 | 9 | 1 | 3 |
| [BSP](BSP.md) | 0 | 0 | 2 | 0 | 0 |
| [BUMP](BUMP.md) | 7 | 2 | 14 | 3 | 6 |
| [SAW](SAW.md) | 0 | 0 | 9 | 0 | 0 |
| [COW](COW.md) | 6 | 9 | 22 | 0 | 4 |
| [WARP](WARP.md) | 15 | 1 | 19 | 9 | 2 |
| [THERM](THERM.md) | 50 | 1 | 16 | 4 | 2 |
| [SIP](SIP.md) | 3 | 1 | 27 | 5 | 1 |
| [FA](FA.md) | 1 | 0 | 15 | 3 | 1 |
| [PROD](PROD.md) | 2 | 1 | 20 | 2 | 2 |
| [DRAM](DRAM.md) | 0 | 0 | 19 | 1 | 0 |
| [MET](MET.md) | 2 | 2 | 18 | 3 | 1 |
| [MIX](MIX.md) | 1 | 0 | 24 | 0 | 0 |
| [FEOL](FEOL.md) | 1 | 0 | 5 | 9 | 1 |

- “용어 E/W” 는 표의 행 수다. COW 의 HCB 표기는 한 행에 여러 문항을 묶었다(아래 §2 의 문항 수 참고).

## 2. 용어 규약 위반 (문항 수)

| 규약 | 등급 | 문항 수 | 분포 | 요지 |
|---|---|---|---|---|
| N단 ↔ 간극 수 | E | 49 | THERM 48 · MET 1 | THERM 열저항 가족이 “12단 → 간극은 die 수보다 하나 적은 11개”, f_therm.n 에 core 수 입력. MET-I-0001 “접합 간극 11곳”. SIP 는 규약대로 “core n 장 → 간극 n 개” |
| N단 ↔ 간극 수 (표현) | W | 71 | SIP 71 | 값은 규약과 일치하나 “접합 간극은 die 수보다 하나 적습니다” — THERM 오류와 같은 문장이라 “간극 수 = core die 수(N)” 로 |
| Smile / Cry | E | 16 | WARP 15 · BUMP 1 | bump 면 아래 자세 12문항(WARP-I-0003~0025 중) 정답 키가 2.5 와 반대, WARP-I-0001 전제·정답 반대, WARP-B-0001 지문 자기모순, WARP-A-0185 자세 미기재, BUMP-A-0150 해설 혼입 |
| Smile / Cry | W | 69 | WARP 12 · TSV 54 · SIP 1 · COW 1 · BUMP 1 | BEOL 면 위 12문항(정답은 맞으나 f_warp 명명표 근거 + 24문항 가족), f_warp 를 CTE 계산에 쓴 TSV 54·SIP 1(명명표 노출), 해설 명명 설명 |
| 공법명: TCB 를 공법명으로 | E | 9 | COW 5 · BUMP 2 · SIP 1 · PROD 1 | “TCB와 MR-MUF”, “TCB 방식/적층” → TC-NCF (TCB 는 장비 방식) |
| 공법명: HCB 비표준 표기 | E | 123 | COW 109 · BUMP 4 · TSV 2 · SIP 2 · THERM 2 · FA·PROD·MET·MIX 각 1 | Hybrid Bonding / hybrid bonding / 하이브리드 본딩 / Hybrid Copper Bonding 혼용 → “HCB” |
| 공법명: 약어 없는 full name | W | 99 | COW 99 | “hybrid copper bonding” 만 반복 → 첫 언급 “HCB(hybrid copper bonding)” |
| 공법명: MUF 단독·Mass Reflow | W | 2 (+BUMP-B-0029 E) | COW 2 | MR-MUF 로 |
| µbump 표기 | W | 10 | COW 5 · MET 2 · BUMP·PROD·THERM 각 1 | micro-bump / Microbump / 마이크로(범프) → µbump |
| 용어 충돌: Erosion | E | 2 | TSV 1 · FEOL 1 | Bosch 측벽 식각을 “Erosion” — CMP Erosion 과 충돌 |
| **합계** | **E** | **199** | | (TCB·HCB 중복 문항 2개 제외 시 고유 197) |
| | **W** | **251** | | f_therm 단수 미기재 311(THERM 노트) 은 별도 |

- 단위 표기(µ/μ, um)는 위반 0건: 전 문항 U+00B5, “um” 단위 없음.
- MR-MUF·TC-NCF 표기는 변형(MR MUF, TCNCF 등) 0건 — 문제는 TCB 대용과 HCB 쪽뿐.

## 3. 교차 중복 · 근중복

- 방법: ① `validate.py --codes W_NEAR_DUP_X`(5-gram ≥ 0.80) → 3쌍(WARP-B-0147↔MIX-B-0017, COW-A-0160↔BUMP-A-0147, MIX-I-0013↔MET-B-0058) + `E_DUP_EXACT` 1쌍(PROD-B-0061↔SIP-I-0130). ② 핵심 텍스트+보기의 char 4-gram Jaccard(숫자 정규화) 0.35 이상 143쌍 전수 판독. ③ 주제 키워드 군집(ESD, KGD, 연삭, 공법 명칭, thermal TSV 등) 판독.
- 결과: **개념 중복 군 70개(교차분야 69개), 교차 분야 문항 쌍 123개** 를 판정했다. 동형 템플릿 우연 일치(예: “A 와 B 를 가르는 결정적 단서는” 틀만 같은 문항)는 중복이 아니라고 판정해 제외.
- 보유 원칙(“그 개념이 어느 분야 학습 목표의 핵심인가”): 접합 공정·NCF·MUF·HCB → COW · 연삭/stress relief/몰드 연삭 → BSP · 신뢰성 시험 규격·가속 시험·ESD·고장 감별 → FA · KGD/시험 흐름·wafer map·SPC → MET · 단수·높이 예산·die 구성 → PROD · 열 경로 판단 → THERM · warpage 거동 → WARP · µbump EM → BUMP · refresh·온도 센서 → DRAM · 인터포저 → SIP · dicing → SAW · 일반론(판단 태도)은 MIX 1개 이하(사례형 재작성 조건).

| # | 개념 | 보유 | 삭제·이관 측 |
|---|---|---|---|
| 1 | HBM 구조 발전 방향 요약 (완전 동일 문항) | PROD-B-0061 (PROD) | SIP-I-0130(SIP) 삭제 |
| 2 | 경화 온도·수지 점도·filler 함량 높/낮 짝짓기 (보기 구조 동일) | WARP-B-0147 (WARP) | MIX-B-0017(MIX) 삭제 |
| 3 | 미세 피치에서 solder 접합 공정 창이 좁아지는 인자 | COW-A-0160 (COW) | BUMP-A-0147(BUMP) 삭제, BUMP-A-0150(BUMP) 삭제 |
| 4 | 공정 조건 불변인데 결과가 서서히 변함 → 마모·축적 | MET-I-0119 (MET) | MET-B-0058(MET) MET 내 통합(삭제), MIX-I-0013(MIX) 삭제, MIX-I-0009(MIX) 삭제 |
| 5 | NCF 필름 두께 편차 → 배출량 편차 | BUMP-I-0134 (BUMP) — mv → COW | WARP-I-0275(WARP) 삭제 |
| 6 | 적층 후 die 교체 불가 이유 | PROD-B-0051 (PROD) | MET-B-0023(MET) 삭제 |
| 7 | 시험 온도를 실사용보다 높이는 이유 / 지나치게 높이면 안 되는 이유 | FA-I-0064 (FA) | WARP-I-0298(THERM) 삭제, WARP-I-0299(THERM) 삭제(FA-I-0065 보유) |
| 8 | 고단 적층에서 구조·공정·시스템이 한 문제로 수렴 | MIX-A-0051 (MIX) | DRAM-A-0074(DRAM) 삭제, PROD-A-0023(PROD) 삭제 |
| 9 | 낱개(개별화) 후 최종 검사를 다시 하는 이유 | MET-B-0074 (MET) | SAW-I-0044(SAW) 삭제 |
| 10 | wafer 단위 작업이 유지되는 마지막 공정 | PROD-B-0050 (PROD) | SIP-I-0129(SIP) 삭제 |
| 11 | 접합층 두께 축소의 이유(높이·열) | PROD-I-0036 (PROD) | SIP-I-0131(SIP) 삭제, WARP-B-0102(WARP) 삭제, FA-I-0043(FA) 삭제, WARP-B-0081(THERM) THERM 보유(열 관점 1개) |
| 12 | 스택 구성 수(die·간극·pad 보유 die) 환산 가족 | SIP-A-0003 (SIP) — mv → PROD (대표 1개) | SIP-A-0004(SIP) 삭제, SIP-A-0005(SIP) 삭제, SIP-A-0006(SIP) 삭제, SIP-A-0007(SIP) 삭제, SIP-A-0008(SIP) 삭제, SIP-A-0009(SIP) 삭제, SIP-A-0010(SIP) 삭제, SIP-A-0011(SIP) 삭제, SIP-A-0012(SIP) 삭제, WARP-A-0002(THERM) 삭제 |
| 13 | 구조·공법 변경 시 검사 체계도 바꿔야 하는 이유(일반론) | COW-A-0078 (COW) | SIP-B-0148(SIP) 삭제, SIP-A-0160(SIP) 삭제, MIX-B-0006(MIX) MIX 내 1개로 통합, MIX-A-0049(MIX) MIX 내 1개로 통합, MIX-A-0039(MIX) MIX 내 1개로 통합, COW-I-0229(COW) 삭제, SAW-I-0041(SAW) 재작성(구체화) 또는 삭제 |
| 14 | EM 자기 가속 되먹임을 끊는 접근 | FA-A-0037 (FA) | MIX-A-0001(MIX) 삭제, MIX-A-0042(MIX) 삭제 |
| 15 | 일괄(gang) 접합 방식의 과제 | COW-I-0167 (COW) | SIP-B-0094(SIP) 삭제 |
| 16 | 인터포저 면적↑ → 수율↓ | SIP-B-0150 (SIP) | SIP-B-0086(SIP) SIP 내 통합(삭제), MET-I-0105(MET) 삭제 |
| 17 | ESD 손상 vs 통전(EM) 열화 감별 | DRAM-A-0061 (DRAM) — mv → FA (재작성) | DRAM-I-0149(DRAM) 삭제, BUMP-A-0164(BUMP) 삭제 |
| 18 | 적층 단마다 정렬 마크 재인식 | COW-B-0057 (COW) | SIP-B-0091(SIP) 삭제 |
| 19 | dicing 방식 이름 고르기 | SAW-B-0037 (SAW) | FEOL-B-0044(FEOL) 삭제 |
| 20 | 상온 warpage 규격 내인데 실장 불량 → 승온 궤적 / 상온 값 하나로 관리하는 한계 | WARP-A-0190 (WARP) | SIP-A-0144(SIP) BGA·interposer 데이터(f_plot)로 재작성 또는 삭제, PROD-A-0027(PROD) 삭제, SIP-A-0148(SIP) 삭제(WARP-A-0191 승온/냉각 이력과 중복) |
| 21 | 조건 변경 후 관찰 기간이 필요한 이유 | MET-A-0108 (MET) | MIX-I-0065(MIX) 삭제 |
| 22 | 절단 전 wafer 상태 검사의 이점(KGD) | MET 분야 | SAW-I-0006(SAW) SAW 1개만 보유(절단 손상 관점으로), SAW-I-0008(SAW) 삭제, SAW-B-0060(SAW) 삭제, PROD-B-0084(PROD) 삭제, PROD-B-0090(PROD) 삭제 |
| 23 | 새 접합 방식을 단계적으로 도입하는 이유 | COW-A-0181 (COW) | COW-I-0178(COW) COW 내 통합(삭제), WARP-A-0217(THERM) 삭제 |
| 24 | 최고온 die 가 refresh 정책을 결정 | DRAM-A-0056 (DRAM) | FA-A-0040(FA) 삭제 |
| 25 | 신뢰성 시험 규격 번호 고르기 | FA-B-0092 (FA) | PROD-B-0115(PROD) 삭제, PROD-B-0116(PROD) 삭제, PROD-B-0117(PROD) 삭제, PROD-B-0118(PROD) 삭제 |
| 26 | Open 이 여러 원인에서 수렴 | FA-I-0027 (FA) | MIX-A-0002(MIX) 삭제 |
| 27 | 적층 후 물리적 수리 불가 → 선별 앞단 배치 | PROD-I-0033 (PROD) | SIP-B-0100(SIP) 삭제 |
| 28 | 조립 지표와 신뢰성 지표를 함께 봐야 하는 이유 | FA-I-0081 (FA) | MET-I-0171(MET) 삭제 |
| 29 | 접합 직전 대기(queue) 시간 관리 | COW-I-0180 (COW) | BSP-B-0106(BSP) 삭제, BUMP-B-0028(BUMP) 삭제 |
| 30 | 불량 위치 패턴(대칭·반복 좌표)으로 원인 계층 판정 | MET-I-0102 (MET) | MET-B-0037(MET) MET 내 통합(삭제), MIX-B-0001(MIX) 삭제, MIX-I-0031(MIX) 삭제, MIX-B-0002(MIX) 삭제, SAW-I-0042(SAW) 재작성(blade·chuck 고유 패턴) 또는 삭제 |
| 31 | 고단에서 접합 방식 전환이 검토되는 이유 | PROD-I-0037 (PROD) | MIX-A-0044(MIX) 삭제 |
| 32 | 절단 측면 미세 crack 이 문제인 이유 | SAW-B-0031 (SAW) | FA-B-0059(FA) 삭제 |
| 33 | 제품 내장 온도 센서의 이유 | DRAM-B-0098 (DRAM) | WARP-B-0125(THERM) 삭제 |
| 34 | TSV 수를 늘려도 방열 효과가 제한적인 이유 | WARP-A-0197 (THERM) | TSV-I-0140(TSV) 삭제, TSV-A-0105(TSV) 삭제 |
| 35 | 작은 단면 = 전류 밀도↑ 로 불리 | BUMP-I-0119 (BUMP) | FA-I-0080(FA) 삭제, FA-I-0062(FA) 삭제, WARP-B-0117(THERM) 삭제, WARP-A-0258(THERM) 삭제 |
| 36 | 통전 중 특정 접점 저항 지속 상승 → crowding 부 void 성장 | BUMP-A-0152 (BUMP) | WARP-A-0259(THERM) 삭제 |
| 37 | TCB 저온·장시간 조정의 부작용 | COW-I-0155 (COW) | MIX-A-0004(MIX) 삭제 |
| 38 | bond head 기울기 vs die warpage 의 불량 맵 분리 | COW-A-0155 (COW) | WARP-A-0184(WARP) 삭제 |
| 39 | 복합 결함 분석 순서(비파괴 → 파괴) | FA-A-0090 (FA) | MIX-A-0036(MIX) 삭제 |
| 40 | 단수↑ → TCB 압착 사이클 누적 | COW-B-0056 (COW) | SIP-B-0090(SIP) 삭제 |
| 41 | 12→16단 확장 시 TC-NCF 제약 조합 | COW-A-0165 (COW) | SIP-A-0143(SIP) 삭제 |
| 42 | Shadow moiré 이름 고르기 | MET-B-0036 (MET) | TSV-B-0097(TSV) 삭제 |
| 43 | chain 저항: 평균 이동 vs 상위 이탈값 해석 | TSV-A-0102 (TSV) | MET-A-0064(MET) 삭제 |
| 44 | 온도 변화에 따른 형상 측정이 필요한 이유 | MET-B-0057 (MET) | WARP-I-0316(THERM) 삭제 |
| 45 | 가장 흔한 판단 실패(한 지표만 봄) — 일반론 | MIX-A-0052 (MIX) | MIX-A-0089(MIX) MIX 내 통합(삭제), FEOL-A-0015(FEOL) 삭제 |
| 46 | 여러 막 응력의 중립면 기준 합성 | WARP-A-0254 (WARP) | FEOL-A-0029(FEOL) 삭제 |
| 47 | 몰드 wafer 연삭 시 EMC/Si 경계 단차 | BSP-B-0091 (BSP) | WARP-A-0174(WARP) mv → BSP (A 대표), WARP-I-0240(WARP) 삭제, WARP-I-0262(WARP) 삭제, WARP-A-0194(THERM) 삭제, WARP-A-0231(THERM) 삭제 |
| 48 | 차세대 검토에 설계·공정·열을 함께 / 경쟁사 도입만으로 전환 금지 / 학회 수치 적용 전제 | MIX-A-0100 (MIX) | PROD-A-0053(PROD) 삭제, PROD-A-0036(PROD) 삭제, PROD-A-0037(PROD) 삭제, MIX-A-0050(MIX) MIX 내 통합, MIX-A-0091(MIX) MIX 내 통합, MIX-A-0057(MIX) MIX 내 통합 |
| 49 | 미세 피치 capillary underfill 충전 난이도 | COW-B-0050 (COW) | COW-I-0188(COW) mv → SIP (SiP 단계 underfill), SIP-I-0134(SIP) 삭제(이관 문항으로 대체) |
| 50 | HCB 에서 CMP 요구가 극단적으로 높은 이유 | COW-I-0237 (COW) | COW-A-0158(COW) COW 내 통합, TSV-A-0136(TSV) 삭제, TSV-A-0124(TSV) 삭제 |
| 51 | warpage 가 있는 die 에 하중만 올린 결과 | COW-I-0141 (COW) | BUMP-A-0146(BUMP) 삭제, WARP-A-0185(WARP) 삭제 |
| 52 | NCF 유동 온도와 solder 용융 구간 불일치 | COW-I-0161 (COW) | BUMP-I-0135(BUMP) 삭제 |
| 53 | fillet 형상 관리 이유 | COW-I-0165 (COW) | BUMP-B-0064(BUMP) 삭제 |
| 54 | 방열 개선이 성능·수명 모두에 이로운 이유 | WARP-B-0127 (THERM) | FA-I-0034(FA) Arrhenius 가속계수 정량 문항으로 재작성 또는 삭제 |
| 55 | core wafer 를 잘라 base wafer 에 올리는 이유(KGD) | PROD-B-0049 (PROD) | SIP-B-0098(SIP) 삭제 |
| 56 | 몰딩·연삭을 절단보다 먼저 하는 이유 | SAW-B-0036 (SAW) | PROD-B-0088(PROD) 삭제, WARP-B-0145(WARP) 삭제 |
| 57 | 연삭 후 stress relief 생략 + 박화 → 취급 crack | TSV-A-0123 (TSV) — mv → BSP | TSV-I-0161(TSV) mv → BSP 또는 삭제, SIP-A-0142(SIP) 삭제 |
| 58 | Bosch 보호 단계↑ → 측면 식각↓·속도↓ | TSV-I-0194 (TSV) | FEOL-I-0013(FEOL) 삭제 |
| 59 | 압착 온도↑ → 초기 강도↑ · TC 수명↓ | COW-A-0153 (COW) | MET-A-0070(MET) 삭제, FA-A-0031(FA) 삭제 |
| 60 | 온도↑ → refresh 주기↓ | DRAM-B-0094 (DRAM) | MET-B-0028(MET) 삭제 |
| 61 | 진공 몰딩 이유 | WARP-B-0068 (WARP) | MET-B-0049(MET) 삭제 |
| 62 | 두 공법을 모두 보유하는 이유 | COW-A-0192 (COW) | MIX-A-0102(MIX) 삭제 |
| 63 | 앞 공정 관리가 강조되는 이유(산포 전파) — 일반론 | MET-B-0078 (MET) | MET-I-0155(MET) MET 내 통합(삭제), PROD-I-0035(PROD) 삭제 |
| 64 | 스택 수직 열 경로의 병목(접합층) | WARP-A-0196 (THERM) | WARP-A-0177(WARP) 삭제(05 WARP 파일에 남은 열 문항) |
| 65 | IR 이 Si 를 투과해 내부 관찰 | MET-B-0066 (MET) | FA-I-0077(FA) 삭제 또는 backside LIT/IR-OBIRCH 판단으로 재작성 |
| 66 | HCB 의 pitch 축소(“18 µm”) | COW-A-0073 (COW) | BUMP-B-0080(BUMP) 삭제 |
| 67 | 강성↑ → 형상↓·접합부 crack↑ 상충 | WARP-I-0238 (WARP) | FA-A-0049(FA) 삭제 |
| 68 | warped wafer 를 흡착 연삭 후 해제 → 두께 편차 | WARP-A-0204 (WARP) — mv → BSP (대표) | WARP-A-0173(WARP) 삭제, WARP-A-0192(WARP) 삭제, WARP-I-0263(WARP) 삭제 |
| 69 | 공법 명칭 고르기(TCB/MR-MUF/HCB) | COW 분야 | BUMP-B-0061(BUMP) 삭제, BUMP-B-0062(BUMP) 삭제, BUMP-B-0029(BUMP) 삭제 |
| 70 | ESD 일반(정의·대책·잠재 손상·시험 모델) 15문항 | FA 분야 | DRAM-B-0141(DRAM) mv → FA, DRAM-I-0143(DRAM) mv → FA, DRAM-I-0148(DRAM) mv → FA, DRAM-A-0060(DRAM) mv → FA, DRAM-B-0142(DRAM) 삭제, DRAM-B-0146(DRAM) 삭제, DRAM-B-0147(DRAM) 삭제, DRAM-B-0148(DRAM) 삭제, DRAM-B-0150(DRAM) 삭제, DRAM-I-0142(DRAM) 삭제, DRAM-I-0147(DRAM) 삭제, DRAM-A-0064(DRAM) 삭제, DRAM-A-0065(DRAM) 삭제 |

- 집계(보유 측 제외 문항): 삭제 123 · mv 12 · 재작성/분야 내 통합 19.

## 4. 오분류 이관 제안 (중복과 무관)

- **40건** (+ 중복 판정 안에서의 mv 12건 = 총 52건).

| id | 현재 | → | 이유 |
|---|---|---|---|
| WARP-I-0244 | WARP | BSP | Post-fab wafer warpage 원인 후보(glue 경화·뒷면 절연막) — 뒷면 공정 관리 목표 |
| WARP-A-0182 | WARP | BSP | 뒷면 공정 후 warpage → pad 노광 위치 이탈 — BSP 의 pad 형성 학습 목표 |
| WARP-A-0218 | WARP | COW | HCB 청정도·평탄도 요구 — HCB 는 COW |
| WARP-A-0235 | WARP | COW | pad 산화 + NCF 유동 지연 → 결함 조합 — TC-NCF 접합 불량 판정 |
| WARP-B-0138 | WARP | COW | 낱개 단위 접합의 과제 — 적층 공법 |
| WARP-A-0256 | WARP | MET | XRD 로 박막 잔류 응력 측정 원리 — 계측 기법 |
| WARP-A-0243 | WARP | FA | EMC 계면 delamination 조기 검출 전략(SAT) — 고장분석 |
| WARP-I-0320 | WARP | THERM | TIM 두께 편차·lid 평탄도·스택 높이 산포 → 특정 스택 고온 — 분할 때 05 에 남은 열 문항 |
| WARP-A-0246 | WARP | THERM | 상면 높이 산포·TIM 압축·lid 평탄도 → 국부 열저항 — 분할 때 05 에 남은 열 문항(WARP-I-0320 과 중복이므로 THERM 에서 1개로) |
| WARP-I-0284 | THERM | WARP | 냉각 속도 → 강도·잔류 응력 — 열 설계가 아니라 기계 물성(13 THERM → 05 WARP) |
| WARP-I-0321 | THERM | WARP | 몰딩 수축 편차 → 형상 → 실장 불량 — 기계(13 THERM → 05 WARP) |
| WARP-I-0283 | THERM | BSP | 연삭 냉각수 공급 이유 — 연삭 공정(13 THERM → BSP) |
| WARP-B-0121 | THERM | FA | 결함 부위의 자기 가속 열화 구조 — 신뢰성 일반(13 THERM → FA). FA 에 동형이 있으면 삭제 |
| BUMP-I-0156 | BUMP | COW | NCF filler 입경 → 미접합 경로 — NCF 재료/공정 |
| BUMP-I-0158 | BUMP | COW | 압착 하중↑ 의 새 문제 — TCB 공정 조건 |
| BUMP-A-0145 | BUMP | COW | height offset + bond force 상향의 한계 — TCB 공정 조건 |
| TSV-A-0155 | TSV | COW | underfill void 위치 예측 — 적층 충전 |
| SIP-B-0165 | SIP | COW | MR-MUF 에서 단수↑ 시 어려워지는 것 — 적층 공법 |
| SIP-A-0187 | SIP | COW | 저단·후막 die 조건의 두 공법 우열 — 적층 공법 비교 |
| SIP-A-0075 | SIP | COW | HCB CMP 목표(거칠기·dishing) — HCB 접합면 |
| SIP-B-0069 | SIP | PROD | 8-Hi 24 GB 와 12-Hi 36 GB 의 동일 대역폭 — 제품 구성 |
| SIP-I-0158 | SIP | MET | SiP 전 HBM 최종 검사 강화 근거 — 시험 흐름 |
| FA-A-0058 | FA | DRAM | 정정 가능 오류(ECC) 증가 추세 대응 — DRAM ECC (FA 브리프 지목) |
| FA-A-0032 | FA | BSP | 뒷면 절연막 저온화 vs glue 열 한계 — BSP (FA 브리프 지목) |
| FA-A-0024 | FA | THERM | HBM cube height 와 SoC 높이 정합 → 접촉 열저항 편차 — 열 설계 (FA 브리프 지목) |
| DRAM-I-0165 | DRAM | PROD | HBM4 I/O 2배의 조립 측 부담 — 제품 구조/세대 비교 |
| PROD-A-0016 | PROD | WARP | 극박 mid core 16-Hi 의 stack warpage 지배 요소 — 기계 |
| PROD-A-0033 | PROD | MET | 스택 간격이 좁을 때 결함 검사 난이도 — 검사 |
| MET-B-0050 | MET | SAW | dicing 냉각수 공급 이유 — 절단 장비 |
| MET-I-0116 | MET | SAW | dicing 이송 속도↑ 결과 — 절단 조건 |
| MET-B-0033 | MET | FA | FIB 로 원하는 지점 단면 가공 — 고장분석 기법 |
| FEOL-A-0003 | FEOL | BSP | reveal 식각 선택비 저하 → Cu 돌출 산포 → 접합 불량 분포 (FEOL 브리프 지목) |
| FEOL-A-0010 | FEOL | FA | 흡습 후 급속 가열 계면 박리(popcorn) — MSL/preconditioning (FEOL 브리프 지목) |
| FEOL-B-0047 | FEOL | FA | 뒷면 광 방출에 InGaAs 검출기 — FA 기법 (FEOL 브리프 지목) |
| FEOL-A-0018 | FEOL | SIP | 전원망 재분배 상충 — PDN (SIP 공백 주제, FEOL 브리프 지목) |
| FEOL-B-0042 | FEOL | SIP | 용량이 다른 decap 병용 이유 — PDN (SIP 공백 주제) |
| FEOL-B-0035 | FEOL | SIP | 신호선 끝 반사 — SI (SIP 공백 주제) |
| FEOL-I-0009 | FEOL | MET | probe 접촉 압력 — 시험 (FEOL 브리프 지목) |
| FEOL-B-0012 | FEOL | MET | wafer 상태 칩 양불 판정(EDS/KGD) — 시험 |
| FEOL-A-0019 | FEOL | COW | 극박 core die + 액상 충전 복합 현상 — MR-MUF. FEOL-A-0037 은 동일 문항이므로 삭제 |

- WARP 분할 경계 정리: 05 에 남은 열 문항(WARP-I-0320, WARP-A-0246 → THERM, WARP-A-0177 은 THERM 의 WARP-A-0196 과 중복이라 삭제), 13 으로 간 비열 문항(WARP-I-0284·I-0321 → WARP, WARP-I-0283 → BSP, WARP-B-0121 → FA, 그리고 중복 삭제 대상 WARP-A-0194·A-0231·A-0217·I-0298·I-0299·I-0316·B-0117·A-0258·A-0259·B-0125·A-0002). 분할 스크립트(`_w05_split_moved_ids.json`)의 기준을 EA 가 확인해 주길.

## 5. 분야 간 사실 충돌

| # | 충돌 | 관련 분야 | 무엇이 다른가 | 판정·처리 |
|---|---|---|---|---|
| F1 | Smile/Cry 정의가 반대 | WARP, COW, BUMP, TSV | f_warp 현행 표와 WARP-I 가족은 “bump 면 아래 + 중앙이 기준면에서 멂 = Smile”(active 면 기준), COW-I-0141·BUMP-A-0146/0150 해설은 같은 형상을 “Cry” 라 부른다. STANDARDS 2.5(위에서 본 형상: ∩ = Cry, ∪ = Smile)는 **COW·BUMP 쪽과 일치**하고 f_warp 표·WARP-I 가족이 틀렸다. bump 면 아래 자세 12문항은 정답 키가 반대. | WARP: 정답 키 교정 + 가족 3개로 축소(§1). DA: EA_to_DA §1 표 교체 전까지 f_warp 명명표를 근거로 쓰지 않음. TSV: f_warp 사용 54문항 그림 교체. |
| F2 | N단의 간극 수가 분야마다 다름 | THERM, MET, SIP | THERM 열저항 가족은 “12단 → 간극은 die 수보다 하나 적은 11개” 로 계산하고 f_therm.n 에 core 수를 넣어(그림이 base 를 빼고 n−1 간극으로 계산) 결과를 맞춘다. SIP 는 “core n 장이면 간극 n 개”, MET-I-0001 은 “접합 간극 11곳”. STANDARDS 2.5: N단 → 간극 N. | THERM: 간극 N 으로 재계산·f_therm.n=N+1(최하단 core 까지를 묻는 경우만 N−1 을 명시). MET-I-0001: 0.995¹² 로 재계산(≈ 74 %). DA: f_therm 고정 pill “간극 수는 die 수보다 하나 적다” → “간극 수 = core die 수” (EA_to_DA §7). |
| F3 | HCB 의 pitch·bump 표현 | BUMP, COW, BUMP | BUMP-B-0080·COW-A-0073 은 HCB 를 “bump pitch 18 µm 이하/미만” 으로 서술(업체 보도 [R]). STANDARDS 2.4 는 HCB pad pitch ≤ 10 µm·bump 간극 없음, COW-I-0245 는 “D2W HCB 2 µm 급 시연”. 한편 BUMP-A-0002·A-0033~0042 는 solder µbump 를 pitch 6–20 µm 로 설정(2.4 의 µbump 25–55 µm 밖, HCB 영역과 겹침). | COW: “18 µm” 는 [V] 출처 확인 전 정답 근거 금지(FACT) — 쓰더라도 “접합 pitch(pad pitch)” 로. BUMP: B-0080 삭제, A-0033~0042 의 pitch 는 µbump 현실 범위로 바꾸거나 “가정” 명시(NUM 과 함께). |
| F4 | preconditioning 규격 번호 | FA, PROD | FA-B-0002·B-0043~0046·A-0033 은 “preconditioning = J-STD-020”, FA-B-0094 는 “preconditioning = JESD22-A113”. STANDARDS 2.3: 절차는 JESD22-A113, J-STD-020 은 MSL 분류·리플로 프로파일. | FA: “JESD22-A113 (J-STD-020 프로파일)” 로 통일. f_rel 기본 seq 첫 행도 같은 문제(EA_to_DA §8). |
| F5 | MR-MUF 의 가압 여부 / Advanced MR-MUF 의 개량점 | COW, BUMP, WARP | COW-I-0021·BUMP-I-0159 는 MR-MUF 를 “die 마다 가압하지 않는 일괄 reflow(층별 하중 제약 없음)” 로, COW-B-0095/B-0114/I-0214/A-0189·WARP-A-0269/0276 은 Advanced MR-MUF 를 “압착(적층) 하중을 낮춘 개량형” 으로 정의한다. 가압이 없다는 방식의 “하중을 낮췄다” 는 서로 맞지 않는다. | FACT 판정 요청: SK hynix [V] 발표 기준으로 Advanced MR-MUF 의 개량점(신규 EMC·칩 휨 제어/가접합 조건 등)을 확정하고, “가접합(pre-bond) 하중” 처럼 무엇의 하중인지 특정. 확정 전에는 COW 가 보유하고 WARP 는 WARP-A-0269/0276 중 1개만, 판정 후 표현 통일. |
| F6 | MR-MUF 방열 우위의 근거 | COW, BUMP, THERM | 근거가 “고열전도 충전재(EMC)”(COW-B-0087/B-0106), “간극을 채워 경로가 연속”(COW-I-0215), “thermal dummy bump 를 더 많이 배치”(BUMP-I-0159), “filler 를 쓰기 쉬운 구조”(WARP-I-0055)로 제각각이다. 각자 정답으로 두면 다른 분야 문항에서 오답 근거가 된다. | COW 가 [V] 출처로 근거를 확정(EMC 열전도 + dummy bump 밀도)해 해설에 명시하고, BUMP·THERM 은 같은 표현을 쓴다. |
| F7 | “Erosion” 의 두 가지 뜻 | TSV, FEOL | TSV-B-0076·A-0099 는 Erosion = CMP 에서 조밀 패턴 영역 전체가 낮아짐, TSV-I-0194·FEOL-I-0013 은 Bosch 측벽 식각을 “Erosion” 이라 부른다. | 식각 문항을 “측면 식각(lateral etch)/scallop” 으로 바꿈. |
| F8 | 도금 전류밀도 과다의 결과 | TSV, BUMP | TSV-I-0151 정답 “결정립이 거칠어진다”, BUMP-I-0144 정답 “거칠어지고 편차가 커진다”(표면 거칠기). TSV 브리프는 TSV-B-0106 에 대해 “고전류밀도는 핵생성 증가로 결정립이 미세해지는 경향, 주 문제는 pinch-off/void” 로 판정. | FACT 판정 후 통일: 한계 전류밀도 초과 시 “표면 거칠어짐(수지상·burnt)”과 “결정립 크기” 를 구분해 서술. |
| F9 | HBM4 12단 용량 | PROD | 정답 “HBM3E 12단과 36 GB 로 동일”. STANDARDS 2.2: HBM4 는 24 Gb·32 Gb die → 12-Hi 36 GB 또는 48 GB. “동일” 은 유일 정답이 아니다(DRAM·PROD 용량 계산 문항의 32 Gb die 설정과도 충돌 가능). | die 밀도를 지문에 주고 계산형으로 바꾸거나, “24 Gb die 기준” 을 명시. |

## 6. 다른 에이전트에 넘길 사항

- **DA**: ① f_warp 명명표 교체(EA_to_DA §1) — F1 의 근원. 교체 전에는 WARP·TSV 가 표를 근거로 쓰지 못한다. ② f_therm 고정 pill “간극 수는 die 수보다 하나 적다” 와 n(=base 포함) 의미 — F2 의 근원(§7, `core` param 제안 지지). ③ f_bond hcb 분기의 gap 치수(§5) — COW-B-0003 계열.
- **FACT**: F5(Advanced MR-MUF 개량점·MR-MUF 가압 여부), F6(MR-MUF 방열 근거), F3(“HCB 18 µm” 의 등급), F8(도금 전류밀도와 결정립), F9(HBM4 12단 용량). THERM 의 iHBM/ICE 문항(WARP-B-0150·B-0154·A-0277)은 브리프대로 [V] 확인 전 사용 금지.
- **NUM**: F2 재계산 대상 THERM 48문항(간극 N 으로 바꾸면 정답·오답 값이 모두 바뀜)과 MET-I-0001(정답 “약 72 %” → 0.98¹²×0.995¹² ≈ 73.9 %).
- **EA**: ① 5-gram 0.80 검사기는 교차 중복을 3쌍만 잡는다. 판독으로 확인한 쌍의 실제 유사도는 0.35–0.75 — `W_NEAR_DUP_X` 임계를 낮추거나 char 4-gram 보조 검사를 W3 에 쓰겠다. ② Phase 2 이관 시 같은 개념의 mv 문항이 대상 분야 기존 문항과 다시 중복되지 않는지 W3 에서 재검사.

## 7. 방법과 한계

- 기계 탐색: 정규식(용어·수치), char 4-gram 역색인 Jaccard(교차 분야 쌍만), 분야별 어휘 점수(오분류 후보) → 판독. 스크립트는 scratchpad(`xd/s/`).
- 오분류는 어휘 점수로 후보 354건을 뽑아 판독했고, SIP↔PROD(높이 계산 231건)처럼 소관이 중첩된 군은 개별 이관 대신 §3 보유 원칙으로 처리했다.
- 사실 충돌은 “같은 물리량·정의를 분야마다 다르게 쓰는 경우” 만 다뤘다. 분야 내부의 단독 사실 오류는 FACT·NUM 소관이며 여기서는 충돌에 걸린 것만 적었다.
