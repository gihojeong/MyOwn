# HBM FEM — 새 세션 인계 지시문 (UI 연계 해석 1단계 MVP)

> 새 Claude Code 세션의 첫 메시지로 이 문서 전체(또는 "hbm4_fem/HANDOFF.md 를 읽고 1단계를 진행해")를 붙여 넣으세요.

## 0. 작업 목표
칩 정보를 입력하는 **웹 UI** + **[열해석] [구조해석] 버튼** → 로컬 백엔드가 CalculiX FEM 을 연계 실행 → 결과(표·그림·판정)를 화면에 표시.
이번 세션 범위 = **1단계 MVP** (아래 §5). 2·3단계는 하지 않는다.

## 1. 저장소
- GitHub `gihojeong/MyOwn`, 브랜치 **`claude/wizardly-bohr-5mo784`**, 폴더 **`hbm4_fem/`** (main 브랜치에는 없음)
- 새 작업은 이 브랜치에서 새 브랜치를 따서 진행하고 커밋·푸시.

## 2. 환경
- CalculiX `ccx` 2.21 (Linux: `apt install calculix-ccx`), Python 3.13 + numpy, scipy, matplotlib, (렌더 시) `bpy` 5.3, NanumGothic 폰트.
- **ccx 는 반드시 단일 스레드 (`OMP_NUM_THREADS=1`)** — 멀티스레드 SPOOLES 가 해를 오염시킨 사례가 있음. 속도는 케이스 병렬로 확보.
- `out*/` 원시 결과(frd, dat, fields.npz)는 git 에 없음 → 필요 시 재계산.

## 3. 반드시 지킬 규칙 (사용자 확정 사항)
1. 대상 공법은 **TCB (TC-NCF)** 만.
2. **총두께는 세대별 고정**(HBM3E 720 μm, HBM4 775 μm), 두께 변경분은 **top core Si 가 흡수**.
3. warp 부호 규약(viewer): **warp = 중앙 − vertex, (+) Cry / (−) Smile**.
4. 다중 무응력온도: Si/BEOL = T0b(**보정값 245 °C**, out2/calib4.json), NCF+SnAg gap 217 °C, EMC 175 °C.
   CalculiX 에서는 `*EXPANSION, ZERO=0` + α_tab(T)=ε_F(T)/T + **가상 초기온도 400 °C** 기법으로 구현(400 °C 는 사용/공정 온도가 아님 — UI·보고서에 혼동 없게 표기).
5. 사용량 절약: 서브에이전트 남발 금지, 순차 진행, 장시간 FEM 은 백그라운드 + 완료 알림 대기(폴링 최소화).
6. 결정론적 FEM 이므로 DOE 유의성은 Lenth 대신 실용 임계(warp 0.1 μm, 응력 0.5 MPa)·기여도.

## 4. 코드 지도 (`hbm4_fem/`)
| 파일 | 역할 |
|---|---|
| `stack.py` | 두께 세트(DESIGN/MICRON), 재료, ε_F(T), 층 생성 `layers(c)`, 직사각 die `Lxy/half_y`, CLT 검산 `clt_warp` |
| `grid3.py` | **제품 정의(PRODUCTS)**: case, die 크기, PHY 박스·전력, BC; 1/2 대칭 격자 `grid()`, 번호 `nodes_elems()` — HA·SA 공통 인터페이스 |
| `ha_thermal.py` | [HA] 열해석: 고객 사용환경(냉각수 45 °C W45, 상면 h 22,000, GPU 가열 interposer 55–80 °C, 스택 전력 HBM3E 30 W / HBM4 36 W), idle→full-load 과도+정상 → `out3/thermal/<prod>/fields.npz`, summary.json |
| `sa_struct.py` | [SA] 열-구조(순차 연성): 25/230 °C·idle·각 시점·정상 → warp(PHY측/반대측/coplanarity), 응력 → `out3/mech/<prod>/summary.json`, figs |
| `ha_lit.py`, `ha_lit_plot.py` | [HA] 3D Lock-in thermography (주파수영역 (K+iωC)θ=Q, 1/4 대칭) |
| `fem2.py`, `doe*.py` | 1/4 대칭 구조 FEM, DOE(2⁴) 실행·분석 |
| `frd.py` | CalculiX frd/dat 판독 |
| `blender_*.py`, `v3_thermal_fig.py` | Blender 3D 시각화 |
| `thermal2.py` | 열물성 `therm()`, `kSi()` (다른 모듈이 import) |

## 5. 1단계 MVP 범위 (이번 세션)
1. **입력 규격(spec JSON)** 정의 — 키 이름은 사용자 viewer(SHBM_viewer ①입력 탭)와 동일하게:
   `gen, nh, tot, lsi, lm, ms, mm, tm, tsi(빈값=자동), nc(J/G), cbD, cbP, bump_N(선택), tg, a1, a2, mE, mA, eE, eA, eA2, eTg`
   + die 크기(`L_logic, L_logic_y, L_dram, L_dram_y`), PHY(`edge_off, depth, length, phy_W`), 전력(base 로직, core), 환경(냉각수 T, h_top, interposer T 분포), 모드(quick/full).
2. `grid3.py` 의 하드코딩 PRODUCTS 를 **spec → case/grid** 로 일반화 (기존 두 프리셋은 spec 파일로 이전: `presets/hbm3e_12h.json`, `presets/hbm4_8h.json`). 입력 검증: 총두께, top Si>0, vf<0.785.
3. `ha_thermal.py`, `sa_struct.py` 를 spec 입력으로 동작하게 리팩터. **quick 모드** = 정상 열해석 + 구조 4스텝(25 °C, 230 °C, idle, full-load).
4. 백엔드: Flask(단일 파일) — `POST /run/thermal`, `POST /run/struct`(열 결과 없으면 열 먼저), `GET /status/<job>`(ccx .sta 파싱 진행률), `GET /result/<job>`. 작업은 subprocess 로 순차 큐.
5. UI: 단일 HTML(입력 폼 + 프리셋 불러오기 + 총두께/top Si 자동 계산 표시 + 버튼 + 진행률 + 결과 표·그림). 
6. **회귀 시험 (필수)**: HBM3E-12H 프리셋으로 UI 경로 실행 → 기존 값 재현
   - 열(정상, full load): Tmax **76.56 °C** (±0.1), hot spot PHY 박스 중앙
   - 구조: 25 °C warp **7.60 μm**, 230 °C **0.41 μm**, idle **6.64**, full-load PHY측 **4.98** / 반대측 **5.20 μm** (±0.02)
   - HBM4-8H: Tmax 75.80 °C, 25 °C warp 18.7 μm, full-load 13.9/14.2 μm
7. README 에 실행법(`python3 app.py` → 브라우저 http://localhost:8000).

## 6. 산정 (PA 판단 근거)
- 1회 실행: quick ≈ 열 1–3분 + 구조 10–15분 ≈ **15분**; full(과도) ≈ **1시간**; LIT ≈ 1.5분.
- 개발: 코드 800–1,200줄, 40–60 tool call, 출력 8–12만 토큰, 입력 200–400만(캐시 위주) — ±50%. 경과 2–4시간(검증 FEM 1–1.5시간 포함).

## 7. 이후 단계 (이번 세션에서 하지 말 것)
- 2단계: full 모드(과도), LIT, 3D 렌더, 작업 큐 고도화.
- 3단계: viewer HTML 에 버튼 통합.

## 8. 미해결·주의
- HBM4 die 크기(base 10.9×12.7, core 10.1×11.9), PHY 33 mm²/9 W 는 **추정값** — 실측 칩 정보(수직구조, bump D/P, J/G, die 크기, 실측 warp)를 받으면 프리셋 갱신 + HBM4 T0b 별도 보정.
- 230 °C warp 보정 오차: 예측 0.41 vs 실측 2.1 μm.
- 응력은 die 모서리 요소평균(격자 의존) → 경향용. 정량은 서브모델 필요.
- 완전 연성 검증은 보류(열탄성 결합계수 δ_Si = 3.9×10⁻⁴ 로 순차 연성 타당).
- S사 수치(viewer 기반)가 코드에 포함 — 사내 반출 규정 확인, 필요 시 프리셋을 git 밖 로컬 파일로 분리.
