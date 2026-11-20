"""v2 FEM: stack.py 케이스 → 1/4 대칭 구조격자 → CalculiX(C3D8I) 다중 무응력온도 열-구조 → warp.
다중 무응력온도 구현: ZERO=0, 초기온도 400 °C(가상)에서 α_tab(T)=ε_F(T)/T, α_tab(400)=0 → 각 재료 ε = ε_F(T).
usage(모듈): run(name, case_dict, temps) → dict"""
import os, json, subprocess, numpy as np
import stack as S
from frd import read_frd, read_elprint
OUT = "out2"; os.makedirs(OUT, exist_ok=True)
TEMPS = [25, 100, 150, 175, 200, 217, 230, 260]
H_IN, N_RING, N_TOP = 0.192, 4, 6
N_THIN = 1          # 얇은 층(BEOL·gap·mid Si·base BEOL) 두께방향 요소 수 (수렴 시험용)
KINDS = ["beol", "si_base", "si", "si_top", "gap", "emc"]

def axis(a, b, n): return np.linspace(a, b, n+1)
def build(name, c, temps=TEMPS, elprint=(25, 230)):
    L = S.layers(c); hd, hl = S.L_DRAM/2, S.L_LOGIC/2
    X = np.r_[axis(0, hd, int(round(hd/H_IN))), axis(hd, hl, N_RING)[1:]]; Y = X.copy()
    Z = [0.0]
    for (n, k, z0, z1, h) in L:
        if k == "emc": continue
        nz = N_TOP if k == "si_top" else (2*N_THIN if n == "Base_Si" else N_THIN)
        Z += list(np.linspace(z0, z1, nz+1)[1:])
    Z = np.round(np.array(Z), 7); nx, ny, nz = len(X), len(Y), len(Z)
    xc, yc, zc = (X[:-1]+X[1:])/2, (Y[:-1]+Y[1:])/2, (Z[:-1]+Z[1:])/2
    XC, YC, ZC = np.meshgrid(xc, yc, zc, indexing="ij")
    kind = np.full(XC.shape, "", object); lname = np.full(XC.shape, "", object)
    for (n, k, z0, z1, h) in sorted(L, key=lambda l: l[1] == "emc"):
        m = (XC < h) & (YC < h) & (ZC > z0) & (ZC < z1) & (kind == "")
        kind[m] = k; lname[m] = n
    assert (kind != "").all()
    nid = lambda i, j, k: 1 + i + nx*(j + ny*k)
    I, J, K = np.meshgrid(range(nx), range(ny), range(nz), indexing="ij")
    ids = nid(I, J, K).ravel(order="F"); xyz = np.stack([X[I], Y[J], Z[K]], -1).reshape(-1, 3, order="F")
    s = [f"** {name}", "*NODE, NSET=NALL"]
    s += [f"{n},{a:.6f},{b:.6f},{d:.7f}" for n, (a, b, d) in zip(ids, xyz)]
    I, J, K = [a.ravel(order="F") for a in np.meshgrid(range(nx-1), range(ny-1), range(nz-1), indexing="ij")]
    conn = np.stack([nid(I, J, K), nid(I+1, J, K), nid(I+1, J+1, K), nid(I, J+1, K),
                     nid(I, J, K+1), nid(I+1, J, K+1), nid(I+1, J+1, K+1), nid(I, J+1, K+1)], 1)
    eid = np.arange(1, XC.size+1).reshape(XC.shape, order="F"); kf = kind.ravel(order="F")
    s.append("*ELEMENT, TYPE=C3D8I, ELSET=EALL"); s += [f"{e}," + ",".join(map(str, cc)) for e, cc in zip(eid.ravel(order="F"), conn)]
    Tt = sorted(set(list(range(25, 261, 5)) + list(temps)))
    for k in KINDS:
        e = eid.ravel(order="F")[kf == k]
        if not len(e): continue
        s.append(f"*ELSET, ELSET=E_{k}"); s += [",".join(map(str, e[i:i+16])) for i in range(0, len(e), 16)]
        p = S.props(k, c); eps = S.eps_free(k, np.array(Tt, float), c)
        Ev = S.E_of(k, np.array(Tt, float), c)
        s += [f"*MATERIAL, NAME={k}", "*ELASTIC"] + [f"{e:.3f},{p['nu']:.4f},{t:.1f}" for e, t in zip(Ev, Tt)] + ["*EXPANSION, ZERO=0."]
        s += [f"{ep/t:.6e},{t:.1f}" for ep, t in zip(eps, Tt)] + ["0.,400."]
        s += [f"*SOLID SECTION, ELSET=E_{k}, MATERIAL={k}"]
    xs = ids[np.isclose(xyz[:, 0], 0)]; ys = ids[np.isclose(xyz[:, 1], 0)]
    s += ["*NSET, NSET=SX"] + [",".join(map(str, xs[i:i+16])) for i in range(0, len(xs), 16)]
    s += ["*NSET, NSET=SY"] + [",".join(map(str, ys[i:i+16])) for i in range(0, len(ys), 16)]
    s += ["*BOUNDARY", "SX,1,1", "SY,2,2", f"{nid(0,0,0)},3,3", "*INITIAL CONDITIONS, TYPE=TEMPERATURE", "NALL,400."]
    for T in temps:
        s += ["*STEP", "*STATIC", "*TEMPERATURE", f"NALL,{T}.", "*NODE FILE", "U", "*EL FILE", "S"]
        s += (["*EL PRINT, ELSET=EALL", "S"] if T in elprint else [])
        s += ["*END STEP"]
    open(f"{OUT}/{name}.inp", "w").write("\n".join(s)+"\n")
    np.savez(f"{OUT}/{name}_mesh.npz", X=X, Y=Y, Z=Z, kind=kind.astype(str), lname=lname.astype(str))
    return X, Y, Z

def solve(name):
    # 주의: SPOOLES 멀티스레드 해 오염 사례 → 단일 스레드
    subprocess.run(["ccx", "-i", name], cwd=OUT, env=dict(os.environ, OMP_NUM_THREADS="1"),
                   stdout=open(f"{OUT}/{name}.log", "w"), check=True)

def warp(name, c, temps=TEMPS):
    m = np.load(f"{OUT}/{name}_mesh.npz"); X, Y, Z = m["X"], m["Y"], m["Z"]; nx, ny, nz = len(X), len(Y), len(Z)
    st = read_frd(f"{OUT}/{name}.frd"); hd = S.L_DRAM/2
    iD = int(np.argmin(abs(X-hd)))
    R = {}
    for T, s in zip(temps, st):
        u = s["DISP"][1].reshape(nz, ny, nx, 3)
        top, bot = u[-1, :, :, 2]*1e3, u[0, :, :, 2]*1e3
        R[T] = dict(w_dram=float(top[0, 0]-top[iD, iD]), w_body=float(top[0, 0]-top[-1, -1]),
                    w_edge=float(top[0, 0]-top[0, iD]), w_bot_body=float(bot[0, 0]-bot[-1, -1]),
                    diag_ptp=float(np.ptp(np.diag(top))))
    return R

def run(name, c, temps=TEMPS, elprint=(25, 230)):
    build(name, c, temps, elprint); solve(name); R = warp(name, c, temps)
    json.dump(dict(case=c, warp={str(k): v for k, v in R.items()}), open(f"{OUT}/{name}.json", "w"), indent=1)
    return R

def stresses(name, temps_printed=(25, 230)):
    """EL PRINT(적분점) → 요소 평균 → 재료별 지표 [MPa]"""
    m = np.load(f"{OUT}/{name}_mesh.npz"); kf = m["kind"].ravel(order="F")
    out = {}
    for T, a in zip(temps_printed, read_elprint(f"{OUT}/{name}.dat")):
        ne = kf.size; se = np.zeros((ne, 6)); np.add.at(se, a[:, 0].astype(int)-1, a[:, 2:]); se /= 8
        Tn = np.zeros((ne, 3, 3)); Tn[:, 0, 0], Tn[:, 1, 1], Tn[:, 2, 2] = se[:, 0], se[:, 1], se[:, 2]
        Tn[:, 0, 1] = Tn[:, 1, 0] = se[:, 3]; Tn[:, 0, 2] = Tn[:, 2, 0] = se[:, 4]; Tn[:, 1, 2] = Tn[:, 2, 1] = se[:, 5]
        s1 = np.linalg.eigvalsh(Tn)[:, -1]; si = np.isin(kf, ["si", "si_top", "si_base"]); g = kf == "gap"
        out[T] = dict(si_s1=float(s1[si].max()), si_s3=float(np.linalg.eigvalsh(Tn[si])[:, 0].min()),
                      gap_peel=float(se[g, 2].max()), gap_shear=float(np.hypot(se[g, 4], se[g, 5]).max()),
                      emc_s1=float(s1[kf == "emc"].max()), beol_s1=float(s1[kf == "beol"].max()))
    return out
