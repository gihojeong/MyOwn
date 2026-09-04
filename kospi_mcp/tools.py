"""MCP 도구 정의와 실행 로직.

각 핸들러는 사람이 읽을 요약 + 원본 JSON을 함께 담은 문자열을 돌려준다.
TR별 응답 필드명은 키움 문서 개정에 따라 달라질 수 있어, 요약은 후보 키를
훑는 방식(`pick`)으로 만들고 원본을 항상 덧붙인다.
"""

from __future__ import annotations

import json
import os
import time
from typing import Any, Callable

from .format import (
    INDEX_CODES,
    direction,
    fmt,
    fmt_int,
    fmt_signed,
    parse_num,
    pick,
    resolve_index_code,
    scale_index,
    table,
)
from .kiwoom import KiwoomClient, KiwoomError

# 리소스 경로 (키움 REST API)
URL_SECT = "/api/dostk/sect"      # 업종
URL_STKINFO = "/api/dostk/stkinfo"  # 종목정보
URL_MRKCOND = "/api/dostk/mrkcond"  # 시세
URL_CHART = "/api/dostk/chart"    # 차트
URL_RKINFO = "/api/dostk/rkinfo"  # 순위정보

RAW_LIMIT = 4000  # 원본 JSON 첨부 최대 길이(문자)


def _index_scale_mode() -> str:
    return (os.environ.get("KIWOOM_INDEX_SCALE") or "auto").strip().lower()


def _raw_block(data: dict[str, Any]) -> str:
    text = json.dumps(data, ensure_ascii=False, indent=2)
    if len(text) > RAW_LIMIT:
        text = text[:RAW_LIMIT] + f"\n... (생략, 전체 {len(text):,}자)"
    return "```json\n" + text + "\n```"


def _first_list_of_dicts(data: dict[str, Any]) -> tuple[str | None, list[dict[str, Any]]]:
    """응답에서 첫 번째 '레코드 목록' 필드를 찾는다 (TR마다 키 이름이 다름)."""
    for key, value in data.items():
        if isinstance(value, list) and value and isinstance(value[0], dict):
            return key, value
    return None, []


# --------------------------------------------------------------------- 지수


def get_index(client: KiwoomClient, index: str = "kospi") -> str:
    """업종현재가요청(ka20001)으로 지수 현재가를 조회한다."""
    code, label = resolve_index_code(index)
    data = client.request(URL_SECT, "ka20001", {"inds_cd": code})

    mode = _index_scale_mode()
    cur = scale_index(pick(data, "cur_prc", "prst_prc", "now_prc"), mode)
    diff = scale_index(pick(data, "pred_pre", "pre_pre", "prev_pre"), mode)
    rate = parse_num(pick(data, "flu_rt", "pred_pre_rt", "fluc_rt"))
    open_p = scale_index(pick(data, "open_pric", "opn_prc"), mode)
    high_p = scale_index(pick(data, "high_pric", "hgpr"), mode)
    low_p = scale_index(pick(data, "low_pric", "lwpr"), mode)
    volume = parse_num(pick(data, "trde_qty", "trde_qty_now", "acc_trde_qty"))
    value = parse_num(pick(data, "trde_prica", "acc_trde_prica"))

    prev_close = None
    if cur is not None and diff is not None:
        prev_close = cur - diff

    rows = [
        ("지수", f"{label} (업종코드 {code})"),
        ("현재지수", f"{fmt(cur)} {direction(diff)}".strip()),
        ("전일대비", fmt_signed(diff)),
        ("등락률", fmt_signed(rate, 2, " %")),
        ("전일종가", fmt(prev_close)),
        ("시가", fmt(open_p)),
        ("고가", fmt(high_p)),
        ("저가", fmt(low_p)),
        ("거래량", fmt_int(volume, " 주")),
        ("거래대금", fmt_int(value, " 천원")),
    ]
    note = ""
    if mode == "auto":
        note = (
            "\n\n※ 지수 원본값에 소수점이 없으면 100으로 나눠 표시합니다"
            " (키움의 암묵적 2자리 스케일). 값이 100배/1/100배로 어긋나면"
            " 환경변수 KIWOOM_INDEX_SCALE 을 1 또는 100 으로 고정하세요."
        )
    return f"[{label} 현재가]\n{table(rows)}{note}\n\n원본 응답:\n{_raw_block(data)}"


def get_index_daily(client: KiwoomClient, index: str = "kospi", count: int = 10) -> str:
    """업종현재가일별요청(ka20009)으로 지수 일별 추이를 조회한다."""
    code, label = resolve_index_code(index)
    data = client.request(URL_SECT, "ka20009", {"inds_cd": code})
    key, rows_raw = _first_list_of_dicts(data)
    mode = _index_scale_mode()

    lines = []
    for item in rows_raw[: max(1, min(count, 200))]:
        date = pick(item, "dt", "trde_dt", "date", "cntr_dt") or "-"
        close = scale_index(pick(item, "cur_prc", "close_pric", "clpr"), mode)
        diff = scale_index(pick(item, "pred_pre", "pre_pre"), mode)
        rate = parse_num(pick(item, "flu_rt", "pred_pre_rt"))
        vol = parse_num(pick(item, "trde_qty", "acc_trde_qty"))
        lines.append(
            f"{date}  종가 {fmt(close):>12}  대비 {fmt_signed(diff):>10}"
            f"  등락 {fmt_signed(rate, 2, '%'):>9}  거래량 {fmt_int(vol):>15}"
        )

    body = "\n".join(lines) if lines else f"(일별 레코드를 찾지 못했습니다. 응답 키: {list(data)})"
    return (
        f"[{label} 일별 추이] (업종코드 {code}, 목록 필드 {key!r})\n{body}"
        f"\n\n원본 응답:\n{_raw_block(data)}"
    )


def list_index_codes(client: KiwoomClient) -> str:
    """네트워크 호출 없이 사용 가능한 지수 이름/코드를 보여준다."""
    rows = [(name, f"{code}  {label}") for name, (code, label) in INDEX_CODES.items()]
    return "[사용 가능한 지수 지정자]\n" + table(rows) + (
        "\n\n한글 별칭(코스피, 코스닥, 코스피200 …)과 3자리 업종코드도 그대로 씁니다."
    )


# --------------------------------------------------------------------- 종목

_STOCK_CACHE: dict[str, Any] = {"at": 0.0, "items": []}
_STOCK_CACHE_TTL = 3600.0


def _load_stock_list(client: KiwoomClient) -> list[dict[str, Any]]:
    """종목정보리스트(ka10099)를 코스피/코스닥 모두 받아 캐싱한다."""
    now = time.time()
    if _STOCK_CACHE["items"] and now - _STOCK_CACHE["at"] < _STOCK_CACHE_TTL:
        return _STOCK_CACHE["items"]

    items: list[dict[str, Any]] = []
    for market in ("0", "10"):  # 0=코스피, 10=코스닥
        try:
            data = client.request(URL_STKINFO, "ka10099", {"mrkt_tp": market})
        except KiwoomError:
            continue
        _, rows = _first_list_of_dicts(data)
        items.extend(rows)

    if items:
        _STOCK_CACHE["items"] = items
        _STOCK_CACHE["at"] = now
    return items


def search_stock(client: KiwoomClient, query: str, limit: int = 15) -> str:
    """종목명 또는 코드 일부로 종목코드를 찾는다."""
    query = (query or "").strip()
    if not query:
        raise ValueError("검색어가 비어 있습니다.")

    items = _load_stock_list(client)
    if not items:
        return "종목 목록(ka10099)을 받지 못했습니다. 앱키 권한과 서버 구분(real/mock)을 확인하세요."

    needle = query.lower().replace(" ", "")
    exact, partial = [], []
    for item in items:
        code = str(pick(item, "code", "stk_cd", "shrn_iscd") or "")
        name = str(pick(item, "name", "stk_nm", "hts_kor_isnm") or "")
        market = str(pick(item, "marketName", "mrkt_nm", "upName") or "")
        flat = name.lower().replace(" ", "")
        if flat == needle or code == query:
            exact.append((code, name, market))
        elif needle in flat or query in code:
            partial.append((code, name, market))

    hits = (exact + partial)[: max(1, min(limit, 50))]
    if not hits:
        return f"'{query}'와 일치하는 종목이 없습니다. (검색 대상 {len(items):,}종목)"

    rows = [(f"{code}", f"{name}  [{market}]") for code, name, market in hits]
    return f"[종목 검색: {query}] {len(hits)}건\n" + table(rows)


def get_stock_price(client: KiwoomClient, stk_cd: str) -> str:
    """주식기본정보요청(ka10001)으로 종목 현재가와 기본 지표를 조회한다."""
    stk_cd = (stk_cd or "").strip()
    if not stk_cd:
        raise ValueError("종목코드(stk_cd)가 필요합니다. 예: 005930")
    data = client.request(URL_STKINFO, "ka10001", {"stk_cd": stk_cd})

    name = pick(data, "stk_nm", "stk_name", "name") or stk_cd
    cur = parse_num(pick(data, "cur_prc", "prst_prc"))
    diff = parse_num(pick(data, "pred_pre", "pre_pre"))
    rate = parse_num(pick(data, "flu_rt", "pred_pre_rt"))
    prev_close = parse_num(pick(data, "base_pric", "pred_close_pric"))
    if prev_close is None and cur is not None and diff is not None:
        prev_close = cur - diff

    rows = [
        ("종목", f"{name} ({stk_cd})"),
        ("현재가", f"{fmt_int(cur, ' 원')} {direction(diff)}".strip()),
        ("전일대비", fmt_signed(diff, 0, " 원")),
        ("등락률", fmt_signed(rate, 2, " %")),
        ("전일종가", fmt_int(prev_close, " 원")),
        ("시가", fmt_int(parse_num(pick(data, "open_pric", "opn_prc")), " 원")),
        ("고가", fmt_int(parse_num(pick(data, "high_pric", "hgpr")), " 원")),
        ("저가", fmt_int(parse_num(pick(data, "low_pric", "lwpr")), " 원")),
        ("거래량", fmt_int(parse_num(pick(data, "trde_qty", "acc_trde_qty")), " 주")),
        ("거래대금", fmt_int(parse_num(pick(data, "trde_prica", "acc_trde_prica")), " 백만원")),
        ("시가총액", fmt_int(parse_num(pick(data, "mac", "mrkt_cap", "hts_avls")), " 억원")),
        ("PER", fmt(parse_num(pick(data, "per")))),
        ("PBR", fmt(parse_num(pick(data, "pbr")))),
        ("EPS", fmt_int(parse_num(pick(data, "eps")), " 원")),
        ("52주 최고", fmt_int(parse_num(pick(data, "250hgst", "yr_hgst")), " 원")),
        ("52주 최저", fmt_int(parse_num(pick(data, "250lwst", "yr_lwst")), " 원")),
    ]
    return f"[종목 현재가]\n{table(rows)}\n\n원본 응답:\n{_raw_block(data)}"


def get_stock_quote(client: KiwoomClient, stk_cd: str) -> str:
    """주식호가요청(ka10004)으로 호가 잔량을 조회한다."""
    stk_cd = (stk_cd or "").strip()
    if not stk_cd:
        raise ValueError("종목코드(stk_cd)가 필요합니다.")
    data = client.request(URL_MRKCOND, "ka10004", {"stk_cd": stk_cd})
    return f"[호가 {stk_cd}]\n원본 응답:\n{_raw_block(data)}"


def get_stock_daily_chart(
    client: KiwoomClient, stk_cd: str, base_dt: str = "", adjusted: bool = True, count: int = 20
) -> str:
    """주식일봉차트조회요청(ka10081)으로 일봉을 조회한다."""
    stk_cd = (stk_cd or "").strip()
    if not stk_cd:
        raise ValueError("종목코드(stk_cd)가 필요합니다.")
    body = {
        "stk_cd": stk_cd,
        "base_dt": (base_dt or time.strftime("%Y%m%d")),
        "upd_stkpc_tp": "1" if adjusted else "0",
    }
    data = client.request(URL_CHART, "ka10081", body)
    key, rows_raw = _first_list_of_dicts(data)

    lines = []
    for item in rows_raw[: max(1, min(count, 300))]:
        date = pick(item, "dt", "trde_dt", "stck_bsop_date") or "-"
        close = parse_num(pick(item, "cur_prc", "close_pric", "clpr"))
        open_p = parse_num(pick(item, "open_pric", "opn_prc"))
        high = parse_num(pick(item, "high_pric", "hgpr"))
        low = parse_num(pick(item, "low_pric", "lwpr"))
        vol = parse_num(pick(item, "trde_qty", "acc_trde_qty"))
        lines.append(
            f"{date}  시 {fmt_int(open_p):>10}  고 {fmt_int(high):>10}"
            f"  저 {fmt_int(low):>10}  종 {fmt_int(close):>10}  거래량 {fmt_int(vol):>14}"
        )

    body_text = "\n".join(lines) if lines else f"(일봉 레코드 없음. 응답 키: {list(data)})"
    return (
        f"[{stk_cd} 일봉 {'(수정주가)' if adjusted else '(원주가)'}, 목록 필드 {key!r}]\n"
        f"{body_text}\n\n원본 응답:\n{_raw_block(data)}"
    )


def get_top_volume(client: KiwoomClient, market: str = "0", limit: int = 20) -> str:
    """당일거래량상위요청(ka10030)으로 거래량 상위 종목을 조회한다."""
    body = {
        "mrkt_tp": market,       # 0 코스피, 1 코스닥, 2 코스피200
        "sort_tp": "1",          # 1 거래량
        "mang_stk_incls": "0",   # 관리종목 제외
        "crd_tp": "0",
        "trde_qty_tp": "0",
        "pric_tp": "0",
        "trde_prica_tp": "0",
        "mrkt_open_tp": "0",
        "stex_tp": "3",          # 3 통합
    }
    data = client.request(URL_RKINFO, "ka10030", body)
    key, rows_raw = _first_list_of_dicts(data)

    lines = []
    for rank, item in enumerate(rows_raw[: max(1, min(limit, 100))], start=1):
        name = pick(item, "stk_nm", "name") or "-"
        code = pick(item, "stk_cd", "code") or "-"
        cur = parse_num(pick(item, "cur_prc", "prst_prc"))
        rate = parse_num(pick(item, "flu_rt", "pred_pre_rt"))
        vol = parse_num(pick(item, "trde_qty", "now_trde_qty"))
        lines.append(
            f"{rank:>2}. {str(name)[:12]:<12} {str(code):>8}  {fmt_int(cur):>10}원"
            f"  {fmt_signed(rate, 2, '%'):>8}  거래량 {fmt_int(vol):>14}"
        )

    body_text = "\n".join(lines) if lines else f"(순위 레코드 없음. 응답 키: {list(data)})"
    market_name = {"0": "코스피", "1": "코스닥", "2": "코스피200"}.get(market, market)
    return (
        f"[{market_name} 거래량 상위, 목록 필드 {key!r}]\n{body_text}"
        f"\n\n원본 응답:\n{_raw_block(data)}"
    )


# ----------------------------------------------------------------- 진단/원본


def check_connection(client: KiwoomClient) -> str:
    """토큰을 실제로 발급받아 연결과 자격증명을 검증한다."""
    started = time.time()
    client.issue_token()
    elapsed = (time.time() - started) * 1000
    rows = [
        ("서버", f"{client.base_url}  ({'모의투자' if client.is_mock else '실전'})"),
        ("앱키", client.app_key[:4] + "…" + client.app_key[-4:] if len(client.app_key) > 8 else "설정됨"),
        ("토큰 발급", f"성공 ({elapsed:.0f} ms)"),
        ("지수 스케일", _index_scale_mode()),
    ]
    return "[키움 REST API 연결 점검]\n" + table(rows)


def kiwoom_raw(
    client: KiwoomClient,
    api_id: str,
    resource_url: str,
    body: dict[str, Any] | None = None,
    cont_yn: str = "N",
    next_key: str = "",
) -> str:
    """임의의 TR을 그대로 호출한다 (문서에 있는 어떤 api-id든 사용 가능).

    조회 계열 TR만 쓰도록 의도한 탈출구다. 주문/체결 TR(kt1000x 등)은 실제
    주문이 나갈 수 있으므로 서버가 미리 차단한다.
    """
    api_id = (api_id or "").strip()
    if not api_id:
        raise ValueError("api_id가 필요합니다. 예: ka20001")
    if not resource_url.startswith("/api/dostk/"):
        raise ValueError("resource_url은 /api/dostk/ 로 시작해야 합니다.")
    blocked = ("/ordr", "/crdordr")
    if any(resource_url.endswith(suffix) for suffix in blocked):
        raise ValueError(
            f"주문 계열 경로({resource_url})는 이 서버에서 허용하지 않습니다. 조회 TR만 호출하세요."
        )
    data = client.request(resource_url, api_id, body or {}, cont_yn=cont_yn, next_key=next_key)
    return f"[{api_id} @ {resource_url}]\n{_raw_block(data)}"


# ---------------------------------------------------------------- 도구 명세

TOOLS: list[dict[str, Any]] = [
    {
        "name": "get_kospi_index",
        "description": (
            "코스피 등 국내 지수의 현재가를 키움 REST API(업종현재가요청 ka20001)로 조회합니다. "
            "현재지수·전일대비·등락률·시고저·거래량/거래대금을 반환합니다."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "index": {
                    "type": "string",
                    "description": "지수 지정자. kospi, kosdaq, kospi200, 코스피, 코스닥 또는 3자리 업종코드(001 등). 기본값 kospi",
                    "default": "kospi",
                }
            },
        },
        "handler": get_index,
    },
    {
        "name": "get_index_daily",
        "description": "지수의 일별 시세 추이를 조회합니다 (업종현재가일별요청 ka20009).",
        "inputSchema": {
            "type": "object",
            "properties": {
                "index": {"type": "string", "description": "지수 지정자", "default": "kospi"},
                "count": {"type": "integer", "description": "표시할 일수 (기본 10)", "default": 10},
            },
        },
        "handler": get_index_daily,
    },
    {
        "name": "list_index_codes",
        "description": "조회 가능한 지수 이름과 업종코드 목록을 보여줍니다 (네트워크 호출 없음).",
        "inputSchema": {"type": "object", "properties": {}},
        "handler": list_index_codes,
    },
    {
        "name": "search_stock",
        "description": "종목명 또는 코드 일부로 종목코드를 검색합니다 (종목정보리스트 ka10099, 1시간 캐시).",
        "inputSchema": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "검색어. 예: 삼성전자, 005930"},
                "limit": {"type": "integer", "description": "최대 결과 수 (기본 15)", "default": 15},
            },
            "required": ["query"],
        },
        "handler": search_stock,
    },
    {
        "name": "get_stock_price",
        "description": "개별 종목의 현재가와 기본 지표(PER/PBR/시가총액 등)를 조회합니다 (주식기본정보요청 ka10001).",
        "inputSchema": {
            "type": "object",
            "properties": {
                "stk_cd": {"type": "string", "description": "종목코드 6자리. 예: 005930"}
            },
            "required": ["stk_cd"],
        },
        "handler": get_stock_price,
    },
    {
        "name": "get_stock_quote",
        "description": "개별 종목의 호가 잔량을 조회합니다 (주식호가요청 ka10004).",
        "inputSchema": {
            "type": "object",
            "properties": {"stk_cd": {"type": "string", "description": "종목코드 6자리"}},
            "required": ["stk_cd"],
        },
        "handler": get_stock_quote,
    },
    {
        "name": "get_stock_daily_chart",
        "description": "개별 종목의 일봉을 조회합니다 (주식일봉차트조회요청 ka10081).",
        "inputSchema": {
            "type": "object",
            "properties": {
                "stk_cd": {"type": "string", "description": "종목코드 6자리"},
                "base_dt": {"type": "string", "description": "기준일자 YYYYMMDD (기본: 오늘)"},
                "adjusted": {"type": "boolean", "description": "수정주가 반영 여부 (기본 true)", "default": True},
                "count": {"type": "integer", "description": "표시할 봉 개수 (기본 20)", "default": 20},
            },
            "required": ["stk_cd"],
        },
        "handler": get_stock_daily_chart,
    },
    {
        "name": "get_top_volume",
        "description": "당일 거래량 상위 종목을 조회합니다 (당일거래량상위요청 ka10030).",
        "inputSchema": {
            "type": "object",
            "properties": {
                "market": {
                    "type": "string",
                    "description": "시장구분 0=코스피, 1=코스닥, 2=코스피200 (기본 0)",
                    "default": "0",
                },
                "limit": {"type": "integer", "description": "표시할 종목 수 (기본 20)", "default": 20},
            },
        },
        "handler": get_top_volume,
    },
    {
        "name": "check_connection",
        "description": "키움 REST API 연결과 앱키/시크릿키를 점검합니다 (토큰 실제 발급).",
        "inputSchema": {"type": "object", "properties": {}},
        "handler": check_connection,
    },
    {
        "name": "kiwoom_raw",
        "description": (
            "키움 문서에 있는 임의의 조회 TR을 그대로 호출합니다. 위 도구가 못 다루는 "
            "항목이 필요할 때 사용하세요. 주문 계열 경로(/ordr, /crdordr)는 차단됩니다."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "api_id": {"type": "string", "description": "TR 코드. 예: ka20003"},
                "resource_url": {
                    "type": "string",
                    "description": "리소스 경로. 예: /api/dostk/sect, /api/dostk/stkinfo",
                },
                "body": {"type": "object", "description": "요청 바디 (TR별 입력 필드)"},
                "cont_yn": {"type": "string", "description": "연속조회 여부 N/Y", "default": "N"},
                "next_key": {"type": "string", "description": "연속조회 키", "default": ""},
            },
            "required": ["api_id", "resource_url"],
        },
        "handler": kiwoom_raw,
    },
]

HANDLERS: dict[str, Callable[..., str]] = {tool["name"]: tool["handler"] for tool in TOOLS}


def tool_specs() -> list[dict[str, Any]]:
    """MCP tools/list 응답에 넣을 명세 (handler 제거)."""
    return [{k: v for k, v in tool.items() if k != "handler"} for tool in TOOLS]
