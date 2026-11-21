import pickle
from solve import *

EXTRA_FAM = set()
famidx = collections.defaultdict(list)
for c, q in ALL:
    famidx[(c, fam(q))].append(q["id"])
for c, q in ALL:
    if q["id"] in ("COW-A-0003", "FA-A-0003", "WARP-A-0003", "COW-A-0043"):
        EXTRA_FAM.update(famidx[(c, fam(q))])

TARGET = [(c, q) for c, q in ALL if is_calc3(q) or q["id"] in EXTRA_FAM]


def matches(ov, v, o, tol):
    if ov is None or v is None:
        return False
    if isinstance(v, tuple):
        if not isinstance(ov, tuple) or len(ov) < len(v):
            return False
        return all(matches(a, b, o, tol) for a, b in zip(ov, v))
    if v == 0:
        return abs(ov) < 1e-9
    d = decimals(o)
    rnd = 0.5 * 10 ** (-d) * 1.05
    rel = abs(ov - v) / abs(v)
    if tol is not None:
        return abs(ov - v) <= rnd or rel <= tol
    return abs(ov - v) <= rnd or rel <= 0.01


def strict_round_ok(ov, v, o):
    if isinstance(v, tuple):
        return all(strict_round_ok(a, b, o) for a, b in zip(ov, v))
    d = decimals(o)
    return abs(ov - v) <= 0.5 * 10 ** (-d) * 1.0001 + 1e-12


def flatnums(obj):
    out = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k in ("flag", "note", "bullet", "title"):
                continue
            out += [(k, x) for _, x in flatnums(v)] if not isinstance(v, (int, float)) else [(k, v)]
    elif isinstance(obj, list):
        for v in obj:
            out += flatnums(v)
    elif isinstance(obj, (int, float)) and not isinstance(obj, bool):
        out.append(("", obj))
    return out


results = []
unsolved = []
for c, q in TARGET:
    t = strip(text(q))
    res = None; sname = None
    for name, doms, pat, fn in SOLVERS:
        if c in doms and pat.search(t):
            try:
                res = fn(t, q)
            except Exception as e:
                res = None
                print("ERR", q["id"], name, e, file=sys.stderr)
            if res:
                sname = name
                break
    if not res:
        unsolved.append((c, q))
        continue
    pick = res["pick"] or (lambda o: (optnums(o)[0] if optnums(o) else None))
    ovals = []
    for o in q["opts"]:
        try:
            ovals.append(pick(o))
        except Exception:
            ovals.append(None)
    v = res["v"]
    ms = [ov is not None and not isinstance(v, tuple) and not isinstance(ov, tuple) and strict_round_ok(ov, v, o) for ov, o in zip(ovals, q["opts"])]
    if isinstance(v, tuple):
        ms = [isinstance(ov, tuple) and len(ov) >= len(v) and strict_round_ok(ov, v, o) for ov, o in zip(ovals, q["opts"])]
    ml = [matches(ov, v, o, res["tol"]) for ov, o in zip(ovals, q["opts"])]
    m = ms if any(ms) else ml
    if res.get("exact"):
        m = [ov is not None and abs(ov - v) < 1e-6 for ov in ovals]
    if res["judge"]:
        # judgement text must also agree
        m = [mm and (res["judge"] in o) if ovals[i] is not None else (res["judge"] in o) for i, (mm, o) in enumerate(zip(m, q["opts"]))]
        if res["pick"] and all(x is None for x in ovals):
            m = [res["judge"] in o for o in q["opts"]]
            if sum(m) > 1:
                m = [False] * 4
    a = q["a"]
    hits = [i for i, x in enumerate(m) if x]
    if m[a] and len(hits) == 1:
        st = "OK"
    elif m[a]:
        st = "MULTI"
    elif hits:
        st = "KEY_WRONG"
    else:
        st = "NO_MATCH"
    if res["judge"] and all(x is None for x in ovals):
        st = "OK" if m[a] and len(hits) == 1 else ("NO_MATCH" if not hits else ("KEY_WRONG" if not m[a] else "MULTI"))
    if sname in ("HCB_OVL", "TC_FAIL"):
        key = q["opts"][a]
        out = res["judge"] == "벗어"
        keyout = "벗어" in key
        cands = [i for i, o in enumerate(q["opts"]) if (("벗어" in o) == out) and ("배율" in o if sname == "HCB_OVL" else "HTS" in o)]
        st = "OK" if keyout == out and a in cands and len(cands) == 1 else ("KEY_WRONG" if cands else "NO_MATCH")
    rounding = None
    if st == "OK" and ovals[a] is not None and not isinstance(v, tuple) and not strict_round_ok(ovals[a], v, q["opts"][a]):
        rounding = f"표시 {q['opts'][a]} vs 계산 {v:.4g}"
    # distinctness
    close = []
    nv = [x for x in ovals if isinstance(x, (int, float))]
    for i in range(4):
        for j in range(i + 1, 4):
            x, y = ovals[i], ovals[j]
            if isinstance(x, (int, float)) and isinstance(y, (int, float)) and max(abs(x), abs(y)) > 0:
                if abs(x - y) / max(abs(x), abs(y)) < 0.10:
                    close.append((i, j, x, y))
            elif isinstance(x, tuple) and isinstance(y, tuple) and x == y:
                close.append((i, j, x, y))
    # figure / metrics leak
    leak = []
    stemnums = set(round(x, 6) for x in optnums(t))
    keyv = v if not isinstance(v, tuple) else None
    if keyv is not None and ovals[a] is not None and not isinstance(ovals[a], tuple):
        targetvals = {round(ovals[a], 6), round(keyv, 6)}
        fp = q.get("fig", [None, {}])[1] if isinstance(q.get("fig"), list) else {}
        WL = {"TSV_AR": {"ar"}, "EM_J": {"j_kA"}, "IMC_KT": {"imc_um"}, "IMC_FWD": {"imc_um"}, "IMC_INV": {"hours"},
              "STACK_H": {"h_um"}, "STACK_H16": {"h_um"}, "STACK_NMAX_A": {"n", "h_um"}, "STACK_NMAX_I": {"n", "h_um"}, "CORE_TMAX": set(),
              "THERM_QMAX": {"q_Wmm2"}}.get(sname, set())
        for k, x in flatnums(fp):
            if k not in WL:
                continue
            if any(abs(x - tv) <= max(0.011 * abs(tv), 1e-9) for tv in targetvals if tv != 0):
                leak.append(f"fig.{k}={x}")
        for mt in q.get("metrics") or []:
            vals = optnums(str(mt[2]))
            for x in vals:
                if round(x, 6) in stemnums:
                    continue
                if any(abs(x - tv) <= max(0.011 * abs(tv), 1e-9) for tv in targetvals if tv != 0):
                    leak.append(f"metrics[{mt[1]}]={mt[2]}")
    results.append(dict(id=q["id"], code=c, lv=q["lv"], solver=sname, st=st, a=a, ovals=ovals, opts=q["opts"], v=v, unit=res["unit"], f=res["f"],
                        real=res["real"], close=close, leak=leak, rounding=rounding, note=res.get("note"), fam=fam(q), k=q["k"], fig=q.get("fig")))

pickle.dump((results, [(c, q["id"]) for c, q in unsolved]), open("results.pkl", "wb"))
cnt = collections.Counter((r["code"], r["st"]) for r in results)
print("solved", len(results), "unsolved", len(unsolved))
for k in sorted(cnt):
    print(k, cnt[k])
uc = collections.Counter(c for c, q in unsolved)
print("unsolved by code", uc)
