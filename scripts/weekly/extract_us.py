# -*- coding: utf-8 -*-
import json
R=json.load(open('kw_weekly2.json'))['results']
def p(s):
    s=str(s).replace(',','').strip().lstrip('+-')
    return float(s)
US={'SPY':'us_sp500_spy','QQQ':'us_nasdaq100_qqq','DIA':'us_dow_dia','SOXX':'us_semis_soxx',
    'NVDA':'us_nvidia','TSM':'us_tsmc','MU':'us_micron','AVGO':'us_broadcom','EWY':'us_ewy_korea_etf',
    'GLD':'us_gold_gld','USO':'us_wti_uso','TLT':'us_ustreasury20y_tlt','UUP':'us_dollar_uup',
    'SKM':'us_adr_sk_telecom','KB':'us_adr_kb_financial'}
out={}
print('%-6s %9s %9s %9s %9s %9s %9s | %8s %8s %8s'%('','0925','0928','0929','0930','1001','1002','주간','9/25→10/1','10/2일간'))
for t,k in US.items():
    v=R[k]['data']
    rows=None
    for kk,vv in v.items():
        if isinstance(vv,list) and vv: rows=vv; break
    d={r['dt']:p(r.get('cur_prc') or r.get('close_pric')) for r in rows}
    ds=['20260925','20260928','20260929','20260930','20261001','20261002']
    c=[d.get(x) for x in ds]
    wk=(c[5]/c[0]-1)*100
    thru1=(c[4]/c[0]-1)*100
    d1=(c[5]/c[4]-1)*100
    out[t]=dict(px=dict(zip(ds,c)), wk=wk, thru_1001=thru1, d_1002=d1)
    print('%-6s %9.2f %9.2f %9.2f %9.2f %9.2f %9.2f | %+7.2f%% %+7.2f%% %+7.2f%%'%(t,*c,wk,thru1,d1))
json.dump(out,open('us.json','w'))
