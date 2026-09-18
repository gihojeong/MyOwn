# -*- coding: utf-8 -*-
import re, sys
h = open("kospi_close_20260918.html", encoding="utf-8").read()

fails = []
# 1) 금지 문자열
BAN = ['<style','var(--','class="','display:grid','inline-block','@media','<svg','http',
       '<script','border-radius','<!DOCTYPE','href="#','<html','<head','<body','&nbsp;&nbsp;&nbsp;']
for b in BAN:
    n = h.count(b)
    if b == '&nbsp;&nbsp;&nbsp;':
        continue
    if n: fails.append("금지문자열 %r %d건" % (b, n))
print("[1] 금지문자열 %d종 검사 -> %s" % (len(BAN)-1, "0건" if not fails else "FAIL"))

# 2) 태그 개폐 균형
print("[2] 태그 개폐 균형")
for t in ["table","tr","td","div","font","b","span"]:
    o = len(re.findall(r"<%s[\s>]" % t, h)); cl = len(re.findall(r"</%s>" % t, h))
    ok = (o == cl)
    if not ok: fails.append("태그 불균형 %s %d/%d" % (t, o, cl))
    print("    %-6s open %4d / close %4d  %s" % (t, o, cl, "OK" if ok else "★FAIL"))

# 3) 부호-기호-색상 일치
pat = re.compile(r'<font color="?(#[0-9a-fA-F]{6})"?>\s*(▲|▼|―)\s*([^<]*)')
pairs = m = 0
for col_, sym, txt in pat.findall(h):
    if col_ not in ("#d03b3b", "#2a78d6", "#555555"): continue
    num = re.search(r'[-−+]?\d[\d,]*\.?\d*', txt)
    if not num: continue
    pairs += 1
    s = num.group(0)
    neg = s.startswith("-") or s.startswith("−")
    pos = s.startswith("+")
    bad = False
    if sym == "▲" and (neg or col_ != "#d03b3b"): bad = True
    if sym == "▼" and (pos or col_ != "#2a78d6"): bad = True
    if sym == "―" and col_ != "#555555": bad = True
    if bad:
        m += 1; fails.append("부호/기호/색 불일치: %s %s %s" % (col_, sym, txt[:30]))
print("[3] 부호-기호-색상 검사: %d쌍 검사, 불일치 %d건" % (pairs, m))
assert pairs > 0, "★검사 대상이 0이면 통과가 아니라 검사 실패다"

# 3b) 포맷을 거치지 않은 리터럴 %% 누출
dbl = h.count("%%")
print("[3b] 리터럴 '%%' 누출: %d건 (0이어야 함)" % dbl)
if dbl: fails.append("리터럴 %%%% 누출 %d건" % dbl)

# 4) 당일 종가 표 안의 과거 일자 문자열
past = re.findall(r'20260917|20260916|2026-09-17|2026-09-16', h)
print("[4] 당일표 내 과거 일자 원시 문자열: %d건 (0이어야 함)" % len(past))
if past: fails.append("과거일자 문자열 %d건" % len(past))

# 5) div 시작/종료
print("[5] div 시작 %s / 종료 %s" % (h.lstrip()[:4] == "<div", h.rstrip()[-6:] == "</div>"))
if h.lstrip()[:4] != "<div": fails.append("div 시작 아님")
if h.rstrip()[-6:] != "</div>": fails.append("div 종료 아님")

# 6) 필수 문구
MUST = ["6,894.23","+178.82","+2.66","827.12","1,090.23","261,000","1,857,000","196,100",
        "+2.417","90.8","4,584","16,591","15,123","36,167","확인 불가","데이터 신뢰도",
        "모델 잔차","항등식","1.51689","2.45867","6,874.26","−0.28970622","2.164021",
        "14회 연속 기각","시간외 단일가","NXT","베이시스","BOJ","1.25","공매도","클러스터",
        "집중도","오차 귀속","0.00000000"]
miss = [x for x in MUST if x not in h]
print("[6] 필수문구 %d종 -> 누락 %d건 %s" % (len(MUST), len(miss), miss if miss else ""))
if miss: fails.append("필수문구 누락 %s" % miss)

# 7) 용량
raw = len(h.encode("utf-8"))
qp = sum(1 if 32 <= b < 127 and b != 61 else 3 for b in h.encode("utf-8"))
print("[7] chars %d / raw %d bytes / QP 추정 %d bytes (Gmail 한도 102,400)" % (len(h), raw, qp))
if raw > 102400: fails.append("raw 용량 초과 %d" % raw)

# 8) 예산
print("[8] 표 %d개 / tr %d행 / td %d셀 / 카드 6장" % (
    len(re.findall(r"<table[\s>]", h)), len(re.findall(r"<tr[\s>]", h)), len(re.findall(r"<td[\s>]", h))))

print()
if fails:
    print("★★ 검증 실패 %d건" % len(fails))
    for f in fails: print("   -", f)
    sys.exit(1)
print("★★ 전 항목 통과")
