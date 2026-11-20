"""v2 검증: viewer FEM 점검값(설계 20.9 / Micron 11.6 μm) 재현 + T0b 1점 보정(실측 |w25| 7.6 μm)."""
import sys, json, stack as S, fem2
from multiprocessing import Pool
JOBS = {
    "V_design_viewer":  S.case("hbm3e", 12, "design", cte_mode="viewer"),
    "V_micron_viewer":  S.case("hbm3e", 12, "micron", cte_mode="viewer"),
    "V_design_int400":  S.case("hbm3e", 12, "design", cte_mode="integral", t0b=400.),
    "V_design_int250":  S.case("hbm3e", 12, "design", cte_mode="integral", t0b=250.),
}
def one(n): R = fem2.run(n, JOBS[n]); return n, R[25]["w_dram"], R[230]["w_dram"]
if __name__ == "__main__":
    with Pool(4) as p:
        for n, w25, w230 in p.imap_unordered(one, JOBS):
            print(f"{n}: w_dram 25°C {w25:+.2f}  230°C {w230:+.2f}  (CLT {S.clt_warp(JOBS[n],25):+.2f} / {S.clt_warp(JOBS[n],230):+.2f})", flush=True)
