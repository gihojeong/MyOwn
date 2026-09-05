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
  ECOS_API_KEY  한국은행 ECOS 키(선택). 원/달러·국고채 금리 수집에만 쓰인다.
                없으면 공개 sample 키로 동작한다. 무료 발급: https://ecos.bok.or.kr/api
  KRX_AUTH_KEY  한국거래소 OpenAPI 키(선택). KOSPI200 선물·옵션 수집에만 쓰인다.
                없으면 그 두 항목만 건너뛰고 나머지는 정상 수집한다.

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

키움이 주지 않는 것은 두 곳에서 메운다. 미국 증시·금·유가·달러·미 국채는 키움
해외주식 API로 추종 ETF를 조회하고(추가 키 불필요), 원/달러와 국고채 금리는
한국은행 ECOS에서 받는다. KOSPI200 선물·옵션은 키움 REST OpenAPI에 파생이 아예 없어
한국거래소 OpenAPI에서 받는다(KRX_AUTH_KEY 필요).
"""

from __future__ import annotations

import argparse
import json
import os
import re
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
    "shsa": "/api/dostk/shsa",
    "us_mrkcond": "/api/us/mrkcond",
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

# 지수 바스켓 대용 ETF·해외 상장 한국물. 관심종목(WATCHLIST)과 달리 수급·공매도는 받지 않고
# 시세만 받는다. KODEX MSCI Korea(무캡)와 KOSPI는 반도체 비중이 달라(65.74% vs 51.44%)
# 두 지수를 연립하면 당일 반도체 S와 나머지 R을 분리할 수 있다 — 리포트 [G] ①-b가 요구하는 계산이다.
BASKETS = {"156080": "kodex_msci_korea"}

# 미국 상장 한국물. EWY는 25/50 캡 바스켓이라 KODEX(무캡)와 다르고, 한국 마감 이후 세션에서
# 거래되므로 KODEX·KOSPI로 만든 이론가와의 차이가 곧 미 세션 재평가분(= 갭 신호)이다.
US_KOREA = [
    ("EWY", "NY", "ewy_korea_etf"),
    ("SKM", "NY", "adr_sk_telecom"),
    ("KB", "NY", "adr_kb_financial"),
]

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

# 미국 상장 종목·ETF. 키움 해외주식 API(usa20590)로 조회하며 별도 API 키가 필요 없다.
# 지수 자체(S&P500·나스닥종합)는 키움에 없어서 추종 ETF로 대신한다. 배당과 추적오차
# 때문에 지수 등락률과 소수점 단위로 어긋나므로, 리포트에는 ETF 기준임을 밝혀야 한다.
# GLD·USO·TLT·UUP은 금·WTI·미 장기국채·달러인덱스의 방향과 등락폭을 대신 읽기 위한 것이다.
# stex_tp는 NY:NYSE(Arca 포함), ND:NASDAQ, NA:AMEX. 심볼별 거래소는 2026-09-05에
# 실측으로 확정했다 — 틀리면 1903 "종목 정보가 없습니다"로 떨어진다.
US_WATCHLIST = [
    ("SPY", "NY", "sp500_spy"),
    ("QQQ", "ND", "nasdaq100_qqq"),
    ("DIA", "NY", "dow_dia"),
    ("SOXX", "ND", "semis_soxx"),
    ("GLD", "NY", "gold_gld"),
    ("USO", "NY", "wti_uso"),
    ("TLT", "ND", "ustreasury20y_tlt"),
    ("UUP", "NY", "dollar_uup"),
    ("NVDA", "ND", "nvidia"),
    ("TSM", "NY", "tsmc"),
    ("MU", "ND", "micron"),
    ("AVGO", "ND", "broadcom"),
]

# 한국은행 ECOS OpenAPI. 원/달러와 국고채 금리는 키움에 없다 — 키움 환율 조회(ust31301)는
# 모의투자에서 거절되고(2026-09-05 실측 RC9000), 실전에서도 "환전 적용 고시환율"이라
# 시장 종가와 다르다. ECOS 키는 무료이며 https://ecos.bok.or.kr/api 에서 즉시 발급된다.
# 키가 없으면 공개 "sample" 키로 동작하지만 1회 10행 제한이 있다(항목별로 나눠 부르므로
# 이 수집기의 질의는 제한에 걸리지 않는다).
ECOS_BASE = "https://ecos.bok.or.kr/api/StatisticSearch"
# 통계표·항목 코드와 값은 2026-09-04자로 실측 확인했다.
ECOS_SERIES = [
    ("fx_usdkrw", "731Y001", "0000001", "원/달러 매매기준율"),
    ("ktb_3y", "817Y002", "010200000", "국고채 3년"),
    ("ktb_10y", "817Y002", "010210000", "국고채 10년"),
    ("ktb_30y", "817Y002", "010230000", "국고채 30년"),
    ("cd_91d", "817Y002", "010502000", "CD 91일"),
    ("corp_bond_aa3y", "817Y002", "010300000", "회사채 3년 AA-"),
]
# 한국거래소 OpenAPI. 키움 REST OpenAPI에는 국내 파생이 아예 없어서(2026-09-05 확인:
# spec_groups에 선물·옵션 그룹 없음, 실시간 스트림 21종도 전부 주식·ETF·ELW·업종,
# 선물 종목코드를 quotes API에 직접 넣어도 빈 응답) KOSPI200 선물은 여기서 받는다.
# KRX_AUTH_KEY가 없으면 이 블록만 건너뛴다 — ECOS와 달리 공개 sample 키가 없다.
KRX_BASE = "https://data-dbg.krx.co.kr/svc/apis"
KRX_SERVICES = [
    ("krx_futures", "drv/fut_bydd_trd", "선물 일별매매정보"),
    ("krx_options", "drv/opt_bydd_trd", "옵션 일별매매정보"),
]
# 응답 실측(2026-09-04, 385행). 한 BAS_DD에 정규장과 야간장이 **각각 별도 행**으로 온다.
#   PROD_NM "코스피200 선물"     × MKT_NM "정규"/"야간"  = 13행씩
#   PROD_NM "미니코스피200 선물" × MKT_NM "정규"/"야간"  = 11행씩
# ISU_NM에는 "미니코스피 F 202609 (주간)"처럼 200이 빠진 표기가 있으므로 판정은 PROD_NM으로 한다.
# 행 전체를 join해 "코스피200"으로 매칭하면 정규·야간·미니가 한 덩어리로 섞인다.
KRX_PRODUCTS = {"코스피200 선물": "k200", "미니코스피200 선물": "k200_mini"}
KRX_SESSIONS = {"정규": "regular", "야간": "night"}
# 야간은 정규에 누적된 값이 아니라 세션별 독립 집계다(둘 다 같은 전일 종가를 기준으로 삼는다).
# 합산하면 거래량이 이중계상되고, SETL_PRC(정산가)는 정규장에만 있다.
# 주요 필드: TDD_CLSPRC(종가) SETL_PRC(정산가) SPOT_PRC(기초자산 지수) ACC_OPNINT_QTY(미결제)
#           ACC_TRDVOL(거래량) ACC_TRDVAL(거래대금). 전부 문자열이며 미거래 월물은 ""로 온다.
KRX_MAX_ROWS = 30

# 옵션(opt_bydd_trd)은 선물과 스키마가 다르다. 2026-09-04 실측 17,092행:
#   · MKT_NM·SETL_PRC·SPOT_PRC가 **없다**. 세션은 ISU_NM 끝의 "(정규)"/"(야간)" 접미사뿐이다.
#   · 콜/풋은 RGHT_TP_NM에 영문 대문자 "CALL"/"PUT"으로 온다.
#   · 행사가 전용 필드가 없다. ISU_NM을 파싱해야 하고 천단위 콤마가 들어간다.
#   · IMP_VOLT(내재변동성)가 직접 온다 — BS 역산이 필요 없다. 단 야간행은 전부 "0.00"이다.
#   · "코스닥150 위클리(월) 옵션" 84행만 세션 접미사가 없다(IMP_VOLT/NXTDD_BAS_PRC로 구분).
KRX_OPT_PRODUCTS = {
    "코스피200 옵션": "k200",
    "미니코스피200 옵션": "k200_mini",
    "코스닥150 옵션": "kq150",
    "코스피200 위클리(월) 옵션": "k200_weekly",
    "코스닥150 위클리(월) 옵션": "kq150_weekly",
}
# "코스피200 C 202609 1,150.0 (정규)" — 상품토큰 · C|P · 만기 · 행사가 · (세션)
ISU_NM_RE = re.compile(
    r"^(?P<prod>\S+)\s+(?P<cp>[CP])\s+(?P<term>\d{6}|\d{4}W\d)\s+"
    r"(?P<strike>[\d,]+(?:\.\d+)?)(?:\s*\((?P<sess>정규|야간)\))?\s*$"
)
# 17,092행을 그대로 실으면 결과 JSON이 못 쓰게 커진다. 미결제 상위 행사가만 남긴다.
KRX_OPT_STRIKES = 25

# ECOS는 당일치가 늦게 올라올 수 있다. 범위로 받아 가장 최근 값을 쓰면 공휴일·지연에 견딘다.
# 다만 ECOS는 오래된 행부터 잘라 주므로, sample 키의 10행 제한 안에 기준일이 들어오도록
# 창을 좁게 잡아야 한다(2026-09-05 실측: 14일 창 + sample이면 기준일 하루 전이 최신으로 잡힘).
ECOS_LOOKBACK_DAYS = 10


# 웹 콘솔에서 키를 복사하면 제로폭 문자(U+200B 등)나 비분리 공백이 딸려오는 일이 흔하다.
# 2026-09-05 실측: KRX_AUTH_KEY에 제로폭 문자가 섞여 헤더가 통째로 거부됐다. 눈으로는
# 구분이 안 되고 길이만 1 늘어나므로, 자격증명은 읽는 즉시 이 문자들을 털어낸다.
INVISIBLE_CHARS = "\u200b\u200c\u200d\u2060\ufeff\u00a0"


def _clean_secret(value: str) -> str:
    for ch in INVISIBLE_CHARS:
        value = value.replace(ch, "")
    return value.strip()


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
    key = _clean_secret(os.environ.get("APP_KEY", ""))
    secret = _clean_secret(os.environ.get("APP_SECRET", ""))
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


def _get_json(url: str, timeout: int, extra_headers: dict[str, str] | None = None) -> Any:
    """ECOS·KRX는 GET을 쓴다. 키움과 인증 체계가 달라 따로 둔다."""
    headers = {"User-Agent": USER_AGENT}
    if extra_headers:
        headers.update(extra_headers)
    request = urllib.request.Request(url, headers=headers, method="GET")
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            body = response.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as exc:
        raise KiwoomError(f"HTTP {exc.code}: {exc.read().decode('utf-8', 'replace')[:300]}") from exc
    except urllib.error.URLError as exc:
        raise KiwoomError(f"연결 실패: {exc.reason}") from exc
    try:
        return json.loads(body)
    except ValueError as exc:
        raise KiwoomError(f"JSON이 아닌 응답: {body[:200]}") from exc


def fetch_ecos(stat_code: str, item_code: str, date: str, timeout: int = 30) -> dict[str, Any]:
    """ECOS 일별 시계열 한 건. 최근 값과 직전 값을 함께 돌려줘 전일대비를 바로 계산한다."""
    key = _clean_secret(os.environ.get("ECOS_API_KEY", "")) or "sample"
    rows_max = 10 if key == "sample" else 100  # sample 키는 11행 이상 요청하면 ERROR-301
    end = datetime.strptime(date, "%Y%m%d")
    start = end - timedelta(days=ECOS_LOOKBACK_DAYS)
    url = (
        f"{ECOS_BASE}/{key}/json/kr/1/{rows_max}/{stat_code}/D/"
        f"{start.strftime('%Y%m%d')}/{end.strftime('%Y%m%d')}/{item_code}"
    )
    data = _get_json(url, timeout)
    if "RESULT" in data:  # ECOS는 오류도 HTTP 200으로 준다
        result = data["RESULT"]
        raise KiwoomError(f"ECOS {result.get('CODE')}: {result.get('MESSAGE', '')[:200]}")
    rows = data.get("StatisticSearch", {}).get("row", [])
    if not rows:
        raise KiwoomError("ECOS 응답에 데이터가 없습니다.")
    rows.sort(key=lambda r: r["TIME"])
    latest = rows[-1]
    previous = rows[-2] if len(rows) > 1 else None
    out: dict[str, Any] = {
        "item_name": latest.get("ITEM_NAME1"),
        "unit": latest.get("UNIT_NAME"),
        "date": latest["TIME"],
        "value": latest["DATA_VALUE"],
        "api_key_used": "sample" if key == "sample" else "env",
    }
    if previous:
        out["prev_date"] = previous["TIME"]
        out["prev_value"] = previous["DATA_VALUE"]
        try:
            out["change"] = round(float(latest["DATA_VALUE"]) - float(previous["DATA_VALUE"]), 4)
        except (TypeError, ValueError):
            pass
    return out


def fetch_krx(path: str, date: str, timeout: int = 30) -> dict[str, Any]:
    """KRX OpenAPI 일별 시세 한 건. 인증키는 AUTH_KEY 헤더로 보낸다."""
    raw = os.environ.get("KRX_AUTH_KEY", "")
    key = _clean_secret(raw)
    if key != raw.strip():
        # 무엇이 지워졌는지 값 노출 없이 알린다.
        print(
            f"[warn] KRX_AUTH_KEY에서 보이지 않는 문자 {len(raw.strip()) - len(key)}개를 제거했습니다.",
            file=sys.stderr,
        )
    if not key:
        raise KiwoomError("KRX_AUTH_KEY가 없습니다 — KOSPI200 선물·옵션 수집을 건너뜁니다.")
    try:
        data = _get_json(f"{KRX_BASE}/{path}?basDd={date}", timeout, {"AUTH_KEY": key})
    except KiwoomError as exc:
        # 401은 두 가지다. 키가 틀린 것과, 키는 유효하나 그 서비스를 신청하지 않은 것.
        if "Unauthorized API Call" in str(exc):
            raise KiwoomError(
                f"KRX 서비스 미신청({path}) — 키는 유효하나 이 API 이용 신청이 승인되지 않았다. "
                "KRX OpenAPI 포털에서 해당 서비스를 신청하면 된다."
            ) from exc
        raise
    if isinstance(data, dict) and data.get("respCode"):
        raise KiwoomError(f"KRX {data.get('respCode')}: {data.get('respMsg')}")
    rows: list[Any] = []
    if isinstance(data, dict):
        for value in data.values():
            if isinstance(value, list):
                rows = value
                break
    if not rows:
        raise KiwoomError("KRX 응답에 데이터가 없습니다.")

    out: dict[str, Any] = {"total_rows": len(rows)}
    if "opt_" in path:
        # 옵션은 스키마가 달라 행을 그대로 담지 않고 행사가별 집계로 접는다.
        for key, session in (("k200_regular", "정규"), ("k200_night", "야간")):
            out[key] = summarize_options([r for r in rows if isinstance(r, dict)], "k200", session)
        return out
    matched = 0
    for row in rows:
        if not isinstance(row, dict):
            continue
        product = KRX_PRODUCTS.get(str(row.get("PROD_NM", "")).strip())
        session = KRX_SESSIONS.get(str(row.get("MKT_NM", "")).strip())
        if not product or not session:
            continue
        bucket = out.setdefault(f"{product}_{session}", [])
        if len(bucket) < KRX_MAX_ROWS:
            bucket.append(row)
        matched += 1
    out["matched_rows"] = matched
    if not matched:
        seen = sorted({str(r.get("PROD_NM", "")) for r in rows if isinstance(r, dict)})
        out["seen_products"] = seen[:40]
        out["rows"] = rows[:KRX_MAX_ROWS]
        out["note"] = "KRX_PRODUCTS에 걸린 행이 없다. seen_products로 실제 표기를 확인해 고쳐라."
    return out


def _num(value: Any) -> float:
    """KRX는 모든 값을 문자열로 주고 미거래 항목은 빈 문자열이다."""
    try:
        return float(str(value).replace(",", ""))
    except (TypeError, ValueError):
        return 0.0


def summarize_options(rows: list[dict[str, Any]], product: str = "k200", session: str = "정규") -> dict[str, Any]:
    """행사가별로 접어 P/C 비율·최대고통점·미결제 분포를 만든다.

    리포트가 쓰는 것은 개별 행이 아니라 이 집계다. 거래량이 아니라 미결제약정이
    현물에 대한 헤지 수요를 결정하므로 P/C는 OI 기준을 주 지표로 둔다.
    """
    want = {v: k for k, v in KRX_OPT_PRODUCTS.items()}.get(product)
    picked: list[tuple[str, str, float, dict[str, Any]]] = []
    for row in rows:
        if str(row.get("PROD_NM", "")).strip() != want:
            continue
        match = ISU_NM_RE.match(str(row.get("ISU_NM", "")).strip())
        if not match:
            continue
        # 세션 접미사가 없는 상품은 IMP_VOLT로 가른다(야간행은 IV가 0이다).
        row_session = match.group("sess") or ("정규" if _num(row.get("IMP_VOLT")) > 0 else "야간")
        if row_session != session:
            continue
        picked.append((match.group("term"), match.group("cp"), _num(match.group("strike")), row))
    if not picked:
        return {"matched_rows": 0, "note": f"{product}/{session}에 해당하는 행이 없다."}

    term = min(t for t, _, _, _ in picked)  # 근월물
    near = [(cp, strike, row) for t, cp, strike, row in picked if t == term]
    strikes: dict[float, dict[str, Any]] = {}
    for cp, strike, row in near:
        slot = strikes.setdefault(strike, {"strike": strike})
        side = "call" if cp == "C" else "put"
        slot[f"{side}_oi"] = _num(row.get("ACC_OPNINT_QTY"))
        slot[f"{side}_vol"] = _num(row.get("ACC_TRDVOL"))
        slot[f"{side}_close"] = _num(row.get("TDD_CLSPRC"))
        slot[f"{side}_iv"] = _num(row.get("IMP_VOLT"))

    call_oi = sum(v.get("call_oi", 0.0) for v in strikes.values())
    put_oi = sum(v.get("put_oi", 0.0) for v in strikes.values())
    call_vol = sum(v.get("call_vol", 0.0) for v in strikes.values())
    put_vol = sum(v.get("put_vol", 0.0) for v in strikes.values())

    # 최대고통점: 만기 시 옵션 보유자 총 내재가치가 최소가 되는 행사가.
    pain = {}
    for k in strikes:
        pain[k] = sum(
            v.get("call_oi", 0.0) * max(0.0, k - v["strike"])
            + v.get("put_oi", 0.0) * max(0.0, v["strike"] - k)
            for v in strikes.values()
        )
    max_pain = min(pain, key=pain.get) if pain else None

    top = sorted(
        strikes.values(),
        key=lambda v: v.get("call_oi", 0.0) + v.get("put_oi", 0.0),
        reverse=True,
    )[:KRX_OPT_STRIKES]
    return {
        "product": want,
        "session": session,
        "term": term,
        "strike_count": len(strikes),
        "call_oi": call_oi,
        "put_oi": put_oi,
        "pc_oi_ratio": round(put_oi / call_oi, 4) if call_oi else None,
        "call_volume": call_vol,
        "put_volume": put_vol,
        "pc_volume_ratio": round(put_vol / call_vol, 4) if call_vol else None,
        "max_pain": max_pain,
        "strikes": sorted(top, key=lambda v: v["strike"]),
    }


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


def _program_trades(date: str) -> list[dict[str, Any]]:
    """ka90010 프로그램매매 추이. mrkt_tp("프로그램 시장코드")는 스펙에 값이 열거돼
    있지 않아 실측으로 확인했다(2026-09-05): P00101=코스피, P10102=코스닥.
    001/000/101 같은 일반 시장구분 코드를 넣으면 에러 없이 0행이 돌아온다."""
    return [
        _job(
            f"program_trades_{label}",
            "ka90010",
            "mrkcond",
            {
                "date": date,
                "amt_qty_tp": "1",
                "mrkt_tp": code,
                "min_tic_tp": "0",
                "stex_tp": EXCHANGE_ALL,
            },
        )
        for code, label in (("P00101", "kospi"), ("P10102", "kosdaq"))
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


def _stock_profile() -> list[dict[str, Any]]:
    """ka10001. 시가총액(mac, 억원)·상장주식수(flo_stk, 천주)·PER/PBR·52주 고저.

    시총과 상장주식수는 그동안 웹 조사로 메우던 항목인데 키움이 그대로 준다.
    자사주 소각으로 상장주식수가 줄면 여기서 바로 드러난다.
    """
    return [
        _job(f"profile_{name}", "ka10001", "stkinfo", {"stk_cd": code})
        for code, name in WATCHLIST.items()
    ]


def _short_selling(date: str) -> list[dict[str, Any]]:
    """ka10014. 일자별 공매도 수량·비중(trde_wght)·잔고(ovr_shrts_qty)·평균가.

    tm_tp=1은 기간 조회. 최근 10거래일을 함께 받아 당일 비중이 평소보다 높은지
    판단할 수 있게 한다.
    """
    end = datetime.strptime(date, "%Y%m%d")
    start = (end - timedelta(days=20)).strftime("%Y%m%d")
    return [
        _job(
            f"short_selling_{name}",
            "ka10014",
            "shsa",
            {"stk_cd": code, "tm_tp": "1", "strt_dt": start, "end_dt": date},
        )
        for code, name in WATCHLIST.items()
    ]


def _overseas(date: str) -> list[dict[str, Any]]:
    """usa20590. 미국 확정 종가·등락률. base_dt 이전 내역을 최신순으로 준다."""
    return [
        _job(
            f"us_{label}",
            "usa20590",
            "us_mrkcond",
            {"stex_tp": exchange, "stk_cd": symbol, "base_dt": date},
        )
        for symbol, exchange, label in US_WATCHLIST + US_KOREA
    ]


def _baskets(date: str) -> list[dict[str, Any]]:
    """지수 바스켓 대용 ETF. 국내 상장이므로 관심종목과 같은 API로 받는다."""
    jobs: list[dict[str, Any]] = []
    for code, label in BASKETS.items():
        jobs.append(_job(f"basket_{label}", "ka10001", "stkinfo", {"stk_cd": code}))
        jobs.append(
            _job(
                f"basket_{label}_daily",
                "ka10081",
                "chart",
                {"stk_cd": code, "base_dt": date, "upd_stkpc_tp": "1"},
            )
        )
    return jobs


def _derivatives(date: str, also_today: str | None = None) -> list[dict[str, Any]]:
    """KRX. KOSPI200 선물·옵션 — 키움에 파생이 없어 여기서만 얻는다.

    야간장 행은 그 BAS_DD 정규장에 **선행하는** 세션이다(2026-09-04 실측: 야간과 정규가
    같은 전일 종가를 기준으로 삼는다). 따라서 개장 전 회차에서는 직전 거래일뿐 아니라
    당일자도 받아야 밤사이 야간선물을 읽을 수 있다. 아직 게시 전이면 error로 남는다.
    """
    jobs = [
        {"name": name, "kind": "krx", "path": path, "label": label, "_date": date}
        for name, path, label in KRX_SERVICES
    ]
    if also_today and also_today != date:
        jobs.append(
            {
                "name": "krx_futures_today",
                "kind": "krx",
                "path": "drv/fut_bydd_trd",
                "label": "선물 일별매매정보(당일 — 밤사이 야간장 확인용)",
                "_date": also_today,
            }
        )
    return jobs


def _macro(date: str) -> list[dict[str, Any]]:
    """ECOS. 키움에 없는 원/달러와 국고채 금리."""
    return [
        {
            "name": f"ecos_{name}",
            "kind": "ecos",
            "stat_code": stat,
            "item_code": item,
            "label": label,
            "_date": date,
        }
        for name, stat, item, label in ECOS_SERIES
    ]


# --- preset -----------------------------------------------------------------


def preset_close(date: str) -> list[dict[str, Any]]:
    """마감 리포트 (평일 18:05). 당일 확정 종가·수급·시간외까지."""
    return (
        _indices()
        + _investor_flows(date)
        + _investor_streak()
        + _program_trades(date)
        + _rankings()
        + _after_hours()
        + _per_stock(date)
        + _stock_profile()
        + _short_selling(date)
        + _baskets(date)
        + _overseas(date)
        + _derivatives(date)
        + _macro(date)
    )


def preset_premarket(date: str) -> list[dict[str, Any]]:
    """개장 전 브리핑 (평일 06:00). --date에 직전 거래일을 넘긴다."""
    return (
        _indices()
        + _investor_flows(date)
        + _investor_streak()
        + _program_trades(date)
        + _rankings()
        + _per_stock(date)
        + _stock_profile()
        + _short_selling(date)
        + _baskets(date)
        + _overseas(date)
        + _derivatives(date, datetime.now(KST).strftime("%Y%m%d"))
        + _macro(date)
    )


def preset_weekly(date: str) -> list[dict[str, Any]]:
    """주간 리뷰 (토 06:00). 주봉과 5거래일 누적 수급 중심."""
    return (
        _indices()
        + _investor_flows(date)
        + _investor_streak("5")
        + _investor_streak("20")
        + _program_trades(date)
        + _per_stock(date, weekly=True)
        + _stock_profile()
        + _short_selling(date)
        + _baskets(date)
        + _overseas(date)
        + _derivatives(date)
        + _macro(date)
    )


PRESETS: dict[str, Callable[[str], list[dict[str, Any]]]] = {
    "close": preset_close,
    "premarket": preset_premarket,
    "weekly": preset_weekly,
}


def run_jobs(jobs: list[dict[str, Any]], token: str, timeout: int, pause: float) -> dict[str, Any]:
    results: dict[str, Any] = {}
    for job in jobs:
        if job.get("kind") == "krx":
            try:
                results[job["name"]] = {
                    "source": "krx",
                    "label": job["label"],
                    "data": fetch_krx(job["path"], job["_date"], timeout),
                }
            except KiwoomError as exc:
                results[job["name"]] = {"source": "krx", "label": job["label"], "error": str(exc)}
            if pause:
                time.sleep(pause)
            continue
        if job.get("kind") == "ecos":
            try:
                results[job["name"]] = {
                    "source": "ecos",
                    "label": job["label"],
                    "data": fetch_ecos(job["stat_code"], job["item_code"], job["_date"], timeout),
                }
            except KiwoomError as exc:
                results[job["name"]] = {"source": "ecos", "label": job["label"], "error": str(exc)}
            if pause:
                time.sleep(pause)
            continue
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
