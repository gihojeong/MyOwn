#!/usr/bin/env python3
"""Pack data/*.json into template.html -> dist/HBM_quiz.html.

Per-question records are denormalized (inline fig/metrics/ctx) so domain agents can
edit their own file independently. This script re-normalizes (dedupes figs, metrics,
contexts) and embeds the raw-deflate + base64 blob the page expects.
Usage: python3 tools/build.py [--out dist/HBM_quiz.html]
"""
import base64, glob, json, os, sys, zlib

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def load():
    meta = json.load(open(os.path.join(ROOT, "data/_meta.json"), encoding="utf8"))
    files = sorted(f for f in glob.glob(os.path.join(ROOT, "data/[0-9]*.json")))
    doms, per = [], []
    for f in files:
        d = json.load(open(f, encoding="utf8"))
        doms.append(d["domain"])
        per.append(d["questions"])
    return meta, doms, per


def pack(meta, doms, per):
    figs, fidx, mets, midx, ctx, cidx = [], {}, [], {}, [], {}
    join = meta["join"]
    out = []

    def intern(v, lst, idx):
        k = json.dumps(v, ensure_ascii=False, sort_keys=True)
        if k not in idx:
            idx[k] = len(lst)
            lst.append(v)
        return idx[k]

    for di, qs in enumerate(per):
        for q in qs:
            r = {"lv": q["lv"], "title": q["title"]}
            if q.get("stem") is not None:
                r["stem"] = q["stem"]
            else:
                r["c"] = intern(q["ctx"], ctx, cidx)
                if q.get("j"):
                    r["j"] = q["j"]
                r["qt"] = q["qt"]
            r["opts"] = q["opts"]
            r["a"] = q["a"]
            r["exp"] = q["exp"]
            r["f"] = intern(q["fig"], figs, fidx)
            r["m"] = [intern(m, mets, midx) for m in q["metrics"]]
            r["d"] = di
            r["k"] = q.get("k", 0)
            r["id"] = q["id"]
            if q.get("src"):
                r["src"] = q["src"]
            out.append(r)
    return {"ctx": ctx, "join": join, "q": out, "figs": figs, "mets": mets, "doms": doms}


def main():
    out = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else os.path.join(ROOT, "dist/HBM_quiz.html")
    meta, doms, per = load()
    db = pack(meta, doms, per)
    raw = json.dumps(db, ensure_ascii=False, separators=(",", ":")).encode("utf8")
    co = zlib.compressobj(9, zlib.DEFLATED, -15)
    b64 = base64.b64encode(co.compress(raw) + co.flush()).decode()
    tpl = open(os.path.join(ROOT, "template.html"), encoding="utf8").read()
    assert tpl.count("__DB_B64__") == 1
    html = tpl.replace("__DB_B64__", b64).replace("__DB_LEN__", str(len(raw)))
    os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out, "w", encoding="utf8").write(html)
    n = len(db["q"])
    print(f"built {out}: {n} questions, {len(db['figs'])} figs, {len(db['mets'])} mets, {len(html)/1e6:.2f} MB")


if __name__ == "__main__":
    main()
