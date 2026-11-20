"""vf 0.353 (D15, 200k) 로 T0b 재보정: Micron 실측두께 세트, Tg 연화."""
import json, stack as S, fem2
from multiprocessing import Pool
JOBS = {f"C3_micron_t{t}": S.case("hbm3e", 12, "micron", soft=True, t0b=float(t)) for t in (400, 250)}
def one(n): return n, fem2.run(n, JOBS[n], temps=[25, 230], elprint=())
if __name__ == "__main__":
    with Pool(2) as p: R = dict(p.map(one, JOBS))
    a, b = R["C3_micron_t400"], R["C3_micron_t250"]
    s25, s230 = (a[25]["w_dram"]-b[25]["w_dram"])/150, (a[230]["w_dram"]-b[230]["w_dram"])/150
    T0 = 250 + (7.6-b[25]["w_dram"])/s25; w230 = b[230]["w_dram"] + s230*(T0-250)
    out = dict(vf=S.bump_vf("hbm3e"), t0b=T0, w25=7.6, w230_pred=w230, delta=a[25]["w_dram"]-a[230]["w_dram"])
    json.dump(out, open("out2/calib3.json", "w"), indent=1); print(out)
