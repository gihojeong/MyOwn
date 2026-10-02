# -*- coding: utf-8 -*-
"""주간 리뷰 채점 — 2026-09-28 ~ 10-02 (5거래일). 전부 실제 계산, 암산 없음."""
import json, math, statistics as st

# ───── 실제 (KRX 확정, 각 회차 리포트·마감 리포트 경유) ─────
A = {  # date: (KOSPI종가, KOSPI%, KOSDAQ종가, KOSDAQ%, 삼전, 삼전%, 우, 우%, 하닉, 하닉%, S, R)
 "09/28": (6889.74,-2.6999, 846.58, 0.25, 270000,-5.43, 207000,-5.91, 1768000,-5.05, -5.2952, 0.4608),
 "09/29": (6870.81,-0.2748, 849.80, 0.38, 272500, 0.93, 204000,-1.45, 1765000,-0.17,  0.3319,-0.9713),
 "09/30": (6838.04,-0.4769, 855.91, 0.7190,268500,-1.47, 195200,-4.31, 1776000, 0.62, -0.7379,-0.1733),
 "10/01": (6971.35, 1.9495, 894.29, 4.48, 276000, 2.79, 204500, 4.76, 1833000, 3.21,  3.0722, 0.6509),
 "10/02": (7003.74, 0.4646, 893.29,-0.11, 276000, 0.00, 201000,-1.71, 1841000, 0.44,  0.0990, 0.8980),
}
PREV_WEEK_CLOSE = 7080.92   # 9/23 종가 (추석 9/24~25 휴장)

# ───── 아침 브리핑 예측 ─────
AM = {  # date: (E%, 종가점추정, 80%하단, 80%상단, 삼전%, 우%, 하닉%, 나머지%, 갭%, 시가점추정)
 "09/28": (-0.6284, 7036.4, 6864.6, 7208.3, -0.44, -0.495, -1.00, None,   -0.2801, 7061.1),
 "09/29": (-0.2464, 6872.77,6781.06,7027.62, -1.088,-1.795, 0.490, 0.039, -0.0536, 6886.05),
 "09/30": ( 0.4880, 6904.34,6781.06,7027.62,  0.528, 0.328, 1.371, 0.039,  0.6177, 6913.25),
 "10/01": (-0.1412, 6828.4, 6705.7, 6951.1, -0.115,-0.525, 0.785,-0.270, -0.0710, 6833.2),
 "10/02": ( 0.4172, 7000.43,6870.88,7129.98,  0.475, 0.190, 1.205,-0.005,  0.4500, 7002.72),
}
# 9/29 아침은 중복 발송 — 06:24 예약본(별건)
AM_DUP_0929 = -0.50

# ───── 저녁(전일 발행) 예측 ─────
PM = {"09/28": -0.1417, "09/29": -0.6300, "09/30": None, "10/01": -0.0947, "10/02": -0.1824}
# 09/30 저녁분 없음 = 9/29 마감 리포트 미발행(루틴 비활성)

days = list(A.keys())
out = {}

# ── 주간 궤적 ──
wk_ret = (A["10/02"][0]/PREV_WEEK_CLOSE - 1)*100
out["week"] = {"start_ref": PREV_WEEK_CLOSE, "end": A["10/02"][0], "ret": round(wk_ret,4),
               "kosdaq_ret": round((A["10/02"][2]/844.48-1)*100,4),
               "삼전": round((276000/285500-1)*100,4), "우": round((201000/220000-1)*100,4),
               "하닉": round((1841000/1862000-1)*100,4)}

# ── 일별 채점 ──
rows=[]
for d in days:
    act = A[d][1]; am = AM[d][0]; pm = PM[d]
    e_am = act - am                      # 오차 = 실제 - 예측
    e_pm = (act - pm) if pm is not None else None
    close_err = A[d][0] - AM[d][1]
    inband = AM[d][2] <= A[d][0] <= AM[d][3]
    gap_act = (0 if d=="09/28" else None)
    rows.append({"d":d,"act":act,"am":am,"pm":pm,"e_am":round(e_am,4),
                 "e_pm":(round(e_pm,4) if e_pm is not None else None),
                 "close_err":round(close_err,2),"inband":inband,
                 "dir_am": (act>0)==(am>0), "dir_pm": ((act>0)==(pm>0)) if pm is not None else None})
out["daily"]=rows

# ── 주간 집계 ──
e_am_l=[r["e_am"] for r in rows]
e_pm_l=[r["e_pm"] for r in rows if r["e_pm"] is not None]
out["agg"]={
 "am_MAE": round(sum(abs(x) for x in e_am_l)/len(e_am_l),4),
 "am_bias":round(sum(e_am_l)/len(e_am_l),4),
 "am_RMSE":round(math.sqrt(sum(x*x for x in e_am_l)/len(e_am_l)),4),
 "pm_MAE": round(sum(abs(x) for x in e_pm_l)/len(e_pm_l),4),
 "pm_bias":round(sum(e_pm_l)/len(e_pm_l),4),
 "pm_n":len(e_pm_l),
 "dir_am": sum(1 for r in rows if r["dir_am"]), "dir_am_n":len(rows),
 "dir_pm": sum(1 for r in rows if r["dir_pm"]), "dir_pm_n":len(e_pm_l),
 "inband": sum(1 for r in rows if r["inband"]), "inband_n":len(rows),
}
# 9/29 중복 발송본 비교
out["dup_0929"]={"예약본_E":AM_DUP_0929,"예약본_오차":round(A["09/29"][1]-AM_DUP_0929,4),
                 "수동본_E":AM["09/29"][0],"수동본_오차":round(A["09/29"][1]-AM["09/29"][0],4)}

# ── 블록별 채점 (삼전/우/하닉/나머지) ──
blk={}
for k,ai,pi in (("삼전",5,4),("우",7,5),("하닉",9,6)):
    errs=[]
    for d in days:
        a=A[d][ai]; p=AM[d][pi]
        errs.append(a-p)
    blk[k]={"MAE":round(sum(abs(x) for x in errs)/5,4),"bias":round(sum(errs)/5,4),
            "errs":[round(x,3) for x in errs]}
errs_R=[]
for d in days:
    p=AM[d][7]
    if p is None: continue
    errs_R.append(A[d][11]-p)
blk["나머지"]={"MAE":round(sum(abs(x) for x in errs_R)/len(errs_R),4),
               "bias":round(sum(errs_R)/len(errs_R),4),"n":len(errs_R),
               "errs":[round(x,3) for x in errs_R]}
out["block"]=blk

# ── 반도체 S vs 나머지 R 주간 ──
out["SR"]={"S":[A[d][10] for d in days],"R":[A[d][11] for d in days],
           "S_sum_compound": round(((math.prod([1+A[d][10]/100 for d in days]))-1)*100,4),
           "R_sum_compound": round(((math.prod([1+A[d][11]/100 for d in days]))-1)*100,4),
           "반대부호_일수": sum(1 for d in days if A[d][10]*A[d][11]<0)}

# ── 오차 귀속 (9/29·9/30·10/1·10/2 — 블록 예측이 있는 4일) ──
W={"09/29":(0.281234,0.028893,0.227590,0.462283),
   "09/30":(0.281234,0.028893,0.227590,0.462283),
   "10/01":(0.278428,0.027780,0.230099,0.463693),
   "10/02":(0.280724,0.028547,0.232962,0.457767)}
attr=[]
for d in ["09/29","09/30","10/01","10/02"]:
    w=W[d]; a=A[d]; p=AM[d]
    c=[w[0]*(a[5]-p[4]), w[1]*(a[7]-p[5]), w[2]*(a[9]-p[6]), w[3]*(a[11]-p[7])]
    tot=sum(c)
    attr.append({"d":d,"삼전":round(c[0],4),"우":round(c[1],4),"하닉":round(c[2],4),
                 "나머지":round(c[3],4),"합":round(tot,4),"실제오차":round(a[1]-p[0],4)})
out["attr"]=attr
tot4=[sum(x) for x in zip(*[[r["삼전"],r["우"],r["하닉"],r["나머지"]] for r in attr])]
grand=sum(abs(x) for x in tot4)
out["attr_share"]={n:round(abs(v)/grand*100,2) for n,v in zip(["삼전","우","하닉","나머지"],tot4)}
out["attr_sum"]={n:round(v,4) for n,v in zip(["삼전","우","하닉","나머지"],tot4)}

# ── 주간 실현변동성 ──
rets=[A[d][1] for d in days]
sig_rms=math.sqrt(sum(x*x for x in rets)/len(rets))
sig_sd=st.stdev(rets)
out["sigma"]={"일간_RMS":round(sig_rms,4),"일간_표본SD":round(sig_sd,4),
              "주간환산_RMS":round(sig_rms*math.sqrt(5),4),
              "최대일간":max(rets,key=abs)}
print(json.dumps(out,ensure_ascii=False,indent=1))
json.dump(out,open('wk.json','w'),ensure_ascii=False)
