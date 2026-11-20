"""두 변형의 차이 비교 (동일 격자 topology 전제). usage: python3 diff_pair.py A_MRMUF D_MID47"""
import sys, json, numpy as np, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
from frd import read_frd
import params as P
plt.rcParams.update({"font.family": "NanumGothic", "axes.unicode_minus": False, "font.size": 10,
                     "axes.spines.top": False, "axes.spines.right": False, "axes.grid": True, "grid.alpha": .25})
a, b = sys.argv[1], sys.argv[2]; R = {v: json.load(open(f"out/summary_{v}.json")) for v in (a, b)}
def bottom_w(v, s):
    m = np.load(f"out/mesh_{v}.npz"); X, Y = m["X"], m["Y"]; nx, ny = len(X), len(Y)
    w = read_frd(f"out/mech_{v}.frd")[s]["DISP"][1][:nx*ny, 2].reshape(ny, nx)*1e3
    XX, YY = np.meshgrid(X, Y); A = np.c_[XX.ravel(), YY.ravel(), np.ones(XX.size)]
    return XX, YY, w - (A @ np.linalg.lstsq(A, w.ravel(), rcond=None)[0]).reshape(ny, nx)
XX, YY, wa = bottom_w(a, 0); _, _, wb = bottom_w(b, 0)
fig = plt.figure(figsize=(15, 4.8))
ax = fig.add_subplot(1, 3, 1)
for v, c in ((a, "#2a78d6"), (b, "#eda100")):
    ax.plot(P.SWEEP, [R[v]["warpage"][f"{t}°C"]["bow_um"] for t in P.SWEEP], "-o", ms=5, lw=2, color=c, label=v)
ax.axhline(0, color="#888", lw=.8); ax.set_xlabel("온도 [°C]"); ax.set_ylabel("bow [μm] (+ smile)"); ax.legend(frameon=False)
ax.set_title("온도별 bow")
d = wb - wa; lim = abs(d).max()
ax = fig.add_subplot(1, 3, 2, projection="3d")
ax.plot_surface(XX, YY, wb, cmap="RdBu_r", vmin=-abs(wb).max(), vmax=abs(wb).max(), linewidth=0)
ax.set_title(f"{b} 하면 w @25°C (bow {R[b]['warpage']['25°C']['bow_um']:+.2f} μm)"); ax.view_init(28, -55); ax.set_box_aspect((1, 1.16, .55))
ax.set_xlabel("x [mm]"); ax.set_ylabel("y [mm]"); ax.set_zlabel("w [μm]")
ax = fig.add_subplot(1, 3, 3, projection="3d")
ax.plot_surface(XX, YY, d, cmap="RdBu_r", vmin=-lim, vmax=lim, linewidth=0)
ax.set_title(f"Δw = {b} - {a} @25°C (max |Δw| {lim:.2f} μm)"); ax.view_init(28, -55); ax.set_box_aspect((1, 1.16, .55))
ax.set_xlabel("x [mm]"); ax.set_ylabel("y [mm]"); ax.set_zlabel("Δw [μm]")
fig.suptitle(f"{a} vs {b}: mid-die 50→47 μm, top die 190→211 μm (H = 720 μm 고정)", fontsize=12); fig.tight_layout()
fig.savefig(f"figs/diff_{a}_vs_{b}.png", dpi=150); print("ok")
