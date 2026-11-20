"""HBM4-8H 형상/재료/하중 파라미터 (단위: mm, N, s, tonne, mW, K/°C).
CalculiX 일관 단위계: 응력 MPa, k[mW/mm/K] = k[W/m/K], h[mW/mm^2/K] = 1e-3*h[W/m^2/K]."""
import numpy as np

# ---------------- 형상 (공개자료 기반 가정치) ----------------
FOOT = (11.0, 12.8)          # base die = package footprint [mm]
INSET = 0.25                 # core die edge inset → EMC sidewall
TSV_BAND = (1.0, 10.0, 5.9, 6.9)   # x0,x1,y0,y1 : 중앙 TSV/µbump band
PHY = (0.25, 1.75, 0.6, 12.2)      # base die PHY (GPU측 edge)
T_BASE, T_BOND, T_CORE = 0.060, 0.015, 0.050

SCOPE = "TCB"                # [규칙] 해석 대상은 TCB(TC-NCF) 공법만. 기준 = B_TCNCF, DOE/신규 변형은 bond="NCF"
BASELINE = "B_TCNCF"
H_PKG = 0.720                # [규칙] 총 높이 720 μm 고정: 두께 변경분은 항상 top die(Core_Die_8)가 흡수
VARIANTS = {
    # name: bonding, mid-die(Core 1~7) 두께, EMC cap  → top die 두께는 H_PKG에서 자동 산출
    "A_MRMUF":      dict(bond="MUF", t_core=0.050, cap=0.000),   # top 190 μm
    "B_TCNCF":      dict(bond="NCF", t_core=0.050, cap=0.000),   # top 190 μm
    "C_MRMUF_CAP":  dict(bond="MUF", t_core=0.050, cap=0.090),   # top 100 μm
    "D_MID47":      dict(bond="MUF", t_core=0.047, cap=0.000),   # mid -3 μm → top 211 μm
    # ---- TCB 범위 (기준 B_TCNCF) ----
    "E_TCNCF_MID47": dict(bond="NCF", t_core=0.047, cap=0.000),  # B 대비 mid -3 μm → top 211 μm
}
REFERENCE_ONLY = ("A_MRMUF", "C_MRMUF_CAP", "D_MID47")         # MR-MUF: 참고용, DOE 대상 아님
def t_top(v):
    c = VARIANTS[v]; return H_PKG - T_BASE - 8*T_BOND - 7*c["t_core"] - c["cap"]

def layers(v):
    """bottom→top layer list: (name, kind, z0, z1, footprint)"""
    cfg = VARIANTS[v]; L = []; z = 0.0
    full = (0, FOOT[0], 0, FOOT[1]); core = (INSET, FOOT[0]-INSET, INSET, FOOT[1]-INSET)
    L.append(("Base_Die", "base", z, z+T_BASE, full)); z += T_BASE
    for k in range(1, 9):
        L.append((f"Bond_{k}", "bond", z, z+T_BOND, core)); z += T_BOND
        t = t_top(v) if k == 8 else cfg["t_core"]
        L.append((f"Core_Die_{k}", "core", z, z+t, core)); z += t
    if cfg["cap"] > 0:
        L.append(("EMC_Cap", "emc", z, z+cfg["cap"], full)); z += cfg["cap"]
    assert abs(z-H_PKG) < 1e-9
    return L, z

# ---------------- 열 하중/경계 ----------------
P_BASE = dict(phy=6.0, tsv=3.0, rest=3.0)   # W
P_CORE = dict(tsv=1.0, array=1.5)           # W per core die (x8 = 20 W)
H_TOP, T_TOP = 7000.0, 40.0                 # W/m2K (TIM+cold plate), °C
H_BOT, T_BOT = 4000.0, 65.0                 # µbump→interposer(GPU 가열)
T_STRESSFREE = 175.0                        # EMC/MUF 경화온도
SWEEP = [25, 75, 125, 150, 175, 200, 225, 260]

# ---------------- 재료 ----------------
def tanh_step(T, lo, hi, Tg, w=8.0):
    return lo + (hi-lo)*0.5*(1+np.tanh((T-Tg)/w))

POLY = {  # E_glass, E_rubber [MPa], Tg, a1, a2 [1/K], nu, k
    "EMC": dict(Eg=20e3, Er=0.8e3, Tg=165., a1=9e-6, a2=35e-6, nu=0.30, k=1.0),
    "NCF": dict(Eg=5e3,  Er=0.3e3, Tg=140., a1=40e-6, a2=110e-6, nu=0.35, k=0.4),
}
def poly(name, T):
    p = POLY[name]
    return dict(E=tanh_step(T, p["Eg"], p["Er"], p["Tg"]), nu=p["nu"],
                a=tanh_step(T, p["a1"], p["a2"], p["Tg"]), k=np.full_like(T, p["k"]), kz=np.full_like(T, p["k"]))
def si(T):
    TK = T+273.15
    return dict(E=np.full_like(T, 130e3), nu=0.28, a=(2.6+0.0040*(T-25))*1e-6,
                k=148*(298.15/TK)**1.3, kz=148*(298.15/TK)**1.3)
CU_BUMP = dict(E=90e3, nu=0.34, a=17.5e-6, k=140.)   # Cu pillar+SnAg 직렬 등가

def mix(m, fb, T):
    """matrix m(dict of arrays) + 원주형 범프/TSV 체적분율 fb → 등가 물성"""
    Eb, ab, kb = CU_BUMP["E"], CU_BUMP["a"], CU_BUMP["k"]
    Ev = fb*Eb + (1-fb)*m["E"]; Er = 1/(fb/Eb + (1-fb)/m["E"]); E = 0.5*(Ev+Er)   # Hill
    a = (fb*Eb*ab + (1-fb)*m["E"]*m["a"])/(fb*Eb + (1-fb)*m["E"])                  # Turner
    km = m["k"]; kz = fb*kb + (1-fb)*km
    kxy = km*((kb+km)+fb*(kb-km))/((kb+km)-fb*(kb-km))                               # Maxwell-Garnett
    nu = fb*CU_BUMP["nu"] + (1-fb)*m["nu"]
    return dict(E=E, nu=nu, a=a, k=kxy, kz=kz)

TT = np.array([25., 75., 125., 150., 165., 175., 185., 200., 225., 260.])
def material_table(bond):
    m = {"SI": si(TT), "SI_TSV": mix(si(TT), 0.03, TT), "EMC": poly("EMC", TT)}
    matrix = poly("EMC" if bond == "MUF" else "NCF", TT)
    m["BOND_TSV"] = mix(matrix, 0.20, TT); m["BOND_DUM"] = mix(matrix, 0.05, TT)
    return m

def secant_alpha(a_inst, T, T0=T_STRESSFREE):
    """순간 CTE → ZERO=T0 기준 secant CTE (CalculiX *EXPANSION 정의)"""
    Tf = np.linspace(T.min()-1, T.max()+1, 4001); af = np.interp(Tf, T, a_inst)
    eps = np.cumsum(af)*(Tf[1]-Tf[0]); eps -= np.interp(T0, Tf, eps)
    out = []
    for t in T:
        out.append(np.interp(t, Tf, af) if abs(t-T0) < 1 else np.interp(t, Tf, eps)/(t-T0))
    return np.array(out)
