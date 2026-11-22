# 레이아웃 규칙 (LAYOUT_RULES) — 문항·그림 작성 시 지킬 화면 제약

- 소유: DA (Design Agent) · 기준: `template.html` (2026-11-20, Phase 1) · 내용 기준은 EA 의 `STANDARDS.md`, 이 문서는 **화면에 들어가는가**만 다룬다.
- 검사: `python3 tools/build.py --out <scratch>/q.html && node tools/smoke.js <scratch>/q.html && node tools/layout_check.js --html <scratch>/q.html --out <scratch>/layout` — 결함 문항 수가 기준선(`docs/reviews/_layout_baseline.json`)보다 늘면 실패(exit 1). `--help` 로 옵션 확인. 결과 기본 위치는 `$TMPDIR/hbm_layout_check/`; 공용 `docs/reviews/_layout_latest.*` 는 **`--publish` 를 줄 때만** 갱신된다(DA·오케스트레이터 전용).
- 글자 수는 **한글 1자 = 1, 영문·숫자·기호 1자 ≈ 0.6** 으로 센 "폭" 기준이다(그림 안 라벨). 화면 텍스트(제목·보기·지문)는 그냥 글자 수.

## 1. 문항 텍스트

| 필드 | 권장 | 상한 | 화면에서 일어나는 일 |
|---|---|---|---|
| `title` | 20–32자 | **36자** | 데스크톱 h1 1–2줄. **말줄임 `…` 금지**(현재 1,771 문항이 `…` 로 끝남 → 잘린 제목으로 보임). 의문문 금지 |
| `stem` (또는 `ctx`+`j`+`qt`) | ≤ 450자 | **520자** (MIX 공유 ctx ≤ 700) | 1440×900 에서 약 10줄을 넘으면 지문 상자 안에서 스크롤된다(그림 영역 보호). 지표·그림은 항상 보인다 |
| `qt` 의 마지막 문장 | ≤ 90자 | — | 오른쪽 패널 머리에 "묻는 것"으로 다시 표시된다. 질문은 **마지막 한 문장**에 두고 `…까?` / `…시오.` 로 끝낸다 |
| `opts[i]` | ≤ 40자 | **60자** (예외 90) | 패널 폭 340–400px 에서 한 줄 ≈ 20자. 60자 = 3줄. 네 보기 길이를 비슷하게 |
| `exp` | ≤ 400자 | **600자** | 문장(`. ` 뒤 공백) 단위로 문단이 나뉜다. 아래 2절 서식 사용 |
| `metrics` | 2–4개 | **0–4개** | 0개면 "제시 조건" 띠 전체가 숨는다. 키는 반드시 있어야 함(`[]`) |
| metric `[icon, label, value]` | icon 1자, label ≤ 10자, value ≤ 12자 | label **12자**, value **16자** | 칸 폭 ≥ 140px 자동 줄바꿈. 현재 value 16자 초과 40건, label 12자 초과 18건 |

## 2. 해설(`exp`) 서식 — 화면이 자동으로 꾸며 주는 규칙
- **계산식**: 한글이 끼지 않은 구간에 `=`, `≈`, `×`, `÷` 와 숫자가 있으면 고정폭 수식으로 표시되고, 그 문장은 점선 "계산" 상자가 된다. 수식은 한글과 **띄어서** 쓴다: `Δα = 16.5 − 2.7 = 13.8 ppm/K 이므로` (O) / `Δα=16.5−2.7=13.8ppm/K이므로` (X — 한 덩어리로 묶이지 않음).
- 지수: `2.07e-03`, `13.8e-6` 은 자동으로 `2.07×10⁻³` 로 바뀐다. 직접 `×10^` 을 쓰지 말 것.
- 보기 참조 `①②③④` 는 강조색으로 표시된다(현재 보기 순서와 일치해야 함 — STANDARDS 3.4).
- 출처: 레코드에 `src` (문자열 · 배열 · `{title, doc, year, url, note}`) 가 있으면 해설 아래 회색 "근거" 각주로 표시되고 **`src` 가 우선**한다. 없으면 본문 끝 ` [근거] …` 꼬리표를 각주로 분리한다(Phase 2 에서 꼬리표 제거 예정). ※ `src` 가 화면에 나오려면 `tools/build.py` 가 `src` 를 DB 에 넣어야 한다(현재 미반영 — 오케스트레이터 확인 대기).
- 문장 끝은 `. ` (마침표+공백). 소수점 뒤에는 공백을 두지 않는다(문장 분리 기준).

## 3. 그림 공통 (fig params)

| 항목 | 상한 | 비고 |
|---|---|---|
| `flag` (카드 머리말 칩) | 20자 | k=0 이면 "주제: …" |
| `note` (그림 아래 캡션 교체) | 40자 | 한 줄 |
| `bullet` / `hint` (오른쪽 열 pill) | 44자 (한 줄 ≈ 24자, 최대 2줄) | |
| `bullets[]` (f_plot · f_film · f_wafermap) | 3개, 각 44자 | |
| 그래프·표 `title` (f_plot · f_note · f_table · f_wafermap) | 22자 | |
| 표식 라벨 (`marks[][1]`, `feats[][2]`, `flags[][1]`) | 12자 | |
| 숫자 | 표시 자리 ≤ 6자 (`1,024`, `0.35`) | 단위는 µm · nm · °C · % 처럼 짧게 |

자동 처리(분야 에이전트가 신경 쓰지 않아도 되는 것): 라벨 글자가 상자보다 크면 상자를 키우고, 라벨(pill)끼리 겹치면 가장 가까운 빈 자리로 옮기며 지시선 끝을 따라 옮긴다(`figPost`). 지시선이 다른 글자·pill 을 가로지르면 **시작점(결함·치수 위치)은 그대로 두고** 직선·ㄱ자·옆 통로 ㄷ자 경로 중 덜 가로지르는 것으로 바꾼다(2026-11-21). 폭 추정이 커서 두 줄 높이로 잡힌 pill 이 실제 한 줄이면 높이를 되돌린다. 상자 안 글자는 상자 높이·폭에 맞춰 최대 5.5pt 까지 줄인다. **그래도 위 상한을 넘기면 줄바꿈이 늘어 다른 요소와 겹칠 수 있다.**

### 정답 노출 방지 — `hideResult: true`
그림이 계산·판정 결과를 표시하는 템플릿에서 계산·판정을 묻는 문항은 `hideResult: true` 를 넣는다. 입력 조건만 그리고 결과 칸은 `?` 로 둔다.

| 템플릿 | `hideResult` 가 숨기는 것 |
|---|---|
| `f_stack` | 표의 die 총 장수 · 간극 수 · backside pad die 수 · 스택 높이, 간극 개수 라벨, 높이 상한 pill 의 초과/이내 색 |
| `f_therm` | core·base die 온도(최상단 `tTop` 만 표시), 층별 R · 합계, ΔT, base 온도, 상한 대비 색, "간극 수 = core die 수 (N개)" pill |
| `f_hcb` | 허용치 대비 "초과/이내" 판정과 색 |
| `f_tsv` | aspect ratio 값 |
| `f_warp` | Smile/Cry 이름, 자세별 die BEOL 면 볼록·오목 (`hideNames` 와 같음) |
| `f_bump` | Kirkendall · current crowding 결함 이름, IMC 상(Cu₆Sn₅ 등) 이름 (`hideLabels` 와 같음) |

## 4. 템플릿별 params 허용 범위

범위 밖 값은 그림이 잘리거나 모양이 무너진다. (현재 데이터의 실제 범위를 함께 적음)

| 템플릿 | params · 허용 범위 |
|---|---|
| `f_tsv` | `dia_um` 2–12, `depth_um` 20–150, `ar` (생략 시 depth/dia 소수 1자리 자동), `fill`: good·void·seam·pinch, `scallop`: 0·1 (**0 이면 scallop 치수 미표시**, "scallop 없음"), `scallopPitch` 0.2–0.6 µm, `scallopDepth` 20–120 nm, `barrier`, `overburden`, `taper` 0.6–1.0, `hideResult` |
| `f_cmp` | `densA` 5–40, `densB` 30–80 (x축 0–80 %, 두 값이 A/B 표식으로 그려짐), `dish_nm` 5–150, `erosion_nm` 10–80, `nA` 3–5, `nB` 6–10 |
| `f_bs` | `step` 0–7, `defect`: none·undercut·residue (step 7 에서만), `ox1` 100–500, `sin` 100–300, `ox2` 300–800 nm, `ni_um` 1–5, **`notes: false`** (희생막·CMP·"최종 절연막 = SiO2/SiN 2층" 주석을 끄고 결함 라벨을 "관찰 부위 (A)" 로), **`labels: false`** (막 이름까지 숨김: 절연막은 회색 "막 1 · 300nm" 식, seed·Ni 는 "seed 층"·"pad 도금 2 µm", 오른쪽 공정 순서도 "막 1 증착 … 평탄화 … seed 제거" — 막 구성·순서를 묻는 문항용, `notes: false` 포함) |
| `f_bump` | `pillar_um` 10–60, `solder_um` 5–25, `imc_um` 0.5–6, `niBarrier` (IMC 라벨이 Ni₃Sn₄ / (Cu,Ni)₆Sn₅ 로 바뀜), `kirkendall`, `em` + `j_kA` (≤ 4자리), `temp`, `k`, `hours` ≤ `tmax`, **`tmax`** (기본 1000 h), **`ymax`** (기본 8 µm), **`hideLabels`** (Kirkendall·EM 결함 라벨을 "관찰된 void (A)"·"결함 위치 (B)" 로, IMC 상 이름 생략 — 명칭·기구를 묻는 문항용, `hideResult` 도 같은 효과), `bullet`. **`k` 가 없으면 성장 곡선을 그리지 않는다**(축·식 라벨만) |
| `f_saw` | `method`: blade·lg·stealth·plasma·deeplaser·dbg (비교표에 **DBG 행**이 따로 있고 dbg 면 그 행이 강조됨), `kerf_um` 0–60, `haz_um` 2–20, `chip_um` 5–30, **`notes: false`** (개념 주석·기본 bullet 을 끄고 지시선 라벨을 "관찰 부위 (A/B)" 로 — 개념을 묻는 문항용), `bullet` (표는 "대표 범위" 캡션 표시) |
| `f_bond` | `method`: ncf·mrmuf·hcb, `pitch_um` 5–60, `gap_um` 3–15 (**hcb 에는 주지 말 것 — 표시 안 함**), `voids` 0–3, `filler_trap`, `nonwet`, **`dish: true`** (hcb 에서 dishing 미접합 pad 를 그릴 때만), `bullet` |
| `f_warp` | `ref`: bump-down·beol-up, `sign` ±1 (1 = 중앙이 기준면에서 멂 ∩ = **Cry**, −1 = 가까움 ∪ = **Smile**), `mag_um` 10–200, `tg` 50–240, `temp` 25–260, **`hideNames`** (`hideResult` 도 같음: 주석의 "= Cry/Smile" 과 명명표의 이름·die 면 볼록/오목 칸을 "?" 로 — 명명·형상 판정 문항 필수) |
| `f_sip` | `type`: cowos-s·cowos-r·cowos-l·emib·emib-t, `nHBM` **1–8**, **`lines`** (예 1024, 2048 — 생략 시 "HBM I/O 배선"), **`msg`** (오른쪽 요점 pill 교체, ≤ 44자), `bullet` |
| `f_therm` | **`core`** (core die 수, 권장 — n = core+1 로 계산) 또는 `n` (base 포함 총 die 수) 4–21, `q_Wmm2` 0.01–1, `tTop`, `limit`, `layers` ≤ 5행 (이름 ≤ 10자), `hideResult`. core 12 초과 시 die 라벨이 작아진다 |
| `f_fa` | `tech`: lit·obirch·eotpr·xrm · `hot` [0–1, 0–1], `fov_um`, `depth` 5–50, `feats` ≤ 4 (라벨 ≤ 10자), `dz` 5–30, `zpeak` 0–45 |
| `f_rel` | `seq` ≤ 4행 [문서 ≤ 12자, 시험명 ≤ 20자, 조건 ≤ 16자], `cur`, `fails` ≤ 5점 (x ≤ `xmax`, y ≤ `ymax`), **`xlab`** (기본 "TC cycle 수"), **`xmax`** (기본 1000), **`ymax`** (기본 10 %), **`tcCycles`** (기본 700 — 기본 seq 의 JESD22-A104 cond. B 행과, TC 축일 때 "규격 N cycle" 점선에 쓰임), `crit`, `hint`, `bullet` |
| `f_stack` | `n` (core die 수) 4–24, `highlight`: height·midcore·base·gap·topcore, `gap_um`, `h_um`, `limit_um`, `bullet`, `hideResult`. **수치는 준 것만 그린다**(2026-11-21): `gap_um` 없으면 "접합 간극 N개" 만(µm 없음), `h_um` 없으면 높이 칸 "—"(산식만), `limit_um` 없으면 높이 상한 pill 생략 |
| `f_hcb` | `pitch_um` 1–10, **패널은 opt-in**: `off_nm` 0–420 (있을 때만 overlay 오차 화살표·라벨), `tol_nm` 20–300 (있을 때만 허용 원·초과/이내 판정), `dish_nm` 1–16 (있을 때만 dishing 미접합 pad·라벨·"dishing > Cu 팽창량" 요점), `bullet`, `hideResult` (판정 "?", dishing 결과 "?") |
| `f_plot` | `title`, `x`/`y` {min, max, ticks ≤ 6개 (라벨 ≤ 5자), lab ≤ 24자}, `series` ≤ 4 {name ≤ 22자, color "RRGGBB", pts ≤ 12, dash}, `marks` ≤ 3 [x, 라벨 ≤ 12자], `bullets` ≤ 3 |
| `f_film` | `layers` ≤ 9 [이름 ≤ 18자, 상대두께, 색], `roles` ≤ 5행 [층, 두께, 역할 ≤ 14자], `bullets` ≤ 3, `flags` ≤ 2 |
| `f_note` | `title` ≤ 22자, `points` ≤ 4 (각 ≤ 50자, **판단 관점** — 정답 문장 금지), `ask` ≤ 12자 |
| **`f_table`** (신규) | `title` ≤ 22자, `unit`, `cols` ≤ 5 (머리글 ≤ 8자), `rows` ≤ 7행 × ≤ 5열 (셀 ≤ 14자, 숫자는 문자열 가능), 강조 `hl: [행, 열]` (행은 rows 기준 0부터) 또는 `hlRow` / `hlCol`, `notes` ≤ 3 (각 ≤ 44자) |
| **`f_wafermap`** (신규) | `title` ≤ 22자, `grid` 9–25 (기본 15), `values` grid×grid 숫자 (`null` = die 없음) **또는** `pattern`: edge·center·ring·notch·random·quadrant, `scale` {min, max, unit}, `bin: true` (합격/불량 2색, values 는 0/1 — `scale` 없이도 1 = 불량으로 칠한다), `marks` ≤ 4 [열, 행, 라벨 ≤ 12자], `bullets` ≤ 3, `seed` (random 배치 변경) |

예시 (f_table):
```json
["f_table", {"title": "lot 별 die shear 강도", "unit": "gf", "cols": ["lot", "평균", "최소", "표준편차", "판정"],
  "rows": [["A01", "182", "151", "9.8", "합격"], ["A03", "149", "98", "21.4", "불합격"]], "hlRow": 1,
  "notes": ["판정 기준: 최소 120 gf 이상"], "flag": "관측: lot A03"}]
```
예시 (f_wafermap):
```json
["f_wafermap", {"title": "bump 높이 분포", "grid": 17, "pattern": "edge", "scale": {"min": 24, "max": 31, "unit": "µm"},
  "marks": [[1, 8, "가장자리 최대 31 µm"]], "bullets": ["가장자리로 갈수록 높아진다"]}]
```

## 5. 레코드 확장 필드
`src`, `vx`, `mv`, `prev`, 파일 수준 `legacy_prefix` 등은 `build.py` 가 읽지 않으므로 화면에 영향이 없다. 그림 params 안의 모르는 키도 무시된다.

## 6. 분야 수
분야 목록·필터·결과 차트는 `data/NN_CODE.json` 의 `domain` 수(현재 14)를 그대로 따른다. 분야 색은 16색 팔레트로 14개까지 모두 다르다.

## 7. 템플릿 고정 문구 변경 기록 (2026-11-21, `_facts.md` · STANDARDS 대조)

| 템플릿 | 이전 | 현재 | 근거 |
|---|---|---|---|
| `f_sip` cowos-s | "전면 Si → reticle 크기가 상한" | "전면 Si 인터포저 · stitching 으로 약 3.3× reticle 까지" | F34 |
| `f_sip` cowos-r | "TSV가 없어 전원은 substrate 경유 · 저비용" | "TSV 없이 RDL 적층 via 로 수직 연결 · 한계는 배선 피치" (단면에 적층 via 점선) | F36 · F37 |
| `f_sip` cowos-l | "미세배선이 필요한 구간만 bridge로 국한" | "미세배선 구간만 LSI bridge · 수직 경로는 TIV · 전역 RDL" (단면에 TIV 선) | F37 |
| `f_sip` emib | "전원은 bridge를 통과하지 못하고 substrate 경유" | "bridge 는 신호 전용 · 전원은 기판 via 로 바로 내려간다" | F37 |
| `f_stack` 표 산식 | 간극 "die 수 − 1" · 높이 "die 두께 × 장수 + 간극" | 간극 "= core 수 (base–core1 포함)" · pad "base + core, top core 제외" · 높이 "base + N × (core + 간극)" | STANDARDS 2.5 |
| `f_stack` pill | "패키지 높이 상한 775 µm" | "높이 상한 (설계 조건) 775 µm" | F13 |
| `f_bond` 표 | "gap 하한 5–7 µm / 7 µm 급", 열 경로 "EMC 전도 유리" | "칩 간 간격 ≈ 7 µm / µm 급", "EMC 유리" | F24 · F33 |
| `f_rel` | 기본 TC 행 "−55/+125 °C, 1000 cycle", "판정 기준선 1%" | "cond. B (−55/+125 °C) × 700" (`tcCycles`), "판정 기준선 (사내) 1%" | F41 · F42 · F43 |
| `f_fa` eotpr | "패키지 내부 경로에는 TDR 이 아니라 EOTPR 을 쓴다" | "패키지 내부 미세 경로는 분해능이 높은 EOTPR 로 본다" | 과잉 단정 완화 |
| `f_hcb` 기본 bullet | "particle 1개가 수 µm 범위 미접합을 만든다" | "particle 1개가 자기보다 훨씬 넓은 미접합을 만든다" | 범위 과소 표기 완화 |

이 문구를 정답 근거로 쓰던 문항은 지문·해설을 새 문구에 맞춰야 한다(특히 CoWoS-R 전원 경로, "reticle 이 상한", "12단 → 간극 11개").
| `f_bump` (2026-11-21) | `k` 미지정 시 기본 k = 0.22 곡선 | `k` 없으면 곡선 생략 | 문항에 없는 성장 속도를 그림이 만들어 내지 않도록 |
| `f_bump` (2026-11-21) | 결함 라벨 항상 명칭 표기 | `hideLabels` / `hideResult` 로 일반 표기 | 정답 노출 방지 (BUMP 요청) |
| `f_saw` (2026-11-21) | dbg 면 blade 행 강조, 개념 주석 항상 표시 | DBG 행 추가·강조, `notes: false` 로 주석 끔 | 정답 노출 방지 (SAW 요청) |
| `f_therm` (2026-11-21) | `hideResult` 에도 "간극 수 = core die 수 (N개)" 표시 | `hideResult` 면 이 pill 생략 | 정답 노출 방지 (THERM 요청) |
| 축 눈금 (공통) | 붙어 있는 x 눈금 글자가 겹침 | 0.34 in 미만으로 붙은 눈금 글자는 생략(눈금선은 유지) | DRAM-A-9019 겹침 |
| `f_bs` (2026-11-21) | 희생막·CMP·최종 절연막 주석 항상 표시 | `notes: false` 로 끔 | 정답 노출 방지 (BSP 요청) |
| `f_hcb` (2026-11-21) | params 없어도 overlay 150 nm·허용 100 nm "초과"·dishing 8 nm 미접합을 기본으로 그림 | `off_nm` / `tol_nm` / `dish_nm` 을 준 패널만 그림(없으면 정렬된 pad 와 정상 접합 단면) | 문항에 없는 판정이 그림에 나오지 않도록 (BSP 요청) |
| `f_warp` (2026-11-21) | "∩ = Cry" 주석·명명표 항상 표시 | `hideNames` / `hideResult` 면 이름·볼록/오목을 "?" 로 | 정답 노출 방지 (WARP 요청) |
| `f_stack` (2026-11-21, DA 최종) | `gap_um`·`h_um`·`limit_um` 이 없으면 기본 7 µm · n×50+100 µm · 775 µm 를 그림 | 준 값만 표시(간극 "N개", 높이 "—", 상한 pill 생략) | EA_to_DA §16 · STANDARDS 3.6. 영향 90 문항(아래) |
| `f_bs` (2026-11-21, DA 최종) | `notes: false` 에도 막 이름 라벨·공정 순서에 SiO2/SiN 표시 | `labels: false` 추가(막 1·2·3 + 두께, 공정 순서 일반 표기) | EA_to_DA §17. 현재 사용 문항 0 → 영향 없음 |
| `f_note` (2026-11-21, DA 최종) | 관점 번호 ①②③④ | Ⅰ Ⅱ Ⅲ Ⅳ | 보기 번호(①–④)와 혼동 — EA 가 지표 아이콘을 Ⅰ Ⅱ Ⅲ 로 바꾼 것과 같은 이유. 해설에서 관점 번호를 인용한 문항 0 |
| `f_wafermap` (2026-11-21, DA 최종) | `bin: true` + `values` 0/1 + `scale` 없음 → 기본 scale 0–100 으로 나눠 불량이 모두 합격색 | `scale` 없으면 values 0/1 그대로 | **SAW-A-9005** 그림에 불량 두 행이 안 보이던 버그 |
| `f_sip` 단면 (2026-11-21, DA 최종) | 두께 배율이 작아 interposer·RDL 이름이 pill 로 밀려나 substrate 아래에 놓임, 수직 연결선이 글자 관통 | 두께 방향 배율 0.16 in/단위로 키워 층 이름을 층 안에, TSV/via/TIV 선은 칩 아래 양 끝, EMIB 는 substrate 이름을 bridge 왼쪽에 | 그림 의미(층 순서·연결 경로) 불변 |
| `f_fa` eotpr (2026-11-21, DA 최종) | 위치 이름 pill 이 파형 봉우리를 가림, 구조 대응 단면의 interposer 이름이 substrate 아래로 밀림 | y 축 −50–100 mV 로 넓혀 이름은 봉우리 위 빈 띠에, 단면 두께 배율 키움, probe 라벨은 HBM 위로 | 파형·표식 위치 불변 |
| `f_warp` · `f_rel` · `f_saw` · `f_hcb` (2026-11-21) | 기준선·규격선이 값 pill 위로 그려짐, 곡선 극값 위에 Tg pill, "Si" 이름이 절단선 밑, SiCN 라벨이 왼쪽 overlay 칸 침범 | 선을 먼저 긋고 pill 을 위에, Tg·측정 pill 은 곡선이 없는 쪽, "Si" 는 왼쪽 위, SiCN 라벨은 단면 아래 | E5 0 |

`f_stack` 수치 규칙 영향 문항(템플릿만 바뀜, 데이터 무수정): `gap_um` 없음 84(k=0 80 · k>0 4: BUMP-A-9005, SIP-I-0137, PROD-I-0026, PROD-I-9012), 높이 "—" 15(hideResult 없이 `h_um` 없음: TSV-B-0078, BSP-A-9043, BSP-A-9053, BUMP-A-9005, COW-I-0112, COW-I-9011, COW-I-9031, COW-A-0133, COW-A-9017, WARP-I-0260, WARP-A-0245, WARP-B-9011, WARP-I-9023, WARP-A-9005, WARP-A-9038), 상한 pill 생략 90(k=0 83 · k>0 7: 위 4 + PROD-I-0036, PROD-I-9019, PROD-I-9020 — 지문에 775 µm 가 없는 문항). 합계 90 문항. 지문이 상한·간극을 근거로 쓰는 문항은 해당 키를 넣으면 다시 표시된다.


`f_bond` (2026-11-21, BJ 형상 결정 반영): 기본값 gap 10 → **11 µm**, pitch 40 → **23 µm**(HCB 는 9 µm) — Micron HBM3E 12H 실측(STANDARDS 2.4). 비교표 "칩 간 간격" TC-NCF 칸 "≈ 7 µm" → "7–11 µm"(_facts F24 발표 7 µm 와 실측 11 µm 병기). 새 옵션 `hideTable`(공법 비교표 숨김)·`hideNotes`(SiCN·silica filler·EMC 주입·HCB 설명 등 공법 식별 주석 숨김; 결함 주석은 유지). 검사기 정보 코드 `I_FIG_BOND_LEAK`: 정답이 공법명·특징인데 두 옵션이 없으면 표시. 기본값 변경 영향 = gap_um·pitch_um 을 주지 않은 f_bond 문항 전부(그림 치수 라벨만 바뀜, k=1 문항은 지문 수치 검사 E 0 으로 확인). layout_check 3 화면 결함 0.

`f_bump`·렌더 점검 (2026-11-22, 사용자 지적 BUMP-B-0067): k 가 없으면 IMC 성장 좌표계 자체를 그리지 않음(빈 좌표계 금지). `axes()`·`curve()` 가 그림별 좌표계·곡선 수를 세고 smoke 가 `figEmpty`(좌표계 > 곡선) 를 보고 — 게이트 조건 figEmpty []. 육안 점검 도구 `tools/sheets.js`(접촉 인화지) 추가, SKILL 완료 게이트에 필수로 넣음.

정답 노출 차단 옵션 추가 (2026-11-22, DA 육안 점검 2 요청): `f_tsv hideLabels`(void·seam·pinch-off 이름 라벨 → "관찰 부위 (A)", 종횡비 주석 생략, 범례 중립화), `f_cmp hideLabels`(결함 이름 → "단차 A/B {nm} nm"), `f_stack hideFormula`(계산식 열 숨김; `hideResult` 도 식을 함께 숨김). 정답이 결함 이름·계산 결과면 켠다.

`f_saw` (2026-11-22, DA 육안 점검 2 지적): kerf 기본값을 방식별 표 대표값으로 통일(blade·lg·dbg 40, plasma 10, deep laser 30 µm; `kerf_um` 은 `??` 처리로 0 허용). stealth 는 kerf 치수선을 그리지 않음("kerf 손실 없음"과 모순 제거). 새 옵션 `hideTable`(방식 비교표 숨김). `notes:false` 이면 비교표의 붉은 행 강조도 끔(방식·결함 단서 차단).

새 템플릿 `f_ubj`·`f_plate`·`f_wet` (2026-11-22, BJ 승인): µbump 접합 단면(접합 불량·IMC·SOH·EM·daisy chain·HCB/ball 비교), through-mask 도금 공정 패널, 젖음 접촉각. params 는 STANDARDS 부록 A. 불량 이름을 그림에 쓰지 않는 것이 기본(이상 부위는 "관찰 부위 (A)"). BUMP-B 33문항의 f_note 를 이 템플릿으로 교체, 렌더 육안 확인·layout_check 3 화면 결함 0.

DA 육안 점검 3 지적 반영 (2026-11-22): `f_sip sideTitle`(오른쪽 단면 제목 지정)·`hidePath`(HBM–XPU 신호 경로 화살표·라벨 끔 — lid·stiffener·BGA·underfill 문항용). `f_therm` tTop 기본값 95 → (상한 − 25) °C(기본 최상단 온도가 상한보다 높게 그려지던 것). `f_ubj` 수지 충전을 배경과 구분되는 색 + 빗금으로, "수지 충전" 라벨을 간극 위쪽으로.
