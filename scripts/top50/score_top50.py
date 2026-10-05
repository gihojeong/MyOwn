#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Top50 ETF 루틴 — 전일 예측 채점기.

입력
  1. 수집 결과 JSON (kiwoom_collect.py --preset premarket --codes "...")
  2. 예측 테이블 TSV/PSV — Drive top50etf_forecast_<기준일> 의 [STOCK TABLE] 본문
     code|name|sector|close_prev|src|ret_prev|mcap_jo|bm_w|model_w|active|exp|lo80|hi80|dir|conf

출력 (JSON)
  bm / model_stock / model_nav / active 와 3분해(배분·섹터배분·종목선택),
  섹터별 Brinson 표, 종목별 실현·오차·구간적중, 예측력 지표.

★수익률 규칙 (collection-contract.md 8-3g)
  일간 수익률은 반드시 같은 스냅샷 안에서 닫는다 — pred_pre / base_pric.
  어제 회차가 기록한 종가를 분모로 쓰면 통합가 재생성 드리프트가 섞인다
  (2026-10-02 실측: 59종목 중 41종목 불일치, 최대 1.68%).

★가격 출처 (8-3e)
  키움 cur_prc 는 전부 통합가(KRX+NXT)다. 거래소 정규장 확정 등락률을 아는 종목만
  --krx-ret 로 덮어쓴다.

사용법
  python3 scripts/top50/score_top50.py kw.json forecast.psv \
      --cash 0.025 --futures -0.0582 --k200-ret 0.41 \
      --krx-ret 005930=0.000,005935=-1.711,000660=0.436 > score.json
"""
import argparse, json, math, sys


def load_forecast(path):
    rows = []
    for ln in open(path, encoding='utf-8'):
        ln = ln.strip()
        if not ln or ln.startswith('code|') or '|' not in ln:
            continue
        p = ln.split('|')
        if len(p) < 13:
            continue
        rows.append(dict(cd=p[0], nm=p[1], sec=p[2], c_prev=float(p[3]), src=p[4],
                         bm=float(p[7]), mw=float(p[8]), exp=float(p[10]),
                         lo=float(p[11]), hi=float(p[12]),
                         dr=(p[13] if len(p) > 13 else 'FLAT')))
    return rows


def snapshot_returns(coll, rows, base_date, krx_ret):
    """같은 응답 안의 (base_pric, pred_pre) 로 수익률을 닫는다."""
    res = coll['results']
    out = []
    for x in rows:
        pr = res.get('profile_' + x['nm'], {}).get('data') or {}
        base = abs(float(str(pr.get('base_pric', '0')).replace(',', '') or 0))
        cur = abs(float(str(pr.get('cur_prc', '0')).replace(',', '') or 0))
        pp = cur - base
        y = dict(x, base=base, cur=cur, drift=(base / x['c_prev'] - 1) * 100 if x['c_prev'] else 0.0)
        if x['cd'] in krx_ret:
            y['ret'] = krx_ret[x['cd']]
            y['src_ret'] = 'KRX'
        elif base:
            y['ret'] = pp / base * 100.0
            y['src_ret'] = '키움통합'
        else:
            y['ret'] = None
            y['src_ret'] = '결측'
        out.append(y)
    miss = [y['nm'] for y in out if y['ret'] is None]
    if miss:
        print('결측 %d종목: %s' % (len(miss), ', '.join(miss)), file=sys.stderr)
    return [y for y in out if y['ret'] is not None]


def brinson(S, cash, fut, k200):
    """액티브 = 배분(현금+선물) + 0.975x섹터배분 + 0.975x종목선택 로 닫는 분해."""
    sw = sum(x['mw'] for x in S) / 100.0            # 주식 슬리브 비중 (= 1 - cash)
    bm = sum(x['bm'] / 100.0 * x['ret'] for x in S)
    mp = sum(x['mw'] / 100.0 / sw * x['ret'] for x in S)
    model = sw * mp + fut * k200
    active = model - bm
    alloc = (sw - 1.0) * bm + fut * k200
    sec_a = sel = 0.0
    rowsec = []
    for s in sorted(set(x['sec'] for x in S)):
        g = [x for x in S if x['sec'] == s]
        wb = sum(x['bm'] for x in g) / 100.0
        wp = sum(x['mw'] for x in g) / 100.0 / sw
        rb = sum(x['bm'] / 100.0 * x['ret'] for x in g) / wb if wb else 0.0
        rp = sum(x['mw'] / 100.0 / sw * x['ret'] for x in g) / wp if wp else 0.0
        if wb:
            a = (wp - wb) * (rb - bm)
            sl = wp * (rp - rb)
        else:                       # BM 밖 섹터는 효과 전액을 배분으로 계상
            a = wp * (rp - bm)
            sl = 0.0
        sec_a += a
        sel += sl
        rowsec.append(dict(sec=s, wb=wb * 100, wp=wp * 100, rb=rb, rp=rp,
                           a=a * sw, sl=sl * sw))
    return dict(bm=bm, model_stock=mp, model_nav=model, active=active, alloc=alloc,
                sec_alloc=sec_a * sw, stock_sel=sel * sw, sectors=rowsec,
                residual=alloc + (sec_a + sel) * sw - active)


def skill(S):
    sa = sum(abs(x['ret']) for x in S)
    return dict(
        n=len(S),
        skill_eq=sum(abs(x['ret'] - x['exp']) for x in S) / sa,
        shrink=sum(abs(x['exp']) for x in S) / sa,
        skill_bm=(sum(x['bm'] * abs(x['ret'] - x['exp']) for x in S if x['bm'] > 0) /
                  sum(x['bm'] * abs(x['ret']) for x in S if x['bm'] > 0)),
        mae=sum(abs(x['ret'] - x['exp']) for x in S) / len(S),
        band=sum(1 for x in S if x['lo'] <= x['ret'] <= x['hi']),
        dir_n=sum(1 for x in S if x['dr'] != 'FLAT'),
        dir_hit=sum(1 for x in S if x['dr'] != 'FLAT' and (x['ret'] > 0) == (x['dr'] == 'UP')),
        xsec_sd=math.sqrt(sum((x['ret'] - sum(y['ret'] for y in S) / len(S)) ** 2
                              for x in S) / (len(S) - 1)),
        drift_max=max(abs(x['drift']) for x in S),
        drift_n=sum(1 for x in S if abs(x['drift']) > 0.001),
    )


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('collection')
    ap.add_argument('forecast')
    ap.add_argument('--cash', type=float, default=0.025)
    ap.add_argument('--futures', type=float, default=0.0,
                    help='선물 명목/NAV. 숏이면 음수 (예: -0.0582)')
    ap.add_argument('--k200-ret', type=float, default=0.0, help='KOSPI200 당일 수익률(%%)')
    ap.add_argument('--krx-ret', default='', help='code=ret 쉼표 구분. 거래소 확정 등락률만')
    a = ap.parse_args()
    krx = {}
    for kv in filter(None, a.krx_ret.split(',')):
        k, v = kv.split('=')
        krx[k.strip()] = float(v)
    coll = json.load(open(a.collection, encoding='utf-8'))
    rows = load_forecast(a.forecast)
    S = snapshot_returns(coll, rows, coll.get('base_date'), krx)
    out = brinson(S, a.cash, a.futures, a.k200_ret)
    out['skill'] = skill(S)
    out['base_date'] = coll.get('base_date')
    out['stocks'] = [dict(cd=x['cd'], nm=x['nm'], sec=x['sec'], bm=x['bm'], mw=x['mw'],
                          exp=x['exp'], ret=x['ret'], err=x['ret'] - x['exp'],
                          band=(x['lo'] <= x['ret'] <= x['hi']), src=x['src_ret'],
                          drift=x['drift'],
                          contrib=(x['mw'] - x['bm']) / 100.0 * x['ret']) for x in S]
    assert abs(out['residual']) < 1e-4, '3분해 항등식이 닫히지 않았다: %r' % out['residual']
    json.dump(out, sys.stdout, ensure_ascii=False, indent=1)
    print()


if __name__ == '__main__':
    main()
