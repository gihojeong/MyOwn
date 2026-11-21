# DRAM 리뷰 보고서 — DRAM 분야 에이전트 · 2026-11-21

## 요약
| | 초급 | 중급 | 고급 | 계 |
|---|---|---|---|---|
| 시작 문항 | 165 | 165 | 83 | 413 |
| 수정(원 id 유지, 전면 재작성) | 45 | 31 | 12 | 88 |
| 삭제 | 120 | 134 | 71 | 325 |
| 추가(신규 9xxx) | 19 | 39 | 52 | 110 |
| 최종 문항 | 64 | 70 | 64 | 198 |

- 브리프 신규 목표(초급 10 · 중급 30 · 고급 50) 충족. 최종 비율 초급 32 % · 중급 35 % · 고급 32 %.
- 문항 수는 413 → 198 로 줄었습니다(브리프 "±10 %" 미충족). 원인은 기계 생성 계산 가족 4 개(218 문항: 대역폭 55·채널 55·패리티 54·retention 54)가 가족당 3 개 제한(STANDARDS 3.10) 대상이었고, 나머지 비가족 문항 다수가 "온도가 내려가서" 같은 무의미 오답의 일반 SI/PI·클록·ESD 용어 문항이었기 때문입니다. 오케스트레이터 방침(질 우선, 하한 없음)에 따라 수량을 채우려 저품질을 남기지 않았습니다.
- 유지 문항(88)은 모두 지문·보기·해설·제목·지표·그림을 다시 썼고 ctx 조립형은 0 건(전부 stem 단일형). 일괄 `[근거]` 꼬리표 0 건, 메타 지표 0 건.
- 게이트: `validate --domain DRAM --gate` 차단 E 0 · **W 0** · I 183(I_JOSA_SPACE 153 — 해설 수식 뒤 공백 유지분, I_FACT_WATCH 30 — 전부 확인함). build OK, smoke `figErr: [] · errs: []`, layout_check(--no-screen) DRAM 결함 0.
- 백업(scratchpad `w2/DRAM/orig_09_DRAM.json`)과 id 대조: 원본 413 = 유지 88 + 삭제 325, 누락 0.

## 주요 기술 정정 (사실·정답·수치)
| id | 무엇이 틀렸나 | 어떻게 고쳤나 | 근거 |
|---|---|---|---|
| 대역폭 가족 55 (F08) | "HBM3E 계열" 5.6–12.8 Gb/s, "HBM4 계열" 5.6–12 Gb/s 등 실재하지 않는 세대·속도 | 3 개만 남겨 실제 구성으로 재작성: B-0003 HBM3 819 GB/s, I-0008 HBM3E(업체 9.6) vs HBM4(JEDEC 8) 비교, A-0009 목표 16 TB/s 스택 수 판단 | JESD238·JESD270-4 발표, 업체 HBM3E 발표 |
| 채널 가족 55 (F09) | 256–4,096 bit × 4–64 채널 비실재 "HBM" 구성 | B-0029(HBM3 16 × 64), I-0035(HBM3→HBM4 PC 32→64, 폭 32 bit 유지)만 남김 | JESD238·JESD270-4 |
| retention 가족 54 (NUM) | 45 °C 기준 32–128 ms → 85 °C 에서 tREFW 미달(정상 셀 가정 모순), 105 °C 사용(F45 금지) | 3 개로 정리, "약한 셀(꼬리)·1,024 ms·10 °C 반감은 문항 가정"으로 명시, 105 °C 제거, f_therm 그림 → 조건 표 | NUM §2.4, FACT F45 |
| ECC 가족 54 | 동형 54 개, 고급이 단순 대입 | B-0045 (72,64) 12.5 %, I-0047 Hamming 한계로 본 (136,128) SEC 의 DED 불가, A-0024 on-die SEC 오정정 + host SECDED 상호작용 | Hamming 한계, JESD79-5 on-die ECC 128+8 |
| DRAM-I-0001 | "고객이 11 Gb/s 요구" 보도([R])를 문항 전제로 사용 | 업체 발표 "10 Gb/s 이상 HBM4"([V])와 JEDEC 8 Gb/s 의 관계 해석으로 재작성 | JESD270-4, SK hynix HBM4 발표 |
| DRAM-B-0086/B-0105 | HBM 데이터 신호를 차동으로 볼 여지 | HBM 데이터선은 단일 종단임을 명시, 차동 문항(B-0105) 삭제 | JESD235/238 |
| DRAM-B-0117 | "리드-솔로몬 = 여러 비트 오류 대응" 단순 회상 | HBM3 의 symbol 기반 on-die ECC([S])로 묶음 오류 이점을 묻도록 재작성 | JEDEC HBM3 발표 |
| DRAM-B-0162 → B-9019 | DRAM 분야에 GAA 나노시트(로직) 회상 | 삭제 후 DRAM 주변 회로 HKMG 신규 문항(B-9019)으로 대체 | 업체 HKMG DRAM 발표 |
| DRAM-A-0083 | "I/O 폭 유지·핀 속도 상향" 을 4 TB/s 경로의 정답으로 단정(근거 없는 로드맵) | 가상의 두 확장안(속도 2 배 vs 폭 2 배)의 주 제약 비교로 재작성, "실재 세대 아님" 명시 | STANDARDS 2.2 |
| DRAM-A-0080 | iHBM ICE 위치 주장(FACT 미확인 업체 주장) | 삭제 | FACT 브리프 §1A |
| DRAM-A-0001 | DRFM 정의 회상(고급 부적합) | RFM 대비 DRFM 의 유리 조건과 대가 판단으로 고급화 | JESD270-4 발표(DRFM) |

신규 문항 주제(공백 보강): 1T1C·charge sharing 신호 계산(I-9001, A-9001·9002·9043), sense amp 오프셋(A-9003), tRCD/tRP/tRC/tWR/tWTR/tFAW·bank group tCCD(B-9002~9004, I-9003~9006·9037, I-9039, A-9006), refresh·tRFC/tREFI·per-bank·self refresh·연기(B-9005·9006·9013, I-9007~9009·9026·9034, A-9004·9005·9036·9040), row hammer·TRR·RFM·DRFM·PRAC·half-double(B-9001, I-9010~9015, A-9007·9008·9041), on-die ECC·symbol ECC·보고(I-9016·9028, A-9011·9017·9045·9047), retention·VRT·Arrhenius·누설 예산(I-9017·9018, A-9009·9031·9037), DRAM 공정 BCAT·capacitor·high-k·EUV·HKMG(B-9008~9010, I-9019·9020, A-9014·9028·9029), HBM 구조·동시성·성능(I-9021·9022·9030, A-9010·9016·9021·9022·9030·9032·9033·9042), 스택 온도와 refresh 정책(I-9025, A-9013·9025·9044·9049·9050).

## 삭제 목록
| id | 사유 |
|---|---|
| DRAM-A-0002, DRAM-A-0003, DRAM-A-0004, DRAM-A-0005, DRAM-A-0006, DRAM-A-0007, DRAM-A-0008, DRAM-A-0010, DRAM-A-0011, DRAM-A-0012, DRAM-B-0001, DRAM-B-0002, DRAM-B-0004, DRAM-B-0005, DRAM-B-0006, DRAM-B-0007, DRAM-B-0008, DRAM-B-0009, DRAM-B-0010, DRAM-B-0011, DRAM-B-0012, DRAM-B-0013, DRAM-B-0014, DRAM-B-0015, DRAM-B-0016, DRAM-B-0017, DRAM-B-0018, DRAM-B-0019, DRAM-B-0020, DRAM-B-0021, DRAM-B-0022, DRAM-I-0002, DRAM-I-0003, DRAM-I-0004, DRAM-I-0005, DRAM-I-0006, DRAM-I-0007, DRAM-I-0009, DRAM-I-0010, DRAM-I-0011, DRAM-I-0012, DRAM-I-0013, DRAM-I-0014, DRAM-I-0015, DRAM-I-0016, DRAM-I-0017, DRAM-I-0018, DRAM-I-0019, DRAM-I-0020, DRAM-I-0021, DRAM-I-0022, DRAM-I-0023 (52) | 가족 초과(대역폭 계산 55문항 → B-0003·I-0008·A-0009 로 재작성 유지) · FACT F08 범위 밖 'HBM3E' 속도 |
| DRAM-A-0013, DRAM-A-0014, DRAM-A-0015, DRAM-A-0017, DRAM-A-0018, DRAM-A-0019, DRAM-A-0020, DRAM-A-0021, DRAM-A-0022, DRAM-A-0023, DRAM-B-0023, DRAM-B-0024, DRAM-B-0025, DRAM-B-0026, DRAM-B-0027, DRAM-B-0028, DRAM-B-0030, DRAM-B-0031, DRAM-B-0032, DRAM-B-0033, DRAM-B-0034, DRAM-B-0035, DRAM-B-0036, DRAM-B-0037, DRAM-B-0038, DRAM-B-0039, DRAM-B-0040, DRAM-B-0041, DRAM-B-0042, DRAM-B-0043, DRAM-B-0044, DRAM-I-0024, DRAM-I-0025, DRAM-I-0026, DRAM-I-0027, DRAM-I-0028, DRAM-I-0029, DRAM-I-0030, DRAM-I-0031, DRAM-I-0032, DRAM-I-0033, DRAM-I-0034, DRAM-I-0036, DRAM-I-0037, DRAM-I-0038, DRAM-I-0039, DRAM-I-0040, DRAM-I-0041, DRAM-I-0042, DRAM-I-0043, DRAM-I-0044, DRAM-I-0045 (52) | 가족 초과(채널·pseudo channel 55문항 → B-0029·I-0035 로 재작성 유지) · FACT F09 비실재 'HBM' 구성 |
| DRAM-A-0016 (1) | 주제가 바뀐 재작성 — 새 문항 DRAM-A-9051 로 재발급(오케스트레이터 결정, prev 없음) |
| DRAM-A-0025, DRAM-A-0026, DRAM-A-0027, DRAM-A-0028, DRAM-A-0029, DRAM-A-0030, DRAM-A-0031, DRAM-A-0032, DRAM-A-0033, DRAM-B-0046, DRAM-B-0047, DRAM-B-0048, DRAM-B-0049, DRAM-B-0050, DRAM-B-0051, DRAM-B-0052, DRAM-B-0053, DRAM-B-0054, DRAM-B-0055, DRAM-B-0056, DRAM-B-0057, DRAM-B-0058, DRAM-B-0059, DRAM-B-0060, DRAM-B-0061, DRAM-B-0062, DRAM-B-0063, DRAM-B-0064, DRAM-B-0065, DRAM-B-0066, DRAM-I-0046, DRAM-I-0048, DRAM-I-0049, DRAM-I-0050, DRAM-I-0051, DRAM-I-0052, DRAM-I-0053, DRAM-I-0054, DRAM-I-0055, DRAM-I-0056, DRAM-I-0057, DRAM-I-0058, DRAM-I-0059, DRAM-I-0060, DRAM-I-0061, DRAM-I-0062, DRAM-I-0063, DRAM-I-0064, DRAM-I-0065, DRAM-I-0066, DRAM-I-0067 (51) | 가족 초과(패리티 비율 54문항 → B-0045·I-0047·A-0024 로 재작성 유지) |
| DRAM-A-0034, DRAM-A-0035, DRAM-A-0036, DRAM-A-0037, DRAM-A-0038, DRAM-A-0039, DRAM-A-0040, DRAM-A-0041, DRAM-A-0042, DRAM-A-0043, DRAM-A-0044, DRAM-A-0045, DRAM-A-0047, DRAM-A-0048, DRAM-A-0049, DRAM-A-0050, DRAM-A-0051, DRAM-A-0052, DRAM-A-0053, DRAM-A-0054, DRAM-A-0055, DRAM-I-0068, DRAM-I-0069, DRAM-I-0071, DRAM-I-0072, DRAM-I-0073, DRAM-I-0074, DRAM-I-0075, DRAM-I-0076, DRAM-I-0077, DRAM-I-0078, DRAM-I-0079, DRAM-I-0080, DRAM-I-0081, DRAM-I-0082, DRAM-I-0083, DRAM-I-0084, DRAM-I-0085, DRAM-I-0086, DRAM-I-0088, DRAM-I-0089, DRAM-I-0090, DRAM-I-0091, DRAM-I-0092, DRAM-I-0093, DRAM-I-0094, DRAM-I-0095, DRAM-I-0096, DRAM-I-0097, DRAM-I-0098, DRAM-I-0099 (51) | 가족 초과(retention 반감 54문항 → I-0070·I-0087·A-0046 로 재작성 유지) · NUM 비현실 설정(기준 보존 32–128 ms)·105 °C 사용 |
| DRAM-A-0064, DRAM-A-0065, DRAM-A-0074, DRAM-B-0142, DRAM-B-0146, DRAM-B-0147, DRAM-B-0148, DRAM-B-0150, DRAM-I-0142, DRAM-I-0147, DRAM-I-0149 (11) | 타 분야 중복(XD 지시 삭제: ESD 일반 → FA 보유 / A-0074 는 MIX-A-0051 보유) |
| DRAM-A-0058, DRAM-A-0076 (2) | 타 분야 중복: FA-I-0071(초음파 반사 위상 반전) — DRAM 학습 목표 밖 |
| DRAM-B-0082 (1) | 타 분야 중복: PROD-B-0036(TSV 영역의 셀 효율) |
| DRAM-A-0062, DRAM-A-0063, DRAM-B-0149, DRAM-I-0144, DRAM-I-0145 (5) | 일반 CMOS latch-up — DRAM 학습 목표 밖, B/I/A 동형 반복 |
| DRAM-B-0143, DRAM-B-0145, DRAM-I-0140, DRAM-I-0141 (4) | 근중복: B-0144·A-0059(I/O 보호 소자 용량 절충) |
| DRAM-I-0146 (1) | ESD 작업 환경(습도) 일반 — FA 범위, 오답 무의미 |
| DRAM-B-0070, DRAM-B-0091 (2) | 근중복: B-0069(채널의 의미) |
| DRAM-B-0077, DRAM-B-0097 (2) | 근중복: B-0094·B-0098(온도와 refresh·온도 보고) |
| DRAM-B-0089 (1) | 품질 미달(용량·대역폭 정의, 오답 무의미) — B-0088 과 중복 |
| DRAM-B-0090 (1) | 근중복: B-0067(넓은 I/O) |
| DRAM-B-0092, DRAM-B-0093 (2) | 근중복: B-0087(짧은 배선·전력 효율) |
| DRAM-B-0095 (1) | 근중복: B-0078(refresh 와 실효 대역폭) |
| DRAM-B-0096 (1) | 근중복: B-0081(on-die ECC 목적) |
| DRAM-B-0099 (1) | 근중복: I-0100(단수와 대역폭) |
| DRAM-B-0102 (1) | 근중복: B-0100(DBI) |
| DRAM-B-0109 (1) | 근중복: B-0110(eye diagram) |
| DRAM-B-0113, DRAM-B-0114 (2) | 근중복: B-0112·B-0117(패리티·정정 부호) |
| DRAM-B-0116 (1) | 근중복: I-0122(CE 증가 추세) |
| DRAM-B-0121, DRAM-I-0125 (2) | 근중복: B-0120(interleaving) |
| DRAM-B-0122 (1) | 근중복: I-0122·I-0124(정정 한계·원인 분석) |
| DRAM-B-0103, DRAM-B-0104, DRAM-B-0105, DRAM-B-0106, DRAM-B-0107, DRAM-B-0111 (6) | 품질 미달: 일반 SI 용어 문항, 물리적으로 무의미한 오답(온도가 내려가서 등) — DRAM I/O 문항으로 대체 |
| DRAM-B-0127, DRAM-B-0128, DRAM-B-0129 (3) | 근중복·품질 미달: I-0115·I-0117·B-0125(PDN 공진·전원 잡음) |
| DRAM-B-0130, DRAM-B-0131, DRAM-B-0132, DRAM-B-0133, DRAM-B-0134, DRAM-B-0135, DRAM-B-0137 (7) | 품질 미달: 일반 디지털 클록·setup/hold 용어, 무의미 오답 — DRAM 타이밍(tRCD·tRP·tRC 등) 신규 문항으로 대체 |
| DRAM-B-0139, DRAM-B-0140 (2) | 근중복: B-0138(training) |
| DRAM-B-0151, DRAM-B-0163 (2) | 품질 미달: 정의 회상·무의미 오답 |
| DRAM-B-0155 (1) | 근중복: B-9018(명령 버스) |
| DRAM-B-0156, DRAM-B-0158 (2) | 근중복: B-0157·I-0150(memory-bound) |
| DRAM-B-0159, DRAM-B-0160 (2) | 근중복: B-0153·B-0098 |
| DRAM-B-0164 (1) | 근중복: I-0159(특정 채널 불량) |
| DRAM-B-0165 (1) | 근거 불충분(D2D PHY 열·iHBM) — A-0080 과 같은 미확인 업체 주장 |
| DRAM-I-0104, DRAM-I-0108, DRAM-I-0109, DRAM-I-0110, DRAM-I-0111, DRAM-I-0112, DRAM-I-0113, DRAM-I-0114, DRAM-I-0116, DRAM-I-0119, DRAM-I-0120, DRAM-I-0121 (12) | 품질 미달: 일반 SI·PI 일반론, 형식적·무의미 오답 — I-0102~0117 재작성 문항과 근중복 |
| DRAM-I-0127 (1) | 근중복: B-0123(ECC 와 공정) |
| DRAM-I-0129 (1) | 근중복: A-9012(온도와 CE) |
| DRAM-I-0130, DRAM-I-0131 (2) | 품질 미달: 일반 클록 skew 용어 |
| DRAM-I-0133, DRAM-I-0134 (2) | 근중복: I-0132·B-0138 |
| DRAM-I-0136, DRAM-I-0137, DRAM-I-0139 (3) | 품질 미달: 일반론·기술 외 오답 |
| DRAM-I-0151, DRAM-I-0152 (2) | 근중복: B-0152·B-0153 |
| DRAM-I-0154, DRAM-I-0155 (2) | 근중복: B-0098·A-0056(온도 보고·throttling) |
| DRAM-I-0156, DRAM-I-0157, DRAM-I-0158 (3) | 근중복·품질 미달: B-0153·B-0157·A-9032 |
| DRAM-I-0160, DRAM-I-0161, DRAM-I-0163 (3) | 근거 불충분 일반론('채널 간 편차 누적') — 정답 근거 없음 |
| DRAM-A-0066, DRAM-A-0067 (2) | 근중복: I-0150·A-9032(memory-bound·실효 대역폭) |
| DRAM-A-0069 (1) | THERM 범위·근거 불충분(상면 높이 정합과 국부 고온) |
| DRAM-A-0070, DRAM-A-0071, DRAM-A-0072, DRAM-A-0075, DRAM-A-0077, DRAM-A-0078, DRAM-A-0079, DRAM-A-0081 (8) | 품질 미달: 일반론 '판단 태도'형 고급(STANDARDS §1 금지) — 정량 고급 신규 문항으로 대체 |
| DRAM-A-0080 (1) | FACT 미확인 업체 주장(iHBM ICE) — 정답 근거 불가 |
| DRAM-A-0057 (1) | 주제가 바뀐 재작성 — 새 문항 DRAM-A-9052 로 재발급(오케스트레이터 결정, prev 없음) |
| DRAM-B-0136 (1) | 주제가 바뀐 재작성 — 새 문항 DRAM-B-9017 로 재발급(오케스트레이터 결정, prev 없음) |
| DRAM-B-0154 (1) | 주제가 바뀐 재작성 — 새 문항 DRAM-B-9018 로 재발급(오케스트레이터 결정, prev 없음) |
| DRAM-B-0162 (1) | 주제가 바뀐 재작성 — 새 문항 DRAM-B-9019 로 재발급(오케스트레이터 결정, prev 없음) |
| DRAM-I-0118 (1) | 주제가 바뀐 재작성 — 새 문항 DRAM-I-9039 로 재발급(오케스트레이터 결정, prev 없음) |

## 난이도 변경 · id 재발급
| 옛 id | 새 id | 이유 |
|---|---|---|
| DRAM-A-0016 | DRAM-A-9051 | 주제 변경(채널 폭 → bank 충돌 확률) — 오케스트레이터 결정으로 새 문항 처리, prev 없음 |
| DRAM-A-0057 | DRAM-A-9052 | 주제 변경(동축 TSV 단정 → TSV 예산 안 차폐 배치) |
| DRAM-B-0136 | DRAM-B-9017 | 주제 변경(속도·타이밍 일반론 → 8 Gb/s UI 계산) |
| DRAM-B-0154 | DRAM-B-9018 | 주제 변경(CA 버스 명칭 → HBM 행/열 명령 버스 분리) |
| DRAM-B-0162 | DRAM-B-9019 | 주제 변경(GAA → DRAM 주변 회로 HKMG) |
| DRAM-I-0118 | DRAM-I-9039 | 주제 변경(전력 급변 일반론 → tFAW) |

난이도 변경은 없습니다. 위 6 건은 원 id 를 삭제 목록에 넣었고, 새 id 에 `prev` 를 두지 않았습니다(풀이 이력이 다른 문항에 연결되지 않도록).

## 이관 제안 (mv)
| id | 대상 분야 | 이유 |
|---|---|---|
| DRAM-B-0141 | FA | XD 지시: ESD 정의(재작성 완료) |
| DRAM-I-0143 | FA | XD 지시: ESD 손상 분석 단서(재작성) |
| DRAM-I-0148 | FA | XD 지시: HBM/CDM 두 시험 모델(재작성, JS-001/JS-002) |
| DRAM-A-0060 | FA | XD 지시: 잠재 ESD 손상 선별(재작성, 누설 꼬리 데이터형) |
| DRAM-A-0061 | FA | XD 지시: ESD vs EM 감별(재작성, 두 시료 데이터형) |
| DRAM-I-0165 | PROD | XD 지시: HBM4 I/O 확대의 조립 측 부담(재작성) |

DRAM 이 보유하는 ESD 설계 관점 문항: B-0144(I/O 보호 용량), A-0059(용량 예산과 CDM 목표).

## 면제(vx) 목록
| id | 코드 | 사유 |
|---|---|---|
| — | — | 없음 |

## 남은 우려 · EA/DA 에 요청
- **수량**: 413 → 198. 고급은 64(브리프 희망 130 이상에 못 미침). 신규 고급 50 은 모두 다단계 계산·표/그래프 해석·원인 규명형입니다. 추가 증원이 필요하면 W3 에서 같은 기준으로 보강 가능합니다.
- **문항 설정값**: retention 10 °C 반감, 열 모델(A-9044), pJ/bit(A-9024), tFAW 16 ns 등은 지문에 "이 문항의 가정/설정값" 으로 명시했고 정답 근거를 업체 값에 두지 않았습니다. DDR4 tRFC(8 Gb 350 ns, 16 Gb 550 ns)·tREFI 7.8 µs, DDR5 on-die ECC 128+8, HBM2 BL2/BL4, PRAC(JESD79-5C)은 `src` 에 표준 근거를 적었습니다 — FACT 가 원문 확인을 원하면 이 `src` 들을 우선 대상으로 해 주십시오.
- **HBM 고유 미확인 사항은 쓰지 않음**: HBM 의 tREFI·tRFC 값, HBM 고유 온도 상한, HBM3/4 bank 수·burst 길이 규격값(I-9021 은 BL8 을 "문항 설정"으로 둠).
- 정답 위치는 손대지 않았습니다(신규 문항 다수가 a=0). EA Phase 2 재배치 대상이며, 해설의 ①–④ 참조는 현재 보기 순서와 일치합니다.
