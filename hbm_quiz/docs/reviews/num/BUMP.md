# NUM 수치 계산 검증 — BUMP

- 작성: NUM (수치 계산 검증 지원 에이전트) · 2026-11-20 · 읽기 전용 검증(data 수정 없음)
- 방법: 계산 유형(가족)마다 재계산 스크립트로 전 멤버의 지문 수치를 파싱해 정답을 다시 계산하고, 정답 키·보기 값·반올림·현실 범위(STANDARDS 2.2–2.4)·그림/지표 정답 노출을 기계 대조했습니다. 비가족 문항은 같은 스크립트의 단건 solver 와 손계산으로 확인했습니다. 스크립트: scratchpad `num/solve.py`, `num/run.py`.
- 대상: 발문이 계산을 요구하거나(얼마·몇·구하·환산 등), 보기가 모두 수치이거나, 보기 3개 이상이 수치+단위인 문항, 그리고 k=1 수치 그림으로 판정하는 가족(COW-A-0003·FA-A-0003·WARP-A-0003 계열).
- 심각도: **E** = 정답 오류·정답 비유일·STANDARDS 2.4 위반 비현실 설정(반드시 수정), **I** = 참고·권고.

## 요약

| 항목 | 건수 |
|---|---|
| 재계산 검증 문항 | 197 |
| 정답 키·보기 값 일치(산술) | 197 |
| **정답 오류 확정**(보기에 정답 없음·키 오류·정답 비유일·정답 근거 결함) | **0** |
| **비현실 설정 E**(STANDARDS 2.2/2.4 범위 위반) | **54** |
| 그림·지표 정답 노출 | 113 |
| N단↔간극 수 규약 위반(STANDARDS 2.5) | 0 |
| 근접 오답(정답과 3 % 미만 차) | 0 |
| 참고(I) 현실성 메모가 있는 문항 | 7 |
| 범위 밖(수치 회상형 — 계산 아님, FACT 대상) | 2 |

## 1. 정답 오류 확정 (문항별)

없음. 산술 정답 키는 전 문항이 재계산 값과 일치합니다.

## 2. 계산 유형(가족)별 검증 결과

### 2.1 Cu pillar 평균 전류 밀도 — 84문항

- 식: `j = I ÷ (π·d²/4)`
- 산술 일치: 84/84 · 정답 오류 0 · 비현실 E 54 · 그림/지표 노출 62 · 근접 오답 0
- 판정: 정답 키는 전 멤버가 맞습니다. 그러나 0.15–0.25 A 를 지름 12–30 µm pillar 하나에 흘리는 설정은 정답값 21–442 kA/cm² 를 만듭니다. STANDARDS 2.4 기준(µbump 당 수십 mA 이하, EM 시험 영역 10 kA/cm² 급)을 크게 넘으므로 '계산은 맞다' 로 넘어갈 수 없습니다. 또 f_bump `j_kA` 에 정답 값이 들어 있어 그림이 답을 보여 줍니다.
- 권고: 전류를 10–50 mA 로 낮춰 결과가 수–수십 kA/cm² 가 되게 하고, EM 가속시험 조건이면 그렇게 명시합니다. 그림 `j_kA` 를 빼거나 k=0 으로 바꿉니다.
- 멤버: BUMP-A-0043, BUMP-A-0044, BUMP-A-0045, BUMP-A-0046, BUMP-A-0047, BUMP-A-0048, BUMP-A-0049, BUMP-A-0050, BUMP-A-0051, BUMP-A-0052, BUMP-A-0053, BUMP-A-0054, BUMP-A-0055, BUMP-A-0056, BUMP-A-0057, BUMP-A-0058, BUMP-A-0059, BUMP-A-0060, BUMP-A-0061, BUMP-A-0062, BUMP-A-0063, BUMP-A-0064, BUMP-A-0065, BUMP-A-0066, BUMP-A-0067, BUMP-A-0068, BUMP-A-0069, BUMP-A-0070, BUMP-A-0071, BUMP-A-0072, BUMP-I-0039, BUMP-I-0040, BUMP-A-0101, BUMP-A-0102, BUMP-I-0041, BUMP-I-0042, BUMP-I-0043, BUMP-A-0103, BUMP-A-0104, BUMP-I-0044, BUMP-I-0045, BUMP-I-0046, BUMP-A-0105, BUMP-A-0106, BUMP-I-0047, BUMP-I-0048, BUMP-I-0049, BUMP-A-0107, BUMP-A-0108, BUMP-I-0050, BUMP-I-0051, BUMP-I-0052, BUMP-A-0109, BUMP-A-0110, BUMP-I-0053, BUMP-I-0054, BUMP-I-0055, BUMP-A-0111, BUMP-A-0112, BUMP-I-0056, BUMP-I-0057, BUMP-I-0058, BUMP-A-0113, BUMP-A-0114, BUMP-I-0059, BUMP-I-0060, BUMP-I-0061, BUMP-A-0115, BUMP-A-0116, BUMP-I-0062, BUMP-I-0063, BUMP-I-0064, BUMP-A-0117, BUMP-A-0118, BUMP-I-0065, BUMP-I-0066, BUMP-I-0067, BUMP-A-0119, BUMP-A-0120, BUMP-I-0068, BUMP-I-0069, BUMP-I-0070, BUMP-A-0121, BUMP-A-0122

| id | 올바른 식·대입 | 올바른 값 | 정답 키 | 판정 | 이슈 |
|---|---|---|---|---|---|
| BUMP-A-0043 | j = I ÷ (πd²/4) = 0.005 A ÷ (π×(40e-4 cm)²/4 = 1.257e-05 cm²) = 0.40 kA/cm² | 0.398 kA/cm² | ① 약 0.40 kA/cm² | 일치 | 노출 fig.j_kA=0.4 |
| BUMP-A-0044 | j = I ÷ (πd²/4) = 0.05 A ÷ (π×(50e-4 cm)²/4 = 1.963e-05 cm²) = 2.55 kA/cm² | 2.55 kA/cm² | ④ 약 2.55 kA/cm² | 일치 | — |
| BUMP-A-0045 | j = I ÷ (πd²/4) = 0.08 A ÷ (π×(15e-4 cm)²/4 = 1.767e-06 cm²) = 45.27 kA/cm² | 45.27 kA/cm² | ③ 약 45.27 kA/cm² | 일치 | I pillar 당 80 mA · 평균 45.3 kA/cm² — 실사용 기준으론 EM 가속시험 수준(설정 의도 명시 권장) / 노출 fig.j_kA=45.3 |
| BUMP-A-0046 | j = I ÷ (πd²/4) = 0.02 A ÷ (π×(40e-4 cm)²/4 = 1.257e-05 cm²) = 1.59 kA/cm² | 1.59 kA/cm² | ② 약 1.59 kA/cm² | 일치 | 노출 fig.j_kA=1.6 |
| BUMP-A-0047 | j = I ÷ (πd²/4) = 0.005 A ÷ (π×(25e-4 cm)²/4 = 4.909e-06 cm²) = 1.02 kA/cm² | 1.02 kA/cm² | ① 약 1.02 kA/cm² | 일치 | — |
| BUMP-A-0048 | j = I ÷ (πd²/4) = 0.005 A ÷ (π×(50e-4 cm)²/4 = 1.963e-05 cm²) = 0.25 kA/cm² | 0.255 kA/cm² | ④ 약 0.25 kA/cm² | 일치 | — |
| BUMP-A-0049 | j = I ÷ (πd²/4) = 0.01 A ÷ (π×(15e-4 cm)²/4 = 1.767e-06 cm²) = 5.66 kA/cm² | 5.66 kA/cm² | ① 약 5.66 kA/cm² | 일치 | 노출 fig.j_kA=5.7 |
| BUMP-A-0050 | j = I ÷ (πd²/4) = 0.005 A ÷ (π×(15e-4 cm)²/4 = 1.767e-06 cm²) = 2.83 kA/cm² | 2.83 kA/cm² | ④ 약 2.83 kA/cm² | 일치 | 노출 fig.j_kA=2.8 |
| BUMP-A-0051 | j = I ÷ (πd²/4) = 0.03 A ÷ (π×(50e-4 cm)²/4 = 1.963e-05 cm²) = 1.53 kA/cm² | 1.53 kA/cm² | ③ 약 1.53 kA/cm² | 일치 | — |
| BUMP-A-0052 | j = I ÷ (πd²/4) = 0.01 A ÷ (π×(20e-4 cm)²/4 = 3.142e-06 cm²) = 3.18 kA/cm² | 3.18 kA/cm² | ③ 약 3.18 kA/cm² | 일치 | 노출 fig.j_kA=3.2 |
| BUMP-A-0053 | j = I ÷ (πd²/4) = 0.02 A ÷ (π×(50e-4 cm)²/4 = 1.963e-05 cm²) = 1.02 kA/cm² | 1.02 kA/cm² | ③ 약 1.02 kA/cm² | 일치 | — |
| BUMP-A-0054 | j = I ÷ (πd²/4) = 0.05 A ÷ (π×(20e-4 cm)²/4 = 3.142e-06 cm²) = 15.92 kA/cm² | 15.92 kA/cm² | ① 약 15.92 kA/cm² | 일치 | I pillar 당 50 mA · 평균 15.9 kA/cm² — 실사용 기준으론 EM 가속시험 수준(설정 의도 명시 권장) / 노출 fig.j_kA=15.9 |
| BUMP-A-0055 | j = I ÷ (πd²/4) = 0.03 A ÷ (π×(40e-4 cm)²/4 = 1.257e-05 cm²) = 2.39 kA/cm² | 2.39 kA/cm² | ④ 약 2.39 kA/cm² | 일치 | 노출 fig.j_kA=2.4 |
| BUMP-A-0056 | j = I ÷ (πd²/4) = 0.08 A ÷ (π×(40e-4 cm)²/4 = 1.257e-05 cm²) = 6.37 kA/cm² | 6.37 kA/cm² | ② 약 6.37 kA/cm² | 일치 | I pillar 당 80 mA · 평균 6.4 kA/cm² — 실사용 기준으론 EM 가속시험 수준(설정 의도 명시 권장) / 노출 fig.j_kA=6.4 |
| BUMP-A-0057 | j = I ÷ (πd²/4) = 0.08 A ÷ (π×(25e-4 cm)²/4 = 4.909e-06 cm²) = 16.30 kA/cm² | 16.3 kA/cm² | ② 약 16.30 kA/cm² | 일치 | I pillar 당 80 mA · 평균 16.3 kA/cm² — 실사용 기준으론 EM 가속시험 수준(설정 의도 명시 권장) / 노출 fig.j_kA=16.3 |
| BUMP-A-0058 | j = I ÷ (πd²/4) = 0.05 A ÷ (π×(30e-4 cm)²/4 = 7.069e-06 cm²) = 7.07 kA/cm² | 7.07 kA/cm² | ② 약 7.07 kA/cm² | 일치 | 노출 fig.j_kA=7.1 |
| BUMP-A-0059 | j = I ÷ (πd²/4) = 0.03 A ÷ (π×(25e-4 cm)²/4 = 4.909e-06 cm²) = 6.11 kA/cm² | 6.11 kA/cm² | ④ 약 6.11 kA/cm² | 일치 | 노출 fig.j_kA=6.1 |
| BUMP-A-0060 | j = I ÷ (πd²/4) = 0.01 A ÷ (π×(30e-4 cm)²/4 = 7.069e-06 cm²) = 1.41 kA/cm² | 1.41 kA/cm² | ④ 약 1.41 kA/cm² | 일치 | 노출 fig.j_kA=1.4 |
| BUMP-A-0061 | j = I ÷ (πd²/4) = 0.02 A ÷ (π×(15e-4 cm)²/4 = 1.767e-06 cm²) = 11.32 kA/cm² | 11.32 kA/cm² | ③ 약 11.32 kA/cm² | 일치 | 노출 fig.j_kA=11.3 |
| BUMP-A-0062 | j = I ÷ (πd²/4) = 0.05 A ÷ (π×(40e-4 cm)²/4 = 1.257e-05 cm²) = 3.98 kA/cm² | 3.98 kA/cm² | ② 약 3.98 kA/cm² | 일치 | 노출 fig.j_kA=4.0 |
| BUMP-A-0063 | j = I ÷ (πd²/4) = 0.03 A ÷ (π×(30e-4 cm)²/4 = 7.069e-06 cm²) = 4.24 kA/cm² | 4.24 kA/cm² | ④ 약 4.24 kA/cm² | 일치 | 노출 fig.j_kA=4.2 |
| BUMP-A-0064 | j = I ÷ (πd²/4) = 0.08 A ÷ (π×(50e-4 cm)²/4 = 1.963e-05 cm²) = 4.07 kA/cm² | 4.07 kA/cm² | ③ 약 4.07 kA/cm² | 일치 | I pillar 당 80 mA · 평균 4.1 kA/cm² — 실사용 기준으론 EM 가속시험 수준(설정 의도 명시 권장) / 노출 fig.j_kA=4.1 |
| BUMP-A-0065 | j = I ÷ (πd²/4) = 0.01 A ÷ (π×(50e-4 cm)²/4 = 1.963e-05 cm²) = 0.51 kA/cm² | 0.509 kA/cm² | ④ 약 0.51 kA/cm² | 일치 | — |
| BUMP-A-0066 | j = I ÷ (πd²/4) = 0.08 A ÷ (π×(20e-4 cm)²/4 = 3.142e-06 cm²) = 25.46 kA/cm² | 25.46 kA/cm² | ① 약 25.46 kA/cm² | 일치 | I pillar 당 80 mA · 평균 25.5 kA/cm² — 실사용 기준으론 EM 가속시험 수준(설정 의도 명시 권장) / 노출 fig.j_kA=25.5 |
| BUMP-A-0067 | j = I ÷ (πd²/4) = 0.02 A ÷ (π×(25e-4 cm)²/4 = 4.909e-06 cm²) = 4.07 kA/cm² | 4.07 kA/cm² | ① 약 4.07 kA/cm² | 일치 | 노출 fig.j_kA=4.1 |
| BUMP-A-0068 | j = I ÷ (πd²/4) = 0.01 A ÷ (π×(25e-4 cm)²/4 = 4.909e-06 cm²) = 2.04 kA/cm² | 2.04 kA/cm² | ③ 약 2.04 kA/cm² | 일치 | — |
| BUMP-A-0069 | j = I ÷ (πd²/4) = 0.02 A ÷ (π×(20e-4 cm)²/4 = 3.142e-06 cm²) = 6.37 kA/cm² | 6.37 kA/cm² | ① 약 6.37 kA/cm² | 일치 | 노출 fig.j_kA=6.4 |
| BUMP-A-0070 | j = I ÷ (πd²/4) = 0.03 A ÷ (π×(20e-4 cm)²/4 = 3.142e-06 cm²) = 9.55 kA/cm² | 9.55 kA/cm² | ④ 약 9.55 kA/cm² | 일치 | 노출 fig.j_kA=9.5 |
| BUMP-A-0071 | j = I ÷ (πd²/4) = 0.01 A ÷ (π×(40e-4 cm)²/4 = 1.257e-05 cm²) = 0.80 kA/cm² | 0.796 kA/cm² | ④ 약 0.80 kA/cm² | 일치 | 노출 fig.j_kA=0.8 |
| BUMP-A-0072 | j = I ÷ (πd²/4) = 0.08 A ÷ (π×(30e-4 cm)²/4 = 7.069e-06 cm²) = 11.32 kA/cm² | 11.32 kA/cm² | ② 약 11.32 kA/cm² | 일치 | I pillar 당 80 mA · 평균 11.3 kA/cm² — 실사용 기준으론 EM 가속시험 수준(설정 의도 명시 권장) / 노출 fig.j_kA=11.3 |
| BUMP-I-0039 | j = I ÷ (πd²/4) = 0.15 A ÷ (π×(12e-4 cm)²/4 = 1.131e-06 cm²) = 132.63 kA/cm² | 132.6 kA/cm² | ④ 약 132.6 kA/cm² | 일치 | **E** pillar 당 150 mA · 평균 133 kA/cm² — µbump 당 전류 수십 mA 이하·EM 시험 영역 10 kA/cm² 급(STANDARDS 2.4)을 크게 넘음 / 노출 fig.j_kA=132 |
| BUMP-I-0040 | j = I ÷ (πd²/4) = 0.15 A ÷ (π×(15e-4 cm)²/4 = 1.767e-06 cm²) = 84.88 kA/cm² | 84.88 kA/cm² | ③ 약 84.9 kA/cm² | 일치 | **E** pillar 당 150 mA · 평균 85 kA/cm² — µbump 당 전류 수십 mA 이하·EM 시험 영역 10 kA/cm² 급(STANDARDS 2.4)을 크게 넘음 / 노출 fig.j_kA=84 |
| BUMP-A-0101 | j = I ÷ (πd²/4) = 0.15 A ÷ (π×(18e-4 cm)²/4 = 2.545e-06 cm²) = 58.95 kA/cm² | 58.95 kA/cm² | ① 약 58.9 kA/cm² | 일치 | **E** pillar 당 150 mA · 평균 59 kA/cm² — µbump 당 전류 수십 mA 이하·EM 시험 영역 10 kA/cm² 급(STANDARDS 2.4)을 크게 넘음 |
| BUMP-A-0102 | j = I ÷ (πd²/4) = 0.15 A ÷ (π×(20e-4 cm)²/4 = 3.142e-06 cm²) = 47.75 kA/cm² | 47.75 kA/cm² | ③ 약 47.7 kA/cm² | 일치 | **E** pillar 당 150 mA · 평균 48 kA/cm² — µbump 당 전류 수십 mA 이하·EM 시험 영역 10 kA/cm² 급(STANDARDS 2.4)을 크게 넘음 |
| BUMP-I-0041 | j = I ÷ (πd²/4) = 0.15 A ÷ (π×(22e-4 cm)²/4 = 3.801e-06 cm²) = 39.46 kA/cm² | 39.46 kA/cm² | ① 약 39.5 kA/cm² | 일치 | **E** pillar 당 150 mA · 평균 39 kA/cm² — µbump 당 전류 수십 mA 이하·EM 시험 영역 10 kA/cm² 급(STANDARDS 2.4)을 크게 넘음 |
| BUMP-I-0042 | j = I ÷ (πd²/4) = 0.15 A ÷ (π×(25e-4 cm)²/4 = 4.909e-06 cm²) = 30.56 kA/cm² | 30.56 kA/cm² | ④ 약 30.6 kA/cm² | 일치 | **E** pillar 당 150 mA · 평균 31 kA/cm² — µbump 당 전류 수십 mA 이하·EM 시험 영역 10 kA/cm² 급(STANDARDS 2.4)을 크게 넘음 |
| BUMP-I-0043 | j = I ÷ (πd²/4) = 0.15 A ÷ (π×(28e-4 cm)²/4 = 6.158e-06 cm²) = 24.36 kA/cm² | 24.36 kA/cm² | ③ 약 24.4 kA/cm² | 일치 | **E** pillar 당 150 mA · 평균 24 kA/cm² — µbump 당 전류 수십 mA 이하·EM 시험 영역 10 kA/cm² 급(STANDARDS 2.4)을 크게 넘음 |
| BUMP-A-0103 | j = I ÷ (πd²/4) = 0.15 A ÷ (π×(30e-4 cm)²/4 = 7.069e-06 cm²) = 21.22 kA/cm² | 21.22 kA/cm² | ① 약 21.2 kA/cm² | 일치 | **E** pillar 당 150 mA · 평균 21 kA/cm² — µbump 당 전류 수십 mA 이하·EM 시험 영역 10 kA/cm² 급(STANDARDS 2.4)을 크게 넘음 / 노출 fig.j_kA=21 |
| BUMP-A-0104 | j = I ÷ (πd²/4) = 0.2 A ÷ (π×(12e-4 cm)²/4 = 1.131e-06 cm²) = 176.84 kA/cm² | 176.8 kA/cm² | ① 약 176.8 kA/cm² | 일치 | **E** pillar 당 200 mA · 평균 177 kA/cm² — µbump 당 전류 수십 mA 이하·EM 시험 영역 10 kA/cm² 급(STANDARDS 2.4)을 크게 넘음 / 노출 fig.j_kA=176 |
| BUMP-I-0044 | j = I ÷ (πd²/4) = 0.2 A ÷ (π×(15e-4 cm)²/4 = 1.767e-06 cm²) = 113.18 kA/cm² | 113.2 kA/cm² | ① 약 113.2 kA/cm² | 일치 | **E** pillar 당 200 mA · 평균 113 kA/cm² — µbump 당 전류 수십 mA 이하·EM 시험 영역 10 kA/cm² 급(STANDARDS 2.4)을 크게 넘음 / 노출 fig.j_kA=113 |
| BUMP-I-0045 | j = I ÷ (πd²/4) = 0.2 A ÷ (π×(18e-4 cm)²/4 = 2.545e-06 cm²) = 78.60 kA/cm² | 78.6 kA/cm² | ③ 약 78.6 kA/cm² | 일치 | **E** pillar 당 200 mA · 평균 79 kA/cm² — µbump 당 전류 수십 mA 이하·EM 시험 영역 10 kA/cm² 급(STANDARDS 2.4)을 크게 넘음 / 노출 fig.j_kA=78 |
| BUMP-I-0046 | j = I ÷ (πd²/4) = 0.2 A ÷ (π×(20e-4 cm)²/4 = 3.142e-06 cm²) = 63.66 kA/cm² | 63.66 kA/cm² | ② 약 63.7 kA/cm² | 일치 | **E** pillar 당 200 mA · 평균 64 kA/cm² — µbump 당 전류 수십 mA 이하·EM 시험 영역 10 kA/cm² 급(STANDARDS 2.4)을 크게 넘음 / 노출 fig.j_kA=63 |
| BUMP-A-0105 | j = I ÷ (πd²/4) = 0.2 A ÷ (π×(22e-4 cm)²/4 = 3.801e-06 cm²) = 52.61 kA/cm² | 52.61 kA/cm² | ① 약 52.6 kA/cm² | 일치 | **E** pillar 당 200 mA · 평균 53 kA/cm² — µbump 당 전류 수십 mA 이하·EM 시험 영역 10 kA/cm² 급(STANDARDS 2.4)을 크게 넘음 |
| BUMP-A-0106 | j = I ÷ (πd²/4) = 0.2 A ÷ (π×(25e-4 cm)²/4 = 4.909e-06 cm²) = 40.74 kA/cm² | 40.74 kA/cm² | ④ 약 40.7 kA/cm² | 일치 | **E** pillar 당 200 mA · 평균 41 kA/cm² — µbump 당 전류 수십 mA 이하·EM 시험 영역 10 kA/cm² 급(STANDARDS 2.4)을 크게 넘음 |
| BUMP-I-0047 | j = I ÷ (πd²/4) = 0.2 A ÷ (π×(28e-4 cm)²/4 = 6.158e-06 cm²) = 32.48 kA/cm² | 32.48 kA/cm² | ④ 약 32.5 kA/cm² | 일치 | **E** pillar 당 200 mA · 평균 32 kA/cm² — µbump 당 전류 수십 mA 이하·EM 시험 영역 10 kA/cm² 급(STANDARDS 2.4)을 크게 넘음 |
| BUMP-I-0048 | j = I ÷ (πd²/4) = 0.2 A ÷ (π×(30e-4 cm)²/4 = 7.069e-06 cm²) = 28.29 kA/cm² | 28.29 kA/cm² | ② 약 28.3 kA/cm² | 일치 | **E** pillar 당 200 mA · 평균 28 kA/cm² — µbump 당 전류 수십 mA 이하·EM 시험 영역 10 kA/cm² 급(STANDARDS 2.4)을 크게 넘음 / 노출 fig.j_kA=28 |
| BUMP-I-0049 | j = I ÷ (πd²/4) = 0.25 A ÷ (π×(12e-4 cm)²/4 = 1.131e-06 cm²) = 221.05 kA/cm² | 221.0 kA/cm² | ④ 약 221.0 kA/cm² | 일치 | **E** pillar 당 250 mA · 평균 221 kA/cm² — µbump 당 전류 수십 mA 이하·EM 시험 영역 10 kA/cm² 급(STANDARDS 2.4)을 크게 넘음 / 노출 fig.j_kA=221 |
| BUMP-A-0107 | j = I ÷ (πd²/4) = 0.25 A ÷ (π×(15e-4 cm)²/4 = 1.767e-06 cm²) = 141.47 kA/cm² | 141.5 kA/cm² | ② 약 141.5 kA/cm² | 일치 | **E** pillar 당 250 mA · 평균 141 kA/cm² — µbump 당 전류 수십 mA 이하·EM 시험 영역 10 kA/cm² 급(STANDARDS 2.4)을 크게 넘음 / 노출 fig.j_kA=141 |
| BUMP-A-0108 | j = I ÷ (πd²/4) = 0.25 A ÷ (π×(18e-4 cm)²/4 = 2.545e-06 cm²) = 98.24 kA/cm² | 98.24 kA/cm² | ③ 약 98.2 kA/cm² | 일치 | **E** pillar 당 250 mA · 평균 98 kA/cm² — µbump 당 전류 수십 mA 이하·EM 시험 영역 10 kA/cm² 급(STANDARDS 2.4)을 크게 넘음 / 노출 fig.j_kA=98 |
| BUMP-I-0050 | j = I ÷ (πd²/4) = 0.25 A ÷ (π×(20e-4 cm)²/4 = 3.142e-06 cm²) = 79.58 kA/cm² | 79.58 kA/cm² | ② 약 79.6 kA/cm² | 일치 | **E** pillar 당 250 mA · 평균 80 kA/cm² — µbump 당 전류 수십 mA 이하·EM 시험 영역 10 kA/cm² 급(STANDARDS 2.4)을 크게 넘음 / 노출 fig.j_kA=79 |
| BUMP-I-0051 | j = I ÷ (πd²/4) = 0.25 A ÷ (π×(22e-4 cm)²/4 = 3.801e-06 cm²) = 65.77 kA/cm² | 65.77 kA/cm² | ① 약 65.8 kA/cm² | 일치 | **E** pillar 당 250 mA · 평균 66 kA/cm² — µbump 당 전류 수십 mA 이하·EM 시험 영역 10 kA/cm² 급(STANDARDS 2.4)을 크게 넘음 |
| BUMP-I-0052 | j = I ÷ (πd²/4) = 0.25 A ÷ (π×(25e-4 cm)²/4 = 4.909e-06 cm²) = 50.93 kA/cm² | 50.93 kA/cm² | ④ 약 50.9 kA/cm² | 일치 | **E** pillar 당 250 mA · 평균 51 kA/cm² — µbump 당 전류 수십 mA 이하·EM 시험 영역 10 kA/cm² 급(STANDARDS 2.4)을 크게 넘음 |
| BUMP-A-0109 | j = I ÷ (πd²/4) = 0.25 A ÷ (π×(28e-4 cm)²/4 = 6.158e-06 cm²) = 40.60 kA/cm² | 40.6 kA/cm² | ③ 약 40.6 kA/cm² | 일치 | **E** pillar 당 250 mA · 평균 41 kA/cm² — µbump 당 전류 수십 mA 이하·EM 시험 영역 10 kA/cm² 급(STANDARDS 2.4)을 크게 넘음 |
| BUMP-A-0110 | j = I ÷ (πd²/4) = 0.25 A ÷ (π×(30e-4 cm)²/4 = 7.069e-06 cm²) = 35.37 kA/cm² | 35.37 kA/cm² | ③ 약 35.4 kA/cm² | 일치 | **E** pillar 당 250 mA · 평균 35 kA/cm² — µbump 당 전류 수십 mA 이하·EM 시험 영역 10 kA/cm² 급(STANDARDS 2.4)을 크게 넘음 / 노출 fig.j_kA=35 |
| BUMP-I-0053 | j = I ÷ (πd²/4) = 0.3 A ÷ (π×(12e-4 cm)²/4 = 1.131e-06 cm²) = 265.26 kA/cm² | 265.3 kA/cm² | ③ 약 265.3 kA/cm² | 일치 | **E** pillar 당 300 mA · 평균 265 kA/cm² — µbump 당 전류 수십 mA 이하·EM 시험 영역 10 kA/cm² 급(STANDARDS 2.4)을 크게 넘음 / 노출 fig.j_kA=265 |
| BUMP-I-0054 | j = I ÷ (πd²/4) = 0.3 A ÷ (π×(15e-4 cm)²/4 = 1.767e-06 cm²) = 169.77 kA/cm² | 169.8 kA/cm² | ② 약 169.8 kA/cm² | 일치 | **E** pillar 당 300 mA · 평균 170 kA/cm² — µbump 당 전류 수십 mA 이하·EM 시험 영역 10 kA/cm² 급(STANDARDS 2.4)을 크게 넘음 / 노출 fig.j_kA=169 |
| BUMP-I-0055 | j = I ÷ (πd²/4) = 0.3 A ÷ (π×(18e-4 cm)²/4 = 2.545e-06 cm²) = 117.89 kA/cm² | 117.9 kA/cm² | ① 약 117.9 kA/cm² | 일치 | **E** pillar 당 300 mA · 평균 118 kA/cm² — µbump 당 전류 수십 mA 이하·EM 시험 영역 10 kA/cm² 급(STANDARDS 2.4)을 크게 넘음 / 노출 fig.j_kA=117 |
| BUMP-A-0111 | j = I ÷ (πd²/4) = 0.3 A ÷ (π×(20e-4 cm)²/4 = 3.142e-06 cm²) = 95.49 kA/cm² | 95.49 kA/cm² | ② 약 95.5 kA/cm² | 일치 | **E** pillar 당 300 mA · 평균 95 kA/cm² — µbump 당 전류 수십 mA 이하·EM 시험 영역 10 kA/cm² 급(STANDARDS 2.4)을 크게 넘음 / 노출 fig.j_kA=95 |
| BUMP-A-0112 | j = I ÷ (πd²/4) = 0.3 A ÷ (π×(22e-4 cm)²/4 = 3.801e-06 cm²) = 78.92 kA/cm² | 78.92 kA/cm² | ② 약 78.9 kA/cm² | 일치 | **E** pillar 당 300 mA · 평균 79 kA/cm² — µbump 당 전류 수십 mA 이하·EM 시험 영역 10 kA/cm² 급(STANDARDS 2.4)을 크게 넘음 |
| BUMP-I-0056 | j = I ÷ (πd²/4) = 0.3 A ÷ (π×(25e-4 cm)²/4 = 4.909e-06 cm²) = 61.12 kA/cm² | 61.12 kA/cm² | ② 약 61.1 kA/cm² | 일치 | **E** pillar 당 300 mA · 평균 61 kA/cm² — µbump 당 전류 수십 mA 이하·EM 시험 영역 10 kA/cm² 급(STANDARDS 2.4)을 크게 넘음 / 노출 fig.j_kA=61 |
| BUMP-I-0057 | j = I ÷ (πd²/4) = 0.3 A ÷ (π×(28e-4 cm)²/4 = 6.158e-06 cm²) = 48.72 kA/cm² | 48.72 kA/cm² | ③ 약 48.7 kA/cm² | 일치 | **E** pillar 당 300 mA · 평균 49 kA/cm² — µbump 당 전류 수십 mA 이하·EM 시험 영역 10 kA/cm² 급(STANDARDS 2.4)을 크게 넘음 |
| BUMP-I-0058 | j = I ÷ (πd²/4) = 0.3 A ÷ (π×(30e-4 cm)²/4 = 7.069e-06 cm²) = 42.44 kA/cm² | 42.44 kA/cm² | ① 약 42.4 kA/cm² | 일치 | **E** pillar 당 300 mA · 평균 42 kA/cm² — µbump 당 전류 수십 mA 이하·EM 시험 영역 10 kA/cm² 급(STANDARDS 2.4)을 크게 넘음 / 노출 fig.j_kA=42 |
| BUMP-A-0113 | j = I ÷ (πd²/4) = 0.35 A ÷ (π×(12e-4 cm)²/4 = 1.131e-06 cm²) = 309.47 kA/cm² | 309.5 kA/cm² | ① 약 309.5 kA/cm² | 일치 | **E** pillar 당 350 mA · 평균 309 kA/cm² — µbump 당 전류 수십 mA 이하·EM 시험 영역 10 kA/cm² 급(STANDARDS 2.4)을 크게 넘음 / 노출 fig.j_kA=309 |
| BUMP-A-0114 | j = I ÷ (πd²/4) = 0.35 A ÷ (π×(15e-4 cm)²/4 = 1.767e-06 cm²) = 198.06 kA/cm² | 198.1 kA/cm² | ③ 약 198.1 kA/cm² | 일치 | **E** pillar 당 350 mA · 평균 198 kA/cm² — µbump 당 전류 수십 mA 이하·EM 시험 영역 10 kA/cm² 급(STANDARDS 2.4)을 크게 넘음 / 노출 fig.j_kA=198 |
| BUMP-I-0059 | j = I ÷ (πd²/4) = 0.35 A ÷ (π×(18e-4 cm)²/4 = 2.545e-06 cm²) = 137.54 kA/cm² | 137.5 kA/cm² | ④ 약 137.5 kA/cm² | 일치 | **E** pillar 당 350 mA · 평균 138 kA/cm² — µbump 당 전류 수십 mA 이하·EM 시험 영역 10 kA/cm² 급(STANDARDS 2.4)을 크게 넘음 / 노출 fig.j_kA=137 |
| BUMP-I-0060 | j = I ÷ (πd²/4) = 0.35 A ÷ (π×(20e-4 cm)²/4 = 3.142e-06 cm²) = 111.41 kA/cm² | 111.4 kA/cm² | ① 약 111.4 kA/cm² | 일치 | **E** pillar 당 350 mA · 평균 111 kA/cm² — µbump 당 전류 수십 mA 이하·EM 시험 영역 10 kA/cm² 급(STANDARDS 2.4)을 크게 넘음 / 노출 fig.j_kA=111 |
| BUMP-I-0061 | j = I ÷ (πd²/4) = 0.35 A ÷ (π×(22e-4 cm)²/4 = 3.801e-06 cm²) = 92.07 kA/cm² | 92.07 kA/cm² | ④ 약 92.1 kA/cm² | 일치 | **E** pillar 당 350 mA · 평균 92 kA/cm² — µbump 당 전류 수십 mA 이하·EM 시험 영역 10 kA/cm² 급(STANDARDS 2.4)을 크게 넘음 / 노출 fig.j_kA=92 |
| BUMP-A-0115 | j = I ÷ (πd²/4) = 0.35 A ÷ (π×(25e-4 cm)²/4 = 4.909e-06 cm²) = 71.30 kA/cm² | 71.3 kA/cm² | ① 약 71.3 kA/cm² | 일치 | **E** pillar 당 350 mA · 평균 71 kA/cm² — µbump 당 전류 수십 mA 이하·EM 시험 영역 10 kA/cm² 급(STANDARDS 2.4)을 크게 넘음 / 노출 fig.j_kA=71 |
| BUMP-A-0116 | j = I ÷ (πd²/4) = 0.35 A ÷ (π×(28e-4 cm)²/4 = 6.158e-06 cm²) = 56.84 kA/cm² | 56.84 kA/cm² | ② 약 56.8 kA/cm² | 일치 | **E** pillar 당 350 mA · 평균 57 kA/cm² — µbump 당 전류 수십 mA 이하·EM 시험 영역 10 kA/cm² 급(STANDARDS 2.4)을 크게 넘음 |
| BUMP-I-0062 | j = I ÷ (πd²/4) = 0.35 A ÷ (π×(30e-4 cm)²/4 = 7.069e-06 cm²) = 49.51 kA/cm² | 49.51 kA/cm² | ② 약 49.5 kA/cm² | 일치 | **E** pillar 당 350 mA · 평균 50 kA/cm² — µbump 당 전류 수십 mA 이하·EM 시험 영역 10 kA/cm² 급(STANDARDS 2.4)을 크게 넘음 / 노출 fig.j_kA=49 |
| BUMP-I-0063 | j = I ÷ (πd²/4) = 0.4 A ÷ (π×(12e-4 cm)²/4 = 1.131e-06 cm²) = 353.68 kA/cm² | 353.7 kA/cm² | ④ 약 353.7 kA/cm² | 일치 | **E** pillar 당 400 mA · 평균 354 kA/cm² — µbump 당 전류 수십 mA 이하·EM 시험 영역 10 kA/cm² 급(STANDARDS 2.4)을 크게 넘음 / 노출 fig.j_kA=353 |
| BUMP-I-0064 | j = I ÷ (πd²/4) = 0.4 A ÷ (π×(15e-4 cm)²/4 = 1.767e-06 cm²) = 226.35 kA/cm² | 226.4 kA/cm² | ① 약 226.4 kA/cm² | 일치 | **E** pillar 당 400 mA · 평균 226 kA/cm² — µbump 당 전류 수십 mA 이하·EM 시험 영역 10 kA/cm² 급(STANDARDS 2.4)을 크게 넘음 / 노출 fig.j_kA=226 |
| BUMP-A-0117 | j = I ÷ (πd²/4) = 0.4 A ÷ (π×(18e-4 cm)²/4 = 2.545e-06 cm²) = 157.19 kA/cm² | 157.2 kA/cm² | ③ 약 157.2 kA/cm² | 일치 | **E** pillar 당 400 mA · 평균 157 kA/cm² — µbump 당 전류 수십 mA 이하·EM 시험 영역 10 kA/cm² 급(STANDARDS 2.4)을 크게 넘음 / 노출 fig.j_kA=157 |
| BUMP-A-0118 | j = I ÷ (πd²/4) = 0.4 A ÷ (π×(20e-4 cm)²/4 = 3.142e-06 cm²) = 127.32 kA/cm² | 127.3 kA/cm² | ① 약 127.3 kA/cm² | 일치 | **E** pillar 당 400 mA · 평균 127 kA/cm² — µbump 당 전류 수십 mA 이하·EM 시험 영역 10 kA/cm² 급(STANDARDS 2.4)을 크게 넘음 / 노출 fig.j_kA=127 |
| BUMP-I-0065 | j = I ÷ (πd²/4) = 0.4 A ÷ (π×(22e-4 cm)²/4 = 3.801e-06 cm²) = 105.23 kA/cm² | 105.2 kA/cm² | ① 약 105.2 kA/cm² | 일치 | **E** pillar 당 400 mA · 평균 105 kA/cm² — µbump 당 전류 수십 mA 이하·EM 시험 영역 10 kA/cm² 급(STANDARDS 2.4)을 크게 넘음 / 노출 fig.j_kA=105 |
| BUMP-I-0066 | j = I ÷ (πd²/4) = 0.4 A ÷ (π×(25e-4 cm)²/4 = 4.909e-06 cm²) = 81.49 kA/cm² | 81.49 kA/cm² | ③ 약 81.5 kA/cm² | 일치 | **E** pillar 당 400 mA · 평균 81 kA/cm² — µbump 당 전류 수십 mA 이하·EM 시험 영역 10 kA/cm² 급(STANDARDS 2.4)을 크게 넘음 / 노출 fig.j_kA=81 |
| BUMP-I-0067 | j = I ÷ (πd²/4) = 0.4 A ÷ (π×(28e-4 cm)²/4 = 6.158e-06 cm²) = 64.96 kA/cm² | 64.96 kA/cm² | ③ 약 65.0 kA/cm² | 일치 | **E** pillar 당 400 mA · 평균 65 kA/cm² — µbump 당 전류 수십 mA 이하·EM 시험 영역 10 kA/cm² 급(STANDARDS 2.4)을 크게 넘음 |
| BUMP-A-0119 | j = I ÷ (πd²/4) = 0.4 A ÷ (π×(30e-4 cm)²/4 = 7.069e-06 cm²) = 56.59 kA/cm² | 56.59 kA/cm² | ③ 약 56.6 kA/cm² | 일치 | **E** pillar 당 400 mA · 평균 57 kA/cm² — µbump 당 전류 수십 mA 이하·EM 시험 영역 10 kA/cm² 급(STANDARDS 2.4)을 크게 넘음 / 노출 fig.j_kA=56 |
| BUMP-A-0120 | j = I ÷ (πd²/4) = 0.5 A ÷ (π×(12e-4 cm)²/4 = 1.131e-06 cm²) = 442.10 kA/cm² | 442.1 kA/cm² | ② 약 442.1 kA/cm² | 일치 | **E** pillar 당 500 mA · 평균 442 kA/cm² — µbump 당 전류 수십 mA 이하·EM 시험 영역 10 kA/cm² 급(STANDARDS 2.4)을 크게 넘음 / 노출 fig.j_kA=442 |
| BUMP-I-0068 | j = I ÷ (πd²/4) = 0.5 A ÷ (π×(15e-4 cm)²/4 = 1.767e-06 cm²) = 282.94 kA/cm² | 282.9 kA/cm² | ① 약 282.9 kA/cm² | 일치 | **E** pillar 당 500 mA · 평균 283 kA/cm² — µbump 당 전류 수십 mA 이하·EM 시험 영역 10 kA/cm² 급(STANDARDS 2.4)을 크게 넘음 / 노출 fig.j_kA=282 |
| BUMP-I-0069 | j = I ÷ (πd²/4) = 0.5 A ÷ (π×(18e-4 cm)²/4 = 2.545e-06 cm²) = 196.49 kA/cm² | 196.5 kA/cm² | ④ 약 196.5 kA/cm² | 일치 | **E** pillar 당 500 mA · 평균 196 kA/cm² — µbump 당 전류 수십 mA 이하·EM 시험 영역 10 kA/cm² 급(STANDARDS 2.4)을 크게 넘음 / 노출 fig.j_kA=196 |
| BUMP-I-0070 | j = I ÷ (πd²/4) = 0.5 A ÷ (π×(20e-4 cm)²/4 = 3.142e-06 cm²) = 159.15 kA/cm² | 159.2 kA/cm² | ③ 약 159.2 kA/cm² | 일치 | **E** pillar 당 500 mA · 평균 159 kA/cm² — µbump 당 전류 수십 mA 이하·EM 시험 영역 10 kA/cm² 급(STANDARDS 2.4)을 크게 넘음 / 노출 fig.j_kA=159 |
| BUMP-A-0121 | j = I ÷ (πd²/4) = 0.5 A ÷ (π×(22e-4 cm)²/4 = 3.801e-06 cm²) = 131.53 kA/cm² | 131.5 kA/cm² | ③ 약 131.5 kA/cm² | 일치 | **E** pillar 당 500 mA · 평균 132 kA/cm² — µbump 당 전류 수십 mA 이하·EM 시험 영역 10 kA/cm² 급(STANDARDS 2.4)을 크게 넘음 / 노출 fig.j_kA=131 |
| BUMP-A-0122 | j = I ÷ (πd²/4) = 0.5 A ÷ (π×(25e-4 cm)²/4 = 4.909e-06 cm²) = 101.86 kA/cm² | 101.9 kA/cm² | ③ 약 101.9 kA/cm² | 일치 | **E** pillar 당 500 mA · 평균 102 kA/cm² — µbump 당 전류 수십 mA 이하·EM 시험 영역 10 kA/cm² 급(STANDARDS 2.4)을 크게 넘음 / 노출 fig.j_kA=101 |

### 2.2 IMC 두께 x = k√t — 54문항

- 식: `x = k·√t`
- 산술 일치: 54/54 · 정답 오류 0 · 비현실 E 0 · 그림/지표 노출 44 · 근접 오답 0
- 판정: 정답 키는 전 멤버가 맞습니다. f_bump `imc_um` 이 정답 두께와 같아 그림이 답을 보여 줍니다. 보기 세트가 멤버 사이에 동일합니다(예: 0.62/1.58/3.16/25.00 µm 가 여러 문항에 반복). 지문의 '관리 기준' 만 바뀌는 근중복입니다.
- 권고: `imc_um` 을 빼고(템플릿 기본값을 피하려면 k=0), 가족 정리 시 관리 기준이 아니라 묻는 값이 다른 문항만 남깁니다.
- 멤버: BUMP-I-0071, BUMP-I-0072, BUMP-A-0123, BUMP-A-0124, BUMP-I-0073, BUMP-I-0074, BUMP-I-0075, BUMP-A-0125, BUMP-A-0126, BUMP-I-0076, BUMP-I-0077, BUMP-I-0078, BUMP-A-0127, BUMP-A-0128, BUMP-I-0079, BUMP-I-0080, BUMP-I-0081, BUMP-A-0129, BUMP-A-0130, BUMP-I-0082, BUMP-I-0083, BUMP-I-0084, BUMP-A-0131, BUMP-A-0132, BUMP-I-0085, BUMP-I-0086, BUMP-I-0087, BUMP-A-0133, BUMP-A-0134, BUMP-I-0088, BUMP-I-0089, BUMP-I-0090, BUMP-A-0135, BUMP-A-0136, BUMP-I-0091, BUMP-I-0092, BUMP-I-0093, BUMP-A-0137, BUMP-A-0138, BUMP-I-0094, BUMP-I-0095, BUMP-I-0096, BUMP-A-0139, BUMP-A-0140, BUMP-I-0097, BUMP-I-0098, BUMP-I-0099, BUMP-A-0141, BUMP-A-0142, BUMP-I-0100, BUMP-I-0101, BUMP-I-0102, BUMP-A-0143, BUMP-A-0144

| id | 올바른 식·대입 | 올바른 값 | 정답 키 | 판정 | 이슈 |
|---|---|---|---|---|---|
| BUMP-I-0071 | x = k√t = 0.1 × √250 = 1.58 µm | 1.58 µm | ③ 약 1.58 µm | 일치 | 노출 fig.imc_um=1.58 |
| BUMP-I-0072 | x = k√t = 0.1 × √250 = 1.58 µm | 1.58 µm | ③ 약 1.58 µm | 일치 | 노출 fig.imc_um=1.58 |
| BUMP-A-0123 | x = k√t = 0.1 × √250 = 1.58 µm | 1.58 µm | ① 약 1.58 µm | 일치 | 노출 fig.imc_um=1.58 |
| BUMP-A-0124 | x = k√t = 0.1 × √250 = 1.58 µm | 1.58 µm | ① 약 1.58 µm | 일치 | 노출 fig.imc_um=1.58 |
| BUMP-I-0073 | x = k√t = 0.1 × √500 = 2.24 µm | 2.24 µm | ④ 약 2.24 µm | 일치 | 노출 fig.imc_um=2.24 |
| BUMP-I-0074 | x = k√t = 0.1 × √500 = 2.24 µm | 2.24 µm | ② 약 2.24 µm | 일치 | 노출 fig.imc_um=2.24 |
| BUMP-I-0075 | x = k√t = 0.1 × √500 = 2.24 µm | 2.24 µm | ④ 약 2.24 µm | 일치 | 노출 fig.imc_um=2.24 |
| BUMP-A-0125 | x = k√t = 0.1 × √500 = 2.24 µm | 2.24 µm | ④ 약 2.24 µm | 일치 | 노출 fig.imc_um=2.24 |
| BUMP-A-0126 | x = k√t = 0.1 × √750 = 2.74 µm | 2.74 µm | ① 약 2.74 µm | 일치 | 노출 fig.imc_um=2.74 |
| BUMP-I-0076 | x = k√t = 0.1 × √750 = 2.74 µm | 2.74 µm | ③ 약 2.74 µm | 일치 | 노출 fig.imc_um=2.74 |
| BUMP-I-0077 | x = k√t = 0.1 × √750 = 2.74 µm | 2.74 µm | ② 약 2.74 µm | 일치 | 노출 fig.imc_um=2.74 |
| BUMP-I-0078 | x = k√t = 0.1 × √750 = 2.74 µm | 2.74 µm | ② 약 2.74 µm | 일치 | 노출 fig.imc_um=2.74 |
| BUMP-A-0127 | x = k√t = 0.1 × √1000 = 3.16 µm | 3.16 µm | ④ 약 3.16 µm | 일치 | 노출 fig.imc_um=3.16 |
| BUMP-A-0128 | x = k√t = 0.1 × √1000 = 3.16 µm | 3.16 µm | ① 약 3.16 µm | 일치 | 노출 fig.imc_um=3.16 |
| BUMP-I-0079 | x = k√t = 0.1 × √1000 = 3.16 µm | 3.16 µm | ① 약 3.16 µm | 일치 | 노출 fig.imc_um=3.16 |
| BUMP-I-0080 | x = k√t = 0.1 × √1000 = 3.16 µm | 3.16 µm | ④ 약 3.16 µm | 일치 | 노출 fig.imc_um=3.16 |
| BUMP-I-0081 | x = k√t = 0.1 × √1500 = 3.87 µm | 3.87 µm | ④ 약 3.87 µm | 일치 | 노출 fig.imc_um=3.87 |
| BUMP-A-0129 | x = k√t = 0.1 × √1500 = 3.87 µm | 3.87 µm | ③ 약 3.87 µm | 일치 | 노출 fig.imc_um=3.87 |
| BUMP-A-0130 | x = k√t = 0.1 × √1500 = 3.87 µm | 3.87 µm | ① 약 3.87 µm | 일치 | 노출 fig.imc_um=3.87 |
| BUMP-I-0082 | x = k√t = 0.1 × √1500 = 3.87 µm | 3.87 µm | ① 약 3.87 µm | 일치 | 노출 fig.imc_um=3.87 |
| BUMP-I-0083 | x = k√t = 0.12 × √250 = 1.90 µm | 1.9 µm | ④ 약 1.90 µm | 일치 | 노출 fig.imc_um=1.9 |
| BUMP-I-0084 | x = k√t = 0.12 × √250 = 1.90 µm | 1.9 µm | ① 약 1.90 µm | 일치 | 노출 fig.imc_um=1.9 |
| BUMP-A-0131 | x = k√t = 0.12 × √250 = 1.90 µm | 1.9 µm | ① 약 1.90 µm | 일치 | 노출 fig.imc_um=1.9 |
| BUMP-A-0132 | x = k√t = 0.12 × √250 = 1.90 µm | 1.9 µm | ③ 약 1.90 µm | 일치 | 노출 fig.imc_um=1.9 |
| BUMP-I-0085 | x = k√t = 0.12 × √500 = 2.68 µm | 2.68 µm | ② 약 2.68 µm | 일치 | 노출 fig.imc_um=2.68 |
| BUMP-I-0086 | x = k√t = 0.12 × √500 = 2.68 µm | 2.68 µm | ④ 약 2.68 µm | 일치 | 노출 fig.imc_um=2.68 |
| BUMP-I-0087 | x = k√t = 0.12 × √500 = 2.68 µm | 2.68 µm | ② 약 2.68 µm | 일치 | 노출 fig.imc_um=2.68 |
| BUMP-A-0133 | x = k√t = 0.12 × √500 = 2.68 µm | 2.68 µm | ④ 약 2.68 µm | 일치 | 노출 fig.imc_um=2.68 |
| BUMP-A-0134 | x = k√t = 0.12 × √750 = 3.29 µm | 3.29 µm | ③ 약 3.29 µm | 일치 | 노출 fig.imc_um=3.29 |
| BUMP-I-0088 | x = k√t = 0.12 × √750 = 3.29 µm | 3.29 µm | ③ 약 3.29 µm | 일치 | 노출 fig.imc_um=3.29 |
| BUMP-I-0089 | x = k√t = 0.12 × √750 = 3.29 µm | 3.29 µm | ④ 약 3.29 µm | 일치 | 노출 fig.imc_um=3.29 |
| BUMP-I-0090 | x = k√t = 0.12 × √750 = 3.29 µm | 3.29 µm | ③ 약 3.29 µm | 일치 | 노출 fig.imc_um=3.29 |
| BUMP-A-0135 | x = k√t = 0.12 × √1000 = 3.79 µm | 3.79 µm | ② 약 3.79 µm | 일치 | 노출 fig.imc_um=3.79 |
| BUMP-A-0136 | x = k√t = 0.12 × √1000 = 3.79 µm | 3.79 µm | ④ 약 3.79 µm | 일치 | 노출 fig.imc_um=3.79 |
| BUMP-I-0091 | x = k√t = 0.12 × √1000 = 3.79 µm | 3.79 µm | ① 약 3.79 µm | 일치 | 노출 fig.imc_um=3.79 |
| BUMP-I-0092 | x = k√t = 0.12 × √1000 = 3.79 µm | 3.79 µm | ③ 약 3.79 µm | 일치 | 노출 fig.imc_um=3.79 |
| BUMP-I-0095 | x = k√t = 0.16 × √250 = 2.53 µm | 2.53 µm | ③ 약 2.53 µm | 일치 | 노출 fig.imc_um=2.53 |
| BUMP-I-0096 | x = k√t = 0.16 × √250 = 2.53 µm | 2.53 µm | ② 약 2.53 µm | 일치 | 노출 fig.imc_um=2.53 |
| BUMP-A-0139 | x = k√t = 0.16 × √250 = 2.53 µm | 2.53 µm | ③ 약 2.53 µm | 일치 | 노출 fig.imc_um=2.53 |
| BUMP-A-0140 | x = k√t = 0.16 × √250 = 2.53 µm | 2.53 µm | ① 약 2.53 µm | 일치 | 노출 fig.imc_um=2.53 |
| BUMP-I-0097 | x = k√t = 0.16 × √500 = 3.58 µm | 3.58 µm | ② 약 3.58 µm | 일치 | 노출 fig.imc_um=3.58 |
| BUMP-I-0098 | x = k√t = 0.16 × √500 = 3.58 µm | 3.58 µm | ② 약 3.58 µm | 일치 | 노출 fig.imc_um=3.58 |
| BUMP-I-0099 | x = k√t = 0.16 × √500 = 3.58 µm | 3.58 µm | ③ 약 3.58 µm | 일치 | 노출 fig.imc_um=3.58 |
| BUMP-A-0141 | x = k√t = 0.16 × √500 = 3.58 µm | 3.58 µm | ④ 약 3.58 µm | 일치 | 노출 fig.imc_um=3.58 |

### 2.3 IMC 성장 k 산출 후 장시간 두께 예측 — 30문항

- 식: `k = x₁/√t₁, x₂ = k·√t₂`
- 산술 일치: 30/30 · 정답 오류 0 · 비현실 E 0 · 그림/지표 노출 0 · 근접 오답 0
- 판정: 정답 키는 전 멤버가 맞고, 결과도 현실 범위(수 µm) 안입니다.
- 권고: 가족 정리(3개 이하)만 하면 됩니다.
- 멤버: BUMP-A-0003, BUMP-A-0004, BUMP-A-0005, BUMP-A-0006, BUMP-A-0007, BUMP-A-0008, BUMP-A-0009, BUMP-A-0010, BUMP-A-0011, BUMP-A-0012, BUMP-A-0013, BUMP-A-0014, BUMP-A-0015, BUMP-A-0016, BUMP-A-0017, BUMP-A-0018, BUMP-A-0019, BUMP-A-0020, BUMP-A-0021, BUMP-A-0022, BUMP-A-0023, BUMP-A-0024, BUMP-A-0025, BUMP-A-0026, BUMP-A-0027, BUMP-A-0028, BUMP-A-0029, BUMP-A-0030, BUMP-A-0031, BUMP-A-0032

### 2.4 IMC 규격 두께 도달 시간 역산 — 28문항

- 식: `t = (x_lim/k)², k = x₁/√t₁`
- 산술 일치: 28/28 · 정답 오류 0 · 비현실 E 0 · 그림/지표 노출 7 · 근접 오답 0
- 판정: 정답 키는 전 멤버가 맞습니다. 일부 멤버는 f_bump `hours` 가 정답 시간과 같아 그림이 답을 보여 줍니다.
- 권고: `hours` 를 입력 조건(측정 시간)으로 바꿉니다.
- 멤버: BUMP-A-0073, BUMP-A-0074, BUMP-A-0075, BUMP-A-0076, BUMP-A-0077, BUMP-A-0078, BUMP-A-0079, BUMP-A-0080, BUMP-A-0081, BUMP-A-0082, BUMP-A-0083, BUMP-A-0084, BUMP-A-0085, BUMP-A-0086, BUMP-A-0087, BUMP-A-0088, BUMP-A-0089, BUMP-A-0090, BUMP-A-0091, BUMP-A-0092, BUMP-A-0093, BUMP-A-0094, BUMP-A-0095, BUMP-A-0096, BUMP-A-0097, BUMP-A-0098, BUMP-A-0099, BUMP-A-0100

| id | 올바른 식·대입 | 올바른 값 | 정답 키 | 판정 | 이슈 |
|---|---|---|---|---|---|
| BUMP-A-0074 | k = 2.0/100^0.5 = 0.2000; t = (x/k)^(1/0.5) = (5/0.2000)² = 625 h | 625 h | ③ 약 625 h | 일치 | 노출 fig.hours=625 |
| BUMP-A-0078 | k = 1.8/100^0.5 = 0.1800; t = (x/k)^(1/0.5) = (5/0.1800)² = 772 h | 771.6 h | ① 약 772 h | 일치 | 노출 fig.hours=771 |
| BUMP-A-0079 | k = 2.0/100^0.5 = 0.2000; t = (x/k)^(1/0.5) = (6/0.2000)² = 900 h | 900 h | ② 약 900 h | 일치 | 노출 fig.hours=900 |
| BUMP-A-0083 | k = 2.4/225^0.5 = 0.1600; t = (x/k)^(1/0.5) = (5/0.1600)² = 977 h | 976.6 h | ③ 약 977 h | 일치 | 노출 fig.hours=976 |
| BUMP-A-0089 | k = 2.0/100^0.5 = 0.2000; t = (x/k)^(1/0.5) = (6/0.2000)² = 900 h | 900 h | ④ 약 900 h | 일치 | 노출 fig.hours=900 |
| BUMP-A-0090 | k = 2.4/196^0.5 = 0.1714; t = (x/k)^(1/0.5) = (5/0.1714)² = 851 h | 850.7 h | ① 약 851 h | 일치 | 노출 fig.hours=850 |
| BUMP-A-0094 | k = 2.0/144^0.5 = 0.1667; t = (x/k)^(1/0.5) = (5/0.1667)² = 900 h | 900 h | ② 약 900 h | 일치 | 노출 fig.hours=900 |

### 2.5 IMC k 산출과 규격 판정 — 1문항

- 식: `k = x/√t`
- 산술 일치: 1/1 · 정답 오류 0 · 비현실 E 0 · 그림/지표 노출 0 · 근접 오답 0
- 판정: 정답 키가 맞습니다(6.96 µm → 약 7.0 µm, 8 µm 규격 이내).
- 권고: —
- 멤버: BUMP-A-0001

| id | 올바른 식·대입 | 올바른 값 | 정답 키 | 판정 | 이슈 |
|---|---|---|---|---|---|
| BUMP-A-0001 | k = 2.2/√100 = 0.220; x = k√1000 = 6.96 µm | 6.96 µm | ② k = 0.22 이고 1000 h 에서 약 7.0 µm 이므로 규격을 만족한다 | 일치 | 반올림 표시 k = 0.22 이고 1000 h 에서 약 7.0 µm 이므로 규격을 만족한다 vs 계산 6.957 |

## 3. 그림·지표 정답 노출 (문항별)

| id | 노출 위치 | 권고 |
|---|---|---|
| BUMP-A-0043 | fig.j_kA=0.4 | 결과값 대신 입력 조건만 그리거나 k=0 (STANDARDS 3.6) |
| BUMP-A-0045 | fig.j_kA=45.3 | 결과값 대신 입력 조건만 그리거나 k=0 (STANDARDS 3.6) |
| BUMP-A-0046 | fig.j_kA=1.6 | 결과값 대신 입력 조건만 그리거나 k=0 (STANDARDS 3.6) |
| BUMP-A-0049 | fig.j_kA=5.7 | 결과값 대신 입력 조건만 그리거나 k=0 (STANDARDS 3.6) |
| BUMP-A-0050 | fig.j_kA=2.8 | 결과값 대신 입력 조건만 그리거나 k=0 (STANDARDS 3.6) |
| BUMP-A-0052 | fig.j_kA=3.2 | 결과값 대신 입력 조건만 그리거나 k=0 (STANDARDS 3.6) |
| BUMP-A-0054 | fig.j_kA=15.9 | 결과값 대신 입력 조건만 그리거나 k=0 (STANDARDS 3.6) |
| BUMP-A-0055 | fig.j_kA=2.4 | 결과값 대신 입력 조건만 그리거나 k=0 (STANDARDS 3.6) |
| BUMP-A-0056 | fig.j_kA=6.4 | 결과값 대신 입력 조건만 그리거나 k=0 (STANDARDS 3.6) |
| BUMP-A-0057 | fig.j_kA=16.3 | 결과값 대신 입력 조건만 그리거나 k=0 (STANDARDS 3.6) |
| BUMP-A-0058 | fig.j_kA=7.1 | 결과값 대신 입력 조건만 그리거나 k=0 (STANDARDS 3.6) |
| BUMP-A-0059 | fig.j_kA=6.1 | 결과값 대신 입력 조건만 그리거나 k=0 (STANDARDS 3.6) |
| BUMP-A-0060 | fig.j_kA=1.4 | 결과값 대신 입력 조건만 그리거나 k=0 (STANDARDS 3.6) |
| BUMP-A-0061 | fig.j_kA=11.3 | 결과값 대신 입력 조건만 그리거나 k=0 (STANDARDS 3.6) |
| BUMP-A-0062 | fig.j_kA=4.0 | 결과값 대신 입력 조건만 그리거나 k=0 (STANDARDS 3.6) |
| BUMP-A-0063 | fig.j_kA=4.2 | 결과값 대신 입력 조건만 그리거나 k=0 (STANDARDS 3.6) |
| BUMP-A-0064 | fig.j_kA=4.1 | 결과값 대신 입력 조건만 그리거나 k=0 (STANDARDS 3.6) |
| BUMP-A-0066 | fig.j_kA=25.5 | 결과값 대신 입력 조건만 그리거나 k=0 (STANDARDS 3.6) |
| BUMP-A-0067 | fig.j_kA=4.1 | 결과값 대신 입력 조건만 그리거나 k=0 (STANDARDS 3.6) |
| BUMP-A-0069 | fig.j_kA=6.4 | 결과값 대신 입력 조건만 그리거나 k=0 (STANDARDS 3.6) |
| BUMP-A-0070 | fig.j_kA=9.5 | 결과값 대신 입력 조건만 그리거나 k=0 (STANDARDS 3.6) |
| BUMP-A-0071 | fig.j_kA=0.8 | 결과값 대신 입력 조건만 그리거나 k=0 (STANDARDS 3.6) |
| BUMP-A-0072 | fig.j_kA=11.3 | 결과값 대신 입력 조건만 그리거나 k=0 (STANDARDS 3.6) |
| BUMP-A-0074 | fig.hours=625 | 결과값 대신 입력 조건만 그리거나 k=0 (STANDARDS 3.6) |
| BUMP-A-0078 | fig.hours=771 | 결과값 대신 입력 조건만 그리거나 k=0 (STANDARDS 3.6) |
| BUMP-A-0079 | fig.hours=900 | 결과값 대신 입력 조건만 그리거나 k=0 (STANDARDS 3.6) |
| BUMP-A-0083 | fig.hours=976 | 결과값 대신 입력 조건만 그리거나 k=0 (STANDARDS 3.6) |
| BUMP-A-0089 | fig.hours=900 | 결과값 대신 입력 조건만 그리거나 k=0 (STANDARDS 3.6) |
| BUMP-A-0090 | fig.hours=850 | 결과값 대신 입력 조건만 그리거나 k=0 (STANDARDS 3.6) |
| BUMP-A-0094 | fig.hours=900 | 결과값 대신 입력 조건만 그리거나 k=0 (STANDARDS 3.6) |
| BUMP-I-0039 | fig.j_kA=132 | 결과값 대신 입력 조건만 그리거나 k=0 (STANDARDS 3.6) |
| BUMP-I-0040 | fig.j_kA=84 | 결과값 대신 입력 조건만 그리거나 k=0 (STANDARDS 3.6) |
| BUMP-A-0103 | fig.j_kA=21 | 결과값 대신 입력 조건만 그리거나 k=0 (STANDARDS 3.6) |
| BUMP-A-0104 | fig.j_kA=176 | 결과값 대신 입력 조건만 그리거나 k=0 (STANDARDS 3.6) |
| BUMP-I-0044 | fig.j_kA=113 | 결과값 대신 입력 조건만 그리거나 k=0 (STANDARDS 3.6) |
| BUMP-I-0045 | fig.j_kA=78 | 결과값 대신 입력 조건만 그리거나 k=0 (STANDARDS 3.6) |
| BUMP-I-0046 | fig.j_kA=63 | 결과값 대신 입력 조건만 그리거나 k=0 (STANDARDS 3.6) |
| BUMP-I-0048 | fig.j_kA=28 | 결과값 대신 입력 조건만 그리거나 k=0 (STANDARDS 3.6) |
| BUMP-I-0049 | fig.j_kA=221 | 결과값 대신 입력 조건만 그리거나 k=0 (STANDARDS 3.6) |
| BUMP-A-0107 | fig.j_kA=141 | 결과값 대신 입력 조건만 그리거나 k=0 (STANDARDS 3.6) |
| BUMP-A-0108 | fig.j_kA=98 | 결과값 대신 입력 조건만 그리거나 k=0 (STANDARDS 3.6) |
| BUMP-I-0050 | fig.j_kA=79 | 결과값 대신 입력 조건만 그리거나 k=0 (STANDARDS 3.6) |
| BUMP-A-0110 | fig.j_kA=35 | 결과값 대신 입력 조건만 그리거나 k=0 (STANDARDS 3.6) |
| BUMP-I-0053 | fig.j_kA=265 | 결과값 대신 입력 조건만 그리거나 k=0 (STANDARDS 3.6) |
| BUMP-I-0054 | fig.j_kA=169 | 결과값 대신 입력 조건만 그리거나 k=0 (STANDARDS 3.6) |
| BUMP-I-0055 | fig.j_kA=117 | 결과값 대신 입력 조건만 그리거나 k=0 (STANDARDS 3.6) |
| BUMP-A-0111 | fig.j_kA=95 | 결과값 대신 입력 조건만 그리거나 k=0 (STANDARDS 3.6) |
| BUMP-I-0056 | fig.j_kA=61 | 결과값 대신 입력 조건만 그리거나 k=0 (STANDARDS 3.6) |
| BUMP-I-0058 | fig.j_kA=42 | 결과값 대신 입력 조건만 그리거나 k=0 (STANDARDS 3.6) |
| BUMP-A-0113 | fig.j_kA=309 | 결과값 대신 입력 조건만 그리거나 k=0 (STANDARDS 3.6) |
| BUMP-A-0114 | fig.j_kA=198 | 결과값 대신 입력 조건만 그리거나 k=0 (STANDARDS 3.6) |
| BUMP-I-0059 | fig.j_kA=137 | 결과값 대신 입력 조건만 그리거나 k=0 (STANDARDS 3.6) |
| BUMP-I-0060 | fig.j_kA=111 | 결과값 대신 입력 조건만 그리거나 k=0 (STANDARDS 3.6) |
| BUMP-I-0061 | fig.j_kA=92 | 결과값 대신 입력 조건만 그리거나 k=0 (STANDARDS 3.6) |
| BUMP-A-0115 | fig.j_kA=71 | 결과값 대신 입력 조건만 그리거나 k=0 (STANDARDS 3.6) |
| BUMP-I-0062 | fig.j_kA=49 | 결과값 대신 입력 조건만 그리거나 k=0 (STANDARDS 3.6) |
| BUMP-I-0063 | fig.j_kA=353 | 결과값 대신 입력 조건만 그리거나 k=0 (STANDARDS 3.6) |
| BUMP-I-0064 | fig.j_kA=226 | 결과값 대신 입력 조건만 그리거나 k=0 (STANDARDS 3.6) |
| BUMP-A-0117 | fig.j_kA=157 | 결과값 대신 입력 조건만 그리거나 k=0 (STANDARDS 3.6) |
| BUMP-A-0118 | fig.j_kA=127 | 결과값 대신 입력 조건만 그리거나 k=0 (STANDARDS 3.6) |
| BUMP-I-0065 | fig.j_kA=105 | 결과값 대신 입력 조건만 그리거나 k=0 (STANDARDS 3.6) |
| BUMP-I-0066 | fig.j_kA=81 | 결과값 대신 입력 조건만 그리거나 k=0 (STANDARDS 3.6) |
| BUMP-A-0119 | fig.j_kA=56 | 결과값 대신 입력 조건만 그리거나 k=0 (STANDARDS 3.6) |
| BUMP-A-0120 | fig.j_kA=442 | 결과값 대신 입력 조건만 그리거나 k=0 (STANDARDS 3.6) |
| BUMP-I-0068 | fig.j_kA=282 | 결과값 대신 입력 조건만 그리거나 k=0 (STANDARDS 3.6) |
| BUMP-I-0069 | fig.j_kA=196 | 결과값 대신 입력 조건만 그리거나 k=0 (STANDARDS 3.6) |
| BUMP-I-0070 | fig.j_kA=159 | 결과값 대신 입력 조건만 그리거나 k=0 (STANDARDS 3.6) |
| BUMP-A-0121 | fig.j_kA=131 | 결과값 대신 입력 조건만 그리거나 k=0 (STANDARDS 3.6) |
| BUMP-A-0122 | fig.j_kA=101 | 결과값 대신 입력 조건만 그리거나 k=0 (STANDARDS 3.6) |
| BUMP-I-0071 | fig.imc_um=1.58 | 결과값 대신 입력 조건만 그리거나 k=0 (STANDARDS 3.6) |
| BUMP-I-0072 | fig.imc_um=1.58 | 결과값 대신 입력 조건만 그리거나 k=0 (STANDARDS 3.6) |
| BUMP-A-0123 | fig.imc_um=1.58 | 결과값 대신 입력 조건만 그리거나 k=0 (STANDARDS 3.6) |
| BUMP-A-0124 | fig.imc_um=1.58 | 결과값 대신 입력 조건만 그리거나 k=0 (STANDARDS 3.6) |
| BUMP-I-0073 | fig.imc_um=2.24 | 결과값 대신 입력 조건만 그리거나 k=0 (STANDARDS 3.6) |
| BUMP-I-0074 | fig.imc_um=2.24 | 결과값 대신 입력 조건만 그리거나 k=0 (STANDARDS 3.6) |
| BUMP-I-0075 | fig.imc_um=2.24 | 결과값 대신 입력 조건만 그리거나 k=0 (STANDARDS 3.6) |
| BUMP-A-0125 | fig.imc_um=2.24 | 결과값 대신 입력 조건만 그리거나 k=0 (STANDARDS 3.6) |
| BUMP-A-0126 | fig.imc_um=2.74 | 결과값 대신 입력 조건만 그리거나 k=0 (STANDARDS 3.6) |
| BUMP-I-0076 | fig.imc_um=2.74 | 결과값 대신 입력 조건만 그리거나 k=0 (STANDARDS 3.6) |
| BUMP-I-0077 | fig.imc_um=2.74 | 결과값 대신 입력 조건만 그리거나 k=0 (STANDARDS 3.6) |
| BUMP-I-0078 | fig.imc_um=2.74 | 결과값 대신 입력 조건만 그리거나 k=0 (STANDARDS 3.6) |
| BUMP-A-0127 | fig.imc_um=3.16 | 결과값 대신 입력 조건만 그리거나 k=0 (STANDARDS 3.6) |
| BUMP-A-0128 | fig.imc_um=3.16 | 결과값 대신 입력 조건만 그리거나 k=0 (STANDARDS 3.6) |
| BUMP-I-0079 | fig.imc_um=3.16 | 결과값 대신 입력 조건만 그리거나 k=0 (STANDARDS 3.6) |
| BUMP-I-0080 | fig.imc_um=3.16 | 결과값 대신 입력 조건만 그리거나 k=0 (STANDARDS 3.6) |
| BUMP-I-0081 | fig.imc_um=3.87 | 결과값 대신 입력 조건만 그리거나 k=0 (STANDARDS 3.6) |
| BUMP-A-0129 | fig.imc_um=3.87 | 결과값 대신 입력 조건만 그리거나 k=0 (STANDARDS 3.6) |
| BUMP-A-0130 | fig.imc_um=3.87 | 결과값 대신 입력 조건만 그리거나 k=0 (STANDARDS 3.6) |
| BUMP-I-0082 | fig.imc_um=3.87 | 결과값 대신 입력 조건만 그리거나 k=0 (STANDARDS 3.6) |
| BUMP-I-0083 | fig.imc_um=1.9 | 결과값 대신 입력 조건만 그리거나 k=0 (STANDARDS 3.6) |
| BUMP-I-0084 | fig.imc_um=1.9 | 결과값 대신 입력 조건만 그리거나 k=0 (STANDARDS 3.6) |
| BUMP-A-0131 | fig.imc_um=1.9 | 결과값 대신 입력 조건만 그리거나 k=0 (STANDARDS 3.6) |
| BUMP-A-0132 | fig.imc_um=1.9 | 결과값 대신 입력 조건만 그리거나 k=0 (STANDARDS 3.6) |
| BUMP-I-0085 | fig.imc_um=2.68 | 결과값 대신 입력 조건만 그리거나 k=0 (STANDARDS 3.6) |
| BUMP-I-0086 | fig.imc_um=2.68 | 결과값 대신 입력 조건만 그리거나 k=0 (STANDARDS 3.6) |
| BUMP-I-0087 | fig.imc_um=2.68 | 결과값 대신 입력 조건만 그리거나 k=0 (STANDARDS 3.6) |
| BUMP-A-0133 | fig.imc_um=2.68 | 결과값 대신 입력 조건만 그리거나 k=0 (STANDARDS 3.6) |
| BUMP-A-0134 | fig.imc_um=3.29 | 결과값 대신 입력 조건만 그리거나 k=0 (STANDARDS 3.6) |
| BUMP-I-0088 | fig.imc_um=3.29 | 결과값 대신 입력 조건만 그리거나 k=0 (STANDARDS 3.6) |
| BUMP-I-0089 | fig.imc_um=3.29 | 결과값 대신 입력 조건만 그리거나 k=0 (STANDARDS 3.6) |
| BUMP-I-0090 | fig.imc_um=3.29 | 결과값 대신 입력 조건만 그리거나 k=0 (STANDARDS 3.6) |
| BUMP-A-0135 | fig.imc_um=3.79 | 결과값 대신 입력 조건만 그리거나 k=0 (STANDARDS 3.6) |
| BUMP-A-0136 | fig.imc_um=3.79 | 결과값 대신 입력 조건만 그리거나 k=0 (STANDARDS 3.6) |
| BUMP-I-0091 | fig.imc_um=3.79 | 결과값 대신 입력 조건만 그리거나 k=0 (STANDARDS 3.6) |
| BUMP-I-0092 | fig.imc_um=3.79 | 결과값 대신 입력 조건만 그리거나 k=0 (STANDARDS 3.6) |
| BUMP-I-0095 | fig.imc_um=2.53 | 결과값 대신 입력 조건만 그리거나 k=0 (STANDARDS 3.6) |
| BUMP-I-0096 | fig.imc_um=2.53 | 결과값 대신 입력 조건만 그리거나 k=0 (STANDARDS 3.6) |
| BUMP-A-0139 | fig.imc_um=2.53 | 결과값 대신 입력 조건만 그리거나 k=0 (STANDARDS 3.6) |
| BUMP-A-0140 | fig.imc_um=2.53 | 결과값 대신 입력 조건만 그리거나 k=0 (STANDARDS 3.6) |
| BUMP-I-0097 | fig.imc_um=3.58 | 결과값 대신 입력 조건만 그리거나 k=0 (STANDARDS 3.6) |
| BUMP-I-0098 | fig.imc_um=3.58 | 결과값 대신 입력 조건만 그리거나 k=0 (STANDARDS 3.6) |
| BUMP-I-0099 | fig.imc_um=3.58 | 결과값 대신 입력 조건만 그리거나 k=0 (STANDARDS 3.6) |
| BUMP-A-0141 | fig.imc_um=3.58 | 결과값 대신 입력 조건만 그리거나 k=0 (STANDARDS 3.6) |

## 5. 범위 밖 — 수치 회상형(계산 아님)

다음 문항은 보기에 수치가 있지만 계산이 아니라 사실·업체 발표 회상입니다. NUM 재계산 대상이 아니므로 FACT(`docs/reviews/_facts.md`) 판정을 따르십시오: BUMP-B-0032, BUMP-B-0080

