"""LIT 위상-주파수 그래프 (HBM3E-12H, Core 1~12, 선형 주파수축, 위상 지연 +)."""
import json, numpy as np, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
plt.rcParams.update({"font.family": "NanumGothic", "axes.unicode_minus": False, "font.size": 10,
                     "axes.spines.top": False, "axes.spines.right": False})
R = json.load(open("out3/thermal/hbm3e_12h/lit_h0.3.json")); f = np.array(R["freq"])
cmap = plt.get_cmap("viridis"); fig, ax = plt.subplots(figsize=(11, 6.5))
for k in range(1, 13):
    ph = np.degrees(np.unwrap(np.radians(np.array(R["phase_deg"][str(k)])))); c = cmap((k-1)/11*0.9)
    ax.plot(f, ph, "-o", ms=3.5, lw=2, color=c, label=f"Core {k}")
    ax.text(f[-1]+1.2, ph[-1], f"C{k}", va="center", fontsize=8, color="#333")
ax.set_xlabel("Lock-in 주파수 f [Hz]"); ax.set_ylabel("위상 지연 [deg] (+ = 지연)")
ax.set_xlim(0, f[-1]+8); ax.grid(alpha=.3)
ax.legend(ncol=2, frameon=False, fontsize=8, loc="upper left", title="열원 위치 (Core 1 = base 위 첫 die)")
ax.set_title("HBM3E-12H 3D Lock-in thermography: 상면(열원 직상) 위상 지연 vs 주파수\n열원 = Core k 소자층(BEOL) 중앙 점 발열(0.3×0.3 mm 요소), 열물성 65 °C, 상·하면 HA 사용환경 h")
fig.tight_layout(); fig.savefig("figs/lit_phase_hbm3e_12h.png", dpi=150); print("ok")
