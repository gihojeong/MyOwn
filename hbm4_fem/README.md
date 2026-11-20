# HBM4-8H 열·열-구조 FEM 파이프라인 (Blender + CalculiX)

**Blender(bpy 5.3)로 형상 생성 → 같은 형상에서 구조격자 hex mesh → CalculiX 2.21 정상상태 열해석 → 그 온도장을 받아 열-구조 해석(온도 스윕 + 운전) → matplotlib/Blender 3D 후처리**

```bash
./run_pipeline.sh          # 전체 (변형 4종 + diff_pair.py, 단일 스레드 ccx: 변형당 ~40–60 min)
```

| 파일 | 역할 |
|---|---|
| `params.py` | 형상·재료·하중 (단일 소스). **총 높이 720 μm 고정, 두께 변화는 top die가 흡수** |
| `blender_build.py` | Blender 모델(.blend), 렌더(실척/z×6 절개/분해도), FEM용 layer bbox export(`geometry_*.json`) |
| `mesh_inp.py` | JSON → 구조격자 hex mesh, 재료 할당, 발열 분포, ccx 입력(DC3D8 / C3D8I) |
| `run_all.py` | mesh → 열해석 → 온도장 매핑(`*TEMPERATURE`) → 열-구조 |
| `post.py`, `compare.py` | 열/warpage/층별 응력, 변형 비교 |
| `blender_results.py` | 결과를 Blender(Cycles)로 3D 렌더 (1/4 절개, uz 확대, 컬러맵) |

## 모델
- 외형 11.0 × 12.8 mm, H = 720 μm. Base die 60 μm / bond 15 μm ×8 / core die 50 μm ×7 / top die 190 μm (Si 노출).
- Core die는 0.25 mm inset, 측벽은 EMC. 중앙 TSV/μbump band(9.0 × 1.0 mm), base die PHY(GPU 측 1.5 mm 폭).
- Bond층 균질화: μbump(Cu pillar+SnAg) 체적분율 band 20 %, 그 외 dummy 5 %. E는 Hill 평균, α는 Turner 식, k_z는 병렬, k_xy는 Maxwell-Garnett.
- 폴리머(EMC, NCF)는 Tg 전이를 tanh로 모델링: EMC 20→0.8 GPa, 9→35 ppm, Tg 165 °C / NCF 5→0.3 GPa, 40→110 ppm, Tg 140 °C.
  CalculiX `*EXPANSION, ZERO=175`에 맞게 순간 CTE를 secant CTE로 적분 변환.
- 변형: **A** MR-MUF / **B** TC-NCF / **C** MR-MUF + EMC cap 90 μm(top 100 μm) / **D** A에서 mid-die 47 μm(top 211 μm).
- Mesh: 45 × 55 × 31 절점, 71,280 요소. 구조해석은 C3D8I(비적합 모드)를 써서 얇은 층의 굽힘을 확보.

## 하중/경계
- 발열 32 W: base die 12 W(PHY 6, TSV 3, 기타 3) + core die 2.5 W × 8.
- 대류 경계: 상면 h = 7000 W/m²K, T∞ = 40 °C / 하면(μbump→interposer) h = 4000 W/m²K, T∞ = 65 °C.
- 응력 0 온도 175 °C(EMC 경화). 균일온도 25…260 °C 8스텝 + 운전 온도장 1스텝. 3-2-1 구속.

## 주의
- **CalculiX SPOOLES 멀티스레드(OMP>1)가 일부 스텝에서 오염된 해를 냄**(C 260 °C: uz 116 μm, 단일 스레드 4.6 μm). `run_all.py`는 `OMP_NUM_THREADS=1`로 고정.
- warpage 지표: `coplanarity`(평면 보정 후 max−min, 국부 모서리 포함), `bow`(2차 곡면 피팅의 모서리−중심, 전역 휨, + smile).
- 한계: 선형 탄성(점탄성, 경화 수축, 공정 이력 없음), 범프/TSV 균질화, die 모서리 응력은 특이점이라 메시 의존. 절대값보다 변형 간 상대 비교에 적합.

## 결과 (단일 스레드 확정)
| Variant | Tmax op [°C] | Bow 25°C [μm] | Bow 260°C [μm] | Bow op [μm] | Si σvm max 25°C [MPa] | Si σ1 max 25°C | Bond peel max 25°C | Bond τ max 25°C | EMC σ1 max 25°C |
|---|---|---|---|---|---|---|---|---|---|
| A_MRMUF | 85.0 | -2.43 | +0.03 | -1.27 | 34.2 | 17.3 | 9.5 | 9.7 | 30.4 |
| B_TCNCF | 85.1 | -2.72 | +0.06 | -1.29 | 42.9 | 22.1 | 34.9 | 5.0 | 30.1 |
| C_MRMUF_CAP | 97.0 | +9.31 | -1.33 | +7.78 | 42.4 | 12.5 | 9.4 | 11.0 | 32.7 |
| D_MID47 | 85.1 | -2.90 | +0.11 | -1.61 | 34.3 | 17.3 | 9.6 | 9.5 | 30.5 |

- **열:** 1D 집중 모델로 검산. A = 140.8 mm², R_top = 1/(7000·1.408e-4) = 1.015 K/W, R_bot = 1.776 K/W.
  32 = (T−40)/1.015 + (T−65)/1.776 → T = 69.8 °C. FEM Tavg ≈ 71–72 °C, PHY hot spot 85 °C.
  C는 EMC cap(90 μm, k = 1)의 R = 90e-6/(1·1.408e-4) = 0.64 K/W에 약 20 W가 흘러 +12.8 K → 97 °C로 FEM과 일치.
- **Bond층 응력:** 등이축 구속 σ = E/(1−ν)·Δα_sec·ΔT = 22.2 GPa/0.698 × (11.92−2.90) ppm × (−150 K) = −43 MPa (dummy).
  TSV band에서는 −70 MPa. FEM von Mises 최대 66 MPa로 일치.
- **Warpage:** CLT(적층판) 25 °C 결과 A 2.70 μm, FEM bow 2.43 μm (crying).
  C는 EMC cap이 위에서 더 수축해 부호가 반전(smile +9.3 μm). Tg 이상에서 EMC가 연화해 bow ≈ 0.
- **D (mid-die 50→47 μm, top 190→211 μm):** bow @25 °C −2.43 → −2.90 μm (**+19 %**, CLT 예측 +16 %), 운전 시 +26 %, Δw max 0.30 μm.
  층별 응력·온도 변화는 1 % 미만. 박화로 고CTE bond층이 아래로 몰리고 top die가 두꺼워져 중립축이 위로 이동하면서 굽힘 모멘트 팔이 커진 효과.

그림: `figs/` (thermal_*, warpage3d_*, stress_*, compare_variants, diff_A_MRMUF_vs_D_MID47, blender_* 3D 렌더), 형상 렌더: `out/render_*`.
