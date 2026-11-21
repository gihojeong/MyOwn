# FEOL 리뷰 보고서 — FEOL 분야 에이전트 · 2026-11-21

## 요약
| | 초급 | 중급 | 고급 | 계 |
|---|---|---|---|---|
| 시작 문항 | 72 | 74 | 37 | 183 |
| 수정(유지 id, 전면 재작성) | 40 | 29 | 14 | 83 |
| 삭제 | 32 | 45 | 20 | 97 |
| 난이도 변경(재발급) | — | +3 | −3 | (A→I 3) |
| 추가(신규 9xxx) | 18 | 34 | 45 | 97 |
| 최종 문항 | 58 | 66 | 59 | 183 |

- 최종 비율 초급 32 % · 중급 36 % · 고급 32 %. 유지 문항도 지문·보기·해설·제목·지표·그림을 모두 새로 썼습니다(ctx 조립형 183 → stem 단일형 183).
- 메타 지표 183건 전부 제거: 지문 조건 2–4개 또는 `[]`.
- 게이트: `validate --domain FEOL --gate` 통과 — **E 0 / W 0** (I 25: I_FACT_WATCH·I_JOSA_SPACE 정보성). build + smoke: `figErr: []`, `errs: []`.
- 해설 ①–④ 참조 ↔ 보기 내용은 스크립트로 전 문항 대조 출력해 직접 확인(오케스트레이터 지시, FEOL-B-0059 포함 수정).
- 고급은 전 문항 core die·base die·HBM 스택 맥락을 넣었고, 데이터 해석형(f_table 21, f_plot 2)과 2단계 이상 계산형 위주입니다.

## 주요 기술 정정 (사실·정답·수치)
| id | 무엇이 틀렸나 | 어떻게 고쳤나 | 근거 |
|---|---|---|---|
| FEOL-A-0018 (mv SIP) | 해설이 정답 ④를 "기술 판단 항목이 아니다"로 서술(E_EXP_REF_ANSWER), 오답이 무관 항목 | PDN 재배치의 IR drop·EM ↔ 신호 배선 트랙 상충으로 재작성 | 설계 원리 |
| FEOL-I-0013 | Bosch 측벽 식각을 "Erosion"으로 표기(XD F7) | 삭제(TSV-I-0194 보유). CMP 용어 dishing/erosion은 B-9005·B-9006·I-9009·I-9010에서 F7 규약대로 구분 | XD F7 |
| FEOL-B-0067 | "14nm 이후" 같은 노드 단정 | 노드 언급 삭제, 구조 정의만 | — |
| FEOL-A-0033 | "HBM core die는 Cu pumping 때문에 BEOL 층수를 늘리기 어렵다" — 근거 불명 | 삭제(사실 근거 불명) | — |
| FEOL-I-0068 | 해설이 정답 ③을 오답처럼 서술 | 삭제(세정 시점 논리 문항, 타 분야·일반론) | — |
| FEOL-A-0019 (mv COW) | MR-MUF 서술 불명확 | X-F5 표현(적층 후 일괄 접합·액상 EMC, Advanced MR-MUF의 chip control)으로 정리, src 기재 | SK hynix Newsroom |
| FEOL-I-0057 | "얇은 barrier로 유효 단면 확보" 외 근거 혼재 | Ru·Mo: barrier 생략으로 단면 확보가 정답, 벌크 비저항은 Cu가 낮음을 오답 근거로 명시 | 교과서 |
| FEOL-I-9027 | (신규) base die 로직 공정 전환 | 업체 발표 기준임을 지문에 명시, 2,048 bit(JESD270-4) 근거, src 기재 | SK hynix–TSMC 보도자료 2024-04 |

- 수치 기준: Cu 1.7 µΩ·cm, Cu 평균 자유 행로 약 40 nm, SiO₂ k 3.9, EUV 13.5 nm/92 eV, ArF 193 nm/6.4 eV, Si 이축 탄성 계수 180 GPa, DDR 85/95 °C refresh 2배(F45). 업체 노드·EUV 층수 같은 [R] 정보는 정답 근거로 쓰지 않았습니다. 계산 문항 값은 모두 스크립트로 재계산(Black 가속 1.58e5, Ea 0.99 eV, Stoney 37 µm/12 µm, KOZ 9.4 µm 등).

## 삭제 목록 (97)
| id | 사유 |
|---|---|
| B-0001 | 타 분야(FA/신뢰성) ECM 용어, FEOL 관점 없음 |
| B-0002, B-0021, B-0033, B-0069, B-0020, I-0010, I-0049, A-0002, A-0004, A-0020 | 흡습·popcorn 근중복 — 대표 문항 A-0010을 FA로 이관 |
| B-0006, B-0015, B-0027, B-0028, I-0021 | 근중복(각각 B-0004·B-0005·B-0016·B-0029와 같은 개념) |
| B-0010, B-0013, B-0031, B-0032, B-0072, I-0002, I-0019, I-0022, I-0023, A-0006, A-0007, A-0015, A-0021, A-0030, A-0031, A-0036 | 품질 미달 재작성 불가 — 일반론·판단 태도형, 기술적 정답 근거 없음(STANDARDS §1 고급 금지 형태 포함) |
| B-0023, B-0030, B-0034, I-0011, I-0025, I-0026, I-0027, I-0028, I-0029, I-0030, I-0031, I-0032, I-0033, I-0034, I-0035, I-0036, I-0068, A-0009 | 타 분야(COW/BUMP) 접합·세정 주제, 해당 분야 보유 |
| B-0024, B-0025, B-0045, I-0037, I-0047 | 근중복: probe 문항 — B-0012·I-0009를 MET로 이관 |
| I-0012, I-0038 | 근중복: 챔버 seasoning(B-0026 보유) |
| B-0037, B-0038, B-0039, B-0040, B-0041, I-0040, I-0041, I-0042 | 타 분야(SIP PDN/SI) — 대표 B-0035·B-0042·A-0018 이관 |
| B-0044 | 타 분야 중복: SAW-B-0037 보유(XD) |
| B-0046, I-0048 | 타 분야(SIP 인터포저) |
| B-0048, I-0005 | 타 분야(TSV Bosch) — TSV 보유 |
| I-0013 | 타 분야 중복: TSV-I-0194 보유 + F7 용어 위반(XD) |
| B-0051, B-0055, B-0056 | 근중복(B-0050·B-0054) / 초급 회상 가치 낮음 |
| I-0001, A-0001 | 근중복: A-0003(BSP 이관) |
| I-0004 | 근중복: B-0022·A-0008 |
| I-0007, I-0043 | 타 분야(BSP 뒷면 절연막) |
| I-0017 | 근중복: I-0016 |
| I-0044, I-0045, I-0046, I-0069, I-0070 | 타 분야(BSP/BUMP seed·UBM) — f_bs 보유 분야 |
| I-0050 | 근중복: B-0060 |
| I-0071, I-0073, I-0074 | 근중복: I-0008·B-0070·B-0071 |
| A-0011, A-0012 | 타 분야(TSV) / 세 조건 나열형으로 정답 근거 불명 |
| A-0013, A-0014, A-0016 | 타 분야(FA/MET 분석 기법) |
| A-0029 | 타 분야 중복: WARP-A-0254 보유(XD) |
| A-0033 | 사실 근거 불명(위 정정 표) |
| A-0037 | 근중복: A-0019(XD) |


## 난이도 변경 · id 재발급
| 옛 id | 새 id | 이유 |
|---|---|---|
| FEOL-A-0017 | FEOL-I-9001 | Kelvin 4단자 구조 — 단일 개념, 중급 |
| FEOL-A-0024 | FEOL-I-9002 | gate-last 대가 — 두 공법 비교, 중급 |
| FEOL-A-0026 | FEOL-I-9003 | GAA 공정 부담 — 단일 인과, 중급 |

## 이관 제안 (mv)
| id | 대상 분야 | 이유 |
|---|---|---|
| FEOL-A-0003 | BSP | reveal 선택비 → Cu 돌출 산포 → 혼합 불량(XD) |
| FEOL-A-0010 | FA | 흡습 급속 가열 박리 기구(XD) |
| FEOL-B-0047 | FA | 뒷면 광 방출 InGaAs 검출기(XD) |
| FEOL-A-0018 | SIP | 전원망 재배치 상충(XD) |
| FEOL-B-0042 | SIP | decap 병용(XD) |
| FEOL-B-0035 | SIP | 선로 반사(XD) |
| FEOL-I-0009 | MET | probe overdrive 오판정(XD) |
| FEOL-B-0012 | MET | wafer 시험(EDS)·KGD(XD) |
| FEOL-A-0019 | COW | 극박 die + MR-MUF(XD) |

## 면제(vx) 목록
| id | 코드 | 사유 |
|---|---|---|
| FEOL-A-0034, A-9010, A-9017, A-9019, A-9027 | W_FIG_LEAK | 후보 비교표(f_table)가 보기 후보를 모두 행으로 나열하는 구조라 정답 어휘가 표에 있을 수밖에 없음. 강조(hl) 없음, 정답을 가리키는 표식 없음 |

## 신규 출제 주제 (브리프 §3 공백 대응)
- DRAM 셀: BCAT·GIDL recess, 6F², supporter·leaning, ZrO₂/Al₂O₃ 유전막(EOT 직렬 합성), 셀 용량 계산, retention·온도·refresh, 전하 공유 신호와 Cbl
- 주변회로·base die: HKMG(EOT·일함수·gate-last·DRAM 공정 순서 열예산), Pelgrom 산포, latch-up, antenna, base die 로직 공정 전환(업체 발표 기준)
- EUV·다중 패터닝: 파장·반사 광학계, 레일리 한계, 광자 수·shot noise·노광량, 확률 결함 Poisson 스택 수율, SADP pitch walking, LELE overlay 산포
- BEOL: damascene·dual damascene, barrier·liner(ALD TaN 단독 부작용), superfill·self-anneal, 크기 효과·Ru via, RC 스케일링·유효 k, EM(Black·Blech·Co cap·이중 분포·Ea·n), SIV, hillock, TDDB·via overlay, resist poisoning
- CMP(F7 규약): dishing/erosion 구분, 밀도·dummy fill, 2단계 CMP, BTA, 광부식, Preston, 과연마 창, HCB pad recess·크기, low-k CMP 박리
- low-k·CPI: 정의·기계 강도, ashing 손상·bake 판별, seal ring·수분, bump 아래 crack·접합 하중, probe CUP, 층별 ILD 배분, BEOL 열저항
- TSV 정합: via-middle 순서·liner 온도(silicide·HKMG), Cu pumping·CMP 전 열처리 온도 선택, KOZ(응력 감쇠·n/p 측정·면적)
- 막 응력: Stoney(wafer → 얇은 die), 앞뒷면 막 균형(부호)

## 남은 우려 · EA/DA 에 요청
- EA: B-0012·B-0035·B-0042·B-0047·I-0009는 이관 대상이라 FEOL 맥락이 약합니다(이관 후 대상 분야 판독 권장).
- EA: 가정 수치(ULK 허용 응력 50 MPa, (jL)c 3,000 A/cm, base die 후보 상대값 등)는 지문에 "가정·설정값"으로 표기했습니다. 정답 근거가 아닌 계산 조건입니다.
- EA: 정답 위치는 조정하지 않았습니다(Phase 2). A-9019·A-9010처럼 보기가 표 행에 대응하는 문항도 swap 가능.
- DA: f_film 프리셋 6종(beol·cell·gate·pad·tsv·litho)을 k=0 주제도로 반복 사용합니다. 레이아웃 확인 요청(smoke 오류 없음).
