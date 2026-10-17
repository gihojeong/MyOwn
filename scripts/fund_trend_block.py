#!/usr/bin/env python3
"""증시자금(투자자예탁금·신용융자잔고) 추이 블록을 리포트 HTML 조각으로 만든다.

    python3 scripts/fund_trend_block.py                 # 실시간으로 받아서 출력
    python3 scripts/fund_trend_block.py kiwoom.json     # 수집 결과의 fund_trend 를 쓴다
    python3 scripts/fund_trend_block.py kiwoom.json -o block.html

★이 블록은 서술 전용이다.★ 2026-10-17 측정(200거래일): 공시 지연 2거래일 +
계열 자체의 내재 지연 2~3거래일(Δ신용 s=3 corr +0.5149 / Δ예탁금 s=2 corr +0.6119)
= 합계 4~5거래일. 시차 회귀 12건 중 유의 1건이고 그 1건도 지연을 바꾸면 부호가 뒤집힌다.
따라서 E 의 성분으로 쓰지 말고 레버리지 수준과 대기 자금의 방향만 적는다.
"""
from __future__ import annotations

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

ROWS = (
    ("dep", "투자자예탁금", "증시에 들어와 대기 중인 현금"),
    ("cred", "신용융자잔고", "빚으로 산 주식의 잔액"),
    ("fund_stock", "주식형 수익증권", "주식형 펀드 설정잔액"),
)
BLUE, RED = "#2a78d6", "#d03b3b"


def _fmt(v: float, unit: str = "조", digits: int = 2) -> str:
    return f"{v:+,.{digits}f}{unit}"


def _color(v: float) -> str:
    return RED if v > 0 else (BLUE if v < 0 else "#555555")


def build(data: dict) -> str:
    lab = data["labels"]
    out = [
        '<table border="0" cellpadding="0" cellspacing="0" width="880"><tr>'
        '<td style="padding:8px 13px;background-color:#2f4a2f;font-size:14px;'
        'font-weight:bold;color:#ffffff;">증시자금 추이 — 예탁금·신용융자. '
        '★선행 변수가 아니다. 추이만 적는다★</td></tr></table><br>',
        '<table border="0" cellpadding="0" cellspacing="0" width="880" '
        'style="border-collapse:collapse;"><tr>',
    ]
    for head, align in (("항목", "left"), ("수준(조원)", "right"), ("1일", "right"),
                        ("5일", "right"), ("20일", "right"), ("읽는 법", "left")):
        out.append(
            f'<td align="{align}" style="padding:5px;border:1px solid #c9d2bb;'
            f'font-size:12px;font-weight:bold;background:#e4e9dc;">{head}</td>'
        )
    out.append("</tr>")

    for i, (key, name, note) in enumerate(ROWS):
        if key not in data["levels_jo"]:
            continue
        bg = "#fff" if i % 2 == 0 else "#fafbf6"
        cell = (f'style="padding:5px;border:1px solid #c9d2bb;font-size:12px;background:{bg};"')
        out.append(f"<tr><td {cell}><b>{lab.get(key, name)}</b></td>")
        out.append(f'<td align="right" {cell}>{data["levels_jo"][key]:,.2f}</td>')
        for n in ("1d", "5d", "20d"):
            d = data["delta"][key].get(n)
            if not d:
                out.append(f'<td align="right" {cell}>—</td>')
                continue
            jo, pct = d["abs_jo"], d["pct"]
            out.append(
                f'<td align="right" {cell}><font color="{_color(jo)}">{_fmt(jo)}</font>'
                f'<br><font color="{_color(jo)}" style="font-size:11px;">'
                f'{pct:+.2f}%</font></td>'
            )
        out.append(f"<td {cell}>{note}</td></tr>")
    out.append("</table><br>")

    dep1 = data["delta"]["dep"]["20d"]
    cred1 = data["delta"]["cred"]["20d"]
    diverge = ""
    if dep1 and cred1 and dep1["abs_jo"] * cred1["abs_jo"] < 0:
        direction = ("대기 자금은 빠지는데 레버리지는 늘었다"
                     if dep1["abs_jo"] < 0 else
                     "대기 자금은 늘었는데 레버리지는 줄었다")
        diverge = (
            f'<br><b>★20일 기준 두 계열이 반대로 갔다 — {direction}'
            f'(예탁금 {_fmt(dep1["abs_jo"])} vs 신용융자 {_fmt(cred1["abs_jo"])}).★</b>'
            "<br>레버리지 비중이 올라간 국면은 급락일에 반대매매가 붙기 쉽다."
        )

    out.append(
        '<table border="0" cellpadding="9" cellspacing="0" width="880"><tr>'
        '<td style="background-color:#16301f;font-family:Consolas,monospace;font-size:12px;'
        'line-height:1.7;color:#eaffea;">'
        '<font color="#9fe6a0" style="font-weight:bold;">'
        f'기준일 {data["as_of"]} · 단위 억원 원자료 · 신용융자÷예탁금 '
        f'{data.get("cred_over_dep_pct", float("nan")):.2f}%</font><br>'
        f'★이 값은 오늘 자료가 아니다★ — 공시 지연 2거래일 + 계열 내재 지연 2~3거래일로<br>'
        f'&nbsp;&nbsp;★4~5거래일 전★ 의 시장을 설명한다. 그래서 지수 전망 E 의 성분으로 쓰지 않는다.<br>'
        f'&nbsp;&nbsp;(측정 근거: Δ신용융자는 s=3 에서 동시상관 +0.5149, Δ예탁금은 s=2 에서 +0.6119 최대.<br>'
        f'&nbsp;&nbsp;&nbsp;시차 회귀 12건 중 |t|&gt;1.96 이 1건이고 지연을 바꾸면 부호가 뒤집힌다 — 제안 P45)'
        f'{diverge}'
        "</td></tr></table><br>"
    )
    return "".join(out)


def main() -> None:
    args = [a for a in sys.argv[1:] if a != "-o"]
    dest = None
    if "-o" in sys.argv:
        dest = sys.argv[sys.argv.index("-o") + 1]
        args = [a for a in args if a != dest]

    if args:
        blob = json.load(open(args[0], encoding="utf-8"))
        node = blob.get("results", blob).get("fund_trend", {})
        if "error" in node:
            sys.exit(f"수집 결과에 fund_trend 오류가 있다: {node['error']}")
        data = node["data"]
    else:
        import kiwoom_collect as kc
        data = kc.fetch_fund_trend(40)

    html = build(data)
    if dest:
        open(dest, "w", encoding="utf-8").write(html)
        print(f"{dest} 저장 — {len(html):,} bytes (기준일 {data['as_of']})", file=sys.stderr)
    else:
        sys.stdout.write(html)


if __name__ == "__main__":
    main()
