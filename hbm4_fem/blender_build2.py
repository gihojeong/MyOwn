"""v2: stack.py 케이스로 Blender 모델 생성 → .blend + 렌더(z 과장 1/4 절개).
usage: python3 blender_build2.py <gen> <nh> [set] [--render]"""
import sys, os, math, bpy
from mathutils import Vector
import stack as S
gen, nh = sys.argv[1], int(sys.argv[2]); st = sys.argv[3] if len(sys.argv) > 3 and not sys.argv[3].startswith("--") else "design"
c = S.case(gen, nh, st); TAG = f"{gen.upper()}_{nh}H_{st}"; OUT = "out2"; ZS = 8.0
bpy.ops.wm.read_factory_settings(use_empty=True); sc = bpy.context.scene
def mat(n, rgb, metal=0., rough=.4):
    m = bpy.data.materials.new(n); m.use_nodes = True; b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*rgb, 1); b.inputs["Metallic"].default_value = metal; b.inputs["Roughness"].default_value = rough
    return m
M = {"si": mat("Si", (.20, .23, .32), .45, .3), "si_base": mat("Si_base", (.14, .17, .25), .45, .3), "si_top": mat("Si_top", (.20, .23, .32), .45, .3),
     "beol": mat("BEOL", (.80, .45, .20), .9, .3), "gap": mat("NCF", (.25, .65, .40), 0, .5), "emc": mat("EMC", (.03, .03, .035), 0, .35)}
root = bpy.data.objects.new("HBM", None); sc.collection.objects.link(root)
def box(n, x0, x1, y0, y1, z0, z1, m):
    bpy.ops.mesh.primitive_cube_add(size=1, location=((x0+x1)/2, (y0+y1)/2, ZS*(z0+z1)/2)); o = bpy.context.object
    o.name = n; o.scale = (x1-x0, y1-y0, ZS*(z1-z0)); bpy.ops.object.transform_apply(scale=True); o.data.materials.append(m); o.parent = root; return o
for (n, k, z0, z1, h) in S.layers(c):
    if k == "emc":
        hd = S.L_DRAM/2   # 링 = 4 slab
        for i, (a, b, cc, d) in enumerate([(-h, h, -h, -hd), (-h, h, hd, h), (-h, -hd, -hd, hd), (hd, h, -hd, hd)]):
            box(f"EMC_{i}", a, b, cc, d, z0, z1, M["emc"])
    else: box(n, -h, h, -h, h, z0, z1, M[k])
bpy.ops.wm.save_as_mainfile(filepath=os.path.abspath(f"{OUT}/HBM_{TAG}.blend"))
if "--render" in sys.argv:
    cut = box("cut", 0, 8, -8, 0, -1, 2, M["emc"]); cut.hide_render = True
    for o in list(root.children):
        if o is cut or o.type != "MESH": continue
        bm = o.modifiers.new("q", "BOOLEAN"); bm.object = cut; bm.operation = "DIFFERENCE"; bm.solver = "EXACT"
    sc.render.engine = "CYCLES"; sc.cycles.device = "CPU"; sc.cycles.samples = 64; sc.cycles.use_denoising = True
    sc.render.resolution_x, sc.render.resolution_y = 1600, 1000
    w = bpy.data.worlds.new("w"); sc.world = w; w.use_nodes = True
    w.node_tree.nodes["Background"].inputs[0].default_value = (.92, .93, .95, 1); w.node_tree.nodes["Background"].inputs[1].default_value = .35
    L = bpy.data.lights.new("s", "SUN"); L.energy = 3.5; lo = bpy.data.objects.new("s", L); sc.collection.objects.link(lo); lo.rotation_euler = (.7, .2, .9)
    bpy.ops.mesh.primitive_plane_add(size=200, location=(0, 0, -.01))
    cam = bpy.data.objects.new("c", bpy.data.cameras.new("c")); sc.collection.objects.link(cam); sc.camera = cam; cam.data.lens = 60
    cam.location = (22, -26, 17); cam.rotation_euler = (Vector((0, 0, ZS*c["tot"]/2)) - cam.location).to_track_quat("-Z", "Y").to_euler()
    sc.render.filepath = os.path.abspath(f"{OUT}/render_{TAG}_cut_z{int(ZS)}.png"); bpy.ops.render.render(write_still=True)
print("ok", TAG, "topSi=%.1f" % (S.top_si(c)*1e3))
