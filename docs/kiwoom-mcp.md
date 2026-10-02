# 키움 MCP (local stdio) — 설치·운영 메모

공식 가이드: <https://github.com/Kiwoom-Securities/Kiwoom-REST-API/blob/main/SETUP-MCP.md>

한 줄 요약: **`bash scripts/setup_kiwoom_mcp.sh` 하나로 끝난다. 멱등이므로 몇 번 돌려도 안전하다.**
검증은 `python3 scripts/verify_kiwoom_mcp.py` — `tools/list`가 통과해야 설치 완료다.

---

## 1. 서버 둘

| server | 무엇 | 앱 키 | tools |
| --- | --- | --- | --- |
| `kiwoom-spec` | API 명세 검색·예제 조회 | **불필요** | `spec_search` `spec_show` `spec_groups` `get_example` |
| `kiwoom-exec` | 시세·계좌 조회 | 조회 시 필요 | `kiwoom_commands` `kiwoom_help` `kiwoom_query` |

주문 도구(`kiwoom_order_preview` / `kiwoom_order_submit`)는 **꺼진 상태로 설치**한다.
켜려면 `~/.claude.json`의 `mcpServers["kiwoom-exec"].env`에
`"KIWOOM_MCP_ALLOW_ORDERS": "1"`을 직접 추가한다. **값이 정확히 `1`일 때만** 켜진다
(`true`/`yes`는 무효 — 오타로 주문이 열리지 않게 설계돼 있다).
자동 승인 모드(`permission_mode=auto`)로 도는 세션에서는 켜지 말 것 — 마지막 안전장치가 도구 실행 승인 화면이다.

## 2. 앱 키는 파일에 쓰지 않는다

가이드 Step 9.1은 config에 값을 직접 넣게 하지만, 이 저장소는 **Step 9.2(환경변수 참조)** 를 쓴다.
Claude Code는 `${...}` 확장을 지원하므로 config에는 참조만 남는다.

```json
"env": { "APP_KEY": "${APP_KEY}", "APP_SECRET": "${APP_SECRET}", "KIWOOM_MODE": "demo" }
```

값은 **환경 설정**에 둔다 — 세션 제목줄의 클라우드 환경 메뉴 → **Edit** → `API credentials`
(없으면 환경변수)에 `APP_KEY` `APP_SECRET` `KRX_AUTH_KEY` `ECOS_API_KEY` `KIWOOM_MODE`.
자세한 건 `docs/setup.md`. **키 값을 대화창에 붙여넣지 말 것.**

`KIWOOM_MODE`는 `demo`(모의)·`real`(실전)이며 **둘은 서로 다른 키**다. 섞이면 `8030`이 뜬다.

## 3. 검증 — `tools/list`까지 가야 완료

아래는 **성공 근거가 아니다**: clone 성공 / sync 성공 / config 생성 / 서버 이름 표시 / 프로세스 기동.

```bash
python3 scripts/verify_kiwoom_mcp.py
```

`initialize` → `tools/list` → tools 배열이 두 서버 모두 떠야 PASS다.
이 스크립트는 `~/.claude.json`에 기록된 `command`/`args`를 **그대로 읽어** 쓴다(가이드 Step 10.1).
`tools/call`은 호출하지 않는다 — 조회도 주문도 하지 않는다(Rule 19).
`kiwoom-exec` 검증에는 앱 키가 **필요 없다**. 서버는 키 없이 기동하고 자격증명은 실제 조회 시점에만 쓴다.

## 4. 클라우드 세션에서의 한계 — 읽고 기대치를 맞출 것

### 4.1 컨테이너는 매번 새로 뜬다
`~/.claude.json`과 `~/.local/share/mcp/`는 **세션 종료 시 사라진다.** 그래서 새 세션마다
`scripts/setup_kiwoom_mcp.sh`를 한 번 돌려야 한다. 첫 실행은 Python 3.13 + 의존성
약 140MB를 받아 **수 분** 걸린다. 두 번째부터는 venv를 재사용해 즉시 끝난다.

### 4.2 같은 세션에서는 도구가 바로 안 붙는다
MCP 서버는 **세션 기동 시점**에 연결된다. 스크립트를 돌린 그 세션에서는 `mcp__kiwoom_*`
도구가 아직 목록에 없을 수 있다. 설치는 **다음 세션부터** 효과가 난다.
→ 그래서 `.mcp.json`을 저장소에 두더라도 **발행 회차(06:00/18:05)에서 즉시 쓸 수는 없다.**

### 4.3 ★MCP는 자격증명 간헐 실패를 고치지 못한다★
`kiwoom-exec`도 `kiwoom_collect.py`와 **똑같이** `APP_KEY`/`APP_SECRET`을 쓴다.
컨테이너에 환경변수가 비어 들어오면 MCP도 같이 실패한다. 키가 필요 없는
`kiwoom-spec`만 항상 동작한다.

실측 이력 (같은 환경 `env_013CTT1sL1S2pkCrCzotsqAj`, 단일 환경):

| 일시 (KST) | 회차 | APP_KEY 주입 |
| --- | --- | --- |
| 2026-09-28 06:09 | 개장 전 | ✗ 비어 있음 |
| 2026-09-29 06:41 | 개장 전(수동) | ○ `token_issued=true`, 77/81 |
| 2026-09-30 05:31 | Top50 | ○ 308/313 |
| 2026-10-02 05:23 | Top50 | ○ 281/285 |
| **2026-10-02 06:17** | **개장 전** | **✗ 비어 있음 → 미가동** |
| 2026-10-02 22:05 | 수동 | ○ `token_issued=true` |

같은 날 아침 **54분 차이**로 한 세션은 받고 한 세션은 못 받았다.
환경은 하나뿐이고 루틴별 환경 차이는 MCP 커넥터·알림 채널뿐이므로 **"다른 루틴의 환경을
이식"하는 경로는 존재하지 않는다.** 원인은 컨테이너 기동 시 시크릿 주입의 간헐 실패다.

**완화책**: 자격증명이 비면 같은 날 먼저 돌아간 **Top50 회차(05:2x)의 수집기 산출물**을
Drive·Gmail에서 읽어 쓴다. 2026-09-30 개장 전 회차에서 이 경로로 약 20분을 절약했다.
`docs/collection-contract.md`의 폴백 절을 따른다.

## 5. 수집기와 MCP 중 무엇을 쓸 것인가

| | `scripts/kiwoom_collect.py` | 키움 MCP |
| --- | --- | --- |
| 용도 | **발행 회차의 정규 경로** | 임시 조회·명세 확인 |
| 범위 | 프리셋 81~313항목 일괄 | 호출당 1건 |
| 속도 | 2~6분에 전량 | 질의당 수 초, 설치에 수 분 |
| 세션 즉시성 | 즉시 | 다음 세션부터 |

→ **발행 회차의 수집 경로를 MCP로 바꾸지 않는다.** 수집 계약서(`docs/collection-contract.md`)가
정본이고 MCP는 그 위의 보조 도구다. MCP가 실제로 이기는 자리는 두 곳이다.

- `kiwoom-spec`: 수집기에 새 TR을 붙일 때 명세·예제를 찾는 용도. **앱 키가 없어도 된다.**
- `kiwoom_query`: 회차 밖에서 한두 종목만 확인할 때.
