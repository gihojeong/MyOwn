"""[PA 공통 인터페이스] 열(HA)·구조(SA) 해석이 공유하는 1/2 대칭 격자와 제품 정의. HA·SA 는 이 모듈만으로 격자를 만든다(절점 번호 일치 보장).
좌표: x∈[−L/2, L/2] (x<0 = GPU 측, PHY 위치), y∈[0, L/2] (y=0 대칭면), z: 0=하면(bump 측) → 상면.
절점 번호 = 1 + i + nx·(j + ny·k),  요소 번호 = 1 + i + (nx−1)·(j + (ny−1)·k)  (i:x, j:y, k:z)."""
import numpy as np, json
import stack as S
CAL_T0B = json.load(open("out2/calib3.json"))["t0b"]          # 272 °C (HBM3E-12H 실측 25/230 °C 보정)
# PHY: 공개자료(GUC/TSMC 발표 인용) HBM3E 11 mm²·6 W, HBM4 15 mm²·9 W. 위치 = GPU 측 가장자리 띠, 길이 9 mm, inset 0.25 mm
PRODUCTS = {
    "hbm4_8h":   dict(case=dict(gen="hbm4", nh=8, set_="design"), phy_area=15.0, phy_W=9.0),
    "hbm3e_12h": dict(case=dict(gen="hbm3e", nh=12, set_="micron"), phy_area=11.0, phy_W=6.0),
}
PHY_LEN, PHY_INSET = 9.0, 0.25
BC = dict(h_top=7000., h_bot=4000., T_ref=45.)               # W/m²K, °C (상면 TIM+cold plate / 하면 μbump→interposer)
H_IN = 0.192
def case(prod):
    p = PRODUCTS[prod]["case"]; return S.case(p["gen"], p["nh"], p["set_"], soft=True, t0b=CAL_T0B)
def phy_box(prod):
    hl = S.L_LOGIC/2; w = PRODUCTS[prod]["phy_area"]/PHY_LEN
    return (-hl+PHY_INSET, -hl+PHY_INSET+w, -PHY_LEN/2, PHY_LEN/2)           # x0,x1,y0,y1 [mm]
def _axis(brk, h):
    brk = np.unique(np.round(brk, 6)); p = [brk[0]]
    for a, b in zip(brk[:-1], brk[1:]): p += list(np.linspace(a, b, max(1, int(np.ceil((b-a)/h-1e-9)))+1)[1:])
    return np.round(np.array(p), 6)
def grid(prod):
    """returns dict(X,Y,Z, kind[nx-1,ny-1,nz-1], lname, phy(mask, base Si 전면 요소층), c=case, phy_box)"""
    c = case(prod); L = S.layers(c); hd, hl = S.L_DRAM/2, S.L_LOGIC/2; px0, px1, py0, py1 = phy_box(prod)
    X = _axis([-hl, -hd, hd, hl, px0, px1, 0], H_IN); Y = _axis([0, hd, hl, py1], H_IN)
    Z = [0.0]
    for (n, k, z0, z1, h) in L:
        if k == "emc": continue
        nzl = 6 if k == "si_top" else (2 if n == "Base_Si" else 1); Z += list(np.linspace(z0, z1, nzl+1)[1:])
    Z = np.round(np.array(Z), 7)
    xc, yc, zc = (X[:-1]+X[1:])/2, (Y[:-1]+Y[1:])/2, (Z[:-1]+Z[1:])/2
    XC, YC, ZC = np.meshgrid(xc, yc, zc, indexing="ij"); kind = np.full(XC.shape, "", "<U10"); lname = np.full(XC.shape, "", "<U16")
    for (n, k, z0, z1, h) in sorted(L, key=lambda l: l[1] == "emc"):
        m = (abs(XC) < h) & (YC < h) & (ZC > z0) & (ZC < z1) & (kind == ""); kind[m] = k; lname[m] = n
    assert (kind != "").all()
    zb0 = [l for l in L if l[0] == "Base_Si"][0][2]; kphy = int(np.argmin(abs(Z-zb0)))
    phy = (XC > px0) & (XC < px1) & (YC < py1) & (np.arange(len(Z)-1)[None, None, :] == kphy)
    return dict(X=X, Y=Y, Z=Z, kind=kind, lname=lname, phy=phy, c=c, phy_box=(px0, px1, py0, py1))
def nodes_elems(g):
    """(node ids, xyz[N,3], elem ids, conn[E,8]) — CalculiX 순서"""
    X, Y, Z = g["X"], g["Y"], g["Z"]; nx, ny, nz = len(X), len(Y), len(Z); nid = lambda i, j, k: 1 + i + nx*(j + ny*k)
    I, J, K = np.meshgrid(range(nx), range(ny), range(nz), indexing="ij")
    ids = nid(I, J, K).ravel(order="F"); xyz = np.stack([X[I], Y[J], Z[K]], -1).reshape(-1, 3, order="F")
    I, J, K = [a.ravel(order="F") for a in np.meshgrid(range(nx-1), range(ny-1), range(nz-1), indexing="ij")]
    conn = np.stack([nid(I, J, K), nid(I+1, J, K), nid(I+1, J+1, K), nid(I, J+1, K), nid(I, J, K+1), nid(I+1, J, K+1), nid(I+1, J+1, K+1), nid(I, J+1, K+1)], 1)
    eids = np.arange(1, (nx-1)*(ny-1)*(nz-1)+1)
    return ids, xyz, eids, conn
if __name__ == "__main__":
    for p in PRODUCTS:
        g = grid(p); X, Y, Z = g["X"], g["Y"], g["Z"]; vol = np.einsum("i,j,k->ijk", np.diff(X), np.diff(Y), np.diff(Z))
        print(p, f"grid {len(X)}x{len(Y)}x{len(Z)} nodes {len(X)*len(Y)*len(Z):,} elems {g['kind'].size:,}", "PHY box", np.round(g["phy_box"], 3),
              f"PHY area(half×2) {2*(np.diff(X)[:,None]*np.diff(Y)[None,:])[g['phy'].any(axis=2)].sum():.2f} mm²", f"top Si {S.top_si(g['c'])*1e3:.1f} μm")
