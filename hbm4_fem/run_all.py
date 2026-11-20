"""variant별: mesh → 열해석(ccx) → 온도장 매핑 → 열-구조(ccx). usage: python3 run_all.py A_MRMUF ..."""
import sys, os, subprocess, time
from frd import read_frd
OUT = "out"; env = dict(os.environ, OMP_NUM_THREADS="1")
for V in sys.argv[1:]:
    t0 = time.time()
    subprocess.run(["python3", "mesh_inp.py", V, OUT], check=True)
    subprocess.run(["ccx", "-i", f"thermal_{V}"], cwd=OUT, env=env, check=True, stdout=open(f"{OUT}/thermal_{V}.log", "w"))
    ids, T = read_frd(f"{OUT}/thermal_{V}.frd")[-1]["NDTEMP"]
    open(f"{OUT}/optemp_{V}.inc", "w").write("\n".join(f"{i},{t[0]:.4f}" for i, t in zip(ids, T)))
    print(V, "thermal Tmax=%.2f" % T.max(), "%.0fs" % (time.time()-t0), flush=True)
    subprocess.run(["ccx", "-i", f"mech_{V}"], cwd=OUT, env=env, check=True, stdout=open(f"{OUT}/mech_{V}.log", "w"))
    print(V, "mech done %.0fs" % (time.time()-t0), flush=True)
