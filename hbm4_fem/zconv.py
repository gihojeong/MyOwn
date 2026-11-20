"""두께방향 격자 수렴 시험: HBM3E-12H Micron 공칭(DOE 중심점) 25 °C, N_THIN = 1/2/3."""
import json, stack as S, fem2, doe
from multiprocessing import Pool
import os; os.environ["DOE_PRODUCT"] = "hbm3e_12h_micron"
def one(n):
    fem2.N_THIN = n; c = S.case("hbm3e", 12, "micron", soft=True, t0b=json.load(open("out2/calib3.json"))["t0b"])
    name = f"zconv_n{n}"; W = fem2.run(name, c, temps=[25], elprint=(25,)); St = fem2.stresses(name, (25,))
    import numpy as np; m = np.load(f"out2/{name}_mesh.npz")
    return dict(n=n, elems=int(m["kind"].size), w25=W[25]["w_dram"], **St[25])
if __name__ == "__main__":
    with Pool(3) as p: R = p.map(one, [1, 2, 3])
    json.dump(R, open("out2/zconv.json", "w"), indent=1)
    for r in R: print(r)
