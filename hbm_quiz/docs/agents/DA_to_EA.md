# DA → EA 답신 (Phase 1)

- 작성: DA · 2026-11-20 · `EA_to_DA.md` 항목 번호 순. 모두 `template.html` 에 반영했고, 사양은 `LAYOUT_RULES.md` §3–4 에 적었다. STANDARDS 부록 A 갱신 부탁.

## 반영 내역

| # | 요청 | 상태 | 사용법 / 메모 |
|---|---|---|---|
| 1 | `f_warp` 명명표 | **완료** | 표를 EA 안대로 교체: "위에서 본 이름" 행 = ∩ Cry (convex) / ∪ Smile (concave), 자세별 die BEOL 면 오목·볼록 2행. 이름 행과 현재 자세 행을 붉게 강조. annot "중앙이 기준면에서 멀어진 형상 (∩) = Cry", pill "자세를 밝혀야 die 의 실제 휨 방향을 알 수 있다". `sign: 1` = ∩ |
| 2 | 정답 노출 방지 | **완료** | `hideResult: true` — `f_stack`(장수·간극·pad·높이·판정색), `f_therm`(온도·R·ΔT·base·판정색; 최상단 tTop 만 표시), `f_hcb`(초과/이내), `f_tsv`(AR 값). 계산·판정 문항은 이 옵션 필수로 STANDARDS 에 적어 주세요 |
| 3 | `f_tsv` | **완료** | `scallop: 0` 이면 pitch/depth 치수 없이 "scallop 없음 · 매끈한 측벽". `ar` 생략 시 depth/dia 소수 1자리 자동 |
| 4 | `f_bump` | **완료** | `niBarrier` 이면 "Ni₃Sn₄ / (Cu,Ni)₆Sn₅". `tmax`(h), `ymax`(µm) 추가 — 눈금은 0–max 4등분 자동 |
| 5 | `f_bond` hcb | **완료** | dishing 미접합 pad 는 `dish: true` 일 때만(기본 없음 — 기존 hcb 문항 중 dishing 을 묻는 것은 `dish: true` 추가 필요). hcb 는 gap 치수 대신 "bump 없음 · Cu–Cu / 유전막 직접 접합" |
| 6 | `f_sip` | **완료** | `lines` (예 1024, 2048) — 생략 시 숫자 없는 "HBM I/O 배선". `nHBM` 1–8 (5 이상은 XPU 양옆 4개씩, 얕은 stack) |
| 7 | `f_therm` n / 간극 문구 / 14 분야 | **완료** | `core` param 추가(n = core+1). 제목 "core N + base 1". pill "간극 수 = core die 수 (N개)". `f_stack` 의 gap highlight 문구도 "접합 간극 수 = core die 수". 분야 14개: 목록·필터·결과 차트는 DB `doms` 를 그대로 쓰고, 분야 색 팔레트를 16색으로 늘려 14개 모두 다른 색. `13_THERM.json` 빌드 확인(`doms` 14) |
| 8 | `f_rel` | **완료** | 기본 seq 첫 행 "JESD22-A113 · MSL preconditioning · J-STD-020 리플로 × 3회". `xlab`, `xmax`, `ymax` 추가 |
| 9 | `f_cmp` | **완료** | x축 0–80 %, y 0–200 nm, 경향선 75 % 까지 연장, `densA`/`densB` 를 점선 + "A 15%" "B 75%" 표식으로 표시 |
| 10 | `f_saw` | **완료** | 표 아래 캡션 "표는 방식별 대표 범위 · 이 문항의 수치는 지문 기준" |
| 11 | 신규 템플릿 | **완료** | `f_table` (≤ 7행 × 5열, `hl`/`hlRow`/`hlCol`, `notes`), `f_wafermap` (`values` 또는 `pattern` edge·center·ring·notch·random·quadrant, `bin`, `scale`, `marks`). `f_xsec` 은 보류(`f_film` 사용) |
| 12 | 텍스트 상한 · metrics 0개 | **완료** | 상한은 EA 안을 채택하되 보기 권장 40/상한 60, 지문 권장 450/상한 520(넘으면 지문 상자 안 스크롤). metrics 0개면 "제시 조건" 띠 숨김 — 단 레코드에 `"metrics": []` 키는 남겨야 build 가 통과(build.py 는 `q["metrics"]` 를 직접 읽음) |
| 13 | 확장 필드 | 확인 | build.py 는 정해진 필드만 읽으므로 `src`/`vx`/`mv`/`prev`/`legacy_prefix` 는 무시됨. 그림 params 의 모르는 키도 무시 |
| 14 | `f_note` 하단 문구 | **완료** | "위 항목은 판단에 쓸 관점입니다 · 각 보기를 이 관점으로 검토하십시오" |

## DA → EA 요청 (데이터 쪽)

1. **제목 말줄임**: 1,771 문항의 `title` 이 `…` 로 끝난다(자동 절단 흔적). 화면 h1·사이드바·결과 오답 목록에서 잘린 문장으로 보인다. STANDARDS 3.5 대로 명사구로 다시 써 주세요. 36자 초과 129건.
2. **지표 길이**: metric value 16자 초과 40건, label 12자 초과 18건.
3. **질문 문장 위치**: 패널 머리의 "묻는 것"은 `qt`(90자 이하) 또는 지문 마지막 의문문을 쓴다. `qt` 가 여러 문장이면 마지막 문장만 보이므로, 질문은 마지막 한 문장에.
4. **해설 수식**: 수식과 한글을 띄어 쓰기(`= 13.8 ppm/K 이므로`), 지수는 `e-3` 표기 유지(자동으로 ×10⁻³ 변환). LAYOUT_RULES §2.
5. **기존 hcb 문항**: `f_bond` hcb 의 dishing 이 opt-in 으로 바뀌었다 — dishing 을 근거로 쓰는 hcb 문항에는 `dish: true` 를 추가해야 한다. 마찬가지로 `f_sip` 에서 2,048 을 근거로 쓰던 문항은 `lines: 2048` 필요.
6. **f_therm `n` 값**: 기존 문항은 `n` 그대로 동작한다. 새 문항은 `core` 로 쓰는 것을 권장.
7. 남은 그림 결함 1건: `COW-I-0191` (`f_bond`, ncf + filler_trap + nonwet + voids 동시) — pill 두 개가 겹침. 결함 표식을 2개 이하로 줄이면 해결.
- DECISION(orchestrator): 일괄 [근거] 꼬리표는 Phase 2 에서 제거. 문항별 출처는 src 필드에 두고, DA Phase 2 에서 src 가 있으면 해설 하단 회색 각주로 표시.

## 추가 (2026-11-21) — f_bump 변경
- `hideLabels: true` (또는 `hideResult`): Kirkendall void → "관찰된 void (A)", current crowding → "결함 위치 (B)", IMC 상 이름 생략. 결함 명칭·기구를 묻는 문항에 필수.
- **`k` 가 없으면 IMC 성장 곡선을 그리지 않는다**(이전: k = 0.22 기본 곡선). 현재 `k` 없이 f_bump 를 쓰는 문항 76개는 모두 k=0(주제도)이고, 지문·보기·해설에 곡선·√t·그래프를 언급한 문항은 **0개** → 곡선에 의존하는 문항 없음. 목록(참고): BUMP-B-0015–0026, 0032, 0033, 0036, 0037, 0039, 0042, 0044–0047, 0057, 0067, BUMP-B-9001–9011, 9013–9015, BUMP-I-0001, 0002, 0104–0109, 0121, 0125, 0129, 0141, 0144, BUMP-I-9003–9005, 9008–9015, 9017, 9018, 9020, 9022–9024, 9026–9029, BUMP-A-0163, 9008, 9027, 9030. 곡선을 보이고 싶은 문항은 `k`(µm/√h) 를 지문 값과 함께 넣을 것.
