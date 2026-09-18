# -*- coding: utf-8 -*-
import json
c = json.load(open("calc_out.json"))
rows = c["rows"]
raw = [(nm,cd,c18,r18,w18*(1+r18/100.0)) for i,nm,cd,c18,r18,w18,wf,con in rows]
small_raw = c["w_small"]*(1+c["small_r"]/100.0)
tot = sum(x[4] for x in raw)+small_raw
TOTMC = 5684.0  # 조원
print("# 종목 코드 종가 등락률% 시총(조) 9/21시작비중%")
for i,(nm,cd,c18,r18,wr) in enumerate(raw,1):
    w21 = wr/tot*100
    print("%d|%s|%s|%d|%+.2f|%.2f|%.6f" % (i,nm,cd,c18,r18,w21*TOTMC/100,w21))
print("32이하|-|-|-|%+.4f|%.2f|%.6f" % (c["small_r"], small_raw/tot*TOTMC, small_raw/tot*100))
print("검산 합 =", sum(x[4] for x in raw)/tot*100 + small_raw/tot*100)
print("상위2 %.4f 상위12 %.4f 상위31 %.4f" % (
  sum(sorted([x[4]/tot*100 for x in raw],reverse=True)[:2]),
  sum(sorted([x[4]/tot*100 for x in raw],reverse=True)[:12]),
  sum(x[4]/tot*100 for x in raw)))
