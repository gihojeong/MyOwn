"""[HA] 3D Lock-in thermography (주파수 영역): (K + iωC)θ = Q, 선형 8절점 hex(직교격자) 해석적 요소행렬.
HBM3E-12H, 1/4 대칭(결함 = die 중앙). 결함 열원: Core k BEOL(소자층) 중앙 요소, 관측: 중앙 상면 절점. 위상 지연(+) [deg].
usage: python3 -u ha_lit.py [h_inplane=0.3] [freqs comma]"""
import sys, json, time, numpy as np, scipy.sparse as sp
from scipy.sparse.linalg import splu
import grid3 as G, stack as S, thermal2 as TH
P = "hbm3e_12h"; T_OP = 65.0
FREQ = [1, 2, 3, 4, 5, 6, 8, 10, 12, 15, 20, 25, 30, 40, 50, 60, 80, 100]
H = float(sys.argv[1]) if len(sys.argv) > 1 else 0.3
if len(sys.argv) > 2: FREQ = [float(v) for v in sys.argv[2].split(",")]
g = G.grid(P); Z = g["Z"]; c = g["c"]; lx, ly, dx, dy = S.Lxy(c)
X = G._axis([0, dx/2, lx/2], H); Y = G._axis([0, dy/2, ly/2], H); nx, ny, nz = len(X), len(Y), len(Z)
xc, yc, zc = (X[:-1]+X[1:])/2, (Y[:-1]+Y[1:])/2, (Z[:-1]+Z[1:])/2
XC, YC, ZC = np.meshgrid(xc, yc, zc, indexing="ij"); kind = np.full(XC.shape, "", "<U10"); lname = np.full(XC.shape, "", "<U16")
for (n_, k_, z0, z1, h_) in sorted(S.layers(c), key=lambda l: l[1] == "emc"):
    m_ = (XC < h_) & (YC < S.half_y(c, h_)) & (ZC > z0) & (ZC < z1) & (kind == ""); kind[m_] = k_; lname[m_] = n_
assert (kind != "").all(); print(f"grid {nx}x{ny}x{nz} = {nx*ny*nz:,} nodes, h={H}", flush=True)
N = nx*ny*nz; nid = lambda i, j, k: i + nx*(j + ny*k)
s1 = lambda h: np.array([[1, -1], [-1, 1]])/h; m1 = lambda h: h/6*np.array([[2, 1], [1, 2]])
def props(k):
    t = TH.therm(k, c)
    if t["kxy"] is None: kk = float(TH.kSi(T_OP)); return kk, kk, t["rho"]*t["cp"]
    return t["kxy"], t["kz"], t["rho"]*t["cp"]
PR = {k: props(k) for k in np.unique(kind)}
I, J, K = np.meshgrid(range(nx-1), range(ny-1), range(nz-1), indexing="ij"); I, J, K = I.ravel(), J.ravel(), K.ravel()
loc = [(a, b, d) for a in (0, 1) for b in (0, 1) for d in (0, 1)]                       # kron 순서 (x,y,z)
conn = np.stack([nid(I+a, J+b, K+d) for a, b, d in loc], 1)
rows, cols, kv, cv = [], [], [], []
hx, hy, hz = np.diff(X)[I], np.diff(Y)[J], np.diff(Z)[K]; kd = kind[I, J, K]
for kk in PR:
    msk = kd == kk; kxy, kz, rc = PR[kk]
    a, b, d = hx[msk], hy[msk], hz[msk]
    # 요소행렬 = kx·S(a)⊗M(b)⊗M(c) + ky·M⊗S⊗M + kz·M⊗M⊗S ;  C = ρc·M⊗M⊗M  (벡터화)
    Sa = np.einsum("n,ij->nij", 1/a, s1(1)); Ma = np.einsum("n,ij->nij", a, m1(1))
    Sb = np.einsum("n,ij->nij", 1/b, s1(1)); Mb = np.einsum("n,ij->nij", b, m1(1))
    Sd = np.einsum("n,ij->nij", 1/d, s1(1)); Md = np.einsum("n,ij->nij", d, m1(1))
    kr = lambda A, B, C: np.einsum("nij,nkl,nmo->nikmjlo", A, B, C).reshape(len(a), 8, 8)
    Ke = kxy*kr(Sa, Mb, Md) + kxy*kr(Ma, Sb, Md) + kz*kr(Ma, Mb, Sd); Ce = rc*kr(Ma, Mb, Md)
    cn = conn[msk]; rows.append(np.repeat(cn, 8, 1).ravel()); cols.append(np.tile(cn, (1, 8)).ravel()); kv.append(Ke.ravel()); cv.append(Ce.ravel())
# film (상면 h_top, 하면 h_bot): h·M(x)⊗M(y) on face
for kface, h in ((nz-1, 22000.), (0, 5000.)):                                       # HA 사용환경 h [W/m²K]
    Ii, Jj = np.meshgrid(range(nx-1), range(ny-1), indexing="ij"); Ii, Jj = Ii.ravel(), Jj.ravel()
    a, b = np.diff(X)[Ii], np.diff(Y)[Jj]
    Fe = h*1e-3*np.einsum("nij,nkl->nikjl", np.einsum("n,ij->nij", a, m1(1)), np.einsum("n,ij->nij", b, m1(1))).reshape(len(a), 4, 4)
    cn = np.stack([nid(Ii+p, Jj+q, kface) for p in (0, 1) for q in (0, 1)], 1)
    rows.append(np.repeat(cn, 4, 1).ravel()); cols.append(np.tile(cn, (1, 4)).ravel()); kv.append(Fe.ravel()); cv.append(np.zeros(Fe.size))
r, cc = np.concatenate(rows), np.concatenate(cols)
Km = sp.csc_matrix((np.concatenate(kv), (r, cc)), shape=(N, N)); Cm = sp.csc_matrix((np.concatenate(cv), (r, cc)), shape=(N, N))
# 열원: Core k BEOL 요소 (x≈+2.5, y=0 인접) → 절점 등분배 (진폭 1 mW, 선형이라 위상 무관)
ix = 0; Q = np.zeros((N, 12)); obs = nid(0, 0, nz-1)
for k in range(1, 13):
    kk = [kz for kz in range(nz-1) if lname[ix, 0, kz] == f"Core{k}_BEOL"][0]
    for a_, b_, d_ in loc: Q[nid(ix+a_, 0+b_, kk+d_), k-1] += 1.0/8
# 검증: ω→0 정상해 (K θ = Q) 양수, 에너지 = Σh A θ
th0 = splu(Km).solve(Q); assert (th0[obs] > 0).all()
R = {"freq": FREQ, "phase_deg": {}, "amp_rel": {}}
t0 = time.time()
for f in FREQ:
    A = (Km + 2j*np.pi*f*Cm).tocsc(); lu = splu(A); th = lu.solve(Q.astype(complex))
    ph = -np.degrees(np.angle(th[obs])); amp = np.abs(th[obs])/th0[obs]
    for k in range(12):
        R["phase_deg"].setdefault(str(k+1), []).append(float(ph[k])); R["amp_rel"].setdefault(str(k+1), []).append(float(amp[k]))
    print(f"f={f:>5} Hz  phase lag Core1 {ph[0]:6.1f}  Core6 {ph[5]:6.1f}  Core12 {ph[11]:6.1f}  ({time.time()-t0:.0f}s)", flush=True)
R["h"] = H; json.dump(R, open(f"out3/thermal/hbm3e_12h/lit_h{H}.json", "w"), indent=1)
