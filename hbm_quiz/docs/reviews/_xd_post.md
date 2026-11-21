# XD W3 사후 점검 — 요약 (`_xd_post.md`)

- 작성: XD · 2026-11-21 · 입력: `data/*.json` 14분야 2,448문항(W2 재편집 후), `mv` 59문항 · 기준: STANDARDS 2.5·3.10, FACT §11·§12, EA 감사 W3 항목(`EA_audit/_status.md`)
- 분야별 지시: `docs/reviews/xd3/<CODE>.md` (조치 문항 · 나가는/들어오는 mv 판정 · 보유 목록 · 개념 보강). 읽기 전용으로 수행(data/·template.html·tools/ 미수정). 분석 스크립트·중간 산출물: scratchpad `xd3/`.
- 방법: 용어 정규식 전수(지문·보기·해설·그림·지표) → 판독 / 교차 중복은 char 4-gram Jaccard(≥ 0.11, 221쌍)·가중 3-gram·정답 문자열 일치·주제 키워드 군집으로 후보를 뽑아 전부 판독 / mv 59문항은 도착 분야 전 문항과 유사도 상위 4개를 판독 / 사실 충돌은 물리량별(공법 기구, pitch, Black n·Ea, retention, 곡률, 높이 식, 열저항, overlay, shoreline) 값을 분야 횡단으로 수집 / 개념 손실은 원본 5,000문항(`scratchpad/w2/*/orig*.json`) 대비 용어·체크리스트 전역 커버리지와 W1 보유 판정 추적.

## 1. 한눈에

| 분야 | 조치 문항 | 나가는 mv | 들어오는 mv | 보유(상대 삭제) |
|---|---|---|---|---|
| [TSV](xd3/TSV.md) | 0 | 5 | 0 | 9 |
| [BSP](xd3/BSP.md) | 8 | 0 | 11 | 3 |
| [BUMP](xd3/BUMP.md) | 7 | 4 | 0 | 7 |
| [SAW](xd3/SAW.md) | 2 | 0 | 2 | 1 |
| [COW](xd3/COW.md) | 14 | 2 | 11 | 13 |
| [WARP](xd3/WARP.md) | 1 | 12 | 3 | 5 |
| [SIP](xd3/SIP.md) | 11 | 5 | 5 | 0 |
| [FA](xd3/FA.md) | 14 | 3 | 14 | 1 |
| [PROD](xd3/PROD.md) | 8 | 2 | 3 | 16 |
| [DRAM](xd3/DRAM.md) | 6 | 6 | 1 | 2 |
| [MET](xd3/MET.md) | 7 | 3 | 5 | 9 |
| [MIX](xd3/MIX.md) | 8 | 0 | 0 | 2 |
| [FEOL](xd3/FEOL.md) | 13 | 9 | 0 | 1 |
| [THERM](xd3/THERM.md) | 15 | 8 | 4 | 6 |

## 2. 용어 규약 재검사 (신규 9xxx 포함 전수)

| 규약 | 결과 | 문항 |
|---|---|---|
| N단 ↔ 간극 N(base 포함), "die 수보다 하나 적다" | **0건** | W1 의 THERM 48·MET 1·SIP 71 은 모두 해소. 오답 해설의 "간극을 N−1 로 센 값" 은 오개념 설명이라 정상. f_stack/f_therm 의 n·core 와 지문 N단 불일치 0 |
| Smile/Cry(위에서 본 형상, ∩ = Cry) | **0건** | 명명 문항 27개 판독 — 자세·정답·해설 모두 규약 일치. 그림 노출 W 1: MET-B-9014(f_warp 이름 표시, 중복 삭제 대상) |
| front-to-back | **E 2** | FA-B-0109 지문 · FA-I-0109 해설: "core die 앞면이 µbump·위 die 로 덮여" — 앞면은 아래를 향함. TSV·BSP·BUMP·COW·PROD·SIP 는 위반 0(TSV-B-0078·BSP-B-0082·COW-B-0053·PROD-I-9043·A-9043·SIP-B-9001 정상, 최상단 core 에 TSV/backside pad 를 두는 서술 0) |
| 공법명(HCB/TC-NCF/MR-MUF, µbump) | **W 7** | "하이브리드 본딩": SIP-I-9030·B-9010·B-0136, BUMP-I-9020 / "TC 본딩" 을 공법명으로: COW-B-0117·A-9023, THERM-A-9036(THERM-I-9032 는 중복 삭제). TCB 공법명 0, micro-bump·μ(그리스 문자) 0(지표의 μ 는 평균 기호) |
| 775 µm 를 JEDEC 규격으로 | **0건** | 33문항 모두 "높이 상한(설계 조건)" 표기 |
| TC 1000 cycle 을 JEDEC 요구로 | **0건** | 1,000 cycle 은 사내·고객 기준 또는 실험 조건으로만 사용. JESD47 condition B 700 / G 850 / J 2,300 일치. template 의 f_rel 기본값도 700 으로 고쳐짐 |
| J-STD-020 ↔ JESD22-A113 | **0건** | preconditioning = A113, MSL 분류·프로파일 = J-STD-020 으로 통일 |
| ECS 를 HBM3 에 | **0건** | ECS 는 DRAM-B-0080 오답(일반 기능 설명)뿐, HBM3 귀속 없음 |
| refresh 판정 die(EA 항목 5) | **12건** | base die 온도로 정상/확장 구간 판정: THERM WARP-A-0003·A-0004·A-0033·A-0208, THERM-A-9004·A-9017·A-9021·A-9024·A-9032, SIP-A-9012·A-9038, (불명확) DRAM-A-9044 → 최하단 core die 로 재계산 |
| (참고) 그림 기본값의 정답 노출 | 4건 | FA-B-0027·B-0035·B-0094·B-0096 — f_rel 에 seq 가 없어 기본 seq 가 정답 문서/시험명을 그림 |

- 합계: **E 2 · W 7(+그림 1) · 규약 통일 12 · 그림 노출 4**. W1 의 E 199 · W 251 은 모두 해소되었습니다.

## 3. 교차 중복 · 근중복

- 5-gram 검사기(`W_NEAR_DUP_X`)에는 0쌍, 4-gram Jaccard 최고 0.27 — W2 재작성으로 문장 수준 중복은 사라졌고 **남은 것은 모두 개념 중복**(같은 판단·같은 식·같은 정답)입니다.
- 판정 **73쌍**(+ EA 항목 1 입자 Poisson 2건, 분야 내부 2건): 상대 쪽 **삭제 65 · 재작성/묻는 지점 변경 8**. 보유 원칙은 W1 과 같음(세대 사양·스택 구성·높이 → PROD, 접합 공정 → COW, 계측 장비·KGD → MET, 기계 응력 → WARP, 열 경로 → THERM, IMC·µbump EM → BUMP, TSV·KOZ → TSV, 신뢰성 모형 → FA). MIX 사례 세트 문항은 세트를 깨지 않도록 "묻는 지점 변경" 을 우선했습니다.

| 군 | 보유 | 삭제(또는 재작성*) |
|---|---|---|
| 용량 24 Gb×12=36 GB | PROD-B-0103 | DRAM-B-9011 |
| Samsung HCB 열저항 20 % | COW-B-0117 | THERM-I-9032 |
| via-middle 이름 / liner 표 / liner 저온 이유 | TSV-B-0061 · A-9020 · B-9004 | FEOL-B-9010 · A-9027 · I-9020 |
| KOZ(EA 항목 2) | TSV-A-9029 · A-9041 · A-9007 · B-0060 | FEOL-A-9001 · A-0028 · A-9037* · B-9011 |
| erosion 명칭 / Cu pumping 명칭 | TSV-B-0076 · B-9006 | FEOL-B-9006 · B-0068 |
| Cry 명칭 | WARP-B-9006 | MET-B-9014 |
| TTV 정의 / TTV 계산 | MET-B-9002 · BSP-B-9001 | BSP-B-0097 · MET-I-9008 |
| 굽힘 강성 1/8 / Stoney 곡률 배율 | WARP-B-9011 · I-0260 | BSP-I-0088 · COW-I-9007 (WARP-A-0276* 내부) |
| MR-MUF 방열 근거 / dummy bump 를 더 두는 이유 | COW-B-0106 · I-0215 | THERM WARP-I-0311 · BUMP-I-0159 |
| formic acid 이점 | COW-I-0181 | BUMP-I-0109 |
| KGD 정의 / HCB probe pad / test escape / base wafer map | MET-B-0032 · I-9037 · A-0008 · I-9001 | BSP-B-9021 · I-9042 · COW-A-9024 · PROD-A-9036 |
| Cu recess 결함 짝 | COW-I-0148 | MIX-B-0016 |
| Kirkendall 기구 | BUMP-I-0001 | FA-I-0038 |
| top core 에 backside pad 없음 | PROD-B-0031 | PROD-B-0032 · BSP-B-0104 · COW-B-0053* |
| N단 계면 수 / pad 보유 die 수 | THERM-B-9002 · SIP-B-9001(→PROD) | COW-B-9003 · PROD-I-9021 |
| shadow moiré / SAM 이름 / SAM 물 / SAM 깊이 | MET-B-0036 · B-0065 · B-9018 · I-9024 | SIP-B-9008 · COW-B-9007 · FA-B-0051 · FA-I-9044* |
| underfill 피로 수명 기구 | WARP-I-9011 | COW-I-9003 · FA-I-0047 |
| seal ring chipping 누설 | SAW-I-9031 | FEOL-I-9028* |
| HCB 입자 하나의 미접합 범위 | COW-B-0065 | SAW-B-9016* |
| HCB 입자 Poisson 예산(EA 항목 1) | COW-A-9001 · MIX-A-9015 | SAW-A-9004* · MET-A-9007* |
| AuSn₄ 취화 | BUMP-I-9022 | BSP-I-9037 |
| step coverage | FEOL-B-0029 | BSP-B-9029 |
| base die 로직 공정 이유 | PROD-B-0037 | FEOL-I-9027 |
| thermal dummy bump 역할 / 병렬 k_eff / 최다 열 통과 계면 | THERM-B-9009 · I-9009 · I-9023 | BUMP-B-9010 · COW-I-9016 · COW-I-9025 |
| refresh 점유율 / 온도↑ refresh 절반 | DRAM-I-9007 · B-0094 | THERM-I-9014 · FEOL-I-9037 |
| EM: Ea 추출 / n 추출 / Black 외삽 / Black 변수 | BUMP-A-9003 · A-9002 · A-9001 · FA-B-9006 | FEOL-A-9041 · FA-A-9013 · MIX-A-9062 · BUMP-B-9006 |
| 스택 수율 곱(계면 / die / W2W) | PROD-I-9032 · I-0033 · COW-A-0187 | MIX-B-9004 · BSP-I-9052 · DRAM-I-9024 · MET-I-0138 |
| 높이 예산(두께 상한 / HCB 여유 / 높이 계산 / 편차 누적) | PROD-I-9005 · I-0037 · I-9019 · BSP-I-0064 | SIP-I-0063 · MIX-I-9001* · MIX-I-0069 · COW-A-0072* · SIP-I-0104 · MET-I-0106 |
| dummy bump 확대 ΔT | MIX-A-9036 | PROD-A-9016 |
| 가장 뜨거운 die | THERM WARP-I-0056 | MIX-B-9012 · PROD-B-9011 |
| 연삭 목표 두께(TSV+TTV) | BSP-I-9013 | MET-A-9012 |
| µbump pitch 자릿수 / pitch² 접점 밀도 | BUMP-B-9003 · COW-I-9001 | PROD-B-0110 · SIP-I-9030 |
| 스택 수 ↔ 대역폭 | PROD-I-9009 | MIX-I-9010* |
| HBM3·HBM4 채널/PC 구성 | PROD-B-9001 · I-9011 | DRAM-B-0029 · I-0035 |
| 하부 joint 누적 열이력 / IMC √t | COW-B-0058 · A-0164 · BUMP-A-9014 | BUMP-I-0138 · A-0158 · COW-A-9018 |
| 접합 온도↑ → 강도↑ 수명↓ | COW-A-0153 | FA-A-0126 · FA-I-0055 |

- 허용으로 판정한 근접 쌍(묻는 판단이 다름): COW-B-0095 ↔ PROD-B-0132(Advanced MR-MUF 정의 vs HBM4 적용 사실), COW-A-9023 ↔ THERM-A-9036(발표 분해 vs 시스템 영향), WARP-I-9003 ↔ SIP-I-9013(die–기판 vs C4 DNP), WARP-I-9004 ↔ MIX-I-9018(사례 세트), PROD-A-9011 ↔ MIX-A-9053(Si vs RDL 배선층), SIP-A-9038 ↔ THERM-A-9024, DRAM-A-9013 ↔ THERM-I-9013, COW-A-0044 ↔ MET-I-0130 ↔ MIX-B-9003.

## 4. mv 59문항 판정

- **이관 수용 36 · 이관 후 삭제 23 · 원 분야 유지 0.** 이관 후 삭제는 도착 분야에 같은 판단의 문항이 이미 있는 경우이며, 삭제 사유는 "근중복: 도착 분야 id".

| id | 출발 → 도착 | 판정 | 근거 |
|---|---|---|---|
| BUMP-A-0145 | BUMP → COW | 이관 수용 | 수치 높이 예산형 고급, COW-I-0149·I-0141 과 판단이 다름 |
| BUMP-I-0134 | BUMP → COW | 이관 수용 | COW-I-0151(NCF 두께↑)과 달리 두께 편차 |
| BUMP-I-0156 | BUMP → COW | 이관 수용 | COW-I-0022(대책)와 같은 관측이지만 묻는 것이 경로 — 지문 관측 문장을 다르게 다듬을 것 |
| BUMP-I-0158 | BUMP → COW | 이관 후 삭제 | COW-I-0149 와 중복 |
| COW-B-0080 | COW → SIP | 이관 후 삭제 | SIP-B-0084 와 중복 |
| COW-I-0188 | COW → SIP | 이관 수용 | SiP 단계 capillary underfill — SIP-B-9011(이름)·I-9043(충전 시간)과 판단이 다름(COW-B-0050 과 같은 물리는 단계가 달라 허용) |
| DRAM-A-0060 | DRAM → FA | 이관 수용 | FA 에 ESD 문항 없음 |
| DRAM-A-0061 | DRAM → FA | 이관 수용 | FA 에 ESD 문항 없음 — DRAM-I-0143 과 정답 단서가 겹치지 않게 해설 정리 |
| DRAM-B-0141 | DRAM → FA | 이관 수용 | FA 에 ESD 문항 없음(FA 가 수신 예정이라 미출제) |
| DRAM-I-0143 | DRAM → FA | 이관 수용 | FA 에 ESD 문항 없음 |
| DRAM-I-0148 | DRAM → FA | 이관 수용 | FA 에 ESD 문항 없음 |
| DRAM-I-0165 | DRAM → PROD | 이관 후 삭제 | PROD-A-9028·PROD-I-0003 와 중복 |
| FA-A-0024 | FA → THERM | 이관 후 삭제 | THERM 의 WARP-A-0208(계산형)·WARP-A-0246 와 중복 |
| FA-A-0032 | FA → BSP | 이관 후 삭제 | BSP-A-9029·BSP-B-9013 (일반론 "상충이므로 찾는다" 성격) 와 중복 |
| FA-A-0058 | FA → DRAM | 이관 후 삭제 | DRAM-I-0122·DRAM-B-0115 와 중복 |
| FEOL-A-0003 | FEOL → BSP | 이관 수용 | BSP-I-9040·A-9020 과 다름. EA 감사 W3 항목 4(FEOL-I-0001·A-0001 삭제 개념)를 BSP 에서 이 문항이 담당 — 반드시 이관 |
| FEOL-A-0010 | FEOL → FA | 이관 후 삭제 | FA-I-0082 (FA-I-9014 도 인접) 와 중복 |
| FEOL-A-0018 | FEOL → SIP | 이관 수용 | SIP-I-9044 와 다른 상충 |
| FEOL-A-0019 | FEOL → COW | 이관 후 삭제 | COW-I-0213 와 중복 |
| FEOL-B-0012 | FEOL → MET | 이관 수용 | MET 에 EDS 명칭 문항 없음 |
| FEOL-B-0035 | FEOL → SIP | 이관 수용 | SIP 에 반사 문항 없음 |
| FEOL-B-0042 | FEOL → SIP | 이관 수용 | SIP-B-9006·I-9003 과 다름(용량 병용) |
| FEOL-B-0047 | FEOL → FA | 이관 수용 | FA-B-0109(Si 투과)와 다름(검출기 대역) |
| FEOL-I-0009 | FEOL → MET | 이관 수용 | MET-I-0131 과 원인이 다름 |
| MET-B-0033 | MET → FA | 이관 후 삭제 | FA-B-9010 와 중복 |
| MET-B-0050 | MET → SAW | 이관 후 삭제 | SAW-B-9008 와 중복 |
| MET-I-0116 | MET → SAW | 이관 후 삭제 | SAW-B-0067 와 중복 |
| PROD-A-0016 | PROD → WARP | 이관 수용 | WARP 에 극박 16-Hi stack warpage 지배 요소 문항 없음 |
| PROD-A-0033 | PROD → MET | 이관 수용 | MET-I-9036(2D X-ray 층 구분)과 다름 |
| SIP-B-0069 | SIP → PROD | 이관 수용 | PROD-B-0029(스택 수)와 달리 단수 ↔ 대역폭 |
| SIP-B-0165 | SIP → COW | 이관 수용 | COW-B-0050(간극 축소 원인)과 묻는 것이 다름(단수 증가 결과) |
| SIP-B-9001 | SIP → PROD | 이관 수용 | PROD 의 스택 구성 세기 대표(PROD-I-9021 은 삭제) |
| SIP-I-0158 | SIP → MET | 이관 수용 | MET-B-0069(die 단위 KGD)와 달리 SiP 전 스택 선별 |
| SIP-I-9001 | SIP → COW | 이관 후 삭제 | COW-I-0237 (COW-I-0169 도 인접) 와 중복 |
| WARP-A-0249 | THERM → FA | 이관 후 삭제 | FA-I-0076 와 중복 |
| WARP-A-0260 | THERM → FA | 이관 후 삭제 | FA-I-0003·FA-B-0001 와 중복 |
| WARP-B-0121 | THERM → FA | 이관 수용 | FA-A-0037(정량)과 B/A 짝 |
| WARP-B-0141 | THERM → FA | 이관 후 삭제 | FA-B-0003 와 중복 |
| WARP-B-0142 | THERM → FA | 이관 후 삭제 | FA-I-0075 와 중복 |
| WARP-I-0283 | THERM → BSP | 이관 수용 | BSP 에 연삭 냉각수 문항 없음 |
| WARP-I-0284 | THERM → WARP | 이관 수용 | WARP 에 냉각 속도 → 잔류 응력 문항 없음 |
| WARP-I-0321 | THERM → WARP | 이관 수용 | WARP-B-0094 와 다름(실장 경로) |
| TSV-A-0123 | TSV → BSP | 이관 수용 | BSP-B-0079(목적)·A-9055(휨)와 묻는 판단(crack 원인 분리)이 다름 |
| TSV-A-0155 | TSV → COW | 이관 수용 | COW 의 EMC 유동 문항과 판단이 다름(예측 인자 조합) |
| TSV-B-0096 | TSV → BSP | 이관 후 삭제 | BSP-I-0095 와 중복 |
| TSV-I-0134 | TSV → BSP | 이관 수용 | BSP 에 reveal CMP dishing → pad 접촉 문항 없음 |
| TSV-I-0139 | TSV → BSP | 이관 후 삭제 | BSP-I-9018 (BSP-I-0113 도 같은 계열) 와 중복 |
| WARP-A-0174 | WARP → BSP | 이관 수용 | BSP-B-0091(B)과 같은 정답 문장이지만 관측 2개로 원인 분리하는 고급 — 보기 문구를 B 와 다르게 |
| WARP-A-0182 | WARP → BSP | 이관 수용 | BSP 에 휨 → 뒷면 pad overlay 문항 없음 |
| WARP-A-0204 | WARP → BSP | 이관 수용 | BSP-B-0077·I-9001(접착층 편차)과 원인이 다름 |
| WARP-A-0218 | WARP → COW | 이관 후 삭제 | COW-B-0065 와 중복 |
| WARP-A-0235 | WARP → COW | 이관 수용 | COW-I-0228(공법별 대표 결함)과 다른 복합 조건 |
| WARP-A-0243 | WARP → FA | 이관 후 삭제 | FA-B-0106·FA-A-0090 와 중복 |
| WARP-A-0246 | WARP → THERM | 이관 수용 | THERM 에 높이 산포·lid 평탄도 복합 기구 없음(WARP-A-0208 은 계산형) |
| WARP-A-0256 | WARP → MET | 이관 수용 | MET 에 XRD 응력 측정 없음 |
| WARP-B-0078 | WARP → THERM | 이관 후 삭제 | THERM-B-9003 와 중복 |
| WARP-B-0138 | WARP → COW | 이관 후 삭제 | COW-I-0220 와 중복 |
| WARP-I-0244 | WARP → BSP | 이관 수용 | BSP-I-0107 은 결과, 이 문항은 원인 판정 — 방향이 다름 |
| WARP-I-0320 | WARP → THERM | 이관 후 삭제 | WARP-A-0246(같이 이관, 고급 보유) 와 중복 |

- EA 감사 W3 항목 4: FEOL-I-0001·A-0001 이 지운 개념(reveal 선택비 → 돌출 산포 → 미접합 + short)은 **FEOL-A-0003(→ BSP, 이관 수용)** 이 담당합니다. BSP 기존 문항(BSP-I-9040 낮은 pad non-wet, BSP-A-9020 맵 판단)은 한쪽 결함만 다룹니다 → FEOL-A-0003 은 반드시 이관.

## 5. 분야 간 사실 충돌

| # | 쟁점 | 분야 · 문항 | 무엇이 다른가 | 처리 |
|---|---|---|---|---|
| F1 | MR-MUF 가접합에 가압이 있는가 | COW-I-9024 ↔ WARP-I-9025·I-0245·A-0276, MIX-A-9035, COW-I-0146 | COW-I-9024 는 "짧게 가열·가압해 가접합", 나머지는 "가압 없이 쌓고 일괄 reflow". FACT X-F5: 가접합 하중은 공식 자료에 없음 | COW-I-9024 에서 가압 단정 삭제("짧게 가열해 가접합") |
| F2 | 접합층 면적 열저항의 자릿수(HCB 계면 · µbump 층) | THERM-I-9022(HCB k≈99, ≈0.01 mm²·K/W) · WARP-I-0029(0.2) · WARP-I-0061(1.2, µbump 4.2) · WARP-A-0059(2, TC-NCF 10) · COW-A-9023(접합층 열저항 30 % 잔존 ≈ 5) · WARP-A-0003/THERM-I-9019(µbump 10–17) | 같은 "HCB 계면" 이 문항마다 0.01–5 mm²·K/W(2.5 자릿수), µbump 층도 4–17 | 모두 "문항 설정값" 이라 개별 오류는 아님. THERM 이 기준 범위를 정해 지문에 명시하고 THERM-I-9022 해설에 병렬 근사 = 상한 명시 |
| F3 | D2W HCB overlay 허용치 | COW-A-0044(±50 nm, 선형 합) ↔ MIX-A-9013(±0.5 µm, RSS) | 10배 차, 둘 다 pitch 미기재 → 학습자에게 상반된 자릿수 | 양쪽 지문에 pad pitch 명시. MIX 는 근중복 해소 겸 재작성 |
| F4 | SoC 변당 HBM 스택 수(shoreline) | PROD-A-9032(폭 10 mm → 3개) · SIP-A-0073(11 mm·간격 없음 → 3개) ↔ SIP-I-9027(11 mm + 1 mm → 2개) | 33 mm 변에 같은 HBM 을 3개/2개로 결론 | 스택 폭(HBM3E ≈ 11 mm, HBM4 12.8 × 11 mm 업체 발표)·간격 가정을 통일해 명시 |
| F5 | refresh/온도 구간 판정 die(EA 항목 5) | THERM 9 · SIP 2 · DRAM 1 ↔ THERM-A-9026·PROD-I-9036·DRAM-A-9013·MIX-A-9056 | base die(셀 없음) 온도로 85/95 °C 판정 vs 최하단 core die 로 판정 | 최하단 core die 로 통일, 재계산(§2 표) |
| F6 | µbump EM 활성화 에너지 | FA-A-0037(0.9 eV) ↔ BUMP-A-9001·I-9007·A-9009, MIX-I-9028·A-9063(0.8 eV) | 같은 SnAg µbump 에 다른 Ea | µbump 0.8 / Cu 배선·TSV 0.9 로 맞추거나 "설정값" 명시 |
| F7 | DRFM 동작 서술 수준 | DRAM-A-0001("컨트롤러가 공격 행을 지목") ↔ PROD-B-9014·I-9028·A-9008(FACT W2-01 에 따라 명령 동작 서술 삭제) | HBM4 본문 미확인 사항을 한쪽만 단정 | DRAM-A-0001 에 근거 수준("DDR5 정의와 같은 개념으로 보면") 명시 |
| F8 | HBM4 접속 2배의 조립 부담 | PROD-A-9028("39 µm, 기존 접합으로 대응 가능") ↔ DRAM-I-0165("정렬·수율 요구 증가") | 경미한 뉘앙스 충돌 | DRAM-I-0165 이관 후 삭제, PROD-A-9028 해설 보완 |

- **일치를 확인한 항목**: MR-MUF 기구(일괄 reflow·무가압 본접합)와 방열 근거(dummy bump 최대 4배 + EMC 1.6배, X-F6) — "하중을 낮춘 개량형"·"filler 를 쓰기 쉬운"·"경로가 연속" 정답 0(MIX-A-9035 오답으로만 존재). Advanced MR-MUF = chip control + 새 EMC. HCB pitch(설정 2–15 µm, 18 µm 는 [V-2차] 발표 기준 표현, imec 2 µm 는 연구 시연 명시), µbump pitch 25–55 µm(BUMP-A-0033~ 6–20 µm 설정 해소). Black n = 2 기본(데이터로 n 추출 문항은 1–3), Ea 0.8–1.0. retention "10 °C 마다 절반" 가정 전 분야 동일(DRAM·MET·MIX·THERM·BSP). 곡률 ∝ 1/t²(Stoney) 전 분야 동일(WARP·COW·FEOL·MIX, sag 계산 WARP-A-9005·FEOL-A-9006 상호 일치). 높이 식 base + N × (core + 간극) (+ mold 별도) 전 분야 동일. 가장 뜨거운 die(상부 냉각 = base die, refresh 기준 = 최하단 core die) 서술 일치.

## 6. 개념 손실 · 전역 커버리지 공백

- 원본 5,000 → 2,448. W1 보유 판정 70군 중 보유 문항까지 사라진 군 9개를 추적했습니다: #12(SIP-A-0003 → SIP-B-9001 로 재발급), #22(KGD 이점 → MET 보유), #66(HCB 18 µm → COW-I-9001), #69(공법 명칭 → COW-B-0001~0003), #70(ESD → DRAM 이관 5문항), #23(단계적 도입 → MIX-A-9078·9079 데이터형) 은 다른 문항이 대체. **#8·#45·#48(MIX 일반론 군)은 EA 감사 W3 항목 3 에 따라 의도된 손실로 확정** — 데이터형 대체: MIX C1 사례(높이×열×수율), MIX-A-9040(한 지표 관리의 실패), COW-A-9023·THERM-A-9036(발표 수치의 적용 전제), MIX-A-9034·9035(공법 전환 판단).
- 전역(전 분야 합산) 커버리지가 0 이거나 핵심 문항이 사라진 개념:

| 개념 | 현재 | 경위 | 보강 분야 |
|---|---|---|---|
| warpage 승온/냉각 곡선 차(이력) 해석 | 0 (WARP-I-0239 는 첫 승온만) | W1 보유 WARP-A-0191 과 상대 SIP-A-0148 동시 삭제 | WARP |
| nanoprobing(트랜지스터 수준 위치 확정) | 0 | FA 브리프 §3 공백이 그대로 | FA |
| JEDEC 패키지 열저항 지표(θJC·ψJT, JESD51) | 0 | 원본에도 없음 — THERM 핵심 용어 | THERM |
| TIM 재료 선택(In·liquid metal·graphite·solder TIM) | 0 | 원본에도 없음 | THERM |
| 저단 제품의 비동작 die·spacer 로 높이 맞춤 | 0 | SIP-B-0071·B-0087 삭제 | PROD |
| 로직 base die ↔ DRAM core 이종 공정 적층 응력 | 0 | PROD-A-0043 삭제 | WARP(낮음) |
| preamble | 0 | DRAM-B-0107 삭제 | DRAM(낮음) |
| Sn whisker | 0 | BUMP 보고서가 의도적 제외 | (참고) |
| ESD(HBM/CDM) 의 FA 소유 | FA 0 | DRAM 이관 5문항 대기 | FA — 이관 수용으로 해소 |
| HBM 고유 개념(MR-MUF 기구, 계면 수 규약, 높이 예산, Smile/Cry, KGD, 하부 누적 열이력, refresh 온도 구간) | 충분 | 오히려 분야 간 중복(§3) | — |

- 브리프 §3 의 다른 공백(DRAM 타이밍·row hammer·on-die ECC, SIP PDN·SI·SoIC, COW fluxless·Advanced MR-MUF, WARP shadow moiré·동적 warpage, FA Weibull·FIT·Peck·Coffin-Manson·LTPD, MET AOI·AFM·GR&R)은 W2 신규 출제로 모두 1–20문항 이상 채워졌습니다.

## 7. 다른 에이전트에 넘길 사항

- **EA**: ① Phase 2 이동 시 §4 의 "이관 후 삭제" 23건은 이동하지 말고 삭제(사유 = 근중복). ② STANDARDS 2.5 에 "DRAM 온도 구간(refresh) 판정은 셀이 있는 최하단 core die 기준" 한 줄 추가(EA 항목 5). ③ 같은 절에 "접합층 면적 열저항·HCB overlay·스택 폭(shoreline) 은 문항 설정값 범위" 를 적으면 F2–F4 재발 방지. ④ 이 점검 중 `tools/validate.py` 를 기본 출력으로 한 번 실행해 `docs/reviews/_auto_latest.md` 가 갱신되었으나 `git checkout` 으로 되돌렸습니다(내용 차이는 W_FIG_NAME_LEAK 1건 표시뿐).
- **NUM**: §2 refresh 판정 die 12문항(정답·오답 값이 바뀜), COW-A-0072 하향, F4 shoreline 3문항, F6 FA-A-0037.
- **FACT**: F1(MR-MUF 가접합 하중) 은 X-F5 의 "불확실" 유지, F7 DRFM 은 W2-01·W2-16 의 같은 한계를 DRAM 에도 적용.
- **DA**: `f_rel` 기본 seq 가 시험명·문서 번호를 그려 FA 명칭 문항 4개의 정답을 노출 — seq 미지정 시 시험명 없이 그리는 opt-out 검토.
