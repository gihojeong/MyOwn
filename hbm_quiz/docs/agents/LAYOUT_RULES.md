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

자동 처리(분야 에이전트가 신경 쓰지 않아도 되는 것): 라벨 글자가 상자보다 크면 상자를 키우고, 라벨(pill)끼리 겹치면 가장 가까운 빈 자리로 옮기며 지시선 끝을 따라 옮긴다(`figPost`). 상자 안 글자는 상자 높이·폭에 맞춰 최대 5.5pt 까지 줄인다. **그래도 위 상한을 넘기면 줄바꿈이 늘어 다른 요소와 겹칠 수 있다.**

### 정답 노출 방지 — `hideResult: true`
그림이 계산·판정 결과를 표시하는 템플릿에서 계산·판정을 묻는 문항은 `hideResult: true` 를 넣는다. 입력 조건만 그리고 결과 칸은 `?` 로 둔다.

| 템플릿 | `hideResult` 가 숨기는 것 |
|---|---|
| `f_stack` | 표의 die 총 장수 · 간극 수 · backside pad die 수 · 스택 높이, 간극 개수 라벨, 높이 상한 pill 의 초과/이내 색 |
| `f_therm` | core·base die 온도(최상단 `tTop` 만 표시), 층별 R · 합계, ΔT, base 온도, 상한 대비 색, "간극 수 = core die 수 (N개)" pill |
| `f_hcb` | 허용치 대비 "초과/이내" 판정과 색 |
| `f_tsv` | aspect ratio 값 |
| `f_bump` | Kirkendall · current crowding 결함 이름, IMC 상(Cu₆Sn₅ 등) 이름 (`hideLabels` 와 같음) |

## 4. 템플릿별 params 허용 범위

범위 밖 값은 그림이 잘리거나 모양이 무너진다. (현재 데이터의 실제 범위를 함께 적음)

| 템플릿 | params · 허용 범위 |
|---|---|
| `f_tsv` | `dia_um` 2–12, `depth_um` 20–150, `ar` (생략 시 depth/dia 소수 1자리 자동), `fill`: good·void·seam·pinch, `scallop`: 0·1 (**0 이면 scallop 치수 미표시**, "scallop 없음"), `scallopPitch` 0.2–0.6 µm, `scallopDepth` 20–120 nm, `barrier`, `overburden`, `taper` 0.6–1.0, `hideResult` |
| `f_cmp` | `densA` 5–40, `densB` 30–80 (x축 0–80 %, 두 값이 A/B 표식으로 그려짐), `dish_nm` 5–150, `erosion_nm` 10–80, `nA` 3–5, `nB` 6–10 |
| `f_bs` | `step` 0–7, `defect`: none·undercut·residue (step 7 에서만), `ox1` 100–500, `sin` 100–300, `ox2` 300–800 nm, `ni_um` 1–5 |
| `f_bump` | `pillar_um` 10–60, `solder_um` 5–25, `imc_um` 0.5–6, `niBarrier` (IMC 라벨이 Ni₃Sn₄ / (Cu,Ni)₆Sn₅ 로 바뀜), `kirkendall`, `em` + `j_kA` (≤ 4자리), `temp`, `k`, `hours` ≤ `tmax`, **`tmax`** (기본 1000 h), **`ymax`** (기본 8 µm), **`hideLabels`** (Kirkendall·EM 결함 라벨을 "관찰된 void (A)"·"결함 위치 (B)" 로, IMC 상 이름 생략 — 명칭·기구를 묻는 문항용, `hideResult` 도 같은 효과), `bullet`. **`k` 가 없으면 성장 곡선을 그리지 않는다**(축·식 라벨만) |
| `f_saw` | `method`: blade·lg·stealth·plasma·deeplaser·dbg (비교표에 **DBG 행**이 따로 있고 dbg 면 그 행이 강조됨), `kerf_um` 0–60, `haz_um` 2–20, `chip_um` 5–30, **`notes: false`** (개념 주석·기본 bullet 을 끄고 지시선 라벨을 "관찰 부위 (A/B)" 로 — 개념을 묻는 문항용), `bullet` (표는 "대표 범위" 캡션 표시) |
| `f_bond` | `method`: ncf·mrmuf·hcb, `pitch_um` 5–60, `gap_um` 3–15 (**hcb 에는 주지 말 것 — 표시 안 함**), `voids` 0–3, `filler_trap`, `nonwet`, **`dish: true`** (hcb 에서 dishing 미접합 pad 를 그릴 때만), `bullet` |
| `f_warp` | `ref`: bump-down·beol-up, `sign` ±1 (1 = 중앙이 기준면에서 멂 ∩ = **Cry**, −1 = 가까움 ∪ = **Smile**), `mag_um` 10–200, `tg` 50–240, `temp` 25–260 |
| `f_sip` | `type`: cowos-s·cowos-r·cowos-l·emib·emib-t, `nHBM` **1–8**, **`lines`** (예 1024, 2048 — 생략 시 "HBM I/O 배선"), **`msg`** (오른쪽 요점 pill 교체, ≤ 44자), `bullet` |
| `f_therm` | **`core`** (core die 수, 권장 — n = core+1 로 계산) 또는 `n` (base 포함 총 die 수) 4–21, `q_Wmm2` 0.01–1, `tTop`, `limit`, `layers` ≤ 5행 (이름 ≤ 10자), `hideResult`. core 12 초과 시 die 라벨이 작아진다 |
| `f_fa` | `tech`: lit·obirch·eotpr·xrm · `hot` [0–1, 0–1], `fov_um`, `depth` 5–50, `feats` ≤ 4 (라벨 ≤ 10자), `dz` 5–30, `zpeak` 0–45 |
| `f_rel` | `seq` ≤ 4행 [문서 ≤ 12자, 시험명 ≤ 20자, 조건 ≤ 16자], `cur`, `fails` ≤ 5점 (x ≤ `xmax`, y ≤ `ymax`), **`xlab`** (기본 "TC cycle 수"), **`xmax`** (기본 1000), **`ymax`** (기본 10 %), **`tcCycles`** (기본 700 — 기본 seq 의 JESD22-A104 cond. B 행과, TC 축일 때 "규격 N cycle" 점선에 쓰임), `crit`, `hint`, `bullet` |
| `f_stack` | `n` (core die 수) 4–24, `highlight`: height·midcore·base·gap·topcore, `gap_um`, `h_um`, `limit_um`, `bullet`, `hideResult` |
| `f_hcb` | `pitch_um` 1–10, `tol_nm` 20–300, `off_nm` 0–420 (그림 변위 상한 0.5 in), `dish_nm` 1–16, `bullet`, `hideResult` |
| `f_plot` | `title`, `x`/`y` {min, max, ticks ≤ 6개 (라벨 ≤ 5자), lab ≤ 24자}, `series` ≤ 4 {name ≤ 22자, color "RRGGBB", pts ≤ 12, dash}, `marks` ≤ 3 [x, 라벨 ≤ 12자], `bullets` ≤ 3 |
| `f_film` | `layers` ≤ 9 [이름 ≤ 18자, 상대두께, 색], `roles` ≤ 5행 [층, 두께, 역할 ≤ 14자], `bullets` ≤ 3, `flags` ≤ 2 |
| `f_note` | `title` ≤ 22자, `points` ≤ 4 (각 ≤ 50자, **판단 관점** — 정답 문장 금지), `ask` ≤ 12자 |
| **`f_table`** (신규) | `title` ≤ 22자, `unit`, `cols` ≤ 5 (머리글 ≤ 8자), `rows` ≤ 7행 × ≤ 5열 (셀 ≤ 14자, 숫자는 문자열 가능), 강조 `hl: [행, 열]` (행은 rows 기준 0부터) 또는 `hlRow` / `hlCol`, `notes` ≤ 3 (각 ≤ 44자) |
| **`f_wafermap`** (신규) | `title` ≤ 22자, `grid` 9–25 (기본 15), `values` grid×grid 숫자 (`null` = die 없음) **또는** `pattern`: edge·center·ring·notch·random·quadrant, `scale` {min, max, unit}, `bin: true` (합격/불량 2색, values 는 0/1), `marks` ≤ 4 [열, 행, 라벨 ≤ 12자], `bullets` ≤ 3, `seed` (random 배치 변경) |

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
