"""[PA 공통 인터페이스] 열(HA)·구조(SA) 해석이 공유하는 1/2 대칭 격자와 제품 정의. HA·SA 는 이 모듈만으로 격자를 만든다(절점 번호 일치 보장).
좌표: x∈[−L/2, L/2] (x<0 = GPU 측, PHY 위치), y∈[0, L/2] (y=0 대칭면), z: 0=하면(bump 측) → 상면.
절점 번호 = 1 + i + nx·(j + ny·k),  요소 번호 = 1 + i + (nx−1)·(j + (ny−1)·k)  (i:x, j:y, k:z)."""
import numpy as np, json
import stack as S
CAL_T0B = json.load(open("out2/calib4.json"))["t0b"]          # 245 °C (HBM3E-12H Micron두께, base die 10.93 mm, 실측 |w25| 7.6 μm 보정)
# PHY 열원 = PHY/μbump 필드 박스. edge_off: GPU 측 die 변에서 필드 시작까지, depth: 변에 수직 폭, length: 변 방향 길이(중앙 정렬) [mm]
#  HBM3E: TechInsights base die 사진(사용자 제공) 측정 — die 10.93×10.94 mm, 필드 8.2×2.9 mm (≈24 mm²), 변에서 1.8 mm 안쪽
#  전력: GUC/TSMC 인용 HBM3E PHY 6 W, HBM4 9 W.  HBM4 형상은 SA 조사 결과로 갱신 예정(현재 임시값)
PRODUCTS = {
    # HBM4: SA 조사(패키지 12.8×11 mm, SK hynix Hot Chips 2026) + 추정 — base 10.9(x)×12.7(y), core 10.1×11.9, 긴 변(y)이 GPU 대향,
    #        PHY 필드 ≈33 mm² (HBM3E 24 mm² × GUC 면적비 1.36), 폭 3.3 × 길이 10.0, 변에서 1.8 mm 안쪽; 전력 9 W (범위 5–10 W)
    "hbm4_8h":   dict(case=dict(gen="hbm4", nh=8, set_="design", L_logic=10.9, L_logic_y=12.7, L_dram=10.1, L_dram_y=11.9),
                      phy=dict(edge_off=1.8, depth=3.3, length=10.0), phy_W=9.0),
    "hbm3e_12h": dict(case=dict(gen="hbm3e", nh=12, set_="micron", L_logic=10.93, L_dram=10.0), phy=dict(edge_off=1.8, depth=2.9, length=8.2), phy_W=6.0),
}
BC = dict(h_top=7000., h_bot=4000., T_ref=45.)               # W/m²K, °C (상면 TIM+cold plate / 하면 μbump→interposer)
H_IN = 0.192
def case(prod):
    p = dict(PRODUCTS[prod]["case"]); g, n, st = p.pop("gen"), p.pop("nh"), p.pop("set_")
    return S.case(g, n, st, soft=True, t0b=CAL_T0B, **p)
def phy_box(prod):
    hl = S.Ls(case(prod))[0]/2; q = PRODUCTS[prod]["phy"]
    return (-hl+q["edge_off"], -hl+q["edge_off"]+q["depth"], -q["length"]/2, q["length"]/2)   # x0,x1,y0,y1 [mm]
def _axis(brk, h):
    brk = np.unique(np.round(brk, 6)); p = [brk[0]]
    for a, b in zip(brk[:-1], brk[1:]): p += list(np.linspace(a, b, max(1, int(np.ceil((b-a)/h-1e-9)))+1)[1:])
    return np.round(np.array(p), 6)
def grid(prod):
    """returns dict(X,Y,Z, kind[nx-1,ny-1,nz-1], lname, phy(mask, base Si 전면 요소층), c=case, phy_box)"""
    c = case(prod); L = S.layers(c); lx, ly, dx, dy = S.Lxy(c); px0, px1, py0, py1 = phy_box(prod)
    X = _axis([-lx/2, -dx/2, dx/2, lx/2, px0, px1, 0], H_IN); Y = _axis([0, dy/2, ly/2, py1], H_IN)
    Z = [0.0]
    for (n, k, z0, z1, h) in L:
        if k == "emc": continue
        nzl = 6 if k == "si_top" else (2 if n == "Base_Si" else 1); Z += list(np.linspace(z0, z1, nzl+1)[1:])
    Z = np.round(np.array(Z), 7)
    xc, yc, zc = (X[:-1]+X[1:])/2, (Y[:-1]+Y[1:])/2, (Z[:-1]+Z[1:])/2
    XC, YC, ZC = np.meshgrid(xc, yc, zc, indexing="ij"); kind = np.full(XC.shape, "", "<U10"); lname = np.full(XC.shape, "", "<U16")
    for (n, k, z0, z1, h) in sorted(L, key=lambda l: l[1] == "emc"):
        m = (abs(XC) < h) & (YC < S.half_y(c, h)) & (ZC > z0) & (ZC < z1) & (kind == ""); kind[m] = k; lname[m] = n
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
              f"phy_W {PRODUCTS[p]['phy_W']}", f"PHY area(half×2) {2*(np.diff(X)[:,None]*np.diff(Y)[None,:])[g['phy'].any(axis=2)].sum():.2f} mm²", f"top Si {S.top_si(g['c'])*1e3:.1f} μm")
