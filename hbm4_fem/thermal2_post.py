"""과도 열해석 후처리: T(t) 곡선(+집중 RC 검산), 시간별 평면·단면 맵."""
import json, numpy as np, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
from frd import read_frd
import thermal2 as T2, stack as S
plt.rcParams.update({"font.family": "NanumGothic", "axes.unicode_minus": False, "font.size": 9,
                     "axes.spines.top": False, "axes.spines.right": False})
m = np.load(f"{T2.OUT}/{T2.NAME}_mesh.npz"); X, Y, Z, kind, lname, phy = m["X"], m["Y"], m["Z"], m["kind"], m["lname"], m["phy"]
nx, ny, nz = len(X), len(Y), len(Z)
st = read_frd(f"{T2.OUT}/{T2.NAME}.frd"); Ts = [s["NDTEMP"][1][:, 0].reshape(nz, ny, nx).transpose(2, 1, 0) for s in st]
times = T2.TP + [np.inf]; assert len(Ts) == len(times), (len(Ts), len(times))
def elemT(T): return sum(T[a:nx-1+a, b:ny-1+b, c:nz-1+c] for a in (0, 1) for b in (0, 1) for c in (0, 1))/8
vol = np.einsum("i,j,k->ijk", np.diff(X), np.diff(Y), np.diff(Z))
def vavg(Te, msk): return float((Te[msk]*vol[msk]).sum()/vol[msk].sum())
R = []
for t, T in zip(times, Ts):
    Te = elemT(T)
    R.append(dict(t=t, Tmax=float(T.max()), phy=vavg(Te, phy), base=vavg(Te, lname == "Base_Si"),
                  top_si=vavg(Te, lname == "Core8_Si"), top_surf_max=float(T[:, :, -1].max()), pkg=vavg(Te, np.ones_like(phy))))
json.dump(R, open(f"{T2.OUT}/summary.json", "w"), indent=1, default=str)
# 집중 RC 검산
A = S.L_LOGIC**2*1e-6; Rth = 1/((T2.H_TOP+T2.H_BOT)*A); C = sum(vol[kind == k].sum()*2*1e-9*T2.therm(k, T2.CASE)["rho"]*1e12*T2.therm(k, T2.CASE)["cp"]*1e-6 for k in np.unique(kind))
tau = Rth*C
fig = plt.figure(figsize=(16, 9.5)); gs = fig.add_gridspec(3, 4, height_ratios=[1.15, 1, 1])
ax = fig.add_subplot(gs[0, :2]); tt = np.array(T2.TP)
for key, lab, c in [("Tmax", "최고온도 (PHY hot spot)", "#e34948"), ("phy", "PHY 영역 평균", "#eb6834"), ("base", "B-die(base Si) 평균", "#2a78d6"),
                    ("top_si", "top core Si 평균", "#1baf7a"), ("pkg", "패키지 체적 평균", "#6250d6")]:
    ax.plot(tt, [r[key] for r in R[:-1]], "-o", ms=3.5, lw=2, color=c, label=lab); ax.axhline(R[-1][key], color=c, lw=.8, ls=":")
tf = np.logspace(-4, np.log10(2), 200); ax.plot(tf, T2.T_REF + T2.P_PHY*Rth*(1-np.exp(-tf/tau)), "--", color="#555", lw=1.2, label=f"집중 RC 검산 (R={Rth:.3f} K/W, τ={tau*1e3:.0f} ms)")
ax.set_xscale("log"); ax.set_xlabel("시간 [s]  (점선: 정상상태)"); ax.set_ylabel("T [°C]"); ax.grid(alpha=.25); ax.legend(frameon=False, fontsize=8)
ax.set_title(f"HBM4-8H B-die PHY {T2.P_PHY:g} W 계단 발열 — 시간 응답 (T₀ {T2.T_REF:g} °C)")
ax = fig.add_subplot(gs[0, 2:]); ax.axis("off")
rows = [["t", "Tmax", "PHY평균", "base평균", "top Si평균", "상면 max"]] + [[("정상" if np.isinf(r["t"]) else f"{r['t']*1e3:g} ms"), *[f"{r[k]:.2f}" for k in ("Tmax", "phy", "base", "top_si", "top_surf_max")]] for r in R]
tb = ax.table(cellText=rows, loc="center", cellLoc="center"); tb.auto_set_font_size(False); tb.set_fontsize(8.5); tb.scale(1, 1.25)
ax.set_title("온도 [°C]", fontsize=10)
show = [(2, "1 ms"), (4, "10 ms"), (6, "100 ms"), (len(R)-1, "정상상태")]
vmin, vmax = T2.T_REF, R[-1]["Tmax"]
kphy = int(np.where(phy.any(axis=(0, 1)))[0][0])
Yf = np.r_[-Y[::-1], Y[1:]]
for c_, (i, lab) in enumerate(show):
    T = Ts[i]; Tp = 0.5*(T[:, :, kphy]+T[:, :, kphy+1]); Tf = np.c_[Tp[:, ::-1], Tp[:, 1:]]
    a = fig.add_subplot(gs[1, c_]); im = a.pcolormesh(X, Yf, Tf.T, cmap="inferno", vmin=vmin, vmax=vmax, shading="gouraud")
    a.set_aspect("equal"); a.set_title(f"{lab}: B-die 전면(PHY층) Tmax {Tp.max():.1f}"); a.set_xlabel("x [mm] (−x: GPU측 PHY)".replace("−", "-"))
    a2 = fig.add_subplot(gs[2, c_]); a2.pcolormesh(X, Z*1e3, T[:, 0, :].T, cmap="inferno", vmin=vmin, vmax=vmax, shading="gouraud")
    a2.set_title(f"{lab}: 단면 y=0 (z μm)"); a2.set_xlabel("x [mm]"); a2.set_ylabel("z [μm]")
fig.colorbar(im, ax=fig.axes[-8:], label="T [°C]", shrink=.8)
fig.suptitle("HBM4-8H 과도 열해석 (CalculiX DC3D8, 1/2 대칭, 62,496 요소)", fontsize=12)
fig.savefig("figs/thermal_phy_transient.png", dpi=140, bbox_inches="tight"); print(json.dumps(R, default=str, indent=0)[:1500]); print("R", Rth, "C", C, "tau", tau)
