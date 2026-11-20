"""후처리: 열/warpage/응력. usage: python3 post.py <variant>"""
import sys, json, numpy as np, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
from frd import read_frd, read_elprint
import params as P
V = sys.argv[1]; O = "out"; FIG = "figs"; import os; os.makedirs(FIG, exist_ok=True)
plt.rcParams.update({"font.family": "NanumGothic", "axes.unicode_minus": False, "font.size": 9, "axes.spines.top": False, "axes.spines.right": False, "axes.grid": True, "grid.alpha": .25})
m = np.load(f"{O}/mesh_{V}.npz"); X, Y, Z, mat, lname = m["X"], m["Y"], m["Z"], m["mat"], m["lname"]
nx, ny, nz = len(X), len(Y), len(Z); ne = (nx-1)*(ny-1)*(nz-1)
Tth = read_frd(f"{O}/thermal_{V}.frd")[-1]["NDTEMP"][1][:, 0].reshape(nz, ny, nx)   # [k,j,i]
steps = read_frd(f"{O}/mech_{V}.frd"); S = read_elprint(f"{O}/mech_{V}.dat")
labels = [f"{t}°C" for t in P.SWEEP] + ["operating"]
assert len(steps) == len(labels) == len(S), (len(steps), len(S))
lname_f = lname.ravel(order="F"); mat_f = mat.ravel(order="F")
layers = list(dict.fromkeys([l for l in lname_f if l != ""]))
zc_layer = {l: Z[:-1][(lname == l).any(axis=(0, 1))].mean() for l in layers}
layers = sorted(layers, key=lambda l: zc_layer[l])
R = dict(variant=V, thermal={}, warpage={}, stress={})

# ---------------- thermal ----------------
Tn = Tth.transpose(2, 1, 0)                     # [i,j,k]
Te = sum(Tn[a:nx-1+a, b:ny-1+b, c:nz-1+c] for a in (0, 1) for b in (0, 1) for c in (0, 1))/8
for l in layers:
    msk = lname == l; R["thermal"][l] = dict(Tmax=float(Te[msk].max()), Tavg=float(Te[msk].mean()))
R["thermal"]["Tmax"] = float(Tth.max()); R["thermal"]["Tmin"] = float(Tth.min())
fig = plt.figure(figsize=(12, 7.5)); gs = fig.add_gridspec(2, 3, height_ratios=[1, 1])
kb = int(np.argmin(abs(Z-P.T_BASE))); kt = nz-1
for c, (k, ttl) in enumerate([(kb, f"Base die 상면 (z={Z[kb]*1e3:.0f} μm)"), (kt, f"Package 상면 (z={Z[kt]*1e3:.0f} μm)")]):
    ax = fig.add_subplot(gs[0, c]); im = ax.pcolormesh(X, Y, Tth[k], cmap="inferno", shading="gouraud")
    ax.set_aspect("equal"); ax.set_title(ttl); ax.set_xlabel("x [mm]"); ax.set_ylabel("y [mm]"); fig.colorbar(im, ax=ax, label="T [°C]")
stk = [l for l in layers if "EMC" not in l]
ax = fig.add_subplot(gs[0, 2]); zl = [zc_layer[l]*1e3 for l in stk]
ax.plot([R["thermal"][l]["Tmax"] for l in stk], zl, "-o", ms=3, color="#e34948", label="Tmax")
ax.plot([R["thermal"][l]["Tavg"] for l in stk], zl, "-o", ms=3, color="#2a78d6", label="Tavg")
ax.set_xlabel("T [°C]"); ax.set_ylabel("z [μm]"); ax.legend(frameon=False); ax.set_title("층별 온도 (bond 포함)")
ax = fig.add_subplot(gs[1, :]); jm = int(np.argmin(abs(Y-6.4)))
im = ax.pcolormesh(X, Z*1e3, Tth[:, jm, :], cmap="inferno", shading="gouraud"); ax.set_xlabel("x [mm]"); ax.set_ylabel("z [μm]")
ax.set_title(f"단면 y={Y[jm]:.2f} mm (TSV band 중앙), x=0 측이 PHY/GPU 방향"); fig.colorbar(im, ax=ax, label="T [°C]")
for l in layers:
    if l.startswith("Core") or l == "Base_Die": ax.axhline(min(Z[:-1][(lname == l).any(axis=(0, 1))])*1e3, color="w", lw=.3)
fig.suptitle(f"HBM4-8H [{V}] 정상상태 열해석: Q=32 W, Tmax={Tth.max():.1f}°C", fontsize=12); fig.tight_layout()
fig.savefig(f"{FIG}/thermal_{V}.png", dpi=150); plt.close(fig)

# ---------------- warpage (bottom surface, LSQ plane 제거) ----------------
XX, YY = np.meshgrid(X, Y); A = np.c_[XX.ravel(), YY.ravel(), np.ones(XX.size)]
W = []
for s in steps:
    w = s["DISP"][1][:nx*ny, 2].reshape(ny, nx)*1e3            # μm
    w = w - (A @ np.linalg.lstsq(A, w.ravel(), rcond=None)[0]).reshape(ny, nx); W.append(w)
for lab, w in zip(labels, W):
    sign = np.sign(w[[0, 0, -1, -1], [0, -1, 0, -1]].mean() - w[ny//2, nx//2])
    R["warpage"][lab] = dict(coplanarity_um=float(w.max()-w.min()), signed_um=float(sign*(w.max()-w.min())))
sel = [0, len(P.SWEEP)-1, len(labels)-1]; lim = max(abs(W[i]).max() for i in sel)
fig = plt.figure(figsize=(15, 4.8))
for c, i in enumerate(sel):
    ax = fig.add_subplot(1, 3, c+1, projection="3d")
    ax.plot_surface(XX, YY, W[i], cmap="RdBu_r", vmin=-lim, vmax=lim, rstride=1, cstride=1, linewidth=0, antialiased=True)
    ax.set_zlim(-lim*1.2, lim*1.2); ax.set_xlabel("x [mm]"); ax.set_ylabel("y [mm]"); ax.set_zlabel("w [μm]")
    r = R["warpage"][labels[i]]; shape = "smile(오목)" if r["signed_um"] > 0 else "crying(볼록)"
    ax.set_title(f"{labels[i]}: {r['signed_um']:+.2f} μm  {shape}"); ax.view_init(28, -55); ax.set_box_aspect((1, 1.16, .55))
fig.suptitle(f"[{V}] 하면 warpage (평면 보정, 응력 0 온도 {P.T_STRESSFREE:.0f}°C, +:smile)", fontsize=12); fig.tight_layout()
fig.savefig(f"{FIG}/warpage3d_{V}.png", dpi=150); plt.close(fig)

# ---------------- stress (integration-point → element) ----------------
def vm(s): return np.sqrt(.5*((s[:, 0]-s[:, 1])**2+(s[:, 1]-s[:, 2])**2+(s[:, 2]-s[:, 0])**2)+3*(s[:, 3]**2+s[:, 4]**2+s[:, 5]**2))
def p1(s):
    T = np.zeros((len(s), 3, 3)); T[:, 0, 0], T[:, 1, 1], T[:, 2, 2] = s[:, 0], s[:, 1], s[:, 2]
    T[:, 0, 1] = T[:, 1, 0] = s[:, 3]; T[:, 0, 2] = T[:, 2, 0] = s[:, 4]; T[:, 1, 2] = T[:, 2, 1] = s[:, 5]
    return np.linalg.eigvalsh(T)[:, -1]
EL = []
for lab, a in zip(labels, S):
    se = np.zeros((ne, 6)); np.add.at(se, a[:, 0].astype(int)-1, a[:, 2:]); se /= 8
    EL.append(se); d = {}
    for l in layers:
        e = lname_f == l; s = se[e]
        r = dict(vm_max=float(vm(s).max()))
        if "Bond" in l: r.update(peel_max=float(s[:, 2].max()), peel_min=float(s[:, 2].min()), shear_max=float(np.hypot(s[:, 4], s[:, 5]).max()))
        else: r.update(s1_max=float(p1(s).max()))
        d[l] = r
    R["stress"][lab] = d
np.save(f"{O}/elstress_{V}.npy", np.stack([EL[i] for i in sel]).astype(np.float32))
fig, axs = plt.subplots(1, 3, figsize=(15, 5))
cols = ["#2a78d6", "#eb6834", "#1baf7a"]; yy = np.arange(len(layers))
for c, i in enumerate(sel):
    axs[0].plot([R["stress"][labels[i]][l]["vm_max"] for l in layers], yy, "-o", ms=3, color=cols[c], label=labels[i])
    bl = [l for l in layers if "Bond" in l]; yb = [layers.index(l) for l in bl]
    axs[1].plot([R["stress"][labels[i]][l]["peel_max"] for l in bl], yb, "-o", ms=3, color=cols[c], label=labels[i])
    axs[1].plot([R["stress"][labels[i]][l]["shear_max"] for l in bl], yb, "--s", ms=3, color=cols[c])
for ax in axs[:2]: ax.set_yticks(yy); ax.set_yticklabels(layers, fontsize=7); ax.legend(frameon=False, fontsize=8)
axs[0].set_xlabel("von Mises max [MPa] (element 평균)"); axs[0].set_title("층별 최대 von Mises")
axs[1].set_xlabel("[MPa]"); axs[1].set_title("Bond층 peel σzz max (실선) / shear τ max (점선)")
i0 = 0; se = EL[i0]; v = vm(se).reshape(nx-1, ny-1, nz-1, order="F")
lmax = max([l for l in layers if "Die" in l], key=lambda l: R["stress"][labels[i0]][l]["vm_max"])
ks = np.where((lname == lmax).any(axis=(0, 1)))[0]; k = ks[0] if lmax != "Core_Die_8" else ks[-1]
im = axs[2].pcolormesh(X, Y, v[:, :, k].T, cmap="magma"); axs[2].set_aspect("equal"); fig.colorbar(im, ax=axs[2], label="von Mises [MPa]")
axs[2].set_title(f"{labels[i0]}: {lmax} (z={Z[k]*1e3:.0f}–{Z[k+1]*1e3:.0f} μm) von Mises"); axs[2].set_xlabel("x [mm]"); axs[2].set_ylabel("y [mm]"); axs[2].grid(False)
fig.suptitle(f"[{V}] 열-구조 응력 (C3D8I, 적분점→요소 평균)", fontsize=12); fig.tight_layout()
fig.savefig(f"{FIG}/stress_{V}.png", dpi=150); plt.close(fig)
json.dump(R, open(f"{O}/summary_{V}.json", "w"), indent=1, ensure_ascii=False)
print(json.dumps({k: R["warpage"][k] for k in labels}, ensure_ascii=False))
