# -*- coding: utf-8 -*-
import re, sys
h=open('weekly.html',encoding='utf-8').read()
BAD=['<style','var(--','class="','display:grid','inline-block','@media','@supports','<svg','http',
     '<script','border-radius','<!DOCTYPE','<!doctype','href="#','<html','<head','<body','&nbsp;&','position:']
fail=[]
for b in BAD:
    n=h.count(b)
    if n: fail.append('FORBIDDEN %r x%d'%(b,n))
for tag in ['table','tr','td','div','font','b','u','sub','code']:
    o=len(re.findall(r'<%s[\s>]'%tag,h)); cl=len(re.findall(r'</%s>'%tag,h))
    if o!=cl: fail.append('UNBALANCED <%s> open=%d close=%d'%(tag,o,cl))
for m in re.finditer(r'([▲▼])\s*([+\-−])',h):
    a,s_=m.group(1),m.group(2)
    if a=='▲' and s_!='+': fail.append('ARROW %r @%d'%(m.group(0),m.start()))
    if a=='▼' and s_ not in '-−': fail.append('ARROW %r @%d'%(m.group(0),m.start()))
# 리터럴 % 포맷 누출
for pat in ['%%','%.4f','%+.','%s','%d','{:']:
    if pat in h: fail.append('FORMAT LEAK %r'%pat)
REQ=['주간 리뷰','주간 결론','지수 분해','EWY','패리티','프리미엄 변화','예측 채점','MAE','RMSE',
     '80% 구간','블록 귀속','공매도','베이시스','콘탱고','반증하는 조건','2026-10-06','토큰 무효화',
     '8005','KRX','ECOS','면책','자기상관','중심 수축','KOSDAQ','MU','SOXX','주봉','기타법인','검증 보류']
for r in REQ:
    if r not in h: fail.append('MISSING %r'%r)
size=len(h.encode('utf-8'))
if size>95000: fail.append('TOO BIG %d'%size)
print('bytes',size,'chars',len(h))
print('table=%d tr=%d td=%d'%(h.count('<table'),h.count('<tr'),h.count('<td')))
if fail:
    print('=== FAIL ===')
    for f in fail: print('  ',f)
    sys.exit(1)
print('=== ALL CHECKS PASSED ===')
