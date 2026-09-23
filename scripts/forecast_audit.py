#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
아침 예측 채점 누적 감사 — KOSPI 리포트 예약작업용.

왜 있나
  매 회차 채점을 20KB 리포트 안에만 적어 온 탓에 누적 집계를 한 회차가 한 번도 없었고,
  6거래일 연속 같은 방향 편향을 놓쳤다. 이 스크립트가 그 집계를 대신한다.

쓰는 법
  1. 저녁 회차에서 채점을 마치면 아래 ROWS 맨 끝에 한 줄을 추가한다.
  2. `python3 scripts/forecast_audit.py` 를 실행한다.
  3. 출력된 [표 B] 통계를 Drive 의 `kospi_forecast_accuracy_log` 에 옮겨 적는다.
  4. 출력 맨 아래 [판정]이 지시하는 대로만 조치한다. 그 이상 손대지 마라.

원칙
  표본이 작을 때 모형을 뜯어고치는 것이 지금까지의 실패 방식이었다.
  t값이 유의 수준을 넘기 전에는 관측만 계속한다.
"""
import math

# (날짜, 아침 확률가중 예측%, 실제 등락률%, 그날 sigma%,
#  상방P, 기본P, 하방P, 실제가 가장 가까웠던 시나리오, 갭예측%, 갭실제%)
# 확률을 모르면 None. 실제착지는 "상방"/"기본"/"하방".
ROWS = [
    ("2026-09-16",  0.209242,  1.368741, 2.168185, None, None, None, "상방",  0.400000, -0.241729),
    ("2026-09-17", -0.634098, -0.038107, 2.385004, 0.32, 0.43, 0.25, "기본", -0.625047,  0.908757),
    ("2026-09-18",  1.145940,  2.662831, 2.143474, 0.34, 0.42, 0.24, "상방",  1.206392,  2.535809),
    ("2026-09-21",  0.612102,  1.646159, 2.164021, 0.30, 0.44, 0.26, "상방",  0.592104,  0.639810),
    ("2026-09-22",  0.856577,  0.145411, 1.857411, 0.40, 0.38, 0.22, "기본",  1.439060,  2.196007),
    ("2026-09-23",  0.351776,  0.897846, 1.931953, 0.42, 0.36, 0.22, "상방",  0.491297,  1.939039),
]

# 자유도별 양측 95% t 임계값 (n-1). 표본이 작아 정규근사를 쓰지 않는다.
T95 = {1: 12.706, 2: 4.303, 3: 3.182, 4: 2.776, 5: 2.571, 6: 2.447, 7: 2.365,
       8: 2.306, 9: 2.262, 10: 2.228, 11: 2.201, 12: 2.179, 13: 2.160, 14: 2.145,
       15: 2.131, 16: 2.120, 17: 2.110, 18: 2.101, 19: 2.093, 20: 2.086}


def mean(v):
    return sum(v) / len(v)


def std(v, ddof=1):
    if len(v) - ddof < 1:
        return float("nan")
    m = mean(v)
    return math.sqrt(sum((x - m) ** 2 for x in v) / (len(v) - ddof))


def binom_tail(n, k):
    """n회 중 k회 이상 한쪽으로 쏠릴 확률(양측 아님, 단측)."""
    return sum(math.comb(n, i) for i in range(k, n + 1)) / 2 ** n


def t_crit(df):
    return T95.get(df, 1.96)


def main():
    n = len(ROWS)
    err = [a - p for _, p, a, *_ in ROWS]
    pred = [p for _, p, *_ in ROWS]
    act = [a for _, p, a, *_ in ROWS]
    sig = [s for _, p, a, s, *_ in ROWS]
    gap_err = [ga - gp for *_, gp, ga in ROWS]

    print("=" * 76)
    print(f"[표 A] 아침 예측 채점 원장  (n={n})   오차 = 실제 - 예측")
    print("=" * 76)
    print(f'{"날짜":<12}{"예측%":>9}{"실제%":>9}{"오차%p":>9}{"착지":>6}{"갭오차%p":>10}')
    for (d, p, a, s, up, bs, dn, land, gp, ga), e, ge in zip(ROWS, err, gap_err):
        print(f"{d:<12}{p:+9.3f}{a:+9.3f}{e:+9.3f}{land:>6}{ge:+10.3f}")

    print()
    print("=" * 76)
    print("[표 B] 요약 통계")
    print("=" * 76)

    m_e, s_e = mean(err), std(err)
    se = s_e / math.sqrt(n)
    t = m_e / se if se else float("nan")
    df = n - 1
    tc = t_crit(df)
    pos = sum(1 for e in err if e > 0)
    print(f"  종가 오차 평균   {m_e:+.4f} %p   표준편차 {s_e:.4f}   표준오차 {se:.4f}")
    print(f"  t = {t:.3f}  (자유도 {df}, 95% 임계 {tc:.3f})"
          f"  -> {'★편향 확정' if abs(t) > tc else '유의 미달 — 확정 아님'}")
    print(f"  부호 양 {pos}/{n}  (한쪽 쏠림 확률 {binom_tail(n, max(pos, n - pos)):.3f})")

    if n >= 3:
        m = m_e
        num = sum((err[i] - m) * (err[i + 1] - m) for i in range(n - 1))
        den = sum((e - m) ** 2 for e in err)
        r1 = num / den if den else float("nan")
        print(f"  lag-1 자기상관 {r1:+.4f}  -> "
              f"{'진동(과잉교정)' if r1 < -0.4 else '진동 아님. 한 방향 편향'}")

    ratio_var = std(pred) / std(act) if std(act) else float("nan")
    print(f"  예측 표준편차 {std(pred):.4f} / 실제 {std(act):.4f} = {ratio_var:.3f}"
          f"  -> 예측이 실제의 {ratio_var*100:.0f}% 크기로만 흔들린다")

    realized = std(act)
    hits = sum(1 for a, s in zip(act, sig) if abs(a) <= 1.2815516 * s)
    print(f"  sigma 사용평균 {mean(sig):.4f}% / 실현 {realized:.4f}% = "
          f"{mean(sig)/realized:.2f}배")
    print(f"  80% 구간 적중 {hits}/{n} ({hits/n:.0%})  기대 80%")

    have = [r for r in ROWS if r[4] is not None]
    if have:
        up_p = mean([r[4] for r in have])
        dn_p = mean([r[6] for r in have])
        r_up = sum(1 for r in ROWS if r[7] == "상방") / n
        r_dn = sum(1 for r in ROWS if r[7] == "하방") / n
        print(f"  확률 부여 상방 {up_p:.0%} / 하방 {dn_p:.0%}"
              f"   실제 착지 상방 {r_up:.0%} / 하방 {r_dn:.0%}")

    m_g = mean(gap_err)
    pos_g = sum(1 for e in gap_err if e > 0)
    print(f"  갭 오차 평균 {m_g:+.4f} %p  (양 {pos_g}/{n})")

    print()
    print("=" * 76)
    print("[판정] 이 지시 이상으로 손대지 마라")
    print("=" * 76)
    if abs(t) > tc:
        print(f"  ★오차 편향이 통계적으로 확정됐다(|t|={abs(t):.3f} > {tc:.3f}).")
        print("   확률 배분 규칙(R3)을 재설계하라. 단 국면을 나눠 재추정한 뒤에 하라.")
    else:
        print(f"  오차 편향은 아직 유의하지 않다(|t|={abs(t):.3f} <= {tc:.3f}).")
        print("   ★관측만 계속하라. 표본이 작을 때 모형을 고치는 것이 지금까지의 실패 방식이다.")

    if hits / n >= 0.95 and n >= 4:
        print("  ★80% 구간 적중률이 95% 이상이다. sigma를 10% 줄여라(R2).")
    elif hits / n <= 0.5 and n >= 4:
        print("  ★80% 구간 적중률이 50% 이하다. sigma를 10% 늘려라(R2).")
    else:
        print("  80% 구간 적중률은 허용 범위다. sigma 유지.")

    regimes = {"상승": [a for a in act if a > 0], "하락": [a for a in act if a <= 0]}
    if min(len(v) for v in regimes.values()) == 0:
        miss = [k for k, v in regimes.items() if not v][0]
        print(f"  ★경고: '{miss} 국면' 표본이 0이다. 지금 편향은 한쪽 국면에서만 측정된 것이다.")
        print("   국면이 바뀌면 정확히 반대로 틀릴 수 있다. 기계적 보정을 금지한다.")
    if n < 20:
        print(f"  표본 {n}/20. 20 도달 시 국면을 나눠 편향을 다시 추정하라.")


if __name__ == "__main__":
    main()
