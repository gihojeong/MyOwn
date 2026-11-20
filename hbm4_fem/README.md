# HBM4-8H 열·열-구조 FEM 파이프라인 (Blender + CalculiX)

**Blender(bpy 5.3)로 형상 생성 → 같은 형상에서 구조격자 hex mesh → CalculiX 2.21 정상상태 열해석 → 그 온도장을 받아 열-구조 해석(온도 스윕 + 운전) → matplotlib/Blender 3D 후처리**

```bash
./run_pipeline.sh          # 전체 (변형 4종, 단일 스레드 ccx: 변형당 ~40–60 min)
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
