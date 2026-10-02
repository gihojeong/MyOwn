#!/usr/bin/env bash
# 키움 MCP(local stdio) 부트스트랩 — 멱등. 이미 설치돼 있으면 아무것도 하지 않는다.
#
# 공식 가이드: https://github.com/Kiwoom-Securities/Kiwoom-REST-API/blob/main/SETUP-MCP.md
# 이 스크립트는 그 문서의 Step 0·3·5·7.2를 비대화형으로 재현한다.
#
# 서버 둘:
#   kiwoom-spec  API 명세 검색·예제 조회      앱 키 불필요
#   kiwoom-exec  시세·계좌 조회               조회 시 APP_KEY/APP_SECRET 필요
#
# 주문 도구는 켜지 않는다. 켜려면 ~/.claude.json 의 kiwoom-exec.env 에
# "KIWOOM_MCP_ALLOW_ORDERS": "1" 을 직접 추가한다(정확히 "1"일 때만 켜짐).
#
# ★앱 키는 이 스크립트가 절대 기록하지 않는다. config 에는 ${APP_KEY} 참조만 넣고
#  값은 환경(세션 제목줄 → 클라우드 환경 → Edit)에 둔다. docs/setup.md 참조.
set -euo pipefail

REPO_URL="https://github.com/Kiwoom-Securities/Kiwoom-REST-API"
MCP_HOME="${MCP_HOME:-$HOME/.local/share/mcp}"
REPO_PATH="$MCP_HOME/Kiwoom-REST-API"
CFG="${CLAUDE_CONFIG:-$HOME/.claude.json}"

log() { printf '[kiwoom-mcp] %s\n' "$*"; }

# ── Step 0: uv ────────────────────────────────────────────────────────────────
UV="$(command -v uv || true)"
[ -n "$UV" ] || { [ -x "$HOME/.local/bin/uv" ] && UV="$HOME/.local/bin/uv"; }
if [ -z "${UV:-}" ]; then
  log "uv 없음 → 설치"
  curl -LsSf https://astral.sh/uv/install.sh | sh >/dev/null 2>&1 || {
    log "ERROR: uv 설치 실패(네트워크 차단 가능). 중단."; exit 1; }
  UV="$HOME/.local/bin/uv"
fi
[ -x "$UV" ] || { log "ERROR: uv 실행 불가: $UV"; exit 1; }
log "uv = $UV ($("$UV" --version 2>/dev/null || echo '?'))"

command -v git >/dev/null || { log "ERROR: git 없음"; exit 1; }

# ── Step 3: clone (기존 저장소는 건드리지 않는다) ──────────────────────────────
if [ -d "$REPO_PATH/.git" ]; then
  log "저장소 존재 → clone 생략: $REPO_PATH"
else
  log "clone → $REPO_PATH"
  mkdir -p "$MCP_HOME"
  git clone --depth 1 "$REPO_URL" "$REPO_PATH" >/dev/null 2>&1 || {
    log "ERROR: clone 실패. 중단."; exit 1; }
fi
for d in mcp_spec mcp_exec; do
  [ -f "$REPO_PATH/$d/uv.lock" ] || { log "ERROR: $d/uv.lock 없음"; exit 1; }
done

# ── Step 5: 의존성 (Python 3.13 + 약 140MB. 첫 실행만 수 분) ───────────────────
for d in mcp_spec mcp_exec; do
  if [ -x "$REPO_PATH/$d/.venv/bin/python" ]; then
    log "$d venv 존재 → sync 생략"
  else
    log "$d sync (수 분 소요)"
    "$UV" sync --frozen --directory "$REPO_PATH/$d" >/dev/null 2>&1 || {
      log "ERROR: $d sync 실패"; exit 1; }
  fi
done

# ── Step 7.2 + Step 8: ~/.claude.json 에 두 항목만 upsert ─────────────────────
UV="$UV" REPO_PATH="$REPO_PATH" CFG="$CFG" python3 <<'PY'
import json, os, shutil
cfg_path = os.environ["CFG"]; uv = os.environ["UV"]; repo = os.environ["REPO_PATH"]
defs = {
    "kiwoom-spec": {"type": "stdio", "command": uv,
        "args": ["run", "--frozen", "--directory", repo + "/mcp_spec", "kiwoom-spec-mcp"]},
    "kiwoom-exec": {"type": "stdio", "command": uv,
        "args": ["run", "--frozen", "--directory", repo + "/mcp_exec", "kiwoom-exec-mcp"],
        # Step 9.2 — 값이 아니라 환경변수 참조. 파일에 키를 쓰지 않는다.
        "env": {"APP_KEY": "${APP_KEY}", "APP_SECRET": "${APP_SECRET}",
                "KIWOOM_MODE": os.environ.get("KIWOOM_MODE_DEFAULT", "demo")}},
}
if os.path.exists(cfg_path):
    cfg = json.loads(open(cfg_path, encoding="utf-8").read())
    shutil.copy2(cfg_path, cfg_path + ".bak-kiwoom-mcp")
else:
    cfg = {}
before = sorted(cfg.keys())
cfg.setdefault("mcpServers", {}).update(defs)
out = json.dumps(cfg, ensure_ascii=False, indent=2)
json.loads(out)                                   # syntax 검증
open(cfg_path, "w", encoding="utf-8").write(out)
again = json.loads(open(cfg_path, encoding="utf-8").read())
for k in before:
    assert k in again, "기존 키 소실: " + k        # 비파괴 확인
assert set(again["mcpServers"]) >= set(defs)
print("[kiwoom-mcp] config OK: %s (mcpServers=%s)"
      % (cfg_path, ", ".join(sorted(again["mcpServers"]))))
PY

log "완료. 검증: python3 scripts/verify_kiwoom_mcp.py"
log "주의: MCP 서버는 세션 기동 시 연결된다 — 이 스크립트를 처음 돌린 세션에서는"
log "      아직 도구가 안 보일 수 있다. 다음 세션부터 붙는다."
