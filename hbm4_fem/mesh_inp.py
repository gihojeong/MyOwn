"""Blender export(JSON) → 구조격자 hex mesh → CalculiX 입력 (열: DC3D8, 구조: C3D8I).
usage: python3 mesh_inp.py <variant> <outdir> [h_inplane]"""
import sys, json, numpy as np
import params as P
V, OUT = sys.argv[1], sys.argv[2]; HMAX = float(sys.argv[3]) if len(sys.argv) > 3 else 0.25
G = json.load(open(f"{OUT}/geometry_{V}.json")); r6 = lambda a: np.round(a, 6)

def axis(brk, hmax):
    brk = np.unique(r6(np.array(brk))); pts = [brk[0]]
    for a, b in zip(brk[:-1], brk[1:]):
        n = max(1, int(np.ceil((b-a)/hmax - 1e-9))); pts += list(np.linspace(a, b, n+1)[1:])
    return r6(np.array(pts))
Ls = G["layers"]
bx = [v for l in Ls for v in l["x"]] + [P.TSV_BAND[0], P.TSV_BAND[1], P.PHY[0], P.PHY[1], P.FOOT[0]/2]
by = [v for l in Ls for v in l["y"]] + [P.TSV_BAND[2], P.TSV_BAND[3], P.PHY[2], P.PHY[3], P.FOOT[1]/2]
X, Y = axis(bx, HMAX), axis(by, HMAX)
zb = sorted(set(r6(np.array([v for l in Ls for v in l["z"]]))))
Z = [zb[0]]
for a, b in zip(zb[:-1], zb[1:]):
    n = max(1, int(np.ceil((b-a)/0.035 - 1e-9))) if b-a > 0.02 else 1
    Z += list(np.linspace(a, b, n+1)[1:])
Z = r6(np.array(Z)); nx, ny, nz = len(X), len(Y), len(Z)
nid = lambda i, j, k: 1 + i + nx*(j + ny*k)

# element centroids & material assignment (Blender layer bounding boxes)
xc, yc, zc = (X[:-1]+X[1:])/2, (Y[:-1]+Y[1:])/2, (Z[:-1]+Z[1:])/2
XC, YC, ZC = np.meshgrid(xc, yc, zc, indexing="ij")
kind = np.full(XC.shape, "", dtype=object); lname = np.full(XC.shape, "", dtype=object)
for l in sorted(Ls, key=lambda l: l["kind"] == "emc_ring"):        # ring은 fallback
    m = (XC > l["x"][0]) & (XC < l["x"][1]) & (YC > l["y"][0]) & (YC < l["y"][1]) & (ZC > l["z"][0]) & (ZC < l["z"][1]) & (kind == "")
    kind[m] = l["kind"]; lname[m] = l["name"]
assert (kind != "").all(), "unassigned elements"
tx0, tx1, ty0, ty1 = P.TSV_BAND
band = (XC > tx0) & (XC < tx1) & (YC > ty0) & (YC < ty1)
mat = np.where(np.isin(kind, ["base", "core"]), np.where(band, "SI_TSV", "SI"),
      np.where(kind == "bond", np.where(band, "BOND_TSV", "BOND_DUM"), "EMC"))
vol = np.einsum("i,j,k->ijk", np.diff(X), np.diff(Y), np.diff(Z))

# 발열 (W → mW, 체적 분포)
q = np.zeros(XC.shape)
px0, px1, py0, py1 = P.PHY
phy = (XC > px0) & (XC < px1) & (YC > py0) & (YC < py1)
def put(mask, W): q[mask] += W*1e3/vol[mask].sum()
b = lname == "Base_Die"
put(b & phy, P.P_BASE["phy"]); put(b & band & ~phy, P.P_BASE["tsv"]); put(b & ~band & ~phy, P.P_BASE["rest"])
for k in range(1, 9):
    c = lname == f"Core_Die_{k}"; put(c & band, P.P_CORE["tsv"]); put(c & ~band, P.P_CORE["array"])
Qtot = (q*vol).sum()/1e3

# ---------------- writers ----------------
eid = np.arange(1, XC.size+1).reshape(XC.shape, order="F")
def nodes_txt():
    I, J, K = np.meshgrid(range(nx), range(ny), range(nz), indexing="ij")
    ids = (1 + I + nx*(J + ny*K)).ravel(order="F")
    xyz = np.stack([X[I], Y[J], Z[K]], -1).reshape(-1, 3, order="F")
    return "*NODE, NSET=NALL\n" + "\n".join(f"{n},{a:.6f},{b_:.6f},{c:.6f}" for n, (a, b_, c) in zip(ids, xyz))
def elems_txt(etype):
    I, J, K = np.meshgrid(range(nx-1), range(ny-1), range(nz-1), indexing="ij")
    I, J, K = [a.ravel(order="F") for a in (I, J, K)]
    conn = np.stack([nid(I, J, K), nid(I+1, J, K), nid(I+1, J+1, K), nid(I, J+1, K),
                     nid(I, J, K+1), nid(I+1, J, K+1), nid(I+1, J+1, K+1), nid(I, J+1, K+1)], 1)
    s = f"*ELEMENT, TYPE={etype}, ELSET=EALL\n" + "\n".join(f"{e}," + ",".join(map(str, c)) for e, c in zip(eid.ravel(order='F'), conn))
    for m in np.unique(mat):
        ids = eid[mat == m]; s += f"\n*ELSET, ELSET=E_{m}\n" + "\n".join(",".join(map(str, ids[i:i+16])) for i in range(0, len(ids), 16))
    return s
def mats_txt():
    T = P.TT; M = P.material_table(P.VARIANTS[V]["bond"]); s = ""
    dens = {"SI": (2.33e-9, 7.0e8), "SI_TSV": (2.5e-9, 6.8e8), "EMC": (2.0e-9, 9.0e8), "BOND_TSV": (3.4e-9, 7.5e8), "BOND_DUM": (2.3e-9, 8.5e8)}
    for m in np.unique(mat):
        d = M[m]; a = P.secant_alpha(d["a"], T)
        s += f"*MATERIAL, NAME={m}\n*ELASTIC\n" + "\n".join(f"{E:.1f},{d['nu']:.3f},{t:.1f}" for E, t in zip(d["E"], T))
        s += f"\n*EXPANSION, ZERO={P.T_STRESSFREE}\n" + "\n".join(f"{x:.4e},{t:.1f}" for x, t in zip(a, T))
        s += "\n*CONDUCTIVITY, TYPE=ORTHO\n" + "\n".join(f"{k:.4f},{k:.4f},{kz:.4f},{t:.1f}" for k, kz, t in zip(d["k"], d["kz"], T))
        s += f"\n*DENSITY\n{dens[m][0]}\n*SPECIFIC HEAT\n{dens[m][1]}\n*SOLID SECTION, ELSET=E_{m}, MATERIAL={m}\n"
    return s

hdr = f"** HBM4-8H {V}: {nx}x{ny}x{nz} nodes, {(nx-1)*(ny-1)*(nz-1)} elements, Q={Qtot:.2f} W\n"
NODES = nodes_txt()
# --- thermal ---
bot = eid[:, :, 0].ravel(); top = eid[:, :, -1].ravel(); qq = q.ravel(order="F"); E = eid.ravel(order="F")
with open(f"{OUT}/thermal_{V}.inp", "w") as f:
    f.write(hdr + NODES + "\n" + elems_txt("DC3D8") + "\n" + mats_txt())
    f.write("*INITIAL CONDITIONS, TYPE=TEMPERATURE\nNALL, 60.0\n*STEP\n*HEAT TRANSFER, STEADY STATE\n1.0, 1.0\n*DFLUX\n")
    f.write("\n".join(f"{e},BF,{v:.6e}" for e, v in zip(E, qq) if v > 0))
    f.write("\n*FILM\n" + "\n".join(f"{e},F2,{P.T_TOP},{P.H_TOP*1e-3:.4e}" for e in top))
    f.write("\n" + "\n".join(f"{e},F1,{P.T_BOT},{P.H_BOT*1e-3:.4e}" for e in bot))
    f.write("\n*NODE FILE\nNT\n*EL FILE\nHFL\n*END STEP\n")
# --- mechanical (thermal field는 run 단계에서 include) ---
ic, jc = int(np.argmin(abs(X-P.FOOT[0]/2))), int(np.argmin(abs(Y-P.FOOT[1]/2)))
with open(f"{OUT}/mech_{V}.inp", "w") as f:
    f.write(hdr + NODES + "\n" + elems_txt("C3D8I") + "\n" + mats_txt())
    f.write(f"*BOUNDARY\n{nid(ic,jc,0)},1,3\n{nid(nx-1,jc,0)},2,3\n{nid(ic,ny-1,0)},3,3\n")
    f.write(f"*INITIAL CONDITIONS, TYPE=TEMPERATURE\nNALL, {P.T_STRESSFREE}\n")
    for T in P.SWEEP:
        f.write(f"*STEP\n*STATIC\n*TEMPERATURE\nNALL, {T}\n*NODE FILE\nU, NT\n*EL FILE\nS\n")
        if T in (25, 260): f.write("*EL PRINT, ELSET=EALL\nS\n")
        f.write("*END STEP\n")
    f.write(f"*STEP\n*STATIC\n*TEMPERATURE\n*INCLUDE, INPUT=optemp_{V}.inc\n*NODE FILE\nU, NT\n*EL FILE\nS\n*EL PRINT, ELSET=EALL\nS\n*END STEP\n")
np.savez(f"{OUT}/mesh_{V}.npz", X=X, Y=Y, Z=Z, mat=mat, lname=lname.astype(str), q=q, vol=vol)
print(hdr.strip(), "| materials:", {m: int((mat == m).sum()) for m in np.unique(mat)})
