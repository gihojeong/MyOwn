# 레이아웃 검사 기준선 (baseline) — 2026-11-20T20:50

검사기: `tools/layout_check.js` · 문항 5000 · 75s · JS 오류 0

## 상황도 (figure) 결함

| 코드 | 의미 | 건수 |
|---|---|---:|
| E1 | 글자가 자기 상자/pill 밖으로 넘침 | 31127 |
| E2 | 라벨 글자끼리 겹침 | 5167 |
| E3 | viewBox 밖으로 잘림 | 0 |
| E4 | pill 배경끼리 겹침 | 1888 |
| E5 | 선이 맨 글자(배경 없는 라벨)를 관통 | 2005 |
| E6 | 표가 상자보다 큼 | 0 |
| E7 | (참고) pill 이 선 위에 얹혀 선을 가림 — 치수·표식 pill 은 의도된 배치 | 7287 |

**고위험(E1–E4, E6) 결함 문항: 5000 / 5000** · 결함 하나라도 있는 문항(E5 포함): 5000

### 그림 종류별

| fig | 문항(결함) | 고위험 문항 | E1 | E2 | E3 | E4 | E5 | E6 | E7 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| f_bond | 377 | 377 | 377 | 0 | 0 | 0 | 79 | 0 | 387 |
| f_bs | 255 | 255 | 510 | 0 | 0 | 0 | 0 | 0 | 0 |
| f_bump | 395 | 395 | 4345 | 1185 | 0 | 394 | 1372 | 0 | 791 |
| f_cmp | 83 | 83 | 1079 | 249 | 0 | 0 | 83 | 0 | 0 |
| f_fa | 233 | 233 | 2739 | 437 | 0 | 325 | 14 | 0 | 843 |
| f_film | 148 | 148 | 148 | 0 | 0 | 0 | 0 | 0 | 0 |
| f_hcb | 308 | 308 | 924 | 308 | 0 | 283 | 0 | 0 | 308 |
| f_note | 538 | 538 | 1076 | 0 | 0 | 0 | 0 | 0 | 0 |
| f_plot | 475 | 475 | 5701 | 794 | 0 | 0 | 0 | 0 | 975 |
| f_rel | 140 | 140 | 1680 | 140 | 0 | 140 | 74 | 0 | 851 |
| f_saw | 181 | 181 | 223 | 0 | 0 | 0 | 168 | 0 | 106 |
| f_sip | 292 | 292 | 843 | 259 | 0 | 1 | 200 | 0 | 0 |
| f_stack | 538 | 538 | 538 | 0 | 0 | 0 | 0 | 0 | 0 |
| f_therm | 531 | 531 | 8058 | 1491 | 0 | 0 | 0 | 0 | 0 |
| f_tsv | 354 | 354 | 1062 | 0 | 0 | 745 | 0 | 0 | 1770 |
| f_warp | 152 | 152 | 1824 | 304 | 0 | 0 | 15 | 0 | 1256 |

## 문항 화면 (screen) 결함 — 채점 후(해설 표시) 상태

| 뷰포트 | 결함 문항 | 코드별 |
|---|---:|---|
| 1440x900 | 0 | {} |
| 820x1180 | 0 | {} |
| 390x844 | 5000 | {"S1":5000} |

S1 가로 스크롤 · S2 패널 겹침 · S3 그림 영역 찌그러짐/본문 잘림 · S4 지표·보기 글자 잘림 · S5 제목 잘림

## 고위험 결함 예시 (그림 종류별 최대 5문항)

**f_bond**
- COW-B-0001 (#1331): E1 "두께 방향 확대 표시 · 평면 치수 비례 아님" overflow 7px
- COW-B-0002 (#1332): E1 "두께 방향 확대 표시 · 평면 치수 비례 아님" overflow 7px
- COW-I-0001 (#1333): E1 "두께 방향 확대 표시 · 평면 치수 비례 아님" overflow 7px
- COW-I-0002 (#1334): E1 "두께 방향 확대 표시 · 평면 치수 비례 아님" overflow 7px
- COW-B-0003 (#1337): E1 "두께 방향 확대 표시 · 평면 치수 비례 아님" overflow 7px

**f_bs**
- BSP-B-0001 (#492): E1 "공정 순서" overflow 7px · E1 "두께 방향 확대 표시 · 평면 치수 비례 아님" overflow 7px
- BSP-B-0002 (#493): E1 "공정 순서" overflow 7px · E1 "두께 방향 확대 표시 · 평면 치수 비례 아님" overflow 7px
- BSP-I-0001 (#494): E1 "공정 순서" overflow 7px · E1 "두께 방향 확대 표시 · 평면 치수 비례 아님" overflow 7px
- BSP-I-0002 (#495): E1 "공정 순서" overflow 7px · E1 "두께 방향 확대 표시 · 평면 치수 비례 아님" overflow 7px
- BSP-A-0001 (#496): E1 "공정 순서" overflow 7px · E1 "두께 방향 확대 표시 · 평면 치수 비례 아님" overflow 7px

**f_bump**
- TSV-A-0048 (#156): E1 "0" overflow 7px · E1 "2" overflow 7px · E1 "4" overflow 7px
- BUMP-B-0001 (#746): E1 "0" overflow 7px · E1 "2" overflow 7px · E1 "4" overflow 7px
- BUMP-B-0002 (#747): E1 "0" overflow 7px · E1 "2" overflow 7px · E1 "4" overflow 7px
- BUMP-I-0001 (#748): E1 "0" overflow 7px · E1 "2" overflow 7px · E1 "4" overflow 7px
- BUMP-I-0002 (#749): E1 "0" overflow 7px · E1 "2" overflow 7px · E1 "4" overflow 7px

**f_cmp**
- TSV-I-0002 (#3): E1 "상면: pattern density 가 다른 두 영" overflow 7px · E1 "CMP 후 단면 표면 높이" overflow 7px · E1 "0" overflow 7px
- TSV-I-0031 (#96): E1 "상면: pattern density 가 다른 두 영" overflow 7px · E1 "CMP 후 단면 표면 높이" overflow 7px · E1 "0" overflow 7px
- TSV-I-0032 (#97): E1 "상면: pattern density 가 다른 두 영" overflow 7px · E1 "CMP 후 단면 표면 높이" overflow 7px · E1 "0" overflow 7px
- TSV-I-0033 (#98): E1 "상면: pattern density 가 다른 두 영" overflow 7px · E1 "CMP 후 단면 표면 높이" overflow 7px · E1 "0" overflow 7px
- TSV-I-0034 (#99): E1 "상면: pattern density 가 다른 두 영" overflow 7px · E1 "CMP 후 단면 표면 높이" overflow 7px · E1 "0" overflow 7px

**f_fa**
- FA-B-0001 (#3186): E1 "Lock-in Thermography (LIT) a" overflow 7px · E1 "0" overflow 7px · E1 "25" overflow 7px
- FA-I-0001 (#3188): E1 "OBIRCH 저항 변화 map" overflow 7px · E1 "0" overflow 7px · E1 "25" overflow 7px
- FA-I-0002 (#3189): E1 "EOTPR 반사 파형 → 전기 길이로 결함 위치 추" overflow 7px · E1 "-40" overflow 7px · E1 "-20" overflow 7px
- FA-A-0001 (#3190): E1 "X-ray tomography (XRM) 단층 sl" overflow 7px · E1 "0" overflow 7px · E1 "25" overflow 7px
- FA-B-0003 (#3192): E1 "Lock-in Thermography (LIT) a" overflow 7px · E1 "0" overflow 7px · E1 "25" overflow 7px

**f_film**
- SIP-A-0076 (#2761): E1 "두께 방향 확대 표시 · 비례 아님" overflow 7px
- FEOL-B-0001 (#4817): E1 "두께 방향 확대 표시 · 비례 아님" overflow 7px
- FEOL-B-0003 (#4819): E1 "두께 방향 확대 표시 · 비례 아님" overflow 7px
- FEOL-B-0004 (#4820): E1 "두께 방향 확대 표시 · 비례 아님" overflow 7px
- FEOL-B-0005 (#4821): E1 "두께 방향 확대 표시 · 비례 아님" overflow 7px

**f_hcb**
- COW-A-0001 (#1335): E1 "상면 overlay — 실선: 상부 die pad," overflow 30px · E1 "단면: CMP dishing이 접합을 막는다" overflow 7px · E1 "변위 · 단차는 과장 표시" overflow 7px
- COW-A-0002 (#1336): E1 "상면 overlay — 실선: 상부 die pad," overflow 30px · E1 "단면: CMP dishing이 접합을 막는다" overflow 7px · E1 "변위 · 단차는 과장 표시" overflow 7px
- COW-A-0003 (#1379): E1 "상면 overlay — 실선: 상부 die pad," overflow 30px · E1 "단면: CMP dishing이 접합을 막는다" overflow 7px · E1 "변위 · 단차는 과장 표시" overflow 7px
- COW-A-0004 (#1380): E1 "상면 overlay — 실선: 상부 die pad," overflow 30px · E1 "단면: CMP dishing이 접합을 막는다" overflow 7px · E1 "변위 · 단차는 과장 표시" overflow 7px
- COW-A-0005 (#1381): E1 "상면 overlay — 실선: 상부 die pad," overflow 30px · E1 "단면: CMP dishing이 접합을 막는다" overflow 7px · E1 "변위 · 단차는 과장 표시" overflow 7px

**f_note**
- COW-A-0078 (#1458): E1 "핵심 개념 — 공법 전환과 검사 설계" overflow 7px · E1 "이 문항은 구조 단면이 아니라 판단 과정을 묻습니다" overflow 5px
- WARP-A-0056 (#2018): E1 "핵심 개념 — 서로 다른 지표의 비교" overflow 7px · E1 "이 문항은 구조 단면이 아니라 판단 과정을 묻습니다" overflow 5px
- SIP-A-0077 (#2762): E1 "핵심 개념 — 공법과 공급망의 결합" overflow 7px · E1 "이 문항은 구조 단면이 아니라 판단 과정을 묻습니다" overflow 5px
- FA-B-0065 (#3297): E1 "핵심 개념 — 물리 분석" overflow 7px · E1 "이 문항은 구조 단면이 아니라 판단 과정을 묻습니다" overflow 5px
- FA-I-0099 (#3427): E1 "핵심 개념 — 물리 분석" overflow 7px · E1 "이 문항은 구조 단면이 아니라 판단 과정을 묻습니다" overflow 5px

**f_plot**
- TSV-A-0002 (#5): E1 "0" overflow 7px · E1 "25" overflow 7px · E1 "50" overflow 7px
- BUMP-A-0002 (#751): E1 "0" overflow 7px · E1 "25" overflow 7px · E1 "50" overflow 7px
- BUMP-A-0033 (#830): E1 "0" overflow 7px · E1 "25" overflow 7px · E1 "50" overflow 7px
- BUMP-A-0034 (#831): E1 "0" overflow 7px · E1 "25" overflow 7px · E1 "50" overflow 7px
- BUMP-A-0035 (#832): E1 "0" overflow 7px · E1 "25" overflow 7px · E1 "50" overflow 7px

**f_rel**
- FA-B-0002 (#3187): E1 "시험 순서 (preconditioning이 먼저)" overflow 7px · E1 "0" overflow 7px · E1 "2.5" overflow 7px
- FA-A-0002 (#3191): E1 "시험 순서 (preconditioning이 먼저)" overflow 7px · E1 "0" overflow 7px · E1 "2.5" overflow 7px
- FA-B-0023 (#3232): E1 "시험 순서 (preconditioning이 먼저)" overflow 7px · E1 "0" overflow 7px · E1 "2.5" overflow 7px
- FA-B-0024 (#3233): E1 "시험 순서 (preconditioning이 먼저)" overflow 7px · E1 "0" overflow 7px · E1 "2.5" overflow 7px
- FA-B-0025 (#3234): E1 "시험 순서 (preconditioning이 먼저)" overflow 7px · E1 "0" overflow 7px · E1 "2.5" overflow 7px

**f_saw**
- SAW-B-0001 (#1151): E1 "두께 방향 확대 표시 · 평면 치수 비례 아님" overflow 7px
- SAW-B-0002 (#1152): E1 "expansion tape" overflow 8px · E1 "두께 방향 확대 표시 · 평면 치수 비례 아님" overflow 7px
- SAW-I-0001 (#1153): E1 "두께 방향 확대 표시 · 평면 치수 비례 아님" overflow 7px
- SAW-I-0002 (#1154): E1 "두께 방향 확대 표시 · 평면 치수 비례 아님" overflow 7px
- SAW-A-0001 (#1155): E1 "두께 방향 확대 표시 · 평면 치수 비례 아님" overflow 7px

**f_sip**
- WARP-I-0062 (#2023): E1 "단면 개념도: 신호 경로" overflow 7px · E1 "RDL" overflow 8px · E1 "두께 방향 확대 표시 · 평면 비례 근사" overflow 7px
- WARP-B-0041 (#2240): E1 "단면 개념도: 신호 경로" overflow 7px · E1 "RDL" overflow 8px · E1 "두께 방향 확대 표시 · 평면 비례 근사" overflow 7px
- WARP-B-0042 (#2241): E1 "단면 개념도: 신호 경로" overflow 7px · E1 "RDL" overflow 8px · E1 "두께 방향 확대 표시 · 평면 비례 근사" overflow 7px
- WARP-I-0181 (#2242): E1 "단면 개념도: 신호 경로" overflow 7px · E1 "RDL" overflow 8px · E1 "두께 방향 확대 표시 · 평면 비례 근사" overflow 7px
- WARP-I-0182 (#2243): E1 "단면 개념도: 신호 경로" overflow 7px · E1 "RDL" overflow 8px · E1 "두께 방향 확대 표시 · 평면 비례 근사" overflow 7px

**f_stack**
- WARP-A-0002 (#1891): E1 "두께 방향 확대 표시 · 평면 치수 비례" overflow 7px
- SIP-A-0002 (#2654): E1 "두께 방향 확대 표시 · 평면 치수 비례" overflow 7px
- SIP-A-0003 (#2655): E1 "두께 방향 확대 표시 · 평면 치수 비례" overflow 7px
- SIP-A-0004 (#2656): E1 "두께 방향 확대 표시 · 평면 치수 비례" overflow 7px
- SIP-A-0005 (#2657): E1 "두께 방향 확대 표시 · 평면 치수 비례" overflow 7px

**f_therm**
- WARP-I-0002 (#1889): E1 "적층 방향 온도 — 12단 (열은 위로 빠져나간다)" overflow 7px · E1 "core 11   95.0 °C" overflow 3px · E1 "core 10   98.8 °C" overflow 3px
- WARP-A-0001 (#1890): E1 "적층 방향 온도 — 16단 (열은 위로 빠져나간다)" overflow 7px · E1 "core 15   95.0 °C" overflow 5px · E1 "core 14   98.8 °C" overflow 5px
- WARP-A-0003 (#1932): E1 "적층 방향 온도 — 12단 (열은 위로 빠져나간다)" overflow 7px · E1 "core 11   95.0 °C" overflow 3px · E1 "core 10   97.4 °C" overflow 3px
- WARP-A-0004 (#1933): E1 "적층 방향 온도 — 20단 (열은 위로 빠져나간다)" overflow 7px · E1 "core 19   95.0 °C" overflow 6px · E1 "core 18   98.0 °C" overflow 6px
- WARP-A-0005 (#1934): E1 "적층 방향 온도 — 8단 (열은 위로 빠져나간다)" overflow 7px · E1 "core 7   90.0 °C" overflow 3px · E1 "core 6   96.0 °C" overflow 3px

**f_tsv**
- TSV-B-0001 (#0): E1 "측벽 확대 (Bosch 주기)" overflow 7px · E1 "막 구성" overflow 7px · E1 "두께 방향 확대 표시 · 평면 치수 비례 아님" overflow 7px
- TSV-B-0002 (#1): E1 "측벽 확대 (Bosch 주기)" overflow 7px · E1 "막 구성" overflow 7px · E1 "두께 방향 확대 표시 · 평면 치수 비례 아님" overflow 7px
- TSV-I-0001 (#2): E1 "측벽 확대 (Bosch 주기)" overflow 7px · E1 "막 구성" overflow 7px · E1 "두께 방향 확대 표시 · 평면 치수 비례 아님" overflow 7px
- TSV-A-0001 (#4): E1 "측벽 확대 (Bosch 주기)" overflow 7px · E1 "막 구성" overflow 7px · E1 "두께 방향 확대 표시 · 평면 치수 비례 아님" overflow 7px
- TSV-B-0003 (#6): E1 "측벽 확대 (Bosch 주기)" overflow 7px · E1 "막 구성" overflow 7px · E1 "두께 방향 확대 표시 · 평면 치수 비례 아님" overflow 7px

**f_warp**
- TSV-I-0058 (#157): E1 "측정 상황: 어느 면을 아래로 두었는가" overflow 7px · E1 "측정 기준면 (chuck)" overflow 7px · E1 "-150" overflow 7px
- TSV-I-0059 (#158): E1 "측정 상황: 어느 면을 아래로 두었는가" overflow 7px · E1 "측정 기준면 (chuck)" overflow 7px · E1 "-150" overflow 7px
- TSV-A-0049 (#159): E1 "측정 상황: 어느 면을 아래로 두었는가" overflow 7px · E1 "측정 기준면 (chuck)" overflow 7px · E1 "-150" overflow 7px
- TSV-A-0050 (#160): E1 "측정 상황: 어느 면을 아래로 두었는가" overflow 7px · E1 "측정 기준면 (chuck)" overflow 7px · E1 "-150" overflow 7px
- TSV-I-0060 (#161): E1 "측정 상황: 어느 면을 아래로 두었는가" overflow 7px · E1 "측정 기준면 (chuck)" overflow 7px · E1 "-150" overflow 7px

전체 목록은 같은 이름의 `.json` 참조 (`fig[]`: 문항별 결함, `screens{}`: 뷰포트별).
