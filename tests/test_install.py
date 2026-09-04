"""Claude 데스크탑 설정 병합 테스트."""

from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from kospi_mcp.install import SERVER_KEY, build_entry, config_path, install  # noqa: E402

LAUNCHER = Path(__file__).resolve().parent.parent / "kospi_mcp_server.py"


class InstallTest(unittest.TestCase):
    def test_config_path_is_absolute(self):
        self.assertTrue(config_path().is_absolute())
        self.assertEqual(config_path().name, "claude_desktop_config.json")

    def test_entry_uses_absolute_paths(self):
        entry = build_entry(LAUNCHER, "K", "S", "real")
        self.assertTrue(Path(entry["command"]).is_absolute() or entry["command"] == "python3")
        self.assertTrue(Path(entry["args"][0]).is_absolute())
        self.assertEqual(entry["env"]["KIWOOM_APP_KEY"], "K")
        self.assertEqual(entry["env"]["KIWOOM_ENV"], "real")

    def test_creates_config_when_absent(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "Claude" / "claude_desktop_config.json"
            install(LAUNCHER, "K", "S", "mock", target)
            config = json.loads(target.read_text(encoding="utf-8"))
            self.assertEqual(config["mcpServers"][SERVER_KEY]["env"]["KIWOOM_ENV"], "mock")
            self.assertEqual(target.stat().st_mode & 0o777, 0o600)

    def test_merges_and_backs_up_existing_config(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "claude_desktop_config.json"
            target.write_text(
                json.dumps({"mcpServers": {"filesystem": {"command": "npx"}}, "theme": "dark"}),
                encoding="utf-8",
            )
            install(LAUNCHER, "K", "S", "real", target)
            config = json.loads(target.read_text(encoding="utf-8"))

            # 기존 서버와 다른 설정이 보존되어야 한다.
            self.assertEqual(config["mcpServers"]["filesystem"]["command"], "npx")
            self.assertEqual(config["theme"], "dark")
            self.assertIn(SERVER_KEY, config["mcpServers"])
            self.assertTrue(target.with_suffix(".json.bak").is_file())

    def test_reinstall_overwrites_only_own_entry(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "claude_desktop_config.json"
            install(LAUNCHER, "OLD", "S", "real", target)
            install(LAUNCHER, "NEW", "S", "mock", target)
            config = json.loads(target.read_text(encoding="utf-8"))
            self.assertEqual(config["mcpServers"][SERVER_KEY]["env"]["KIWOOM_APP_KEY"], "NEW")
            self.assertEqual(len(config["mcpServers"]), 1)

    def test_invalid_existing_json_aborts(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "claude_desktop_config.json"
            target.write_text("{ broken", encoding="utf-8")
            with self.assertRaises(SystemExit):
                install(LAUNCHER, "K", "S", "real", target)


if __name__ == "__main__":
    unittest.main()
