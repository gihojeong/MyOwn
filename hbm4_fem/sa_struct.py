"""[SA] 단방향(one-way) 준정적 열-구조 해석: grid3 1/2 대칭 격자(절점 번호 동일), HA 온도장(out3/thermal/<prod>/fields.npz) → CalculiX C3D8I.
다중 무응력온도: fem2 와 같은 방식 (*EXPANSION ZERO=0, α_tab(T)=ε_F(T)/T, 초기 가상온도 400 °C).
경계: y=0 면 uy=0, 절점 (−L/2,0,0) ux=uz=0, (+L/2,0,0) uz=0.
스텝: 균일 25 / 230 / 45 °C, 이후 HA 시간별 절점온도(*TEMPERATURE include).
usage:
  python3 sa_struct.py verify            # 결합 검증 (hbm4_8h, 단일 무응력온도 45 °C, C3D8 완전결합 vs 순차)
  python3 sa_struct.py run <prod>        # fields.npz 대기(30 s 폴링, 최대 3 h) → 해석 → summary.json
  python3 sa_struct.py post <prod>       # 후처리만
  python3 sa_struct.py figs              # 그림
부호: warp = w(중앙) − w(DRAM vertex), (+) Cry(중앙 볼록). 단위 mm, MPa, °C, 출력 μm."""
import os, sys, json, time, subprocess, numpy as np
import grid3 as G, stack as S, thermal2 as TH
from frd import read_frd, read_elprint
KINDS = ["beol", "si_base", "si", "si_top", "gap", "emc"]
SIK = ("si", "si_top", "si_base")
ENV = dict(os.environ, OMP_NUM_THREADS="1", CCX_NPROC_EQUATION_SOLVER="1", CCX_NPROC_STIFFNESS="1", CCX_NPROC_RESULTS="1")
HD = S.L_DRAM/2

def odir(prod, sub="mech"):
    d = f"out3/{sub}/{prod}"; os.makedirs(d, exist_ok=True); return d
def l16(a): return [",".join(map(str, a[i:i+16])) for i in range(0, len(a), 16)]

# ---------------------------------------------------------------- 공통 격자/경계
def model(prod):
    g = G.grid(prod); ids, xyz, eids, conn = G.nodes_elems(g)
    assert (ids == np.arange(1, len(ids)+1)).all()
    return g, ids, xyz, eids, conn, g["kind"].ravel(order="F")
def geom_lines(g, ids, xyz, eids, conn, kf, etype):
    s = ["*NODE, NSET=NALL"] + [f"{n},{a:.6f},{b:.6f},{d:.7f}" for n, (a, b, d) in zip(ids, xyz)]
    s += [f"*ELEMENT, TYPE={etype}, ELSET=EALL"] + [f"{e}," + ",".join(map(str, cc)) for e, cc in zip(eids, conn)]
    for k in KINDS:
        e = eids[kf == k]
        if len(e): s += [f"*ELSET, ELSET=E_{k}"] + l16(e)
    s += ["*ELSET, ELSET=E_PRT"] + l16(eids[kf != "emc"])        # EL PRINT 대상 (EMC 제외)
    return s
def bc_lines(g, ids, xyz):
    nx = len(g["X"]); sy = ids[np.isclose(xyz[:, 1], 0)]
    a, b = 1, nx                                                   # (−L/2,0,0), (+L/2,0,0)
    assert np.allclose(xyz[a-1], [g["X"][0], 0, 0]) and np.allclose(xyz[b-1], [g["X"][-1], 0, 0])
    return ["*NSET, NSET=SY"] + l16(sy) + ["*BOUNDARY", "SY,2,2", f"{a},1,1", f"{a},3,3", f"{b},3,3"]
def write_temp_inc(fn, T):
    with open(fn, "w") as f:
        f.write("\n".join(f"{i+1},{t:.4f}" for i, t in enumerate(T)) + "\n")
def ccx(d, name):
    t0 = time.time()
    r = subprocess.run(["ccx", "-i", name], cwd=d, env=ENV, stdout=open(f"{d}/{name}.log", "w"), stderr=subprocess.STDOUT)
    txt = open(f"{d}/{name}.log").read()
    if r.returncode or "*ERROR" in txt: raise RuntimeError(f"ccx {d}/{name} failed: " + txt[-1500:])
    return time.time() - t0
def disp(st, N):
    i, v = st["DISP"]; u = np.zeros((N, 3)); m = i <= N; u[i[m]-1] = v[m]; return u
def ntemp(st, N):
    i, v = st["NDTEMP"]; t = np.zeros(N); m = i <= N; t[i[m]-1] = v[m, 0]; return t

# ---------------------------------------------------------------- warp 지표
def top_w(g, u):
    """상면 uz [μm], shape (nx, ny)"""
    nx, ny, nz = len(g["X"]), len(g["Y"]), len(g["Z"])
    return u[:, 2].reshape(nz, ny, nx)[-1].T*1e3
def mirror(g, w):
    """y 전 범위로 대칭 확장 → (Yf, wf[nx, 2ny−1])"""
    Y = g["Y"]; return np.r_[-Y[:0:-1], Y], np.concatenate([w[:, :0:-1], w], 1)
def trib(a):
    d = np.diff(a); t = np.zeros(len(a)); t[:-1] += d/2; t[1:] += d/2; return t
def dram_box(g):
    """DRAM(top core) 상면 범위: (x_min, x_max, y_half) — 격자의 si_top 요소에서 직접 구함"""
    m = (g["kind"][:, :, -1] == "si_top"); X, Y = g["X"], g["Y"]
    i = np.flatnonzero(m.any(1)); j = np.flatnonzero(m.any(0))
    return float(X[i[0]]), float(X[i[-1]+1]), float(Y[j[-1]+1])
def metrics(g, w):
    """평면(가중 최소자승, DRAM 영역) 제거 후 warp_phy(x=−5), warp_far(x=+5), coplanarity(DRAM)"""
    X = g["X"]; Yf, wf = mirror(g, w); x0, x1, hy = dram_box(g)
    mx, my = (X >= x0-1e-9) & (X <= x1+1e-9), np.abs(Yf) <= hy+1e-9
    XX, YY = np.meshgrid(X[mx], Yf[my], indexing="ij"); W = wf[np.ix_(mx, my)]
    wt = np.outer(trib(X[mx]), trib(Yf[my])).ravel()
    A = np.c_[np.ones(XX.size), XX.ravel(), YY.ravel()]; sw = np.sqrt(wt)
    p = np.linalg.lstsq(A*sw[:, None], W.ravel()*sw, rcond=None)[0]
    R = W - (A @ p).reshape(W.shape)
    xs, ys = X[mx], Yf[my]; ix = lambda v: int(np.argmin(abs(xs-v))); iy = lambda v: int(np.argmin(abs(ys-v)))
    c = R[ix(0), iy(0)]
    return dict(warp_phy=float(c - 0.5*(R[ix(x0), iy(hy)]+R[ix(x0), iy(-hy)])),
                warp_far=float(c - 0.5*(R[ix(x1), iy(hy)]+R[ix(x1), iy(-hy)])),
                copl=float(R.max()-R.min()), tilt_x_um_per_mm=float(p[1]))

# ---------------------------------------------------------------- 응력 지표
def stress_metrics(g, eids, kf, a):
    ne = len(eids); se = np.zeros((ne, 6)); cnt = np.zeros(ne)
    np.add.at(se, a[:, 0].astype(int)-1, a[:, 2:]); np.add.at(cnt, a[:, 0].astype(int)-1, 1)
    ok = cnt > 0; se[ok] /= cnt[ok, None]
    Tn = np.zeros((ne, 3, 3)); Tn[:, 0, 0], Tn[:, 1, 1], Tn[:, 2, 2] = se[:, 0], se[:, 1], se[:, 2]
    Tn[:, 0, 1] = Tn[:, 1, 0] = se[:, 3]; Tn[:, 0, 2] = Tn[:, 2, 0] = se[:, 4]; Tn[:, 1, 2] = Tn[:, 2, 1] = se[:, 5]
    s1 = np.linalg.eigvalsh(Tn)[:, -1]
    X, Y, Z = g["X"], g["Y"], g["Z"]; xc, yc, zc = (X[:-1]+X[1:])/2, (Y[:-1]+Y[1:])/2, (Z[:-1]+Z[1:])/2
    XC, YC, ZC = [m.ravel(order="F") for m in np.meshgrid(xc, yc, zc, indexing="ij")]
    ln = g["lname"].ravel(order="F"); px0, px1, _, py1 = g["phy_box"]
    inphy = (XC > px0) & (XC < px1) & (YC < py1)                   # PHY 투영 영역 (전 높이)
    defs = dict(si_s1=(np.isin(kf, SIK), s1), si_base_s1=(kf == "si_base", s1), gap_peel=(kf == "gap", se[:, 2]),
                gap_shear=(kf == "gap", np.hypot(se[:, 4], se[:, 5])), beol_s1=(kf == "beol", s1))
    out = {}
    for key, (m, v) in defs.items():
        m = m & ok
        for reg, rm in (("all", m), ("phy", m & inphy), ("else", m & ~inphy)):
            if rm.any():
                j = np.flatnonzero(rm)[np.argmax(v[rm])]
                out[f"{key}_{reg}"] = float(v[j])
                if reg == "all": out[f"{key}_at"] = [round(float(XC[j]), 3), round(float(YC[j]), 3), round(float(ZC[j]), 4), str(ln[j])]
    return out

# ================================================================ 1) 결합 검증
def verify(prod="hbm4_8h", tps=(1e-3, 0.01, 0.1), deltmx=1.0):
    d = odir(prod, "mech_verify"); g, ids, xyz, eids, conn, kf = model(prod); c = g["c"]; N = len(ids)
    X, Y, Z = g["X"], g["Y"], g["Z"]; nx, ny, nz = len(X), len(Y), len(Z)
    eid3 = eids.reshape(nx-1, ny-1, nz-1, order="F")
    vol = np.einsum("i,j,k->ijk", np.diff(X), np.diff(Y), np.diff(Z)); vphy = vol[g["phy"]].sum()
    q = G.PRODUCTS[prod]["phy_W"]/2*1e3/vphy; Tr = G.BC["T_ref"]
    TT = [25, 50, 75, 100, 125, 150]
    def mats(thermal, mech):
        s = []
        for k in KINDS:
            if not (kf == k).any(): continue
            s += [f"*MATERIAL, NAME=M_{k}"]
            if thermal:
                t = TH.therm(k, c); s += ["*CONDUCTIVITY, TYPE=ORTHO"]
                s += ([f"{TH.kSi(T):.3f},{TH.kSi(T):.3f},{TH.kSi(T):.3f},{T:.1f}" for T in TT] if t["kxy"] is None else [f"{t['kxy']:.4f},{t['kxy']:.4f},{t['kz']:.4f}"])
                s += ["*DENSITY", f"{t['rho']:.4e}", "*SPECIFIC HEAT", f"{t['cp']:.4e}"]
            if mech:
                p = S.props(k, c); E = float(S.E_of(k, Tr, c)); a = float(S._alpha(k, np.array([Tr]), c)[0])
                s += ["*ELASTIC", f"{E:.3f},{p['nu']:.4f}", f"*EXPANSION, ZERO={Tr}", f"{a:.6e}"]
            s += [f"*SOLID SECTION, ELSET=E_{k}, MATERIAL=M_{k}"]
        return s
    top, bot = eid3[:, :, -1].ravel(), eid3[:, :, 0].ravel()
    loads = ["*DFLUX"] + [f"{e},BF,{q:.6e}" for e in eid3[g["phy"]]] + ["*FILM"] + \
        [f"{e},F2,{Tr},{G.BC['h_top']*1e-3:.4e}" for e in top] + [f"{e},F1,{Tr},{G.BC['h_bot']*1e-3:.4e}" for e in bot]
    tend = max(tps); inc = [f"1e-5, {tend}, 1e-9, {tend/10}"]
    hdr = ["*INITIAL CONDITIONS, TYPE=TEMPERATURE", f"NALL,{Tr}", "*TIME POINTS, NAME=TP", ",".join(map(str, tps))]
    # (a) 완전결합
    s = ["** coupled"] + geom_lines(g, ids, xyz, eids, conn, kf, "C3D8") + mats(True, True) + bc_lines(g, ids, xyz) + hdr
    s += ["*STEP, INC=100000", f"*COUPLED TEMPERATURE-DISPLACEMENT, DELTMX={deltmx}"] + inc + loads
    s += ["*NODE FILE, TIME POINTS=TP", "U,NT", "*END STEP"]
    s += ["*STEP, INC=1000", "*COUPLED TEMPERATURE-DISPLACEMENT, STEADY STATE", "1.,1."] + ["*NODE FILE", "U,NT", "*END STEP"]
    open(f"{d}/coupled.inp", "w").write("\n".join(s)+"\n")
    # (b1) 열 단독
    s = ["** thermal"] + geom_lines(g, ids, xyz, eids, conn, kf, "DC3D8") + mats(True, False) + hdr
    s += ["*STEP, INC=100000", f"*HEAT TRANSFER, DELTMX={deltmx}"] + inc + loads + ["*NODE FILE, TIME POINTS=TP", "NT", "*END STEP"]
    s += ["*STEP", "*HEAT TRANSFER, STEADY STATE", "1.,1.", "*NODE FILE", "NT", "*END STEP"]
    open(f"{d}/thermal.inp", "w").write("\n".join(s)+"\n")
    R = dict(prod=prod, deltmx=deltmx, q_mW_mm3=q, n_nodes=N)
    R["t_thermal_s"] = ccx(d, "thermal")
    Tb = [ntemp(st, N) for st in read_frd(f"{d}/thermal.frd")]
    labels = [str(t) for t in tps] + ["steady"]; assert len(Tb) == len(labels), len(Tb)
    # (b2) 구조 (같은 C3D8, 순차)
    s = ["** sequential mech"] + geom_lines(g, ids, xyz, eids, conn, kf, "C3D8") + mats(False, True) + bc_lines(g, ids, xyz)
    s += ["*INITIAL CONDITIONS, TYPE=TEMPERATURE", f"NALL,{Tr}"]
    for i, T in enumerate(Tb):
        write_temp_inc(f"{d}/Tseq_{i}.inc", T)
        s += ["*STEP", "*STATIC", "*TEMPERATURE", f"*INCLUDE, INPUT=Tseq_{i}.inc", "*NODE FILE", "U", "*END STEP"]
    open(f"{d}/seqmech.inp", "w").write("\n".join(s)+"\n")
    R["t_seqmech_s"] = ccx(d, "seqmech")
    Ub = [disp(st, N) for st in read_frd(f"{d}/seqmech.frd")]
    R["t_coupled_s"] = ccx(d, "coupled")
    sa = read_frd(f"{d}/coupled.frd"); assert len(sa) == len(labels), len(sa)
    Ta = [ntemp(st, N) for st in sa]; Ua = [disp(st, N) for st in sa]
    rows = {}
    for lab, ta, tb, ua, ub in zip(labels, Ta, Tb, Ua, Ub):
        ma, mb = metrics(g, top_w(g, ua)), metrics(g, top_w(g, ub))
        rows[lab] = dict(Tmax_coupled=float(ta.max()), Tmax_seq=float(tb.max()), dT_max_abs=float(abs(ta-tb).max()),
                         coupled=ma, seq=mb, duz_max_abs_um=float(abs(ua[:, 2]-ub[:, 2]).max()*1e3),
                         uz_max_abs_um=float(abs(ub[:, 2]).max()*1e3),
                         rel_warp_phy=float((ma["warp_phy"]-mb["warp_phy"])/mb["warp_phy"]) if mb["warp_phy"] else None,
                         rel_warp_far=float((ma["warp_far"]-mb["warp_far"])/mb["warp_far"]) if mb["warp_far"] else None)
    R["rows"] = rows
    # 열탄성 결합계수 δ = E α² T / (ρ c (1−2ν)) (Si, 318 K)
    p = S.props("si_top", c); t = TH.therm("si_top", c)
    R["thermoelastic_delta_Si"] = float(p["E"]*1e6*(2.6e-6)**2*(Tr+273.15)/(t["rho"]*1e12*t["cp"]*1e-6*(1-2*p["nu"])))
    json.dump(R, open(f"{d}/verify.json", "w"), indent=1); print(json.dumps(R, indent=1)); return R

# ================================================================ 2) 본 해석
def fields_path(prod): return f"out3/thermal/{prod}/fields.npz"
def wait_fields(prod, every=30, tmax=3*3600):
    t0 = time.time()
    while not os.path.exists(fields_path(prod)):
        if time.time()-t0 > tmax: raise TimeoutError(fields_path(prod))
        time.sleep(every)
    time.sleep(5)
def tlabel(t): return "steady" if not np.isfinite(t) else f"{t:g}s"
def build_main(prod):
    d = odir(prod); g, ids, xyz, eids, conn, kf = model(prod); c = g["c"]; N = len(ids)
    F = np.load(fields_path(prod)); times, TF = np.asarray(F["times"], float), np.asarray(F["T"], float)
    assert TF.shape[1] == N, (TF.shape, N)
    lo, hi = int(np.floor(min(20., TF.min()-1))), int(np.ceil(max(240., TF.max()+5)))
    assert hi < 400
    Tt = np.arange(lo, hi+1, 1.0)
    s = [f"** SA one-way thermo-mech {prod}"] + geom_lines(g, ids, xyz, eids, conn, kf, "C3D8I")
    for k in KINDS:
        if not (kf == k).any(): continue
        p = S.props(k, c); eps = S.eps_free(k, Tt, c); Ev = S.E_of(k, Tt, c)
        s += [f"*MATERIAL, NAME={k}", "*ELASTIC"] + [f"{e:.3f},{p['nu']:.4f},{t:.1f}" for e, t in zip(Ev, Tt)]
        s += ["*EXPANSION, ZERO=0."] + [f"{ep/t:.7e},{t:.1f}" for ep, t in zip(eps, Tt)] + ["0.,400."]
        s += [f"*SOLID SECTION, ELSET=E_{k}, MATERIAL={k}"]
    s += bc_lines(g, ids, xyz) + ["*INITIAL CONDITIONS, TYPE=TEMPERATURE", "NALL,400."]
    steps = [("25C", 25.), ("230C", 230.), ("45C", 45.)] + [(tlabel(t), i) for i, t in enumerate(times)]
    pr_t = [0.01, 0.1]
    def printed(lab, t):
        if lab in ("25C", "45C", "steady"): return True
        if isinstance(t, float): return False
        return bool(any(np.isclose(times[t], x) for x in pr_t))
    meta = []
    for lab, v in steps:
        s += ["*STEP", "*STATIC", "*TEMPERATURE"]
        if isinstance(v, float): s += [f"NALL,{v}"]; tinfo = dict(Tmax=v, Tmin=v, Tmean=v)
        else:
            write_temp_inc(f"{d}/T_{v:02d}.inc", TF[v]); s += [f"*INCLUDE, INPUT=T_{v:02d}.inc"]
            tinfo = dict(Tmax=float(TF[v].max()), Tmin=float(TF[v].min()), Tmean=float(TF[v].mean()), time=float(times[v]) if np.isfinite(times[v]) else "inf")
        pr = printed(lab, v); s += ["*NODE FILE", "U"] + (["*EL PRINT, ELSET=E_PRT", "S"] if pr else []) + ["*END STEP"]
        meta.append(dict(label=lab, printed=pr, **tinfo))
    open(f"{d}/mech.inp", "w").write("\n".join(s)+"\n")
    json.dump(meta, open(f"{d}/steps.json", "w"), indent=1); return meta
def post(prod):
    d = odir(prod); g, ids, xyz, eids, conn, kf = model(prod); N = len(ids)
    meta = json.load(open(f"{d}/steps.json")); st = read_frd(f"{d}/mech.frd"); assert len(st) == len(meta), (len(st), len(meta))
    W = {m["label"]: top_w(g, disp(s, N)) for m, s in zip(meta, st)}
    els = read_elprint(f"{d}/mech.dat"); pl = [m["label"] for m in meta if m["printed"]]; assert len(els) == len(pl)
    SM = {lab: stress_metrics(g, eids, kf, a) for lab, a in zip(pl, els)}
    w45 = W["45C"]; m45 = metrics(g, w45); out = []
    for m in meta:
        lab = m["label"]; mm = metrics(g, W[lab]); dm = metrics(g, W[lab]-w45)
        r = dict(m, **mm, dwarp_phy=mm["warp_phy"]-m45["warp_phy"], dwarp_far=mm["warp_far"]-m45["warp_far"],
                 dcopl=mm["copl"]-m45["copl"], copl_of_dw=dm["copl"], uz_top_max=float(W[lab].max()), uz_top_min=float(W[lab].min()))
        if lab in SM: r["stress"] = SM[lab]
        out.append(r)
    Yf, _ = mirror(g, w45)
    np.savez(f"{d}/top_w.npz", X=g["X"], Yf=Yf, labels=np.array(list(W)), W=np.array([mirror(g, W[k])[1] for k in W]))
    summ = dict(prod=prod, conv="warp = w(center) - w(DRAM vertex) [um], + = Cry; plane (area-weighted LSQ over DRAM 10x10 mm) removed; "
                "phy = corners x=-5 mm (GPU/PHY side), far = x=+5 mm; d* = relative to uniform 45C step; copl_of_dw = coplanarity of (w - w45C); "
                "stress = element-average [MPa], phy = elements within PHY footprint (all z), mesh-dependent (0.19 mm in-plane)",
                phy_box=list(map(float, g["phy_box"])), phy_W=G.PRODUCTS[prod]["phy_W"], steps=out)
    json.dump(summ, open(f"{d}/summary.json", "w"), indent=1)
    for r in out:
        s = r.get("stress", {})
        print(f"{r['label']:>8} Tmax {r['Tmax']:6.1f} warpPHY {r['warp_phy']:7.3f} far {r['warp_far']:7.3f} copl {r['copl']:6.3f} "
              f"dPHY {r['dwarp_phy']:+.3f} dFar {r['dwarp_far']:+.3f} coplDw {r['copl_of_dw']:.3f}"
              + (f" | Si {s['si_s1_all']:.1f} baseSi {s['si_base_s1_all']:.1f} peel {s['gap_peel_all']:.1f} shr {s['gap_shear_all']:.1f} beol {s['beol_s1_all']:.1f}" if s else ""))
    return summ
def run(prod):
    wait_fields(prod); meta = build_main(prod); d = odir(prod)
    t = ccx(d, "mech"); print(f"{prod}: ccx {t:.0f} s, {len(meta)} steps"); post(prod)

# ================================================================ 3) 그림
def figs():
    import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
    plt.rcParams["font.family"] = "NanumGothic"; plt.rcParams["axes.unicode_minus"] = False
    os.makedirs("figs", exist_ok=True); prods = [p for p in G.PRODUCTS if os.path.exists(f"out3/mech/{p}/summary.json")]
    fig, ax = plt.subplots(1, 2, figsize=(12, 4.6)); col = {"hbm4_8h": "tab:red", "hbm3e_12h": "tab:blue"}
    for p in prods:
        R = [r for r in json.load(open(f"out3/mech/{p}/summary.json"))["steps"] if r["label"].endswith("s") or r["label"] == "steady"]
        tr = [r for r in R if r["label"] != "steady"]; t = np.array([r["time"] for r in tr]); tss = t.max()*10
        for key, ls, nm in (("phy", "-", "PHY 측"), ("far", "--", "반대측")):
            for a, pre in ((ax[0], "warp_"), (ax[1], "dwarp_")):
                y = [r[pre+key] for r in tr]; ys = [r[pre+key] for r in R if r["label"] == "steady"]
                a.plot(t, y, ls, marker="o", ms=3, color=col[p], label=f"{p} {nm}")
                if ys: a.plot([tss], ys, marker="*", ms=11, color=col[p], ls="none")
        r45 = [r for r in json.load(open(f"out3/mech/{p}/summary.json"))["steps"] if r["label"] == "45C"][0]
        ax[0].axhline(r45["warp_phy"], color=col[p], lw=0.7, ls=":")
    for a, tt in zip(ax, ("warp (중앙 - 모서리) [μm], 점선 = 45 °C 균일", "Δwarp (운전 - 45 °C 균일) [μm]")):
        a.set_xscale("log"); a.set_xlabel("시간 [s] (★ = 정상상태)"); a.set_title(tt); a.grid(alpha=0.3); a.legend(fontsize=8)
    fig.suptitle("PHY 발열에 따른 상면 warpage 변화 (+ = Cry, 평면 보정)"); fig.tight_layout(); fig.savefig("figs/sa_warp_vs_time.png", dpi=150); plt.close(fig)
    for p in prods:
        Z = np.load(f"out3/mech/{p}/top_w.npz"); lab = list(Z["labels"]); X, Yf, W = Z["X"], Z["Yf"], Z["W"]
        g = G.grid(p); pb = g["phy_box"]; x0, x1, hy = dram_box(g)
        def deplane(w):
            mx, my = (X >= x0-1e-9) & (X <= x1+1e-9), np.abs(Yf) <= hy+1e-9; XX, YY = np.meshgrid(X, Yf, indexing="ij")
            wt = np.outer(trib(X[mx]), trib(Yf[my])).ravel(); A = np.c_[np.ones(wt.size), XX[np.ix_(mx, my)].ravel(), YY[np.ix_(mx, my)].ravel()]
            sw = np.sqrt(wt); c = np.linalg.lstsq(A*sw[:, None], w[np.ix_(mx, my)].ravel()*sw, rcond=None)[0]
            return w - (c[0]+c[1]*XX+c[2]*YY)
        sel = [("45C", "45 °C 균일 (t=0)"), (next((l for l in lab if l in ("0.1s",)), None), "t = 0.1 s"), ("steady", "정상상태")]
        panels = [(deplane(W[lab.index(k)]), t) for k, t in sel if k in lab]
        if "steady" in lab: panels.append((deplane(W[lab.index("steady")]-W[lab.index("45C")]), "Δ(정상 - 45 °C)"))
        fig, ax = plt.subplots(1, len(panels), figsize=(4.4*len(panels), 4.2))
        for a, (w, tt) in zip(np.atleast_1d(ax), panels):
            v = np.abs(w).max(); cs = a.contourf(X, Yf, w.T, 31, cmap="RdBu_r", vmin=-v, vmax=v); fig.colorbar(cs, ax=a, shrink=0.8, label="w [μm]")
            a.add_patch(plt.Rectangle((x0, -hy), x1-x0, 2*hy, fill=False, ls="--", lw=0.8))
            a.add_patch(plt.Rectangle((pb[0], -pb[3]), pb[1]-pb[0], 2*pb[3], fill=False, ec="k", lw=1.2))
            a.set_aspect("equal"); a.set_title(tt); a.set_xlabel("x [mm] (x<0: GPU/PHY 측)"); a.set_ylabel("y [mm]")
        fig.suptitle(f"{p} 상면 w(x,y) (평면 보정, 대칭 확장, 실선 = PHY)"); fig.tight_layout(); fig.savefig(f"figs/sa_topw_{p}.png", dpi=150); plt.close(fig)
    print("figs written")

if __name__ == "__main__":
    a = sys.argv[1]
    if a == "verify": verify(*sys.argv[2:3])
    elif a == "run": run(sys.argv[2])
    elif a == "post": post(sys.argv[2])
    elif a == "figs": figs()
