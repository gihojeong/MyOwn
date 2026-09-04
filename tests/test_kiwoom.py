"""KiwoomClient 단위 테스트. 실제 네트워크 대신 가짜 전송 계층을 끼운다."""

from __future__ import annotations

import json
import sys
import time
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from kospi_mcp import kiwoom  # noqa: E402
from kospi_mcp.kiwoom import AuthError, KiwoomClient, KiwoomError  # noqa: E402


class FakeTransport:
    """http_post_json 대체물. 호출을 기록하고 미리 정한 응답을 돌려준다."""

    def __init__(self, responses):
        self.responses = list(responses)
        self.calls = []

    def __call__(self, url, headers, payload, timeout=20.0):
        self.calls.append({"url": url, "headers": headers, "payload": payload})
        if not self.responses:
            raise AssertionError(f"예상보다 많은 호출: {url}")
        status, body = self.responses.pop(0)
        return status, {}, json.dumps(body, ensure_ascii=False)


TOKEN_OK = (200, {"token": "TKN-1", "expires_dt": "20991231235959", "return_code": 0})


class KiwoomClientTest(unittest.TestCase):
    def setUp(self):
        self._orig_post = kiwoom.http_post_json
        self._orig_interval = kiwoom.MIN_INTERVAL_PER_TR
        kiwoom.MIN_INTERVAL_PER_TR = 0.0  # 테스트에서 호출 간격 대기 제거

    def tearDown(self):
        kiwoom.http_post_json = self._orig_post
        kiwoom.MIN_INTERVAL_PER_TR = self._orig_interval

    def client(self, transport, **kwargs):
        kiwoom.http_post_json = transport
        return KiwoomClient("KEY", "SECRET", cache_token=False, **kwargs)

    def test_missing_credentials_raises(self):
        with self.assertRaises(AuthError):
            KiwoomClient("", "", cache_token=False)

    def test_base_url_follows_env(self):
        self.assertEqual(
            KiwoomClient("a", "b", cache_token=False).base_url, kiwoom.PROD_URL
        )
        self.assertEqual(
            KiwoomClient("a", "b", is_mock=True, cache_token=False).base_url, kiwoom.MOCK_URL
        )

    def test_token_issued_once_and_reused(self):
        transport = FakeTransport([TOKEN_OK, (200, {"return_code": 0, "cur_prc": "1"}),
                                   (200, {"return_code": 0, "cur_prc": "2"})])
        client = self.client(transport)
        client.request("/api/dostk/sect", "ka20001", {"inds_cd": "001"})
        client.request("/api/dostk/sect", "ka20001", {"inds_cd": "001"})
        token_calls = [c for c in transport.calls if c["url"].endswith("/oauth2/token")]
        self.assertEqual(len(token_calls), 1, "토큰은 한 번만 발급되어야 한다")
        self.assertEqual(
            token_calls[0]["payload"],
            {"grant_type": "client_credentials", "appkey": "KEY", "secretkey": "SECRET"},
        )

    def test_tr_headers(self):
        transport = FakeTransport([TOKEN_OK, (200, {"return_code": 0})])
        client = self.client(transport)
        client.request("/api/dostk/sect", "ka20001", {"inds_cd": "001"}, next_key="NK", cont_yn="Y")
        tr_call = transport.calls[-1]
        self.assertEqual(tr_call["url"], kiwoom.PROD_URL + "/api/dostk/sect")
        self.assertEqual(tr_call["headers"]["authorization"], "Bearer TKN-1")
        self.assertEqual(tr_call["headers"]["api-id"], "ka20001")
        self.assertEqual(tr_call["headers"]["cont-yn"], "Y")
        self.assertEqual(tr_call["headers"]["next-key"], "NK")
        self.assertEqual(tr_call["payload"], {"inds_cd": "001"})

    def test_nonzero_return_code_raises(self):
        transport = FakeTransport([TOKEN_OK, (200, {"return_code": 3, "return_msg": "권한 없음"})])
        client = self.client(transport)
        with self.assertRaises(KiwoomError) as ctx:
            client.request("/api/dostk/sect", "ka20001", {})
        self.assertEqual(ctx.exception.code, 3)
        self.assertIn("권한 없음", str(ctx.exception))

    def test_401_triggers_reissue_and_retry(self):
        transport = FakeTransport(
            [
                TOKEN_OK,
                (401, {"return_msg": "만료된 토큰"}),
                (200, {"token": "TKN-2", "expires_dt": "20991231235959", "return_code": 0}),
                (200, {"return_code": 0, "cur_prc": "252050"}),
            ]
        )
        client = self.client(transport)
        data = client.request("/api/dostk/sect", "ka20001", {})
        self.assertEqual(data["cur_prc"], "252050")
        self.assertEqual(transport.calls[-1]["headers"]["authorization"], "Bearer TKN-2")

    def test_bad_credentials_message(self):
        transport = FakeTransport([(401, {"return_code": 8, "return_msg": "유효하지 않은 appkey"})])
        client = self.client(transport)
        with self.assertRaises(AuthError) as ctx:
            client.request("/api/dostk/sect", "ka20001", {})
        self.assertIn("유효하지 않은 appkey", str(ctx.exception))

    def test_expiry_parsing(self):
        self.assertIsNone(kiwoom._parse_expiry({}))
        self.assertAlmostEqual(
            kiwoom._parse_expiry({"expires_in": 3600}), time.time() + 3600, delta=5
        )
        self.assertIsInstance(kiwoom._parse_expiry({"expires_dt": "20301231235959"}), float)

    def test_token_cache_roundtrip(self):
        import tempfile

        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "token.json"
            transport = FakeTransport([TOKEN_OK, (200, {"return_code": 0})])
            kiwoom.http_post_json = transport
            first = KiwoomClient("KEY", "SECRET", token_path=path)
            first.request("/api/dostk/sect", "ka20001", {})

            # 새 인스턴스는 캐시에서 토큰을 읽어 재발급하지 않아야 한다.
            transport2 = FakeTransport([(200, {"return_code": 0})])
            kiwoom.http_post_json = transport2
            second = KiwoomClient("KEY", "SECRET", token_path=path)
            second.request("/api/dostk/sect", "ka20001", {})
            self.assertFalse(
                [c for c in transport2.calls if c["url"].endswith("/oauth2/token")],
                "캐시된 토큰이 있으면 재발급하지 않는다",
            )
            self.assertEqual(path.stat().st_mode & 0o777, 0o600)

    def test_client_from_env(self):
        client = kiwoom.client_from_env(
            {"KIWOOM_APP_KEY": "k", "KIWOOM_APP_SECRET": "s", "KIWOOM_ENV": "mock"}
        )
        self.assertTrue(client.is_mock)
        with self.assertRaises(AuthError):
            kiwoom.client_from_env({"KIWOOM_APP_KEY": "k", "KIWOOM_APP_SECRET": "s",
                                    "KIWOOM_ENV": "실전"})


if __name__ == "__main__":
    unittest.main()
