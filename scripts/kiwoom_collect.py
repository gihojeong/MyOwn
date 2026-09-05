#!/usr/bin/env python3
"""키움증권 REST OpenAPI 수집기 — KOSPI 개장전·마감후·주간 리포트 예약작업용.

표준 라이브러리만 사용한다. 예약작업이 뜨는 컨테이너는 매번 새로 만들어지므로
uv sync(약 140MB)나 MCP 기동 없이 바로 돌아가야 한다. urllib은 https_proxy와
SSL_CERT_FILE을 자동으로 따르므로 프록시 환경에서 추가 설정이 필요 없다.

자격증명은 환경변수로만 받는다. 인자로 받지 않는 이유는 프로세스 목록과
셸 히스토리에 남기지 않기 위해서다.

  APP_KEY       발급받은 앱키
  APP_SECRET    발급받은 시크릿
  KIWOOM_MODE   demo(모의투자, 기본) | real(실전투자)

사용 예:

  # 자격증명·도달성 점검 (토큰 발급까지만)
  python3 scripts/kiwoom_collect.py --check

  # 마감 리포트 (평일 18:05) — 당일 확정치
  python3 scripts/kiwoom_collect.py --preset close --out data/close_$(date +%Y%m%d).json

  # 개장 전 브리핑 (평일 06:00) — 직전 거래일 확정치를 --date로 지정
  python3 scripts/kiwoom_collect.py --preset premarket --date 20260904 --out data/pre.json

  # 주간 리뷰 (토 06:00)
  python3 scripts/kiwoom_collect.py --preset weekly --out data/weekly.json

  # 임의 API 단건 (스펙 확인·디버깅)
  python3 scripts/kiwoom_collect.py --call ka20001 --path /api/dostk/sect \
      --body '{"mrkt_tp":"0","inds_cd":"001"}'

개별 호출이 실패해도 전체를 중단하지 않는다. 실패한 항목은 결과 JSON에 error로
남으므로, 리포트에서 "확인 불가"가 데이터 부재인지 수집 실패인지 구분할 수 있다.

요청 파라미터는 모두 kiwoom-spec MCP(spec_show / kiwoom_help)로 확인한 값이다.
추측으로 채운 항목은 없다.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timedelta, timezone
from typing import Any, Callable

KST = timezone(timedelta(hours=9))

BASE_URLS = {
    "real": "https://api.kiwoom.com",
    "demo": "https://mockapi.kiwoom.com",
}

TOKEN_PATH = "/oauth2/token"

# urllib이 기본으로 보내는 "Python-urllib/3.x"는 키움 WAF가 400 Request Blocked로
# 막는다(2026-09-05 실측). 평범한 User-Agent를 명시하면 통과한다.
USER_AGENT = "kiwoom-collect/1.0"

# 유량 초과(1700)는 API별로 창이 좁아 연속조회에서 자주 걸린다. 짧게 기다렸다 재시도한다.
RATE_LIMIT_RETRIES = 3
RATE_LIMIT_BACKOFF = 1.0

# 토큰 발급(au10001)에는 유량 제한이 있어 연속 호출하면 1700으로 거절된다.
# 발급 토큰은 24시간짜리이므로 만료 전까지 재사용한다.
TOKEN_CACHE_DIR = os.path.join(
    os.environ.get("XDG_CACHE_HOME") or os.path.expanduser("~/.cache"), "kiwoom-collect"
)

PATHS = {
    "sect": "/api/dostk/sect",
    "mrkcond": "/api/dostk/mrkcond",
    "stkinfo": "/api/dostk/stkinfo",
    "chart": "/api/dostk/chart",
    "rkinfo": "/api/dostk/rkinfo",
    "frgnistt": "/api/dostk/frgnistt",
}

# 리포트가 종목 단위로 추적하는 관심종목. --codes로 덮어쓸 수 있다.
WATCHLIST = {
    "005930": "삼성전자",
    "005935": "삼성전자우",  # 자사주 소각 국면에서 보통주와 등락이 갈린다
    "000660": "SK하이닉스",
    "402340": "SK스퀘어",
    "034020": "두산에너빌리티",
    "373220": "LG에너지솔루션",
    "009150": "삼성전기",
    "005380": "현대차",
}

# ka10063 투자자별 코드. 기관 세부주체까지 분해해야 수급 해부가 채워진다.
# 이 API에는 금융투자와 사모펀드 코드가 없다 — 그 둘은 ka10066 응답의
# fnnc_invt / samo_fund 필드를 종목 단위로 합산해서 얻는다.
INVESTORS = {
    "6": "외국인",
    "7": "기관계",
    "1": "투신",
    "3": "연기금",
    "0": "보험",
    "2": "은행",
    "4": "국가",
    "5": "기타법인",
}

# 거래소구분: 1=KRX, 2=NXT, 3=통합. 지수 산출 기준과 맞추려면 통합을 쓴다.
EXCHANGE_ALL = "3"


class KiwoomError(RuntimeError):
    pass


class KiwoomRateLimited(KiwoomError):
    """유량 초과(HTTP 429 / return_code 1700). 잠시 기다렸다 다시 부르면 된다."""


def _mode() -> str:
    mode = os.environ.get("KIWOOM_MODE", "demo").strip().lower()
    if mode not in BASE_URLS:
        raise KiwoomError(f"KIWOOM_MODE는 demo 또는 real이어야 합니다 (받은 값: {mode!r})")
    return mode


def _credentials() -> tuple[str, str]:
    key = os.environ.get("APP_KEY", "").strip()
    secret = os.environ.get("APP_SECRET", "").strip()
    missing = [n for n, v in (("APP_KEY", key), ("APP_SECRET", secret)) if not v]
    if missing:
        raise KiwoomError(f"환경변수 {', '.join(missing)}가 비어 있습니다.")
    if key.startswith("your_app") or secret.startswith("your_app"):
        raise KiwoomError("APP_KEY/APP_SECRET이 placeholder 상태입니다.")
    return key, secret


def _post(
    url: str, payload: dict[str, Any], headers: dict[str, str], timeout: int
) -> tuple[dict[str, Any], dict[str, str]]:
    """응답 body와 헤더를 함께 돌려준다. 연속조회 키가 헤더로 오기 때문이다."""
    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    request = urllib.request.Request(url, data=data, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            body = response.read().decode("utf-8", errors="replace")
            response_headers = {k.lower(): v for k, v in response.headers.items()}
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")[:500]
        if exc.code == 429:
            raise KiwoomRateLimited(f"HTTP 429: {detail}") from exc
        raise KiwoomError(f"HTTP {exc.code}: {detail}") from exc
    except urllib.error.URLError as exc:
        # 프록시 정책 차단(CONNECT 403)도 여기로 떨어진다.
        raise KiwoomError(f"연결 실패: {exc.reason}") from exc
    try:
        return json.loads(body), response_headers
    except ValueError as exc:
        raise KiwoomError(f"JSON이 아닌 응답: {body[:200]}") from exc


def _token_cache_path() -> str:
    return os.path.join(TOKEN_CACHE_DIR, f"token_{_mode()}.json")


def _cached_token() -> str | None:
    """만료 5분 전까지만 재사용한다. expires_dt는 KST YYYYMMDDHHMMSS."""
    try:
        with open(_token_cache_path(), encoding="utf-8") as handle:
            cache = json.load(handle)
    except (OSError, ValueError):
        return None
    try:
        expires = datetime.strptime(cache["expires_dt"], "%Y%m%d%H%M%S").replace(tzinfo=KST)
    except (KeyError, ValueError):
        return None
    if expires - timedelta(minutes=5) <= datetime.now(KST):
        return None
    return cache.get("token")


def _save_token(token: str, expires_dt: str) -> None:
    """캐시 파일은 토큰을 담으므로 소유자만 읽을 수 있게 만든다."""
    try:
        os.makedirs(TOKEN_CACHE_DIR, mode=0o700, exist_ok=True)
        path = _token_cache_path()
        with open(path, "w", encoding="utf-8") as handle:
            json.dump({"token": token, "expires_dt": expires_dt}, handle)
        os.chmod(path, 0o600)
    except OSError:
        pass  # 캐시는 최적화일 뿐이라 실패해도 수집은 계속한다


def issue_token(timeout: int = 20, use_cache: bool = True) -> str:
    """접근토큰을 얻는다 (au10001). 응답의 토큰 필드명은 'token'이다.

    발급에 유량 제한이 있어(초과 시 return_code 1700) 캐시된 토큰을 우선 쓴다.
    """
    if use_cache:
        cached = _cached_token()
        if cached:
            return cached
    key, secret = _credentials()
    payload = {"grant_type": "client_credentials", "appkey": key, "secretkey": secret}
    headers = {"Content-Type": "application/json;charset=UTF-8", "User-Agent": USER_AGENT}
    data, _ = _post(BASE_URLS[_mode()] + TOKEN_PATH, payload, headers, timeout)
    if data.get("return_code") not in (None, 0):
        raise KiwoomError(f"토큰 발급 실패 [{data.get('return_code')}]: {data.get('return_msg')}")
    token = data.get("token")
    if not token:
        raise KiwoomError("토큰 응답에 token 필드가 없습니다.")
    if data.get("expires_dt"):
        _save_token(token, str(data["expires_dt"]))
    return token


def call(
    api_id: str,
    path: str,
    body: dict[str, Any],
    token: str,
    timeout: int = 30,
    max_pages: int = 1,
) -> dict[str, Any]:
    """조회 API 한 건을 호출한다. return_code가 0이 아니면 KiwoomError.

    응답 헤더의 cont-yn이 Y면 next-key로 이어 받는다. 목록형 응답은 한 페이지가
    100행 안팎이라(ka10066 실측), 시장 전체 수급을 다루려면 이어받아야 한다.
    페이지를 합칠 때는 리스트 필드만 이어붙이고 스칼라 필드는 첫 페이지 값을 남긴다.
    """
    url = BASE_URLS[_mode()] + path
    merged: dict[str, Any] = {}
    cont_yn = ""
    next_key = ""
    for page in range(max_pages):
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "User-Agent": USER_AGENT,
            "authorization": f"Bearer {token}",
            "api-id": api_id,
        }
        if cont_yn == "Y" and next_key:
            headers["cont-yn"] = cont_yn
            headers["next-key"] = next_key
        # 유량 제한은 API마다 다르고 ka10066은 1회로 좁다. 초당 한도라 짧은 대기로 풀린다.
        for attempt in range(RATE_LIMIT_RETRIES + 1):
            try:
                data, response_headers = _post(url, body, headers, timeout)
                break
            except KiwoomRateLimited:
                if attempt == RATE_LIMIT_RETRIES:
                    raise
                time.sleep(RATE_LIMIT_BACKOFF * (2**attempt))
        code = data.get("return_code")
        if code not in (None, 0):
            raise KiwoomError(f"{api_id} 실패 [{code}]: {data.get('return_msg')}")
        if not merged:
            merged = data
        else:
            for key, value in data.items():
                if isinstance(value, list) and isinstance(merged.get(key), list):
                    merged[key].extend(value)
        merged["_pages_fetched"] = page + 1
        cont_yn = response_headers.get("cont-yn", "")
        next_key = response_headers.get("next-key", "")
        if cont_yn != "Y" or not next_key:
            break
    return merged


def _job(
    name: str, api_id: str, path_key: str, body: dict[str, Any], max_pages: int = 1
) -> dict[str, Any]:
    return {
        "name": name,
        "api_id": api_id,
        "path": PATHS[path_key],
        "body": body,
        "max_pages": max_pages,
    }


# --- 재사용 블록 -------------------------------------------------------------


def _indices() -> list[dict[str, Any]]:
    """ka20001. inds_cur_prc_tm에 시간별 지수가 함께 와서 장중 궤적까지 한 번에 얻는다."""
    return [
        _job("index_kospi", "ka20001", "sect", {"mrkt_tp": "0", "inds_cd": "001"}),
        _job("index_kosdaq", "ka20001", "sect", {"mrkt_tp": "1", "inds_cd": "101"}),
        _job("index_kospi200", "ka20001", "sect", {"mrkt_tp": "2", "inds_cd": "201"}),
        _job("sector_indices_kospi", "ka20003", "sect", {"inds_cd": "001"}),
    ]


def _investor_flows(date: str) -> list[dict[str, Any]]:
    """ka10063을 투자자별로 나눠 호출해야 기관 세부주체가 분리된다."""
    jobs = [
        _job(
            f"investor_intraday_{label}",
            "ka10063",
            "mrkcond",
            {
                "mrkt_tp": "001",
                "amt_qty_tp": "1",
                "invsr": code,
                "frgn_all": "0",
                "smtm_netprps_tp": "0",
                "stex_tp": EXCHANGE_ALL,
            },
            max_pages=6,
        )
        for code, label in INVESTORS.items()
    ]
    jobs.append(
        # 종목 단위 행. etc_corp(기타법인)가 응답에 직접 있어 3주체 잔차 역산이 불필요하다.
        _job(
            "investor_after_close",
            "ka10066",
            "mrkcond",
            {"mrkt_tp": "001", "amt_qty_tp": "1", "trde_tp": "0", "stex_tp": EXCHANGE_ALL},
            max_pages=12,
        )
    )
    jobs.append(
        _job(
            "sector_investor_flows_kospi",
            "ka10051",
            "sect",
            {"mrkt_tp": "0", "amt_qty_tp": "0", "base_dt": date, "stex_tp": EXCHANGE_ALL},
        )
    )
    jobs.append(
        _job(
            "foreign_institution_top",
            "ka90009",
            "rkinfo",
            {
                "mrkt_tp": "001",
                "amt_qty_tp": "1",
                "qry_dt_tp": "1",
                "date": date,
                "stex_tp": EXCHANGE_ALL,
            },
        )
    )
    return jobs


def _investor_streak(days: str = "5") -> list[dict[str, Any]]:
    """ka10131. 최근 N거래일 연속 순매수 — 오늘 수급이 추세 지속인지 전환인지 판별용."""
    return [
        _job(
            f"investor_streak_{days}d",
            "ka10131",
            "frgnistt",
            {
                "dt": days,
                "mrkt_tp": "001",
                "netslmt_tp": "2",
                "stk_inds_tp": "0",
                "amt_qty_tp": "0",
                "stex_tp": EXCHANGE_ALL,
            },
        )
    ]


def _rankings() -> list[dict[str, Any]]:
    jobs = [
        _job(
            "amount_top",
            "ka10032",
            "rkinfo",
            {"mrkt_tp": "001", "mang_stk_incls": "1", "stex_tp": EXCHANGE_ALL},
        )
    ]
    # sort_tp 1=상승률, 3=하락률
    for sort_tp, label in (("1", "rise"), ("3", "fall")):
        jobs.append(
            _job(
                f"change_rate_top_{label}",
                "ka10027",
                "rkinfo",
                {
                    "mrkt_tp": "001",
                    "sort_tp": sort_tp,
                    "trde_qty_cnd": "0000",
                    "stk_cnd": "0",
                    "crd_cnd": "0",
                    "updown_incls": "1",
                    "pric_cnd": "0",
                    "trde_prica_cnd": "0",
                    "stex_tp": EXCHANGE_ALL,
                },
            )
        )
    return jobs


def _after_hours() -> list[dict[str, Any]]:
    """시간외 단일가(16:00~18:00). 마감 리포트는 18:05 실행이라 데이터가 이미 확정돼 있다."""
    jobs = []
    # sort_base 1=상승률, 3=하락률
    for sort_base, label in (("1", "rise"), ("3", "fall")):
        jobs.append(
            _job(
                f"after_hours_rank_{label}",
                "ka10098",
                "rkinfo",
                {
                    "mrkt_tp": "001",
                    "sort_base": sort_base,
                    "stk_cnd": "0",
                    "trde_qty_cnd": "0",
                    "crd_cnd": "0",
                    "trde_prica": "0",
                },
            )
        )
    for code, name in WATCHLIST.items():
        jobs.append(_job(f"after_hours_{name}", "ka10087", "mrkcond", {"stk_cd": code}))
    return jobs


def _per_stock(date: str, weekly: bool = False) -> list[dict[str, Any]]:
    api_id = "ka10082" if weekly else "ka10081"
    kind = "weekly" if weekly else "daily"
    jobs = [
        # upd_stkpc_tp는 kiwoom_help에 optional로 적혀 있으나 서버는 필수로 요구한다
        # (2026-09-05 실측: 생략 시 1511 "필수 입력 값에 값이 존재하지 않습니다"). 1=수정주가.
        _job(
            f"candle_{kind}_{name}",
            api_id,
            "chart",
            {"stk_cd": code, "base_dt": date, "upd_stkpc_tp": "1"},
        )
        for code, name in WATCHLIST.items()
    ]
    if not weekly:
        jobs += [
            _job(
                f"investor_by_stock_{name}",
                "ka10059",
                "stkinfo",
                {
                    "dt": date,
                    "stk_cd": code,
                    "amt_qty_tp": "1",
                    "trde_tp": "0",
                    "unit_tp": "1000",
                },
            )
            for code, name in WATCHLIST.items()
        ]
    return jobs


# --- preset -----------------------------------------------------------------


def preset_close(date: str) -> list[dict[str, Any]]:
    """마감 리포트 (평일 18:05). 당일 확정 종가·수급·시간외까지."""
    return _indices() + _investor_flows(date) + _investor_streak() + _rankings() + _after_hours() + _per_stock(date)


def preset_premarket(date: str) -> list[dict[str, Any]]:
    """개장 전 브리핑 (평일 06:00). --date에 직전 거래일을 넘긴다."""
    return _indices() + _investor_flows(date) + _investor_streak() + _rankings() + _per_stock(date)


def preset_weekly(date: str) -> list[dict[str, Any]]:
    """주간 리뷰 (토 06:00). 주봉과 5거래일 누적 수급 중심."""
    return (
        _indices()
        + _investor_flows(date)
        + _investor_streak("5")
        + _investor_streak("20")
        + _per_stock(date, weekly=True)
    )


PRESETS: dict[str, Callable[[str], list[dict[str, Any]]]] = {
    "close": preset_close,
    "premarket": preset_premarket,
    "weekly": preset_weekly,
}


def run_jobs(jobs: list[dict[str, Any]], token: str, timeout: int, pause: float) -> dict[str, Any]:
    results: dict[str, Any] = {}
    for job in jobs:
        try:
            results[job["name"]] = {
                "api_id": job["api_id"],
                "request": job["body"],
                "data": call(
                    job["api_id"], job["path"], job["body"], token, timeout, job.get("max_pages", 1)
                ),
            }
        except KiwoomError as exc:
            results[job["name"]] = {"api_id": job["api_id"], "request": job["body"], "error": str(exc)}
        if pause:
            time.sleep(pause)
    return results


def main() -> int:
    parser = argparse.ArgumentParser(description="키움 REST OpenAPI 수집기")
    parser.add_argument("--preset", choices=sorted(PRESETS), help="리포트별 수집 묶음")
    parser.add_argument("--call", metavar="API_ID", help="임의 API 단건 호출")
    parser.add_argument("--path", help="--call과 함께 쓰는 URL 경로 (예: /api/dostk/sect)")
    parser.add_argument("--body", default="{}", help="--call과 함께 쓰는 요청 body (JSON 문자열)")
    parser.add_argument("--check", action="store_true", help="토큰 발급까지만 수행해 자격증명·도달성 확인")
    parser.add_argument("--no-token-cache", action="store_true", help="캐시된 토큰을 무시하고 새로 발급")
    parser.add_argument("--date", help="기준일자 YYYYMMDD (기본: 오늘 KST)")
    parser.add_argument("--codes", help="관심종목을 code:name 쌍의 쉼표 목록으로 덮어쓰기")
    parser.add_argument("--out", help="결과 JSON을 저장할 경로 (미지정 시 stdout)")
    parser.add_argument("--timeout", type=int, default=30, help="호출당 타임아웃 초 (기본 30)")
    parser.add_argument("--pause", type=float, default=0.2, help="호출 간 대기 초 (기본 0.2)")
    args = parser.parse_args()

    if not (args.preset or args.call or args.check):
        parser.error("--preset, --call, --check 중 하나는 지정해야 합니다.")

    if args.codes:
        WATCHLIST.clear()
        for pair in args.codes.split(","):
            code, _, name = pair.strip().partition(":")
            WATCHLIST[code] = name or code

    now = datetime.now(KST)
    date = args.date or now.strftime("%Y%m%d")

    try:
        mode = _mode()
        token = issue_token(args.timeout, use_cache=not args.no_token_cache)
    except KiwoomError as exc:
        print(f"[FAIL] {exc}", file=sys.stderr)
        return 1

    payload: dict[str, Any] = {
        "collected_at_kst": now.isoformat(),
        "base_date": date,
        "mode": mode,
        "base_url": BASE_URLS[mode],
    }

    if args.check:
        payload["token_issued"] = True
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 0

    if args.call:
        if not args.path:
            print("[FAIL] --call에는 --path가 필요합니다.", file=sys.stderr)
            return 1
        jobs = [{"name": args.call, "api_id": args.call, "path": args.path, "body": json.loads(args.body)}]
    else:
        payload["preset"] = args.preset
        jobs = PRESETS[args.preset](date)

    payload["results"] = run_jobs(jobs, token, args.timeout, args.pause)

    failed = sorted(k for k, v in payload["results"].items() if "error" in v)
    payload["summary"] = {
        "requested": len(jobs),
        "succeeded": len(jobs) - len(failed),
        "failed": failed,
    }

    text = json.dumps(payload, ensure_ascii=False, indent=2)
    if args.out:
        os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
        with open(args.out, "w", encoding="utf-8") as handle:
            handle.write(text)
        print(f"{args.out} 저장 — 성공 {payload['summary']['succeeded']}/{len(jobs)}")
        if failed:
            print("실패: " + ", ".join(failed))
    else:
        print(text)

    return 0


if __name__ == "__main__":
    sys.exit(main())
