"""제품 간 DOE 효과 비교 (HBM4-8H vs HBM3E-12H)."""
import json, numpy as np, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
plt.rcParams.update({"font.family": "NanumGothic", "axes.unicode_minus": False, "font.size": 9,
                     "axes.spines.top": False, "axes.spines.right": False, "axes.grid": True, "grid.alpha": .25})
P = {"HBM4-8H (775 μm)": "out2/doe/summary.json", "HBM3E-12H (720 μm)": "out2/doe_hbm3e_12h/summary.json"}
S = {k: json.load(open(v)) for k, v in P.items()}
RESP = {"w25": "warp 25°C [μm]", "w230": "warp 230°C [μm]", "si_s1_25": "Si σ1 max 25°C [MPa]",
        "gap_peel_25": "gap peel σzz 25°C [MPa]", "gap_shear_25": "gap τ max 25°C [MPa]"}
TERMS = ["A", "C", "D", "E", "AC"]; COL = ["#2a78d6", "#eb6834"]
fig, ax = plt.subplots(1, len(RESP), figsize=(17, 3.8))
md = ["| 응답 | 제품 | 평균 | " + " | ".join(TERMS) + " |", "|---|---|---|" + "---|"*len(TERMS)]
for a, (q, lab) in zip(ax, RESP.items()):
    x = np.arange(len(TERMS)); w = .38
    for i, (pn, s) in enumerate(S.items()):
        e = [s[q]["eff"][t] for t in TERMS]
        a.bar(x+(i-.5)*w, e, w*.92, color=COL[i], label=pn)
        md.append(f"| {lab} | {pn} | {s[q]['mean']:.2f} | " + " | ".join(f"{v:+.3f}" for v in e) + " |")
    a.axhline(0, color="#888", lw=.8); a.set_xticks(x); a.set_xticklabels(TERMS); a.set_title(lab, fontsize=10)
    a.set_ylabel("효과 (+수준 − −수준)".replace("−", "-"))
ax[0].legend(frameon=False, fontsize=8, loc="lower left")
fig.suptitle("제품별 요인 효과 비교 — A: mid Si −3 μm 폭, C: BEOL α 7.6/9.9, D: NCF α1 30/50, E: NCF α2 70/110".replace("−", "-"), fontsize=11)
fig.tight_layout(); fig.savefig("figs/doe_compare_products.png", dpi=140)
open("out2/doe_compare.md", "w").write("\n".join(md)+"\n"); print("\n".join(md))
