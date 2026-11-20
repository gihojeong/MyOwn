"""Blender(bpy)로 HBM4-8H 3D 모델 생성 → .blend 저장, 렌더, FEM용 layer export(JSON).
usage: python3 blender_build.py <variant> <outdir>"""
import sys, os, json, math, bpy, bmesh
from mathutils import Vector
import params as P

V = sys.argv[1] if len(sys.argv) > 1 else "A_MRMUF"
OUT = sys.argv[2] if len(sys.argv) > 2 else "out"; os.makedirs(OUT, exist_ok=True)
bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene

def mat(name, rgb, metal=0.0, rough=0.4, alpha=1.0, trans=0.0):
    m = bpy.data.materials.new(name); m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*rgb, 1); b.inputs["Metallic"].default_value = metal
    b.inputs["Roughness"].default_value = rough; b.inputs["Alpha"].default_value = alpha
    if trans: b.inputs["Transmission Weight"].default_value = trans
    return m
M = {"base": mat("Si_base", (0.10, 0.12, 0.18), 0.35, 0.35),
     "core": mat("Si_core", (0.20, 0.23, 0.32), 0.45, 0.3),
     "bond": mat("MUF" if P.VARIANTS[V]["bond"] == "MUF" else "NCF",
                 (0.85, 0.55, 0.12) if P.VARIANTS[V]["bond"] == "MUF" else (0.2, 0.6, 0.35), 0.0, 0.5),
     "emc": mat("EMC", (0.03, 0.03, 0.035), 0.0, 0.35, alpha=1.0),
     "cu": mat("Cu", (0.95, 0.55, 0.3), 1.0, 0.25),
     "phy": mat("PHY", (0.15, 0.55, 0.85), 0.3, 0.3)}

def box(name, x0, x1, y0, y1, z0, z1, m, props):
    bpy.ops.mesh.primitive_cube_add(size=1, location=((x0+x1)/2, (y0+y1)/2, (z0+z1)/2))
    o = bpy.context.object; o.name = name; o.scale = (x1-x0, y1-y0, z1-z0)
    bpy.ops.object.transform_apply(scale=True); o.data.materials.append(m)
    for k, v in props.items(): o[k] = v
    bevel = o.modifiers.new("bev", "BEVEL"); bevel.width = min(0.004, (z1-z0)/4); bevel.segments = 2
    return o

Ls, H = P.layers(V); objs = []
for (n, kind, z0, z1, (x0, x1, y0, y1)) in Ls:
    objs.append(box(n, x0, x1, y0, y1, z0, z1, M[kind], dict(fem_kind=kind, fem_layer=n)))
# EMC sidewall ring (MR-MUF: MUF가 그대로 mold, TC-NCF: 별도 EMC mold)
zc0, zc1 = P.T_BASE, max(l[3] for l in Ls if l[1] in ("core", "bond"))
ring = box("EMC_Sidewall", 0, P.FOOT[0], 0, P.FOOT[1], zc0, zc1, M["emc"], dict(fem_kind="emc_ring", fem_layer="EMC_Sidewall"))
cut = box("cut", P.INSET, P.FOOT[0]-P.INSET, P.INSET, P.FOOT[1]-P.INSET, zc0-0.01, zc1+0.01, M["emc"], {})
b = ring.modifiers.new("hole", "BOOLEAN"); b.object = cut; b.operation = "DIFFERENCE"
bpy.context.view_layer.objects.active = ring; bpy.ops.object.modifier_apply(modifier="hole")
bpy.data.objects.remove(cut); objs.append(ring)
# PHY 영역 (base die 상면 표식)
x0, x1, y0, y1 = P.PHY
phy = box("PHY_mark", x0, x1, y0, y1, P.T_BASE-0.004, P.T_BASE+0.0005, M["phy"], dict(fem_kind="mark"))
# µbump/TSV 배열 (geometry: array modifier, 시각화 전용 — FEM은 균질화)
tx0, tx1, ty0, ty1 = P.TSV_BAND; pitch = 0.30; nx = int((tx1-tx0)/pitch); ny = 3
for (n, kind, z0, z1, _) in Ls:
    if kind not in ("bond", "core"): continue
    r, dz = (0.06, z1-z0) if kind == "bond" else (0.02, z1-z0)
    bpy.ops.mesh.primitive_cylinder_add(vertices=12, radius=r, depth=dz,
        location=(tx0+pitch/2, ty0+0.2, (z0+z1)/2))
    c = bpy.context.object; c.name = f"{'ubump' if kind=='bond' else 'TSV'}_{n}"; c.data.materials.append(M["cu"])
    a1 = c.modifiers.new("ax", "ARRAY"); a1.count = nx; a1.use_relative_offset = False
    a1.use_constant_offset = True; a1.constant_offset_displace = (pitch, 0, 0)
    a2 = c.modifiers.new("ay", "ARRAY"); a2.count = ny; a2.use_relative_offset = False
    a2.use_constant_offset = True; a2.constant_offset_displace = (0, 0.3, 0)

# ---- FEM export: Blender 오브젝트의 world bounding box → layer 정의 ----
exp = []
for o in bpy.data.objects:
    if "fem_layer" not in o: continue
    bb = [o.matrix_world @ Vector(c) for c in o.bound_box]
    exp.append(dict(name=o["fem_layer"], kind=o["fem_kind"],
                    x=[min(p.x for p in bb), max(p.x for p in bb)], y=[min(p.y for p in bb), max(p.y for p in bb)],
                    z=[min(p.z for p in bb), max(p.z for p in bb)]))
json.dump(dict(variant=V, height=H, foot=P.FOOT, inset=P.INSET, layers=exp),
          open(f"{OUT}/geometry_{V}.json", "w"), indent=1)

# ---- 장면/렌더 ----
root = bpy.data.objects.new("HBM4_8H", None); sc.collection.objects.link(root)
for o in bpy.data.objects:
    if o is not root and o.type == "MESH": o.parent = root
root.location = (-P.FOOT[0]/2, -P.FOOT[1]/2, 0)
sc.render.engine = "CYCLES"; sc.cycles.device = "CPU"; sc.cycles.samples = 64
sc.cycles.use_denoising = True; sc.render.resolution_x, sc.render.resolution_y = 1600, 1000
sc.render.film_transparent = False
w = bpy.data.worlds.new("w"); sc.world = w; w.use_nodes = True
w.node_tree.nodes["Background"].inputs[0].default_value = (0.92, 0.93, 0.95, 1)
w.node_tree.nodes["Background"].inputs[1].default_value = 0.3
for loc, e in [((20, -25, 30), 4.0), ((-25, 10, 20), 2.0)]:
    L = bpy.data.lights.new("sun", "SUN"); L.energy = e; lo = bpy.data.objects.new("sun", L)
    sc.collection.objects.link(lo); lo.rotation_euler = (Vector((0, 0, 0)) - Vector(loc)).to_track_quat("-Z", "Y").to_euler()
# ground
bpy.ops.mesh.primitive_plane_add(size=200, location=(0, 0, -0.002)); g = bpy.context.object
g.data.materials.append(mat("ground", (0.85, 0.86, 0.88), 0, 0.8))
cam = bpy.data.objects.new("cam", bpy.data.cameras.new("cam")); sc.collection.objects.link(cam); sc.camera = cam
cam.data.lens = 60
def shoot(fn, loc, target=(0, 0, 0.3)):
    cam.location = loc; cam.rotation_euler = (Vector(target)-Vector(loc)).to_track_quat("-Z", "Y").to_euler()
    sc.render.filepath = f"{OUT}/{fn}"; bpy.ops.render.render(write_still=True)

if "--render" in sys.argv:
    shoot(f"render_{V}_true_scale.png", (30, -36, 24), (0, 0, 0.36))      # 실척: 얇은 tile
    # z 6배 확대 + 1/4 절개 (layer 가시화)
    root.scale = (1, 1, 6)
    cutter = box("q_cut", 0, 8, -8, 0, -1, 10, M["emc"], {})  # world 좌표(중심 기준) 1사분면 아래쪽
    for o in list(root.children):
        if o.type != "MESH": continue
        bm = o.modifiers.new("q", "BOOLEAN"); bm.object = cutter; bm.operation = "DIFFERENCE"; bm.solver = "EXACT"
    cutter.hide_render = True
    shoot(f"render_{V}_cutaway_z6.png", (28, -33, 22), (0, 0, 1.6))
    for o in root.children:
        if o.type == "MESH": o.modifiers.remove(o.modifiers["q"])
    # 분해도 (exploded): layer 순서대로 z offset
    order = {n: i for i, (n, *_r) in enumerate(Ls)}
    for o in root.children:
        n = o.get("fem_layer") or o.name.split("_", 1)[-1]
        i = order.get(n, None)
        if o.name.startswith("EMC_Sidewall"): o.hide_render = True; continue
        if i is None and o.name == "PHY_mark": i = 0
        if i is not None: o.location.z += 0.10*i
    shoot(f"render_{V}_exploded.png", (42, -48, 30), (0, 0, 5.5))
bpy.ops.wm.save_as_mainfile(filepath=os.path.abspath(f"{OUT}/HBM4_8H_{V}.blend"))
print("done", V, "H=", H)
