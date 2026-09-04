"""도구 핸들러와 포맷 헬퍼 테스트."""

from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from kospi_mcp import kiwoom, tools  # noqa: E402
from kospi_mcp.format import (  # noqa: E402
    parse_num,
    resolve_index_code,
    scale_index,
    table,
)
from kospi_mcp.kiwoom import KiwoomClient  # noqa: E402
from tests.test_kiwoom import TOKEN_OK, FakeTransport  # noqa: E402


class FormatTest(unittest.TestCase):
    def test_resolve_index_code(self):
        self.assertEqual(resolve_index_code("kospi")[0], "001")
        self.assertEqual(resolve_index_code("코스피")[0], "001")
        self.assertEqual(resolve_index_code("KOSPI200")[0], "201")
        self.assertEqual(resolve_index_code("101")[0], "101")
        self.assertEqual(resolve_index_code("999")[0], "999")
        with self.assertRaises(ValueError):
            resolve_index_code("nasdaq")

    def test_parse_num(self):
        self.assertEqual(parse_num("+2,350"), 2350.0)
        self.assertEqual(parse_num("-1.25"), -1.25)
        self.assertEqual(parse_num(42), 42.0)
        for empty in ("", "-", None, "abc"):
            self.assertIsNone(parse_num(empty))

    def test_scale_index_auto(self):
        # 소수점이 없으면 암묵적 2자리 스케일로 본다.
        self.assertAlmostEqual(scale_index("252050"), 2520.50)
        # 이미 소수점이 있으면 그대로 쓴다.
        self.assertAlmostEqual(scale_index("2520.50"), 2520.50)
        self.assertAlmostEqual(scale_index("-1320"), -13.20)
        # 명시 모드
        self.assertAlmostEqual(scale_index("252050", "1"), 252050.0)
        self.assertAlmostEqual(scale_index("2520.50", "100"), 25.205)
        self.assertIsNone(scale_index(None))

    def test_table_aligns_hangul(self):
        # 한글은 2칸으로 세므로 문자 인덱스가 아니라 표시 폭으로 정렬된다.
        from kospi_mcp.format import _display_width

        rendered = table([("현재지수", "2,520.50"), ("PER", "12.3")])
        first, second = rendered.splitlines()
        self.assertEqual(
            _display_width(first.split(":")[0]), _display_width(second.split(":")[0])
        )


class ToolTest(unittest.TestCase):
    def setUp(self):
        self._orig_post = kiwoom.http_post_json
        self._orig_interval = kiwoom.MIN_INTERVAL_PER_TR
        kiwoom.MIN_INTERVAL_PER_TR = 0.0
        tools._STOCK_CACHE.update({"at": 0.0, "items": []})

    def tearDown(self):
        kiwoom.http_post_json = self._orig_post
        kiwoom.MIN_INTERVAL_PER_TR = self._orig_interval

    def client(self, responses):
        kiwoom.http_post_json = FakeTransport([TOKEN_OK] + list(responses))
        return KiwoomClient("KEY", "SECRET", cache_token=False)

    def test_get_index_summary(self):
        client = self.client(
            [
                (
                    200,
                    {
                        "return_code": 0,
                        "cur_prc": "252050",
                        "pred_pre": "+1320",
                        "flu_rt": "+0.53",
                        "open_pric": "251000",
                        "high_pric": "253100",
                        "low_pric": "250400",
                        "trde_qty": "412356789",
                        "trde_prica": "9876543",
                    },
                )
            ]
        )
        out = tools.get_index(client, "코스피")
        self.assertIn("코스피 종합 (업종코드 001)", out)
        self.assertIn("2,520.50", out)      # 현재지수
        self.assertIn("+13.20", out)        # 전일대비
        self.assertIn("+0.53 %", out)       # 등락률
        self.assertIn("2,507.30", out)      # 전일종가 = 2520.50 - 13.20
        self.assertIn("412,356,789 주", out)
        self.assertIn("원본 응답:", out)

    def test_get_index_rejects_unknown_name(self):
        client = self.client([])
        with self.assertRaises(ValueError):
            tools.get_index(client, "nikkei")

    def test_get_stock_price_summary(self):
        client = self.client(
            [
                (
                    200,
                    {
                        "return_code": 0,
                        "stk_nm": "삼성전자",
                        "cur_prc": "+75600",
                        "pred_pre": "+1200",
                        "flu_rt": "+1.61",
                        "per": "13.42",
                        "pbr": "1.28",
                    },
                )
            ]
        )
        out = tools.get_stock_price(client, "005930")
        self.assertIn("삼성전자 (005930)", out)
        self.assertIn("75,600 원", out)
        self.assertIn("+1,200 원", out)
        self.assertIn("13.42", out)

    def test_get_stock_price_requires_code(self):
        with self.assertRaises(ValueError):
            tools.get_stock_price(self.client([]), "  ")

    def test_search_stock_matches_name(self):
        listing = {
            "return_code": 0,
            "list": [
                {"code": "005930", "name": "삼성전자", "marketName": "거래소"},
                {"code": "005935", "name": "삼성전자우", "marketName": "거래소"},
                {"code": "000660", "name": "SK하이닉스", "marketName": "거래소"},
            ],
        }
        client = self.client([(200, listing), (200, {"return_code": 0, "list": []})])
        out = tools.search_stock(client, "삼성전자")
        self.assertIn("005930", out)
        self.assertIn("005935", out)
        self.assertNotIn("SK하이닉스", out)
        # 정확 일치가 앞에 온다.
        self.assertLess(out.index("005930"), out.index("005935"))

    def test_search_stock_uses_cache(self):
        listing = {"return_code": 0, "list": [{"code": "005930", "name": "삼성전자"}]}
        transport = FakeTransport([TOKEN_OK, (200, listing), (200, {"return_code": 0})])
        kiwoom.http_post_json = transport
        client = KiwoomClient("KEY", "SECRET", cache_token=False)
        tools.search_stock(client, "삼성")
        before = len(transport.calls)
        tools.search_stock(client, "전자")  # 캐시 적중 -> 추가 호출 없음
        self.assertEqual(len(transport.calls), before)

    def test_index_daily_lists_rows(self):
        client = self.client(
            [
                (
                    200,
                    {
                        "return_code": 0,
                        "inds_cur_prc_daly_rept": [
                            {"dt": "20260904", "cur_prc": "252050", "pred_pre": "+1320",
                             "flu_rt": "+0.53", "trde_qty": "412356789"},
                            {"dt": "20260903", "cur_prc": "250730", "pred_pre": "-880",
                             "flu_rt": "-0.35", "trde_qty": "398112004"},
                        ],
                    },
                )
            ]
        )
        out = tools.get_index_daily(client, "kospi", count=5)
        self.assertIn("20260904", out)
        self.assertIn("2,520.50", out)
        self.assertIn("2,507.30", out)

    def test_kiwoom_raw_blocks_order_paths(self):
        client = self.client([])
        with self.assertRaises(ValueError):
            tools.kiwoom_raw(client, "kt10000", "/api/dostk/ordr", {})
        with self.assertRaises(ValueError):
            tools.kiwoom_raw(client, "ka20001", "https://evil.example/api", {})
        with self.assertRaises(ValueError):
            tools.kiwoom_raw(client, "", "/api/dostk/sect", {})

    def test_kiwoom_raw_passes_through(self):
        client = self.client([(200, {"return_code": 0, "hello": "world"})])
        out = tools.kiwoom_raw(client, "ka20003", "/api/dostk/sect", {"idx_tp": "0"})
        self.assertIn("ka20003 @ /api/dostk/sect", out)
        self.assertIn('"hello": "world"', out)

    def test_list_index_codes_needs_no_network(self):
        out = tools.list_index_codes(self.client([]))
        self.assertIn("kospi200", out)
        self.assertIn("201", out)

    def test_tool_specs_are_valid_json_schema_shape(self):
        specs = tools.tool_specs()
        self.assertEqual(len(specs), len(tools.TOOLS))
        for spec in specs:
            self.assertNotIn("handler", spec)
            self.assertIn(spec["name"], tools.HANDLERS)
            self.assertTrue(spec["description"])
            self.assertEqual(spec["inputSchema"]["type"], "object")
            json.dumps(spec)  # 직렬화 가능해야 한다


if __name__ == "__main__":
    unittest.main()
