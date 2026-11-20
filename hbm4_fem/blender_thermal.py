"""과도 열해석 3D 렌더: 1/2 모델(y≥0) 외곽면 + y=0 대칭 단면 = 절개면. z×4. usage: python3 blender_thermal.py"""
import numpy as np, bpy, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt; from matplotlib import cm, colors
from mathutils import Vector
from frd import read_frd
import thermal2 as T2
plt.rcParams.update({"font.family": "NanumGothic", "axes.unicode_minus": False})
ZS = 4.0; m = np.load(f"{T2.OUT}/{T2.NAME}_mesh.npz"); X, Y, Z = m["X"], m["Y"], m["Z"]; nx, ny, nz = len(X), len(Y), len(Z)
st = read_frd(f"{T2.OUT}/{T2.NAME}.frd"); Ts_all = [s["NDTEMP"][1][:, 0] for s in st]
t_all = [float(l.split()[2]) for l in open(f"{T2.OUT}/{T2.NAME}.frd") if l.startswith("  100CL")]
pick = lambda t: Ts_all[int(np.argmin([abs(x-t) for x in t_all]))]
nid = lambda i, j, k: i + nx*(j + ny*k); faces = []
for k in range(nz-1):
    for j in range(ny-1):
        for i in (0, nx-1): faces.append([nid(i, j, k), nid(i, j+1, k), nid(i, j+1, k+1), nid(i, j, k+1)])
    for i in range(nx-1):
        for j in (0, ny-1): faces.append([nid(i, j, k), nid(i+1, j, k), nid(i+1, j, k+1), nid(i, j, k+1)])
for j in range(ny-1):
    for i in range(nx-1):
        for k in (0, nz-1): faces.append([nid(i, j, k), nid(i+1, j, k), nid(i+1, j+1, k), nid(i, j+1, k)])
I, J, K = np.meshgrid(range(nx), range(ny), range(nz), indexing="ij"); V = np.zeros((nx*ny*nz, 3))
V[(I+nx*(J+ny*K)).ravel()] = np.c_[X[I.ravel()], Y[J.ravel()], ZS*Z[K.ravel()]]
used = np.unique(np.array(faces)); remap = -np.ones(len(V), int); remap[used] = np.arange(len(used)); F = remap[np.array(faces)]
bpy.ops.wm.read_factory_settings(use_empty=True); sc = bpy.context.scene
me = bpy.data.meshes.new("t"); me.from_pydata(V[used].tolist(), [], F.tolist()); me.update()
ca = me.color_attributes.new("C", "FLOAT_COLOR", "POINT"); ob = bpy.data.objects.new("t", me); sc.collection.objects.link(ob)
mt = bpy.data.materials.new("m"); mt.use_nodes = True; nt = mt.node_tree; bs = nt.nodes["Principled BSDF"]
vc = nt.nodes.new("ShaderNodeVertexColor"); vc.layer_name = "C"; nt.links.new(vc.outputs["Color"], bs.inputs["Base Color"])
nt.links.new(vc.outputs["Color"], bs.inputs["Emission Color"]); bs.inputs["Emission Strength"].default_value = .15; bs.inputs["Roughness"].default_value = .6
ob.data.materials.append(mt)
wo = bpy.data.worlds.new("w"); sc.world = wo; wo.use_nodes = True; wo.node_tree.nodes["Background"].inputs[0].default_value = (.93, .94, .96, 1); wo.node_tree.nodes["Background"].inputs[1].default_value = .4
L = bpy.data.lights.new("s", "SUN"); L.energy = 2.5; lo = bpy.data.objects.new("s", L); sc.collection.objects.link(lo); lo.rotation_euler = (.8, .1, -.6)
cam = bpy.data.objects.new("c", bpy.data.cameras.new("c")); sc.collection.objects.link(cam); sc.camera = cam; cam.data.lens = 38
cam.location = (-13.0, -13.5, 9.0); cam.rotation_euler = (Vector((-0.8, 2.6, 0.6)) - cam.location).to_track_quat("-Z", "Y").to_euler()
sc.render.engine = "CYCLES"; sc.cycles.device = "CPU"; sc.cycles.samples = 32; sc.cycles.use_denoising = True
sc.render.resolution_x, sc.render.resolution_y = 1200, 820; sc.view_settings.view_transform = "Standard"
show = [(pick(1e-3), "t = 1 ms"), (pick(1e-2), "t = 10 ms"), (pick(0.1), "t = 100 ms"), (Ts_all[-1], "정상상태")]
vmin, vmax = T2.T_REF, Ts_all[-1].max(); norm = colors.Normalize(vmin, vmax); cmo = plt.get_cmap("inferno")
imgs = []
for i, (Tv, lab) in enumerate(show):
    rgb = cmo(norm(Tv[used])); c3 = rgb[:, :3]; rgb[:, :3] = np.where(c3 <= .04045, c3/12.92, ((c3+.055)/1.055)**2.4)
    ca.data.foreach_set("color", rgb.ravel()); me.update()
    fn = f"{T2.OUT}/_r{i}.png"; sc.render.filepath = fn; bpy.ops.render.render(write_still=True); imgs.append((plt.imread(fn), lab, Tv.max()))
fig, axs = plt.subplots(2, 2, figsize=(14, 9.6))
for a, (im, lab, tm) in zip(axs.ravel(), imgs): a.imshow(im); a.axis("off"); a.set_title(f"{lab}   Tmax {tm:.1f} °C", fontsize=12)
fig.colorbar(cm.ScalarMappable(norm, cmo), ax=axs, shrink=.7, label="T [°C]")
fig.suptitle(f"HBM4-8H B-die PHY {T2.P_PHY:g} W 발열 — 1/2 모델(앞면 = y=0 대칭 단면), z×{ZS:g}", fontsize=13)
fig.savefig("figs/thermal_phy_transient_3d.png", dpi=130, bbox_inches="tight"); print("ok")
