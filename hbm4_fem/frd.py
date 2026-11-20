"""CalculiX .frd(ASCII) / .dat reader."""
import numpy as np
def read_frd(fn):
    """returns list of steps: dict(name -> (node_ids, values[n,ncomp])), with 'time' """
    steps, cur, blk, ids, vals, ncomp = [], None, None, [], [], 0
    def flush():
        if blk is not None and cur is not None:
            cur[blk] = (np.array(ids), np.array(vals))
    with open(fn) as f:
        for line in f:
            if line.startswith("  100C"):
                flush(); blk = None; ids, vals = [], []; newstep = True
            elif line.startswith(" -4"):
                blk = line[5:13].strip()
                if cur is None or blk in cur: cur = {}; steps.append(cur)
            elif line.startswith(" -1") and blk is not None:
                ids.append(int(line[3:13])); s = line[13:].rstrip("\n")
                vals.append([float(s[i*12:(i+1)*12]) for i in range(len(s)//12)])
            elif line.startswith(" -3"):
                flush(); blk = None
    return steps
def read_elprint(fn):
    """.dat *EL PRINT S → list per printed step of array[n,8] (elem, ip, sxx,syy,szz,sxy,sxz,syz)"""
    txt = open(fn).read(); out = []
    for ch in txt.split("stresses (elem")[1:]:
        body = ch.split("\n\n")[1]
        out.append(np.fromstring(body.replace("\n", " "), sep=" ").reshape(-1, 8))
    return out
