"""키움 응답 필드를 사람이 읽을 수 있는 요약으로 바꾸는 헬퍼.

키움은 숫자를 문자열로 주고, 부호를 앞에 붙인다("+2350", "-1.25"). 지수값은
소수점을 생략한 정수로 오는 경우가 있어(252050 = 2520.50) 배율 보정이 필요하다.
"""

from __future__ import annotations

from typing import Any, Iterable

#: 업종(지수) 코드. 키움 업종코드 체계 기준.
INDEX_CODES: dict[str, tuple[str, str]] = {
    "kospi": ("001", "코스피 종합"),
    "kospi_large": ("002", "코스피 대형주"),
    "kospi_mid": ("003", "코스피 중형주"),
    "kospi_small": ("004", "코스피 소형주"),
    "kosdaq": ("101", "코스닥 종합"),
    "kospi200": ("201", "코스피200"),
    "kospi100": ("202", "코스피100"),
    "kospi50": ("203", "코스피50"),
    "krx100": ("701", "KRX100"),
}

#: 별칭 -> 표준 키
INDEX_ALIASES: dict[str, str] = {
    "코스피": "kospi",
    "종합": "kospi",
    "kospi종합": "kospi",
    "코스닥": "kosdaq",
    "코스피200": "kospi200",
    "k200": "kospi200",
    "코스피100": "kospi100",
    "코스피50": "kospi50",
    "대형주": "kospi_large",
    "중형주": "kospi_mid",
    "소형주": "kospi_small",
}


def resolve_index_code(name: str) -> tuple[str, str]:
    """'kospi' / '코스피' / '001' 등을 (업종코드, 표시이름)으로 정규화한다."""
    key = (name or "kospi").strip().lower().replace(" ", "")
    key = INDEX_ALIASES.get(key, key)
    if key in INDEX_CODES:
        return INDEX_CODES[key]
    if key.isdigit():
        for code, label in INDEX_CODES.values():
            if code == key:
                return code, label
        return key, f"업종코드 {key}"
    raise ValueError(
        f"알 수 없는 지수 이름: {name!r}. 사용 가능: "
        + ", ".join(sorted(INDEX_CODES)) + " 또는 3자리 업종코드"
    )


def parse_num(raw: Any) -> float | None:
    """'+2,350' -> 2350.0. 해석 불가면 None."""
    if raw is None:
        return None
    if isinstance(raw, (int, float)):
        return float(raw)
    text = str(raw).strip().replace(",", "").replace(" ", "")
    if not text or text in ("-", "+"):
        return None
    negative = text.startswith("-")
    text = text.lstrip("+-")
    if not text:
        return None
    try:
        value = float(text)
    except ValueError:
        return None
    return -value if negative else value


def scale_index(raw: Any, mode: str = "auto") -> float | None:
    """지수 원본값을 실제 지수 포인트로 환산한다.

    mode="auto"  소수점이 없으면 100으로 나눈다 (키움의 암묵적 2자리 스케일).
    mode="100"   항상 100으로 나눈다.
    mode="1"     원본 그대로 쓴다.
    """
    if raw is None:
        return None
    text = str(raw).strip()
    value = parse_num(text)
    if value is None:
        return None
    if mode == "1":
        return value
    if mode == "100":
        return value / 100.0
    return value if "." in text else value / 100.0


def pick(data: dict[str, Any], *names: str) -> Any:
    """후보 키 중 처음으로 값이 있는 것을 돌려준다 (TR별 필드명 차이 흡수)."""
    for name in names:
        value = data.get(name)
        if value not in (None, "", "-"):
            return value
    return None


def fmt(value: float | None, digits: int = 2, unit: str = "") -> str:
    if value is None:
        return "-"
    return f"{value:,.{digits}f}{unit}"


def fmt_signed(value: float | None, digits: int = 2, unit: str = "") -> str:
    if value is None:
        return "-"
    return f"{value:+,.{digits}f}{unit}"


def fmt_int(value: float | None, unit: str = "") -> str:
    if value is None:
        return "-"
    return f"{int(round(value)):,}{unit}"


def direction(value: float | None) -> str:
    if value is None:
        return ""
    if value > 0:
        return "▲"
    if value < 0:
        return "▼"
    return "―"


def table(rows: Iterable[tuple[str, str]]) -> str:
    """(항목, 값) 목록을 정렬된 텍스트 표로 만든다."""
    rows = [(k, v) for k, v in rows if v not in ("", None)]
    if not rows:
        return "(표시할 항목 없음)"
    width = max(_display_width(k) for k, _ in rows)
    return "\n".join(
        f"{k}{' ' * (width - _display_width(k))} : {v}" for k, v in rows
    )


def _display_width(text: str) -> int:
    """한글을 2칸으로 세어 표 정렬을 맞춘다."""
    return sum(2 if ord(ch) > 0x2E80 else 1 for ch in text)
