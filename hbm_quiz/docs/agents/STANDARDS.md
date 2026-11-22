# HBM 이해도 평가 — 문항 품질 기준서 (STANDARDS)

- 소유: EA (Editor-in-chief Agent) · 적용 대상: `data/NN_CODE.json` 전 문항 · 자동 검사: `tools/validate.py`
- 변경 이력: 2026-11-21 용어 규약에 front-to-back 적층 방향 추가(TSV-B-0078 정정 계기).
- 변경 이력: 2026-11-21 조사 사전 HBM 을 받침 있음(에이치비엠)으로 정정, 검사기가 `f_therm.core` 를 N단과 비교.
- 변경 이력: 2026-11-21 2.4 형상 기준을 Micron HBM3E 12H 실측으로 통일(BJ 결정: pitch 23 / 48 × 55 µm, 간극 11 µm; 같은 날 잠시 쓴 25 µm·6.5–7.5 µm 는 폐기). 2026-11-20 FACT §9 반영 — 부록 B 참조(HBM3 단수, 패키지 높이 비확정, HBM4 하위 호환, JESD47 조건, HCB pitch·휨, 105 °C).
- 변경 이력: 2026-11-20 DA Phase 1 반영 — 부록 A 를 LAYOUT_RULES §3–4 와 일치(hideResult 의무, f_bond `dish` opt-in, f_sip `lines`, f_therm `core`, f_table·f_wafermap), 질문 마지막 문장 ≤ 90자, 수식 띄어쓰기, `metrics: []` 키 유지.
- 변경 이력: 2026-11-20 W0.5 — WARP 를 WARP(Warpage 와 기계적 응력)·THERM(열 설계와 방열, `data/13_THERM.json`, legacy_prefix WARP)으로 분할. Smile/Cry 규약 확정.
- 이 문서는 **모든 분야 에이전트의 공통 헌장**이다. 분야 브리프(`docs/agents/briefs/CODE.md`)는 이 문서를 전제로 쓴다.
- 판정 순서: ① 기술적 사실 → ② 정답 유일성 → ③ 난이도 적합성 → ④ 오답 품질 → ⑤ 해설 → ⑥ 그림·지표 일치 → ⑦ 문체.
  앞 단계가 틀리면 뒤 단계는 의미가 없다. 사용자는 반도체 패키징 실무·연구 수준의 전문가다. **"그럴듯한 문장"이 아니라 "현업 전문가가 검토해도 반박할 수 없는 문항"이 기준**이다.

---

## 1. 난이도 정의 (인지 수준)

| 등급 | 무엇을 묻는가 | 허용되는 문항 형태 | 허용되지 않는 것 |
|---|---|---|---|
| **초급 B** | 용어·구조·원리의 **인지** | 용어↔정의, 구조의 구성요소·순서, 단일 원리의 방향(늘리면 늘어난다/줄어든다), 단위 환산 1단계 | 다단계 계산, 두 조건의 비교 판단 |
| **중급 I** | **인과·조건 비교·간단한 정량** | 원인→결과 연결, 두 조건(공법·재료·치수) 비교, 공식 1개에 2–3개 값 대입, 관측 1–2개로 결함 이름·기구 판정 | 공식 하나에 값만 바꿔 넣는 "고급" |
| **고급 A** | **다변수 트레이드오프 · 실측 데이터 해석 · 불량 원인 규명 · 수치 추정** | 3개 이상 변수가 얽힌 판단, 표·그래프·맵 형태의 데이터에서 결론 도출, 복수 관측을 모두 만족하는 원인 1개 특정, 공식 2개 이상을 연결하는 추정(Fermi), 대책의 부작용까지 고려한 선택 | ① 단순 대입 계산(예: 저항 = ρL/A 한 번), ② 일반론적 "판단 태도" 문항(예: "발표 수치를 볼 때 확인할 것"), ③ 두 개의 독립 사실을 "A 이며 B 이다" 로 묶은 이중 정답 |

- 같은 주제라도 난이도는 **요구하는 사고 단계 수**로 정한다. 고급은 "이 문항을 풀려면 최소 두 단계 이상 추론이 필요한가?" 에 예라고 답할 수 있어야 한다.
- 고급 문항은 HBM 고유 맥락(고단 적층, 미세 피치, 높이 예산, base die 발열, KGD, 재작업 불가 등)을 반드시 가진다. 일반 반도체·일반 품질관리 상식만으로 풀리는 문항은 고급이 아니다.

---

## 2. 기술적 사실 정확성

### 2.1 기준 시점과 출처 등급
- 기준 시점: **2024–2026 년 HBM3E / HBM4 양산·개발 상황**. HBM2E 이하는 비교 대상일 때만 쓴다.
- 출처 등급: **[S] JEDEC 등 표준 문서** > **[V] 제조사 공식 발표(보도자료·ISSCC/ECTC/IEDM 논문)** > **[R] 언론·분석 보도**. 문항의 정답 근거는 [S] 또는 [V] 여야 한다. [R] 수준 정보(예: 특정 회사의 미발표 로드맵, 샘플 속도 소문)는 **정답 근거로 쓰지 않는다**.
- 업체 고유 수치(핀 속도, 단수, 두께)를 쓸 때는 "업체 발표 기준" 임을 지문에 밝히고, JEDEC 값과 혼동하지 않는다.
- **해설 끝의 `[근거] …` 꼬리표는 일괄 부착된 것으로 문항별 근거가 아니다.** 새로 쓰거나 고친 해설에는 넣지 않는다(남은 것은 EA 가 Phase 2 에서 제거). 검증 가능한 고유 출처가 있으면 레코드의 선택 필드 `"src": "JESD270-4 §x / ISSCC 2025 paper n"` 에 적는다(화면에는 나오지 않음).

### 2.2 확실한 기준값 (이 표 밖의 JEDEC 수치는 출처 확인 없이 쓰지 말 것)

| 항목 | HBM2E (JEDEC 문서명은 HBM2, JESD235C) | HBM3 (JESD238) | HBM3E | HBM4 (JESD270-4, 2025-04) |
|---|---|---|---|---|
| I/O 폭 / 스택 | 1,024 bit | 1,024 bit | 1,024 bit | **2,048 bit** |
| 독립 채널 × 폭 | 8 × 128 bit | 16 × 64 bit | 16 × 64 bit | **32 × 64 bit** |
| pseudo channel | 16 × 64 bit | 32 × 32 bit | 32 × 32 bit | **64 × 32 bit** |
| 핀 속도 | JEDEC 3.2 Gb/s (업체 3.6) | **6.4 Gb/s** | 별도 JEDEC 세대 아님. 업체 9.2–10 Gb/s 급(Samsung 12H 1,280 GB/s) | **JEDEC 8 Gb/s**, 업체는 그 이상 발표 |
| 스택 대역폭 | ≈ 410–460 GB/s | ≈ 819 GB/s | ≈ 1.2 TB/s 급 | ≈ 2 TB/s (8 Gb/s 기준) |
| 단수 | 최대 12-Hi | 4/8/12-Hi (16-Hi 는 향후 확장 조항) | 8-Hi 24 GB, 12-Hi 36 GB (24 Gb die) | 4/8/12/16-Hi, 24 Gb·32 Gb die, 최대 64 GB |
| 패키지 높이 ¹ | 720 µm | 720 µm | 720 µm | 775 µm |
| 컨트롤러 호환 | | | HBM3 컨트롤러 호환(업체) | **HBM3 컨트롤러와 하위 호환(JESD270-4 발표문 명시)** |

- ¹ **패키지 높이는 JEDEC 확정값으로 쓰지 않는다**(FACT F12·F13): 720 µm 은 Samsung 공식(2019, 8·12단 패키지) [V], HBM3/3E 의 "JEDEC 720 µm" 은 보도 [R]. 775 µm 은 JESD270-4 발표문에 없고 보도 [R] + SK hynix Hot Chips 2026 의 HBM4 제품 Z-height [V-2차]. JESD270-4(4A) 본문 확인 전까지 문항에서는 **"높이 상한(설계 조건) 775 µm"** 처럼 주어진 조건으로만 쓰고 "JEDEC 규격값" 으로 묻지 않는다. HBM4E 높이 완화(825–900 µm)는 [R] 뿐 → 사용 금지.
- 대역폭 = I/O 폭(bit) × 핀 속도(Gb/s) ÷ 8 → GB/s. 해설에 반드시 이 식을 보인다.
- 용량 = die 밀도(Gb) × core die 수 ÷ 8 → GB. base die 는 셀 배열이 없어 용량에 기여하지 않는다.
- 위 표 중 **굵게 표시하지 않은 업체 값**은 "업체 발표 기준" 으로만 쓴다. HBM3E 를 "JEDEC 규격" 이라 부르지 않는다.
- 가상의 인터페이스 구성(예: 512 bit · 4 채널, 4,096 bit · 32 채널)은 계산 연습용으로도 **"HBM" 이라는 이름을 붙여 출제하지 않는다**. 실제 세대 구성을 쓰거나 "가상의 메모리 인터페이스" 임을 명시한다.

### 2.3 신뢰성 시험 표준 (확실한 것)
| 시험 | 문서 | 대표 조건 |
|---|---|---|
| MSL 분류 / preconditioning | J-STD-020 (분류·리플로 프로파일) / **JESD22-A113** (preconditioning 절차) | 흡습 후 리플로 3회 |
| Temperature Cycling | JESD22-A104 | JESD47 자격: condition B −55/+125 °C **700 cycle**, condition G −40/+125 °C 850 cycle. 1000 cycle 은 고객·사내 기준으로만 |
| HTOL | JESD22-A108 | Tj ≥ 125 °C, Vcc ≥ Vccmax, 1000 h |
| HTSL | JESD22-A103 | Ta ≥ 150 °C, 무바이어스, 1000 h |
| THB | JESD22-A101 | 85 °C / 85 %RH, 바이어스, 1000 h |
| bHAST / uHAST | JESD22-A110 / JESD22-A118 | 130 °C / 85 %RH, 96 h (또는 110 °C, 264 h), 바이어스 유무 |
| 자격 시험 체계 | JESD47 | HTOL 3 lot × 77, 패키지 시험(TC·THB/HAST·uHAST·HTSL) 3 lot × 25, 모두 0 fail — "누적 고장률 n % 이하" 는 JEDEC 판정 기준이 아니다. 사내 기준으로 쓸 때는 그렇게 명시. (FACT 는 JESD47G 원문으로 확인 — 최신판에서 수치가 바뀌었을 수 있으므로 문항에 판 번호를 쓰지 않는다) |
| ESD | ANSI/ESDA/JEDEC JS-001 (HBM), JS-002 (CDM) | |

### 2.4 물성·범위 (계산 문항의 기본값; 문항이 다른 값을 주면 그 값을 따른다)
- Cu 비저항 1.68–1.72 × 10⁻⁸ Ω·m · CTE: Cu 16.5–17, Si 2.6–2.9, SnAg ≈ 22, 충전 EMC 7–15 (Tg 이하) ppm/K
- 열전도율(W/m·K): Si 120–150, Cu ≈ 390, SiO₂ ≈ 1.4, NCF·underfill 0.2–0.7, 충전 EMC/MUF 0.7–3, TIM 3–10
- HBM 현실 범위(설정값이 벗어나면 사유를 지문에 밝힌다): core die 30–60 µm(실측 기준 34–35 µm), base die 40–100 µm(실측 기준 44 µm, Si 31 µm), **형상 기준 = Micron HBM3E 12H 단면 실측(TechInsights; 2026-11-21 BJ 결정)**: core die 사이 µbump pitch 23 µm(지름 약 10–11.6 µm), base die 아래 면(인터포저 쪽) JEDEC 48 × 55 µm, core die 34–35 µm, 최상단 die 139 µm, base die 44 µm(Si 31 µm), TSV Cu 지름 2.2–2.6 µm, 스택 720 µm(775 µm 상한은 _facts F12·F13 에 따라 JEDEC 확정값으로 쓰지 않는다); 다른 값을 쓰면 '설정값'과 사유를 지문에 밝힌다, core die 사이 접합 간극(joint gap, NCP 접합 후) 11 µm(층 피치 46 µm; Micron 실측. 접합 전 도금 bump 높이와 혼동 금지), HCB pitch: HBM 용 공개 발표는 < 18 µm 수준(SK hynix Hot Chips 2026), 로직 SoIC 는 9 µm 이하 — 문항 설정값은 2–15 µm(그림 `f_hcb` 는 ≤ 10 µm 만 표시 가능하므로 그보다 크면 `f_note`/`f_table`) 이고 **HCB 에는 bump 간극이 없다**. HCB 의 nm 급 요구는 **표면 거칠기·Cu recess** 이며 die 휨 허용치는 µm 급이다("die 휨 100 nm" 류 서술 금지), µbump 당 전류 수십 mA 이하(평균 전류 밀도 10⁴ A/cm² 급이 EM 시험 영역), DRAM 접합부 온도 상한 85 / 95 °C(확장, refresh 2배). 105 °C 는 출처 확인 전 정답 근거로 쓰지 않는다. 스택 전력·열유속은 '보고된 범위' 로 단정하지 말고 **문항 설정값**으로만 준다
- **결과값이 비현실적이면(예: 최하단 die 150 °C 이상, 단일 pillar 100 kA/cm², 1 ppm 배율 오차가 125 µm 변위) 문항 설정 자체를 고친다.** "계산은 맞다" 는 변명이 되지 않는다.

### 2.5 용어 규약 (분야 간 통일 — 위반은 교차분야 검사에서 E)
- **N단 (N-Hi)** = core DRAM die N 장 + base die 1 장. 접합 계면(간극) 수 = **N** (base–core1 포함). "die 수" 라고 쓸 때는 base 포함 여부를 지문에 적는다. "12단 → 간극 11 개" 처럼 base 를 빼고 세는 서술은 금지.
- **적층 방향 (front-to-back)**: HBM core die 는 회로(BEOL)면이 아래를 향하게 쌓는다. 접합은 **위 die 앞면(BEOL 쪽) µbump ↔ 아래 die 뒷면 backside pad(TSV 끝)** 이다. base die 도 앞면이 아래(interposer 쪽)를 향하고, base 의 뒷면 TSV pad 가 core1 앞면 µbump 와 만난다. 최상단 core die 는 위에 접합할 die 가 없어 TSV·backside pad 가 없다(대개 더 두껍게 둔다). "앞면끼리(face-to-face)", "뒷면끼리" 접합 서술은 HBM core 적층에 쓰지 않는다(HCB 도 같은 방향).
- **스택 높이** = base die + N × (core die + 간극) (+ 최상단 mold 가 있으면 따로 명시). 최상단 core die 두께가 다르면 따로 준다.
- **Warpage 명칭(Smile / Cry)**: 이 문항집은 **"측정 자세를 그대로 둔 채 위에서 내려다본 형상"** 으로 부른다. 중앙이 기준면(chuck)에서 멀어진 볼록(∩) = **Cry (convex)**, 중앙이 기준면에 가까워진 오목(∪) = **Smile (concave)**. 자세(bump 면 아래 / BEOL 면 위)는 반드시 지문에 적고, die 자체의 휨 방향을 물을 때는 "BEOL 면 기준 볼록/오목" 으로 따로 묻는다. **(2026-11-20 오케스트레이터 승인으로 확정.)** 그림 `f_warp` 표는 DA Phase 1 에서 이 규약으로 교체되었다(sign 1 = ∩ = Cry).
- **refresh·온도 구간 판정 die**: DRAM 셀이 있는 **최하단 core die**(가장 뜨거운 core) 온도로 판정한다. 셀이 없는 base die 온도로 85/95 °C 구간·refresh 배수를 판정하지 않는다. (2026-11-21, EA 감사·XD W3 권고, 오케스트레이터 반영)
- **분야 간 공통 가정값**: 접합층 면적 열저항 등 여러 분야가 쓰는 가정값의 기준 범위는 `docs/agents/CONVENTIONS_W3.md` 를 따른다 (W3 수정 라운드에서 THERM 이 확정).
- 공법 명칭: **TC-NCF**, **MR-MUF**, **HCB (hybrid copper bonding, Cu–Cu hybrid bonding)**. "TCB" 는 장비 방식(열압착) 이름이고 NCF/NCP/MUF 와 결합해 쓴다.
- 단위 표기: µm (U+00B5), °C, Gb/s(핀 속도), GB/s(대역폭), W/m·K, m²·K/W, kA/cm². 숫자와 단위 사이 한 칸("5 µm"). 곱셈 ×, 나눗셈 ÷, 근사 ≈.

---

## 3. 문항 요건

### 3.1 지문 (stem / ctx+qt)
- **질문은 지문(또는 qt)의 마지막 한 문장**에 두고 **90자 이하**로 쓴다(화면 패널 머리에 "묻는 것" 으로 다시 표시됨, `W_QT_LONG`). 지문 전체는 권장 450자, 상한 520자(MIX 사례 ctx 700자).
- 하나의 문항은 **하나의 판단**을 묻는다. 두 독립 사실을 "A 이고 B 이다" 로 묶지 않는다.
- 묻는 문장은 하나이며 "…무엇입니까? / 얼마입니까? / 옳은 것은 무엇입니까?" 로 끝난다. **이중 의문형 금지**: "…무엇이라 하는가 무엇입니까", "…인가 무엇입니까".
- 부정형 발문("옳지 않은 것은")은 꼭 필요할 때만 쓰고 **'않은'** 을 지문 안에서 강조하지 않는다(화면 강조 불가) → 가급적 긍정형으로 바꾼다.
- 지문의 모든 조건은 풀이에 쓰이거나 오답을 가르는 데 쓰인다. 장식용 문장(“이 값은 설계 초기에 환산해 둡니다” 류)은 1문장 이내.
- `ctx + join + qt` 조립형은 **ctx 가 그 문항을 푸는 데 실제로 필요할 때만** 유지한다. ctx 가 qt 와 무관하면 `stem` 단일형으로 바꾼다(ctx/j/qt 삭제 → stem 작성). 조립 연결구("이 맥락에서 다음을 판단하십시오 —")는 새 문항에 쓰지 않는다.
- 지시어("이 상충", "위 조건")는 같은 지문 안에서 지시 대상이 있어야 한다.

### 3.2 정답 유일성
- 정답은 **지문 조건만으로** 하나로 결정되어야 한다. "가장 적절한" 을 쓰더라도 차점 오답이 전문가 기준으로 명확히 틀려야 한다.
- 수치 보기: 정답과 오답의 차이가 반올림 범위보다 커야 하고(최소 10 % 이상 또는 다른 유효숫자), **같은 값 보기 중복 금지**.
- 해설이 정답 번호를 오답처럼 서술하면(예: a=③ 인데 "②④③은 무관하다") **정답 키 자체를 의심하고 재검증**한다.

### 3.3 오답(distractor) 품질
- 각 오답은 **구체적인 오개념 하나**에 대응한다: 계산 실수(반지름/지름, 단위 10ⁿ, base die 누락, 간극 수 ±1), 개념 혼동(seam↔void, dishing↔erosion, HTS↔HTOL), 인과 역전, 다른 공법의 특성.
- **금지 오답**: 규정·관행·비용·장비 일정·색상·포장·작업자·조직 등 기술 외 사유("규정으로 정해져 있기 때문"), 다른 분야의 엉뚱한 항목("리프레시 주기와 채널 수" 를 dicing 문항에), 물리적으로 터무니없는 진술("패키지 두께를 10 mm 이상으로"), "모두 옳다/해당 없음".
- 형식 단서 금지:
  - 정답이 오답보다 눈에 띄게 길거나(25 % 초과) 유일하게 구체적이지 않게 한다. 네 보기의 길이·구조를 맞춘다.
  - 오답 3개는 "…때문" 인데 정답만 "…해서/…시점" 처럼 **어미가 다른 것 금지**. 마침표 유무도 통일.
  - 절대어(항상·전혀·반드시·오직)가 오답에만 있는 패턴 금지.
  - 정답만 지문 어휘를 그대로 반복하는 연상 단서 금지.
- 보기 길이 권장 40자, 상한 60자, 네 보기 길이를 비슷하게.
- 수치 보기는 오름차순 정렬을 권장한다(정답 위치는 EA 가 Phase 2 에서 조정하므로 신경 쓰지 않아도 된다).

### 3.4 해설 (exp)
- 구조: **① 정답 근거(원리·식) → ② 각 오답이 틀린 이유(번호 또는 내용으로 3개 모두) → ③ (선택) 실무 함의 1문장**.
- 계산 문항: **식 → 값 대입(단위 포함) → 결과(반올림 규칙)** 를 그대로 보이고, 각 오답 값이 어떤 실수에서 나오는지 적는다.
- ①–④ 참조는 **현재 보기 순서**와 일치해야 한다. 조사 규칙: ①은 ②는 ③은 ④는 / ①이 ②가 ③이 ④가 / ①을 ②를 ③을 ④를 / ①과 ②와 ③과 ④와. 묶음 참조("②③④는")는 마지막 번호에 맞춘다.
- 길이 80–400 자(상한 600). "②①④은 기술적 근거가 아니다" 식 번호 나열 해설은 금지.
- **수식 표기**(화면이 수식 구간을 고정폭 "계산" 상자로 꾸민다 — LAYOUT_RULES §2): 수식과 한글을 **띄어 쓴다**(`Δα = 16.5 − 2.7 = 13.8 ppm/K 이므로`). 지수는 `2.07e-03` 표기(자동 변환), `×10^` 금지. 문장 끝은 `. `, 소수점 뒤 공백 금지.
- 해설에서 처음 등장하는 새 사실(지문에 없는 수치·주장)은 2.1 의 출처 등급을 따른다.

### 3.5 제목 (title)
- 8–36 자(30 자 내외)의 **명사구**. 말줄임(…) 금지, 의문문 금지, 질문 문장 복사 금지.
- 정답을 드러내지 않는다(예: 정답이 Kirkendall void 인데 제목이 "Kirkendall void 의 생성 기구").
- 좋은 예: "Cu 측 계면에만 줄지어 생긴 공극", "16-Hi 스택의 높이 예산 판정". 나쁜 예: "TSV가 열을 빼는 통로로서 기대만큼 효과가 크지 않은 이유…".

### 3.6 그림 (fig) — `[템플릿 이름, params]`
- **k = 1 (상황도)**: 그림이 지문의 상황을 그린다. 그림에 표시되는 모든 수치(params 의 치수·온도·개수)는 **지문 수치와 동일**해야 하며, 지문에 없는 수치를 그림에만 두지 않는다(필요하면 지문에 추가). 기본값이 그려지는 키를 빠뜨리지 않는다(부록 A).
- 결과를 스스로 계산·판정해 그리는 템플릿(f_stack·f_therm·f_hcb·f_tsv)으로 그 결과를 묻는 k=1 문항은 **`hideResult: true` 필수**(부록 A.1).
- **그림은 정답을 보여 주면 안 된다.** 계산 문항에서 결과값(최대 단수, 높이, IMC 두께, 변위)을 params 에 넣으면 그림이 답을 알려 준다 → 결과값 대신 입력 조건만 그린다(예: `f_stack.n` 에 답인 최대 단수를 넣지 말 것; 필요하면 k=0 주제도로 바꾼다).
- **k = 0 (주제도)**: 주제의 일반 구조만 그린다. 문항과 무관한 결함(void, pinch, undercut)이나 지문과 다른 공법·기법 분기(LIT 문항에 OBIRCH 그림)를 그리지 않는다. `flag` 는 "주제: …".
- 지문이 "그림" 을 지칭하면 k=1 이어야 하며 그림이 실제로 그 내용을 보여야 한다.
- `f_note` 의 points 는 판단 관점을 주되 **정답 문장을 그대로 쓰지 않는다**.
- 템플릿별 params 형식·제약은 부록 A. 새 템플릿이 필요하면 브리프에 적고 EA 가 DA 와 조율한다.

### 3.7 지표 (metrics) — `[[아이콘, 라벨, 값], …]`
- 지문의 **조건·관측값**을 2–4 개 요약한다. 값은 지문과 **동일한 수치·단위**. label ≤ 12자, value ≤ 16자.
- 요약할 조건이 없으면 **`"metrics": []`** 로 둔다(화면의 "제시 조건" 띠가 숨는다). **키 자체는 지우지 않는다** — build 가 이 키를 읽는다.
- 메타 지표는 화면 "제시 조건" 띠에 "난이도: 고급", "묻는 것: 해당 항목" 처럼 그대로 보인다 → **최우선 수정 대상**.
- 메타 정보 금지: "난이도 · 초급", "묻는 것 · 이유", "세부 주제", "핵심어". (현재 2,580 문항이 이 형태 — 전부 교체)
- 계산 결과·정답을 지표에 넣지 않는다. 개념 문항이라 요약할 조건이 없으면 지문의 핵심 전제(예: "측정 자세 · bump 면 아래")를 쓴다.

### 3.8 문체 (한국어)
- 지문·해설은 **합니다체**로 통일. "…다." (해라체) 금지. 보기는 명사형 종결 또는 "~다" 평서형 중 하나로 **문항 안에서 통일**, 마침표 없음.
- 조사는 앞말에 붙여 쓴다: "TSV가", "5 µm의"(숫자+단위 뒤도 붙임). **예외: 해설의 수식 바로 뒤**(`Δα = 16.5 − 2.7 = 13.8 ppm/K 이므로`, `≈ 0.24 로`)는 띄어 쓴다 — 3.4 수식 표기 규칙이 우선하며 검사기 `I_JOSA_SPACE` 도 이 경우를 잡지 않는다.
- 영문 용어 뒤 조사는 **한글 독음의 받침 유무**로 고른다. 자동 검사기 `E_JOSA_EN` 의 사전(`EN_BATCHIM`)이 기준이다.

  | 받침 있음 → 이 / 은 / 을 / 과 | 받침 없음 → 가 / 는 / 를 / 와 |
  |---|---|
  | seam(심), scallop(스캘럽), dishing, erosion, delamination, crack, open, chipping, bonding, underfill(언더필), retention, channel, DRAM(디램), HBM(에이치비엠), SiCN, TIM(팀), reveal(리빌), smile | void(보이드), kerf, warpage, residue, short(쇼트), seed, bump(범프), pitch, pad(패드), pillar, solder, barrier, interposer, overlay, bridge, tape, TSV, IMC, CMP, NCF, HCB, Tg, EMC, ECC, PHY |

  예: "void가 생긴다", "seam이 남는다", "warpage를 줄인다", "Kirkendall void는".
- 영문 용어 표기: 공정 일반명사는 소문자(void, seam, warpage, underfill, reveal), 약어·고유명사는 정해진 대소문자(TSV, HBM3E, CoWoS-L, MR-MUF, TC-NCF, JESD22-A104). 같은 문항 안에서 한글/영문 혼용 금지(“Void”와 “void”, “Warpage”와 “휨”).
- "X(X)" 같은 치환 흔적, "…층을입니다" 같은 잘라 붙인 문장은 즉시 수정.

### 3.9 정답 위치 균형
- 분야 × 난이도별로 ①②③④ 각 **25 % ± 3 %**. 분야 에이전트는 신경 쓰지 않는다 — **EA 가 Phase 2 에서 일괄 조정**(해설 ①–④ 참조 동시 갱신). 단, 보기 문장 안에서 다른 보기를 번호로 지칭("①과 ②가 모두")하지 않는다(재배열 불가).

### 3.10 중복 · 근중복
- 동일 문항 금지. 핵심 텍스트(공유 ctx 제외)+보기의 5-gram Jaccard ≥ 0.80 인 근중복은 하나만 남기거나 묻는 지점을 바꾼다.
- **수치만 바꾼 동형 문항(템플릿 가족)은 분야당 가족별 최대 3개**, 그리고 가능하면 난이도별 1개. 나머지는 삭제하거나, 같은 식이라도 다른 판단(역산, 설계 선택, 결과 해석)을 묻도록 재작성한다.
- 교차 분야 중복은 XD 에이전트가 판정하고 한쪽만 남긴다(소유 분야 우선).

---

## 4. 레코드 스키마와 편집 규칙

```json
{ "id": "TSV-A-0016", "lv": "A", "title": "…", "stem": "…",       // 또는 "ctx","j","qt"
  "opts": ["…","…","…","…"], "a": 2, "exp": "…", "k": 1,
  "fig": ["f_tsv", { … }], "metrics": [["Ø","via 직경","8 µm"], …],
  "src": "선택 · 검증 가능한 출처",  "vx": ["W_코드", …],  "mv": "BSP",  "prev": "옛 id" }
```
- `id` 유지. 새 문항은 `CODE-LV-9xxx` (예: `TSV-A-9001`), lv 와 일치. 난이도를 바꿔 id 의 LV 가 달라지면 새 `CODE-LV-9xxx` 를 발급하고 `prev` 에 옛 id 를 남긴다(풀이 기록 연결용).
- 선택 필드: `src`(출처, 비표시), `vx`(검사기 면제 코드 — 사유는 리뷰 보고서에 기록; E 코드는 `WAIVABLE_E` 만), `mv`(다른 분야로 이관 제안 — EA 가 Phase 2 에서 이동). build 는 이 필드를 무시한다.
- 삭제는 리뷰 보고서에 id·사유 기록(“family 초과”, “근중복: X 와”, “사실 오류로 복구 불가” 등).

## 5. 자동 검사와 게이트
- `python3 tools/validate.py --domain CODE` — 자기 분야 이슈 목록(문항별). `--codes E_` 로 필터.
- `python3 tools/validate.py --domain CODE --gate` — **E 0 건이어야 완료**. W 는 수정하거나 `vx` + 사유.
- 이어서 `python3 tools/build.py` 와 `node tools/smoke.js dist/HBM_quiz.html` 가 오류 없이 끝나야 한다.
- 자동 검사로 잡히지 않는 것(사실 정확성, 정답 유일성, 오답 매력도, 난이도 적합성)은 **에이전트가 문항마다 직접** 판단한다. 자동 검사 통과 ≠ 품질 통과.

---

## 부록 A. 그림 템플릿 params (template.html DA Phase 1 이후, 2026-11-20 갱신)

허용 범위·글자 수 상한의 **원본은 `docs/agents/LAYOUT_RULES.md` §3–4** 이다(DA 소유). 아래는 그 사양에 **내용 규칙**을 더한 것이며, 둘이 다르면 LAYOUT_RULES 의 범위·상한을 따른다.

공통: `flag`(≤ 20자, k=0 이면 "주제: …"), `note`(캡션 교체 ≤ 40자), `bullet`/`hint`(≤ 44자). k=1 이면 그림의 모든 숫자는 지문과 같아야 한다.

### A.1 `hideResult: true` — 의무 조건
그림이 계산·판정 결과를 스스로 표시하는 템플릿은 **그 결과를 묻는 k=1 문항에서 반드시 `hideResult: true`** 를 넣는다(검사기 `E_FIG_HIDE_RESULT`).
| 템플릿 | 숨겨지는 것 | 의무가 되는 문항 |
|---|---|---|
| `f_stack` | die 총 장수·간극 수·pad die 수·스택 높이·상한 판정색 | 높이·최대 단수·간극 수·상한 판정을 묻는 문항 |
| `f_therm` | core/base 온도(최상단 `tTop` 만 표시), R·ΔT·상한 판정색 | 온도·ΔT·상한 판정을 묻는 문항 |
| `f_hcb` | 허용치 "초과/이내" 판정 | overlay 판정을 묻는 문항 |
| `f_tsv` | aspect ratio 값 | AR 을 묻는 문항 |
`hideResult` 를 써도 **입력 params 에 정답 값을 넣으면 여전히 노출**이다(예: 최대 단수 문항에서 `f_stack.n` = 답). 그런 문항은 k=0 주제도로 바꾼다.

### A.2 템플릿별 params 와 내용 규칙
| 템플릿 | params (범위는 LAYOUT_RULES §4) | 내용 규칙 · 주의 |
|---|---|---|
| `f_tsv` | `dia_um`, `depth_um`, `ar`(생략 시 depth/dia 자동 — **생략 권장**), `fill`: good·void·seam·pinch, `scallop` 0·1, `scallopPitch`, `scallopDepth`, `barrier`, `overburden`, `taper`, `hideResult` | `ar` 을 주면 depth/dia 와 일치(E_FIG_INTERNAL). `scallop: 0` 이면 scallop 치수 미표시. k=0 은 `fill: "good"` |
| `f_cmp` | `densA`, `densB`(%, 그래프에 A/B 표식), `dish_nm`, `erosion_nm`, `nA`, `nB` | 경향 그래프는 설명용 |
| `f_bs` | `step` 0–7 (0 reveal … 7 seed etching), `defect`: none·undercut·residue(step 7), `ox1`, `sin`, `ox2`(nm), `ni_um` | 공정 흐름 고정 8단계 — "이 공정 흐름에서는" 으로 한정 |
| `f_bump` | `pillar_um`, `solder_um`, `imc_um`, `niBarrier`(라벨 Ni₃Sn₄/(Cu,Ni)₆Sn₅), `kirkendall`, `em`+`j_kA`, `temp`, `k`, `hours`, `tmax`, `ymax`, `bullet` | 계산 결과를 `imc_um` 에 넣지 말 것(측정값만) |
| `f_saw` | `method`: blade·lg·stealth·plasma·deeplaser·dbg, `kerf_um`, `haz_um`, `chip_um`, `bullet` | 표는 "대표 범위" — kerf 는 방식별 범위 안으로 |
| `f_bond` | `method`: ncf·mrmuf·hcb, `pitch_um`, `gap_um`, `voids` 0–3, `filler_trap`, `nonwet`, **`dish`**, `bullet` | **hcb: dishing 미접합 pad 는 `dish: true` 일 때만 그려진다(기본 없음)** — dishing 을 근거로 쓰는 hcb 문항은 `dish: true` 필수(E_FIG_DISH_OPTIN). **hcb 에 `gap_um` 금지**(표시 안 됨, HCB 는 bump 간극 없음). 결함 표식(voids·filler_trap·nonwet·dish)은 동시에 2개 이하 |
| `f_warp` | `ref`: bump-down·beol-up, `sign` 1 = ∩ = **Cry** / −1 = ∪ = **Smile**, `mag_um`, `tg`, `temp` | 표가 확정 규약(2.5)으로 교체됨. 정답 명칭과 sign 일치(E_FIG_WARP_NAME) |
| `f_sip` | `type`: cowos-s·cowos-r·cowos-l·emib·emib-t, `nHBM` 1–8, **`lines`**, `bullet` | **`lines` 생략 시 숫자 없는 "HBM I/O 배선"**. 지문이 1,024 / 2,048 배선을 말하면 `lines` 를 그 값으로(E_FIG_SIP_LINES). HBM3E = 1024, HBM4 = 2048 |
| `f_therm` | **`core`**(권장, n = core+1) 또는 `n`(base 포함 총 die 수), `q_Wmm2`, `tTop`, `limit`, `layers` ≤ 5행, `hideResult` | 새 문항은 `core` 로. N단 → `core: N`. 결과 온도는 현실 범위(≈ 110 °C 이하) |
| `f_fa` | `tech`: lit·obirch·eotpr·xrm · `hot`, `fov_um`, `depth` · `feats` ≤ 4 · `dz`, `zpeak` | 지문 기법과 tech 일치 |
| `f_rel` | `seq` ≤ 4행, `cur`, `fails` ≤ 5점, `xlab`, `xmax`, `ymax`, `crit`, `hint`, `bullet` | 기본 seq 첫 행은 JESD22-A113 preconditioning. 기본 seq 의 TC "1000 cycle" 은 JESD47(condition B 700 cycle)과 다르다 — JEDEC 자격 시험을 묻는 문항은 `seq` 를 직접 준다(DA 수정 요청 중). HTOL·HTS 는 `xlab`/`xmax` 를 시간 축으로 |
| `f_stack` | `n`(core die 수), `highlight`, `gap_um`, `h_um`, `limit_um`, `bullet`, `hideResult` | 계산 답을 `n`/`h_um` 에 넣지 말 것 |
| `f_hcb` | `pitch_um` ≤ 10, `tol_nm`, `off_nm`, `dish_nm`, `bullet`, `hideResult` | |
| `f_plot` | `title`, `x`/`y`{min,max,ticks ≤ 6,lab}, `series` ≤ 4, `marks` ≤ 3, `bullets` ≤ 3 | 데이터 해석형 고급의 주력 |
| `f_film` | `layers` ≤ 9, `roles` ≤ 5, `bullets` ≤ 3, `flags` ≤ 2 | |
| `f_ubj` | µbump 접합 단면. `n`(≤6)·`st`[bump별: ok·nonwet·hip·open·bridge·squeeze·fullimc·imcthick·imcgrow·kv·em·crowd·void·trap·dendrite·unfill]·`fillet`(+`filletTag`)·`stage`("pre"=접합 전)·`h`/`w`(bump별 높이·폭 배율)·`cap`·`fill`(none·ncf·muf)·`ni`·`imc`(one·two·none)·`zoom`(확대할 bump 번호)·`layerNames`·`names`(재료 이름 범례·확대 라벨)·`tags`·`tsv`·`chain`·`shear`·`I`·`electron`·`trace`·`dims`{pitch,gap,dia}(문자열 그대로)·`cand`(후보 치수 A·B·C)·`residue`·`cmp`(ball·hcb) | 불량 이름은 그리지 않고 이상 부위는 "관찰 부위 (A)". 재료명이 정답이면 `names` 를 끄고 `layerNames` 로 "층 A" |
| `f_plate` | through-mask 도금 단면 패널. `steps`(seed·pr·plate·strip·etch·reflow 중, 준 순서대로 ≤6)·`labels`·`hideNames`((가)(나)…) | 순서 문항은 섞어서 준다 |
| `f_wet` | 녹은 solder 접촉각. `drops`[{surf: clean·oxide, theta, label, vapor}] ≤3·`hideAngle` | 같은 부피로 그림 |
| `f_note` | `title` ≤ 22자, `points` ≤ 4(각 ≤ 50자), `ask` ≤ 12자 | points 는 **판단 관점** — 정답 문장 금지 |
| **`f_table`** | `title`, `unit`, `cols` ≤ 5, `rows` ≤ 7 × 5(셀 ≤ 14자), `hl`/`hlRow`/`hlCol`, `notes` ≤ 3 | 고급 '실측 데이터 해석' 용. 강조(hl)가 정답을 가리키지 않게 — 관측 대상만 강조 |
| **`f_wafermap`** | `title`, `grid` 9–25, `values` 또는 `pattern`(edge·center·ring·notch·random·quadrant), `scale`, `bin`, `marks` ≤ 4, `bullets` ≤ 3, `seed` | 맵 패턴을 묻는 문항에서 bullets·marks 로 원인을 쓰지 말 것 |

예시는 LAYOUT_RULES §4 참조.


## 부록 B. FACT §9 정정 제안 검토 결과 (2026-11-20, EA)

| # | 제안 | 판정 | 반영 위치 · 근거 |
|---|---|---|---|
| 1 | HBM3 단수 4/8/12-Hi (16-Hi 는 향후 확장) | **수용** | 2.2 표. JEDEC HBM3 발표문 [S] 문구와 일치 |
| 2 | 패키지 높이 775 µm 굵게 해제 + 각주 | **수용** | 2.2 각주 ¹. 정답 근거는 [S]/[V] 만 쓴다는 2.1 원칙과 일치. JESD270-4 본문 확인 시 복원 |
| 3 | HBM2E 문서명(JESD235C), HBM3E 업체 9.2–10 Gb/s, HBM4 의 HBM3 컨트롤러 하위 호환 | **수용** | 2.2 표. 하위 호환은 JEDEC 발표문 [S] 명시 — EA 가 Phase 1 브리프(PROD §2)에서 PROD-I-0003 의 "HBM4 비호환" 을 '유지 가치' 로 적은 것은 **철회**(F04 정정이 우선) |
| 4 | JESD47 조건(TC B 700 / G 850 cycle, 표본 77·25, HTOL·HTSL·bHAST 조건) | **수용(판 번호 단서 포함)** | 2.3 표. FACT 가 JESD47G 원문을 직접 확인. 최신판 차이 가능성이 있어 문항에는 판 번호·표본 수를 정답으로 묻지 않도록 단서 추가 |
| 5 | HCB pad pitch "≤ 10 µm" 완화, die 휨 µm 급 | **부분 수용** | 2.4. 공개 발표(< 18 µm)와 로직(≤ 9 µm)을 함께 적고 문항 설정값 2–15 µm 로 정함. "≤ 10 µm" 를 버리지 않은 이유: `f_hcb` 그림 표시 범위가 1–10 µm(LAYOUT_RULES §4)라 그 이상은 그림 대신 다른 템플릿을 쓰도록 안내 필요. die 휨 µm 급 문구는 그대로 수용 |
| 6 | 105 °C 근거 미확인 표기, 열유속은 '문항 설정값' | **수용** | 2.4 |
| 부기 | `f_rel` 기본 seq TC 1000 cycle ≠ JESD47 700 | **수용** | 부록 A `f_rel` 행 + `EA_to_DA.md` §15 |
