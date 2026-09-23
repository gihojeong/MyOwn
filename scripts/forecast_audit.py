#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
KOSPI 예측 정확도 누적 감사 — 일간·주간·월간 3시계.

왜 있나
  매 회차 채점을 20KB 리포트 안에만 적어 온 탓에 누적 집계를 한 회차가 한 번도 없었다.
  주간 리뷰는 "계통 편향을 진단하라"는 지시를 받고 있었으나 한 주 안의 5개 점만 보고
  매번 새로 시작했다. 그래서 2026-09-16~23의 6거래일 연속 편향을 아무도 잡지 못했다.
  이 스크립트가 그 누적 집계를 대신한다.

쓰는 법 (예약작업 세션에는 저장소가 붙지 않으므로 URL로 받아 쓴다)
  curl -fsSL -o fa.py https://raw.githubusercontent.com/gihojeong/MyOwn/master/scripts/forecast_audit.py
  # Drive 의 kospi_forecast_accuracy_log [표 A] 행을 그대로 파일로 저장한 뒤
  python3 fa.py rows.txt            # 전체(일간+주간+월간)
  python3 fa.py rows.txt --window weekly     # 주간 리뷰용
  python3 fa.py rows.txt --window monthly    # 월간 점검용
  인자를 생략하면 아래 ROWS(최종 갱신분)를 쓴다.

입력 형식 (파이프 구분. [표 A]와 같은 순서. 모르는 값은 - )
  YYYY-MM-DD | 예측% | 실제% | sigma% | 상방P | 기본P | 하방P | 착지 | 갭예측% | 갭실제%

원칙
  표본이 작을 때 모형을 뜯어고치는 것이 지금까지의 실패 방식이었다.
  t값이 유의 수준을 넘기 전에는 관측만 계속한다. 스크립트가 그렇게 판정한다.
"""
import sys
import math
import datetime

# (날짜, 아침 확률가중 예측%, 실제 등락률%, sigma%, 상방P, 기본P, 하방P, 착지, 갭예측%, 갭실제%)
ROWS = [
    ("2026-09-16",  0.209242,  1.368741, 2.168185, None, None, None, "상방",  0.400000, -0.241729),
    ("2026-09-17", -0.634098, -0.038107, 2.385004, 0.32, 0.43, 0.25, "기본", -0.625047,  0.908757),
    ("2026-09-18",  1.145940,  2.662831, 2.143474, 0.34, 0.42, 0.24, "상방",  1.206392,  2.535809),
    ("2026-09-21",  0.612102,  1.646159, 2.164021, 0.30, 0.44, 0.26, "상방",  0.592104,  0.639810),
    ("2026-09-22",  0.856577,  0.145411, 1.857411, 0.40, 0.38, 0.22, "기본",  1.439060,  2.196007),
    ("2026-09-23",  0.351776,  0.897846, 1.931953, 0.42, 0.36, 0.22, "상방",  0.491297,  1.939039),
]

# 자유도별 양측 95% t 임계값. 표본이 작아 정규근사를 쓰지 않는다.
T95 = {1: 12.706, 2: 4.303, 3: 3.182, 4: 2.776, 5: 2.571, 6: 2.447, 7: 2.365,
       8: 2.306, 9: 2.262, 10: 2.228, 11: 2.201, 12: 2.179, 13: 2.160, 14: 2.145,
       15: 2.131, 16: 2.120, 17: 2.110, 18: 2.101, 19: 2.093, 20: 2.086,
       21: 2.080, 22: 2.074, 23: 2.069, 24: 2.064, 25: 2.060, 29: 2.045, 39: 2.023}


def t_crit(df):
    if df in T95:
        return T95[df]
    for k in sorted(T95):
        if df < k:
            return T95[k]
    return 1.96


def mean(v):
    return sum(v) / len(v) if v else float("nan")


def std(v, ddof=1):
    if len(v) - ddof < 1:
        return float("nan")
    m = mean(v)
    return math.sqrt(sum((x - m) ** 2 for x in v) / (len(v) - ddof))


def binom_tail(n, k):
    return sum(math.comb(n, i) for i in range(k, n + 1)) / 2 ** n


def parse(path):
    out = []
    for raw in open(path, encoding="utf-8"):
        line = raw.strip()
        if not line or line.startswith("#") or line.startswith("날짜"):
            continue
        f = [c.strip() for c in line.split("|")]
        if len(f) < 10:
            continue
        num = lambda x: None if x in ("-", "") else float(x.replace("%", "").replace("+", ""))
        out.append((f[0], num(f[1]), num(f[2]), num(f[3]), num(f[4]), num(f[5]),
                    num(f[6]), f[7], num(f[8]), num(f[9])))
    return out


def stats(rows, label):
    """한 구간의 통계. 출력하고 판정에 필요한 값을 돌려준다."""
    n = len(rows)
    if n == 0:
        return None
    err = [a - p for _, p, a, *_ in rows]
    pred = [p for _, p, *_ in rows]
    act = [a for _, p, a, *_ in rows]
    sig = [s for _, p, a, s, *_ in rows]
    gerr = [ga - gp for *_, gp, ga in rows if gp is not None and ga is not None]

    m_e = mean(err)
    s_e = std(err)
    se = s_e / math.sqrt(n) if n > 1 else float("nan")
    t = m_e / se if se and not math.isnan(se) and se != 0 else float("nan")
    df = n - 1
    tc = t_crit(df) if df >= 1 else float("nan")
    pos = sum(1 for e in err if e > 0)
    realized = std(act)
    hits = sum(1 for a, s in zip(act, sig) if abs(a) <= 1.2815516 * s)
    up_real = sum(1 for r in rows if r[7] == "상방") / n
    dn_real = sum(1 for r in rows if r[7] == "하방") / n
    have = [r for r in rows if r[4] is not None]
    up_p = mean([r[4] for r in have]) if have else float("nan")
    dn_p = mean([r[6] for r in have]) if have else float("nan")

    print(f"  n={n:<3} 오차평균 {m_e:+7.4f}%p  부호 +{pos}/{n}", end="")
    if n > 1:
        sig_mark = "★유의" if abs(t) > tc else "미달"
        print(f"  t={t:+6.3f}(임계 {tc:.3f}, {sig_mark})", end="")
    print()
    if n > 1 and not math.isnan(realized) and realized > 0:
        print(f"      sigma {mean(sig):.3f}% / 실현 {realized:.3f}% = {mean(sig)/realized:.2f}배"
              f"   80%구간 적중 {hits}/{n}({hits/n:.0%})")
        print(f"      예측분산/실제분산 {std(pred)/realized:.3f}", end="")
    if have:
        print(f"   확률 상방 {up_p:.0%}→실제 {up_real:.0%} / 하방 {dn_p:.0%}→실제 {dn_real:.0%}", end="")
    print()
    if gerr:
        gp = sum(1 for e in gerr if e > 0)
        print(f"      갭오차 평균 {mean(gerr):+.4f}%p (부호 +{gp}/{len(gerr)})")
    return dict(n=n, m_e=m_e, t=t, tc=tc, pos=pos, hits=hits,
                ratio=(mean(sig) / realized) if realized else float("nan"),
                up_p=up_p, up_real=up_real, act=act)


def iso_week(d):
    y, w, _ = datetime.date.fromisoformat(d).isocalendar()
    return f"{y}-W{w:02d}"


def month(d):
    return d[:7]


def main():
    argv = sys.argv[1:]
    win = "all"
    args = []
    i = 0
    while i < len(argv):
        a = argv[i]
        if a == "--window":                      # --window weekly
            if i + 1 < len(argv):
                win = argv[i + 1]
                i += 2
                continue
            i += 1
            continue
        if a.startswith("--window="):             # --window=weekly
            win = a.split("=", 1)[1]
            i += 1
            continue
        if a.startswith("--"):                    # 알 수 없는 플래그는 무시
            i += 1
            continue
        args.append(a)
        i += 1
    if win not in ("all", "daily", "weekly", "monthly"):
        print(f"--window 값이 잘못됐다: {win!r}. all|daily|weekly|monthly 중 하나여야 한다.")
        return
    rows = parse(args[0]) if args else ROWS
    rows = sorted(rows, key=lambda r: r[0])
    if not rows:
        print("행이 없다. 입력을 확인하라.")
        return

    print("=" * 78)
    print(f"KOSPI 예측 정확도 감사   구간 {rows[0][0]} ~ {rows[-1][0]}   총 {len(rows)}행")
    print("=" * 78)

    if win in ("all", "daily"):
        print("\n[일간] 전체 누적")
        overall = stats(rows, "전체")
        print("\n[일간] 최근 5거래일")
        stats(rows[-5:], "최근5")
    else:
        overall = stats(rows, "전체")

    weeks = {}
    for r in rows:
        weeks.setdefault(iso_week(r[0]), []).append(r)
    if win in ("all", "weekly"):
        print("\n[주간] 주 단위 롤업  ← 토요일 주간 리뷰가 보는 것")
        for wk in sorted(weeks):
            print(f"  {wk}", end="")
            stats(weeks[wk], wk)
        if len(weeks) >= 2:
            ks = sorted(weeks)
            a = mean([x[2] - x[1] for x in weeks[ks[-2]]])
            b = mean([x[2] - x[1] for x in weeks[ks[-1]]])
            print(f"\n  주간 추세: {ks[-2]} {a:+.4f}%p → {ks[-1]} {b:+.4f}%p "
                  f"({'개선' if abs(b) < abs(a) else '악화'}, 절대값 {abs(b)-abs(a):+.4f}%p)")
        else:
            print("\n  ★주가 1개뿐이다. 주간 추세는 다음 주부터 판정 가능하다.")

    months = {}
    for r in rows:
        months.setdefault(month(r[0]), []).append(r)
    if win in ("all", "monthly"):
        print("\n[월간] 월 단위 롤업  ← 매월 첫 주간 리뷰가 보는 것")
        for mo in sorted(months):
            print(f"  {mo}", end="")
            stats(months[mo], mo)
        if len(months) < 2:
            print("\n  ★월이 1개뿐이다. 월간 비교는 다음 달부터 판정 가능하다.")

    print()
    print("=" * 78)
    print("[판정] 이 지시 이상으로 손대지 마라")
    print("=" * 78)
    o = overall
    n, t, tc = o["n"], o["t"], o["tc"]
    if n > 1 and abs(t) > tc:
        print(f"  ★오차 편향이 통계적으로 확정됐다 (|t|={abs(t):.3f} > {tc:.3f}).")
        print("   확률 배분 규칙(R3)을 재설계하라. 단 반드시 국면을 나눠 재추정한 뒤에 하라.")
    else:
        print(f"  오차 편향은 아직 유의하지 않다 (|t|={abs(t):.3f} <= {tc:.3f}).")
        print("   ★관측만 계속하라. 표본이 작을 때 모형을 고치는 것이 지금까지의 실패 방식이다.")

    hr = o["hits"] / n
    if hr >= 0.95 and n >= 4:
        print(f"  ★80% 구간 적중률 {hr:.0%}. 구간이 넓어 무의미하다. sigma를 10% 줄여라(R2).")
    elif hr <= 0.5 and n >= 4:
        print(f"  ★80% 구간 적중률 {hr:.0%}. sigma를 10% 늘려라(R2).")
    else:
        print(f"  80% 구간 적중률 {hr:.0%}. 허용 범위. sigma 유지.")

    up = [a for a in o["act"] if a > 0]
    dn = [a for a in o["act"] if a <= 0]
    if not up or not dn:
        miss = "하락" if not dn else "상승"
        print(f"  ★경고: '{miss} 국면' 표본이 0이다. 지금 편향은 한쪽 국면에서만 측정된 것이다.")
        print("   국면이 바뀌면 정확히 반대로 틀린다. 기계적 보정을 금지한다.")
    else:
        print(f"  국면 표본: 상승 {len(up)} / 하락 {len(dn)}. 국면별 편향을 나눠 보라.")

    print(f"  누적 {n}행 / 주 {len(weeks)}개 / 월 {len(months)}개.", end="")
    if n < 20:
        print(f" 20행 도달 시 국면별 재추정.")
    else:
        print(f" 국면별 재추정 가능 구간이다.")


if __name__ == "__main__":
    main()
