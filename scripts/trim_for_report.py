#!/usr/bin/env python3
"""수집 결과 JSON을 리포트가 실제로 쓰는 만큼만 남겨 줄인다.

수집기 원본은 close 기준 3.2MB다(2026-09-04 실측). 리포트 세션이 그대로 열면
컨텍스트가 날아가고, 저장소에 매일 올리면 이력이 감당이 안 된다. 리포트가
읽는 것은 지수 스칼라·집계·관심종목 몇 행뿐이므로 그 형태로 접는다.

  python3 trim_for_report.py 원본.json 축소.json
"""

from __future__ import annotations

import json
import sys

# 일봉 600행 중 리포트가 보는 것은 앞부분뿐이다(전일 대비·5일·20일 추세).
CANDLE_ROWS = 25
# 순위표는 상위 20위까지만 쓴다.
RANK_ROWS = 20
# 종목 단위 수급 원자료는 집계와 관심종목만 남기고 버린다.
FLOW_FIELDS = [
    "ind_invsr", "frgnr_invsr", "orgn", "fnnc_invt", "insrnc", "invtrt",
    "etc_fnnc", "bank", "penfnd_etc", "samo_fund", "natn", "etc_corp",
]


def _num(v):
    try:
        return float(str(v).replace(",", ""))
    except (TypeError, ValueError):
        return 0.0


def _lists(block):
    return [k for k, v in block.items() if isinstance(v, list)]


def trim(payload: dict) -> dict:
    out = {k: v for k, v in payload.items() if k != "results"}
    results = payload.get("results") or {}
    trimmed: dict = {}

    for name, entry in results.items():
        if "error" in entry:
            trimmed[name] = entry
            continue
        data = entry.get("data")
        if not isinstance(data, dict):
            trimmed[name] = entry
            continue

        if name == "investor_after_close":
            rows = data.get("opaf_invsr_trde") or []
            totals = {f: sum(_num(r.get(f)) for r in rows) for f in FLOW_FIELDS}
            watch = [r for r in rows if _num(r.get("trde_qty")) > 0][:60]
            trimmed[name] = {
                "source": "aggregated",
                "row_count": len(rows),
                "totals_million_won": {k: round(v) for k, v in totals.items()},
                "top_rows": watch,
            }
            continue

        if name.startswith("investor_intraday_"):
            rows = next((data[k] for k in _lists(data) if data[k]), [])
            trimmed[name] = {
                "source": "aggregated",
                "row_count": len(rows),
                "net_buy_million_won": round(sum(_num(r.get("netprps_amt")) for r in rows)),
                "top_rows": rows[:RANK_ROWS],
            }
            continue

        kept = {k: v for k, v in data.items() if not isinstance(v, list)}
        limit = CANDLE_ROWS if name.startswith(("candle_", "short_selling_")) else RANK_ROWS
        for key in _lists(data):
            kept[key] = data[key][:limit]
            if len(data[key]) > limit:
                kept[f"_{key}_truncated_from"] = len(data[key])
        trimmed[name] = {**{k: v for k, v in entry.items() if k != "data"}, "data": kept}

    out["results"] = trimmed
    out["_trimmed"] = True
    return out


def main() -> int:
    if len(sys.argv) != 3:
        print(__doc__, file=sys.stderr)
        return 2
    src, dst = sys.argv[1], sys.argv[2]
    with open(src, encoding="utf-8") as handle:
        payload = json.load(handle)
    result = trim(payload)
    text = json.dumps(result, ensure_ascii=False, separators=(",", ":"))
    with open(dst, "w", encoding="utf-8") as handle:
        handle.write(text)
    before = len(json.dumps(payload, ensure_ascii=False).encode())
    after = len(text.encode())
    print(f"{before/1024/1024:.2f}MB -> {after/1024:.0f}KB ({after/before*100:.1f}%)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
