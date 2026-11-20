"""v2 과도 열해석: B-die(base) PHY 발열 → 시간별 온도 분포. 1/2 대칭(y=0, 단열 대칭면), DC3D8.
단위: mm, tonne, s, mW, mJ → k[mW/mm/K]=k[W/m/K], h[mW/mm²/K]=1e-3·h[W/m²K], cp[mJ/t/K]=1e6·cp[J/kg/K].
usage: python3 thermal2.py run|post"""
import sys, os, json, subprocess, numpy as np
import stack as S
from frd import read_frd
OUT = "out2/thermal"; os.makedirs(OUT, exist_ok=True); NAME = "phy_transient"
CASE = S.case("hbm4", 8, "design", soft=True)          # HBM4-8H 775 μm
P_PHY = 5.0                                            # W (전체), 1/2 모델은 절반
PHY = (-5.50, -4.00, -4.50, 4.50)                      # x0,x1,y0,y1 [mm]: GPU 측 가장자리 1.5×9 mm (0.25 mm inset)
H_TOP, H_BOT, T_REF = 7000., 4000., 45.               # W/m²K, °C (상면 TIM+cold plate / 하면 μbump→interposer)
TP = [1e-4, 3e-4, 1e-3, 3e-3, 1e-2, 3e-2, 0.1, 0.2, 0.5, 1.0, 2.0]
# ---- 열물성 (k_xy, k_z, ρ, cp) ----
def kSi(T): return 148*(298.15/(np.asarray(T)+273.15))**1.3
def therm(kind, c):
    if kind in ("si", "si_top", "si_base"): return dict(kxy=None, kz=None, rho=2.33e-9, cp=7.0e8)   # k(T)
    if kind == "beol": return dict(kxy=12., kz=2.5, rho=4.0e-9, cp=6.8e8)       # Cu/low-k 배선층 (가정)
    if kind == "emc": return dict(kxy=1.0, kz=1.0, rho=2.0e-9, cp=9.0e8)
    if kind == "gap":
        v, kb, km = c["vf"], 57., 0.3                                            # SnAg bump / NCF
        kz = v*kb + (1-v)*km; kxy = km*((kb+km)+v*(kb-km))/((kb+km)-v*(kb-km))   # 병렬 / Maxwell-Garnett
        rho = v*7.4e-9 + (1-v)*1.3e-9; cp = (v*7.4*2.3e8 + (1-v)*1.3*1.2e9)/(v*7.4+(1-v)*1.3)
        return dict(kxy=kxy, kz=kz, rho=rho, cp=cp)
def axis(brk, h):
    brk = np.unique(np.round(brk, 6)); p = [brk[0]]
    for a, b in zip(brk[:-1], brk[1:]): p += list(np.linspace(a, b, max(1, int(np.ceil((b-a)/h-1e-9)))+1)[1:])
    return np.round(np.array(p), 6)
def build():
    c = CASE; L = S.layers(c); hd, hl = S.L_DRAM/2, S.L_LOGIC/2
    X = axis([-hl, -hd, hd, hl, PHY[0], PHY[1], 0], 0.192); Y = axis([0, hd, hl, PHY[3]], 0.192)
    Z = [0.0]
    for (n, k, z0, z1, h) in L:
        if k == "emc": continue
        nzl = 6 if k == "si_top" else (2 if n == "Base_Si" else 1); Z += list(np.linspace(z0, z1, nzl+1)[1:])
    Z = np.round(np.array(Z), 7); nx, ny, nz = len(X), len(Y), len(Z)
    xc, yc, zc = (X[:-1]+X[1:])/2, (Y[:-1]+Y[1:])/2, (Z[:-1]+Z[1:])/2
    XC, YC, ZC = np.meshgrid(xc, yc, zc, indexing="ij"); kind = np.full(XC.shape, "", "<U10"); lname = np.full(XC.shape, "", "<U16")
    for (n, k, z0, z1, h) in sorted(L, key=lambda l: l[1] == "emc"):
        m = (abs(XC) < h) & (YC < h) & (ZC > z0) & (ZC < z1) & (kind == ""); kind[m] = k; lname[m] = n
    assert (kind != "").all()
    zb = [l for l in L if l[0] == "Base_Si"][0]; kphy = int(np.argmin(abs(Z-zb[2])))      # base Si 최하단(전면, BEOL 접) 요소층
    phy = (XC > PHY[0]) & (XC < PHY[1]) & (YC < PHY[3]) & (np.arange(nz-1)[None, None, :] == kphy)
    nid = lambda i, j, k: 1 + i + nx*(j + ny*k)
    I, J, K = np.meshgrid(range(nx), range(ny), range(nz), indexing="ij")
    ids = nid(I, J, K).ravel(order="F"); xyz = np.stack([X[I], Y[J], Z[K]], -1).reshape(-1, 3, order="F")
    s = ["** PHY transient", "*NODE, NSET=NALL"] + [f"{n},{a:.6f},{b:.6f},{d:.7f}" for n, (a, b, d) in zip(ids, xyz)]
    I, J, K = [a.ravel(order="F") for a in np.meshgrid(range(nx-1), range(ny-1), range(nz-1), indexing="ij")]
    conn = np.stack([nid(I, J, K), nid(I+1, J, K), nid(I+1, J+1, K), nid(I, J+1, K), nid(I, J, K+1), nid(I+1, J, K+1), nid(I+1, J+1, K+1), nid(I, J+1, K+1)], 1)
    eid = np.arange(1, XC.size+1).reshape(XC.shape, order="F"); kf = kind.ravel(order="F")
    s.append("*ELEMENT, TYPE=DC3D8, ELSET=EALL"); s += [f"{e}," + ",".join(map(str, cc)) for e, cc in zip(eid.ravel(order="F"), conn)]
    TT = np.array([25, 50, 75, 100, 125, 150])
    for k in np.unique(kf):
        e = eid.ravel(order="F")[kf == k]; t = therm(k, c)
        s += [f"*ELSET, ELSET=E_{k}"] + [",".join(map(str, e[i:i+16])) for i in range(0, len(e), 16)]
        s += [f"*MATERIAL, NAME=T_{k}", "*CONDUCTIVITY, TYPE=ORTHO"]
        s += ([f"{kSi(T):.3f},{kSi(T):.3f},{kSi(T):.3f},{T:.1f}" for T in TT] if t["kxy"] is None else [f"{t['kxy']:.4f},{t['kxy']:.4f},{t['kz']:.4f}"])
        s += ["*DENSITY", f"{t['rho']:.4e}", "*SPECIFIC HEAT", f"{t['cp']:.4e}", f"*SOLID SECTION, ELSET=E_{k}, MATERIAL=T_{k}"]
    vphy = (np.einsum("i,j,k->ijk", np.diff(X), np.diff(Y), np.diff(Z)))[phy].sum(); q = P_PHY/2*1e3/vphy
    s += ["*INITIAL CONDITIONS, TYPE=TEMPERATURE", f"NALL,{T_REF}", "*TIME POINTS, NAME=TP", ",".join(map(str, TP))]
    bot, top = eid[:, :, 0].ravel(), eid[:, :, -1].ravel()
    loads = ["*DFLUX"] + [f"{e},BF,{q:.6e}" for e in eid[phy]] + ["*FILM"] + [f"{e},F2,{T_REF},{H_TOP*1e-3:.4e}" for e in top] + [f"{e},F1,{T_REF},{H_BOT*1e-3:.4e}" for e in bot]
    s += ["*STEP, INC=100000", "*HEAT TRANSFER, DELTMX=0.25", f"1e-6, {TP[-1]}, 1e-9, 0.05"] + loads + ["*NODE FILE, TIME POINTS=TP", "NT", "*END STEP"]
    s += ["*STEP", "*HEAT TRANSFER, STEADY STATE", "1.,1."] + ["*NODE FILE", "NT", "*END STEP"]
    open(f"{OUT}/{NAME}.inp", "w").write("\n".join(s)+"\n")
    np.savez(f"{OUT}/{NAME}_mesh.npz", X=X, Y=Y, Z=Z, kind=kind, lname=lname, phy=phy)
    print(f"mesh {nx}x{ny}x{nz} nodes {nx*ny*nz:,} elems {(nx-1)*(ny-1)*(nz-1):,}, PHY elems {phy.sum()} vol {vphy:.4f} mm3 q={q:.1f} mW/mm3")
if __name__ == "__main__" and sys.argv[1] == "run":
    build(); subprocess.run(["ccx", "-i", NAME], cwd=OUT, env=dict(os.environ, OMP_NUM_THREADS="1"), stdout=open(f"{OUT}/{NAME}.log", "w"), check=True)
    print("solved")
