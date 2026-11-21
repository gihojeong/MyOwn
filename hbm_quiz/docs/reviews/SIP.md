# SIP 리뷰 보고서 — 분야 에이전트 SIP · 2026-11-21

## 요약
| | 초급 | 중급 | 고급 | 계 |
|---|---|---|---|---|
| 시작 문항 | 175 | 172 | 190 | 537 |
| 수정(기존 id 유지·재작성, 원 lv 기준) | 37 | 16 | 12 | 65 |
| 삭제 | 138 | 156 | 178 | 472 |
| 추가(신규 9xxx) | 12 | 31 | 32 | 75 |
| 최종 문항 | 50 | 50 | 40 | 140 |

- 수정 65 에는 난이도 변경 재발급 4건 포함(고급→초급 1, 고급→중급 3; 아래 표). 최종 비율 B 36 % · I 36 % · A 29 %.
- 기존 유지 문항 대조: 백업(537 id) 대비 **누락 0** — 모든 원 id 는 최종 파일에 있거나(동일 id 또는 `prev`) 아래 삭제 표에 사유가 있음.
- 게이트: `validate --domain SIP --gate` 통과 — **E 0 · W 0** (I 145: I_JOSA_SPACE 136, I_FACT_WATCH 9 — 모두 "775 µm" 설계 조건 문구·대역폭 식 확인 표시). build(스크래치 출력) + smoke `figErr: [] · errs: []`. layout_check(--no-screen) SIP 결함 0.
- 규모 축소 사유: 원 537 중 약 320 이 수치만 바꾼 계산 가족(높이·최대 단수·두께·reticle 면적·구조 이름 고르기)이었고, ctx 조립형 B/I/A 약 200 은 같은 개념(인터포저 이점, bridge 이점, C4 크기 등)을 3–5회 반복하거나 기술 외 오답(색상·포장·보관·조직)·번호 나열 해설이었습니다. 코디네이터 방침(질 우선, 수량 하한 없음, 신규 목표 B10/I30/A30 충족)에 따라 대표만 재작성했습니다.
- 작업 파일(재현용): scratchpad `w2/SIP/` 의 `p_10_fam.py`(가족)·`p_20_B.py`·`p_30_IA.py`(기존 재작성/삭제)·`p_40/50/60/61_*`(신규), `apply.py` 가 `orig.json` 에서 data 를 생성, `ledger.json` 에 R/D/N 기록.

## 주요 기술 정정 (사실·정답·수치)
| id | 무엇이 틀렸나 | 어떻게 고쳤나 | 근거 |
|---|---|---|---|
| SIP-A-0064·0069·0070 | 같은 값 보기 2개(정답 비유일) | 가족 정리로 삭제, 대표 SIP-I-0016 을 현실 값(14장)으로 재작성 | NUM §1 |
| SIP-B-0023·B-0024·I-0082·I-0083 | 면적 나눗셈(⌊858÷s²⌋)을 "배치 가능한 최대 개수"로 정답화 — 12 mm 부품은 실제 2×2=4개 | B-0023 은 면적만 묻게, I-0082 는 격자 배치 개수(4개, 면적 상한 5와 구분)로 재작성, 나머지 삭제 | NUM §1 |
| 높이 가족 2.1·2.6(85) | 결과 17–31단, f_stack `n`·`h_um` 에 정답 노출, "JEDEC 775 µm" 근거 | 대표 I-0016(14장)·A-0043(공법별 core 두께 선택)·I-0063(36.1 µm)·I-0104(740 µm)·A-0013(최악 조건 산포 배분)으로 재작성. 모두 "높이 상한(설계 조건) 775 µm", 그림은 입력만 + `hideResult` | NUM §2, FACT F12·F13, STANDARDS 2.4 |
| 2.2 두께 가족 8단 멤버 | 8단에서 허용 core 78–92 µm — 높이 제약이 의미 없음 | 16단(I-0063)으로 재설정 | NUM §2.2 |
| SIP-I-0011·I-0144·I-0013 | CoWoS-R 은 "수직 통로가 없어 전원이 기판을 돌아간다/기판이 담당" | I-0013 을 S=TSV · R=RDL 적층 via · L=몰딩층 TIV 짝짓기 문항으로 정정, I-0011·I-0144 삭제 | FACT F37 (TSMC ECTC 2023) |
| SIP-I-0146 | CoWoS-L "칩 간 배선이 브리지로만 이어진다" 를 정답화 | 정답을 "LSI 위 미세 pitch 정렬 여유"로, F37 서술은 오답으로 | FACT F37 |
| SIP-I-0145·I-0136·I-0139·B-0131·B-0138·A-0153·A-0178·B-0171 | CoWoS-R 한계를 "die·기판과 팽창률 차이"로 정답화 | B-0138 정답을 "최소 L/S 2/2 µm 로 배선 수 적음"으로, I-0014 는 RDL 의 CTE 완충이 C4 변형 에너지를 줄인다로, A-0178 은 RDL 전환+배선 수용 계산(6 mm 폭 4층 6,000 트랙 ≥ 2,000)으로 재작성; 나머지 삭제 | FACT F36 (TSMC CoWoS-R, ECTC 2021) |
| SIP-B-0001·B-0003~0022·I-0003~0012 | 세대 없이 "2,048개 데이터 선" + `lines` 누락 | B-0001 에 "HBM4" 명시 + `lines: 2048`, I-9025 는 HBM3E 1,024 vs HBM4 2,048 비교; 가족 나머지 삭제 | FACT F11 · JESD270-4 |
| SIP-I-0015 | "전면 Si 8 · 유기 RDL 4–6 · 브리지 12+" 탑재 수를 사실로 제시 | 수치 삭제, "면적과 미세 배선 범위" 원리만 묻도록 재작성 | FACT F35 |
| SIP-I-0142 | Si interposer 면적 한계 대응의 정답이 "브리지 전환" 하나 — stitching(CoWoS-S 3.3×)도 정답 | stitching + 경계 정렬 관리 문항으로 재작성 | FACT F34 |
| SIP-A-0002·B-0175·I-0162·A-0185·A-0190·B-0163 | "JEDEC 720→775 µm 완화"·"775 µm 규격"을 정답 근거로 사용 | 삭제(사용 금지 판정) | FACT F12·F13 |
| SIP-A-0075 → I-9001 | HCB 비표준 표기, dishing 그림 opt-in 누락 | "HCB(Cu–Cu hybrid bonding)" 통일, `f_bond hcb dish:true`, mv COW | XD §1·§3 |
| SIP-A-0003 → B-9001 | 간극 수 "die 수보다 하나 적다" 서술(XD 권고) | "간극 수 = core die 수(base–core1 포함)" 로 명시, mv PROD | STANDARDS 2.5, XD |
| SIP-A-0187·A-0188 | "저단·후막이면 MR-MUF 유리" 공법 우열 단정 | 출처 없음으로 삭제(XD 는 mv COW 제안 — 근거 부족으로 다르게 처리) | FACT X-F6 범위 밖 |

### 템플릿 문구(DA §7, 2026-11-21) 대조
- f_sip cowos-r/l/s/emib 고정 문구 변경 확인: 남은 문항 중 옛 문구("TSV가 없어 전원은 substrate 경유", "reticle 크기가 상한")를 정답 근거로 쓰는 문항 없음. 전원 경로를 묻는 문항(B-0002, I-0013, I-0014)은 애초에 f_note/f_table 을 써서 그림 문구와 독립. 새 param `msg` 는 validate 스키마에 없어 사용하지 않음.

## 신규 출제(75) — 공백 주제 보강
- 초급 12: 접합 계층 pitch, L/S→피치, 차폐선, IR drop, decap, eye diagram, shadow moiré, HBM-on-logic 과제, SoIC, CUF, 인터포저 사전 검사, TIM1/TIM2.
- 중급 31: 배선 R·RC·전파 지연·Nyquist·skew, RDL 층수·배선 폭 비, crosstalk 대책, IR 예산·µbump 수·decap 용량, C4 전단 변형·DNP 스케일, CoS 우선 위험, CoW 후 몰딩, underfill void·물성·충전 시간(Washburn), reflow 휨(Smile)과 non-wet, bare die vs lid, TIM ΔT, stitching 경계, HBM3E→HBM4 배선 수요, shoreline, logic-on-bottom TSV 부담, HCB 접속 밀도, TC 피로 판별, bump 배분, ISI 판별, 2-SoC + LSI.
- 고급 32: 배선 수용+저항 동시 판정, RC 예산 최대 길이, 직렬 PDN 병목, crosstalk/SSN 데이터 판독(2), Coffin–Manson 수명 예측·교란 변수 보정, 휨 대책 동시 판정, 조립 순서 수율 비교, 3D 열 ΔT, lid 온도→base die 판정, 전류 쏠림 µbump 수, IR+EM TSV 수, underfill 충전 대책, 대역폭+shoreline 구성, 검사 누락률 역산, underfill 후보 선택(Tg 함정), 열·휨 동시 규격, 2.5D/3D I/O 전력, skew 예산, C4 전원 비율, CoWoS 종류 선택, EMIB/EMIB-T 강하, ground bounce, C4 reflow 휨 위치, PHY 거리 전력, TIM 최악 두께, 온도 외삽(f_plot), bridge 병목 자원, 거리–지연 상충, decap 위치, 스택별 TIM void 판독.
- 수치는 모두 "설계 조건/사내 기준/가정" 으로 지문에 주고 해설에 식·대입·결과·오답별 실수를 적음. 고급 결과 온도는 ≤ 93 °C, 단수 ≤ 16.

## 삭제 목록
### 가족 정리로 삭제 (사유 동일 묶음)

| 가족 (NUM 절) | 삭제 수 | 삭제 id |
|---|---|---|
| 가족 초과·근중복 (2.7 die·간극·pad 수 환산(10)) — 대표만 재작성 유지 | 9 | SIP-A-0004, SIP-A-0005, SIP-A-0006, SIP-A-0007, SIP-A-0008, SIP-A-0009, SIP-A-0010, SIP-A-0011, SIP-A-0012 |
| 가족 초과·근중복 (2.5 N단 높이·상한 판정(30)) — 대표만 재작성 유지 | 29 | SIP-A-0014, SIP-A-0015, SIP-A-0016, SIP-A-0017, SIP-A-0018, SIP-A-0019, SIP-A-0020, SIP-A-0021, SIP-A-0022, SIP-A-0023, SIP-A-0024, SIP-A-0025, SIP-A-0026, SIP-A-0027, SIP-A-0028, SIP-A-0029, SIP-A-0030, SIP-A-0031, SIP-A-0032, SIP-A-0033, SIP-A-0034, SIP-A-0035, SIP-A-0036, SIP-A-0037, SIP-A-0038, SIP-A-0039, SIP-A-0040, SIP-A-0041, SIP-A-0042 |
| 가족 초과·근중복 (2.6 최대 core die 수(30)) — 대표만 재작성 유지; 17–31단 비현실 결과·그림 n 노출 포함 | 26 | SIP-A-0044, SIP-A-0045, SIP-A-0046, SIP-A-0047, SIP-A-0048, SIP-A-0049, SIP-A-0050, SIP-A-0051, SIP-A-0052, SIP-A-0053, SIP-A-0054, SIP-A-0055, SIP-A-0056, SIP-A-0057, SIP-A-0058, SIP-A-0059, SIP-A-0060, SIP-A-0061, SIP-A-0062, SIP-A-0063, SIP-A-0065, SIP-A-0066, SIP-A-0067, SIP-A-0068, SIP-A-0071, SIP-A-0072 |
| 가족 초과·근중복 (2.1 높이 상한 내 최대 단수(55)) — 대표만 재작성 유지; 17–31단 비현실 결과·그림 n 노출 포함 | 54 | SIP-A-0078, SIP-A-0079, SIP-A-0080, SIP-A-0081, SIP-A-0082, SIP-A-0083, SIP-A-0084, SIP-A-0085, SIP-A-0086, SIP-A-0087, SIP-A-0088, SIP-A-0089, SIP-A-0090, SIP-A-0091, SIP-A-0092, SIP-A-0093, SIP-A-0094, SIP-A-0095, SIP-A-0096, SIP-A-0097, SIP-A-0098, SIP-A-0099, SIP-I-0017, SIP-I-0018, SIP-I-0019, SIP-I-0020, SIP-I-0021, SIP-I-0022, SIP-I-0023, SIP-I-0024, SIP-I-0025, SIP-I-0026, SIP-I-0027, SIP-I-0028, SIP-I-0029, SIP-I-0030, SIP-I-0031, SIP-I-0032, SIP-I-0033, SIP-I-0034, SIP-I-0035, SIP-I-0036, SIP-I-0037, SIP-I-0038, SIP-I-0039, SIP-I-0040, SIP-I-0041, SIP-I-0042, SIP-I-0043, SIP-I-0044, SIP-I-0045, SIP-I-0046, SIP-I-0047, SIP-I-0048 |
| 가족 초과·근중복 (2.2 core die 최대 두께(55)) — 대표만 재작성 유지 | 54 | SIP-A-0100, SIP-A-0101, SIP-A-0102, SIP-A-0103, SIP-A-0104, SIP-A-0105, SIP-A-0106, SIP-A-0107, SIP-A-0108, SIP-A-0109, SIP-A-0110, SIP-A-0111, SIP-A-0112, SIP-A-0113, SIP-A-0114, SIP-A-0115, SIP-A-0116, SIP-A-0117, SIP-A-0118, SIP-A-0119, SIP-A-0120, SIP-A-0121, SIP-I-0049, SIP-I-0050, SIP-I-0051, SIP-I-0052, SIP-I-0053, SIP-I-0054, SIP-I-0055, SIP-I-0056, SIP-I-0057, SIP-I-0058, SIP-I-0059, SIP-I-0060, SIP-I-0061, SIP-I-0062, SIP-I-0064, SIP-I-0065, SIP-I-0066, SIP-I-0067, SIP-I-0068, SIP-I-0069, SIP-I-0070, SIP-I-0071, SIP-I-0072, SIP-I-0073, SIP-I-0074, SIP-I-0075, SIP-I-0076, SIP-I-0077, SIP-I-0078, SIP-I-0079, SIP-I-0080, SIP-I-0081 |
| 가족 초과·근중복 (2.3 reticle 배수 면적(54)) — 대표만 재작성 유지 | 50 | SIP-A-0122, SIP-A-0123, SIP-A-0124, SIP-A-0125, SIP-A-0126, SIP-A-0127, SIP-A-0128, SIP-A-0129, SIP-A-0130, SIP-A-0131, SIP-B-0025, SIP-B-0026, SIP-B-0027, SIP-B-0028, SIP-B-0029, SIP-B-0030, SIP-B-0031, SIP-B-0032, SIP-B-0033, SIP-B-0034, SIP-B-0035, SIP-B-0036, SIP-B-0037, SIP-B-0038, SIP-B-0039, SIP-B-0040, SIP-B-0041, SIP-B-0042, SIP-B-0043, SIP-B-0044, SIP-I-0084, SIP-I-0085, SIP-I-0086, SIP-I-0087, SIP-I-0088, SIP-I-0089, SIP-I-0090, SIP-I-0091, SIP-I-0092, SIP-I-0093, SIP-I-0094, SIP-I-0095, SIP-I-0096, SIP-I-0097, SIP-I-0098, SIP-I-0099, SIP-I-0100, SIP-I-0101, SIP-I-0102, SIP-I-0103 |
| 가족 초과·근중복 (2.4 스택 높이(54)) — 대표만 재작성 유지 | 53 | SIP-A-0132, SIP-A-0133, SIP-A-0134, SIP-A-0135, SIP-A-0136, SIP-A-0137, SIP-A-0138, SIP-A-0139, SIP-A-0140, SIP-A-0141, SIP-B-0045, SIP-B-0046, SIP-B-0047, SIP-B-0048, SIP-B-0049, SIP-B-0050, SIP-B-0051, SIP-B-0052, SIP-B-0053, SIP-B-0054, SIP-B-0055, SIP-B-0056, SIP-B-0057, SIP-B-0058, SIP-B-0059, SIP-B-0060, SIP-B-0061, SIP-B-0062, SIP-B-0063, SIP-B-0064, SIP-B-0065, SIP-B-0066, SIP-I-0105, SIP-I-0106, SIP-I-0107, SIP-I-0108, SIP-I-0109, SIP-I-0110, SIP-I-0111, SIP-I-0112, SIP-I-0113, SIP-I-0114, SIP-I-0115, SIP-I-0116, SIP-I-0117, SIP-I-0118, SIP-I-0119, SIP-I-0120, SIP-I-0121, SIP-I-0122, SIP-I-0123, SIP-I-0124, SIP-I-0125 |
| 가족 초과·근중복 (구조 이름 고르기(20)) — 대표만 재작성 유지 | 18 | SIP-B-0003, SIP-B-0005, SIP-B-0006, SIP-B-0007, SIP-B-0008, SIP-B-0009, SIP-B-0011, SIP-B-0012, SIP-B-0013, SIP-B-0014, SIP-B-0015, SIP-B-0016, SIP-B-0017, SIP-B-0018, SIP-B-0019, SIP-B-0020, SIP-B-0021, SIP-B-0022 |
| 가족 초과·근중복 (중간 기판 쟁점 쌍(10)) — 대표만 재작성 유지 | 10 | SIP-I-0003, SIP-I-0004, SIP-I-0005, SIP-I-0006, SIP-I-0007, SIP-I-0008, SIP-I-0009, SIP-I-0010, SIP-I-0011, SIP-I-0012 |

### 개별 사유 삭제

| id | 사유 |
|---|---|
| SIP-A-0001 | 근중복: SIP-B-0080 (reticle 제약) — 고급 기준 미달 |
| SIP-A-0002 | 판단 일반론 + 그림 수치 불일치(h 720, 상한 775) — FACT F12/F13 |
| SIP-A-0064 | 정답 비유일(같은 값 보기 2개, NUM) + 가족 초과(2.6) — 대표 SIP-I-0016 으로 대체 |
| SIP-A-0069 | 정답 비유일(같은 값 보기 2개, NUM) + 가족 초과(2.6) — 대표 SIP-I-0016 으로 대체 |
| SIP-A-0070 | 정답 비유일(같은 값 보기 2개, NUM) + 가족 초과(2.6) — 대표 SIP-I-0016 으로 대체 |
| SIP-A-0074 | 근중복: SIP-B-0081 (bridge 이점) + F37 서술 오류 |
| SIP-A-0076 | 타 분야(FEOL/MET) 일반론 — HBM 맥락 없음 |
| SIP-A-0077 | [R] 보도 근거·판단 태도형(STANDARDS §1 고급 금지 유형) |
| SIP-A-0142 | XD 지시: 타 분야 중복 TSV-A-0123 (mv BSP 대상) |
| SIP-A-0143 | XD 지시: 타 분야 중복 COW-A-0165 |
| SIP-A-0145 | 일반론 조합형 — 고급 기준 미달 |
| SIP-A-0146 | 일반론 — 고급 기준 미달 |
| SIP-A-0147 | 일반론(판단 태도형) |
| SIP-A-0148 | XD 지시: 타 분야 중복 WARP-A-0190/0191 |
| SIP-A-0149 | 근중복: SIP-A-0144 |
| SIP-A-0150 | 판단 태도형 일반론 |
| SIP-A-0151 | 판단 태도형 일반론 — 근중복: SIP-A-0150 |
| SIP-A-0152 | 정답 키 의심(E_EXP_REF_ANSWER)·오답 무의미 |
| SIP-A-0153 | FACT F36 오류 |
| SIP-A-0154 | 근중복: SIP-B-0081 |
| SIP-A-0155 | 근중복: SIP-B-0079 |
| SIP-A-0156 | 근중복: SIP-B-0150 |
| SIP-A-0157 | 근중복: SIP-B-0107 |
| SIP-A-0158 | 인과 서술 모호 — 품질 미달 |
| SIP-A-0159 | 일반론·오답 형식적 |
| SIP-A-0160 | XD 지시: 타 분야 중복 COW-A-0078 |
| SIP-A-0161 | 근중복: SIP-B-0137 |
| SIP-A-0162 | 판단 태도형 일반론 |
| SIP-A-0163 | 타 분야(WARP) 일반론·오답 형식적 |
| SIP-A-0164 | 타 분야(BSP/WARP) |
| SIP-A-0165 | 근중복: SIP-A-0144, WARP 소관 |
| SIP-A-0167 | 근중복: SIP-I-9002 |
| SIP-A-0168 | FACT F36 계열(유기 인터포저 변형 증가 전제) — 판단 근거 불확실 |
| SIP-A-0169 | 일반론·오답 기술 외 사유 |
| SIP-A-0171 | 인과 서술 모호 |
| SIP-A-0172 | 근중복: SIP-I-0146 |
| SIP-A-0173 | 근중복: SIP-A-0166 |
| SIP-A-0175 | 일반론 — 근중복: SIP-A-0166 |
| SIP-A-0177 | 오답 무의미·일반론 |
| SIP-A-0179 | FACT F36 계열 — 근거 불확실 |
| SIP-A-0180 | FACT F36 계열 — 근거 불확실 |
| SIP-A-0181 | 타 분야(FA) 일반론 |
| SIP-A-0183 | 오답 기술 외 사유(보관·색상·포장) |
| SIP-A-0184 | 근중복: SIP-I-0165 |
| SIP-A-0185 | FACT F13 (775 µm 규격 근거) + 일반론 |
| SIP-A-0186 | 타 분야(COW) 일반론 |
| SIP-A-0187 | 공법 우열 단정 — 출처 없음(X-F6 근거 범위 밖), XD mv COW 대신 삭제 |
| SIP-A-0188 | 공법 우열 단정 — 출처 없음 |
| SIP-A-0189 | 타 분야(COW) — 일반론 |
| SIP-A-0190 | FACT F13 (775 µm 규격 근거) + 수치 단순 |
| SIP-B-0024 | 정답 근거 결함(면적 상한을 배치 개수로 오답 처리, NUM) + 가족 초과(2.3) — SIP-I-0082 로 대체 |
| SIP-B-0068 | 타 분야 중복: PROD-B-0003 (n-Hi 의미) |
| SIP-B-0070 | 근중복: SIP-B-0085 (HBM·SoC 높이 정합) |
| SIP-B-0071 | 사실 불확실(저단수 dummy die 목적) + 타 분야(PROD/COW) |
| SIP-B-0072 | 타 분야 중복: FA-B-0096 등 (MSL floor life) |
| SIP-B-0073 | 근중복: SIP-B-0103 (Si interposer CTE 정합) |
| SIP-B-0086 | XD 지시: SIP-B-0150 으로 통합 |
| SIP-B-0087 | 사실 불확실(dummy die) + 근중복: SIP-B-0071 |
| SIP-B-0088 | 타 분야(COW/BUMP 접합 간극) — 품질 미달(ctx 무관·해설 번호 나열) |
| SIP-B-0089 | 타 분야(COW/BUMP 접합 간극) — 품질 미달 |
| SIP-B-0090 | XD 지시: 타 분야 중복 COW-B-0056 |
| SIP-B-0091 | XD 지시: 타 분야 중복 COW-B-0057 |
| SIP-B-0092 | 타 분야 중복: COW 열이력 문항(COW-I-0145 등) |
| SIP-B-0093 | 타 분야 중복: COW-I-0166/0167 (일괄 접합) |
| SIP-B-0094 | XD 지시: 타 분야 중복 COW-I-0167 |
| SIP-B-0095 | 품질 미달(용어 정의 수준, 오답 무의미) |
| SIP-B-0096 | 타 분야 중복: PROD-I-0001/0005 (단수와 용량) |
| SIP-B-0097 | 근중복: SIP-B-0102 (인터포저 역할) |
| SIP-B-0098 | XD 지시: 타 분야 중복 PROD-B-0049 |
| SIP-B-0099 | 사실 불확실("마지막까지 wafer 단위 공정=전기검사") + XD 지시 SIP-I-0129 와 동일 주제(PROD-B-0050 보유) |
| SIP-B-0100 | XD 지시: 타 분야 중복 PROD-I-0033 |
| SIP-B-0101 | 일반론 요약형(판단 태도) + XD 지시 SIP-I-0130 과 같은 주제(PROD-B-0061 보유) |
| SIP-B-0104 | 근중복: SIP-B-0080 (reticle 제약) |
| SIP-B-0105 | 근중복: SIP-B-0081 (bridge 이점) |
| SIP-B-0106 | 근중복: SIP-B-0075 (substrate 역할) |
| SIP-B-0108 | 근중복: SIP-B-0084 (C4 underfill) |
| SIP-B-0109 | 근중복: SIP-B-0152 (휨 억제 보강) |
| SIP-B-0110 | 근중복: SIP-B-0076 (BGA) |
| SIP-B-0111 | 근중복: SIP-B-0082 (HBM 근접 배치) |
| SIP-B-0115 | 근중복: SIP-B-0085 (높이 정합) |
| SIP-B-0116 | 타 분야(PROD) 일반 상식 — 품질 미달 |
| SIP-B-0117 | 근중복: SIP-B-0082 |
| SIP-B-0118 | 일반론·오답 무의미 — 품질 미달 |
| SIP-B-0119 | 일반론("관리 항목이 많아서") — 품질 미달 |
| SIP-B-0120 | 근중복: SIP-B-0102 |
| SIP-B-0121 | 근중복: SIP-B-0081 |
| SIP-B-0122 | 타 분야(PROD) 일반론 — 품질 미달 |
| SIP-B-0123 | 타 분야(PROD) 일반론 — 근중복: SIP-B-0122 |
| SIP-B-0124 | 일반론 상충 문항 — 품질 미달 |
| SIP-B-0125 | 일반론(비용) — 품질 미달 |
| SIP-B-0126 | 일반론("선택지를 주려고") — 품질 미달 |
| SIP-B-0127 | 타 분야(COW) 일반론 — 품질 미달 |
| SIP-B-0128 | 근중복: SIP-I-0137 (스택 PDN) |
| SIP-B-0129 | 근중복: SIP-B-0136 (RDL 인터포저 명칭) |
| SIP-B-0130 | 근중복: SIP-B-0137 (CoWoS-R 장점) |
| SIP-B-0131 | FACT F36 오류(팽창률 차이를 한계로 정답화) + 근중복: SIP-B-0138 |
| SIP-B-0132 | 근중복: SIP-B-0136 + 지문 미완(W_STEM_NO_QMARK) |
| SIP-B-0133 | 정답 키 의심(E_EXP_REF_ANSWER)·오답 무의미 — 품질 미달 |
| SIP-B-0134 | 근중복: SIP-B-0001 (Si interposer 명칭) |
| SIP-B-0135 | 근중복: SIP-B-0079 (interposer TSV) |
| SIP-B-0139 | 근중복: SIP-B-0004 (CoWoS-L 명칭) |
| SIP-B-0141 | 근중복: SIP-B-0081 |
| SIP-B-0143 | 근중복: SIP-B-0002 (EMIB 전원 경로) |
| SIP-B-0145 | 근중복: SIP-B-0081 |
| SIP-B-0146 | 근중복: SIP-B-0107 (C4 크기) |
| SIP-B-0147 | 인과 서술 모호(열전도와 두께) — 품질 미달, 신규 열 결합 문항으로 대체 |
| SIP-B-0148 | XD 지시: 타 분야 중복 COW-A-0078 |
| SIP-B-0149 | 근중복: SIP-B-0082 |
| SIP-B-0153 | 일반론 — 품질 미달 |
| SIP-B-0155 | 근중복: SIP-B-0010 (EMIB-T 명칭) |
| SIP-B-0156 | 근중복: SIP-I-0002 (EMIB-T 효과) |
| SIP-B-0157 | 근거 없는 주장(20단 이상 과제) — 사실 불확실 |
| SIP-B-0158 | 근중복: SIP-B-0137/SIP-B-0159 |
| SIP-B-0160 | 타 분야(PROD) 중복: SIP-B-9001(mv PROD) |
| SIP-B-0161 | 타 분야(PROD) 중복: SIP-B-9001 + E_CALC_NO_WORK |
| SIP-B-0162 | 출처 없는 수치(55→32.5 µm) |
| SIP-B-0163 | FACT F13 (775 µm 규격 근거) + 출처 없는 25 µm |
| SIP-B-0164 | 타 분야(BSP/COW) 일반론 |
| SIP-B-0166 | 타 분야 중복: FA (MSL) — 비표준 용어("MSL 라이프") |
| SIP-B-0167 | 타 분야(COW) — 품질 미달(발문 비문) |
| SIP-B-0168 | 근중복: SIP-B-0150 |
| SIP-B-0169 | 일반론 상충 — 품질 미달 |
| SIP-B-0170 | 일반론 — 품질 미달 |
| SIP-B-0171 | FACT F36 오류(유기 인터포저 팽창 부담) + 근중복: SIP-B-0137 |
| SIP-B-0172 | 근중복: SIP-A-0144 (승온 warpage 궤적), WARP 소관 |
| SIP-B-0173 | FACT F26 조건부([V-2차]) 업체 수치 회상형 + COW 소관 — 유지 가치 낮음 |
| SIP-B-0174 | 타 분야(THERM) 일반론 |
| SIP-B-0175 | FACT F13 사용 금지(720→775 완화를 규격 사실로 정답화) |
| SIP-I-0083 | 정답 근거 결함(면적 상한을 배치 개수로 오답 처리, NUM) + 가족 초과(2.3) — SIP-I-0082 로 대체 |
| SIP-I-0126 | XD: 타 분야 중복 TSV-A-0123/BSP (stress relief) |
| SIP-I-0127 | 근중복: SIP-A-0144 (승온 휨 궤적), WARP-A-0190 소관 |
| SIP-I-0128 | 타 분야 중복: PROD (단수 확대와 두께) |
| SIP-I-0129 | XD 지시: 타 분야 중복 PROD-B-0050 |
| SIP-I-0130 | XD 지시: 동일 문항 PROD-B-0061 |
| SIP-I-0131 | XD 지시: 타 분야 중복 PROD-I-0036 |
| SIP-I-0132 | 타 분야(COW) 일반론 — 오답 기술 외 사유 |
| SIP-I-0133 | 타 분야 중복: COW 열이력 문항 |
| SIP-I-0134 | XD 지시: 타 분야 중복 COW-B-0050 |
| SIP-I-0135 | 타 분야(TSV/BSP) 일반론 |
| SIP-I-0136 | FACT F36 오류(열팽창 차이를 단점으로 정답화) + 근중복: SIP-B-0137/0138 |
| SIP-I-0138 | 정답 키 의심(E_EXP_REF_ANSWER)·오답 무의미 |
| SIP-I-0139 | FACT F36 오류(팽창률 차이로 신뢰성 불리) |
| SIP-I-0140 | 근중복: SIP-B-0080 |
| SIP-I-0141 | 일반론·오답 형식적 — 품질 미달 |
| SIP-I-0143 | 근중복: SIP-B-0079 |
| SIP-I-0144 | FACT F37 오류(CoWoS-R 수직 연결을 "기판이 담당") — SIP-I-0013 으로 정정 통합 |
| SIP-I-0145 | FACT F36 오류 — SIP-I-0014 로 정정 통합 |
| SIP-I-0147 | 근중복: SIP-I-0001 |
| SIP-I-0149 | 근중복: SIP-B-0002 (EMIB 전원 경로) |
| SIP-I-0150 | 근중복: SIP-B-0081 |
| SIP-I-0151 | 근중복: SIP-I-0146 (LSI 정렬) |
| SIP-I-0152 | 근중복: SIP-B-0154 (SiP 열이력) |
| SIP-I-0154 | 근중복: SIP-B-0107 (C4 크기) |
| SIP-I-0155 | 일반론·오답 기술 외 사유 |
| SIP-I-0156 | 일반론·오답 기술 외 사유 |
| SIP-I-0157 | 일반론 — 품질 미달 |
| SIP-I-0159 | 인과 서술 모호 — 품질 미달 |
| SIP-I-0160 | 일반론("여러 항목이 함께 걸려서") — 판단 태도형 |
| SIP-I-0161 | 오답 무의미(타 분야 항목 나열) |
| SIP-I-0162 | FACT F13 + 일반론 |
| SIP-I-0163 | 오답 기술 외 사유(보관·색상·포장) |
| SIP-I-0164 | 근중복: SIP-I-9003 (interposer decap) |
| SIP-I-0166 | FACT F13 + 근중복: 높이 가족 |
| SIP-I-0167 | 발문 비문·일반론 |
| SIP-I-0168 | 일반론·오답 기술 외 사유 |
| SIP-I-0169 | 근중복: SIP-A-0144 |
| SIP-I-0170 | 근중복: SIP-I-0153 |
| SIP-I-0171 | 근중복: SIP-I-9002 (bridge 매립 산포) |
| SIP-I-0172 | 타 분야(COW) — 근중복: SIP-A-0043 |

## 난이도 변경 · id 재발급
| 옛 id | 새 id | 이유 |
|---|---|---|
| SIP-A-0003 | SIP-B-9001 | die·간극·pad 수 세기는 인지 수준(초급). XD 지시로 mv PROD |
| SIP-A-0075 | SIP-I-9001 | HCB CMP 기준 이유 — 단일 원리 판단(중급). mv COW |
| SIP-A-0174 | SIP-I-9002 | bridge 매립 산포→pad 높이 — 단일 인과(중급) |
| SIP-A-0182 | SIP-I-9003 | interposer decap 효과 — 단일 원리(중급) |

## 이관 제안 (mv)
| id | 대상 분야 | 이유 |
|---|---|---|
| SIP-B-9001 (← A-0003) | PROD | 스택 구성 수(XD §2: 단수 구성은 PROD 소관) |
| SIP-B-0069 | PROD | 8-Hi/12-Hi 용량·대역폭(XD §3) |
| SIP-B-0165 | COW | MR-MUF 충전(XD §3) |
| SIP-I-9001 (← A-0075) | COW | HCB 접합면 CMP(XD §3) |
| SIP-I-0158 | MET | SiP 전 KGSD 선별 근거(XD §3) |
- XD 가 mv COW 로 제안한 SIP-A-0187 은 공법 우열 단정의 출처가 없어 삭제(위 표).

## 면제(vx) 목록
| id | 코드 | 사유 |
|---|---|---|
| SIP-A-0043 | W_FIG_LEAK | 후보 설계표(f_table)의 한 행이 곧 보기 — 표는 4 후보를 모두 같은 형식으로 보여 줘 정답을 가리키지 않음 |
| SIP-A-9008 | W_FIG_LEAK | 대책 후보표 — 위와 같음 |
| SIP-A-9017 | W_FIG_LEAK | 대책 후보표 — 위와 같음 |
| SIP-A-9032 | W_FIG_LEAK | EMIB/EMIB-T 저항표 — 두 구조를 동등하게 제시 |
| SIP-I-9018 | W_OPT_LONGEST | 기호(≈, >) 포함 물성 조합 보기라 글자 수가 부풀려짐; 오답도 같은 형식 |
| SIP-A-9040 | W_OPT_ODD_END | 판정(채택/기각) 보기라 정답만 "기각" 으로 끝나는 것이 불가피 |

## 남은 우려 · EA/DA 에 요청
- **규모**: 537 → 140. 계산 가족·반복 개념 정리 결과이며 신규 목표(B10/I30/A30)는 충족(B12/I31/A32). 고급 비율 29 % 로 권장(30–35 %) 하한에 약간 못 미침.
- **수치 조건의 출처**: 신규 고급의 I/O 에너지(pJ/bit), bump·TSV 허용 전류, 경로 저항·인덕턴스, 휨 흡수 한도 등은 "설계 조건/사내 기준" 으로 지문에 명시한 가정값입니다(정답 근거가 업체 수치가 아님). EA 표본 판독 시 현실 범위 확인 요청.
- **HBM3E 9.6 Gb/s**(A-9018)는 "업체 사양 가정" 으로 명시했고 `src` 에 기록. CoWoS-L 5.5×(A-9030 해설)는 F34 [V] "계획" 으로 표기.
- **f_stack k=1 + hideResult 에서 `h_um` 키**: 지문에 "높이" 가 있으면 `h_um` 부재가 E_K1_FIG_NUM 으로 잡혀, 숨겨진 칸에 상한값(775)을 넣어 통과시켰습니다(그림에는 "?" 로 표시). validate 가 hideResult 일 때 h_um 기본값을 문제 삼지 않도록 EA 검토 요청.
- **STANDARDS 2.5 조사 사전의 "hbm: 받침 없음"**: 독음(에이치비엠)과 맞지 않아 "HBM 이/은" 을 쓸 수 없습니다. 이번에는 "HBM 스택이" 등으로 우회했으나 사전 수정 검토 요청.
- f_sip 의 `msg` 신규 param 이 validate FIG 스키마(keys)에 없어 쓰면 W_FIG_UNKNOWN_KEY 가 납니다 — 필요하면 EA 가 스키마에 추가.
- 받을 이관 문항(COW-I-0188, FEOL-A-0018, FEOL-B-0035, FEOL-B-0042)은 W3 에서 중복 재확인 필요.
