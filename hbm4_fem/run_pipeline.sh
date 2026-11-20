#!/usr/bin/env bash
# HBM4-8H: Blender 모델링 → 구조격자 mesh → CalculiX 열해석 → 열-구조 해석 → 후처리/렌더
set -e; cd "$(dirname "$0")"; mkdir -p out figs
VARS="A_MRMUF B_TCNCF C_MRMUF_CAP"
for v in $VARS; do python3 blender_build.py $v out --render; done   # Blender: .blend, 렌더, geometry_*.json
python3 run_all.py $VARS                                            # mesh + ccx(thermal) + ccx(mech, OMP=1)
for v in $VARS; do python3 post.py $v; done
python3 compare.py
for v in $VARS; do for f in T_op w_25 vm_25; do python3 blender_results.py $v $f 400; done; done
python3 diff_pair.py A_MRMUF D_MID47
