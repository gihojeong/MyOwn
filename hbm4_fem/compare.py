"""변형(variant) 비교: warpage-온도 곡선 + 핵심 지표 표."""
import json, glob, numpy as np, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
import params as P
plt.rcParams.update({"font.family": "NanumGothic", "axes.unicode_minus": False, "font.size": 10,
                     "axes.spines.top": False, "axes.spines.right": False, "axes.grid": True, "grid.alpha": .25})
COL = {"A_MRMUF": "#2a78d6", "B_TCNCF": "#eb6834", "C_MRMUF_CAP": "#1baf7a", "D_MID47": "#eda100"}
NAME = {"A_MRMUF": "A: MR-MUF (top Si 노출)", "B_TCNCF": "B: TC-NCF", "C_MRMUF_CAP": "C: MR-MUF + EMC cap 90μm", "D_MID47": "D: MR-MUF, mid 47μm (top 211μm)"}
Rs = {json.load(open(f))["variant"]: json.load(open(f)) for f in sorted(glob.glob("out/summary_*.json"))}
fig, axs = plt.subplots(1, 2, figsize=(13, 4.8))
for v, R in Rs.items():
    w = [R["warpage"][f"{t}°C"]["bow_um"] for t in P.SWEEP]
    axs[0].plot(P.SWEEP, w, "-o", ms=5, lw=2, color=COL[v], label=NAME[v])
    axs[0].annotate(f"{w[0]:+.2f}", (P.SWEEP[0], w[0]), xytext=(-34, 0), textcoords="offset points", fontsize=8, va="center")
    lay = [l for l in R["stress"]["25°C"] if "Bond" in l]
    axs[1].plot([R["stress"]["25°C"][l]["vm_max"] for l in lay], range(1, 9), "-o", ms=4, color=COL[v], label=NAME[v])
axs[0].axhline(0, color="#888", lw=.8); axs[0].axvline(P.T_STRESSFREE, color="#888", lw=.8, ls=":")
axs[0].text(P.T_STRESSFREE+2, axs[0].get_ylim()[1]*0.9, "stress-free 175°C", fontsize=8, color="#555")
axs[0].set_xlabel("온도 [°C]"); axs[0].set_ylabel("하면 bow [μm] (2차 곡면 피팅, + smile / - crying)"); axs[0].legend(frameon=False, fontsize=9)
axs[0].set_title("온도별 전역 warpage (bow)")
axs[1].set_yticks(range(1, 9)); axs[1].set_yticklabels([f"Bond_{i}" for i in range(1, 9)])
axs[1].set_xlabel("von Mises max @25°C [MPa]"); axs[1].set_title("Bond층 응력 (상온)"); axs[1].legend(frameon=False, fontsize=9)
fig.tight_layout(); fig.savefig("figs/compare_variants.png", dpi=150)
rows = []
for v, R in Rs.items():
    s25, op = R["stress"]["25°C"], R["stress"]["operating"]
    si = lambda d, key: max(d[l][key] for l in d if "Die" in l)
    bd = lambda d, key: max(d[l][key] for l in d if "Bond" in l)
    rows.append([v, R["thermal"]["Tmax"], R["warpage"]["25°C"]["bow_um"], R["warpage"]["260°C"]["bow_um"],
                 R["warpage"]["operating"]["bow_um"], si(s25, "vm_max"), si(s25, "s1_max"), bd(s25, "peel_max"), bd(s25, "shear_max"),
                 max(s25[l]["s1_max"] for l in s25 if "EMC" in l)])
hdr = "| Variant | Tmax op [°C] | Bow 25°C [μm] | Bow 260°C [μm] | Bow op [μm] | Si σvm max 25°C [MPa] | Si σ1 max 25°C | Bond peel max 25°C | Bond τ max 25°C | EMC σ1 max 25°C |"
md = hdr + "\n|" + "---|"*10 + "\n" + "\n".join("| " + r[0] + " | " + " | ".join(f"{x:+.2f}" if 2 <= i <= 4 else f"{x:.1f}" for i, x in enumerate(r[1:], 1)) + " |" for r in rows)
open("figs/summary_table.md", "w").write(md + "\n"); print(md)
