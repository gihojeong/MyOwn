"""키움증권 REST API 클라이언트 (표준 라이브러리만 사용).

프로토콜 요약
-------------
* 실전  https://api.kiwoom.com   / 모의 https://mockapi.kiwoom.com
* 토큰  POST /oauth2/token  {"grant_type":"client_credentials","appkey":..,"secretkey":..}
        -> {"token": "...", "expires_dt": "yyyyMMddHHmmss", "return_code": 0}
* TR    POST <resource_url>  헤더 authorization / api-id / cont-yn / next-key
        -> 본문에 return_code(0=정상), return_msg 와 TR별 응답 필드
"""

from __future__ import annotations

import hashlib
import json
import os
import ssl
import threading
import time
import urllib.error
import urllib.request
from datetime import datetime
from pathlib import Path
from typing import Any

PROD_URL = "https://api.kiwoom.com"
MOCK_URL = "https://mockapi.kiwoom.com"

TOKEN_PATH = "/oauth2/token"
REVOKE_PATH = "/oauth2/revoke"

#: 토큰 만료 이 초 전이면 미리 재발급한다.
EXPIRY_MARGIN = 60.0

#: 키움은 api-id(TR) 단위로 초당 호출을 제한한다. 여유 있게 1초 간격을 둔다.
MIN_INTERVAL_PER_TR = 1.0

USER_AGENT = "kospi-mcp/0.1 (+https://github.com/gihojeong/MyOwn)"


class KiwoomError(Exception):
    """키움 API 호출 실패. `code`/`message`/`payload`에 원인이 담긴다."""

    def __init__(self, message: str, code: Any = None, payload: Any = None) -> None:
        super().__init__(message)
        self.code = code
        self.message = message
        self.payload = payload


class AuthError(KiwoomError):
    """토큰 발급 실패 (앱키/시크릿키 또는 서버 구분이 잘못된 경우)."""


def _ssl_context() -> ssl.SSLContext:
    """기본 검증을 켠 SSL 컨텍스트. 사내 프록시용 CA 번들만 선택적으로 얹는다."""
    ca_bundle = os.environ.get("KIWOOM_CA_BUNDLE") or os.environ.get("REQUESTS_CA_BUNDLE")
    if ca_bundle and Path(ca_bundle).is_file():
        return ssl.create_default_context(cafile=ca_bundle)
    return ssl.create_default_context()


def http_post_json(
    url: str, headers: dict[str, str], payload: dict[str, Any], timeout: float = 20.0
) -> tuple[int, dict[str, str], str]:
    """POST 한 번. (status, 응답헤더, 본문문자열)을 그대로 돌려준다.

    HTTPError도 예외로 던지지 않고 상태코드와 본문으로 환원한다 — 키움은 4xx
    응답 본문에 return_msg를 담아 보내므로 그 메시지가 진단에 필요하다.
    """
    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(url, data=data, method="POST")
    req.add_header("Content-Type", "application/json;charset=UTF-8")
    req.add_header("User-Agent", USER_AGENT)
    for key, value in headers.items():
        req.add_header(key, value)

    try:
        with urllib.request.urlopen(req, timeout=timeout, context=_ssl_context()) as resp:
            return resp.status, {k.lower(): v for k, v in resp.headers.items()}, resp.read().decode(
                "utf-8", "replace"
            )
    except urllib.error.HTTPError as exc:  # 4xx/5xx
        body = exc.read().decode("utf-8", "replace") if exc.fp else ""
        return exc.code, {k.lower(): v for k, v in (exc.headers or {}).items()}, body


def _parse_expiry(data: dict[str, Any]) -> float | None:
    """expires_dt(yyyyMMddHHmmss, 로컬시각) 또는 expires_in(초) -> unix timestamp."""
    expires_dt = data.get("expires_dt")
    if expires_dt:
        try:
            return datetime.strptime(str(expires_dt), "%Y%m%d%H%M%S").timestamp()
        except (ValueError, TypeError):
            pass
    expires_in = data.get("expires_in")
    if expires_in is not None:
        try:
            return time.time() + float(expires_in)
        except (ValueError, TypeError):
            pass
    return None


class _TokenStore:
    """토큰을 디스크에 캐싱한다 (0600). 앱키/서버가 바뀌면 자동 무효화."""

    def __init__(self, app_key: str, base_url: str, path: Path | None = None) -> None:
        self.path = path or Path.home() / ".kospi-mcp" / "token.json"
        self.fingerprint = hashlib.sha256(
            f"{app_key}|{base_url}".encode("utf-8")
        ).hexdigest()[:16]

    def load(self) -> tuple[str, float | None] | None:
        try:
            data = json.loads(self.path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            return None
        if data.get("fingerprint") != self.fingerprint:
            return None
        token = data.get("token")
        if not token:
            return None
        return token, data.get("expires_at")

    def save(self, token: str, expires_at: float | None) -> None:
        try:
            self.path.parent.mkdir(parents=True, exist_ok=True)
            tmp = self.path.with_suffix(".tmp")
            tmp.write_text(
                json.dumps(
                    {
                        "fingerprint": self.fingerprint,
                        "token": token,
                        "expires_at": expires_at,
                    }
                ),
                encoding="utf-8",
            )
            os.chmod(tmp, 0o600)
            tmp.replace(self.path)
        except OSError:
            pass  # 캐시는 최적화일 뿐이므로 실패해도 조용히 넘어간다.

    def clear(self) -> None:
        try:
            self.path.unlink()
        except OSError:
            pass


class KiwoomClient:
    """토큰 관리 + TR 호출 + 호출 간격 제어를 담당하는 동기 클라이언트.

    Args:
        app_key: 키움 REST API 앱키.
        app_secret: 시크릿키.
        is_mock: True면 모의투자 서버(mockapi)를 쓴다.
        base_url: 직접 지정할 경우의 베이스 URL (테스트용).
        cache_token: 토큰을 홈 디렉터리에 캐싱할지 여부.
    """

    def __init__(
        self,
        app_key: str,
        app_secret: str,
        *,
        is_mock: bool = False,
        base_url: str | None = None,
        timeout: float = 20.0,
        cache_token: bool = True,
        token_path: Path | None = None,
    ) -> None:
        if not app_key or not app_secret:
            raise AuthError(
                "앱키/시크릿키가 없습니다. 환경변수 KIWOOM_APP_KEY, KIWOOM_APP_SECRET을 설정하세요."
            )
        self.app_key = app_key
        self.app_secret = app_secret
        self.is_mock = is_mock
        self.base_url = (base_url or (MOCK_URL if is_mock else PROD_URL)).rstrip("/")
        self.timeout = timeout

        self._lock = threading.Lock()
        self._token: str | None = None
        self._expires_at: float | None = None
        self._last_call: dict[str, float] = {}
        self._store = _TokenStore(app_key, self.base_url, token_path) if cache_token else None

        if self._store:
            cached = self._store.load()
            if cached:
                self._token, self._expires_at = cached

    # ------------------------------------------------------------------ 토큰

    def _token_expiring(self) -> bool:
        if self._token is None:
            return True
        if self._expires_at is None:
            return False  # 만료시각을 모르면 401이 뜰 때 갱신한다.
        return time.time() >= self._expires_at - EXPIRY_MARGIN

    def issue_token(self) -> str:
        """새 토큰을 발급받아 캐시한다."""
        status, _, body = http_post_json(
            self.base_url + TOKEN_PATH,
            {},
            {
                "grant_type": "client_credentials",
                "appkey": self.app_key,
                "secretkey": self.app_secret,
            },
            self.timeout,
        )
        try:
            data = json.loads(body) if body else {}
        except ValueError:
            raise AuthError(f"토큰 응답을 해석할 수 없습니다 (HTTP {status}): {body[:200]}") from None

        token = data.get("token") or data.get("access_token")
        if status != 200 or not token:
            msg = data.get("return_msg") or data.get("message") or body[:200] or "알 수 없는 오류"
            raise AuthError(
                f"토큰 발급 실패 (HTTP {status}): {msg}",
                code=data.get("return_code", status),
                payload=data,
            )

        self._token = token
        self._expires_at = _parse_expiry(data)
        if self._store:
            self._store.save(token, self._expires_at)
        return token

    def get_token(self) -> str:
        with self._lock:
            if self._token_expiring():
                return self.issue_token()
            assert self._token is not None
            return self._token

    def invalidate_token(self) -> None:
        with self._lock:
            self._token = None
            self._expires_at = None
            if self._store:
                self._store.clear()

    def revoke_token(self) -> None:
        """서버 측 토큰을 폐기한다 (선택)."""
        if not self._token:
            return
        http_post_json(
            self.base_url + REVOKE_PATH,
            {},
            {"appkey": self.app_key, "secretkey": self.app_secret, "token": self._token},
            self.timeout,
        )
        self.invalidate_token()

    # ------------------------------------------------------------------ 호출

    def _throttle(self, api_id: str) -> None:
        """같은 TR을 연속 호출할 때 최소 간격을 지킨다."""
        last = self._last_call.get(api_id)
        if last is not None:
            wait = MIN_INTERVAL_PER_TR - (time.monotonic() - last)
            if wait > 0:
                time.sleep(wait)
        self._last_call[api_id] = time.monotonic()

    def request(
        self,
        resource_url: str,
        api_id: str,
        body: dict[str, Any] | None = None,
        *,
        cont_yn: str = "N",
        next_key: str = "",
        max_retries: int = 3,
    ) -> dict[str, Any]:
        """TR 하나를 호출하고 파싱된 응답 dict를 돌려준다.

        401은 토큰 재발급 후 1회 재시도하고, 429/5xx/네트워크 오류는 지수
        백오프로 재시도한다. return_code가 0이 아니면 KiwoomError를 던진다.
        """
        url = self.base_url + resource_url
        payload = dict(body or {})
        retried_auth = False
        delay = 1.0

        for attempt in range(max_retries):
            self._throttle(api_id)
            headers = {
                "authorization": f"Bearer {self.get_token()}",
                "api-id": api_id,
                "cont-yn": cont_yn,
                "next-key": next_key,
            }
            try:
                status, resp_headers, text = http_post_json(url, headers, payload, self.timeout)
            except (urllib.error.URLError, OSError) as exc:
                if attempt == max_retries - 1:
                    raise KiwoomError(f"네트워크 오류: {exc}") from exc
                time.sleep(delay)
                delay *= 2
                continue

            if status in (401, 403) and not retried_auth:
                retried_auth = True
                self.invalidate_token()
                continue

            if status == 429 or status >= 500:
                if attempt == max_retries - 1:
                    raise KiwoomError(f"HTTP {status}: {text[:200]}", code=status)
                time.sleep(delay)
                delay *= 2
                continue

            try:
                data = json.loads(text) if text else {}
            except ValueError:
                raise KiwoomError(f"응답 JSON 파싱 실패 (HTTP {status}): {text[:200]}") from None

            if not isinstance(data, dict):
                raise KiwoomError(f"예상치 못한 응답 형태: {type(data).__name__}", payload=data)

            return_code = data.get("return_code", 0)
            if return_code not in (0, "0", None):
                raise KiwoomError(
                    data.get("return_msg") or f"TR {api_id} 실패 (return_code={return_code})",
                    code=return_code,
                    payload=data,
                )
            if status != 200:
                raise KiwoomError(f"HTTP {status}: {text[:200]}", code=status, payload=data)

            # 연속조회 키는 헤더로 오는 경우와 본문으로 오는 경우가 모두 있다.
            data.setdefault("cont_yn", resp_headers.get("cont-yn", "N"))
            data.setdefault("next_key", resp_headers.get("next-key", ""))
            return data

        raise KiwoomError(f"TR {api_id} 호출이 {max_retries}회 모두 실패했습니다.")


def client_from_env(env: dict[str, str] | None = None) -> KiwoomClient:
    """환경변수에서 자격증명을 읽어 클라이언트를 만든다.

    KIWOOM_APP_KEY, KIWOOM_APP_SECRET, KIWOOM_ENV(real|mock), KIWOOM_BASE_URL,
    KIWOOM_TOKEN_CACHE(캐시 파일 경로, "none"이면 캐시 끔).
    """
    src = os.environ if env is None else env
    mode = (src.get("KIWOOM_ENV") or "real").strip().lower()
    if mode not in ("real", "prod", "production", "mock", "paper", "sim"):
        raise AuthError(f"KIWOOM_ENV 값이 잘못되었습니다: {mode!r} (real 또는 mock)")

    cache_setting = (src.get("KIWOOM_TOKEN_CACHE") or "").strip()
    cache_token = cache_setting.lower() != "none"
    token_path = Path(cache_setting).expanduser() if cache_token and cache_setting else None

    return KiwoomClient(
        app_key=(src.get("KIWOOM_APP_KEY") or "").strip(),
        app_secret=(src.get("KIWOOM_APP_SECRET") or "").strip(),
        is_mock=mode in ("mock", "paper", "sim"),
        base_url=(src.get("KIWOOM_BASE_URL") or "").strip() or None,
        cache_token=cache_token,
        token_path=token_path,
    )
