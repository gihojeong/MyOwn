# -*- coding: utf-8 -*-
"""Step 10 검증: MCP initialize -> tools/list -> tools 배열.
config(~/.claude.json)에 기록된 command/args를 그대로 읽어 쓴다(Step 10.1).
tools/call 은 호출하지 않는다(Rule 19)."""
import json, os, subprocess, sys

CFG = os.path.expanduser("~/.claude.json")
servers = json.load(open(CFG, encoding="utf-8"))["mcpServers"]
EXPECTED = {"kiwoom-spec": "spec_search", "kiwoom-exec": "kiwoom_query"}

def frame(obj):
    return json.dumps(obj, ensure_ascii=False) + "\n"

def run(name):
    s = servers[name]
    # exec 검증에는 env(앱 키) 불필요 — Step 10.1
    env = dict(os.environ)
    env.pop("APP_KEY", None); env.pop("APP_SECRET", None)
    msgs = (
        frame({"jsonrpc": "2.0", "id": 1, "method": "initialize",
               "params": {"protocolVersion": "2024-11-05",
                          "capabilities": {},
                          "clientInfo": {"name": "setup-verify", "version": "1.0"}}})
        + frame({"jsonrpc": "2.0", "method": "notifications/initialized"})
        + frame({"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}})
    )
    p = subprocess.run([s["command"]] + s["args"], input=msgs, capture_output=True,
                       text=True, timeout=240, env=env)
    init_ok, tools = False, None
    for line in p.stdout.splitlines():
        line = line.strip()
        if not line.startswith("{"):
            continue
        try:
            m = json.loads(line)
        except Exception:
            continue
        if m.get("id") == 1 and "result" in m:
            init_ok = True
            sv = m["result"].get("serverInfo", {})
            print("   initialize    : OK  protocol=%s server=%s %s"
                  % (m["result"].get("protocolVersion"), sv.get("name"), sv.get("version", "")))
        if m.get("id") == 2:
            if "result" in m:
                tools = m["result"].get("tools")
            else:
                print("   tools/list    : ERROR", json.dumps(m.get("error"), ensure_ascii=False)[:200])
    if tools is None:
        print("   tools/list    : 응답 없음 (exit=%s)" % p.returncode)
        print("   stderr        :", (p.stderr or "")[-500:])
        return False
    names = [t.get("name") for t in tools]
    print("   tools/list    : OK  tools %d개" % len(tools))
    print("   tools         :", ", ".join(names[:12]) + (" ..." if len(names) > 12 else ""))
    exp = EXPECTED[name]
    print("   EXPECTED_TOOL : %s -> %s" % (exp, "있음" if exp in names else "★없음★"))
    return init_ok and bool(tools) and exp in names

ok = True
for name in ("kiwoom-spec", "kiwoom-exec"):
    print("=== %s ===" % name)
    try:
        ok &= run(name)
    except subprocess.TimeoutExpired:
        print("   TIMEOUT"); ok = False
    except Exception as e:
        print("   EXCEPTION:", e); ok = False
    print()
print("설치 검증:", "PASS — 두 서버 모두 initialize + tools/list 성공" if ok else "FAIL")
sys.exit(0 if ok else 1)
