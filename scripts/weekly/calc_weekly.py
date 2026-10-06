# -*- coding: utf-8 -*-
"""주간 리뷰 계산 전량. 암산 없음 — 모든 수치는 여기서 나온다."""
import json, math, statistics as st
R=json.load(open('kw_weekly2.json'))['results']
US=json.load(open('us.json'))
O={}

# ───────── 1. 지수·환율·금리 ─────────
ki=R['index_kospi']['data']; kq=R['index_kosdaq']['data']; k2=R['index_kospi200']['data']
def f(x): return float(str(x).replace(',','').lstrip('+-'))
O['kospi_1002']=dict(close=f(ki['cur_prc']), chg=f(ki['pred_pre']), rt=f(ki['flu_rt']),
  op=f(ki['open_pric']), hi=f(ki['high_pric']), lo=f(ki['low_pric']),
  prica=f(ki['trde_prica'])/1e6, up=int(ki['rising']), dn=int(ki['fall']), flat=int(ki['stdns']),
  hi52=f(ki['52wk_hgst_pric']), hi52dt=ki['52wk_hgst_pric_dt'], hi52gap=float(str(ki['52wk_hgst_pric_pre_rt']).replace(',','').replace('+','')),
  lo52=f(ki['52wk_lwst_pric']), lo52dt=ki['52wk_lwst_pric_dt'], lo52gap=float(str(ki['52wk_lwst_pric_pre_rt']).replace(',','').replace('+','')))
O['kosdaq_1002']=dict(close=f(kq['cur_prc']), rt=f(kq['flu_rt']), prica=f(kq['trde_prica'])/1e6)
FX={'0923':1360.0,'0928':1352.0,'0929':1360.0,'0930':1358.4,'1001':1355.7,'1002':1359.6}
O['fx']=FX
O['fx_wk']=(FX['1002']/FX['0923']-1)*100
O['rates']={k:R['ecos_'+k]['data'] for k in ['ktb_3y','ktb_10y','ktb_30y','cd_91d','corp_bond_aa3y']}

# ───────── 2. 5블록 주간 분해 ─────────
# 기준주가: 9/23 종가는 9/28 일간등락률로 역산(자기정합), 10/2 종가는 ka10066(★키움 통합가★ —
#          KRX 정규장 확정치와 최대 0.25%p 어긋난다, collection-contract 8-3e)
S0={'삼성전자':285500.0,'삼성전자우':220000.0,'SK하이닉스':1862000.0}
S1={'삼성전자':276000.0,'삼성전자우':201500.0,'SK하이닉스':1842000.0}
IDX0, IDX1 = 7080.92, O['kospi_1002']['close']
r_idx=(IDX1/IDX0-1)*100
W1={'삼성전자':0.280724,'삼성전자우':0.028547,'SK하이닉스':0.232962}   # 10/2 기준 시총비중
rb={k:(S1[k]/S0[k]-1)*100 for k in S0}
W0={k: W1[k]*(1+r_idx/100)/(1+rb[k]/100) for k in S0}
W0['나머지']=1-sum(W0[k] for k in S0)
W1['나머지']=1-sum(W1[k] for k in S0)
contrib={k:W0[k]*rb[k] for k in S0}
r_rest=(r_idx-sum(contrib.values()))/W0['나머지']
contrib['나머지']=W0['나머지']*r_rest
rb['나머지']=r_rest
wS=sum(W0[k] for k in S0); rS=sum(contrib[k] for k in S0)/wS
O['block']=dict(r_idx=r_idx, S0=S0, S1=S1, W0=W0, W1=W1, rb=rb, contrib=contrib,
  r_rest=r_rest, wS=wS, rS=rS, spread=rS-r_rest,
  residual=r_idx-sum(contrib.values()))

# ───────── 3. EWY 이론가 대비 괴리 (일별 프리미엄 변화 → 익일 선행성 검증) ─────────
KO={'0928':-2.6999,'0929':-0.2748,'0930':-0.4769,'1001':1.9495,'1002':0.4646}
EWYpx=US['EWY']['px']
ed=['20260925','20260928','20260929','20260930','20261001','20261002']
prem=[]
keys=['0928','0929','0930','1001','1002']
for i,d in enumerate(keys):
    prev='0923' if i==0 else keys[i-1]
    dfx=(FX[d]/FX[prev]-1)
    rtheo=((1+KO[d]/100)/(1+dfx)-1)*100
    rewy=(EWYpx[ed[i+1]]/EWYpx[ed[i]]-1)*100
    prem.append(dict(d=d, kospi=KO[d], dfx=dfx*100, rtheo=rtheo, ewy=rewy, prem=rewy-rtheo,
                     nxt_kospi=(KO[keys[i+1]] if i+1<len(keys) else None)))
O['prem']=prem
sig=[p['prem'] for p in prem if p['nxt_kospi'] is not None]
nxt=[p['nxt_kospi'] for p in prem if p['nxt_kospi'] is not None]
hit=sum(1 for a,b in zip(sig,nxt) if (a>0)==(b>0))
ms,mn=sum(sig)/len(sig), sum(nxt)/len(nxt)
cov=sum((a-ms)*(b-mn) for a,b in zip(sig,nxt))/len(sig)
cor=cov/(st.pstdev(sig)*st.pstdev(nxt))
_n=len(sig); _t=cor*math.sqrt(_n-2)/math.sqrt(1-cor*cor)
# df=2 양측 p (t분포 CDF 해석해)
_p=1-abs(_t)/math.sqrt(2+_t*_t)
O['prem_test']=dict(n=_n, hit=hit, corr=cor, sig=sig, nxt=nxt, last=prem[-1]['prem'], t=_t, p=_p)

# ───────── 4. KODEX / 스프레드 삼각형 ─────────
kd={r['dt']:f(r['cur_prc']) for r in list(R['basket_kodex_msci_korea_daily']['data'].values() if 0 else [])} if 0 else None
for kk,vv in R['basket_kodex_msci_korea_daily']['data'].items():
    if isinstance(vv,list) and vv: kd={r['dt']:f(r['cur_prc']) for r in vv}; break
O['kodex']=dict(d1002=kd['20261002'], d0923=kd['20260923'],
  wk=(kd['20261002']/kd['20260923']-1)*100,
  pred=0.6574*rS+0.3426*r_rest, hist={d:kd[d] for d in ['20260923','20260928','20260929','20260930','20261001','20261002']})
O['kodex']['gap']=O['kodex']['wk']-O['kodex']['pred']
O['ewy_tri']=dict(pred_krw=0.4428*rS+0.5572*r_rest,
  act_usd=US['EWY']['wk'], act_krw=(1+US['EWY']['wk']/100)*(1+O['fx_wk']/100)*100-100)
O['ewy_tri']['gap']=O['ewy_tri']['act_krw']-O['ewy_tri']['pred_krw']

# ───────── 5. 수급 (ka10066 백만원 → 억원 /100) ─────────
rows=R['investor_after_close']['data']['opaf_invsr_trde']
def nn(s):
    s=str(s).replace(',','').strip()
    neg=s.startswith('-') or s.startswith('--')
    s=s.lstrip('+-')
    try: v=float(s)
    except: return 0.0
    return -v if neg else v
idx={r['stk_cd']:r for r in rows}
TGT=[('005930','삼성전자'),('005935','삼성전자우'),('000660','SK하이닉스'),('402340','SK스퀘어'),
     ('034020','두산에너빌리티'),('373220','LG에너지솔루션'),('009150','삼성전기'),('005380','현대차')]
flow={}
for cd,nm in TGT:
    r=idx[cd]
    flow[nm]=dict(close=abs(nn(r['cur_prc'])), frg=nn(r['frgnr_invsr'])/100, org=nn(r['orgn'])/100,
      ind=nn(r['ind_invsr'])/100, etc=nn(r['etc_corp'])/100, inv=nn(r['invtrt'])/100,
      pen=nn(r['penfnd_etc'])/100, fin=nn(r['fnnc_invt'])/100)
O['flow']=flow
sf=R['sector_investor_flows_kospi']['data']['inds_netprps'][0]   # 종합(KOSPI), 억원
O['mkt_flow']=dict(frg=nn(sf['frgnr_netprps']), org=nn(sf['orgn_netprps']), ind=nn(sf['ind_netprps']),
  etc=nn(sf['etc_corp_netprps']), sc=nn(sf['sc_netprps']), inv=nn(sf['invtrt_netprps']),
  pen=nn(sf['endw_netprps']), samo=nn(sf['samo_fund_netprps']), ins=nn(sf['insrnc_netprps']))
O['mkt_flow']['sum']=sum(O['mkt_flow'][k] for k in ['frg','org','ind','etc'])
pt=R['program_trades_kospi']['data']['prm_trde_trnsn'][0]
O['prog']=dict(dfrt=nn(pt['dfrt_trde_netprps'])/100, ndfrt=nn(pt['ndiffpro_trde_netprps'])/100,
  all=nn(pt['all_netprps'])/100, k200=f(pt['kospi200']), basis=f(pt['basis']))

# ───────── 6. 공매도 ─────────
ss={}
for nm in ['삼성전자','삼성전자우','SK하이닉스','SK스퀘어','두산에너빌리티','LG에너지솔루션','삼성전기','현대차']:
    rs=[r for r in R['short_selling_'+nm]['data']['shrts_trnsn'] if '20260928'<=r['dt']<='20261002']
    sq=sum(f(r['shrts_qty']) for r in rs); tq=sum(f(r['trde_qty']) for r in rs)
    ss[nm]=dict(wght=sq/tq*100, byday={r['dt'][4:]:f(r['trde_wght']) for r in rs})
O['short']=ss

# ───────── 7. 업종 ─────────
sec=[(r['stk_nm'], f(r['flu_rt'])*(-1 if str(r['flu_rt']).startswith('-') else 1)) for r in R['sector_indices_kospi']['data']['all_inds_idex']]
sec=[(a,b) for a,b in sec if a not in ('종합(KOSPI)','대형주','중형주','소형주','변동성지수')]
O['sector_top']=sorted(sec,key=lambda x:-x[1])[:6]
O['sector_bot']=sorted(sec,key=lambda x:x[1])[:6]

# ───────── 8. 주봉 ─────────
wk={}
for nm in ['삼성전자','삼성전자우','SK하이닉스','SK스퀘어','두산에너빌리티','LG에너지솔루션','삼성전기','현대차']:
    r=R['candle_weekly_'+nm]['data']['stk_stk_pole_chart_qry'][0]
    o,h,l,c=f(r['open_pric']),f(r['high_pric']),f(r['low_pric']),f(r['cur_prc'])
    wk[nm]=dict(o=o,h=h,l=l,c=c,rng=(h-l)/l*100,prica=f(r['trde_prica'])/1e12,
                pos=(c-l)/(h-l)*100)
O['wkcandle']=wk
O['us']=US
json.dump(O,open('calcw.json','w'),ensure_ascii=False,indent=1)
print(json.dumps(O,ensure_ascii=False,indent=1)[:200])
print()
print('r_idx %.4f  삼전 %.4f 우 %.4f 하닉 %.4f 나머지 %.4f'%(r_idx,rb['삼성전자'],rb['삼성전자우'],rb['SK하이닉스'],r_rest))
print('W0',{k:round(v,6) for k,v in W0.items()})
print('기여',{k:round(v,4) for k,v in contrib.items()},'합 %.6f  잔차 %.2e'%(sum(contrib.values()),O['block']['residual']))
print('반도체 wS %.4f rS %.4f  스프레드 %.4f%%p'%(wS,rS,O['block']['spread']))
print('프리미엄 n=%d hit=%d corr=%.4f last=%+.4f'%(O['prem_test']['n'],O['prem_test']['hit'],O['prem_test']['corr'],O['prem_test']['last']))
print('KODEX 주간 %.4f pred %.4f gap %.4f'%(O['kodex']['wk'],O['kodex']['pred'],O['kodex']['gap']))
print('EWY tri', {k:round(v,4) for k,v in O['ewy_tri'].items()})
print('시장수급(억) ',{k:round(v) for k,v in O['mkt_flow'].items()})
print('프로그램(억) ',{k:round(v,1) for k,v in O['prog'].items()})
