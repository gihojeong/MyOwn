"""v3(HA) 정상상태 온도장: 2D(PHY 층 평면·y=0 단면, PHY 윤곽) + Blender 3D(1/2 모델, 앞면=y=0 단면, PHY 윤곽). usage: python3 v3_thermal_fig.py <prod>"""
import sys, numpy as np, bpy, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt; from matplotlib import cm, colors
from matplotlib.patches import Rectangle
from mathutils import Vector
import grid3 as G, stack as S
plt.rcParams.update({"font.family": "NanumGothic", "axes.unicode_minus": False, "font.size": 9})
P = sys.argv[1]; ZS = 4.0
g = G.grid(P); X, Y, Z = g["X"], g["Y"], g["Z"]; nx, ny, nz = len(X), len(Y), len(Z); px0, px1, _, py1 = g["phy_box"]
f = np.load(f"out3/thermal/{P}/fields.npz"); Tn = f["T"][-1]; T = Tn.reshape(nz, ny, nx).transpose(2, 1, 0)
lx, ly, dx, dy = S.Lxy(g["c"]); kb = int(np.argmin(abs(Z-0.0174)))
vmin, vmax = float(Tn.min()), float(Tn.max()); norm = colors.Normalize(vmin, vmax); cmo = plt.get_cmap("inferno")
# ---------- Blender 3D ----------
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
used = np.unique(np.array(faces)); rm = -np.ones(len(V), int); rm[used] = np.arange(len(used)); F = rm[np.array(faces)]
bpy.ops.wm.read_factory_settings(use_empty=True); sc = bpy.context.scene
me = bpy.data.meshes.new("t"); me.from_pydata(V[used].tolist(), [], F.tolist()); me.update()
rgb = cmo(norm(Tn[used])); c3 = rgb[:, :3]; rgb[:, :3] = np.where(c3 <= .04045, c3/12.92, ((c3+.055)/1.055)**2.4)
ca = me.color_attributes.new("C", "FLOAT_COLOR", "POINT"); ca.data.foreach_set("color", rgb.ravel())
ob = bpy.data.objects.new("t", me); sc.collection.objects.link(ob)
mt = bpy.data.materials.new("m"); mt.use_nodes = True; nt = mt.node_tree; bs = nt.nodes["Principled BSDF"]
vc = nt.nodes.new("ShaderNodeVertexColor"); vc.layer_name = "C"; nt.links.new(vc.outputs["Color"], bs.inputs["Base Color"])
nt.links.new(vc.outputs["Color"], bs.inputs["Emission Color"]); bs.inputs["Emission Strength"].default_value = .25; bs.inputs["Roughness"].default_value = .6
ob.data.materials.append(mt)
# PHY 윤곽: 열원층(base Si 전면) 높이의 사각 테두리 + 상면 투영 테두리
def frame(z, col, r=0.03):
    m = bpy.data.materials.new("f"); m.use_nodes = True; b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*col, 1); b.inputs["Emission Color"].default_value = (*col, 1); b.inputs["Emission Strength"].default_value = 2.0
    for (a, b_) in [((px0, 0), (px1, 0)), ((px1, 0), (px1, py1)), ((px1, py1), (px0, py1)), ((px0, py1), (px0, 0))]:
        p0, p1 = Vector((*a, z)), Vector((*b_, z)); d = p1-p0
        bpy.ops.mesh.primitive_cylinder_add(radius=r, depth=d.length, location=(p0+p1)/2)
        o = bpy.context.object; o.rotation_euler = d.to_track_quat("Z", "Y").to_euler(); o.data.materials.append(m)
frame(ZS*(Z[kb]+Z[kb+1])/2, (0.2, 0.9, 1.0)); frame(ZS*Z[-1]+0.02, (0.2, 0.9, 1.0), 0.02)
wo = bpy.data.worlds.new("w"); sc.world = wo; wo.use_nodes = True; wo.node_tree.nodes["Background"].inputs[0].default_value = (.93, .94, .96, 1); wo.node_tree.nodes["Background"].inputs[1].default_value = .4
L = bpy.data.lights.new("s", "SUN"); L.energy = 2.5; lo = bpy.data.objects.new("s", L); sc.collection.objects.link(lo); lo.rotation_euler = (.8, .1, -.6)
cam = bpy.data.objects.new("c", bpy.data.cameras.new("c")); sc.collection.objects.link(cam); sc.camera = cam; cam.data.lens = 38
cam.location = (-12.5, -13.0, 9.5); cam.rotation_euler = (Vector((-0.5, ly/4, 0.6)) - cam.location).to_track_quat("-Z", "Y").to_euler()
sc.render.engine = "CYCLES"; sc.cycles.device = "CPU"; sc.cycles.samples = 32; sc.cycles.use_denoising = True
sc.render.resolution_x, sc.render.resolution_y = 1400, 950; sc.view_settings.view_transform = "Standard"
raw = f"out3/thermal/{P}/_r.png"; sc.render.filepath = raw; bpy.ops.render.render(write_still=True)
# ---------- 합성 ----------
fig = plt.figure(figsize=(17, 9)); gs = fig.add_gridspec(2, 2, width_ratios=[1.35, 1])
a = fig.add_subplot(gs[:, 0]); a.imshow(plt.imread(raw)); a.axis("off")
a.set_title(f"3D (1/2 모델, 앞면 = y=0 대칭 단면, z×{ZS:g})  하늘색 = PHY 박스(열원층·상면 투영)", fontsize=10)
Yf = np.r_[-Y[::-1], Y[1:]]; Tp = 0.5*(T[:, :, kb]+T[:, :, kb+1]); Tf = np.c_[Tp[:, ::-1], Tp[:, 1:]]
b = fig.add_subplot(gs[0, 1]); im = b.pcolormesh(X, Yf, Tf.T, cmap=cmo, norm=norm, shading="gouraud"); b.set_aspect("equal")
b.add_patch(Rectangle((px0, -py1), px1-px0, 2*py1, fill=False, ec="cyan", lw=1.5, ls="--"))
b.add_patch(Rectangle((-dx/2, -dy/2), dx, dy, fill=False, ec="w", lw=.8, ls=":"))
b.set_title(f"B-die 전면(열원층) 평면: Tmax {Tp.max():.1f} °C   (점선 흰색 = DRAM die)"); b.set_xlabel("x [mm]  (x<0: GPU 측)"); b.set_ylabel("y [mm]")
c = fig.add_subplot(gs[1, 1]); c.pcolormesh(X, Z*1e3, T[:, 0, :].T, cmap=cmo, norm=norm, shading="gouraud")
c.add_patch(Rectangle((px0, Z[kb]*1e3), px1-px0, (Z[kb+1]-Z[kb])*1e3, fill=False, ec="cyan", lw=1.5))
c.set_title("y=0 단면 (z 실척 μm)"); c.set_xlabel("x [mm]"); c.set_ylabel("z [μm]")
fig.colorbar(cm.ScalarMappable(norm, cmo), ax=[b, c], label="T [°C]", shrink=.85)
fig.suptitle(f"{P}: 고객 사용환경 full-load 정상상태 (HA, v3) — PHY {G.PRODUCTS[P]['phy_W']:g} W / 스택 합계 {'36' if '4' in P[:4] else '30'} W", fontsize=13)
fig.savefig(f"figs/v3_thermal_{P}.png", dpi=130, bbox_inches="tight"); print("ok", P)
