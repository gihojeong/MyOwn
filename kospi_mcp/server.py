"""MCP stdio 서버.

Claude 데스크탑 앱이 이 프로세스를 자식으로 띄우고 stdin/stdout으로 줄 단위
JSON-RPC 2.0 메시지를 주고받는다. stdout은 프로토콜 전용이므로 모든 로그는
stderr로만 나가야 한다 — 여기에 print를 하나라도 섞으면 연결이 깨진다.
"""

from __future__ import annotations

import json
import sys
import traceback
from typing import Any, TextIO

from . import __version__
from .kiwoom import KiwoomClient, KiwoomError, client_from_env
from .tools import HANDLERS, tool_specs

SERVER_NAME = "kiwoom-kospi"

#: 우리가 말할 줄 아는 MCP 프로토콜 버전 (최신 우선).
SUPPORTED_PROTOCOLS = ("2025-06-18", "2025-03-26", "2024-11-05")

# JSON-RPC 오류 코드
PARSE_ERROR = -32700
INVALID_REQUEST = -32600
METHOD_NOT_FOUND = -32601
INVALID_PARAMS = -32602
INTERNAL_ERROR = -32603


def log(message: str) -> None:
    print(f"[{SERVER_NAME}] {message}", file=sys.stderr, flush=True)


class Server:
    """MCP 요청을 처리한다. 키움 클라이언트는 첫 호출 때 지연 생성한다."""

    def __init__(self, env: dict[str, str] | None = None) -> None:
        self._env = env
        self._client: KiwoomClient | None = None
        self._client_error: str | None = None

    # ------------------------------------------------------------- 클라이언트

    def client(self) -> KiwoomClient:
        """키움 클라이언트를 얻는다. 자격증명 오류는 도구 호출 시점에 보고된다."""
        if self._client is None:
            self._client = client_from_env(self._env)
        return self._client

    # ------------------------------------------------------------ 메시지 처리

    def handle(self, message: dict[str, Any]) -> dict[str, Any] | None:
        """요청 하나를 처리한다. 알림(id 없음)이면 None을 돌려준다."""
        method = message.get("method")
        msg_id = message.get("id")
        params = message.get("params") or {}
        is_notification = msg_id is None

        if not isinstance(method, str):
            return None if is_notification else _error(msg_id, INVALID_REQUEST, "method가 없습니다.")

        try:
            if method == "initialize":
                result = self._initialize(params)
            elif method in ("notifications/initialized", "initialized", "notifications/cancelled"):
                return None
            elif method == "ping":
                result = {}
            elif method == "tools/list":
                result = {"tools": tool_specs()}
            elif method == "tools/call":
                result = self._call_tool(params)
            elif method in ("resources/list", "prompts/list"):
                # 이 서버는 도구만 제공한다. 빈 목록으로 답해 클라이언트 경고를 막는다.
                result = {"resources": []} if method.startswith("resources") else {"prompts": []}
            else:
                if is_notification:
                    return None
                return _error(msg_id, METHOD_NOT_FOUND, f"지원하지 않는 메서드: {method}")
        except Exception as exc:  # 서버가 죽지 않도록 모든 예외를 JSON-RPC 오류로 환원
            log(f"{method} 처리 중 예외: {exc!r}\n{traceback.format_exc()}")
            if is_notification:
                return None
            return _error(msg_id, INTERNAL_ERROR, str(exc))

        if is_notification:
            return None
        return {"jsonrpc": "2.0", "id": msg_id, "result": result}

    def _initialize(self, params: dict[str, Any]) -> dict[str, Any]:
        requested = params.get("protocolVersion")
        version = requested if requested in SUPPORTED_PROTOCOLS else SUPPORTED_PROTOCOLS[0]
        log(f"initialize (client={params.get('clientInfo')}, protocol={requested} -> {version})")
        return {
            "protocolVersion": version,
            "capabilities": {"tools": {"listChanged": False}},
            "serverInfo": {"name": SERVER_NAME, "version": __version__},
        }

    def _call_tool(self, params: dict[str, Any]) -> dict[str, Any]:
        name = params.get("name")
        arguments = params.get("arguments") or {}
        handler = HANDLERS.get(name)
        if handler is None:
            return _tool_error(f"알 수 없는 도구: {name}")
        if not isinstance(arguments, dict):
            return _tool_error("arguments는 객체여야 합니다.")

        try:
            text = handler(self.client(), **arguments)
        except TypeError as exc:
            return _tool_error(f"인자가 잘못되었습니다: {exc}")
        except ValueError as exc:
            return _tool_error(str(exc))
        except KiwoomError as exc:
            detail = f" (return_code={exc.code})" if exc.code is not None else ""
            return _tool_error(f"키움 API 오류{detail}: {exc.message}")
        except Exception as exc:  # 예상 못 한 오류도 도구 오류로 돌려준다
            log(f"도구 {name} 실행 중 예외:\n{traceback.format_exc()}")
            return _tool_error(f"{type(exc).__name__}: {exc}")

        return {"content": [{"type": "text", "text": text}], "isError": False}


def _error(msg_id: Any, code: int, message: str) -> dict[str, Any]:
    return {"jsonrpc": "2.0", "id": msg_id, "error": {"code": code, "message": message}}


def _tool_error(message: str) -> dict[str, Any]:
    return {"content": [{"type": "text", "text": message}], "isError": True}


def serve(stdin: TextIO | None = None, stdout: TextIO | None = None) -> int:
    """stdio 루프. EOF까지 줄 단위 JSON-RPC를 처리한다."""
    stdin = stdin or sys.stdin
    stdout = stdout or sys.stdout
    server = Server()
    log(f"v{__version__} 시작 — stdio 대기 중")

    for line in stdin:
        line = line.strip()
        if not line:
            continue
        try:
            message = json.loads(line)
        except ValueError:
            _write(stdout, _error(None, PARSE_ERROR, "JSON 파싱 실패"))
            continue

        if isinstance(message, list):  # 배치 요청
            responses = [r for r in (server.handle(m) for m in message if isinstance(m, dict)) if r]
            for response in responses:
                _write(stdout, response)
            continue
        if not isinstance(message, dict):
            _write(stdout, _error(None, INVALID_REQUEST, "요청은 객체여야 합니다."))
            continue

        response = server.handle(message)
        if response is not None:
            _write(stdout, response)

    log("stdin 종료 — 서버를 닫습니다")
    return 0


def _write(stdout: TextIO, payload: dict[str, Any]) -> None:
    stdout.write(json.dumps(payload, ensure_ascii=False) + "\n")
    stdout.flush()


def main() -> int:
    try:
        return serve()
    except KeyboardInterrupt:
        return 0
