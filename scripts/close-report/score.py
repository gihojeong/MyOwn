# -*- coding: utf-8 -*-
import json
c = json.load(open("calc_out.json"))
ACT = c["act"]; KP=6715.41
W = {"삼성전자":0.26661822,"삼성전자우":0.02801082,"SK하이닉스":0.23020900,
     "상위31기타":0.24728182,"32위이하":0.22788016}
REAL = {"삼성전자":3.37,"삼성전자우":1.45,"SK하이닉스":6.42,
        "상위31기타":c["r_other31"],"32위이하":c["small_r"]}
AM  = {"삼성전자":1.8440,"삼성전자우":1.9260,"SK하이닉스":2.2960,"상위31기타":0.2000,"32위이하":0.0980}
EVE = {"삼성전자":0.4780,"삼성전자우":0.4880,"SK하이닉스":0.6560,"상위31기타":-0.2120,"32위이하":-0.1560}
AM_PW, EVE_PW = 1.14594026, 0.20415639
print("=== [F] 예측 대비 괴리 ===")
print("  실제 KOSPI %+.6f%%  종가 6894.23" % ACT)
for nm,pw,pt in [("아침(_am)",AM_PW,6792.36),("어제저녁",EVE_PW,6729.12)]:
    print("  %-10s 확률가중 %+.6f%% 점추정 %.2f -> 괴리 %+.6f%%p / %+.2fp" % (nm,pw,pt,ACT-pw,6894.23-pt))
print("\n  아침 시나리오별 괴리:")
for nm,v,lo,hi in [("상방40%",2.178214,6860,6960),("기본42%",0.982141,6760,6860),("하방18%",-0.765803,6660,6760)]:
    hit = "★밴드 적중" if lo<=6894.23<=hi else "미적중"
    print("    %-8s %+.6f%% -> 괴리 %+.6f%%p  밴드 %d~%d %s" % (nm,v,ACT-v,lo,hi,hit))
gap_p, gap_a = 1.206392, 6885.70/6715.41*100-100
print("\n  시가갭: 예측 %+.6f%%(6,796.42) vs 실제 %+.6f%%(6,885.70) -> 괴리 %+.6f%%p ★부호 적중(4회만에 첫 방향 적중)" % (gap_p,gap_a,gap_a-gap_p))
print("  80%% 구간 6,594.6~6,990.1 -> %s" % ("★적중" if 6594.6<=6894.23<=6990.1 else "미적중"))

print("\n=== 블록별 괴리 (아침 기준) ===")
tot=0.0
print("  블록          비중        예측%     실제%     괴리%p    배율    기여오차%p")
for k in W:
    dev = REAL[k]-AM[k]; att = W[k]*dev; tot+=att
    mul = REAL[k]/AM[k] if AM[k]!=0 else float('nan')
    print("  %-12s %.8f %+8.4f %+8.4f %+8.4f %7.2f배 %+10.6f" % (k,W[k],AM[k],REAL[k],dev,mul,att))
print("  합계 기여오차 = %+.6f %%p   vs 실제괴리 %+.6f %%p -> ★모델잔차 %+.2e %%p" % (tot, ACT-AM_PW, tot-(ACT-AM_PW)))
semi = sum(W[k]*(REAL[k]-AM[k]) for k in ["삼성전자","삼성전자우","SK하이닉스"])
rest = tot-semi
print("  반도체 3블록 %+.6f%%p (%.1f%%) / 비반도체 2블록 %+.6f%%p (%.1f%%)" % (semi,semi/tot*100,rest,rest/tot*100))
print("  KOSDAQ: 예측 +0.55%% vs 실제 +0.60%% -> 괴리 +0.05%%p ★베타 폐기·독립추정 적중")

# ---------- 내일(9/21 월) 시나리오 ----------
print("\n=== [G] 2026-09-21(월) 시나리오 ===")
W21 = {}
raw={}
for k in W:
    raw[k]=W[k]*(1+REAL[k]/100.0)
s=sum(raw.values())
for k in raw: W21[k]=raw[k]/s
print("  9/21 시작 비중(9/18 종가 기준):")
for k in W21: print("    %-12s %.8f" % (k,W21[k]))
print("    합 검산 = %.10f" % sum(W21.values()))

SC = {
 "삼성전자":     (+1.20,-0.40,-2.80),
 "삼성전자우":   (+1.30,-0.30,-2.60),
 "SK하이닉스":   (+1.60,-0.70,-3.80),
 "상위31기타":   (+1.00,+0.30,-1.00),
 "32위이하":     (+0.80,+0.20,-0.90),
}
P = (0.30,0.44,0.26)
idx=[0.0,0.0,0.0]
for k in SC:
    for j in range(3): idx[j]+=W21[k]*SC[k][j]
print("\n  블록          비중        상방30%   기본44%   하방26%   확률가중")
for k in SC:
    pw=sum(P[j]*SC[k][j] for j in range(3))
    print("  %-12s %.8f %+8.2f %+8.2f %+8.2f  %+8.4f" % (k,W21[k],SC[k][0],SC[k][1],SC[k][2],pw))
print("  유도 지수                  %+8.6f %+8.6f %+8.6f" % tuple(idx))
pw_idx=sum(P[j]*idx[j] for j in range(3))
bu=sum(W21[k]*sum(P[j]*SC[k][j] for j in range(3)) for k in SC)
print("\n  prob_weighted = %.2f(%+.6f) + %.2f(%+.6f) + %.2f(%+.6f) = ★%+.8f%%" % (P[0],idx[0],P[1],idx[1],P[2],idx[2],pw_idx))
print("  바텀업 검산 = %+.8f%% -> ★잔차 %+.2e %%p" % (bu, bu-pw_idx))
K=6894.23
print("  점추정 종가 = 6894.23 x (1%+.8f) = ★%.2f (%+.2fp)" % (pw_idx/100, K*(1+pw_idx/100), K*pw_idx/100))
for j,nm in enumerate(["상방","기본","하방"]):
    print("    %s: %+.6f%% -> %.2f" % (nm, idx[j], K*(1+idx[j]/100)))

# sigma
import math
rets=[-0.854381,1.368741,-0.038107,2.662831]
m=sum(rets)/len(rets); var=sum((x-m)**2 for x in rets)/(len(rets)-1); sd=math.sqrt(var)
print("\n  최근4일 등락률:", ["%+.6f"%x for x in rets])
print("  표본 sigma(ddof=1) = %.6f%%" % sd)
shrunk=0.55*sd+0.45*1.85
vk=43.56/math.sqrt(252)
mix=0.70*shrunk+0.30*vk
final=mix*1.08
print("  사전 1.85%% 수축 w=0.55 -> %.6f%% / VKOSPI 43.56 -> 일간 %.6f%%" % (shrunk,vk))
print("  혼합 0.70x%.6f + 0.30x%.6f = %.6f%%" % (shrunk,vk,mix))
print("  ★추석 연휴(9/24~26) 직전주 + 주말갭 할증 x1.08 -> sigma_final = %.6f%%" % final)
h=1.2815516*final
print("  ci80 반폭 = %.6f%% -> ★KOSPI 종가 80%% 구간 %.1f ~ %.1f" % (h, K*(1-h/100), K*(1+h/100)))
for nm,px,sg in [("삼성전자",261000,2.613),("삼성전자우",196100,2.613),("SK하이닉스",1857000,3.067)]:
    pw=sum(P[j]*SC[nm][j] for j in range(3))
    print("  %-10s 점추정 %.0f (%+.3f%%) / 상방 %.0f / 기본 %.0f / 하방 %.0f" % (
        nm, px*(1+pw/100), pw, px*(1+SC[nm][0]/100), px*(1+SC[nm][1]/100), px*(1+SC[nm][2]/100)))
json.dump({"W21":W21,"idx":idx,"pw":pw_idx,"sigma":final,"ci":h},open("fc.json","w"),ensure_ascii=False)
