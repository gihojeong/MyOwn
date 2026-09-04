"""Claude 데스크탑 앱의 claude_desktop_config.json에 이 MCP 서버를 등록한다."""

from __future__ import annotations

import json
import os
import platform
import shutil
import sys
from pathlib import Path
from typing import Any

SERVER_KEY = "kiwoom-kospi"


def config_path() -> Path:
    """OS별 Claude 데스크탑 설정 파일 경로."""
    system = platform.system()
    if system == "Darwin":
        return Path.home() / "Library" / "Application Support" / "Claude" / "claude_desktop_config.json"
    if system == "Windows":
        appdata = os.environ.get("APPDATA") or str(Path.home() / "AppData" / "Roaming")
        return Path(appdata) / "Claude" / "claude_desktop_config.json"
    # Linux 데스크탑 빌드
    return Path.home() / ".config" / "Claude" / "claude_desktop_config.json"


def python_command() -> str:
    """서버를 띄울 파이썬 실행 파일의 절대경로.

    Claude 데스크탑은 사용자의 셸 PATH를 상속하지 않는 경우가 많아 'python3'
    같은 이름만 적으면 실행에 실패한다. 절대경로를 쓴다.
    """
    return sys.executable or shutil.which("python3") or "python3"


def build_entry(launcher: Path, app_key: str, app_secret: str, env_mode: str) -> dict[str, Any]:
    return {
        "command": python_command(),
        "args": [str(launcher.resolve())],
        "env": {
            "KIWOOM_APP_KEY": app_key,
            "KIWOOM_APP_SECRET": app_secret,
            "KIWOOM_ENV": env_mode,
        },
    }


def install(
    launcher: Path,
    app_key: str,
    app_secret: str,
    env_mode: str = "real",
    target: Path | None = None,
) -> Path:
    """설정 파일을 읽어 mcpServers에 항목을 병합하고 저장한다. 백업을 남긴다."""
    path = target or config_path()
    path.parent.mkdir(parents=True, exist_ok=True)

    config: dict[str, Any] = {}
    if path.is_file():
        raw = path.read_text(encoding="utf-8").strip()
        if raw:
            try:
                config = json.loads(raw)
            except ValueError as exc:
                raise SystemExit(
                    f"기존 설정 파일이 올바른 JSON이 아닙니다: {path}\n  {exc}\n"
                    "직접 고친 뒤 다시 실행하세요."
                ) from exc
        backup = path.with_suffix(path.suffix + ".bak")
        shutil.copy2(path, backup)

    if not isinstance(config, dict):
        raise SystemExit(f"설정 파일의 최상위가 객체가 아닙니다: {path}")

    servers = config.setdefault("mcpServers", {})
    if not isinstance(servers, dict):
        raise SystemExit("설정 파일의 mcpServers가 객체가 아닙니다.")

    servers[SERVER_KEY] = build_entry(launcher, app_key, app_secret, env_mode)
    path.write_text(json.dumps(config, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    try:
        os.chmod(path, 0o600)  # 앱키가 평문으로 들어가므로 권한을 조인다.
    except OSError:
        pass
    return path
