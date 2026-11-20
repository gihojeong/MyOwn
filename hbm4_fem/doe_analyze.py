"""DOE 분석: 효과·Lenth PSE·Pareto·반정규·주효과·교호작용·회귀·곡률 → figs/doe_*.png, out2/doe/report.md"""
import json, glob, itertools, numpy as np, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
from scipy import stats
import doe
plt.rcParams.update({"font.family": "NanumGothic", "axes.unicode_minus": False, "font.size": 9,
                     "axes.spines.top": False, "axes.spines.right": False, "axes.grid": True, "grid.alpha": .25})
K = doe.K; R = sorted([json.load(open(f)) for f in glob.glob(f"{doe.OUTD}/doe_*.json")], key=lambda r: r["run"])
F = [r for r in R if any(r["x"][k] != 0 for k in K)]; Cn = [r for r in R if all(r["x"][k] == 0 for k in K)]
X = np.array([[r["x"][k] for k in K] for r in F], float); N = len(F)
TERMS = [t for n in range(1, len(K)+1) for t in itertools.combinations(K, n)]
col = lambda t: np.prod(X[:, [K.index(k) for k in t]], axis=1)
RESP = {"w25": ("warp 25°C [μm]", "중앙−vertex, +Cry"), "w230": ("warp 230°C [μm]", "중앙−vertex, +Cry"),
        "si_s1_25": ("Si σ1 max 25°C [MPa]", "die crack"), "gap_peel_25": ("gap peel σzz max 25°C [MPa]", "NCF/bump 박리"),
        "gap_shear_25": ("gap τ max 25°C [MPa]", "계면 전단")}
FN = {k: f"{k}:{doe.FAC[k][0]}" for k in K}
BLUE, ORANGE, GRAY, RED = "#2a78d6", "#eb6834", "#8a8a85", "#e34948"
def lenth(e):
    a = np.abs(e); s0 = 1.5*np.median(a); pse = 1.5*np.median(a[a < 2.5*s0]); d = len(e)/3
    g = (1+0.95**(1/len(e)))/2
    return pse, stats.t.ppf(.975, d)*pse, stats.t.ppf(g, d)*pse
md = ["# HBM4-8H TCB DOE (2⁴ 완전요인 + 중심점)", "",
      f"기준: HBM4-8H 775 μm, S 설계두께, Tg 연화, T0b {doe.CAL['t0b']:.0f} °C, bump vf {doe.case_of(F[0]['x'])['vf']:.3f}, 1/4 대칭 C3D8I.", "",
      "| 요인 | − | 0 | + |", "|---|---|---|---|"]
for k in K:
    nm, key, lo, hi, sc, u = doe.FAC[k]; md.append(f"| {k}: {nm} | {lo*sc:g} {u} | {(lo+hi)/2*sc:g} | {hi*sc:g} {u} |")
md += ["", "## 실행 결과", "", "| run | " + " | ".join(K) + " | top Si | " + " | ".join(RESP) + " |", "|" + "---|"*(len(K)+2+len(RESP))]
for r in R: md.append(f"| {r['run']} | " + " | ".join(f"{r['x'][k]:+d}" for k in K) + f" | {r['top_si']:.1f} | " + " | ".join(f"{r[q]:.2f}" for q in RESP) + " |")
summary = {}
for q, (lab, note) in RESP.items():
    y = np.array([r[q] for r in F]); yb = y.mean()
    eff = np.array([col(t) @ y/(N/2) for t in TERMS]); pse, ME, SME = lenth(eff)
    names = ["".join(t) for t in TERMS]; sig = np.abs(eff) > ME
    keep = set(); [keep.update(itertools.chain.from_iterable(itertools.combinations(t, n) for n in range(1, len(t)+1))) for t, s in zip(TERMS, sig) if s]
    mt = [t for t in TERMS if t in keep]; Xm = np.c_[np.ones(N), *[col(t) for t in mt]] if mt else np.ones((N, 1))
    b = np.linalg.lstsq(Xm, y, rcond=None)[0]; r2 = 1 - ((y-Xm@b)**2).sum()/((y-yb)**2).sum()
    curv = (Cn[0][q]-yb) if Cn else np.nan
    summary[q] = dict(eff=dict(zip(names, eff)), ME=ME, SME=SME, PSE=pse, mean=yb, center=Cn[0][q] if Cn else None, curv=curv, r2=r2,
                      model={("".join(t) if t else "1"): v for t, v in zip([()]+mt, b)})
    # ---- fig 1: Pareto / 반정규 / 주효과 ----
    fig, ax = plt.subplots(1, 3, figsize=(16, 4.6)); o = np.argsort(np.abs(eff))
    ax[0].barh(range(len(eff)), np.abs(eff[o]), color=[BLUE if s else GRAY for s in sig[o]], height=.7)
    ax[0].set_yticks(range(len(eff))); ax[0].set_yticklabels([names[i] for i in o])
    for v, l in ((ME, "ME"), (SME, "SME")): ax[0].axvline(v, color=RED, lw=1, ls="--" if l == "ME" else ":"); ax[0].text(v, len(eff)-.5, f" {l} {v:.3g}", color=RED, fontsize=8)
    ax[0].set_xlabel(f"|효과| ({lab.split('[')[1].rstrip(']')})"); ax[0].set_title(f"Pareto (Lenth PSE={pse:.3g}, α=0.05)")
    ae = np.sort(np.abs(eff)); oo = np.argsort(np.abs(eff)); qn = stats.norm.ppf(.5+.5*(np.arange(1, len(ae)+1)-.5)/len(ae))
    ax[1].plot(ae, qn, "o", color=GRAY, ms=5)
    for i, (a_, q_) in enumerate(zip(ae, qn)):
        if sig[oo[i]]: ax[1].plot(a_, q_, "o", color=BLUE, ms=7); ax[1].annotate(names[oo[i]], (a_, q_), xytext=(5, -3), textcoords="offset points", fontsize=9)
    ax[1].plot([0, pse*qn.max()], [0, qn.max()], color=RED, lw=1, ls="--"); ax[1].set_xlabel("|효과|"); ax[1].set_ylabel("반정규 분위수"); ax[1].set_title("반정규 확률그림 (직선: PSE)")
    for i, k in enumerate(K):
        m_ = [y[X[:, i] == s].mean() for s in (-1, 1)]; xs = [3*i, 3*i+1]
        ax[2].plot(xs, m_, "-o", color=BLUE if sig[names.index(k)] else GRAY, lw=2, ms=6)
        ax[2].text(3*i+.5, max(m_), f"{k}\n{eff[names.index(k)]:+.3g}", ha="center", va="bottom", fontsize=8)
    if Cn: ax[2].axhline(Cn[0][q], color=ORANGE, lw=1, ls=":"); ax[2].text(3*len(K)-1.6, Cn[0][q], " 중심점", color=ORANGE, fontsize=8, va="bottom")
    ax[2].axhline(yb, color=GRAY, lw=.8); ax[2].set_xticks([3*i+.5 for i in range(len(K))]); ax[2].set_xticklabels([FN[k] for k in K], fontsize=8)
    ax[2].set_ylabel(lab); ax[2].set_title("주효과 (− → +)")
    fig.suptitle(f"{lab} — {note}   ȳ={yb:.3g}, 곡률(중심−ȳ)={curv:+.3g}, 축소모형 R²={r2:.4f}", fontsize=11); fig.tight_layout()
    fig.savefig(f"figs/doe_{q}_effects.png", dpi=140); plt.close(fig)
    # ---- fig 2: 2인자 교호작용 ----
    pairs = list(itertools.combinations(K, 2)); fig, ax = plt.subplots(1, len(pairs), figsize=(16, 3.4), sharey=True)
    for a_, (p1, p2) in zip(ax, pairs):
        i1, i2 = K.index(p1), K.index(p2)
        for s2, cc in ((-1, BLUE), (1, ORANGE)):
            a_.plot([-1, 1], [y[(X[:, i1] == s1) & (X[:, i2] == s2)].mean() for s1 in (-1, 1)], "-o", color=cc, lw=2, ms=5, label=f"{p2}{'+' if s2 > 0 else '−'}")
        e_ = eff[names.index(p1+p2)]; a_.set_title(f"{p1}×{p2}  효과 {e_:+.3g}" + (" *" if abs(e_) > ME else ""), fontsize=9)
        a_.set_xticks([-1, 1]); a_.set_xticklabels([f"{p1}−", f"{p1}+"]); a_.legend(frameon=False, fontsize=8)
    ax[0].set_ylabel(lab); fig.suptitle(f"{lab}: 2인자 교호작용 (평행 = 교호작용 없음, * = |효과|>ME)", fontsize=11); fig.tight_layout()
    fig.savefig(f"figs/doe_{q}_interactions.png", dpi=140); plt.close(fig)
    md += ["", f"## {lab}", "", f"ȳ = {yb:.4g}, 중심점 = {summary[q]['center']:.4g}, 곡률 = {curv:+.3g}, Lenth PSE = {pse:.3g}, ME = {ME:.3g}, SME = {SME:.3g}", "",
           "| 항 | 효과 | 계수(coded) | 판정 |", "|---|---|---|---|"]
    for i in np.argsort(-np.abs(eff)):
        md.append(f"| {names[i]} | {eff[i]:+.4g} | {eff[i]/2:+.4g} | {'**SME**' if abs(eff[i]) > SME else ('ME' if sig[i] else '')} |")
    md += ["", "축소 모형 (coded, x∈[−1,1]): ŷ = " + " ".join(f"{v:+.4g}" + ("" if t == "1" else "·" + "·".join(t)) for t, v in summary[q]["model"].items()) + f"   (R² = {r2:.5f})"]
# ---- 전체 개요: 표준화 효과 heatmap ----
fig, ax = plt.subplots(figsize=(13, 3.6)); names = ["".join(t) for t in TERMS]
Z = np.array([[summary[q]["eff"][n]/summary[q]["ME"] for n in names] for q in RESP]); lim = np.abs(Z).max()
im = ax.imshow(Z, cmap="RdBu_r", vmin=-lim, vmax=lim, aspect="auto"); ax.grid(False)
ax.set_xticks(range(len(names))); ax.set_xticklabels(names); ax.set_yticks(range(len(RESP))); ax.set_yticklabels([RESP[q][0] for q in RESP])
for i in range(Z.shape[0]):
    for j in range(Z.shape[1]): ax.text(j, i, f"{Z[i,j]:.1f}", ha="center", va="center", fontsize=7, color="k" if abs(Z[i, j]) < .6*lim else "w")
fig.colorbar(im, ax=ax, label="효과 / ME (|값|>1 유의)"); ax.set_title("응답별 표준화 효과 (효과/ME, Lenth α=0.05)")
fig.tight_layout(); fig.savefig("figs/doe_overview.png", dpi=140)
open(f"{doe.OUTD}/report.md", "w").write("\n".join(md)+"\n"); json.dump(summary, open(f"{doe.OUTD}/summary.json", "w"), indent=1)
print("\n".join(md[-40:]))
