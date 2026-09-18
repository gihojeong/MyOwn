#!/usr/bin/env python3
"""KRX 파생 일별매매정보 게시 여부 점검기.

`krx_futures` / `krx_options` 가 실패했을 때 **인증 문제인지 당일 미게시인지**를
30초 안에 가른다. 날짜만 바꿔 같은 키로 호출하므로, 전일이 정상 응답하면
키는 유효하고 서비스도 신청돼 있다는 뜻이다.

    python3 scripts/close-report/krx_probe.py 20260918 20260917 20260916

인자를 생략하면 오늘·어제·그제를 본다. 키 값은 절대 출력하지 않는다.

2026-09-18 18:4x / 20:0x 실측:
    20260916  선물 385행 / 옵션 16,332행
    20260917  선물 385행 / 옵션 16,788행
    20260918  선물   0행 / 옵션      0행   <- 당일은 저녁까지 미게시

즉 저녁 회차(18:0x)에서 당일 선물·옵션은 구조적으로 확보 불가다.
9/08~9/18 마감 리포트 10회가 이것을 "인증 오류"로 오진했다. 반복하지 마라.
"""
import os
import sys
import json
import datetime
import urllib.request

KRX_BASE = "http://data-dbg.krx.co.kr/svc/apis"
PATHS = (("drv/fut_bydd_trd", "선물"), ("drv/opt_bydd_trd", "옵션"))

# 웹 콘솔에서 붙여넣을 때 딸려오는 비가시 문자. 수집기 _clean_secret()과 같은 집합이다.
INVISIBLE = tuple(chr(cp) for cp in (0x200B, 0x200C, 0x200D, 0xFEFF))


def load_key() -> str:
    raw = os.environ.get("KRX_AUTH_KEY", "")
    key = raw.strip()
    for ch in INVISIBLE:
        key = key.replace(ch, "")
    if not key:
        sys.exit("KRX_AUTH_KEY가 비어 있다 — 환경변수를 확인하라.")
    stripped = len(raw.strip()) - len(key)
    if stripped:
        # 값은 노출하지 않는다. 제거했다는 사실만 알린다 — 이것은 실패 원인이 아니다.
        print(f"[info] 비가시 문자 {stripped}개를 제거했다(무해).", file=sys.stderr)
    return key


def probe(key: str, path: str, date: str) -> str:
    req = urllib.request.Request(
        f"{KRX_BASE}/{path}?basDd={date}", headers={"AUTH_KEY": key}
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            status = resp.status
            body = resp.read().decode("utf-8", "replace")
    except Exception as exc:  # 401·타임아웃 등
        return f"HTTP 예외: {type(exc).__name__} {exc}"
    try:
        data = json.loads(body)
    except ValueError:
        return f"status={status} 비JSON 앞 200자: {body[:200]!r}"
    if isinstance(data, dict) and data.get("respCode"):
        return f"status={status} respCode={data['respCode']} respMsg={data.get('respMsg')}"
    rows: list = []
    if isinstance(data, dict):
        for value in data.values():
            if isinstance(value, list):
                rows = value
                break
    verdict = "미게시" if not rows else "정상"
    return f"status={status} rows={len(rows):,} -> {verdict}"


def main() -> None:
    dates = sys.argv[1:]
    if not dates:
        today = datetime.date.today()
        dates = [(today - datetime.timedelta(days=n)).strftime("%Y%m%d") for n in range(3)]
    key = load_key()
    for date in dates:
        for path, label in PATHS:
            print(f"{date} {label} {path:22s} -> {probe(key, path, date)}")
    print(
        "\n전일이 '정상'이면 키는 유효하다. 당일만 '미게시'인 것은 인증 문제가 아니라\n"
        "KRX 게시 지연이며 손댈 것이 없다 — 아침 회차가 전일자로 받으면 된다."
    )


if __name__ == "__main__":
    main()
