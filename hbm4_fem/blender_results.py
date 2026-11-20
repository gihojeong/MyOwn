"""FEM 결과를 Blender(Cycles)로 3D 렌더: 1/4 절개 + 변형(uz 확대) + 컬러맵.
usage: python3 blender_results.py <variant> <field: T_op | vm_25 | vm_op | w_25 | w_260> [mag]"""
import sys, os, numpy as np, bpy, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt; from matplotlib import cm, colors
from mathutils import Vector
from frd import read_frd
import params as P
V, F = sys.argv[1], sys.argv[2]; MAG = float(sys.argv[3]) if len(sys.argv) > 3 else 150.0
ZS = 6.0; O = "out"; FIG = "figs"
plt.rcParams.update({"font.family": "NanumGothic", "axes.unicode_minus": False})
m = np.load(f"{O}/mesh_{V}.npz"); X, Y, Z = m["X"], m["Y"], m["Z"]; nx, ny, nz = len(X), len(Y), len(Z)
steps = read_frd(f"{O}/mech_{V}.frd"); SEL = {"25": 0, "260": len(P.SWEEP)-1, "op": len(P.SWEEP)}
sid = SEL[F.split("_")[1]]; U = steps[sid]["DISP"][1].reshape(nz, ny, nx, 3).transpose(2, 1, 0, 3)  # [i,j,k,3]
XX, YY = np.meshgrid(X, Y, indexing="ij"); A = np.c_[XX.ravel(), YY.ravel(), np.ones(XX.size)]
c = np.linalg.lstsq(A, U[:, :, 0, 2].ravel(), rcond=None)[0]; uz = U[..., 2] - (A @ c).reshape(nx, ny)[:, :, None]
cut = F != "w_25" and F != "w_260"
# element keep mask (1/4 절개: x>xm & y<ym 제거)
xc, yc = (X[:-1]+X[1:])/2, (Y[:-1]+Y[1:])/2
keep = np.ones((nx-1, ny-1, nz-1), bool)
if cut: keep[np.ix_(xc > P.FOOT[0]/2, yc < P.FOOT[1]/2, np.ones(nz-1, bool))] = False
# field
if F.startswith("vm"):
    s = np.load(f"{O}/elstress_{V}.npy")[{"25": 0, "260": 1, "op": 2}[F.split("_")[1]]].astype(float)
    val_e = np.sqrt(.5*((s[:, 0]-s[:, 1])**2+(s[:, 1]-s[:, 2])**2+(s[:, 2]-s[:, 0])**2)+3*(s[:, 3:]**2).sum(1)).reshape(nx-1, ny-1, nz-1, order="F")
    nodal = None; cmap, lab = "magma", "von Mises [MPa]"; vmin, vmax = 0, np.percentile(val_e[keep], 99.7)
elif F == "T_op":
    nodal = read_frd(f"{O}/thermal_{V}.frd")[-1]["NDTEMP"][1][:, 0].reshape(nz, ny, nx).transpose(2, 1, 0)
    cmap, lab = "inferno", "Temperature [°C]"; vmin, vmax = nodal.min(), nodal.max()
else:
    nodal = uz*1e3; lim = abs(nodal).max(); cmap, lab, vmin, vmax = "RdBu_r", "w (uz, 평면보정) [μm]", -lim, lim
norm = colors.Normalize(vmin, vmax); cmo = plt.get_cmap(cmap)
# boundary quads
nid = lambda i, j, k: i + nx*(j + ny*k)
faces, fval, fnodes = [], [], []
K = np.pad(keep, 1)
dirs = [((-1, 0, 0), [(0, 0, 0), (0, 1, 0), (0, 1, 1), (0, 0, 1)]), ((1, 0, 0), [(1, 0, 0), (1, 0, 1), (1, 1, 1), (1, 1, 0)]),
        ((0, -1, 0), [(0, 0, 0), (0, 0, 1), (1, 0, 1), (1, 0, 0)]), ((0, 1, 0), [(0, 1, 0), (1, 1, 0), (1, 1, 1), (0, 1, 1)]),
        ((0, 0, -1), [(0, 0, 0), (1, 0, 0), (1, 1, 0), (0, 1, 0)]), ((0, 0, 1), [(0, 0, 1), (0, 1, 1), (1, 1, 1), (1, 0, 1)])]
I, J, Kk = np.nonzero(keep)
for (di, dj, dk), corners in dirs:
    b = ~K[I+1+di, J+1+dj, Kk+1+dk]; i, j, k = I[b], J[b], Kk[b]
    q = np.stack([nid(i+a, j+bb, k+cc) for a, bb, cc in corners], 1); fnodes.append(q)
    if nodal is None: fval.append(val_e[i, j, k])
fq = np.concatenate(fnodes)
used, inv = np.unique(fq, return_inverse=True); inv = inv.reshape(-1, 4)
ii, jj, kk = used % nx, (used // nx) % ny, used // (nx*ny)
pos = np.c_[X[ii] + U[ii, jj, kk, 0], Y[jj] + U[ii, jj, kk, 1], ZS*Z[kk] + MAG*uz[ii, jj, kk]] - [P.FOOT[0]/2, P.FOOT[1]/2, 0]
if nodal is None: corner_rgb = np.repeat(cmo(norm(np.concatenate(fval)))[:, None, :], 4, 1)
else: corner_rgb = cmo(norm(nodal[ii, jj, kk]))[inv]
corner_rgb = corner_rgb.copy(); c3 = corner_rgb[..., :3]
corner_rgb[..., :3] = np.where(c3 <= 0.04045, c3/12.92, ((c3+0.055)/1.055)**2.4)   # sRGB→linear
# ---- Blender scene ----
bpy.ops.wm.read_factory_settings(use_empty=True); sc = bpy.context.scene
me = bpy.data.meshes.new("fem"); me.from_pydata(pos.tolist(), [], inv.tolist()); me.update()
ca = me.color_attributes.new("C", "FLOAT_COLOR", "CORNER"); ca.data.foreach_set("color", corner_rgb.reshape(-1))
ob = bpy.data.objects.new("fem", me); sc.collection.objects.link(ob)
mt = bpy.data.materials.new("m"); mt.use_nodes = True; nt = mt.node_tree
bs = nt.nodes["Principled BSDF"]; at = nt.nodes.new("ShaderNodeVertexColor"); at.layer_name = "C"
nt.links.new(at.outputs["Color"], bs.inputs["Base Color"]); nt.links.new(at.outputs["Color"], bs.inputs["Emission Color"])
bs.inputs["Emission Strength"].default_value = 0.12; bs.inputs["Roughness"].default_value = 0.55; ob.data.materials.append(mt)
# layer 경계선 (wire overlay): 각 die/bond 경계 z에 얇은 edge — Freestyle 대신 wireframe modifier 생략, 대신 edge split 없이 flat shading
w = bpy.data.worlds.new("w"); sc.world = w; w.use_nodes = True
w.node_tree.nodes["Background"].inputs[0].default_value = (0.95, 0.95, 0.96, 1); w.node_tree.nodes["Background"].inputs[1].default_value = 0.35
L = bpy.data.lights.new("s", "SUN"); L.energy = 2.5; lo = bpy.data.objects.new("s", L); sc.collection.objects.link(lo); lo.rotation_euler = (0.6, 0.3, 0.8)
bpy.ops.mesh.primitive_plane_add(size=300, location=(0, 0, min(pos[:, 2].min(), 0)-0.05))
g = bpy.context.object; gm = bpy.data.materials.new("g"); gm.use_nodes = True
gm.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (0.9, 0.9, 0.92, 1); g.data.materials.append(gm)
cam = bpy.data.objects.new("c", bpy.data.cameras.new("c")); sc.collection.objects.link(cam); sc.camera = cam; cam.data.lens = 60
cam.location = (24, -29, 19); cam.rotation_euler = (Vector((0, 0, 1.4)) - cam.location).to_track_quat("-Z", "Y").to_euler()
sc.render.engine = "CYCLES"; sc.cycles.device = "CPU"; sc.cycles.samples = 48; sc.cycles.use_denoising = True
sc.render.resolution_x, sc.render.resolution_y = 1500, 1000; sc.view_settings.view_transform = "Standard"; sc.view_settings.exposure = -0.3
raw = f"{O}/_r_{V}_{F}.png"; sc.render.filepath = raw; bpy.ops.render.render(write_still=True)
# colorbar 합성
img = plt.imread(raw); fig = plt.figure(figsize=(11, 7)); ax = fig.add_axes([0, 0, .86, .92]); ax.imshow(img); ax.axis("off")
cax = fig.add_axes([.88, .2, .018, .6]); fig.colorbar(cm.ScalarMappable(norm, cmo), cax=cax, label=lab)
ttl = {"T_op": "운전 온도장", "vm_25": "von Mises @25°C", "vm_op": "von Mises @운전", "w_25": "warpage @25°C", "w_260": "warpage @260°C"}[F]
fig.text(.02, .95, f"HBM4-8H [{V}]  {ttl}   (z 형상 ×{ZS:.0f}, uz 변위 ×{MAG:.0f})", fontsize=13)
fig.savefig(f"{FIG}/blender_{V}_{F}.png", dpi=140); os.remove(raw); print("ok", F)
