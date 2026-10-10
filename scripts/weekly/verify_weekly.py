# -*- coding: utf-8 -*-
"""
verify_weekly.py — 주간 리뷰 HTML 검수 (공통 가이드 guide v2 대응본)

구버전(scripts/weekly/verify_weekly.py @ ccr-18bf9b3d-8q16j8)의 문제 셋을 고쳤다.
  ① REQ 가 단일 문자열 목록이라 가이드 치환이 일어나면 반드시 오탐한다.
     '패리티' → '이론가' 로 바꾸면 MISSING '패리티' 로 FAIL.  → 동의어 그룹으로 바꿨다.
  ② REQ 에 '2026-10-06' 이 하드코딩돼 있어 그 주가 지나면 ★매주 FAIL★ 한다.
     → 환경변수 WEEKLY_NEXT_TRADING_DAY 로 받고, 없으면 날짜 형태만 본다.
  ③ 가이드 G1-3 번역체 금칙어와 G2-3 부록 완전성을 전혀 안 봤다. → 둘 다 추가.

사용:  python3 scripts/weekly/verify_weekly.py
       WEEKLY_NEXT_TRADING_DAY=2026-10-06 python3 scripts/weekly/verify_weekly.py
종료코드 0 = PASS. PASS 없이는 발송하지 않는다.
"""
import os
import re
import sys

# 콘솔 코드페이지가 UTF-8이 아니면(윈도 cp949 등) 실패 메시지를 찍다가 죽는다.
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

HTML = os.environ.get("WEEKLY_HTML", "weekly.html")
h = open(HTML, encoding="utf-8").read()
fail = []
warn = []

# ───────────────────────────────────────────────────────────────────
# 1) Outlook/Exchange 금칙 태그
# ───────────────────────────────────────────────────────────────────
BAD = ['<style', 'var(--', 'class="', 'display:grid', 'display:flex', 'inline-block',
       '@media', '@supports', '<svg', 'http', '<script', 'border-radius',
       '<!DOCTYPE', '<!doctype', 'href="#', '<html', '<head', '<body',
       '&nbsp;&', 'position:']
for b in BAD:
    n = h.count(b)
    if n:
        fail.append("FORBIDDEN %r x%d" % (b, n))

# ───────────────────────────────────────────────────────────────────
# 2) 태그 개폐 균형
# ───────────────────────────────────────────────────────────────────
for tag in ['table', 'tr', 'td', 'div', 'font', 'b', 'u', 'sub', 'code']:
    o = len(re.findall(r'<%s[\s>]' % tag, h))
    c = len(re.findall(r'</%s>' % tag, h))
    if o != c:
        fail.append("UNBALANCED <%s> open=%d close=%d" % (tag, o, c))

# ───────────────────────────────────────────────────────────────────
# 3) 화살표와 숫자 부호 일치
# ───────────────────────────────────────────────────────────────────
for m in re.finditer(r'([▲▼])\s*([+\-−])', h):
    a, s = m.group(1), m.group(2)
    if a == '▲' and s != '+':
        fail.append("ARROW %r @%d" % (m.group(0), m.start()))
    if a == '▼' and s not in '-−':
        fail.append("ARROW %r @%d" % (m.group(0), m.start()))

# ───────────────────────────────────────────────────────────────────
# 4) 포맷 문자열 누출
# ───────────────────────────────────────────────────────────────────
for pat in ['%%', '%.4f', '%+.', '%s', '%d', '{:']:
    if pat in h:
        fail.append("FORMAT LEAK %r" % pat)

# ───────────────────────────────────────────────────────────────────
# 5) 필수 내용 — ★동의어 그룹★
#    가이드 [T] 치환표가 표현을 바꿔도 통과해야 한다.
#    그룹 안의 표현 중 ★하나라도★ 있으면 통과.
# ───────────────────────────────────────────────────────────────────
REQ_GROUPS = [
    ("리포트 제목",      ["주간 리뷰"]),
    ("한 줄 결론",       ["주간 결론", "한 줄 결론"]),
    ("지수 분해",        ["지수 분해", "블록 분해"]),
    ("EWY",              ["EWY"]),
    # 가이드 v2 [T]: 패리티 → 이론가.  구버전은 '패리티'만 요구해 치환 시 FAIL 했다.
    ("이론가 대비 괴리", ["이론가", "패리티", "괴리"]),
    ("프리미엄 변화",    ["프리미엄 변화", "웃돈", "비싼 정도"]),
    ("예측 채점",        ["예측 채점", "채점"]),
    ("MAE",              ["MAE", "평균절대오차"]),
    ("RMSE",             ["RMSE", "제곱평균제곱근"]),
    ("80% 구간",         ["80% 구간"]),
    ("블록 귀속",        ["블록 귀속", "귀속"]),
    ("공매도",           ["공매도"]),
    ("베이시스",         ["베이시스"]),
    # [T]: 콘탱고/백워데이션도 풀어 쓸 수 있다
    ("선물-현물 상태",   ["콘탱고", "백워데이션", "선물이 현물보다"]),
    ("반증 조건",        ["반증하는 조건", "반증 조건"]),
    ("수집기 토큰 사고", ["토큰 무효화", "8005"]),
    ("KRX",              ["KRX", "거래소 전종목", "거래소 확정"]),
    ("ECOS",             ["ECOS", "한국은행 통계"]),
    ("면책",             ["면책"]),
    ("자기상관",         ["자기상관"]),
    # [T]: 중심 수축 → 예측 폭이 실제보다 좁았던 정도
    ("예측 폭 진단",     ["중심 수축", "예측 폭"]),
    ("KOSDAQ",           ["KOSDAQ"]),
    ("MU",               ["MU"]),
    ("SOXX",             ["SOXX"]),
    ("주봉",             ["주봉"]),
    ("기타법인",         ["기타법인"]),
    ("검증 보류",        ["검증 보류"]),
    # ── guide v2 신설 ──
    ("부록",             ["[부록]", "찾아보기"]),
    ("예측력 블록",      ["예측력"]),
    ("가이드 버전 표기", ["guide v"]),
]
for name, alts in REQ_GROUPS:
    if not any(a in h for a in alts):
        fail.append("MISSING %s — 허용 표현 중 하나도 없다: %s" % (name, " / ".join(repr(a) for a in alts)))

# ───────────────────────────────────────────────────────────────────
# 6) 다음 거래일 — ★날짜를 코드에 박지 않는다★
#    구버전은 REQ 에 '2026-10-06' 이 있어 그 주가 지나면 매주 FAIL 했다.
# ───────────────────────────────────────────────────────────────────
nxt = os.environ.get("WEEKLY_NEXT_TRADING_DAY", "").strip()
if nxt:
    if nxt not in h:
        fail.append("MISSING 다음 거래일 %r (WEEKLY_NEXT_TRADING_DAY)" % nxt)
elif not re.search(r'20\d{2}-\d{2}-\d{2}', h):
    fail.append("MISSING 다음 거래일 — YYYY-MM-DD 형태 날짜가 본문에 없다")

# ───────────────────────────────────────────────────────────────────
# 7) guide v2 G1-3 / G1-3-2 — 번역체 금칙 표현
# ───────────────────────────────────────────────────────────────────
BANNED_STYLE = ["되어지", "보여진", "지어진", "에 대한", "에 있어서", "에 있어",
                "로 인한 영향", "로 판단된다", "로 보인다", "라고 할 수 있다", "한 모습"]
for b in BANNED_STYLE:
    n = h.count(b)
    if n:
        fail.append("STYLE 번역체 %r x%d (guide v2 G1-3)" % (b, n))

# ───────────────────────────────────────────────────────────────────
# 8) guide v2 G2-3 — 부록 완전성
#    본문에 나온 영문 약어와 6자리 종목코드가 부록에 다 올라왔는지.
#    처음 돌릴 때 NOISE 에 걸러야 할 항목이 몇 개 나온다 — 거짓 양성은
#    NOISE 에 추가하고, 진짜 누락은 부록에 추가하라.
# ───────────────────────────────────────────────────────────────────
NOISE = {
    # HTML/스타일/포맷 잡음
    "BR", "TD", "TR", "B", "U", "P", "DIV", "FONT", "KB", "MB",
    # 리포트 구조 표기
    "REV", "OHLC", "RMS", "SD", "TEST", "NEW",
}


def strip_tags(s):
    s = re.sub(r'<[^>]+>', ' ', s)
    s = s.replace('&nbsp;', ' ').replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>')
    return s


cut = max(h.find('[부록]'), h.find('찾아보기'))
if cut < 0:
    fail.append("APPENDIX 부록 절을 찾을 수 없다 (guide v2 G2-1)")
else:
    body_txt = strip_tags(h[:cut])
    appx_txt = strip_tags(h[cut:])

    abbr = {a for a in re.findall(r'[A-Z]{2,6}', body_txt)} - NOISE
    # 계산박스(bgcolor="#16301f")는 산식 본문이라 소수가 많다. 코드 검사에서 뺀다.
    #   실측 2026-10-10: 0.019807 같은 소수가 '019807' 로 잡혀 16건이 오탐됐다.
    body_nocalc = re.sub(r'<table[^>]*bgcolor="#16301f".*?</table>', ' ', h[:cut], flags=re.S)
    body_nocalc = strip_tags(body_nocalc)
    # 소수점 뒤에 붙은 숫자 덩어리도 코드가 아니다 — 앞뒤로 숫자와 점을 모두 막는다.
    codes = set(re.findall(r'(?<![\d.])[0-9]{6}(?![\d.])', body_nocalc))

    miss_a = sorted(a for a in abbr if a not in appx_txt)
    miss_c = sorted(c for c in codes if c not in appx_txt)
    if miss_a:
        fail.append("APPENDIX 약어 %d건이 부록에 없다: %s" % (len(miss_a), ", ".join(miss_a)))
    if miss_c:
        fail.append("APPENDIX 종목코드 %d건이 부록에 없다: %s" % (len(miss_c), ", ".join(miss_c)))

    # (ㄷ) 한글 전문용어 — 치환도 설명도 안 된 용어
    JARGON = ["패리티", "리레이팅", "디레이팅", "요인분해", "전이율", "익스포저",
              "센티먼트", "롤오버", "최대고통점", "중심 수축", "서프라이즈"]
    for j in JARGON:
        if j in body_txt and j not in appx_txt:
            # 괄호 설명이 바로 뒤에 붙었으면 통과
            if not re.search(re.escape(j) + r'\s*[(（]', body_txt):
                fail.append("JARGON %r — 치환도, 괄호 설명도, 부록 등재도 없다 (guide v2 G2-3)" % j)

# ───────────────────────────────────────────────────────────────────
# 9) 용량 — Gmail 클리핑 한도
# ───────────────────────────────────────────────────────────────────
size = len(h.encode("utf-8"))
if size > 95000:
    fail.append("TOO BIG %d bytes (목표 <=95,000)" % size)
elif size > 90000:
    warn.append("size %d bytes — 95,000 에 근접했다" % size)

# ───────────────────────────────────────────────────────────────────
print("file   %s" % HTML)
print("bytes  %d   chars %d" % (size, len(h)))
print("tags   table=%d tr=%d td=%d" % (h.count('<table'), h.count('<tr'), h.count('<td')))
for w in warn:
    print("  WARN  %s" % w)
if fail:
    print("=== FAIL (%d) ===" % len(fail))
    for f in fail:
        print("   %s" % f)
    sys.exit(1)
print("=== ALL CHECKS PASSED ===")
