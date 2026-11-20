# 사실 검증 결과 (FACT) — 2026-11-20

- 작성: FACT (W1 지원, 읽기 전용). 대상: `data/*.json` 5,000 문항, 검사기 `I_FACT_WATCH` 350건 + 브리프 "사실 검증 필요" + 업체 고유 주장 전수 탐색(정규식 → 문장 판독).
- 판정: **확인** / **정정**(올바른 값 제시) / **사용 금지**(출처 없음 또는 [R] 뿐 — 정답 근거로 쓰지 말 것) / **조건부**(주장 자체는 [V] 이나 표현을 고쳐야 정답 근거가 됨).
- 등급: [S] 표준 문서(원문 또는 JEDEC 공식 발표문) · [V] 제조사 공식(보도자료·학회 논문·학회 발표) · [R] 언론·분석.
- **접근 한계(정직하게 밝힘)**: jedec.org · businesswire 는 이 환경에서 403 이라 JEDEC 보도자료는 원문 전재본(HPCwire, StorageNewsletter)으로 읽었습니다. **JESD270-4 / JESD238 / JESD235 본문(패키지 외형·높이 표)은 열람하지 못했습니다.** JESD47 은 **JESD47G 원문 PDF** 의 Table 을 직접 확인했습니다(현행 최신판과 수치가 다를 수 있음 — EA 가 최신판으로 재확인 권장). SK hynix Hot Chips 2026 발표는 슬라이드 원문이 아니라 ServeTheHome 의 슬라이드 인용 기사로 확인했습니다.
- 해설 끝 `[근거] …` 꼬리표(1,479 문항)는 대부분 [R] 2차 매체(Tom's Hardware, Electronics Cooling, Siemens EDA 블로그, AllAboutCircuits 등)이며 문항별 근거가 아닙니다. `src` 로 옮기지 말고, 아래 표의 [S]/[V] 출처를 쓰십시오.

## 0. 요약


- 검증한 주장 **47 건**(같은 주장이 반복된 문항을 묶음).
- **확인 24 건 · 정정 13 건 · 사용 금지(출처 없음/[R] 뿐) 5 건 · 조건부(표현 수정 시 사용 가능) 5 건.**
- 정정 대상 문항(중복 제거) **536 문항** — 이 중 내용(지문·보기·정답) 수정이 필요한 문항은 **118 문항**이고, 나머지는 해설 꼬리표 제거(F15, 282 문항)와 `f_rel` 그림 기본값(F42, 140 문항 — template 측 수정 1건으로 해소)입니다, 사용 금지 대상 **242 문항**(F13 은 높이 775 µm 를 쓰는 전 문항 — 계산 조건으로 바꾸면 유지 가능, "JEDEC 규격" 어휘 동반 51 문항이 우선), 조건부 **82 문항**.
- 가장 무거운 오류: ① F04 "HBM4 는 HBM3 컨트롤러와 비호환"(JEDEC 공식 발표와 정반대) ② F36·F37 CoWoS-R/L 의 CTE·수직 경로 서술(TSMC 공식 설명과 반대) ③ F40 preconditioning 규격 번호 ④ F08·F09 실재하지 않는 HBM 구성·속도 ⑤ F32 HCB die 휨 100 nm.
- STANDARDS 자체 정정 제안 6 건(§9).


## 1. 세대 사양 (JEDEC)

| # | 주장 | 판정 | 출처 등급 · 출처 | 문항 수 |
|---|---|---|---|---|
| F01 | HBM4 = 2,048 bit/스택, 독립 채널 32 × 64 bit, 채널당 pseudo channel 2개(64 PC) | 확인 | [S] JEDEC JESD270-4 보도자료 2025-04-16 ("32 channels with 2 pseudo-channels per channel", "2048-bit interface") | 55 |
| F02 | HBM4 JEDEC 최대 8 Gb/s, 스택 ≈ 2 TB/s | 확인 | [S] 동 보도자료 ("transfer speeds up to 8Gb/s … up to 2TB/s") | 7 |
| F03 | HBM4 4/8/12/16-Hi, 24·32 Gb die, 최대 64 GB(32 Gb×16), VDDQ 0.7/0.75/0.8/0.9 V·VDDC 1.0/1.05 V | 확인 | [S] 동 보도자료 | 4 |
| F04 | **HBM4 는 HBM3 컨트롤러와 호환되지 않는다** | **정정** → JESD270-4 는 "existing HBM3 controllers 와 backwards compatible, 한 컨트롤러로 HBM3·HBM4 모두 구동 가능"을 명시. 문항 전제·정답 근거가 틀림 → 재출제(예: "폭이 2배가 되어도 호환이 유지되는 방식" 또는 PHY 배선 수 증가가 중간 기판에 주는 영향) | [S] 동 보도자료 "Compatibility and Flexibility" | 1 |
| F05 | HBM3(JESD238, 2022-01): 6.4 Gb/s, 819 GB/s, 16 채널 × 64 bit, 32 pseudo channel, 8–32 Gb die, 4–64 GB, VDD 1.1 V, I/O 0.4 V swing | 확인 | [S] JEDEC JESD238 보도자료 2022-01-27(HPCwire 전재) | 2 |
| F06 | HBM3 의 지원 단수 "4/8/12/16-Hi" | **정정** → JESD238 발표 기준 4/8/12-Hi, **16-Hi 는 "future extension" 조항**. 16-Hi HBM3 를 "JEDEC 규격 지원"으로 출제하지 말 것(STANDARDS 표 정정 제안 §4-1) | [S] 동 보도자료 | 0 |
| F07 | HBM3E 는 별도 JEDEC 세대가 아님; 업체 핀 속도 9.2(Micron)·9.6(SK hynix 12H)·9.8(Samsung) Gb/s, 1.2–1.28 TB/s; 8-Hi 24 GB / 12-Hi 36 GB(24 Gb die) | 확인(업체 발표 기준). 단, JEDEC 이 JESD238A(2023) 등 개정판에서 상위 속도를 넣었는지는 **본문 미확인** → "HBM3E = JEDEC 규격 아님" 을 정답으로 묻는 문항은 만들지 말 것 | [V] Samsung 36GB HBM3E 12H 보도자료(2024-02, 1,280 GB/s), Micron·SK hynix HBM3E 보도자료 | 56 |
| F08 | "HBM3E 계열" 1,024 bit 스택이 5.6·6.4·7.2 Gb/s 또는 10.4–12.8 Gb/s 로 동작 | **정정** → 업체 발표 HBM3E 는 약 8–10 Gb/s(최고 Samsung 12H 1,280 GB/s ≈ 10 Gb/s). 범위 밖 값은 "HBM3E" 이름을 떼고 "가상의 1,024 bit 스택" 으로 바꾸거나 8.0/9.2/9.6/9.8 Gb/s 로 교체 | [V] 위 업체 보도자료 | 21 |
| F09 | "HBM 스택" 이 512·4,096 bit, 또는 2,048 bit × 4/8/16/64 채널, 1,024 bit × 4/32/64 채널 등으로 구성 | **정정** → 실재 구성은 1,024 bit × 8 ch(HBM2/2E), 1,024 × 16(HBM3/3E), 2,048 × 32(HBM4) 뿐. STANDARDS 2.2 금지 사항 그대로 위반 → "가상의 메모리 인터페이스" 로 명시하거나 실제 구성으로 교체 | [S] JESD235/238/270-4 | 49 |
| F10 | HBM2E(JEDEC 명칭은 HBM2, JESD235C): 3.2 Gb/s, 8 ch × 128 bit, pseudo channel 16 × 64 bit, 최대 12-Hi·24 GB(16 Gb die); 업체 3.6 Gb/s | 확인. 다만 "HBM2E" 는 업계 통칭이고 JEDEC 문서명은 HBM2(JESD235C) — "JEDEC HBM2E 규격" 으로 쓰지 말 것 | [S] JEDEC JESD235C 발표(2020-01, AnandTech 표 경유) · [V] SK hynix 3.6 Gb/s HBM2E | 0 |
| F11 | SIP 문항의 "HBM 스택과 XPU 사이에는 2,048개의 데이터 선" (세대 미표기) | **정정** → 2,048 은 HBM4 에만 해당, HBM3E 이하는 1,024. 지문에 "HBM4 기준" 명시 필요(템플릿 `f_sip` 의 "2,048선" 고정 라벨과 같은 문제) | [S] JESD270-4 / JESD238 | 31 |

## 2. 패키지 높이 (720 / 775 µm)

| # | 주장 | 판정 | 출처 등급 · 출처 | 문항 수 |
|---|---|---|---|---|
| F12 | 720 µm = HBM 패키지 높이(8/12-Hi) | **조건부 확인** → [V] Samsung 2019: 12단 3D-TSV 패키지가 8단 HBM2 와 같은 **720 µm**. HBM3/3E 의 "JEDEC 720 µm" 은 보도([R])로만 확인, 규격 원문 미확인. Samsung HBM3E 12H 는 "8H 와 같은 높이 규격"(수치 없음, [V]). → 지문에서 "JEDEC 규격 상한" 대신 "업계 표준 패키지 높이 720 µm(설계 조건)" 로 쓰면 사용 가능 | [V] Samsung Newsroom 2019-10-07 · [V] Samsung 36GB HBM3E 12H 2024-02 · [R] TechPowerUp/TrendForce | 58 |
| F13 | 775 µm = HBM4 패키지 높이 규격 상한(12·16-Hi), HBM3E 720 → HBM4 775 로 완화 | **조건부 / JEDEC 값으로는 사용 금지** → JESD270-4 공식 발표문에 높이 언급 없음. 근거는 ZDNet Korea→TrendForce·TechPowerUp 보도(2024-03, [R])와 SK hynix Hot Chips 2026 슬라이드의 "HBM4 12.8×11 mm, 775 µm Z-height"(제품 치수, 2차 기사 경유). JESD270-4(또는 4A) 본문 확인 전까지 "JEDEC 규격 상한 775 µm" 를 정답 근거로 쓰지 말고, 계산 문항은 "높이 상한(설계 조건) 775 µm" 로 주어진 조건화하면 유지 가능. **PROD-B-0107**("HBM4 규격에서 720→775 완화" 를 정답으로 묻는 문항)은 원문 확인 전 사용 금지 | [R] TrendForce 2025-04-21, TechPowerUp 2024-03-13 · [V-2차] SK hynix Hot Chips 2026 (ServeTheHome) | 184 |
| F14 | HBM4E 세대에서 패키지 높이를 약 900 µm 로 추가 완화 검토 | **사용 금지** — [R] 만 존재(TrendForce·Chosun 2026-03/04 "825–900 µm 논의"). JEDEC·업체 공식 발표 없음 | [R] TrendForce 2026-03-06, 2026-04-01 | 1 |
| F15 | 해설 꼬리표 "Hot Chips 2026 SK hynix 발표 정리 (775 µm **한계**·HB 로드맵)" | **정정** → 해당 발표는 775 µm 를 HBM4 제품 Z-height 로 제시했을 뿐 "한계(규격 상한)" 로 제시하지 않음(2차 기사 기준). 꼬리표 제거(STANDARDS 2.1 방침과 동일) | [V-2차] ServeTheHome | 282 |

## 3. 업체 고유 수치 (모두 "업체 발표 기준" 으로 지문에 명시해야 함)

| # | 주장 | 판정 | 출처 등급 · 출처 | 문항 수 |
|---|---|---|---|---|
| F16 | SK hynix HBM4: I/O 2,048, 전력 효율 40 % 이상 개선, 10 Gb/s 이상(JEDEC 8 Gb/s 초과), Advanced MR-MUF, 1b(10 nm급 5세대) | 확인 | [V] SK hynix 보도자료 2025-09-12 (HBM4 개발 완료·양산 체제) | 4 |
| F17 | PROD-B-0124 해설 "JEDEC 규격 핀 속도는 **하한선**" | **정정** → JESD270-4 의 8 Gb/s 는 "up to 8 Gb/s", 즉 규격이 정의한 **최대** 속도. 업체 제품(10–11.7 Gb/s)은 규격 정의 범위를 넘는 업체 사양. 정답 보기(규격 8, 실제 10 이상)는 확인 | [S] JESD270-4 발표 · [V] Samsung 2026-02-12(11.7 Gb/s), SK hynix 2025-09-12 | 1 |
| F18 | Samsung HBM4: core 1c(10 nm급 6세대), base die 자사 파운드리 4 nm 로직, 11.7 Gb/s(최대 13) | 확인 | [V] Samsung Newsroom 2026-02-12 "Samsung Ships Industry-First Commercial HBM4" | 2 |
| F19 | ISSCC 2026 공개 12단 HBM4 스택 대역폭 3 TB/s 급 | 확인 — Samsung ISSCC 2026 논문(36 GB 12-Hi, 2,048 I/O, 3.3 TB/s). 지문에 "Samsung 발표" 명시 권장 | [V] ISSCC 2026 Samsung HBM4 논문(SemiAnalysis·Wccftech 요약 경유) | 1 |
| F20 | HBM4 12단 제품 용량 = HBM3E 12단과 같은 36 GB | 확인(24 Gb die 제품 기준; 규격상 32 Gb die 12단 48 GB 도 가능하므로 "현재 양산 제품 기준" 명시) | [V] Samsung ISSCC 2026 36 GB 12-Hi · [S] JESD270-4 | 1 |
| F21 | Samsung HBM4E(GTC 2026 최초 공개): 16 Gb/s, 4.0 TB/s | 확인 — 단 **목표치**. 2026-05-29 샘플 출하 발표는 "안정 14 Gb/s, 최대 16 Gb/s, 최대 3.6 TB/s, 12단 48 GB". PROD-B-0129 는 "최대" 를 지문에 넣을 것 | [V] Samsung Newsroom 2026-03-16(GTC), 2026-05-29(HBM4E 샘플) | 2 |
| F22 | SK hynix HBM4E 12단 샘플: 최대 16 Gb/s, 48 GB, Advanced MR-MUF, 전력 효율 20 % 이상↑ | 확인 | [V] SK hynix 보도자료 2026-06-18 (PRNewswire) | 1 |
| F23 | Samsung 이 GTC 2026 에서 밝힌 HCB 열저항 개선 = "TC 본딩 대비 **최대** 20 %" | **정정** → Samsung 발표는 "열저항 **20 % 이상** 개선(TCB 대비), 16단 이상 적층 가능". 정답 보기를 "20 % 이상 개선" 으로 수정 | [V] Samsung Newsroom KR 2026-03-16 "삼성전자 GTC서 HBM4E 최초 공개" | 1 |
| F24 | Samsung HBM3E 12H: TC NCF 박막화로 칩 간 간격 7 µm, 8H 와 같은 높이에서 수직 집적도 20 % 이상↑, 1,280 GB/s | 확인 | [V] Samsung Newsroom 2024-02-27 | 2 |
| F25 | SK hynix iHBM: ICE(전기 절연·고열전도 Si 계 소재)를 D2D PHY 영역에 집적, 기존(코어 die 경유 방열) 대비 열저항 30 % 저감, MR-MUF 기반 WLP 로 구현, HBM5 부터 적용 계획 | 확인. 발표 수치는 "30 %"(국내 보도 "30 % 이상") — 보기 "30 % 이상 저감" 은 허용 범위. 적용 시점(HBM5) 을 지문에 넣으면 오해 방지 | [V] SK hynix 보도자료 2026-05-25 (iHBM) | 7 |
| F26 | SK hynix: 하이브리드 본딩은 20단 이상(≥20Hi) 에서 필요, HB 시 bump pitch 18 µm 미만(MR-MUF 로 불가), 같은 Z-height 에서 core die 를 더 두껍게·열저항 낮게 | **조건부 확인** — 학회 발표([V]) 이나 슬라이드 원문 미열람, 2차 기사(ServeTheHome)로만 확인. 18 µm 가 bump pitch 인지 TSV pitch 인지 매체 간 불일치(STH 는 bump pitch). `src: Hot Chips 2026 SK hynix` 를 달고 지문에 "SK hynix 발표 기준" 명시 | [V-2차] Hot Chips 2026 SK hynix 발표(ServeTheHome 2026-08) | 3 |
| F27 | HBM4 base die 를 로직 공정으로: 한 회사는 외부 파운드리 12 nm, 다른 회사는 자사 4 nm | **조건부** → Samsung 자사 4 nm 는 [V]. "외부 파운드리 12 nm" 는 TSMC 가 HBM4 base die 용 N12FFC+·N5 를 제공한다고 발표한 것([V])까지만 확인되고, SK hynix 의 실제 채택 노드는 공식 발표 없음([R]). Micron 은 HBM4 = 자사 CMOS base die, HBM4E 부터 TSMC 제조([V] 실적 발표, 2차 경유). 지문을 "TSMC 는 12 nm·5 nm 급 base die 공정을 제공한다고 발표" 로 바꾸면 사용 가능 | [V] TSMC 2024 European Technology Symposium · [V] Samsung 2026-02-12 · [V-2차] Micron FQ4'25 실적 발표 | 1 |

## 4. 접합 공법 (MR-MUF / TC-NCF / HCB)

| # | 주장 | 판정 | 출처 등급 · 출처 | 문항 수 |
|---|---|---|---|---|
| F28 | HBM4 세대 양산 주력은 µbump 기반 기존 공법, HCB 는 차세대 후보 | 확인. 단 **PROD-B-0109 정답 보기 "기존 열압착 계열 방식" 은 정정** → SK hynix 의 Advanced MR-MUF 는 일괄 리플로(mass reflow) 기반이므로 "열압착 계열" 로 통칭할 수 없음 → "기존 µbump 접합 방식(TC-NCF·MR-MUF)" 으로 수정 | [V] SK hynix 2025-09-12(MR-MUF), Samsung TC NCF(2024-02) · [R] Semiconductor Engineering "HBM4 Sticks With Microbumps" | 2 |
| F29 | MR-MUF = SK hynix, TC-NCF = Samsung·Micron | 확인(SK hynix·Samsung 은 [V]; Micron 의 TC-NCF 채택은 [R] 수준 → 정답 근거로는 Samsung 만 쓸 것) | [V] SK hynix·Samsung 보도자료 · [R] Micron | 1 |
| F30 | MR-MUF 의 방열 우위 근거 = 고열전도 EMC + 더 많은 thermal dummy bump | 확인 — SK hynix: TC-NCF 대비 thermal dummy bump 최대 4배, Advanced MR-MUF EMC 방열 특성 1.6배(기존 MR-MUF EMC 대비); ECTC 2023 SK hynix 논문: 동일 조건 Tj 14 °C 낮음. COW-B-0106 해설에 두 근거를 명시(브리프 요구) | [V] SK hynix Newsroom "MR-MUF unlocks HBM heat control" · [V] ECTC 2023 (SK hynix) | 1 |
| F31 | TC-NCF = die 별 하중·온도 정밀 제어, MR-MUF = 일괄 리플로로 생산성 유리 | 확인(공법 원리 + SK hynix 설명: TC-NCF 는 접합 압력 때문에 bump 수 증가에 한계) | [V] ECTC 2023 SK hynix | 2 |
| F32 | HCB 는 접합 전 die 휨 100 nm 미만 요구, µbump 는 수 µm 허용(약 100배 차이) | **사용 금지(출처 없음)** → 공개 자료에서 HBM HCB 용 die 휨 허용치를 100 nm 로 제시한 [S]/[V] 를 찾지 못함. 공개 비교(KLA, TechSearch/DARPA 2025)는 HB die 휨을 **µm 급(약 10–20 µm 대 µbump 60–100 µm)** 으로 제시하고, imec IITC 2025 는 허용 휨이 접합 방식·가압력에 좌우된다고 보고. nm 급 요구는 표면 거칠기(Ra ≲ 0.5–1 nm)·Cu recess(수 nm) 에 해당 → 문항을 "표면 평탄도·Cu recess" 로 바꾸거나 "가정" 으로 명시 | [R] TechSearch (DARPA NGMM 2025-12 발표), imec IITC 2025 초록 | 1 |
| F33 | 현행 HBM die 간 접속 피치 "20 µm 안팎"(자릿수 문항) | **불확실** → 정확한 양산 µbump 피치의 [V] 공개값 없음(업계 통념 25–55 µm; SK hynix Hot Chips 2026 은 16-Hi 에서 bump pitch 를 대략 절반으로 줄였다고만 언급). 자릿수(2 / 20 / 200 µm) 판별용으로는 성립하나 "20 µm" 를 확정값처럼 쓰지 말고 "수십 µm" 로 표기 권장 | [R]/[V-2차] | 1 |

## 5. 중간 기판 · CoWoS

| # | 주장 | 판정 | 출처 등급 · 출처 | 문항 수 |
|---|---|---|---|---|
| F34 | reticle(1회 노광 면적) ≈ 26 × 33 mm = 858 mm²; CoWoS-S 최대 3.3× reticle(≈ 2,700 mm²); CoWoS-L 3.5× 양산(2024), 5.5× 2026 양산 예정 | 확인 | [V] TSMC 3DFabric CoWoS 페이지, TSMC HPC WLSI 페이지 | 59 |
| F35 | HBM 탑재 수: 전면 Si ≈ 8, 유기 RDL 4–6, 브리지 12개 이상 | **부분 사용 금지** → TSMC 는 CoWoS 유형별 HBM 탑재 상한을 공식 발표하지 않음. 제품 사례로는 Si 인터포저 8 stack(AMD MI300X, CoWoS-S, [V]), CoWoS-L 8 stack(NVIDIA B200, [V]/[R]) 정도만 확인. "유기 RDL 4–6" 은 출처 없음, "브리지 12+" 는 로드맵 보도([R]). 수치 대신 "면적·배선 밀도가 탑재 수를 정한다" 는 원리만 묻도록 수정 | [V] AMD MI300X 사양, NVIDIA B200 사양 · [R] 보도 | 1 |
| F36 | CoWoS-R(유기 RDL 인터포저)은 die·기판과 팽창률 차이가 커서 접합 신뢰성이 불리 / 한계가 "팽창률 차이" | **정정** → TSMC 공식 설명은 반대: 폴리머+Cu RDL 인터포저가 유연해 SoC–기판 CTE 불일치의 **완충층** 역할을 하고 C4 접합부 변형 에너지를 크게 줄임(TSMC 2021 논문: TCC −65/150 °C 1,300 cycle 통과). CoWoS-R 의 한계는 **배선 피치(최소 L/S 2/2 µm)·층수** 쪽. 팽창률을 정답 근거로 쓰는 보기는 "미세 피치 한계" 로 교체 | [V] TSMC 3DFabric CoWoS-R 설명, TSMC ECTC 2021 CoWoS-R 신뢰성 논문 | 4 |
| F37 | 유기 RDL·브리지 구조는 "수직 통로가 없어" 전원이 기판을 돌아가거나 "기판이 담당" 한다; CoWoS-L 칩 간 배선은 "브리지로만" 이어진다 | **정정** → CoWoS-R 의 RDL 인터포저는 적층 via 로 전원·신호를 수직 통과시키고(TSV 불필요), CoWoS-L 은 몰딩 내 **TIV(through-insulator via)** 와 전역 RDL 을 가지며 LSI 는 국소 고밀도 구간만 담당. 기판 내장 EMIB 은 기판 via 로 전원이 바로 내려감 | [V] TSMC ECTC 2023 CoWoS-L 논문(LSI + global RDL + TIV), TSMC CoWoS-R 설명 | 3 |
| F38 | CoWoS-S·-R·-L·EMIB·EMIB-T 구조 정의(Si 전면 인터포저+TSV / RDL 인터포저 / RDL+LSI / 기판 내장 브리지 / TSV 를 가진 기판 내장 브리지) | 확인 | [V] TSMC 3DFabric · [V] Intel Foundry EMIB-T 발표(2025) | 14 |

## 6. 신뢰성 표준 (JESD22 / JESD47 / J-STD-020)

| # | 주장 | 판정 | 출처 등급 · 출처 | 문항 수 |
|---|---|---|---|---|
| F39 | 시험 번호 대응: A101 THB · A103 HTS(HTSL) · A104 TC · A108 HTOL · A110 bHAST · A118 uHAST · A113 preconditioning · J-STD-020 MSL 분류·리플로 프로파일 · JESD47 자격 시험 요구 수준 | 확인 | [S] JESD47G Table(원문 PDF) — 각 시험의 참조 문서 열 | 53 |
| F40 | "MSL preconditioning 의 규격 번호는 J-STD-020" | **정정** → preconditioning **절차**는 **JESD22-A113**, J-STD-020 은 MSL **분류**와 리플로 프로파일. 정답이 "preconditioning" 인 이름 맞히기 문항은 지문의 규격 번호를 JESD22-A113 으로 바꾸고 J-STD-020 은 "MSL 등급 판정에 쓰는 문서" 로 병기. (FA-B-0096 "MSL·개봉 후 허용 시간 = J-STD-020" 과 FA-B-0002 는 확인) | [S] JESD47G 주석("Preconditioning to JESD22A113"), PC 행 | 5 |
| F41 | JESD47 조건: HTOL Tj ≥ 125 °C·Vcc ≥ Vccmax·1,000 h·**3 lot × 77**·0 fail / HTSL ≥ 150 °C·1,000 h·3 × 25 / THB 85 °C·85 %RH·1,000 h·3 × 25 / HAST 130 °C·85 %RH·96 h(또는 110 °C·264 h) / uHAST 130 °C·85 %RH·96 h / **TC: B(−55/+125) 700 cycle, G(−40/+125) 850, C(−65/+150) 500, K(0/125) 1,500, J(0/100) 2,300**, 3 × 25, 0 fail | 확인(JESD47G 기준). 문항이 "TC condition B 1,000 cycle" 을 JEDEC 요구로 쓰면 정정(700 cycle). 1,000 cycle 은 고객·사내 기준으로 명시 | [S] JESD47G Table 1·2 | 0 |
| F42 | `f_rel` 그림 기본 seq 의 "JESD22-A104 · −55 / +125 °C, 1000 cycle"(seq 미지정 문항에 그대로 그려짐) | **정정 요청(DA/EA)** → JESD47 condition B 요구는 700 cycle. 그림 기본값을 "700 cycle" 로 바꾸거나 "사내 기준 1000 cycle" 로 표기. 기본 seq 를 그리는 문항 목록 첨부(데이터가 아니라 template 문제) | [S] JESD47G | 140 |
| F43 | TC 판정 기준 "1,000 cycle 누적 고장률 n % 이하" | **확인 불가 → JEDEC 기준 아님** (JESD47 은 lot × 표본 0 fail). 지문에 "사내 기준" 명시 필요(STANDARDS 2.3 과 동일) | [S] JESD47G | 19 |

## 7. 열 · 온도 · 물성

| # | 주장 | 판정 | 출처 등급 · 출처 | 문항 수 |
|---|---|---|---|---|
| F44 | "보고된 HBM 스택의 열유속 범위 15–25 W/cm²" | **사용 금지(출처 없음)** → [S]/[V] 출처를 찾지 못함(해설 꼬리표 Electronics Cooling 2026-11 은 [R]·발행 시점 미확인). 참고로 업체 공식 스택 전력·면적(HBM4 12.8 × 11 mm)으로 역산하면 수십 W/cm² 급도 가능해 범위 자체가 낮을 수 있음. 지문을 "이 문항에서는 열유속을 X W/cm² 로 가정" 으로 바꾸고 "보고된 범위" 문장 삭제 | [R] | 55 |
| F45 | DRAM 접합부 온도 85 °C(정상) / 95 °C(확장, refresh 2배) | 확인(DDR 계열 JEDEC 규격의 정상·확장 온도 구간). **105 °C 구간과 HBM 고유 온도 상한은 출처 미확인** → HBM 문항에서 105 °C 를 정답 근거로 쓰지 말 것 | [S] JESD79 계열(DDR) 온도 구간 · HBM 은 미확인 | 0 |
| F46 | 물성 기본값: Cu ρ 1.68–1.72×10⁻⁸ Ω·m, CTE Cu 16.5–17·Si 2.6–2.9·SnAg/SAC ≈ 21–24·EMC 7–15 ppm/K, SiO₂ ≈ 0.5 ppm/K, k: Si 120–150·Cu ≈ 390–400·SiO₂ ≈ 1.4·underfill/NCF 0.2–0.7(충전형 ~1)·EMC/MUF 0.7–3·In TIM 30–80(벌크 In ≈ 82) W/m·K | 확인(교과서·핸드북 값 범위 내). 문항 사용 값(TSV 의 Cu 1.72·1.7×10⁻⁸ Ω·m, SAC305 24·EMC 10·유기기판 15·Si 2.7·SiO₂ 0.43 ppm/K, WARP 의 Cu 390·Si 120·TIM 3–12 W/m·K 등) 모두 범위 내 | [S] 참고 데이터(CRC Handbook 수준) | 0 |
| F47 | EM 수명은 온도에 지수적으로 감소(Black 식 MTTF ∝ J⁻ⁿ·exp(Ea/kT)) | 확인(정성 서술 1건, 수치 지수 n·Ea 를 쓰는 문항은 없음) | [S] Black (1969) 원식 | 0 |

## 8. 문항 id 목록 (분야별)

- **F01** — **COW**(24): COW-I-0126, COW-I-0127, COW-I-0128, COW-A-0143, COW-A-0144, COW-I-0129, COW-I-0130, COW-I-0131, COW-A-0145, COW-A-0146, COW-I-0132, COW-I-0133, COW-I-0134, COW-A-0147, COW-A-0148, COW-I-0135, COW-I-0136, COW-I-0137, COW-A-0149, COW-A-0150, COW-I-0138, COW-I-0139, COW-I-0140, COW-A-0151 · **PROD**(5): PROD-B-0001, PROD-B-0002, PROD-I-0003, PROD-B-0095, PROD-B-0099 · **DRAM**(26): DRAM-B-0013, DRAM-B-0014, DRAM-I-0014, DRAM-I-0015, DRAM-A-0008, DRAM-B-0015, DRAM-B-0016, DRAM-I-0016, DRAM-I-0017, DRAM-A-0009, DRAM-B-0017, DRAM-B-0018, DRAM-I-0018, DRAM-I-0019, DRAM-A-0010, DRAM-B-0019, DRAM-B-0020, DRAM-I-0020, DRAM-I-0021, DRAM-A-0011, DRAM-B-0021, DRAM-B-0022, DRAM-I-0022, DRAM-I-0023, DRAM-A-0012, DRAM-B-0084
- **F02** — **PROD**(2): PROD-B-0002, PROD-B-0124 · **DRAM**(5): DRAM-I-0001, DRAM-I-0018, DRAM-I-0019, DRAM-A-0010, DRAM-A-0057
- **F03** — **PROD**(4): PROD-I-0001, PROD-I-0002, PROD-B-0003, PROD-B-0102
- **F04** — **PROD**(1): PROD-I-0003
- **F05** — **PROD**(2): PROD-I-0003, PROD-B-0099
- **F06** — —
- **F07** — **COW**(24): COW-I-0112, COW-I-0113, COW-A-0133, COW-A-0134, COW-I-0114, COW-I-0115, COW-I-0116, COW-A-0135, COW-A-0136, COW-I-0117, COW-I-0118, COW-I-0119, COW-A-0137, COW-A-0138, COW-I-0120, COW-I-0121, COW-I-0122, COW-A-0139, COW-A-0140, COW-I-0123, COW-I-0124, COW-I-0125, COW-A-0141, COW-A-0142 · **PROD**(2): PROD-I-0003, PROD-I-0004 · **DRAM**(30): DRAM-B-0001, DRAM-B-0002, DRAM-I-0002, DRAM-I-0003, DRAM-A-0002, DRAM-B-0003, DRAM-B-0004, DRAM-I-0004, DRAM-I-0005, DRAM-A-0003, DRAM-B-0005, DRAM-B-0006, DRAM-I-0006, DRAM-I-0007, DRAM-A-0004, DRAM-B-0007, DRAM-B-0008, DRAM-I-0008, DRAM-I-0009, DRAM-A-0005, DRAM-B-0009, DRAM-B-0010, DRAM-I-0010, DRAM-I-0011, DRAM-A-0006, DRAM-B-0011, DRAM-B-0012, DRAM-I-0012, DRAM-I-0013, DRAM-A-0007
- **F08** — **DRAM**(21): DRAM-B-0001, DRAM-B-0002, DRAM-I-0002, DRAM-I-0003, DRAM-A-0002, DRAM-B-0003, DRAM-B-0004, DRAM-I-0004, DRAM-I-0005, DRAM-I-0009, DRAM-A-0005, DRAM-B-0009, DRAM-B-0010, DRAM-I-0010, DRAM-I-0011, DRAM-A-0006, DRAM-B-0011, DRAM-B-0012, DRAM-I-0012, DRAM-I-0013, DRAM-A-0007
- **F09** — **DRAM**(49): DRAM-B-0031, DRAM-B-0032, DRAM-A-0015, DRAM-B-0029, DRAM-I-0032, DRAM-I-0033, DRAM-I-0035, DRAM-A-0018, DRAM-A-0017, DRAM-B-0033, DRAM-I-0036, DRAM-I-0037, DRAM-B-0034, DRAM-I-0034, DRAM-A-0013, DRAM-B-0025, DRAM-I-0043, DRAM-A-0022, DRAM-B-0023, DRAM-B-0024, DRAM-A-0021, DRAM-B-0041, DRAM-I-0024, DRAM-I-0025, DRAM-B-0042, DRAM-I-0042, DRAM-I-0039, DRAM-A-0020, DRAM-B-0039, DRAM-B-0040, DRAM-A-0019, DRAM-B-0037, DRAM-I-0040, DRAM-I-0041, DRAM-B-0038, DRAM-I-0038, DRAM-B-0027, DRAM-B-0028, DRAM-A-0023, DRAM-I-0028, DRAM-I-0029, DRAM-B-0026, DRAM-I-0026, DRAM-B-0043, DRAM-B-0044, DRAM-I-0027, DRAM-A-0014, DRAM-I-0044, DRAM-I-0045
- **F10** — —
- **F11** — **SIP**(31): SIP-B-0001, SIP-B-0003, SIP-B-0004, SIP-B-0005, SIP-B-0006, SIP-B-0007, SIP-B-0008, SIP-B-0009, SIP-B-0010, SIP-B-0011, SIP-B-0012, SIP-B-0013, SIP-B-0014, SIP-B-0015, SIP-B-0016, SIP-B-0017, SIP-B-0018, SIP-B-0019, SIP-B-0020, SIP-B-0021, SIP-B-0022, SIP-I-0003, SIP-I-0004, SIP-I-0005, SIP-I-0006, SIP-I-0007, SIP-I-0008, SIP-I-0009, SIP-I-0010, SIP-I-0011, SIP-I-0012
- **F12** — **SIP**(56): SIP-A-0002, SIP-A-0013, SIP-A-0023, SIP-A-0044, SIP-A-0045, SIP-A-0047, SIP-A-0049, SIP-A-0050, SIP-A-0051, SIP-A-0052, SIP-A-0054, SIP-A-0055, SIP-A-0056, SIP-A-0057, SIP-A-0058, SIP-A-0062, SIP-A-0063, SIP-A-0068, SIP-A-0119, SIP-I-0078, SIP-I-0079, SIP-I-0080, SIP-A-0120, SIP-A-0121, SIP-I-0081, SIP-B-0046, SIP-I-0105, SIP-B-0047, SIP-I-0106, SIP-A-0133, SIP-B-0050, SIP-I-0109, SIP-B-0051, SIP-I-0110, SIP-A-0135, SIP-B-0054, SIP-I-0113, SIP-B-0055, SIP-I-0114, SIP-A-0137, SIP-B-0058, SIP-I-0117, SIP-B-0059, SIP-I-0118, SIP-A-0139, SIP-B-0062, SIP-I-0120, SIP-I-0121, SIP-A-0140, SIP-B-0063, SIP-B-0064, SIP-I-0122, SIP-A-0141, SIP-B-0066, SIP-I-0125, SIP-B-0175 · **PROD**(2): PROD-A-0001, PROD-B-0107
  - "규격"·"JEDEC" 어휘와 함께 쓴 문항: **SIP**(18): SIP-A-0013, SIP-A-0023, SIP-A-0044, SIP-A-0045, SIP-A-0047, SIP-A-0049, SIP-A-0050, SIP-A-0051, SIP-A-0052, SIP-A-0054, SIP-A-0055, SIP-A-0056, SIP-A-0057, SIP-A-0058, SIP-A-0062, SIP-A-0063, SIP-A-0068, SIP-B-0175 · **PROD**(2): PROD-A-0001, PROD-B-0107
- **F13** — **SIP**(181): SIP-A-0002, SIP-A-0013, SIP-A-0014, SIP-A-0015, SIP-A-0016, SIP-A-0017, SIP-A-0018, SIP-A-0019, SIP-A-0020, SIP-A-0021, SIP-A-0022, SIP-A-0023, SIP-A-0024, SIP-A-0025, SIP-A-0026, SIP-A-0027, SIP-A-0028, SIP-A-0029, SIP-A-0030, SIP-A-0031, SIP-A-0032, SIP-A-0033, SIP-A-0034, SIP-A-0035, SIP-A-0036, SIP-A-0037, SIP-A-0038, SIP-A-0039, SIP-A-0040, SIP-A-0041, SIP-A-0042, SIP-A-0043, SIP-A-0046, SIP-A-0048, SIP-A-0053, SIP-A-0059, SIP-A-0060, SIP-A-0061, SIP-A-0064, SIP-A-0065, SIP-A-0066, SIP-A-0067, SIP-A-0069, SIP-A-0070, SIP-A-0071, SIP-A-0072, SIP-I-0016, SIP-I-0017, SIP-A-0078, SIP-A-0079, SIP-I-0018, SIP-I-0019, SIP-I-0020, SIP-A-0080, SIP-A-0081, SIP-I-0021, SIP-I-0022, SIP-I-0023, SIP-A-0082, SIP-A-0083, SIP-I-0024, SIP-I-0025, SIP-I-0026, SIP-A-0084, SIP-A-0085, SIP-I-0027, SIP-I-0028, SIP-I-0029, SIP-A-0086, SIP-A-0087, SIP-I-0030, SIP-I-0031, SIP-I-0032, SIP-A-0088, SIP-A-0089, SIP-I-0033, SIP-I-0034, SIP-I-0035, SIP-A-0090, SIP-A-0091, SIP-I-0036, SIP-I-0037, SIP-I-0038, SIP-A-0092, SIP-A-0093, SIP-I-0039, SIP-I-0040, SIP-I-0041, SIP-A-0094, SIP-A-0095, SIP-I-0042, SIP-I-0043, SIP-I-0044, SIP-A-0096, SIP-A-0097, SIP-I-0045, SIP-I-0046, SIP-I-0047, SIP-A-0098, SIP-A-0099, SIP-I-0048, SIP-I-0049, SIP-I-0050, SIP-A-0100, SIP-A-0101, SIP-I-0051, SIP-I-0052, SIP-I-0053, SIP-A-0102, SIP-A-0103, SIP-I-0054, SIP-I-0055, SIP-I-0056, SIP-A-0104, SIP-A-0105, SIP-I-0057, SIP-I-0058, SIP-I-0059, SIP-A-0106, SIP-A-0107, SIP-I-0060, SIP-I-0061, SIP-I-0062, SIP-A-0108, SIP-A-0109, SIP-I-0063, SIP-I-0064, SIP-I-0065, SIP-A-0110, SIP-A-0111, SIP-I-0066, SIP-I-0067, SIP-I-0068, SIP-A-0112, SIP-A-0113, SIP-I-0069, SIP-I-0070, SIP-I-0071, SIP-A-0114, SIP-A-0115, SIP-I-0072, SIP-I-0073, SIP-I-0074, SIP-A-0116, SIP-A-0117, SIP-I-0075, SIP-I-0076, SIP-I-0077, SIP-A-0118, SIP-B-0045, SIP-I-0104, SIP-A-0132, SIP-B-0048, SIP-I-0107, SIP-B-0049, SIP-I-0108, SIP-A-0134, SIP-B-0052, SIP-I-0111, SIP-B-0053, SIP-I-0112, SIP-A-0136, SIP-B-0056, SIP-I-0115, SIP-B-0057, SIP-I-0116, SIP-A-0138, SIP-B-0060, SIP-I-0119, SIP-B-0061, SIP-I-0120, SIP-A-0140, SIP-B-0064, SIP-I-0123, SIP-B-0065, SIP-I-0124, SIP-B-0163, SIP-B-0175, SIP-I-0162, SIP-A-0185, SIP-A-0190 · **PROD**(3): PROD-A-0001, PROD-A-0002, PROD-B-0107
  - "규격"·"JEDEC" 어휘와 함께 쓴 문항(우선 수정 대상): **SIP**(49): SIP-A-0013, SIP-A-0014, SIP-A-0015, SIP-A-0016, SIP-A-0017, SIP-A-0018, SIP-A-0019, SIP-A-0020, SIP-A-0021, SIP-A-0022, SIP-A-0023, SIP-A-0024, SIP-A-0025, SIP-A-0026, SIP-A-0027, SIP-A-0028, SIP-A-0029, SIP-A-0030, SIP-A-0031, SIP-A-0032, SIP-A-0033, SIP-A-0034, SIP-A-0035, SIP-A-0036, SIP-A-0037, SIP-A-0038, SIP-A-0039, SIP-A-0040, SIP-A-0041, SIP-A-0042, SIP-A-0043, SIP-A-0046, SIP-A-0048, SIP-A-0053, SIP-A-0059, SIP-A-0060, SIP-A-0061, SIP-A-0064, SIP-A-0065, SIP-A-0066, SIP-A-0067, SIP-A-0069, SIP-A-0070, SIP-A-0071, SIP-A-0072, SIP-B-0163, SIP-B-0175, SIP-I-0162, SIP-A-0185 · **PROD**(2): PROD-A-0001, PROD-B-0107
- **F14** — **PROD**(1): PROD-B-0135
- **F15** — **COW**(112): COW-I-0021, COW-A-0071, COW-A-0072, COW-A-0073, COW-B-0027, COW-B-0028, COW-I-0026, COW-I-0027, COW-A-0079, COW-B-0029, COW-B-0030, COW-I-0028, COW-I-0029, COW-A-0080, COW-B-0031, COW-B-0032, COW-I-0030, COW-I-0031, COW-A-0081, COW-B-0033, COW-B-0034, COW-I-0032, COW-I-0033, COW-A-0082, COW-B-0035, COW-B-0036, COW-I-0034, COW-I-0035, COW-A-0083, COW-B-0037, COW-B-0038, COW-I-0036, COW-I-0037, COW-A-0084, COW-B-0039, COW-B-0040, COW-I-0038, COW-I-0039, COW-A-0085, COW-B-0041, COW-B-0042, COW-I-0040, COW-I-0041, COW-A-0086, COW-B-0043, COW-B-0044, COW-I-0042, COW-I-0043, COW-A-0087, COW-B-0045, COW-B-0046, COW-I-0044, COW-I-0045, COW-A-0088, COW-B-0047, COW-B-0048, COW-I-0046, COW-I-0047, COW-I-0080, COW-I-0081, COW-A-0111, COW-A-0112, COW-I-0082, COW-I-0083, COW-I-0084, COW-A-0113, COW-A-0114, COW-I-0085, COW-I-0086, COW-I-0087, COW-A-0115, COW-A-0116, COW-I-0088, COW-I-0089, COW-I-0090, COW-A-0117, COW-A-0118, COW-I-0091, COW-I-0092, COW-I-0093, COW-A-0119, COW-A-0120, COW-I-0094, COW-I-0095, COW-I-0096, COW-A-0121, COW-A-0122, COW-I-0097, COW-I-0098, COW-I-0099, COW-A-0123, COW-A-0124, COW-I-0100, COW-I-0101, COW-I-0102, COW-A-0125, COW-A-0126, COW-I-0103, COW-I-0104, COW-I-0105, COW-A-0127, COW-A-0128, COW-I-0106, COW-I-0107, COW-I-0108, COW-A-0129, COW-A-0130, COW-I-0109, COW-I-0110, COW-I-0111, COW-A-0131, COW-A-0132 · **WARP**(3): WARP-I-0059, WARP-A-0055, WARP-A-0056 · **SIP**(164): SIP-I-0016, SIP-I-0017, SIP-A-0078, SIP-A-0079, SIP-I-0018, SIP-I-0019, SIP-I-0020, SIP-A-0080, SIP-A-0081, SIP-I-0021, SIP-I-0022, SIP-I-0023, SIP-A-0082, SIP-A-0083, SIP-I-0024, SIP-I-0025, SIP-I-0026, SIP-A-0084, SIP-A-0085, SIP-I-0027, SIP-I-0028, SIP-I-0029, SIP-A-0086, SIP-A-0087, SIP-I-0030, SIP-I-0031, SIP-I-0032, SIP-A-0088, SIP-A-0089, SIP-I-0033, SIP-I-0034, SIP-I-0035, SIP-A-0090, SIP-A-0091, SIP-I-0036, SIP-I-0037, SIP-I-0038, SIP-A-0092, SIP-A-0093, SIP-I-0039, SIP-I-0040, SIP-I-0041, SIP-A-0094, SIP-A-0095, SIP-I-0042, SIP-I-0043, SIP-I-0044, SIP-A-0096, SIP-A-0097, SIP-I-0045, SIP-I-0046, SIP-I-0047, SIP-A-0098, SIP-A-0099, SIP-I-0048, SIP-I-0049, SIP-I-0050, SIP-A-0100, SIP-A-0101, SIP-I-0051, SIP-I-0052, SIP-I-0053, SIP-A-0102, SIP-A-0103, SIP-I-0054, SIP-I-0055, SIP-I-0056, SIP-A-0104, SIP-A-0105, SIP-I-0057, SIP-I-0058, SIP-I-0059, SIP-A-0106, SIP-A-0107, SIP-I-0060, SIP-I-0061, SIP-I-0062, SIP-A-0108, SIP-A-0109, SIP-I-0063, SIP-I-0064, SIP-I-0065, SIP-A-0110, SIP-A-0111, SIP-I-0066, SIP-I-0067, SIP-I-0068, SIP-A-0112, SIP-A-0113, SIP-I-0069, SIP-I-0070, SIP-I-0071, SIP-A-0114, SIP-A-0115, SIP-I-0072, SIP-I-0073, SIP-I-0074, SIP-A-0116, SIP-A-0117, SIP-I-0075, SIP-I-0076, SIP-I-0077, SIP-A-0118, SIP-A-0119, SIP-I-0078, SIP-I-0079, SIP-I-0080, SIP-A-0120, SIP-A-0121, SIP-I-0081, SIP-B-0045, SIP-B-0046, SIP-I-0104, SIP-I-0105, SIP-A-0132, SIP-B-0047, SIP-B-0048, SIP-I-0106, SIP-I-0107, SIP-A-0133, SIP-B-0049, SIP-B-0050, SIP-I-0108, SIP-I-0109, SIP-A-0134, SIP-B-0051, SIP-B-0052, SIP-I-0110, SIP-I-0111, SIP-A-0135, SIP-B-0053, SIP-B-0054, SIP-I-0112, SIP-I-0113, SIP-A-0136, SIP-B-0055, SIP-B-0056, SIP-I-0114, SIP-I-0115, SIP-A-0137, SIP-B-0057, SIP-B-0058, SIP-I-0116, SIP-I-0117, SIP-A-0138, SIP-B-0059, SIP-B-0060, SIP-I-0118, SIP-I-0119, SIP-A-0139, SIP-B-0061, SIP-B-0062, SIP-I-0120, SIP-I-0121, SIP-A-0140, SIP-B-0063, SIP-B-0064, SIP-I-0122, SIP-I-0123, SIP-A-0141, SIP-B-0065, SIP-B-0066, SIP-I-0124, SIP-I-0125 · **PROD**(3): PROD-A-0001, PROD-A-0002, PROD-A-0003
- **F16** — **PROD**(4): PROD-B-0122, PROD-B-0123, PROD-B-0125, PROD-B-0132
- **F17** — **PROD**(1): PROD-B-0124
- **F18** — **PROD**(2): PROD-B-0126, PROD-B-0127
- **F19** — **PROD**(1): PROD-B-0101
- **F20** — **PROD**(1): PROD-B-0103
- **F21** — **PROD**(2): PROD-B-0128, PROD-B-0129
- **F22** — **PROD**(1): PROD-B-0130
- **F23** — **COW**(1): COW-B-0117
- **F24** — **PROD**(2): PROD-B-0133, PROD-B-0134
- **F25** — **WARP**(7): WARP-B-0149, WARP-B-0150, WARP-B-0151, WARP-B-0152, WARP-B-0153, WARP-B-0154, WARP-A-0056
- **F26** — **BUMP**(1): BUMP-B-0080 · **COW**(1): COW-A-0072 · **SIP**(1): SIP-B-0173
- **F27** — **PROD**(1): PROD-A-0004
- **F28** — **PROD**(2): PROD-B-0109, PROD-B-0108
- **F29** — **PROD**(1): PROD-B-0132
- **F30** — **COW**(1): COW-B-0106
- **F31** — **COW**(1): COW-I-0146 · **PROD**(1): PROD-B-0111
- **F32** — **COW**(1): COW-I-0023
- **F33** — **PROD**(1): PROD-B-0110
- **F34** — **SIP**(59): SIP-I-0013, SIP-A-0073, SIP-I-0014, SIP-A-0074, SIP-I-0015, SIP-B-0023, SIP-B-0024, SIP-I-0082, SIP-I-0083, SIP-A-0122, SIP-B-0025, SIP-B-0026, SIP-I-0084, SIP-I-0085, SIP-A-0123, SIP-B-0027, SIP-B-0028, SIP-I-0086, SIP-I-0087, SIP-A-0124, SIP-B-0029, SIP-B-0030, SIP-I-0088, SIP-I-0089, SIP-A-0125, SIP-B-0031, SIP-B-0032, SIP-I-0090, SIP-I-0091, SIP-A-0126, SIP-B-0033, SIP-B-0034, SIP-I-0092, SIP-I-0093, SIP-A-0127, SIP-B-0035, SIP-B-0036, SIP-I-0094, SIP-I-0095, SIP-A-0128, SIP-B-0037, SIP-B-0038, SIP-I-0096, SIP-I-0097, SIP-A-0129, SIP-B-0039, SIP-B-0040, SIP-I-0098, SIP-I-0099, SIP-A-0130, SIP-B-0041, SIP-B-0042, SIP-I-0100, SIP-I-0101, SIP-A-0131, SIP-B-0043, SIP-B-0044, SIP-I-0102, SIP-I-0103
- **F35** — **SIP**(1): SIP-I-0015
- **F36** — **SIP**(4): SIP-I-0145, SIP-A-0178, SIP-B-0138, SIP-I-0136
  - SIP-I-0014(유기 RDL 의 CTE 이점)는 확인 — 서로 모순되는 위 4 문항을 이쪽에 맞출 것
- **F37** — **SIP**(3): SIP-I-0013, SIP-I-0144, SIP-I-0146
- **F38** — **SIP**(14): SIP-B-0077, SIP-B-0134, SIP-B-0135, SIP-B-0136, SIP-B-0139, SIP-B-0140, SIP-B-0141, SIP-B-0142, SIP-B-0144, SIP-B-0155, SIP-I-0143, SIP-I-0147, SIP-I-0148, SIP-A-0074
- **F39** — **FA**(49): FA-B-0002, FA-A-0002, FA-B-0023, FA-B-0024, FA-B-0025, FA-B-0026, FA-B-0027, FA-B-0028, FA-B-0029, FA-B-0030, FA-B-0031, FA-B-0032, FA-B-0033, FA-B-0034, FA-B-0035, FA-B-0036, FA-B-0037, FA-B-0038, FA-B-0039, FA-B-0040, FA-B-0041, FA-B-0042, FA-B-0043, FA-B-0044, FA-B-0045, FA-B-0046, FA-A-0003, FA-A-0004, FA-A-0005, FA-A-0006, FA-A-0007, FA-A-0008, FA-A-0009, FA-A-0010, FA-A-0011, FA-A-0012, FA-A-0013, FA-A-0014, FA-A-0015, FA-A-0016, FA-A-0017, FA-A-0018, FA-A-0019, FA-A-0020, FA-B-0092, FA-B-0093, FA-B-0094, FA-B-0096, FA-A-0033 · **PROD**(4): PROD-B-0115, PROD-B-0116, PROD-B-0117, PROD-B-0118
- **F40** — **FA**(5): FA-B-0043, FA-B-0044, FA-B-0045, FA-B-0046, FA-A-0033
- **F41** — —
- **F42** — **FA**(137): FA-B-0002, FA-A-0002, FA-B-0023, FA-B-0024, FA-B-0025, FA-B-0026, FA-B-0027, FA-B-0028, FA-B-0029, FA-B-0030, FA-B-0031, FA-B-0032, FA-B-0033, FA-B-0034, FA-B-0035, FA-B-0036, FA-B-0037, FA-B-0038, FA-B-0039, FA-B-0040, FA-B-0041, FA-B-0042, FA-B-0043, FA-B-0044, FA-B-0045, FA-B-0046, FA-A-0003, FA-A-0004, FA-A-0005, FA-A-0006, FA-A-0007, FA-A-0008, FA-A-0009, FA-A-0010, FA-A-0011, FA-A-0012, FA-A-0013, FA-A-0014, FA-A-0015, FA-A-0016, FA-A-0017, FA-A-0018, FA-A-0019, FA-A-0020, FA-I-0023, FA-A-0022, FA-B-0055, FA-B-0056, FA-B-0084, FA-B-0085, FA-B-0092, FA-B-0093, FA-B-0094, FA-B-0095, FA-B-0096, FA-B-0097, FA-B-0119, FA-B-0120, FA-I-0028, FA-I-0029, FA-I-0030, FA-I-0031, FA-I-0032, FA-I-0033, FA-I-0034, FA-I-0038, FA-I-0039, FA-I-0042, FA-I-0043, FA-I-0044, FA-I-0045, FA-I-0046, FA-I-0047, FA-I-0051, FA-I-0054, FA-I-0055, FA-I-0056, FA-I-0061, FA-I-0062, FA-I-0063, FA-I-0064, FA-I-0065, FA-I-0066, FA-I-0067, FA-I-0068, FA-I-0069, FA-I-0078, FA-I-0080, FA-I-0081, FA-I-0082, FA-I-0083, FA-I-0084, FA-I-0085, FA-I-0086, FA-I-0087, FA-I-0088, FA-I-0114, FA-A-0024, FA-A-0025, FA-A-0026, FA-A-0027, FA-A-0028, FA-A-0031, FA-A-0032, FA-A-0035, FA-A-0036, FA-A-0037, FA-A-0038, FA-A-0039, FA-A-0040, FA-A-0041, FA-A-0044, FA-A-0047, FA-A-0048, FA-A-0050, FA-A-0051, FA-A-0052, FA-A-0056, FA-A-0057, FA-A-0058, FA-A-0059, FA-A-0076, FA-A-0077, FA-A-0078, FA-A-0093, FA-A-0094, FA-A-0095, FA-A-0096, FA-A-0097, FA-A-0098, FA-A-0099, FA-A-0124, FA-A-0129, FA-A-0131, FA-A-0132, FA-A-0138, FA-A-0139 · **MET**(3): MET-I-0002, MET-I-0003, MET-A-0005
- **F43** — **FA**(19): FA-A-0002, FA-A-0003, FA-A-0004, FA-A-0005, FA-A-0006, FA-A-0007, FA-A-0008, FA-A-0009, FA-A-0010, FA-A-0011, FA-A-0012, FA-A-0013, FA-A-0014, FA-A-0015, FA-A-0016, FA-A-0017, FA-A-0018, FA-A-0019, FA-A-0020
- **F44** — **WARP**(55): WARP-I-0058, WARP-B-0019, WARP-B-0020, WARP-I-0127, WARP-I-0128, WARP-A-0103, WARP-B-0021, WARP-B-0022, WARP-I-0129, WARP-I-0130, WARP-A-0104, WARP-B-0023, WARP-B-0024, WARP-I-0131, WARP-I-0132, WARP-A-0105, WARP-B-0025, WARP-B-0026, WARP-I-0133, WARP-I-0134, WARP-A-0106, WARP-B-0027, WARP-B-0028, WARP-I-0135, WARP-I-0136, WARP-A-0107, WARP-B-0029, WARP-B-0030, WARP-I-0137, WARP-I-0138, WARP-A-0108, WARP-B-0031, WARP-B-0032, WARP-I-0139, WARP-I-0140, WARP-A-0109, WARP-B-0033, WARP-B-0034, WARP-I-0141, WARP-I-0142, WARP-A-0110, WARP-B-0035, WARP-B-0036, WARP-I-0143, WARP-I-0144, WARP-A-0111, WARP-B-0037, WARP-B-0038, WARP-I-0145, WARP-I-0146, WARP-A-0112, WARP-B-0039, WARP-B-0040, WARP-I-0147, WARP-I-0148
- **F45** — —
- **F46** — —
- **F47** — —

## 9. STANDARDS 정정 제안 (EA 반영)

1. **§2.2 HBM3 단수**: "4/8/12/16-Hi" → "4/8/12-Hi (16-Hi 는 JESD238 의 향후 확장 조항)". [S] JESD238 발표문.
2. **§2.2 패키지 높이 행**: HBM4 의 **775 µm 굵게 표시(=JEDEC 확정값 취급)를 해제**하고 각주 추가 — "720 µm: Samsung 공식(2019, HBM2/2E 8·12단) [V], HBM3/3E 의 JEDEC 값은 보도 [R]. 775 µm: JESD270-4 발표문에 없음, 보도 [R] + SK hynix Hot Chips 2026 제품 Z-height. JESD270-4(4A) 본문 확인 전까지 문항에서는 '높이 상한(설계 조건)' 으로 주고 'JEDEC 규격값' 으로 묻지 않는다." (EA 가 JEDEC 계정으로 JESD270-4 본문을 받아 확인하면 굵게 복원)
3. **§2.2 HBM2E 열**: 머리말에 "JEDEC 문서명은 HBM2 (JESD235C)" 추가. HBM3E 핀 속도 "업체 9.2–9.8 Gb/s 급" → "업체 9.2–10 Gb/s 급(Samsung 12H 1,280 GB/s)". HBM4 행에 "HBM3 컨트롤러와 하위 호환(JESD270-4 명시)" 한 줄 추가(F04 재발 방지).
4. **§2.3 신뢰성 표**:
   - Temperature Cycling 대표 조건 "−55 / +125 °C (condition B), 1000 cycle" → **"condition B −55/+125 °C 700 cycle (JESD47); G −40/+125 °C 850 cycle; 1000 cycle 은 고객·사내 기준"**.
   - 자격 시험 체계 "3 lot × 77 개, 0 fail" → **"HTOL 3 lot × 77, 패키지 시험(TC·THB/HAST·uHAST·HTSL) 3 lot × 25, 모두 0 fail"**.
   - HTOL "125 °C 급" → "Tj ≥ 125 °C, Vcc ≥ Vccmax"; HTS → "HTSL Ta ≥ 150 °C, 1000 h"; bHAST 행에 "또는 110 °C·264 h" 병기.
   - 출처 문구: "JESD47G 기준 — 최신판(JESD47L 등)으로 재확인".
5. **§2.4 HCB pad pitch "≤ 10 µm"**: HBM 용 HCB 공개 발표는 "bump pitch < 18 µm"(SK hynix Hot Chips 2026) 수준이므로 "HCB pad pitch: HBM 발표 < 18 µm, 로직 SoIC 9 µm 이하" 로 완화하거나 "≤ 10 µm 는 문항 설정값" 으로 명시. 또 "HCB 접합 전 die 휨 nm 급" 같은 서술을 막기 위해 "nm 급 요구는 표면 거칠기·Cu recess, die 휨은 µm 급" 한 줄 추가.
6. **§2.4 DRAM 온도 "105 °C(일부 규격)"**: 출처 미확인 → "(출처 확인 전 정답 근거로 쓰지 않음)" 표기. 열유속 기본 범위를 둘 경우 "보고된 범위" 가 아니라 "문항 설정값" 으로만 쓰도록 명시.
- 부록 A `f_rel` 기본 seq 의 "1000 cycle" 은 JESD47 condition B(700 cycle)와 다름 → `EA_to_DA.md` 에 추가 요청(F42).

## 10. 출처

- [S] JEDEC JESD270-4 HBM4 보도자료 2025-04-16 — 전재 https://www.storagenewsletter.com/2025/04/17/jedec-and-industry-leaders-collaborate-to-release-jesd270-4-hbm4-standard/
- [S] JEDEC JESD238 HBM3 보도자료 2022-01-27 — 전재 https://www.hpcwire.com/off-the-wire/jedec-publishes-hbm3-updated-to-high-bandwidth-memory-hbm-standard/
- [S] JESD47G Stress-Test-Driven Qualification of Integrated Circuits (원문 PDF) https://designers-guide.org/forum/Attachments/JESD47G.pdf
- [S](2차 경유) JESD235C 표 — https://www.anandtech.com/show/15469
- [V] Samsung 12-layer 3D-TSV (720 µm) 2019-10-07 https://news.samsung.com/us/samsung-12-layer-3d-tsv-chip-packaging-technology
- [V] Samsung 36GB HBM3E 12H 2024-02-27 https://news.samsung.com/global/samsung-develops-industry-first-36gb-hbm3e-12h-dram
- [V] Samsung HBM4 양산 출하 2026-02-12 https://news.samsung.com/global/samsung-ships-industry-first-commercial-hbm4
- [V] Samsung GTC 2026 HBM4E 공개·HCB 열저항 20 % 이상 2026-03-16 https://news.samsung.com/kr/삼성전자-gtc서-hbm4e-최초-공개토털-솔루션으로-엔비
- [V] Samsung HBM4E 샘플 출하 2026-05-29 https://news.samsung.com/global/samsung-electronics-begins-shipment-of-industry-first-hbm4e-samples
- [V] SK hynix HBM4 개발 완료 2025-09-12 (보도 전재) https://www.hpcwire.com/off-the-wire/sk-hynix-completes-development-of-hbm4-and-prepares-for-mass-production/
- [V] SK hynix HBM4E 12단 샘플 2026-06-18 https://en.prnasia.com/releases/global/sk-hynix-ships-samples-of-12-layer-next-gen-hbm4e--537615.shtml
- [V] SK hynix iHBM 2026-05-25 https://www.barchart.com/story/news/2119947/sk-hynix-unveils-ihbm-thermal-solution-to-boost-ai-performance
- [V] SK hynix MR-MUF 방열(thermal dummy bump 4배, EMC 1.6배) https://news.skhynix.com/rulebreaker-revolutions-mr-muf-unlocks-hbm-heat-control/
- [V] SK hynix ECTC 2023 MR-MUF vs TC-NCF (Tj −14 °C) https://conferences.computer.org/ectc/pdfs/ECTC2023-1NkkviSxgDnmPjptC1ysqm/349800a878/349800a878.pdf
- [V-2차] SK hynix Hot Chips 2026 (ServeTheHome) https://www.servethehome.com/sk-hynix-hbm-packaging-at-hot-chips-2026/
- [V] TSMC CoWoS(3DFabric) https://3dfabric.tsmc.com/english/dedicatedFoundry/technology/cowos.htm · HPC WLSI https://www.tsmc.com/english/dedicatedFoundry/technology/platform_HPC_tech_WLSI
- [V] TSMC CoWoS-L ECTC 2023 https://conferences.computer.org/ectc/pdfs/ECTC2023-1NkkviSxgDnmPjptC1ysqm/349800b022/349800b022.pdf
- [V-2차] TSMC HBM4 base die N12FFC+/N5 (2024 symposium) https://www.tomshardware.com/pc-components/gpus/tsmc-to-build-base-dies-for-hbm4-memory-on-its-12nm-and-5nm-nodes
- [V-2차] Samsung ISSCC 2026 HBM4 (36 GB 12-Hi, 3.3 TB/s) https://newsletter.semianalysis.com/p/isscc-2026-nvidia-and-broadcom-cpo
- [R] HBM4 775 µm 보도 https://www.trendforce.com/news/2025/04/21/news-jedec-finalizes-hbm4-standard-potentially-easing-pressure-on-hybrid-bonding-adoption/ · https://www.techpowerup.com/320314/jedec-agrees-to-relax-hbm4-package-thickness
- [R] HBM 높이 900 µm 검토 보도 https://www.trendforce.com/news/2026/04/01/news-jedec-reportedly-plans-to-relax-hbm-height-specs-to-900%C2%B5m-potentially-slowing-hybrid-bonding-adoption/
- [R] HB die 휨(KLA 표) TechSearch DARPA 2025 https://www.darpa.mil/sites/default/files/attachment/2025-12/mto-ngmm-summit-presentation-3d-hybrid-bonding.pdf

