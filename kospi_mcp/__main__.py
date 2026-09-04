"""CLI 진입점.

  python3 kospi_mcp_server.py            # MCP stdio 서버 (Claude 앱이 이렇게 실행)
  python3 kospi_mcp_server.py check      # 자격증명/연결 점검
  python3 kospi_mcp_server.py kospi      # 코스피 현재가 한 번 조회
  python3 kospi_mcp_server.py stock 005930
  python3 kospi_mcp_server.py tools      # 등록된 도구 목록
  python3 kospi_mcp_server.py install    # Claude 데스크탑 설정에 등록
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from . import __version__


def _client():
    from .kiwoom import client_from_env

    return client_from_env()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="kospi-mcp", description="키움 REST API용 MCP 서버 (Claude 데스크탑 앱 연동)"
    )
    parser.add_argument("--version", action="version", version=f"kospi-mcp {__version__}")
    sub = parser.add_subparsers(dest="command")

    sub.add_parser("serve", help="MCP stdio 서버 실행 (기본값)")
    sub.add_parser("check", help="토큰 발급으로 연결/자격증명 점검")
    sub.add_parser("tools", help="등록된 MCP 도구 목록 출력")

    p_index = sub.add_parser("kospi", help="지수 현재가 조회")
    p_index.add_argument("index", nargs="?", default="kospi", help="기본 kospi")

    p_stock = sub.add_parser("stock", help="종목 현재가 조회")
    p_stock.add_argument("stk_cd", help="종목코드 6자리. 예: 005930")

    p_search = sub.add_parser("search", help="종목명으로 코드 검색")
    p_search.add_argument("query")

    p_install = sub.add_parser("install", help="Claude 데스크탑 설정에 이 서버를 등록")
    p_install.add_argument("--app-key", help="키움 앱키 (생략 시 입력 프롬프트)")
    p_install.add_argument("--app-secret", help="키움 시크릿키 (생략 시 입력 프롬프트)")
    p_install.add_argument(
        "--env", dest="env_mode", default="real", choices=["real", "mock"], help="기본 real"
    )
    p_install.add_argument("--config", help="설정 파일 경로를 직접 지정")

    args = parser.parse_args(argv)
    command = args.command or "serve"

    if command == "serve":
        from .server import main as serve_main

        return serve_main()

    if command == "tools":
        from .tools import tool_specs

        for spec in tool_specs():
            print(f"- {spec['name']}: {spec['description']}")
        return 0

    if command == "install":
        return _install(args)

    # 아래 명령은 실제 API 호출이 필요하다.
    from .kiwoom import KiwoomError

    try:
        client = _client()
        if command == "check":
            from .tools import check_connection

            print(check_connection(client))
        elif command == "kospi":
            from .tools import get_index

            print(get_index(client, args.index))
        elif command == "stock":
            from .tools import get_stock_price

            print(get_stock_price(client, args.stk_cd))
        elif command == "search":
            from .tools import search_stock

            print(search_stock(client, args.query))
        else:
            parser.print_help()
            return 2
    except KiwoomError as exc:
        print(f"오류: {exc}", file=sys.stderr)
        return 1
    return 0


def _install(args: argparse.Namespace) -> int:
    from getpass import getpass

    from .install import config_path, install

    app_key = args.app_key or input("키움 앱키(App Key): ").strip()
    app_secret = args.app_secret or getpass("키움 시크릿키(Secret Key, 화면에 표시되지 않음): ").strip()
    if not app_key or not app_secret:
        print("앱키와 시크릿키가 모두 필요합니다.", file=sys.stderr)
        return 1

    launcher = Path(__file__).resolve().parent.parent / "kospi_mcp_server.py"
    if not launcher.is_file():
        print(f"실행 스크립트를 찾을 수 없습니다: {launcher}", file=sys.stderr)
        return 1

    target = Path(args.config).expanduser() if args.config else config_path()
    written = install(launcher, app_key, app_secret, args.env_mode, target)
    print(f"설정을 저장했습니다: {written}")
    print("Claude 데스크탑 앱을 완전히 종료했다가 다시 실행하면 도구가 나타납니다.")
    return 0
