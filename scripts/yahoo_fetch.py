#!/usr/bin/env python3
"""야후 차트 API 일괄 수집 — 키움 자격증명 무효 시의 대체 경로.
2026-10-06 am 회차가 검증한 경로(77심볼 2.0초). 국내 KS/KQ 정규장 종가가 KRX 확정치와 일치.
"""
import json, sys, urllib.request, concurrent.futures as cf

BASE = "https://query1.finance.yahoo.com/v8/finance/chart/{}?range=1mo&interval=1d"
UA = {"User-Agent": "Mozilla/5.0"}

SYMS = {
    # 지수
    "^KS11": "KOSPI", "^KQ11": "KOSDAQ",
    # 시총 상위 31 (KOSPI)
    "005930.KS": "삼성전자", "005935.KS": "삼성전자우", "000660.KS": "SK하이닉스",
    "402340.KS": "SK스퀘어", "009150.KS": "삼성전기", "373220.KS": "LG에너지솔루션",
    "005380.KS": "현대차", "207940.KS": "삼성바이오로직스", "105560.KS": "KB금융",
    "032830.KS": "삼성생명", "028260.KS": "삼성물산", "012450.KS": "한화에어로스페이스",
    "034020.KS": "두산에너빌리티", "055550.KS": "신한지주", "329180.KS": "HD현대중공업",
    "000270.KS": "기아", "068270.KS": "셀트리온", "034730.KS": "SK",
    "006400.KS": "삼성SDI", "066570.KS": "LG전자", "086790.KS": "하나금융지주",
    "012330.KS": "현대모비스", "010120.KS": "LS ELECTRIC", "000810.KS": "삼성화재",
    "035420.KS": "NAVER", "298040.KS": "효성중공업", "042700.KS": "한미반도체",
    "000150.KS": "두산", "316140.KS": "우리금융지주", "005490.KS": "POSCO홀딩스",
    "267260.KS": "HD현대일렉트릭",
    # 섹터 지도 보강
    "009540.KS": "HD한국조선해양", "042660.KS": "한화오션", "079550.KS": "LIG넥스원",
    "064350.KS": "현대로템", "090430.KS": "아모레퍼시픽", "161890.KS": "한국콜마",
    "035720.KS": "카카오", "352820.KS": "하이브", "096770.KS": "SK이노베이션",
    "010950.KS": "S-Oil", "051910.KS": "LG화학", "018260.KS": "삼성에스디에스",
    "247540.KQ": "에코프로비엠", "196170.KQ": "알테오젠", "058470.KQ": "리노공업",
    "240810.KQ": "원익IPS", "041510.KQ": "에스엠", "000990.KS": "DB하이텍",
    # ETF·환율·미 선물
    "156080.KS": "KODEX MSCI Korea", "KRW=X": "USDKRW",
    "ES=F": "S&P500선물", "NQ=F": "나스닥100선물", "CL=F": "WTI선물",
}


def one(sym):
    try:
        req = urllib.request.Request(BASE.format(urllib.parse.quote(sym)), headers=UA)
        with urllib.request.urlopen(req, timeout=20) as r:
            j = json.load(r)
        res = j["chart"]["result"][0]
        ts = res["timestamp"]
        q = res["indicators"]["quote"][0]
        meta = res["meta"]
        rows = []
        for i, t in enumerate(ts):
            c = q["close"][i]
            if c is None:
                continue
            rows.append({
                "t": t, "o": q["open"][i], "h": q["high"][i],
                "l": q["low"][i], "c": c, "v": q["volume"][i],
            })
        return sym, {"rows": rows, "prevClose": meta.get("chartPreviousClose"),
                     "regularMarketPrice": meta.get("regularMarketPrice"),
                     "tz": meta.get("exchangeTimezoneName")}
    except Exception as e:
        return sym, {"error": "%s: %s" % (type(e).__name__, e)}


def main():
    out = {}
    with cf.ThreadPoolExecutor(max_workers=16) as ex:
        for sym, data in ex.map(one, list(SYMS)):
            out[sym] = data
            out[sym]["name"] = SYMS[sym]
    json.dump(out, open("/tmp/yf.json", "w"), ensure_ascii=False)
    ok = [s for s, v in out.items() if "error" not in v]
    bad = [s for s, v in out.items() if "error" in v]
    print("OK %d / %d" % (len(ok), len(SYMS)))
    if bad:
        print("FAILED:", bad)
        for s in bad[:5]:
            print("  ", s, out[s]["error"])
    # 최근 2영업일 요약
    print("\n%-22s %12s %12s %9s" % ("name", "last", "prev", "chg%"))
    for s in SYMS:
        v = out[s]
        if "error" in v or len(v["rows"]) < 2:
            continue
        last, prev = v["rows"][-1], v["rows"][-2]
        chg = (last["c"] / prev["c"] - 1) * 100
        print("%-22s %12.2f %12.2f %+9.3f" % (v["name"][:22], last["c"], prev["c"], chg))


if __name__ == "__main__":
    import urllib.parse
    main()
