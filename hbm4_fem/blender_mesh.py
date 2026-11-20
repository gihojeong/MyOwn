"""Blender: 1/4 대칭 FEM 격자 3D 렌더 (재료색 면 + 요소 경계선, z 과장). usage: python3 blender_mesh.py <mesh_name> [zscale]"""
import sys, numpy as np, bpy
from mathutils import Vector
NAME = sys.argv[1]; ZS = float(sys.argv[2]) if len(sys.argv) > 2 else 8.0
m = np.load(f"out2/{NAME}_mesh.npz"); X, Y, Z, K = m["X"], m["Y"], m["Z"]*ZS, m["kind"].astype("<U10"); K[m["lname"] == "Base_Si"] = "si_base"
nx, ny, nz = len(X), len(Y), len(Z); nid = lambda i, j, k: i + nx*(j + ny*k)
RGB = {"si": (.49, .56, .70), "si_top": (.35, .43, .59), "si_base": (.27, .33, .48), "beol": (.82, .54, .24), "gap": (.25, .65, .42), "emc": (.17, .17, .18)}
faces, cols = [], []
def lin(c): return tuple(((v+.055)/1.055)**2.4 if v > .04045 else v/12.92 for v in c)
for k in range(nz-1):
    for j in range(ny-1):
        for i, ie in ((nx-1, nx-2), (0, 0)): faces.append([nid(i, j, k), nid(i, j+1, k), nid(i, j+1, k+1), nid(i, j, k+1)]); cols.append(K[ie, j, k])
    for i in range(nx-1):
        for j, je in ((ny-1, ny-2), (0, 0)): faces.append([nid(i, j, k), nid(i+1, j, k), nid(i+1, j, k+1), nid(i, j, k+1)]); cols.append(K[i, je, k])
for j in range(ny-1):
    for i in range(nx-1):
        for k, ke in ((nz-1, nz-2), (0, 0)): faces.append([nid(i, j, k), nid(i+1, j, k), nid(i+1, j+1, k), nid(i, j+1, k)]); cols.append(K[i, j, ke])
I, J, Kk = np.meshgrid(range(nx), range(ny), range(nz), indexing="ij")
V = np.zeros((nx*ny*nz, 3)); idx = (I + nx*(J + ny*Kk)).ravel(); V[idx] = np.c_[X[I.ravel()], Y[J.ravel()], Z[Kk.ravel()]]
bpy.ops.wm.read_factory_settings(use_empty=True); sc = bpy.context.scene
me = bpy.data.meshes.new("m"); me.from_pydata(V.tolist(), [], faces); me.update()
ca = me.color_attributes.new("C", "FLOAT_COLOR", "CORNER"); cc = np.repeat(np.array([(*lin(RGB[c]), 1) for c in cols]), 4, 0); ca.data.foreach_set("color", cc.ravel())
ob = bpy.data.objects.new("mesh", me); sc.collection.objects.link(ob)
mt = bpy.data.materials.new("m"); mt.use_nodes = True; nt = mt.node_tree; bs = nt.nodes["Principled BSDF"]
vc = nt.nodes.new("ShaderNodeVertexColor"); vc.layer_name = "C"; nt.links.new(vc.outputs["Color"], bs.inputs["Base Color"]); bs.inputs["Roughness"].default_value = .6
ob.data.materials.append(mt)
wf = ob.copy(); wf.data = ob.data.copy(); sc.collection.objects.link(wf)
w = wf.modifiers.new("w", "WIREFRAME"); w.thickness = 0.0045; w.use_replace = True
wm = bpy.data.materials.new("wire"); wm.use_nodes = True; wm.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (.9, .9, .92, 1)
wf.data.materials.clear(); wf.data.materials.append(wm)
wo = bpy.data.worlds.new("w"); sc.world = wo; wo.use_nodes = True
wo.node_tree.nodes["Background"].inputs[0].default_value = (.93, .94, .96, 1); wo.node_tree.nodes["Background"].inputs[1].default_value = .45
L = bpy.data.lights.new("s", "SUN"); L.energy = 3.0; lo = bpy.data.objects.new("s", L); sc.collection.objects.link(lo); lo.rotation_euler = (.75, .15, 2.4)
cam = bpy.data.objects.new("c", bpy.data.cameras.new("c")); sc.collection.objects.link(cam); sc.camera = cam
sc.render.engine = "CYCLES"; sc.cycles.device = "CPU"; sc.cycles.samples = 48; sc.cycles.use_denoising = True
sc.render.resolution_x, sc.render.resolution_y = 1600, 1100; sc.view_settings.view_transform = "Standard"
def shoot(fn, loc, tgt, lens):
    cam.location = loc; cam.data.lens = lens; cam.rotation_euler = (Vector(tgt)-Vector(loc)).to_track_quat("-Z", "Y").to_euler()
    sc.render.filepath = f"figs/{fn}"; bpy.ops.render.render(write_still=True)
H = Z[-1]
shoot(f"mesh3d_{NAME}_full.png", (-6.5, -7.5, 7.0), (2.9, 2.9, H*0.35), 40)                 # 대칭 단면(x=0,y=0) 쪽: 내부 층 노출
shoot(f"mesh3d_{NAME}_corner.png", (5.0, -2.2, H*0.85), (5.0, 0.0, H*0.45), 50)              # y=0 단면, DRAM 모서리(x=5)·EMC 링 확대
print("ok")
