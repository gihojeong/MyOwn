"""v2 적층 모델 — S사 HBM viewer(v219) 입력 기준. TCB(TC-NCF) 전용.
단위 mm, MPa, °C.  부호 규약(viewer): warp = 중앙 − vertex, (+) Cry(중앙 볼록) / (−) Smile.
[규칙] 총두께는 세대별 고정(HBM3E 720, HBM4 775 μm). 두께 변경분은 top core Si 가 흡수."""
import numpy as np

GEN_TOT = {"hbm3e": 0.720, "hbm4": 0.775}
L_DRAM, L_LOGIC = 10.0, 11.5            # die 변 [mm] (몰드바디 = logic)

# ---- 두께·물성 세트 (viewer ① 입력 DEF / SET_MICRON) ----
DESIGN = dict(lsi=0.0444, lm=0.0174, mm=0.0099, tm=0.0096, ms={12: 0.0273, 8: 0.0356}, nc=0.0072,
              mE=102.5e3, mA=9.9e-6, oxT=0.0010, nxT=0.0004)
MICRON = dict(lsi=0.0576, lm=0.0174, mm=0.0078, tm=0.0096, ms={12: 0.0262, 8: 0.0262}, nc=0.0110,
              mE=107.3e3, mA=7.64e-6, oxT=0.0010, nxT=0.0004)
MAT = dict(
    si=dict(M=180.5e3, nu=0.28, a=2.6e-6),
    snag=dict(M=50e3/0.64, nu=0.36, a=22e-6),
    ncf=dict(M=8e3/0.70, nu=0.30, tg=130., a1=30e-6, a2=90e-6),
    emc=dict(M=20e3, nu=0.30, tg=150., a1=15e-6, a2=45e-6),     # viewer eE(=M), eA, eA2, eTg
    ox=dict(M=86.7e3, a=0.5e-6), nx=dict(M=333e3, a=3.2e-6),
    beol_nu=0.34,
)
VF_VIEWER = np.pi/4*(25/45)**2          # viewer 기본 D25/P45 → 0.2424 (참고)
BUMP = dict(D=0.015, N={"hbm3e": 200_000, "hbm4": 250_000}, N_tsv=25_000)   # 총 개수(TSV 포함), 직경 15 μm
def bump_vf(gen):
    """vf = N·πD²/4 / A_DRAM  (TSV·dummy 동일 pitch 가정) → HBM3E 0.353, HBM4 0.442"""
    return BUMP["N"][gen]*np.pi/4*BUMP["D"]**2/L_DRAM**2
def tsv_band(gen):
    """TSV 영역 면적 = N_tsv/N · A_DRAM (같은 pitch) → 중앙 band 폭 [mm] (길이 = L_DRAM)"""
    return BUMP["N_tsv"]/BUMP["N"][gen]*L_DRAM
T0 = dict(b=400., j=217., m=175.)       # 무응력: Si·BEOL(T0b) / NCF+SnAg(T0j) / EMC(T0m)
MEAS = dict(w25=-7.6, w230=-2.1)        # HBM3E-12H 실측 (중앙−vertex, μm)

def case(gen="hbm3e", nh=12, set_="design", **over):
    """케이스 dict. over 로 임의 값 덮어쓰기 (예: ms=0.0326, nc=0.0080, t0b=300, ncf_a1=40e-6 ...)"""
    S = dict(DESIGN if set_ == "design" else MICRON); S["ms"] = S["ms"][nh]
    c = dict(gen=gen, nh=nh, set=set_, tot=GEN_TOT[gen], vf=bump_vf(gen), t0b=T0["b"], t0j=T0["j"], t0m=T0["m"],
             cte_mode="integral", **S)
    c.update(over); return c

def top_si(c):
    return c["tot"] - (c["lm"] + c["lsi"] + (c["nh"]-1)*(c["nc"]+c["mm"]+c["ms"]) + c["nc"] + c["tm"])

def layers(c):
    """bottom→top: (name, kind, z0, z1, half_span)  kind ∈ beol, si_base(순수 Si), gap, si(mid, BS-ONO 혼합), si_top, emc"""
    L, z = [], 0.0; hl, hd = L_LOGIC/2, L_DRAM/2
    def add(n, k, t, h):
        nonlocal z; L.append((n, k, z, z+t, h)); z += t
    add("Base_BEOL", "beol", c["lm"], hl); add("Base_Si", "si_base", c["lsi"], hl)
    zr0 = z
    for i in range(1, c["nh"]+1):
        add(f"Gap_{i}", "gap", c["nc"], hd)
        if i < c["nh"]:
            add(f"Core{i}_BEOL", "beol", c["mm"], hd); add(f"Core{i}_Si", "si", c["ms"], hd)
        else:
            ts = top_si(c); assert ts > 0.01, f"top Si {ts*1e3:.1f} μm"
            add(f"Core{i}_BEOL", "beol", c["tm"], hd); add(f"Core{i}_Si", "si_top", ts, hd)
    assert abs(z - c["tot"]) < 1e-9
    L.append(("EMC_Ring", "emc", zr0, z, hl))
    return L

# ---- 물성 / 자유 열변형률 ε_F(T) (각 재료 자기 무응력 온도 기준) ----
def _alpha(kind, T, c):
    m = MAT
    if kind in ("si", "si_top", "si_base"):
        if kind == "si":     # mid core Si 안의 BS-ONO 를 M 가중 혼합 (동일 T0b)
            ts = c["ms"]; fo, fn = c["oxT"]/ts, c["nxT"]/ts; fs = 1-fo-fn
            M = fs*m["si"]["M"]+fo*m["ox"]["M"]+fn*m["nx"]["M"]
            return (fs*m["si"]["M"]*m["si"]["a"]+fo*m["ox"]["M"]*m["ox"]["a"]+fn*m["nx"]["M"]*m["nx"]["a"])/M*np.ones_like(T)
        return m["si"]["a"]*np.ones_like(T)
    if kind == "beol": return c["mA"]*np.ones_like(T)
    if kind == "gap":
        aN = np.where(T < c.get("ncf_tg", m["ncf"]["tg"]), c.get("ncf_a1", m["ncf"]["a1"]), c.get("ncf_a2", m["ncf"]["a2"]))
        Ms, Mn = m["snag"]["M"], poly_M("ncf", T, c); v = c["vf"]
        return (v*Ms*m["snag"]["a"] + (1-v)*Mn*aN)/(v*Ms+(1-v)*Mn)
    if kind == "emc":
        return np.where(T < c.get("emc_tg", m["emc"]["tg"]), c.get("emc_a1", m["emc"]["a1"]), c.get("emc_a2", m["emc"]["a2"]))
SOFT = dict(ncf=0.3e3/0.70, emc=1.0e3, w=8.0)   # Tg 이상 고무영역 M [MPa] (c["soft"]=True 일 때)
def _tanh(T, lo, hi, Tg, w): return lo + (hi-lo)*0.5*(1+np.tanh((T-Tg)/w))
def poly_M(name, T, c):
    m = MAT[name]; Mg = c.get(f"{name}_M", m["M"]); T = np.asarray(T, float)
    if not c.get("soft"): return Mg*np.ones_like(T)
    return _tanh(T, Mg, c.get(f"{name}_Mr", SOFT[name]), c.get(f"{name}_tg", m["tg"]), SOFT["w"])
def E_of(kind, T, c):
    """온도 의존 E [MPa] (soft=False 이면 상수)"""
    p = props(kind, c); T = np.asarray(T, float)
    if kind == "gap":
        v = c["vf"]; Mf, Mm = MAT["snag"]["M"], poly_M("ncf", T, c)
        if c.get("soft"):   # 면내: 고립 기둥(bump) + 연질 기지 → Halpin-Tsai (ξ=2)
            eta = (Mf/Mm-1)/(Mf/Mm+2); M = Mm*(1+2*eta*v)/(1-eta*v)
        else: M = v*Mf + (1-v)*Mm          # viewer 규약 (Voigt)
        return M*(1-p["nu"])
    if kind == "emc": return poly_M("emc", T, c)*(1-p["nu"])
    return p["E"]*np.ones_like(T)
def props(kind, c):
    m = MAT
    if kind in ("si", "si_top", "si_base"):
        if kind == "si":
            ts = c["ms"]; fo, fn = c["oxT"]/ts, c["nxT"]/ts; M = (1-fo-fn)*m["si"]["M"]+fo*m["ox"]["M"]+fn*m["nx"]["M"]
        else: M = m["si"]["M"]
        nu = m["si"]["nu"]; T0 = c["t0b"]
    elif kind == "beol": M, nu, T0 = c["mE"], m["beol_nu"], c["t0b"]
    elif kind == "gap":
        v = c["vf"]; Mn = c.get("ncf_M", m["ncf"]["M"]); M = v*m["snag"]["M"]+(1-v)*Mn
        nu = v*m["snag"]["nu"]+(1-v)*m["ncf"]["nu"]; T0 = c["t0j"]
    elif kind == "emc": M, nu, T0 = c.get("emc_M", m["emc"]["M"]), m["emc"]["nu"], c["t0m"]
    return dict(E=M*(1-nu), nu=nu, T0=T0)
def eps_free(kind, T, c):
    """ε_F(T): cte_mode 'integral' = ∫_{T0}^{T} α dT (물리), 'viewer' = α(T)·(T−T0) (viewer CLT 규약)"""
    T = np.atleast_1d(np.asarray(T, float)); T0 = props(kind, c)["T0"]
    if c["cte_mode"] == "viewer": return _alpha(kind, T, c)*(T-T0)
    out = []
    for t in T:
        tt = np.linspace(T0, t, 2001); a = _alpha(kind, tt, c)
        out.append(np.trapezoid(a, tt))
    return np.array(out)

def clt_warp(c, T):
    """viewer 방식 CLT 검산: 구면 곡률 → DRAM vertex warp (중앙−vertex, μm). 측면 EMC 는 면적혼합 F_eff=0.85."""
    F = 1-0.615*(1-(L_DRAM/L_LOGIC)**2); z = [0.0]; Ls = []
    Me, eE = props("emc", c)["E"]/(1-props("emc", c)["nu"]), eps_free("emc", T, c)[0]
    for (n, k, z0, z1, h) in layers(c):
        if k == "emc": continue
        p = props(k, c); M = p["E"]/(1-p["nu"]); e = eps_free(k, T, c)[0]
        if h < L_LOGIC/2:  # DRAM 레벨: EMC 와 면적 혼합
            Mm = F*M+(1-F)*Me; e = (F*M*e+(1-F)*Me*eE)/Mm; M = Mm
        Ls.append((z1-z0, M, e))
    zz = np.cumsum([0]+[l[0] for l in Ls]); zm = zz[-1]/2; A = B = D = N = Mt = 0
    for (t, M, e), z0, z1 in zip(Ls, zz[:-1]-zm, zz[1:]-zm):
        A += M*(z1-z0); B += M*(z1**2-z0**2)/2; D += M*(z1**3-z0**3)/3; N += M*e*(z1-z0); Mt += M*e*(z1**2-z0**2)/2
    k = (A*Mt-B*N)/(A*D-B*B)                       # 1/mm, w = −½κr² 규약 → 중앙−vertex = +½κ r²
    return 0.5*k*(L_DRAM/np.sqrt(2))**2*1e3

# ---- 보정 결과 (validate2/calib2, HBM3E-12H 실측 25/230 °C) ----
#  viewer 규약(상수 E, Voigt gap)  : 25→230 °C 변화폭 13.5 μm (실측 5.5) → T0b 로는 보정 불가
#  Tg 연화 + Halpin-Tsai, Micron 실측두께 세트: 변화폭 5.42 μm, T0b=284 °C → |w25| 7.6, |w230| 1.67 (실측 2.1)
#  설계 두께 세트는 같은 물성으로 변화폭 10.6 μm → 실측과 불일치 (두께·BEOL 물성 차이가 지배)
CALIB_VF024 = dict(soft=True, t0b=284.)   # vf 0.242 기준 (구)
