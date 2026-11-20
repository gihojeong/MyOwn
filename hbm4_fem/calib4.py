"""HBM3E-12H Micron 두께 + base die 10.93 mm(사진) 로 T0b 재보정 (|w25|=7.6 μm)."""
import json, stack as S, fem2
from multiprocessing import Pool
JOBS = {f"C4_t{t}": S.case("hbm3e", 12, "micron", soft=True, t0b=float(t), L_logic=10.93, L_dram=10.0) for t in (400, 250)}
def one(n): return n, fem2.run(n, JOBS[n], temps=[25, 230], elprint=())
if __name__ == "__main__":
    with Pool(2) as p: R = dict(p.map(one, JOBS))
    a, b = R["C4_t400"], R["C4_t250"]
    s25, s230 = (a[25]["w_dram"]-b[25]["w_dram"])/150, (a[230]["w_dram"]-b[230]["w_dram"])/150
    T0 = 250 + (7.6-b[25]["w_dram"])/s25; w230 = b[230]["w_dram"] + s230*(T0-250)
    out = dict(L_logic=10.93, t0b=T0, w25=7.6, w230_pred=w230, delta=a[25]["w_dram"]-a[230]["w_dram"])
    json.dump(out, open("out2/calib4.json", "w"), indent=1); print(out)
