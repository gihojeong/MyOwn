"""MCP stdio 서버 프로토콜 테스트 (실제 stdin/stdout 왕복 포함)."""

from __future__ import annotations

import io
import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from kospi_mcp import kiwoom, server, tools  # noqa: E402
from kospi_mcp.server import Server, serve  # noqa: E402
from tests.test_kiwoom import TOKEN_OK, FakeTransport  # noqa: E402

# 테스트는 사용자 홈의 토큰 캐시를 건드리지 않는다.
CREDS = {
    "KIWOOM_APP_KEY": "KEY",
    "KIWOOM_APP_SECRET": "SECRET",
    "KIWOOM_ENV": "mock",
    "KIWOOM_TOKEN_CACHE": "none",
}


def request(method, params=None, msg_id=1):
    msg = {"jsonrpc": "2.0", "method": method}
    if msg_id is not None:
        msg["id"] = msg_id
    if params is not None:
        msg["params"] = params
    return msg


class ProtocolTest(unittest.TestCase):
    def setUp(self):
        self.server = Server(env=dict(CREDS))

    def test_initialize_echoes_supported_protocol(self):
        resp = self.server.handle(
            request("initialize", {"protocolVersion": "2024-11-05", "clientInfo": {"name": "claude"}})
        )
        result = resp["result"]
        self.assertEqual(result["protocolVersion"], "2024-11-05")
        self.assertIn("tools", result["capabilities"])
        self.assertEqual(result["serverInfo"]["name"], "kiwoom-kospi")

    def test_initialize_falls_back_for_unknown_protocol(self):
        resp = self.server.handle(request("initialize", {"protocolVersion": "1999-01-01"}))
        self.assertEqual(resp["result"]["protocolVersion"], server.SUPPORTED_PROTOCOLS[0])

    def test_notification_gets_no_response(self):
        self.assertIsNone(self.server.handle(request("notifications/initialized", msg_id=None)))
        self.assertIsNone(self.server.handle(request("unknown/method", msg_id=None)))

    def test_tools_list(self):
        resp = self.server.handle(request("tools/list"))
        names = {t["name"] for t in resp["result"]["tools"]}
        self.assertIn("get_kospi_index", names)
        self.assertIn("search_stock", names)
        self.assertEqual(names, set(tools.HANDLERS))

    def test_ping_and_empty_lists(self):
        self.assertEqual(self.server.handle(request("ping"))["result"], {})
        self.assertEqual(self.server.handle(request("resources/list"))["result"], {"resources": []})
        self.assertEqual(self.server.handle(request("prompts/list"))["result"], {"prompts": []})

    def test_unknown_method_is_error(self):
        resp = self.server.handle(request("does/not/exist"))
        self.assertEqual(resp["error"]["code"], server.METHOD_NOT_FOUND)

    def test_unknown_tool_is_tool_error(self):
        resp = self.server.handle(request("tools/call", {"name": "nope", "arguments": {}}))
        self.assertTrue(resp["result"]["isError"])
        self.assertIn("알 수 없는 도구", resp["result"]["content"][0]["text"])

    def test_bad_argument_is_reported_not_raised(self):
        resp = self.server.handle(
            request("tools/call", {"name": "get_kospi_index", "arguments": {"nope": 1}})
        )
        self.assertTrue(resp["result"]["isError"])
        self.assertIn("인자가 잘못되었습니다", resp["result"]["content"][0]["text"])

    def test_missing_credentials_reported_as_tool_error(self):
        bare = Server(env={"KIWOOM_APP_KEY": "", "KIWOOM_APP_SECRET": "", "KIWOOM_TOKEN_CACHE": "none"})
        resp = bare.handle(request("tools/call", {"name": "check_connection", "arguments": {}}))
        self.assertTrue(resp["result"]["isError"])
        self.assertIn("KIWOOM_APP_KEY", resp["result"]["content"][0]["text"])

    def test_kiwoom_error_surfaces_return_code(self):
        orig = kiwoom.http_post_json
        kiwoom.http_post_json = FakeTransport(
            [TOKEN_OK, (200, {"return_code": 3, "return_msg": "일시적 오류"})]
        )
        try:
            resp = self.server.handle(
                request("tools/call", {"name": "get_kospi_index", "arguments": {"index": "kospi"}})
            )
        finally:
            kiwoom.http_post_json = orig
        text = resp["result"]["content"][0]["text"]
        self.assertTrue(resp["result"]["isError"])
        self.assertIn("return_code=3", text)
        self.assertIn("일시적 오류", text)


class StdioRoundTripTest(unittest.TestCase):
    """실제 serve() 루프를 가짜 stdin/stdout으로 한 번 돌린다."""

    def setUp(self):
        self._orig_post = kiwoom.http_post_json
        self._orig_interval = kiwoom.MIN_INTERVAL_PER_TR
        self._orig_env = {k: __import__("os").environ.get(k) for k in CREDS}
        kiwoom.MIN_INTERVAL_PER_TR = 0.0
        import os

        os.environ.update(CREDS)

    def tearDown(self):
        import os

        kiwoom.http_post_json = self._orig_post
        kiwoom.MIN_INTERVAL_PER_TR = self._orig_interval
        for key, value in self._orig_env.items():
            if value is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = value

    def test_full_session(self):
        kiwoom.http_post_json = FakeTransport(
            [
                TOKEN_OK,
                (200, {"return_code": 0, "cur_prc": "252050", "pred_pre": "+1320",
                       "flu_rt": "+0.53", "trde_qty": "412356789"}),
            ]
        )
        lines = [
            json.dumps(request("initialize", {"protocolVersion": "2025-06-18"}, 1)),
            json.dumps(request("notifications/initialized", msg_id=None)),
            json.dumps(request("tools/list", msg_id=2)),
            json.dumps(request("tools/call", {"name": "get_kospi_index", "arguments": {}}, 3)),
        ]
        stdin = io.StringIO("\n".join(lines) + "\n")
        stdout = io.StringIO()
        stderr = io.StringIO()
        real_stderr, sys.stderr = sys.stderr, stderr
        try:
            self.assertEqual(serve(stdin, stdout), 0)
        finally:
            sys.stderr = real_stderr

        responses = [json.loads(line) for line in stdout.getvalue().splitlines() if line.strip()]
        # 알림에는 응답하지 않으므로 3건이어야 한다.
        self.assertEqual([r["id"] for r in responses], [1, 2, 3])
        self.assertEqual(responses[0]["result"]["protocolVersion"], "2025-06-18")
        self.assertGreater(len(responses[1]["result"]["tools"]), 5)
        text = responses[2]["result"]["content"][0]["text"]
        self.assertFalse(responses[2]["result"]["isError"])
        self.assertIn("2,520.50", text)
        # stdout은 프로토콜 전용 — 로그는 stderr로만 나가야 한다.
        self.assertIn("stdio 대기 중", stderr.getvalue())

    def test_malformed_line_gets_parse_error(self):
        stdin = io.StringIO("{not json}\n")
        stdout = io.StringIO()
        real_stderr, sys.stderr = sys.stderr, io.StringIO()
        try:
            serve(stdin, stdout)
        finally:
            sys.stderr = real_stderr
        resp = json.loads(stdout.getvalue().strip())
        self.assertEqual(resp["error"]["code"], server.PARSE_ERROR)


if __name__ == "__main__":
    unittest.main()
