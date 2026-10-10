# -*- coding: utf-8 -*-
"""주간 리뷰 채점 — 2026-10-06 ~ 10-08 (3거래일). 전부 실제 계산, 암산 없음.

★대상 주의 거래일이 3일뿐이다★ — 10/5(개천절 대체공휴일)와 10/9(한글날)가 휴장이고
주초 기준점은 10/2(금) 종가다. 종전 회차는 5일 고정이었으므로 일수를 len(days)로 바꿨다.
"""
import json, math, statistics as st

# ───── 실제 (각 회차 마감 리포트·Drive 기록 경유, 야후 정규장 교차) ─────
A = {  # date: (KOSPI종가, KOSPI%, KOSDAQ종가, KOSDAQ%, 삼전, 삼전%, 우, 우%, 하닉, 하닉%, S, R)
 "10/06": (6941.39,-0.8902, 919.92, 2.9812, 272000,-1.4493, 198200,-1.3930, 1773000,-3.6937, -2.4139, 0.9003),
 "10/07": (6803.90,-1.9807, 898.43,-2.3361, 268500,-1.2868, 198000,-0.1009, 1723000,-2.8201, -1.8772,-2.0984),
 "10/08": (6625.93,-2.6157, 892.27,-0.6857, 262000,-2.4209, 194000,-2.0202, 1681000,-2.4376, -2.4066,-2.8539),
}
PREV_WEEK_CLOSE = 7003.74   # 10/2(금) 종가. 10/3 개천절·10/5 대체공휴일 휴장
PREV_WEEK_KOSDAQ = 893.29
PREV_WEEK_STOCKS = {"삼전": 276000, "우": 201000, "하닉": 1841000}

# ───── 아침 브리핑 예측 (Drive kospi_forecast_<YYYYMMDD>_am, 발행 당시 값) ─────
AM = {  # date: (E%, 종가점추정, 80%하단, 80%상단, 삼전%, 우%, 하닉%, 나머지%, 갭%, 시가점추정)
 "10/06": ( 1.0710, 7078.7, 6913.3, 7244.1, None, None, None,    None,  1.0710, 7078.7),
 "10/07": (-1.0243, 6870.3, 6706.4, 7034.2, None, None,-6.7896,  None, -1.0243, 6870.3),
 "10/08": (-0.1000, 6797.1, 6636.4, 6957.8, None, None,-2.3952,  None, -0.1000, 6797.1),
}
# 하닉% 는 각 회차가 적은 ★이론가★를 전일 종가로 나눈 값이다(10/7 1,652,619원 / 10/8 1,681,732원).
# 10/6 회차는 이론가 대신 반증조건 문턱(1,823,000원)만 적었으므로 예측으로 치지 않는다.
# 삼전·우·나머지 블록 예측은 이번 주 세 회차 모두 발행하지 않았다 → None. 표본을 늘리지 않는다.

# 10/8 am 은 패리티 생신호 +0.3918% 를 ★방향 뒤집기 금지 규칙★으로 기각하고 -0.1000% 를 적었다.
AM_RAW_SIGNAL_1008 = 0.3918

# ───── 저녁(전일 발행) 예측 ─────
PM = {"10/06": -0.112, "10/07": 0.0884, "10/08": -0.4336}
PM_POINT = {"10/06": 6995.9, "10/07": 6947.53, "10/08": 6774.40}
# 10/8 pm 만 80% 구간을 남겼다(하단 6636.02, z=1.2816 — R-B 미준수본)
PM_BAND = {"10/08": (6636.02, None)}

# ───── 실제 시가 (갭 채점용) ─────
OPEN = {"10/06": 7044.67, "10/07": 6864.25, "10/08": 6808.68}

days = list(A.keys())
n = len(days)
out = {"days": days, "n": n}

# ── 주간 궤적 ──
wk_ret = (A["10/08"][0]/PREV_WEEK_CLOSE - 1)*100
out["week"] = {
  "start_ref": PREV_WEEK_CLOSE, "end": A["10/08"][0], "ret": round(wk_ret,4),
  "kosdaq_ret": round((A["10/08"][2]/PREV_WEEK_KOSDAQ-1)*100,4),
  "삼전": round((A["10/08"][4]/PREV_WEEK_STOCKS["삼전"]-1)*100,4),
  "우":   round((A["10/08"][6]/PREV_WEEK_STOCKS["우"]-1)*100,4),
  "하닉": round((A["10/08"][8]/PREV_WEEK_STOCKS["하닉"]-1)*100,4),
}
out["week"]["kospi_minus_kosdaq"] = round(out["week"]["ret"]-out["week"]["kosdaq_ret"],4)

# ── 일별 채점 ──
rows=[]
for d in days:
    act=A[d][1]; am=AM[d][0]; pm=PM[d]
    e_am = act-am
    e_pm = (act-pm) if pm is not None else None
    gap_act = (OPEN[d]/ (PREV_WEEK_CLOSE if d==days[0] else A[days[days.index(d)-1]][0]) -1)*100
    rows.append({
      "d":d, "act":act, "close":A[d][0],
      "am":am, "pm":pm,
      "e_am":round(e_am,4), "e_pm":(round(e_pm,4) if e_pm is not None else None),
      "close_err_am":round(A[d][0]-AM[d][1],2),
      "close_err_pm":round(A[d][0]-PM_POINT[d],2),
      "inband_am": AM[d][2] <= A[d][0] <= AM[d][3],
      "dir_am": (act>0)==(am>0),
      "dir_pm": ((act>0)==(pm>0)) if pm is not None else None,
      "skill_am": round(abs(e_am)/abs(act),4),
      "skill_pm": (round(abs(e_pm)/abs(act),4) if e_pm is not None else None),
      "gap_act": round(gap_act,4), "gap_pred": AM[d][8],
      "gap_err": round(gap_act-AM[d][8],4) if AM[d][8] is not None else None,
      "intraday": round((A[d][0]/OPEN[d]-1)*100,4),
    })
out["daily"]=rows

# 10/8 pm 구간 이탈 폭 / 10/8 am 구간 이탈 폭
out["band_miss"]={
 "pm_1008": round(A["10/08"][0]-PM_BAND["10/08"][0],2),
 "am_1008": round(A["10/08"][0]-AM["10/08"][2],2),
}

# ── 주간 집계 ──
e_am_l=[r["e_am"] for r in rows]
e_pm_l=[r["e_pm"] for r in rows if r["e_pm"] is not None]
act_l=[r["act"] for r in rows]
out["agg"]={
 "am_MAE": round(sum(abs(x) for x in e_am_l)/len(e_am_l),4),
 "am_bias":round(sum(e_am_l)/len(e_am_l),4),
 "am_RMSE":round(math.sqrt(sum(x*x for x in e_am_l)/len(e_am_l)),4),
 "am_skill":round(sum(abs(x) for x in e_am_l)/sum(abs(x) for x in act_l),4),
 "pm_MAE": round(sum(abs(x) for x in e_pm_l)/len(e_pm_l),4),
 "pm_bias":round(sum(e_pm_l)/len(e_pm_l),4),
 "pm_RMSE":round(math.sqrt(sum(x*x for x in e_pm_l)/len(e_pm_l)),4),
 "pm_skill":round(sum(abs(x) for x in e_pm_l)/sum(abs(x) for x in act_l),4),
 "pm_n":len(e_pm_l),
 "dir_am": sum(1 for r in rows if r["dir_am"]), "dir_am_n":len(rows),
 "dir_pm": sum(1 for r in rows if r["dir_pm"]), "dir_pm_n":len(e_pm_l),
 "inband_am": sum(1 for r in rows if r["inband_am"]), "inband_n":len(rows),
 "gap_MAE": round(sum(abs(r["gap_err"]) for r in rows if r["gap_err"] is not None)/
                  sum(1 for r in rows if r["gap_err"] is not None),4),
}
# 중심 수축 = |E|평균 / |실현|평균
out["agg"]["shrink_am"]=round((sum(abs(AM[d][0]) for d in days)/n)/(sum(abs(A[d][1]) for d in days)/n),4)
out["agg"]["shrink_pm"]=round((sum(abs(PM[d]) for d in days)/n)/(sum(abs(A[d][1]) for d in days)/n),4)

# ── 아침 vs 저녁: 간밤 미 세션 정보의 정량 가치 ──
out["am_vs_pm"]=[{"d":r["d"],"am":abs(r["e_am"]),"pm":abs(r["e_pm"]),
                  "value":round(abs(r["e_pm"])-abs(r["e_am"]),4)} for r in rows]
out["am_vs_pm_mean"]=round(sum(x["value"] for x in out["am_vs_pm"])/n,4)

# ── 블록별 채점 (이번 주는 하닉 이론가 2건만 발행됐다) ──
blk={}
hy=[(d, A[d][9]-AM[d][6]) for d in days if AM[d][6] is not None]
blk["하닉"]={"n":len(hy),"errs":[(d,round(e,4)) for d,e in hy],
             "MAE":round(sum(abs(e) for _,e in hy)/len(hy),4),
             "bias":round(sum(e for _,e in hy)/len(hy),4)}
for k in ("삼전","우","나머지"):
    blk[k]={"n":0,"note":"이번 주 세 회차 모두 블록 예측 미발행 → 채점 불가"}
out["block"]=blk

# ── 반도체 S vs 나머지 R ──
out["SR"]={"S":[A[d][10] for d in days],"R":[A[d][11] for d in days],
  "S_compound": round((math.prod([1+A[d][10]/100 for d in days])-1)*100,4),
  "R_compound": round((math.prod([1+A[d][11]/100 for d in days])-1)*100,4),
  "반대부호_일수": sum(1 for d in days if A[d][10]*A[d][11]<0),
  "설명도": {d: round(A[d][10]*0 + 0,4) for d in days},
}
out["SR"]["spread"]=round(out["SR"]["S_compound"]-out["SR"]["R_compound"],4)

# ── 설명도 (각 회차가 발행한 값) ──
out["explain"]={"10/06":146.5,"10/07":50.41,"10/08":48.99}

# ── 주간 실현변동성 ──
rets=[A[d][1] for d in days]
sig_rms=math.sqrt(sum(x*x for x in rets)/len(rets))
sig_sd=st.stdev(rets)
out["sigma"]={"일간_RMS":round(sig_rms,4),"일간_표본SD":round(sig_sd,4),
  "주간환산_RMS":round(sig_rms*math.sqrt(n),4),
  "최대일간":max(rets,key=abs),
  "am_내재σ_10/08":round((AM["10/08"][3]-AM["10/08"][2])/2/AM["10/08"][1]*100/1.476,4),
}
print(json.dumps(out,ensure_ascii=False,indent=1))
json.dump(out,open('wk.json','w'),ensure_ascii=False)
