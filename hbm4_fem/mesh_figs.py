"""격자 시각화: (1) Blender 3D 1/4 모델(재료색+요소 경계선), (2) 2D 평면/단면 격자도. usage: python3 mesh_figs.py <mesh_name>"""
import sys, numpy as np, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Patch
NAME = sys.argv[1]; m = np.load(f"out2/{NAME}_mesh.npz"); X, Y, Z, K = m["X"], m["Y"], m["Z"], m["kind"].astype("<U10")
K[m["lname"] == "Base_Si"] = "si_base"   # 표시용 (구 메시 호환)
COL = {"si": "#7d8fb3", "si_top": "#5a6d96", "si_base": "#46557a", "beol": "#d08a3c", "gap": "#3fa66a", "emc": "#2b2b2e"}
LAB = {"si": "mid core Si", "si_top": "top core Si", "si_base": "base Si", "beol": "BEOL", "gap": "NCF+bump gap", "emc": "EMC 링"}
plt.rcParams.update({"font.family": "NanumGothic", "axes.unicode_minus": False, "font.size": 9})
nx, ny, nz = len(X)-1, len(Y)-1, len(Z)-1
fig = plt.figure(figsize=(16, 7.5)); gs = fig.add_gridspec(2, 3, width_ratios=[1, 1.25, 1.25])
# (a) 평면 격자 (top 면)
ax = fig.add_subplot(gs[:, 0]); kt = K[:, :, -1]
for i in range(nx):
    for j in range(ny): ax.add_patch(Rectangle((X[i], Y[j]), X[i+1]-X[i], Y[j+1]-Y[j], fc=COL[kt[i, j]], ec="w", lw=.4))
ax.set_xlim(0, X[-1]); ax.set_ylim(0, Y[-1]); ax.set_aspect("equal"); ax.set_xlabel("x [mm] (중심=0, 대칭면)"); ax.set_ylabel("y [mm]")
ax.set_title(f"평면 격자 (상면) {nx}×{ny}\nDRAM 0–5.0 mm: 26분할(0.192), EMC 링 0.75 mm: 4분할(0.188)")
# (b) x-z 단면 전체 (y=0 대칭면), z 실척 μm
def section(ax, x0, x1, z0, z1, title):
    for i in range(nx):
        if X[i+1] < x0 or X[i] > x1: continue
        for k in range(nz):
            if Z[k+1]*1e3 < z0 or Z[k]*1e3 > z1: continue
            ax.add_patch(Rectangle((X[i], Z[k]*1e3), X[i+1]-X[i], (Z[k+1]-Z[k])*1e3, fc=COL[K[i, 0, k]], ec="w", lw=.35))
    ax.set_xlim(x0, x1); ax.set_ylim(z0, z1); ax.set_xlabel("x [mm]"); ax.set_ylabel("z [μm]"); ax.set_title(title)
section(fig.add_subplot(gs[0, 1:]), 0, X[-1], 0, Z[-1]*1e3, f"x-z 단면 (y=0) 전체 — z 방향 {nz}층, 종축 μm (가로 대비 약 ×8 과장)")
ax2 = fig.add_subplot(gs[1, 1]); section(ax2, 4.2, X[-1], 0, 200, "확대: DRAM 모서리·EMC 링, 하부 0–200 μm")
ax3 = fig.add_subplot(gs[1, 2]); section(ax3, 4.2, X[-1], Z[-1]*1e3-220, Z[-1]*1e3, "확대: 상부 (top die 6분할)")
for a in (ax2, ax3):
    for k in range(nz+1):
        z = Z[k]*1e3
        if a.get_ylim()[0] <= z <= a.get_ylim()[1]: a.text(X[-1]+.02, z, f"{z:.1f}", fontsize=6, va="center", color="#555")
fig.legend(handles=[Patch(fc=COL[k], label=LAB[k]) for k in COL], loc="lower center", ncol=5, frameon=False)
dz = np.diff(Z)*1e3
fig.suptitle(f"{NAME}: 1/4 대칭 C3D8I 구조격자 — 절점 {len(X)*len(Y)*len(Z):,} · 요소 {nx*ny*nz:,} · Δz {dz.min():.1f}–{dz.max():.1f} μm · 최대 종횡비 {np.diff(X).max()*1e3/dz.min():.0f}", fontsize=12)
fig.tight_layout(rect=(0, .04, 1, .96)); fig.savefig(f"figs/mesh_{NAME}_2d.png", dpi=150); print("2d ok")
