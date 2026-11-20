"""HBM4-8H TCB DOE: 2^4 완전요인 + 중심점. 실행 → 효과(주효과·교호작용), Lenth PSE, Pareto, 반정규, 회귀, 곡률.
usage: python3 doe.py run|analyze"""
import sys, os, json, itertools, numpy as np
import stack as S, fem2
OUTD = "out2/doe"; os.makedirs(OUTD, exist_ok=True)
FAC = {  # code: (이름, key, low, high, 단위표시배율, 단위)
    "A": ("mid core Si", "ms", 0.0326, 0.0356, 1e3, "μm"),
    "C": ("BEOL α", "mA", 7.6e-6, 9.9e-6, 1e6, "ppm"),
    "D": ("NCF α1", "ncf_a1", 30e-6, 50e-6, 1e6, "ppm"),
    "E": ("NCF α2", "ncf_a2", 70e-6, 110e-6, 1e6, "ppm"),
}
K = list(FAC)
BASE = dict(gen="hbm4", nh=8, set_="design")
CAL = json.load(open("out2/calib3.json")); FIX = dict(soft=True, t0b=CAL["t0b"])
def design():
    runs = [dict(zip(K, x)) for x in itertools.product([-1, 1], repeat=len(K))]
    return runs + [dict.fromkeys(K, 0)]          # 결정론적 해석 → 중심점 1회로 충분 (반복오차 0)
def case_of(x):
    over = {FAC[k][1]: FAC[k][2] + (x[k]+1)/2*(FAC[k][3]-FAC[k][2]) for k in K}
    return S.case(BASE["gen"], BASE["nh"], BASE["set_"], **FIX, **over)
def name_of(i): return f"doe_{i:02d}"
def one(i):
    x = design()[i]; n = name_of(i); f = f"{OUTD}/{n}.json"
    if os.path.exists(f): return json.load(open(f))
    c = case_of(x); W = fem2.run(n, c, temps=[25, 230], elprint=(25, 230)); St = fem2.stresses(n)
    r = dict(run=i, x=x, top_si=S.top_si(c)*1e3,
             w25=W[25]["w_dram"], w230=W[230]["w_dram"], wbody25=W[25]["w_body"],
             si_s1_25=St[25]["si_s1"], gap_peel_25=St[25]["gap_peel"], gap_shear_25=St[25]["gap_shear"],
             gap_peel_230=St[230]["gap_peel"], emc_s1_25=St[25]["emc_s1"])
    json.dump(r, open(f, "w"), indent=1)
    for ext in (".dat", ".frd"):            # 용량 정리 (지표 저장 후)
        try: os.remove(f"out2/{n}{ext}")
        except FileNotFoundError: pass
    return r
if __name__ == "__main__" and sys.argv[1] == "run":
    from multiprocessing import Pool
    with Pool(4) as p:
        for r in p.imap_unordered(one, range(len(design()))):
            print(r["run"], r["x"], "w25=%.2f w230=%.2f" % (r["w25"], r["w230"]), flush=True)
