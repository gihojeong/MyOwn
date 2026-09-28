#!/usr/bin/env python3
"""수집 경로 4곳(키움·KRX·ECOS·환경변수)을 한 번에 점검하는 세팅 진단기.

`kiwoom_collect.py --check`는 키움 토큰 발급까지만 본다. 그래서 키움은 되는데
KRX 서비스 하나가 미신청이거나 ECOS 키가 없는 상태를 잡아내지 못하고, 그 사실이
회차 중에 실패로 처음 드러난다. 이 스크립트는 그것을 **회차 전에** 가른다.

    python3 scripts/setup_check.py            # 사람이 읽는 표
    python3 scripts/setup_check.py --json     # 기계가 읽는 JSON
    python3 scripts/setup_check.py --date 20260922

네 가지를 본다.

  1) 환경변수 — 존재·길이·비가시 문자. **값은 절대 출력하지 않는다.**
  2) 키움 REST — demo·real 양쪽에 토큰을 발급해 보고 키의 투자구분을 판정한다.
     return_code 8030("투자구분이 달라서 Appkey를 사용할수가 없습니다")이 판정 근거다.
     발급된 쪽에서는 지수 조회(ka20001) 1건까지 실제로 쏴 본다.
  3) KRX OpenAPI — **서비스별로 이용신청이 따로**다. 401은 미신청, 200+0행은 미게시다
     (`docs/collection-contract.md` 6절). 둘을 가르려면 "게시된 날"을 먼저 찾아야 하므로
     기준일에서 뒤로 걸어가며 행이 있는 날을 잡고, 그 날짜로 전 서비스를 찍는다.
  4) ECOS — 키가 없으면 공개 sample 키로 떨어진다. 어느 쪽으로 동작 중인지 밝힌다.

종료 코드는 필수 경로가 전부 살아 있을 때만 0이다. 선택 항목(코스닥 전종목·지수,
ECOS 전용 키)이 빠져 있으면 경고만 남기고 0을 준다.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from datetime import datetime, timedelta

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import kiwoom_collect as kc  # noqa: E402

# 환경변수 — (이름, 필수 여부, 쓰임)
ENV_VARS = [
    ("APP_KEY", True, "키움 앱키"),
    ("APP_SECRET", True, "키움 시크릿"),
    ("KIWOOM_MODE", False, "demo(모의) | real(실전). 미설정 시 demo"),
    ("KRX_AUTH_KEY", True, "KRX OpenAPI 키 — 파생·확정종가 전용"),
    ("ECOS_API_KEY", False, "한국은행 ECOS 키. 없으면 sample 폴백(10행 제한)"),
]

# KRX 서비스 — (경로, 라벨, 필수 여부). 필수는 수집기가 실제로 호출하는 것들이다.
KRX_PROBES = [
    ("sto/stk_bydd_trd", "유가증권 전종목 일별매매정보(종가 정본)", True),
    ("drv/fut_bydd_trd", "선물 일별매매정보", True),
    ("drv/opt_bydd_trd", "옵션 일별매매정보", True),
    ("sto/ksq_bydd_trd", "코스닥 전종목 일별매매정보", False),
    ("idx/krx_dd_trd", "KRX 지수 일별시세", False),
]

# 게시된 날을 찾으려고 뒤로 걸어갈 최대 일수. 추석·설 연휴가 최대 4영업일이라 12일이면 넉넉하다.
LOOKBACK_DAYS = 12

OK, WARN, FAIL = "OK", "WARN", "FAIL"


def _mark(status: str) -> str:
    return {OK: "[OK]  ", WARN: "[WARN]", FAIL: "[FAIL]"}[status]


# --- 1. 환경변수 -------------------------------------------------------------


def check_env() -> dict:
    rows = []
    for name, required, usage in ENV_VARS:
        raw = os.environ.get(name)
        if raw is None or not raw.strip():
            rows.append(
                {
                    "name": name,
                    "status": FAIL if required else WARN,
                    "detail": "미설정",
                    "usage": usage,
                }
            )
            continue
        cleaned = kc._clean_secret(raw)
        stripped = len(raw.strip()) - len(cleaned)
        detail = f"설정됨 ({len(cleaned)}자)"
        if stripped:
            # 값은 노출하지 않는다. 수집기가 읽는 즉시 털어내므로 실패 원인은 아니다.
            detail += f", 비가시 문자 {stripped}개 포함(수집기가 자동 제거)"
        rows.append({"name": name, "status": OK, "detail": detail, "usage": usage})
    return {"section": "환경변수", "rows": rows}


# --- 2. 키움 REST ------------------------------------------------------------


def _token_for(mode: str, timeout: int) -> tuple[bool, str]:
    """해당 투자구분으로 토큰 발급을 시도한다. (성공여부, 메시지)."""
    saved = os.environ.get("KIWOOM_MODE")
    os.environ["KIWOOM_MODE"] = mode
    try:
        token = kc.issue_token(timeout=timeout, use_cache=True)
        return True, token
    except kc.KiwoomError as exc:
        return False, str(exc)
    finally:
        if saved is None:
            os.environ.pop("KIWOOM_MODE", None)
        else:
            os.environ["KIWOOM_MODE"] = saved


def check_kiwoom(timeout: int) -> dict:
    rows = []
    live_mode = None
    tokens: dict[str, str] = {}
    for mode in ("demo", "real"):
        ok, payload = _token_for(mode, timeout)
        if ok:
            tokens[mode] = payload
            live_mode = live_mode or mode
            rows.append(
                {
                    "name": f"{mode} 토큰({kc.BASE_URLS[mode]})",
                    "status": OK,
                    "detail": "발급 성공",
                }
            )
        else:
            # 8030은 "키는 유효하나 반대편 투자구분"이라는 뜻이다. 키 오류와 구분해 적는다.
            mismatch = "8030" in payload or "투자구분" in payload
            rows.append(
                {
                    "name": f"{mode} 토큰({kc.BASE_URLS[mode]})",
                    "status": WARN if mismatch else FAIL,
                    "detail": ("투자구분 불일치 — 이 키는 다른 쪽 전용" if mismatch else payload),
                    "raw": payload,
                }
            )

    if live_mode is None:
        rows.append({"name": "지수 조회(ka20001)", "status": FAIL, "detail": "토큰이 없어 건너뜀"})
        return {"section": "키움 REST", "rows": rows, "live_mode": None}

    # 토큰 발급만으로는 api-id 권한을 알 수 없다. 가장 싼 조회 1건을 실제로 쏴 본다.
    saved = os.environ.get("KIWOOM_MODE")
    os.environ["KIWOOM_MODE"] = live_mode
    try:
        data = kc.call("ka20001", kc.PATHS["sect"], {"mrkt_tp": "0", "inds_cd": "001"},
                       tokens[live_mode], timeout=timeout)
        price = data.get("cur_prc")
        rows.append(
            {
                "name": f"지수 조회(ka20001, {live_mode})",
                "status": OK,
                "detail": f"KOSPI cur_prc={price}",
            }
        )
    except kc.KiwoomError as exc:
        rows.append(
            {"name": f"지수 조회(ka20001, {live_mode})", "status": FAIL, "detail": str(exc)}
        )
    finally:
        if saved is None:
            os.environ.pop("KIWOOM_MODE", None)
        else:
            os.environ["KIWOOM_MODE"] = saved

    return {"section": "키움 REST", "rows": rows, "live_mode": live_mode}


# --- 3. KRX OpenAPI ----------------------------------------------------------


def _krx_probe(path: str, date: str, key: str, timeout: int) -> tuple[str, str]:
    """(status, detail). 401=미신청 / 200+0행=미게시 / 200+n행=정상."""
    url = f"{kc.KRX_BASE}/{path}?basDd={date}"
    request = urllib.request.Request(url, headers={"AUTH_KEY": key})
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            body = response.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as exc:
        if exc.code == 401:
            return "unauthorized", "401 — 이용신청 미승인(서비스별로 따로 신청해야 한다)"
        if exc.code == 404:
            return "missing", f"404 — 경로 없음: {path}"
        return "error", f"HTTP {exc.code}"
    except Exception as exc:  # 타임아웃·프록시 차단
        return "error", f"{type(exc).__name__}: {str(exc)[:120]}"
    try:
        data = json.loads(body)
    except ValueError:
        return "error", f"비JSON 응답 앞 120자: {body[:120]!r}"
    if isinstance(data, dict) and data.get("respCode"):
        return "error", f"respCode={data['respCode']} {str(data.get('respMsg'))[:80]}"
    for value in (data.values() if isinstance(data, dict) else []):
        if isinstance(value, list):
            return ("rows", f"{len(value):,}행") if value else ("empty", "0행 — 해당일 미게시")
    return "error", f"목록 필드 없음: {list(data)[:4] if isinstance(data, dict) else type(data)}"


def check_krx(date: str, timeout: int) -> dict:
    raw = os.environ.get("KRX_AUTH_KEY", "")
    if not raw.strip():
        return {
            "section": "KRX OpenAPI",
            "rows": [{"name": "KRX_AUTH_KEY", "status": FAIL, "detail": "미설정 — 파생·확정종가 전체가 빠진다"}],
            "posted_date": None,
        }
    key = kc._clean_secret(raw)

    # 기준일이 휴장일이면 전 서비스가 0행으로 나와 미신청과 구분되지 않는다.
    # 먼저 "행이 있는 날"을 하나 찾는다 — 이 스크립트에서 가장 중요한 한 단계다.
    base = datetime.strptime(date, "%Y%m%d")
    posted = None
    walked = []
    for offset in range(LOOKBACK_DAYS + 1):
        probe_date = (base - timedelta(days=offset)).strftime("%Y%m%d")
        status, detail = _krx_probe("sto/stk_bydd_trd", probe_date, key, timeout)
        walked.append((probe_date, status, detail))
        if status == "rows":
            posted = probe_date
            break
        if status in ("unauthorized", "error"):
            break

    rows = []
    if posted is None:
        last_date, last_status, last_detail = walked[-1]
        rows.append(
            {
                "name": "게시일 탐색",
                "status": FAIL,
                "detail": f"{walked[0][0]}부터 {last_date}까지 행 있는 날 없음 — 마지막 응답: {last_detail}",
            }
        )
        # 키 유효성만이라도 가른다.
        for path, label, required in KRX_PROBES:
            status, detail = _krx_probe(path, last_date, key, timeout)
            rows.append(
                {
                    "name": f"{path} ({label})",
                    "status": FAIL if status == "unauthorized" and required else WARN,
                    "detail": detail,
                }
            )
        return {"section": "KRX OpenAPI", "rows": rows, "posted_date": None}

    lag = (base - datetime.strptime(posted, "%Y%m%d")).days
    rows.append(
        {
            "name": "게시일 탐색",
            "status": OK,
            "detail": f"{posted} 기준으로 점검 (기준일 {date}에서 {lag}일 전)"
            + (" — 휴장·게시지연 구간이다" if lag else ""),
        }
    )
    for path, label, required in KRX_PROBES:
        status, detail = _krx_probe(path, posted, key, timeout)
        if status == "rows":
            verdict = OK
        elif status == "empty":
            # 게시일로 확정한 날짜인데 0행이면 서비스별 게시 주기가 다른 경우다.
            verdict = WARN
        else:
            verdict = FAIL if required else WARN
        rows.append(
            {
                "name": f"{path} ({label})" + ("" if required else " [선택]"),
                "status": verdict,
                "detail": detail,
            }
        )
    return {"section": "KRX OpenAPI", "rows": rows, "posted_date": posted}


# --- 4. ECOS ----------------------------------------------------------------


def check_ecos(date: str, timeout: int) -> dict:
    keyed = bool(kc._clean_secret(os.environ.get("ECOS_API_KEY", "")))
    name, stat, item, label = kc.ECOS_SERIES[0]
    rows = [
        {
            "name": "인증",
            "status": OK if keyed else WARN,
            "detail": "전용 키 사용" if keyed else "키 없음 — 공개 sample 키로 폴백(1회 10행 제한)",
        }
    ]
    try:
        data = kc.fetch_ecos(stat, item, date, timeout=timeout)
        rows.append(
            {
                "name": f"{label}({name})",
                "status": OK,
                "detail": f"{data.get('date')} {data.get('value')}",
            }
        )
    except kc.KiwoomError as exc:
        rows.append({"name": f"{label}({name})", "status": FAIL, "detail": str(exc)})
    return {"section": "ECOS", "rows": rows, "keyed": keyed}


# --- 출력 -------------------------------------------------------------------


def render(sections: list[dict]) -> int:
    worst = OK
    for section in sections:
        print(f"\n== {section['section']} ==")
        for row in section["rows"]:
            print(f"{_mark(row['status'])} {row['name']}: {row['detail']}")
            if row["status"] == FAIL:
                worst = FAIL
            elif row["status"] == WARN and worst == OK:
                worst = WARN

    fails = [
        (s["section"], r) for s in sections for r in s["rows"] if r["status"] == FAIL
    ]
    warns = [
        (s["section"], r) for s in sections for r in s["rows"] if r["status"] == WARN
    ]
    print("\n== 판정 ==")
    if not fails:
        print("[OK] 필수 수집 경로 전부 정상 — 회차를 돌릴 수 있다.")
    else:
        print(f"[FAIL] 필수 경로 {len(fails)}건 실패 — 아래를 먼저 고쳐라.")
        for section, row in fails:
            print(f"  · {section} / {row['name']}: {row['detail']}")
    if warns:
        print(f"[WARN] 선택 항목 {len(warns)}건 — 없어도 돌지만 그만큼 항목이 빠진다.")
        for section, row in warns:
            print(f"  · {section} / {row['name']}: {row['detail']}")
    print("\n조치 방법은 docs/setup.md, 실패 유형 분류는 docs/collection-contract.md 6절.")
    return 1 if fails else 0


def main() -> int:
    parser = argparse.ArgumentParser(description="키움·KRX·ECOS 세팅 진단")
    parser.add_argument("--date", help="기준일자 YYYYMMDD (기본: 오늘 KST)")
    parser.add_argument("--timeout", type=int, default=30, help="호출당 타임아웃 초 (기본 30)")
    parser.add_argument("--json", action="store_true", help="JSON으로 출력")
    parser.add_argument("--skip-krx", action="store_true", help="KRX 점검 생략(게시일 탐색이 느릴 때)")
    args = parser.parse_args()

    date = args.date or datetime.now(kc.KST).strftime("%Y%m%d")
    sections = [check_env(), check_kiwoom(args.timeout)]
    if not args.skip_krx:
        sections.append(check_krx(date, args.timeout))
    sections.append(check_ecos(date, args.timeout))

    if args.json:
        fails = sum(1 for s in sections for r in s["rows"] if r["status"] == FAIL)
        print(
            json.dumps(
                {
                    "checked_at_kst": datetime.now(kc.KST).isoformat(),
                    "base_date": date,
                    "sections": sections,
                    "ok": fails == 0,
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        return 1 if fails else 0
    return render(sections)


if __name__ == "__main__":
    sys.exit(main())
