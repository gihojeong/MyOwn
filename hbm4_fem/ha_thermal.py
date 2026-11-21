"""[HA] grid3 공통 격자 위 HBM 스택 열해석 (DC3D8, 1/2 대칭) — 고객 사용환경(수냉 AI 가속기) 시나리오, 제품별 병렬.
시나리오 "use": step1 idle 정상상태(t=0 기준장) → t=0 full-load 계단(스택 전력 + GPU 결합 경계온도) → 과도 TP → load 정상상태.
시나리오 "phy": (이전 요청) PHY 만 발열, 상·하면 45 °C film, 45 °C 균일 초기상태 → 과도 → 정상.
출력(SA 계약): out3/thermal/<prod>/fields.npz (times: [0, TP..., inf], T[n_t, N] float32, 열 = node id-1, X,Y,Z), summary.json
       (phy 시나리오는 out3/thermal_phyonly/<prod>/).
시간점 누락 방지: *TIME POINTS 대신 시간점마다 *STEP 분할, 각 step 끝에서만 출력(FREQUENCY 큼). frd 100CL 헤더 시간으로 검증.
usage: python3 ha_thermal.py [use|phy]           (두 제품 병렬 + 후처리)
       python3 ha_thermal.py one <prod> [use|phy] / post <prod> [use|phy]"""
import sys, os, json, time, subprocess, numpy as np
import grid3
from thermal2 import therm, kSi
from frd import read_frd

TP = [1e-4, 3e-4, 1e-3, 3e-3, 1e-2, 3e-2, 0.1, 0.3, 1.0, 3.0]
NAME, BIG, DELTMX = "ha", 1000000, 2.0
# ---------------- 고객 사용환경 정의 (근거·불확실성은 보고서 표 참조) ----------------
# 상면: Si top → TIM1 → lid → TIM2 → cold plate → 냉각수. R''≈0.45 cm²K/W (TIM1 0.15, lid 0.05, TIM2 0.10, CP 0.15) → h≈22000
#   싱크온도 = 냉각수(TCS 공급 45 °C, NVIDIA/ASHRAE W45 상한) + 유로 승온 3 K + GPU 발열에 의한 lid/CP 국부 승온(GPU 쪽 지수 감쇠)
# 하면: base die μbump/underfill → Si interposer. interposer 온도는 GPU(Tj≈85 °C 부하)에서 측방 감쇠 (λ≈2 mm), h=5000 (R''≈2 cm²K/W)
ENV = dict(
    gap=0.5,                                        # GPU die 변 ~ HBM 변 간격 [mm]
    h_top=22000., lam_top=5.0, h_bot=5000., lam_bot=2.0,
    load=dict(T_cool=48., dT_lid=10., T_int_far=55., T_int_edge=80.),
    idle=dict(T_cool=46., dT_lid=1.5, T_int_far=47., T_int_edge=50.),
)
# 스택 전력 [W, 전체 스택]: PHY = grid3 값; base 기타 로직; core DRAM(전 코어 die 합, die 별 균일, active=BEOL 층)
POWER = {
    "hbm3e_12h": dict(load=dict(phy=None, base=4.0, core=20.0), idle=dict(phy=1.0, base=0.5, core=1.0)),
    "hbm4_8h":   dict(load=dict(phy=None, base=6.0, core=21.0), idle=dict(phy=1.5, base=0.8, core=1.0)),
}


def root(sc): return "out3/thermal" if sc == "use" else "out3/thermal_phyonly"
def odir(prod, sc):
    d = f"{root(sc)}/{prod}"; os.makedirs(d, exist_ok=True); return d
def powers(prod, sc, state):
    if sc == "phy": return dict(phy=grid3.PRODUCTS[prod]["phy_W"], base=0., core=0.) if state == "load" else dict(phy=0., base=0., core=0.)
    p = dict(POWER[prod][state]); p["phy"] = grid3.PRODUCTS[prod]["phy_W"] if p["phy"] is None else p["phy"]; return p


def model(prod):
    g = grid3.grid(prod); ids, xyz, eids, conn = grid3.nodes_elems(g)
    vol = np.einsum("i,j,k->ijk", np.diff(g["X"]), np.diff(g["Y"]), np.diff(g["Z"]))
    return g, ids, xyz, eids, conn, vol


def heat_groups(g):
    """요소 mask (3D) : phy, base(기타, PHY 제외 base Si 전면층), core die 별 BEOL"""
    zb0 = [l for l in __import__("stack").layers(g["c"]) if l[0] == "Base_Si"][0][2]
    kphy = int(np.argmin(abs(g["Z"]-zb0))); lay = np.arange(len(g["Z"])-1)[None, None, :] == kphy
    base = (g["lname"] == "Base_Si") & lay & ~g["phy"]
    cores = [g["lname"] == f"Core{i}_BEOL" for i in range(1, g["c"]["nh"]+1)]
    return g["phy"], base, cores


def sinks(g, sc, state):
    """요소 별 (top sink, bot sink) [°C] (상면·하면 요소층, 2D [nx-1, ny-1])"""
    xc = (g["X"][:-1]+g["X"][1:])/2; ny = len(g["Y"])-1
    if sc == "phy": T = np.full((len(xc), ny), grid3.BC["T_ref"]); return T, T
    e = ENV[state]; d = xc - g["X"][0] + ENV["gap"]
    top = e["T_cool"] + e["dT_lid"]*np.exp(-d/ENV["lam_top"]); bot = e["T_int_far"] + (e["T_int_edge"]-e["T_int_far"])*np.exp(-d/ENV["lam_bot"])
    return np.repeat(top[:, None], ny, 1), np.repeat(bot[:, None], ny, 1)
def hs(sc): return (grid3.BC["h_top"], grid3.BC["h_bot"]) if sc == "phy" else (ENV["h_top"], ENV["h_bot"])


def loads(prod, sc, state, g, vol, E3):
    P = powers(prod, sc, state); phy, base, cores = heat_groups(g); q = {}
    for key, m in (("phy", phy), ("base", base)): q.update({e: P[key]/2*1e3/vol[m].sum() for e in E3[m]} if P[key] > 0 else {})
    for m in cores:
        if P["core"] > 0: q.update({e: P["core"]/len(cores)/2*1e3/vol[m].sum() for e in E3[m]})
    s = ["*DFLUX, OP=NEW"] + [f"{e},BF,{v:.6e}" for e, v in sorted(q.items())]
    (Tt, Tb), (ht, hb) = sinks(g, sc, state), hs(sc)
    s += ["*FILM, OP=NEW"] + [f"{e},F2,{t:.4f},{ht*1e-3:.4e}" for e, t in zip(E3[:, :, -1].ravel(), Tt.ravel())]
    s += [f"{e},F1,{t:.4f},{hb*1e-3:.4e}" for e, t in zip(E3[:, :, 0].ravel(), Tb.ravel())]
    return s, P


def build(prod, sc):
    g, ids, xyz, eids, conn, vol = model(prod); c = g["c"]
    kf = g["kind"].ravel(order="F"); E3 = eids.reshape(g["kind"].shape, order="F")
    s = [f"** HA {prod} {sc}", "*NODE, NSET=NALL"] + [f"{n},{a:.6f},{b:.6f},{d:.7f}" for n, (a, b, d) in zip(ids, xyz)]
    s.append("*ELEMENT, TYPE=DC3D8, ELSET=EALL"); s += [f"{e}," + ",".join(map(str, cc)) for e, cc in zip(eids, conn)]
    TT = np.array([0, 25, 50, 75, 100, 125, 150, 200])
    for k in np.unique(kf):
        e = eids[kf == k]; t = therm(k, c)
        s += [f"*ELSET, ELSET=E_{k}"] + [",".join(map(str, e[i:i+16])) for i in range(0, len(e), 16)]
        s += [f"*MATERIAL, NAME=T_{k}", "*CONDUCTIVITY, TYPE=ORTHO"]
        s += ([f"{kSi(T):.3f},{kSi(T):.3f},{kSi(T):.3f},{T:.1f}" for T in TT] if t["kxy"] is None
              else [f"{t['kxy']:.4f},{t['kxy']:.4f},{t['kz']:.4f}"])
        s += ["*DENSITY", f"{t['rho']:.4e}", "*SPECIFIC HEAT", f"{t['cp']:.4e}", f"*SOLID SECTION, ELSET=E_{k}, MATERIAL=T_{k}"]
    T0 = grid3.BC["T_ref"] if sc == "phy" else ENV["idle"]["T_cool"]
    s += ["*INITIAL CONDITIONS, TYPE=TEMPERATURE", f"NALL,{T0}"]
    out = [f"*NODE FILE, FREQUENCY={BIG}", "NT", "*END STEP"]
    if sc == "use":                                                   # step 1: idle 정상상태 (t=0 기준장)
        li, _ = loads(prod, sc, "idle", g, vol, E3)
        s += ["*STEP, INC=100", "*HEAT TRANSFER, STEADY STATE", "1.,1."] + li + out
    ll, P = loads(prod, sc, "load", g, vol, E3); t0 = 0.0
    for i, tp in enumerate(TP):
        span = tp - t0; dt0 = 2e-6 if i == 0 else span/5
        s += ["*STEP, INC=100000", f"*HEAT TRANSFER, DELTMX={DELTMX}", f"{dt0:.6e}, {span:.6e}, 1e-10, {span:.6e}"]
        if i == 0: s += ll
        s += out; t0 = tp
    s += ["*STEP, INC=100", "*HEAT TRANSFER, STEADY STATE", "1.,1."] + out
    open(f"{odir(prod, sc)}/{NAME}.inp", "w").write("\n".join(s)+"\n")
    print(f"[{prod}/{sc}] nodes {len(ids):,} elems {len(eids):,} load P={P}", flush=True)


def solve(prod, sc):
    d = odir(prod, sc); t = time.time()
    subprocess.run(["ccx", "-i", NAME], cwd=d, env=dict(os.environ, OMP_NUM_THREADS="1"), stdout=open(f"{d}/{NAME}.log", "w"), check=True)
    print(f"[{prod}/{sc}] solved in {time.time()-t:.0f} s", flush=True)


def frd_times(fn): return [float(l.split()[2]) for l in open(fn) if l.startswith("  100CL")]


def post(prod, sc):
    d = odir(prod, sc); g, ids, xyz, eids, conn, vol = model(prod); N = len(ids)
    tf = frd_times(f"{d}/{NAME}.frd"); steps = read_frd(f"{d}/{NAME}.frd")
    off = 1.0 if sc == "use" else 0.0
    exp_t = ([1.0] if sc == "use" else []) + [off+t for t in TP] + [off+TP[-1]+1.0]
    assert len(tf) == len(exp_t) == len(steps), f"frd records {len(tf)} vs expected {len(exp_t)}: {tf}"
    assert np.allclose(tf, exp_t, rtol=0, atol=1e-6*max(exp_t)), f"time mismatch {tf}"
    times = np.array(([0.0] if sc == "use" else []) + TP + [np.inf]); T = np.zeros((len(times), N), np.float32)
    for i, st in enumerate(steps):
        nid, v = st["NDTEMP"]; assert len(nid) == N; T[i, nid-1] = v[:, 0]
    kind = g["kind"].ravel(order="F"); lname = g["lname"].ravel(order="F"); V = vol.ravel(order="F")
    E3 = eids.reshape(g["kind"].shape, order="F")
    phy3, base3, cores3 = heat_groups(g)
    core_si = np.char.startswith(lname, "Core")
    grp = dict(phy=phy3.ravel(order="F"), base=lname == "Base_Si", top_si=kind == "si_top", core_dies=core_si,
               pkg=np.ones(len(V), bool))
    Te = T[:, conn-1].mean(-1)
    A2 = np.diff(g["X"])[:, None]*np.diff(g["Y"])[None, :]
    (ht, hb) = hs(sc)
    def film(Tn, state):
        Tt, Tb = sinks(g, sc, state); out = {}
        for key, lay, sl, h, Ts in (("bot", 0, slice(0, 4), hb, Tb), ("top", -1, slice(4, 8), ht, Tt)):
            e = E3[:, :, lay].ravel(order="F")-1; Tf = Tn[conn[e][:, sl]-1].mean(-1)
            out[key] = float((h*1e-3*A2.ravel(order="F")*(Tf-Ts.ravel(order="F"))).sum())*2e-3     # W, 전체(×2)
        return out
    R = []
    for i, t in enumerate(times):
        state = "idle" if (sc == "use" and i == 0) else "load"
        k = int(np.argmax(T[i])); f = film(T[i].astype(float), state)
        kc = int(np.argmax(np.where(core_si, Te[i], -1e9)))
        r = dict(t=float(t), state=state, Tmax=float(T[i, k]), Tmax_xyz=[round(float(v), 4) for v in xyz[k]],
                 Tmax_core_elem=float(Te[i, kc]), Tmax_core_lname=str(lname[kc]))
        for key, m in grp.items(): r[key] = float((Te[i, m]*V[m]).sum()/V[m].sum())
        r["Q_top_W"], r["Q_bot_W"] = f["top"], f["bot"]; R.append(r)
    P = powers(prod, sc, "load"); Ptot = sum(P.values()); ss = R[-1]
    eb = (ss["Q_top_W"]+ss["Q_bot_W"]-Ptot)/Ptot
    eb0 = None
    if sc == "use":
        Pi = sum(powers(prod, sc, "idle").values()); eb0 = (R[0]["Q_top_W"]+R[0]["Q_bot_W"]-Pi)/Pi
    # 집중 RC (전체 모델): T_ss = (P + hA_t·T̄t + hA_b·T̄b)/((ht+hb)A), τ = C/((ht+hb)A)
    rcp = np.zeros(len(kind))
    for k in np.unique(kind): t_ = therm(k, g["c"]); rcp[kind == k] = t_["rho"]*t_["cp"]
    C = 2*(rcp*V).sum()*1e-3; A = 2*A2.sum()*1e-6                                # J/K, m²
    Tt, Tb = sinks(g, sc, "load"); Tbar = lambda S_: float((S_*A2).sum()/A2.sum())
    G = (ht+hb)*A; Tss_rc = (Ptot + ht*A*Tbar(Tt) + hb*A*Tbar(Tb))/G; tau = C/G
    pk = np.array([r["pkg"] for r in R]); T_start = pk[0] if sc == "use" else grid3.BC["T_ref"]
    pk_tr = pk[1:-1] if sc == "use" else pk[:-1]
    fr = (pk_tr - T_start)/(pk[-1]-T_start)
    tau63 = float(np.exp(np.interp(1-np.exp(-1), fr, np.log(TP)))) if fr[-1] > 0.632 else None
    rc = dict(R_KperW=1/G, C_JperK=C, tau_RC_s=tau, Tpkg_ss_RC=Tss_rc, Tpkg_ss_FEM=float(pk[-1]), Tpkg_start=float(T_start),
              tau63_FEM_s=tau63, curve=[dict(t=t, Tpkg_FEM=float(a), Tpkg_RC=float(Tss_rc+(T_start-Tss_rc)*np.exp(-t/tau))) for t, a in zip(TP, pk_tr)])
    J = dict(product=prod, scenario=sc, power_load_W=P, power_idle_W=(powers(prod, sc, "idle") if sc == "use" else None),
             env=(ENV if sc == "use" else grid3.BC), h_top=ht, h_bot=hb, frd_times=tf, records=R,
             energy_balance=dict(P_in_W=Ptot, Q_top_W=ss["Q_top_W"], Q_bot_W=ss["Q_bot_W"], err_rel=float(eb), err_rel_idle=eb0),
             rc_check=rc, notes="times: 0=idle steady (use), inf=load steady; group means = volume-weighted element (8-node avg) means; "
                                "pkg = whole 1/2 model incl. EMC; Q_bot<0 means heat flows from interposer into HBM")
    json.dump(J, open(f"{d}/summary.json", "w"), indent=1)
    tmp = f"{d}/fields.tmp.npz"
    np.savez(tmp, times=times, T=T, X=g["X"], Y=g["Y"], Z=g["Z"]); os.replace(tmp, f"{d}/fields.npz")
    print(f"[{prod}/{sc}] P={Ptot:.1f} W  energy balance err {eb*100:+.3f} % (idle {None if eb0 is None else round(eb0*100,3)} %)  "
          f"Q_top {ss['Q_top_W']:.2f} Q_bot {ss['Q_bot_W']:.2f} W | RC: R={1/G:.4f} K/W C={C:.4e} J/K tau={tau*1e3:.1f} ms "
          f"Tpkg_ss RC {Tss_rc:.2f} FEM {pk[-1]:.2f} tau63_FEM {tau63}", flush=True)
    for r in R: print(f"  t={r['t']:<8g} Tmax={r['Tmax']:.2f} @{r['Tmax_xyz']} phy={r['phy']:.2f} base={r['base']:.2f} "
                      f"top={r['top_si']:.2f} core={r['core_dies']:.2f} coreMax={r['Tmax_core_elem']:.2f}({r['Tmax_core_lname']}) pkg={r['pkg']:.2f}")


if __name__ == "__main__":
    a = sys.argv[1:]
    if not a or a[0] in ("use", "phy"):
        sc = a[0] if a else "use"
        ps = [subprocess.Popen([sys.executable, __file__, "one", p, sc], stdout=open(f"{odir(p, sc)}/run.log", "w"), stderr=subprocess.STDOUT)
              for p in grid3.PRODUCTS]
        print("exit codes", [p.wait() for p in ps])
    elif a[0] == "one": sc = a[2] if len(a) > 2 else "use"; build(a[1], sc); solve(a[1], sc); post(a[1], sc)
    elif a[0] == "post": post(a[1], a[2] if len(a) > 2 else "use")
