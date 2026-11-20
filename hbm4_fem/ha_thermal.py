"""[HA] grid3 공통 격자 위 PHY 발열 과도+정상 열해석 (DC3D8, 1/2 대칭) — 제품별 병렬 실행.
출력(SA 계약): out3/thermal/<prod>/fields.npz (times[정상=inf], T[n_t, N] float32, 열 = node id-1, X,Y,Z), summary.json.
시간점 누락 방지: *TIME POINTS 대신 시간점마다 *STEP 을 나눠 각 step 끝에서만 출력(FREQUENCY 큼) → 마지막 정상 step.
usage: python3 ha_thermal.py            (두 제품 병렬 실행 + 후처리)
       python3 ha_thermal.py one <prod> (한 제품: build+solve+post)
       python3 ha_thermal.py post <prod>"""
import sys, os, json, time, subprocess, numpy as np
import grid3
from thermal2 import therm, kSi
from frd import read_frd

ROOT = "out3/thermal"
TP = [1e-4, 3e-4, 1e-3, 3e-3, 1e-2, 3e-2, 0.1, 0.3, 1.0, 3.0]
NAME = "ha"
BIG = 1000000


def odir(prod):
    d = f"{ROOT}/{prod}"; os.makedirs(d, exist_ok=True); return d


def model(prod):
    g = grid3.grid(prod); ids, xyz, eids, conn = grid3.nodes_elems(g)
    X, Y, Z = g["X"], g["Y"], g["Z"]
    vol = np.einsum("i,j,k->ijk", np.diff(X), np.diff(Y), np.diff(Z))
    return g, ids, xyz, eids, conn, vol


def build(prod):
    g, ids, xyz, eids, conn, vol = model(prod); c = g["c"]; B = grid3.BC
    kf = g["kind"].ravel(order="F"); E3 = eids.reshape(g["kind"].shape, order="F")
    s = [f"** HA {prod}", "*NODE, NSET=NALL"] + [f"{n},{a:.6f},{b:.6f},{d:.7f}" for n, (a, b, d) in zip(ids, xyz)]
    s.append("*ELEMENT, TYPE=DC3D8, ELSET=EALL"); s += [f"{e}," + ",".join(map(str, cc)) for e, cc in zip(eids, conn)]
    TT = np.array([0, 25, 50, 75, 100, 125, 150, 200])
    for k in np.unique(kf):
        e = eids[kf == k]; t = therm(k, c)
        s += [f"*ELSET, ELSET=E_{k}"] + [",".join(map(str, e[i:i+16])) for i in range(0, len(e), 16)]
        s += [f"*MATERIAL, NAME=T_{k}", "*CONDUCTIVITY, TYPE=ORTHO"]
        s += ([f"{kSi(T):.3f},{kSi(T):.3f},{kSi(T):.3f},{T:.1f}" for T in TT] if t["kxy"] is None
              else [f"{t['kxy']:.4f},{t['kxy']:.4f},{t['kz']:.4f}"])
        s += ["*DENSITY", f"{t['rho']:.4e}", "*SPECIFIC HEAT", f"{t['cp']:.4e}", f"*SOLID SECTION, ELSET=E_{k}, MATERIAL=T_{k}"]
    P_half = grid3.PRODUCTS[prod]["phy_W"]/2*1e3                       # mW
    vphy = vol[g["phy"]].sum(); q = P_half/vphy
    s += ["*INITIAL CONDITIONS, TYPE=TEMPERATURE", f"NALL,{B['T_ref']}"]
    bot, top = E3[:, :, 0].ravel(), E3[:, :, -1].ravel()
    loads = ["*DFLUX"] + [f"{e},BF,{q:.6e}" for e in E3[g["phy"]]]
    loads += ["*FILM"] + [f"{e},F2,{B['T_ref']},{B['h_top']*1e-3:.4e}" for e in top]
    loads += [f"{e},F1,{B['T_ref']},{B['h_bot']*1e-3:.4e}" for e in bot]
    t0 = 0.0
    for i, tp in enumerate(TP):                                        # step 마다 끝 시간 = 시간점
        span = tp - t0; dt0 = 1e-5 if i == 0 else span/5
        s += ["*STEP, INC=100000", "*HEAT TRANSFER, DELTMX=1.0", f"{dt0:.6e}, {span:.6e}, 1e-10, {span:.6e}"]
        if i == 0: s += loads
        s += [f"*NODE FILE, FREQUENCY={BIG}", "NT", "*END STEP"]; t0 = tp
    s += ["*STEP, INC=100", "*HEAT TRANSFER, STEADY STATE", "1.,1.", "*NODE FILE, FREQUENCY=1", "NT", "*END STEP"]
    open(f"{odir(prod)}/{NAME}.inp", "w").write("\n".join(s)+"\n")
    print(f"[{prod}] nodes {len(ids):,} elems {len(eids):,} PHY elems {g['phy'].sum()} vol(half) {vphy:.4f} mm3 q={q:.1f} mW/mm3", flush=True)


def solve(prod):
    d = odir(prod); t = time.time()
    subprocess.run(["ccx", "-i", NAME], cwd=d, env=dict(os.environ, OMP_NUM_THREADS="1"), stdout=open(f"{d}/{NAME}.log", "w"), check=True)
    print(f"[{prod}] solved in {time.time()-t:.0f} s", flush=True)


def frd_times(fn):
    return [float(l.split()[2]) for l in open(fn) if l.startswith("  100CL")]


def post(prod):
    d = odir(prod); g, ids, xyz, eids, conn, vol = model(prod); B = grid3.BC; N = len(ids)
    tf = frd_times(f"{d}/{NAME}.frd"); steps = read_frd(f"{d}/{NAME}.frd")
    assert len(tf) == len(TP)+1 == len(steps), f"frd records {len(tf)} vs expected {len(TP)+1}: {tf}"
    assert np.allclose(tf[:-1], TP, rtol=1e-4), f"time mismatch {tf}"
    times = np.array(TP + [np.inf]); T = np.zeros((len(times), N), np.float32)
    for i, st in enumerate(steps):
        nid, v = st["NDTEMP"]; assert len(nid) == N; T[i, nid-1] = v[:, 0]
    # 요소 평균 (8절점 평균) 및 그룹
    kind = g["kind"].ravel(order="F"); lname = g["lname"].ravel(order="F"); V = vol.ravel(order="F")
    phy = g["phy"].ravel(order="F"); E3 = eids.reshape(g["kind"].shape, order="F")
    grp = dict(phy=phy, base=lname == "Base_Si", top_si=kind == "si_top", pkg=np.ones_like(phy))
    Te = T[:, conn-1].mean(-1)
    # 상/하면 막 열유출 (1/2 모델)
    def film(Tn):
        out = {}
        for key, lay, sl, h in (("bot", 0, slice(0, 4), B["h_bot"]), ("top", -1, slice(4, 8), B["h_top"])):
            e = E3[:, :, lay].ravel()-1; Tf = Tn[conn[e][:, sl]-1].mean(-1)
            A = (np.diff(g["X"])[:, None]*np.diff(g["Y"])[None, :]).ravel(order="F")
            out[key] = float((h*1e-3*A*(Tf-B["T_ref"])).sum())          # mW (half)
        return out
    P_half = grid3.PRODUCTS[prod]["phy_W"]/2*1e3
    R = []
    for i, t in enumerate(times):
        k = int(np.argmax(T[i])); f = film(T[i].astype(float))
        r = dict(t=float(t), Tmax=float(T[i, k]), Tmax_xyz=[float(v) for v in xyz[k]], Tmax_node=int(ids[k]))
        for key, m in grp.items(): r[key] = float((Te[i, m]*V[m]).sum()/V[m].sum())
        r["Q_out_W_full"] = 2*(f["bot"]+f["top"])*1e-3; r["Q_top_frac"] = f["top"]/(f["bot"]+f["top"]+1e-30)
        R.append(r)
    ss = R[-1]; eb = (ss["Q_out_W_full"] - 2*P_half*1e-3)/(2*P_half*1e-3)
    # 집중 RC 검산 (전체 모델)
    rcp = np.zeros(len(kind))
    for k in np.unique(kind):
        t_ = therm(k, g["c"]); rcp[kind == k] = t_["rho"]*t_["cp"]                 # mJ/mm3/K
    C = 2*(rcp*V).sum()*1e-3                                                         # J/K
    A_full = 2*(g["X"][-1]-g["X"][0])*(g["Y"][-1]-g["Y"][0])                        # mm2
    Rth = 1/((B["h_top"]+B["h_bot"])*A_full*1e-6); tau = Rth*C; P = grid3.PRODUCTS[prod]["phy_W"]
    dT_fem = np.array([r["pkg"] for r in R]) - B["T_ref"]; dss = dT_fem[-1]
    lt, fr = np.log(np.array(TP)), dT_fem[:-1]/dss
    tau63 = float(np.exp(np.interp(1-np.exp(-1), fr, lt))) if fr[-1] > 0.632 else None
    Eheat = 2*((Te[-1]-B["T_ref"])*rcp*V).sum()*1e-3                                 # J
    rc = dict(R_KperW=Rth, C_JperK=C, tau_s=tau, dT_pkg_RC=P*Rth, dT_pkg_FEM=float(dss), tau63_FEM_s=tau63,
              tau_energy_FEM_s=float(Eheat/P), A_full_mm2=A_full,
              curve=[dict(t=t, dT_FEM=float(a), dT_RC=float(P*Rth*(1-np.exp(-t/tau)))) for t, a in zip(TP, dT_fem[:-1])])
    J = dict(product=prod, P_W=P, P_half_mW=P_half, BC=B, frd_times=tf, records=R,
             energy_balance=dict(P_in_W=P, Q_out_W=ss["Q_out_W_full"], err_rel=float(eb), top_frac=ss["Q_top_frac"]), rc_check=rc,
             notes="times[-1]=inf: steady state; group means are volume-weighted element(8-node avg) means; pkg = whole 1/2 model incl. EMC")
    json.dump(J, open(f"{d}/summary.json", "w"), indent=1, default=lambda o: None if o is None else str(o))
    tmp = f"{d}/fields.tmp.npz"
    np.savez(tmp, times=times, T=T, X=g["X"], Y=g["Y"], Z=g["Z"]); os.replace(tmp, f"{d}/fields.npz")
    print(f"[{prod}] energy balance err {eb*100:+.3f} %  RC: R={Rth:.4f} K/W C={C:.4e} J/K tau={tau*1e3:.1f} ms dT_RC={P*Rth:.2f} dT_FEM={dss:.2f} tau63_FEM={tau63}", flush=True)
    for r in R: print(f"  t={r['t']:<8g} Tmax={r['Tmax']:.2f} @{np.round(r['Tmax_xyz'],3)} phy={r['phy']:.2f} base={r['base']:.2f} top={r['top_si']:.2f} pkg={r['pkg']:.3f}")


if __name__ == "__main__":
    a = sys.argv[1:]
    if not a:
        ps = [subprocess.Popen([sys.executable, __file__, "one", p], stdout=open(f"{odir(p)}/run.log", "w"), stderr=subprocess.STDOUT) for p in grid3.PRODUCTS]
        rc = [p.wait() for p in ps]; print("exit codes", rc)
    elif a[0] == "one": build(a[1]); solve(a[1]); post(a[1])
    elif a[0] == "post": post(a[1])
