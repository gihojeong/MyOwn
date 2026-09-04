#!/usr/bin/env python3
"""키움 REST API MCP 서버 실행 스크립트.

Claude 데스크탑 앱의 claude_desktop_config.json이 이 파일의 절대경로를 가리킨다.
패키지 경로를 직접 잡아주므로 PYTHONPATH나 가상환경 설정이 필요 없다.

  python3 kospi_mcp_server.py            # MCP stdio 서버
  python3 kospi_mcp_server.py check      # 연결 점검
  python3 kospi_mcp_server.py install    # 데스크탑 앱에 등록
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from kospi_mcp.__main__ import main  # noqa: E402

if __name__ == "__main__":
    raise SystemExit(main())
