#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""반도체 ETF 보유내역 스냅샷 + ★능동 비중 변화★ 분해.

왜 이 스크립트가 필요한가
  "최근 비중이 늘어난 종목"을 비중 차이로 바로 읽으면 틀린다. ★비중은 가격만 올라도 늘어난다.★
  수량이 그대로여도 그 종목이 남들보다 더 오르면 비중이 커진다. 그 몫을 걷어내야
  운용사·지수가 ★의도적으로 늘린 몫★이 남는다. 두 가지로 따로 구하고 서로 대조한다.

    (1) 가격 보정 비중 변화   Δa_i = w_i,t − w_i,t−1 × (1+r_i) / (1+r_P)
        r_P 는 포트폴리오 수익률(보유 종목 가중). 수량이 안 변했으면 Δa_i = 0 이 나온다.
    (2) 초과 수량 변화        x_i = (Q_i,t / Q_i,t−1) ÷ (S_t / S_t−1) − 1
        Q=보유 주식수, S=ETF 좌수(발행 주식수). 설정 유입으로 전 종목이 똑같이 늘어난 몫을
        S 변화로 나눠 제거한다. 남는 것이 종목별 의도다.
    ★(1)과 (2)의 부호가 어긋나면 데이터를 먼저 의심하라.★ 둘 다 같은 방향일 때만 신호로 쓴다.

검증된 소스 (2026-10-05 실측 상태코드)
  · iShares  https://www.ishares.com/us/products/<id>/<slug>/latest-holdings.csv
             200 / 6.4KB. Weight(%) + Quantity + Shares Outstanding ★전부 있다★. 1순위.
             (구 `NNNNNNN.ajax?fileType=csv` 경로는 HTML을 돌려준다 — 쓰지 마라)
  · stockanalysis  https://stockanalysis.com/etf/<ticker>/holdings/
             200. HTML 표 No.|Symbol|Name|%Weight|Shares. 좌수는 없다. 2순위.
  · VanEck   302 쿠키 리다이렉트 루프(최대 50회) → ★쓸 수 없다.★ SMH 는 stockanalysis 로.
  · KRX 정보데이터시스템 OTP  POST generate.cmd → 본문 "LOGOUT" ★세션 없이는 안 된다.★
  · stockanalysis 국내 ETF  /quote/krx/<6자리>/holdings/ 는 200 이지만
             ★기준일이 두 달 지난 월말 스냅샷이고 상위 10행만 준다.★ (091160 조회 시 Jul 31)
             비중 '수준'의 참고로만 쓰고 ★'최근 변화'로 쓰지 마라.★
             국내 ETF 일별 보유내역은 운용사 공시가 정본이며 이 환경에서 미검증이다.

사용법
  python3 scripts/etf/etf_holdings.py --fetch --out snap_20261002.json
  python3 scripts/etf/etf_holdings.py --delta snap_20260925.json snap_20261002.json
"""
import argparse, json, re, subprocess, sys, datetime

# iShares 상품 id/slug 는 상품 페이지에서 가져온 고정값이다.
ISHARES = {
    'SOXX': ('239705', 'ishares-phlx-semiconductor-etf'),
}
# 좌수가 없어 (2)를 못 구하는 ETF — (1)만 쓴다.
SA_ONLY = ['SMH', 'XSD', 'SOXQ']

TIMEOUT = 25


def _curl(url):
    r = subprocess.run(['curl', '-sS', '--max-time', str(TIMEOUT), '-L', url],
                       capture_output=True)
    if r.returncode:
        return None
    return r.stdout.decode('utf-8', 'replace')


def _num(s):
    s = re.sub(r'[,%\s"]', '', str(s))
    if s in ('', '-', 'n/a', 'N/A'):
        return None
    try:
        return float(s)
    except ValueError:
        return None


def fetch_ishares(tkr):
    pid, slug = ISHARES[tkr]
    txt = _curl('https://www.ishares.com/us/products/%s/%s/latest-holdings.csv' % (pid, slug))
    if not txt or txt.lstrip().startswith('<'):
        return None
    asof, shares_out, rows, hdr = None, None, [], None
    for ln in txt.splitlines():
        if ln.startswith('Fund Holdings as of'):
            asof = ln.split(',', 1)[1].strip().strip('"')
        elif ln.startswith('Shares Outstanding'):
            shares_out = _num(ln.split(',', 1)[1])
        elif ln.startswith('Ticker,Name,'):
            hdr = [c.strip().strip('"') for c in ln.split(',')]
        elif hdr and ln.startswith('"'):
            c = next(__import__('csv').reader([ln]))
            d = dict(zip(hdr, c))
            if d.get('Asset Class') != 'Equity':
                continue
            rows.append(dict(sym=d['Ticker'], name=d['Name'],
                             w=_num(d['Weight (%)']), q=_num(d['Quantity']),
                             px=_num(d['Price'])))
    if not rows:
        return None
    return dict(etf=tkr, src='ishares-csv', asof=asof, shares_out=shares_out, rows=rows)


def fetch_stockanalysis(tkr):
    txt = _curl('https://stockanalysis.com/etf/%s/holdings/' % tkr.lower())
    if not txt:
        return None
    t = re.sub(r'<!--.*?-->', '', txt, flags=re.S)
    rows = []
    for r in re.findall(r'<tr[^>]*>(.*?)</tr>', t, flags=re.S):
        c = [re.sub(r'<[^>]+>', '', x).strip()
             for x in re.findall(r'<t[dh][^>]*>(.*?)</t[dh]>', r, flags=re.S)]
        if len(c) >= 5 and c[0].isdigit():
            rows.append(dict(sym=c[1].replace('KRX: ', '').strip(), name=c[2],
                             w=_num(c[3]), q=_num(c[4]), px=None))
    if not rows:
        return None
    m = re.search(r'[Aa]s of ([A-Z][a-z]{2} \d{1,2}, \d{4})', t)
    return dict(etf=tkr, src='stockanalysis-html', asof=(m.group(1) if m else None),
                shares_out=None, rows=rows)


def fetch_all(tickers):
    out = {}
    for tkr in tickers:
        d = fetch_ishares(tkr) if tkr in ISHARES else None
        if d is None:
            d = fetch_stockanalysis(tkr)
        if d is None:
            print('  %-6s 실패 — 두 경로 모두' % tkr, file=sys.stderr)
            continue
        out[tkr] = d
        print('  %-6s %s  as of %s  %d종목  좌수 %s'
              % (tkr, d['src'], d['asof'], len(d['rows']),
                 ('%d' % d['shares_out']) if d['shares_out'] else '없음'), file=sys.stderr)
    return out


def delta_one(a, b):
    """a=이전, b=현재. (1) 가격 보정 비중 변화와 (2) 초과 수량 변화."""
    pa = {r['sym']: r for r in a['rows']}
    pb = {r['sym']: r for r in b['rows']}
    both = [s for s in pb if s in pa]
    # r_P: 두 스냅샷에 모두 있고 가격이 있는 종목의 이전 비중 가중 수익률
    num = den = 0.0
    for s in both:
        if pa[s].get('px') and pb[s].get('px') and pa[s]['w']:
            num += pa[s]['w'] * (pb[s]['px'] / pa[s]['px'] - 1.0)
            den += pa[s]['w']
    rP = (num / den) if den else None
    sr = ((b['shares_out'] / a['shares_out']) if (a.get('shares_out') and b.get('shares_out'))
          else None)
    out = []
    for s in both:
        ri = ((pb[s]['px'] / pa[s]['px'] - 1.0)
              if (pa[s].get('px') and pb[s].get('px')) else None)
        da = (pb[s]['w'] - pa[s]['w'] * (1 + ri) / (1 + rP)) if (ri is not None and rP is not None) else None
        xq = ((pb[s]['q'] / pa[s]['q']) / sr - 1.0) * 100.0 if (sr and pa[s].get('q')) else None
        out.append(dict(sym=s, name=pb[s]['name'], w_prev=pa[s]['w'], w_now=pb[s]['w'],
                        w_raw_chg=pb[s]['w'] - pa[s]['w'], ret=(ri * 100 if ri is not None else None),
                        active_w_chg=da, excess_qty_chg=xq,
                        agree=(None if (da is None or xq is None)
                               else (da > 0) == (xq > 0))))
    newly = sorted(set(pb) - set(pa))
    dropped = sorted(set(pa) - set(pb))
    return dict(etf=b['etf'], asof_prev=a['asof'], asof_now=b['asof'],
                r_port=(rP * 100 if rP is not None else None),
                shares_out_chg=((sr - 1) * 100 if sr else None),
                newly_added=newly, dropped=dropped,
                rows=sorted(out, key=lambda z: -(z['active_w_chg'] if z['active_w_chg'] is not None
                                                 else (z['w_raw_chg'] or 0))))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--fetch', action='store_true')
    ap.add_argument('--tickers', default='SOXX,SMH,XSD')
    ap.add_argument('--out', default='')
    ap.add_argument('--delta', nargs=2, metavar=('PREV', 'NOW'))
    a = ap.parse_args()
    if a.delta:
        p = json.load(open(a.delta[0], encoding='utf-8'))
        n = json.load(open(a.delta[1], encoding='utf-8'))
        res = {k: delta_one(p['etfs'][k], n['etfs'][k])
               for k in n['etfs'] if k in p.get('etfs', {})}
        json.dump(res, sys.stdout, ensure_ascii=False, indent=1)
        print()
        return 0
    if a.fetch:
        etfs = fetch_all([x.strip().upper() for x in a.tickers.split(',') if x.strip()])
        snap = dict(captured_at=datetime.datetime.now().isoformat(timespec='seconds'),
                    etfs=etfs)
        txt = json.dumps(snap, ensure_ascii=False, indent=1)
        if a.out:
            open(a.out, 'w', encoding='utf-8').write(txt + '\n')
            print('wrote %s (%d bytes)' % (a.out, len(txt)), file=sys.stderr)
        else:
            print(txt)
        return 0
    print(__doc__)
    return 2


if __name__ == '__main__':
    sys.exit(main())
