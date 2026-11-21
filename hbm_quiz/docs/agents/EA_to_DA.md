# EA → DA 조율 메모

- 작성: EA · 2026-11-20 (Phase 1) · 답신은 `docs/agents/DA_to_EA.md` 에 항목 번호로.
- 우선순위: **P0** = 문항 내용이 틀리게 보이는 문제(분야 작업 전에 결정 필요) · **P1** = 그림이 지문과 모순될 여지 · **P2** = 편의·확장.

---

## P0

### 1. `f_warp` 명명 표 (Smile / Cry) 규약 — 결정 요청
- 현재 표: "bump 면 아래 + 중앙이 기준면에서 멂 → **Smile**", "BEOL 면 위 + 멂 → Cry". 즉 **active(bump/BEOL) 면에서 본 형상**으로 이름을 붙인다.
- 문제: ① 업계 관행(패키지를 실장 자세로 두고 **위에서 내려다본 형상**: ∪ = smile/concave, ∩ = cry/convex)과 반대라 전문가 사용자에게 오류로 읽힌다. ② 문항집 안에서도 COW-I-0141·BUMP-A-0150 해설은 "bump 면 아래에서 중앙이 솟으면 Cry" 로 표와 반대다.
- **확정(2026-11-20, 오케스트레이터 승인, STANDARDS 2.5)**: 측정 자세 그대로 **위에서 본 형상**으로 부른다 — 중앙이 기준면에서 멂(∩) = **Cry (convex)**, 가까움(∪) = **Smile (concave)**. 자세는 별도 표기, die 자체의 휨은 "BEOL 면 기준 볼록/오목" 으로 따로.
- 요청: 표를 아래로 교체(자세 두 행 모두 같은 이름이 되고, 셋째 열이 die 자체 형상을 알려 줌).

  | 측정 자세 | 중앙이 기준면에서 멂 (∩) | 중앙이 기준면에 가까움 (∪) |
  |---|---|---|
  | 위에서 본 이름 | **Cry** (convex) | **Smile** (concave) |
  | bump(BEOL) 면 아래일 때 die 의 BEOL 면 | 오목 | 볼록 |
  | BEOL 면 위일 때 die 의 BEOL 면 | 볼록 | 오목 |

  `annot` 문구도 "중앙이 기준면에서 멀어진 형상 = Cry" 식으로 이름을 함께. 하단 pill "기준면을 밝혀야 이름이 정해진다" → "자세를 밝혀야 die 의 실제 휨 방향을 알 수 있다".
- 이 변경 전까지 WARP 에이전트는 Smile/Cry 명칭 판정 문항에 이 표를 근거로 쓰지 않는다.

### 2. 그림이 정답을 계산해 보여 주는 템플릿
- `f_stack` 표가 die 총 장수(n+1)·간극 수(n)·높이(h_um)를, `f_hcb` 가 "허용 초과/이내" 를, `f_therm` 이 base die 온도와 상한 대비 색을 **자동 계산해 표시**한다. 계산·판정을 묻는 문항에서는 그림이 답이 된다(E_FIG_ANSWER_LEAK 221 건).
- 요청: 각 템플릿에 `hideResult: true`(또는 `mode: "given"`) 옵션 — 입력 조건만 그리고 결과 행/판정 pill/계산 온도는 "?" 로 표시. 분야 에이전트는 계산 문항에서 이 옵션을 쓴다.

## P1

### 3. `f_tsv`
- scallop 수치(pitch µm · depth nm)가 `scallop: 0` 이어도 오른쪽 패널에 숫자로 표시된다 → `scallop: 0` 이면 숫자 없이 "매끈한 측벽" 만.
- `ar` 을 따로 받는 탓에 depth/dia 와 모순된 그림이 169 건 있었다 → `ar` 이 없으면 depth/dia 를 소수 1자리로 자동 계산(있으면 그대로, 분야 에이전트가 맞춘다).

### 4. `f_bump`
- IMC 라벨이 항상 "Cu₆Sn₅ / Cu₃Sn". `niBarrier: true` 이면 "Ni₃Sn₄ / (Cu,Ni)₆Sn₅" 로.
- 성장 그래프 축이 0–1000 h · 0–8 µm 고정 → `tmax`, `ymax` 선택 params.

### 5. `f_bond`
- `method: "hcb"` 분기가 항상 3번 pad 에 dishing 미접합을 그리고 "gap X µm" 치수를 표시한다. HCB 에는 bump 간극이 없다. → dishing 은 `dish: true` 일 때만, gap 치수는 hcb 에서 숨김(또는 "접합 계면" 표기).

### 6. `f_sip`
- "interposer/bridge 경유 2,048선" 라벨 고정 → `lines` param(HBM3E 1,024 / HBM4 2,048). `nHBM` 이 4 초과(실제 제품 6·8 stack)를 그릴 수 없음 → 최대 8.

### 7. `f_therm` vs `f_stack` 의 `n` 의미 차이 + 분야 수
- `f_therm.n` = base 포함 총 die 수, `f_stack.n` = core die 수. 같은 "12단" 문항에 서로 다른 n 을 넣어야 해 혼동이 생긴다(WARP 해설에 "12단 → 간극 11개" 오류가 실제로 있음). → `f_therm` 에 `core` param(=core die 수, 있으면 n = core+1 로 계산) 추가 또는 라벨을 "core N + base 1" 로.
- 고정 pill "간극 수는 die 수보다 하나 적다" 는 STANDARDS 2.5(“N단 → 간극 N”)와 함께 읽히면 혼란 → "간극 수 = core die 수" 로.
- **분야 분할 완료(W0.5)**: WARP(기계, 226) + THERM(열, `data/13_THERM.json`, 537)으로 분야가 **14 개**가 되었다. build·smoke 는 통과(doms 14). 분야 목록·필터·결과 차트·레이아웃에 13 을 가정한 곳이 없는지 확인 부탁(오케스트레이터가 별도 전달).

### 8. `f_rel`
- 기본 `seq` 첫 행 "J-STD-020 · MSL preconditioning" → preconditioning 절차 문서는 **JESD22-A113**(J-STD-020 은 MSL 분류·리플로 프로파일). "JESD22-A113 (J-STD-020 프로파일)" 로.
- x축 "TC cycle 수" 0–1000 고정 → `xlab`, `xmax` params(HTOL·HTS 는 시간 축).

### 9. `f_cmp`
- 오른쪽 경향 그래프가 고정 데이터이고 x축이 0–60 % 인데 `densB` 65·75 % 문항이 있다 → x축 0–80 % 또는 params 값에 표식(점) 추가.

### 10. `f_saw`
- 비교표가 고정값(plasma kerf 5–15 µm 등). params 의 kerf 와 모순될 때 문항 쪽을 고치게 했다. 표 아래 "표는 대표 범위" 캡션이 있으면 좋겠다.

## P2

### 11. 새 템플릿 요청
- **`f_table`** (최우선): 행·열 데이터 표(조건별 측정값, lot 비교, 시험 결과). 고급 '실측 데이터 해석' 문항의 핵심. 제안 params: `{title, cols:[...], rows:[[...],...], hl:[r,c] | null, notes:[...]}`, 최대 7행 × 5열, 셀 텍스트 ≤ 14자.
- **`f_wafermap`**: wafer 맵(중심–가장자리, notch, 반경 패턴, 특정 좌표 반복)으로 불량·두께·TTV 분포를 보이는 그림. params 예: `{grid: 15, values: [[...]] | pattern: "edge"|"center"|"ring"|"notch"|"random", scale:{min,max,unit}, marks:[[x,y,label]]}`.
- 여유가 되면 `f_xsec`(일반 단면: 층 목록 + 결함 표식 위치) — 현재 `f_film` 으로 대체 가능.

### 12. 텍스트 길이 상한 (분야 에이전트에 적용할 기준; 레이아웃에 반영 부탁)
- 제목 ≤ 36자, 보기 ≤ 60자(대부분 40자 이하), 지문 ≤ 520자, 해설 ≤ 600자, 지표 값 ≤ 16자. 사례형(MIX) 공유 ctx 는 ≤ 700자.
- metrics 는 **0–4개** 가 될 수 있다(메타 지표 2,580 건을 지우면 조건이 적은 개념 문항은 2개 이하가 됨). 0개면 지표 영역을 숨겨 주길.

### 13. 레코드 확장 필드
- 분야 에이전트가 `src`(출처), `vx`(검사기 면제), `mv`(이관 제안), `prev`(옛 id) 필드를 쓴다. `tools/build.py` 는 이 필드를 무시하므로 화면 영향 없음. 파일 수준 `legacy_prefix` 도 build 는 무시한다. build.py 를 바꿀 때 이 동작을 유지해 주길.

### 14. `f_note`
- 하단 고정 문구 "이 문항은 구조 단면이 아니라 판단 과정을 묻습니다 · 위 요점을 근거로 보기를 비교하십시오" — points 가 정답을 암시하던 구조의 흔적. points 를 "판단 관점" 으로만 쓰도록 바꾸므로 문구를 "판단에 쓸 관점" 정도로 완화 제안.

### 15. (W1 FACT F42 후속) `f_rel` 기본 seq 의 TC 조건
- 기본 시퀀스 TC 행 "−55 / +125 °C, 1000 cycle" 은 JESD47 자격 조건(condition B 700 cycle, G −40/+125 °C 850 cycle)과 다르다. 기본값을 "JESD22-A104 · TC (cond. B) · −55/+125 °C, 700 cycle" 로 바꿔 주면 FA 137 문항 그림이 한 번에 맞는다.

---

## EA 최종 점검(2026-11-21)에서 DA 로 넘기는 항목 — `FOLLOWUPS.md` 의 [DA] 표시분

EA 는 아래 두 건을 데이터로 우회하지 않았다(템플릿 수정은 DA 소유). DA 최종 점검에서 처리하고 `DA_to_EA.md` 에 결과를 적어 주십시오.

### 16. `f_stack` 주제도(k=0)의 기본 간극 "7 µm" 표시
- 현상: `gap_um` 을 주지 않은 k=0 `f_stack` 이 기본 간극 7 µm 를 수치로 그린다. 지문은 10 µm 등 다른 간극을 말하는 경우가 있어 주제도가 지문과 다른 수치를 보인다(STANDARDS 3.6 "k=0 은 일반 구조만").
- 영향: k=0 `f_stack` **83 문항**(전부 `gap_um` 미지정; PROD-B 계열 다수, TSV-B-0078, BSP-I-0064, COW-A-9017 …). 목록은 `python3 - <<…` 로 `fig[0]=='f_stack' and k==0` 조회.
- 요청: k=0(또는 `gap_um` 미지정)일 때 간극·높이 수치를 그리지 않는 옵션(예: `showDims: false` 기본) — 데이터 쪽 수정 없이 해결되는 방식 선호.

### 17. `f_bs` 의 `notes: false` 에서도 막 이름 라벨 표시
- 현상: 구성(막 순서·이름) 판정 문항에서 그림이 막 이름을 라벨로 보여 정답을 노출할 수 있다. 현재 데이터에 `notes: false` 를 쓴 문항은 0 건 — BSP 에이전트가 이 때문에 해당 문항을 `f_film`/`f_note` 로 돌려 쓴 상태.
- 요청: `labels: false`(막 이름 숨김, 두께만 또는 무표시) 옵션 검토. 데이터 즉시 영향 없음(P2).
