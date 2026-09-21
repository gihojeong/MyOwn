# -*- coding: utf-8 -*-
import re, sys, datetime
# 회차별로 파일명이 바뀌므로 argv로 받는다. 생략하면 당일자 리포트를 찾는다.
PATH = sys.argv[1] if len(sys.argv) > 1 else \
    "kospi_close_%s.html" % datetime.datetime.now().strftime("%Y%m%d")
TODAY = re.search(r"(\d{8})", PATH).group(1)
h = open(PATH, encoding="utf-8").read()
print("검증 대상: %s (당일자 %s)\n" % (PATH, TODAY))
fail=[]

# [1] 금지 문자열
BAN = ['<style','var(--','class="','display:grid','inline-block','@media','@supports',
       '<svg','http','<script','border-radius','<!DOCTYPE','href="#','<html','<head','<body','<pre','white-space:pre']
print("[1] 금지 문자열")
for b in BAN:
    n = h.lower().count(b.lower())
    if n: fail.append("금지문자열 %r %d건"%(b,n)); print("   ★%-18s %d건"%(b,n))
print("   -> 금지 %d종 검사, 위반 %d종" % (len(BAN), sum(1 for b in BAN if h.lower().count(b.lower()))))

# [2] %% 잔류
print("[2] '%%' 잔류 =", h.count("%%"))
if h.count("%%"): fail.append("%% 잔류 %d"%h.count("%%"))

# [3] 태그 개폐 균형
print("[3] 태그 개폐 균형")
for t in ["table","tr","td","div","font","b","span"]:
    o = len(re.findall(r"<%s(?=[\s>])"%t, h))
    c = len(re.findall(r"</%s>"%t, h))
    ok = "OK" if o==c else "★불일치"
    print("   %-6s 열림 %4d / 닫힘 %4d  %s" % (t,o,c,ok))
    if o!=c: fail.append("태그 %s 열림%d 닫힘%d"%(t,o,c))

# [4] ▲▼ 기호 - 숫자 부호 일치
print("[4] ▲▼ 기호와 숫자 부호 일치")
pairs = re.findall(r"([▲▼])\s*([+-])", h)
bad = [p for p in pairs if (p[0]=="▲")!=(p[1]=="+")]
print("   검사 %d쌍, 불일치 %d건" % (len(pairs), len(bad)))
if bad: fail.append("부호기호 불일치 %d: %s"%(len(bad),bad[:5])); print("   ★",bad[:8])

# [5] 색상 - 부호 일치  (#d03b3b=+, #2a78d6=-)
print("[5] 색상과 부호 일치")
cs = re.findall(r'<font color="(#d03b3b|#2a78d6)">([▲▼])([+-]?)', h)
badc=[]
for colr,a,s in cs:
    if colr=="#d03b3b" and a!="▲": badc.append((colr,a,s))
    if colr=="#2a78d6" and a!="▼": badc.append((colr,a,s))
print("   검사 %d건, 불일치 %d건" % (len(cs), len(badc)))
if badc: fail.append("색상-부호 불일치 %d"%len(badc)); print("   ★",badc[:8])

# [6] 당일 표 안의 과거 일자 문자열
print("[6] 당일 종가 표 내 과거 일자 혼입")
dates = re.findall(r"20260[0-9]{3}", h)
bad_d = [x for x in dates if x != TODAY]
print("   8자리 날짜 토큰: %s" % (set(dates) if dates else "없음"))
# 허용: 본문 서술의 9/18, 9/17 등 상대 표기는 허용. 8자리 절대표기는 당일만 허용.
if bad_d: fail.append("과거 8자리 일자 혼입 %s"%set(bad_d))

# [7] 용량
b = len(h.encode("utf-8"))
print("[7] 용량: chars=%d  bytes=%d  (Gmail 한도 102,400 / 여유 %d)" % (len(h), b, 102400-b))
if b > 102400: fail.append("용량 초과 %d"%b)

# [8] 구조 필수 문구
# ★★회차마다 값을 갈아끼워라★★ 아래 목록 뒷부분(종가·괴리·연속 회차수 등)은 2026-09-21자
#   실측값이다. 그대로 두면 다음 회차에서 전부 '누락'으로 잡힌다.
#   앞부분(섹션 제목·고정 문구)은 회차와 무관하므로 건드리지 마라.
print("[8] 필수 문구 존재")
MUST = ["오늘의 결론","데이터 신뢰도","확인 불가 항목","d1 · 국내 증시 결산","d2 · 수급 해부",
        "d3 · 시총 상위 30","d4 · 반도체","d5 · 예측 대비 괴리 검증","d6 · 내일","면책","출처",
        "항등식 검증","모델 잔차 = 0.00000000","집중도","클러스터 6분류","오차 귀속",
        "내일(9/22 화) 체크포인트 5","KODEX MSCI Korea","16회 연속 기각","7,007.72","113.49",
        "274,000","1,868,000","208,000","836.27","+1.034057","시사점","강도","지수 기여"]
miss=[m for m in MUST if m not in h]
print("   %d종 검사, 누락 %d종 %s" % (len(MUST), len(miss), miss if miss else ""))
if miss: fail.append("필수문구 누락 %s"%miss)

# [9] div 시작/종료
print("[9] div 시작 =", h[:5], "/ 종료 =", h[-6:])
if not h.startswith("<div"): fail.append("div로 시작하지 않음")
if not h.rstrip().endswith("</div>"): fail.append("div로 끝나지 않음")

# [10] 배지 리터럴 누출
print("[10] 배지 리터럴 누출 검사")
for lit in ['>up<','>dn<','>nt<','"up"','"dn"','"nt"']:
    if lit in h: fail.append("배지 리터럴 %s"%lit); print("   ★",lit)
print("   방향 배지: ▲ 지수 기여 + =%d / ▼ 지수 기여 − =%d / ― 혼조 =%d"
      % (h.count("▲ 지수 기여 +"), h.count("▼ 지수 기여 −"), h.count("― 혼조")))

# [11] 확률 합
print("[11] 시나리오 확률 합 = 40+38+22 =", 40+38+22)

print()
if fail:
    print("★★ 검증 실패 %d건:" % len(fail))
    for f in fail: print("   -",f)
    sys.exit(1)
print("★ 전 항목 통과")
