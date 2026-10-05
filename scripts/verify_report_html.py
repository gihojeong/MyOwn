#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""리포트 HTML 발송 전 검증 — 4개 루틴 공용.

사용법:
    python3 scripts/verify_report_html.py report.html [gloss.json] [--coverage]

gloss.json (선택) 형식 — 부록 누락 검사를 켠다:
    {"terms": ["SOXX", "EWY", ...], "codes": ["005930", ...], "ignore": ["KST"]}

검사 항목
  1. Outlook/Exchange 금칙 문자열
  2. 태그 개폐 균형 (table tr td div font b u)
  3. ▲/▼ 와 숫자 부호 일치
  4. %-포맷 누출 (%%  %.4f  None 등)
  5. ★부록 누락 — 본문 약어·종목코드가 부록 사전에 다 있나 (gloss.json 있을 때)
  6. Gmail 클리핑 한도 (기본 95,000 bytes)
  7. ★커버리지 체크표 18행 — 섹터 11 + 요인군 7 (--coverage 를 줬을 때만)
     guide v11 에서 "변화 없음" 줄이 본문에서 부록 (라)로 내려갔다. 발행 회차는 반드시 켜라.
     복기·리허설 산출물처럼 시장 전망이 없는 문서에는 켜지 마라.

종료코드 0 = PASS. 0이 아니면 ★발송하지 마라.★
"""
import re, sys, json

FORBIDDEN = ['<style', 'var(--', 'class="', 'display:grid', 'display:flex', 'inline-block',
             '@media', '@supports', '<svg', '<script', 'border-radius', '<!DOCTYPE', '<!doctype',
             'href="#', '<html', '<head', '<body', 'position:', 'http']
TAGS = ['table', 'tr', 'td', 'div', 'font', 'b', 'u']
LEAKS = ['%%', '%.4f', '%.2f', '%+.', '{:', 'None', 'nan', 'inf']
APPENDIX_MARKER = '찾아보기'
LIMIT = 95000

# [G2-2] (라) 커버리지 체크표 — 섹터 11 + 요인군 7 = 18행 고정.
# guide v11 에서 "변화 없음" 줄이 본문에서 부록으로 내려갔다. 그 대가로 이 검사가 생겼다.
SECTORS = ['반도체', '조선', '방산', '전력기기', '2차전지', '자동차',
           '화장품', '바이오', '금융', '인터넷', '엔터']
FACTORS = ['해외시장', '매크로', '국제정치', '업체', '수급', '정책', '캘린더']


def check_coverage(h):
    """부록 (라) 18행이 다 있나. 발행 회차에만 켠다(--coverage)."""
    miss_s = [s for s in SECTORS if s not in h]
    miss_f = [f for f in FACTORS if f not in h]
    out = []
    if miss_s:
        out.append('커버리지(섹터 11) 누락: %s' % ', '.join(miss_s))
    if miss_f:
        out.append('커버리지(요인군 7) 누락: %s' % ', '.join(miss_f))
    return out


def verify(path, gloss_path=None, limit=LIMIT, coverage=False):
    h = open(path, encoding='utf-8').read()
    fail, warn = [], []

    for b in FORBIDDEN:
        n = h.count(b)
        if n:
            fail.append('금칙 문자열 %r x%d' % (b, n))

    for t in TAGS:
        o = len(re.findall(r'<%s[\s>]' % t, h))
        c = len(re.findall(r'</%s>' % t, h))
        if o != c:
            fail.append('태그 불균형 <%s> 열림%d 닫힘%d' % (t, o, c))

    for m in re.finditer(r'([▲▼])\s*([+\-−])', h):
        a, s = m.group(1), m.group(2)
        if a == '▲' and s != '+':
            fail.append('화살표 부호 불일치 %r @%d' % (m.group(0), m.start()))
        if a == '▼' and s not in '-−':
            fail.append('화살표 부호 불일치 %r @%d' % (m.group(0), m.start()))

    for p in LEAKS:
        if p in h:
            fail.append('포맷 누출 %r' % p)

    if gloss_path:
        g = json.load(open(gloss_path, encoding='utf-8'))
        terms = set(g.get('terms', []))
        codes = set(g.get('codes', []))
        ignore = set(g.get('ignore', [])) | {'KST', 'REST', 'OK'}
        body = h.split(APPENDIX_MARKER)[0]
        text = re.sub(r'<[^>]+>', ' ', body)
        found_ab = set(re.findall(r'\b([A-Z]{2,6})\b', text))
        # ★소수점 내부 숫자를 종목코드로 오인하지 않게 한다.
        #   0.280724 의 "280724" 를 잡아 거짓 실패를 내던 버그를 2026-10-05 리허설에서 잡았다.
        found_cd = set(re.findall(r'(?<![\d.])(\d{6})(?![\d.])', text))
        miss_ab = sorted(found_ab - terms - ignore)
        miss_cd = sorted(found_cd - codes)
        if miss_ab:
            fail.append('부록(가) 누락 약어: %s' % ', '.join(miss_ab))
        if miss_cd:
            fail.append('부록(나) 누락 종목코드: %s' % ', '.join(miss_cd))
        unused = sorted(terms - found_ab)
        if unused:
            warn.append('부록에만 있고 본문에 없는 약어: %s' % ', '.join(unused))

    if coverage:
        fail += check_coverage(h)

    size = len(h.encode('utf-8'))
    if size > limit:
        fail.append('용량 초과 %d bytes (한도 %d)' % (size, limit))

    print('bytes %d / chars %d / table %d' % (size, len(h), h.count('<table')))
    for w in warn:
        print('  [warn]', w)
    if fail:
        print('=== FAIL %d ===' % len(fail))
        for f in fail:
            print('  ', f)
        return 1
    print('=== ALL CHECKS PASSED ===')
    return 0


if __name__ == '__main__':
    args = [a for a in sys.argv[1:] if a != '--coverage']
    cov = '--coverage' in sys.argv
    if not args:
        print(__doc__)
        sys.exit(2)
    sys.exit(verify(args[0], args[1] if len(args) > 1 else None, coverage=cov))
