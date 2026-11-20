import pickle, os, math
from solve import *
from fams_desc import D

D["PCH"] = tuple(x.replace("조합 대부분이 실재하지 않는 구성에 'HBM 스택' 이름을 붙였습니다", "조합 대부분이 실재하지 않는 구성인데도 'HBM 스택' 이름을 붙였습니다") for x in D["PCH"])

R, U = pickle.load(open("results.pkl", "rb"))
Q = {q["id"]: (c, q) for c, q in ALL}
OUT = "/home/user/MyOwn/hbm_quiz/docs/reviews/num/"
os.makedirs(OUT, exist_ok=True)
CIRC = "①②③④"


def fmt(v):
    if isinstance(v, tuple):
        return " · ".join(fmt(x) for x in v)
    if isinstance(v, int) or (isinstance(v, float) and abs(v - round(v)) < 1e-9 and abs(v) >= 1):
        return f"{int(round(v)):,}"
    if abs(v) >= 100:
        return f"{v:,.1f}"
    if abs(v) >= 1:
        return f"{v:.3g}" if abs(v) < 10 else f"{v:.4g}"
    return f"{v:.3g}"


def esc(s):
    return str(s).replace("|", "\\|").replace("\n", " ")


# ---- 문항별 추가 판정 ----
INHERENT_LEAK = {"THERM_BASE": "f_therm 이 base 온도 = tTop + ΔT·(n−1) 을 계산해 표시(정답 값 노출)",
                 "HCB_OVL": "f_hcb 가 off_nm·tol_nm 로 초과/이내 판정을 표시(판정 노출)"}
CONV = {"THERM_BASE": "지문·해설 '간극은 die 수보다 하나 적은 N−1 개' — STANDARDS 2.5 위반",
        "THERM_QMAX": "지문·해설 '간극 수는 die 수보다 하나 적은 N−1 개' — STANDARDS 2.5 위반"}

rows = []
for r in R:
    c, q = Q[r["id"]]
    r["dom"] = c
    t = strip(text(q))
    ans_err = None  # (판정, 올바른 값, 권고)
    if r["st"] == "NO_MATCH":
        ans_err = ("보기에 올바른 값 없음", "보기·정답키 수정")
    elif r["st"] == "KEY_WRONG":
        hits = [i for i, o in enumerate(r["ovals"])]
        ans_err = ("정답 키 오류", "정답키 수정")
    elif r["st"] == "MULTI":
        ans_err = ("정답 비유일(같은 값 보기 2개)", "보기 수정")
    # reticle 1.0× 기하 배치
    if r["solver"] == "RETICLE":
        m = g(r"'" + F + r"× reticle'", t); s = g(r"한 변이\s*" + F + r"\s*mm 인 정사각형", t)
        if m == 1.0:
            geo = math.floor(26 / s) * math.floor(33 / s)
            key = optnums(r["opts"][r["a"]])
            if len(key) >= 2 and key[1] != geo:
                r["geo"] = geo
                ans_err = (f"정답 근거 결함 — 26×33 mm 에 {s:g} mm 정사각형은 {math.floor(26/s)}×{math.floor(33/s)} = {geo}개만 배치 가능(키 {int(key[1])}개는 면적 상한)", "지문 수정('면적 기준 상한' 으로) 또는 정답 수정")
    r["ans_err"] = ans_err
    r["realE"] = [x[3:] for x in r["real"] if x.startswith("E:")]
    r["realI"] = [x[3:] for x in r["real"] if x.startswith("I:")]
    lk = list(r["leak"])
    if r["solver"] in INHERENT_LEAK:
        lk.append(INHERENT_LEAK[r["solver"]])
    r["leak2"] = lk
    r["conv"] = CONV.get(r["solver"])
    if r["id"] == "MET-I-0001":
        r["conv"] = "해설 '접합 간극 11곳' — 12단은 접합 12회(STANDARDS 2.5)"
    # 근접 오답 (<3 %)
    close3 = []
    for i in range(4):
        for j in range(i + 1, 4):
            x, y = r["ovals"][i], r["ovals"][j]
            if isinstance(x, (int, float)) and isinstance(y, (int, float)) and max(abs(x), abs(y)) > 0 and i != j:
                if (i == r["a"] or j == r["a"]) and abs(x - y) / max(abs(x), abs(y)) < 0.03 and x != y:
                    close3.append(f"{CIRC[i]} {r['opts'][i]} ↔ {CIRC[j]} {r['opts'][j]}")
    r["close3"] = close3
    rows.append(r)

DOM_FILE = {"TSV": "TSV", "BSP": "BSP", "BUMP": "BUMP", "SAW": "SAW", "COW": "COW", "WARP": "WARP", "THERM": "THERM", "SIP": "SIP",
            "FA": "FA", "PROD": "PROD", "DRAM": "DRAM", "MET": "MET", "MIX": "MIX", "FEOL": "FEOL"}

PPM_FIX = {}


def correct_cell(r):
    """올바른 값 칸."""
    v = r["v"]
    if r["solver"] == "PPM_DISP":
        c, q = Q[r["id"]]; t = strip(text(q))
        tol = g(r"허용치는\s*±\s*" + F, t)
        verdict = "허용치 이내" if v <= tol else "허용치 초과"
        if v == tol:
            verdict = "허용치 경계(= ±tol) — 판정 모호"
        return f"**{fmt(v)} nm · {verdict}**"
    if r["solver"] in ("HCB_OVL", "TC_FAIL"):
        return esc(r["f"].split("→")[-1].strip())
    if r.get("geo"):
        return f"면적 {fmt(v[0])} mm² · 배치 {r['geo']}개 (면적 상한 {v[1]})"
    return f"{fmt(v)} {r['unit']}".strip()


def keytxt(r):
    return f"{CIRC[r['a']]} {esc(r['opts'][r['a']])}"


def write_domain(dom, rs, extra_unsolved):
    fn = OUT + DOM_FILE[dom] + ".md"
    n = len(rs)
    ansE = [r for r in rs if r["ans_err"]]
    realE = [r for r in rs if r["realE"]]
    leak = [r for r in rs if r["leak2"]]
    conv = [r for r in rs if r["conv"]]
    close = [r for r in rs if r["close3"]]
    L = []
    title = {"THERM": "THERM (열 설계 — 13_THERM.json, id 는 WARP-* 유지)"}.get(dom, dom)
    L.append(f"# NUM 수치 계산 검증 — {title}")
    L.append("")
    L.append("- 작성: NUM (수치 계산 검증 지원 에이전트) · 2026-11-20 · 읽기 전용 검증(data 수정 없음)")
    L.append("- 방법: 계산 유형(가족)마다 재계산 스크립트로 전 멤버의 지문 수치를 파싱해 정답을 다시 계산하고, 정답 키·보기 값·반올림·현실 범위(STANDARDS 2.2–2.4)·그림/지표 정답 노출을 기계 대조했습니다. 비가족 문항은 같은 스크립트의 단건 solver 와 손계산으로 확인했습니다. 스크립트: scratchpad `num/solve.py`, `num/run.py`.")
    L.append("- 대상: 발문이 계산을 요구하거나(얼마·몇·구하·환산 등), 보기가 모두 수치이거나, 보기 3개 이상이 수치+단위인 문항, 그리고 k=1 수치 그림으로 판정하는 가족(COW-A-0003·FA-A-0003·WARP-A-0003 계열).")
    L.append("- 심각도: **E** = 정답 오류·정답 비유일·STANDARDS 2.4 위반 비현실 설정(반드시 수정), **I** = 참고·권고.")
    L.append("")
    L.append("## 요약")
    L.append("")
    L.append("| 항목 | 건수 |")
    L.append("|---|---|")
    L.append(f"| 재계산 검증 문항 | {n} |")
    L.append(f"| 정답 키·보기 값 일치(산술) | {sum(1 for r in rs if r['st']=='OK')} |")
    L.append(f"| **정답 오류 확정**(보기에 정답 없음·키 오류·정답 비유일·정답 근거 결함) | **{len(ansE)}** |")
    L.append(f"| **비현실 설정 E**(STANDARDS 2.2/2.4 범위 위반) | **{len(realE)}** |")
    L.append(f"| 그림·지표 정답 노출 | {len(leak)} |")
    L.append(f"| N단↔간극 수 규약 위반(STANDARDS 2.5) | {len(conv)} |")
    L.append(f"| 근접 오답(정답과 3 % 미만 차) | {len(close)} |")
    L.append(f"| 참고(I) 현실성 메모가 있는 문항 | {sum(1 for r in rs if r['realI'])} |")
    if extra_unsolved:
        L.append(f"| 범위 밖(수치 회상형 — 계산 아님, FACT 대상) | {len(extra_unsolved)} |")
    L.append("")
    # 1. 정답 오류
    L.append("## 1. 정답 오류 확정 (문항별)")
    L.append("")
    if not ansE:
        L.append("없음. 산술 정답 키는 전 문항이 재계산 값과 일치합니다.")
    else:
        L.append("| id | 문제 | 올바른 식과 대입 계산 | 올바른 값 | 현재 정답 키 | 권고 |")
        L.append("|---|---|---|---|---|---|")
        for r in ansE:
            prob = r["ans_err"][0]
            if r["solver"] == "PPM_DISP":
                prob = "보기 4개 모두 1,000배 과대(mm→nm 환산 오류)" + ("; 판정도 반대" if "이내" in correct_cell(r) else "")
            if r["solver"] == "WASTE":
                prob = "정답 비유일: '평균 0.0 장' 과 '0 장' 이 같은 값(1장마다 검사 → 자명)"
            if r["solver"] == "STACK_NMAX_A":
                prob = "정답 비유일: 같은 값 보기 2개"
            if r["id"] == "SAW-A-0033":
                prob = "정답 비유일: '약 1개(0.1 %)' 와 '약 1개(0.2 %)' 개수 동일; % 도 연속값 0.31 % 와 불일치"
            if r["id"] == "MET-I-0001":
                prob = "정답 보기 값 72 % 가 계산값(73.9 %; 해설의 11회 적용 시 74.3 %)과 불일치"
            rec = r["ans_err"][1]
            if r["solver"] == "PPM_DISP":
                rec = "보기·정답키·해설 수정 + 설정 수정(D2W die 반경으로)"
            if r["solver"] == "WASTE":
                rec = "삭제 또는 m ≥ 2 로 재작성, '0 장' 보기 교체"
            if r["id"] == "MET-I-0001":
                rec = "보기 수정: '약 74 %' (해설도 접합 12회로)"
            L.append(f"| {r['id']} | {esc(prob)} | {esc(r['f'])} | {correct_cell(r)} | {keytxt(r)} | {rec} |")
    L.append("")
    # 2. 가족 단위
    L.append("## 2. 계산 유형(가족)별 검증 결과")
    L.append("")
    if not rs:
        L.append("이 파일(분할 후 남은 문항)에는 계산형 문항이 없습니다." + (" 열 관련 계산 문항(WARP-* id)은 `THERM.md` 에 있습니다." if dom == "WARP" else ""))
        L.append("")
    by = collections.defaultdict(list)
    for r in rs:
        by[r["solver"]].append(r)
    for sname, lst in sorted(by.items(), key=lambda kv: -len(kv[1])):
        d = D.get(sname, (sname, "", "", ""))
        ok = sum(1 for r in lst if r["st"] == "OK")
        L.append(f"### 2.{list(sorted(by.items(), key=lambda kv: -len(kv[1]))).index((sname, lst))+1} {d[0]} — {len(lst)}문항")
        L.append("")
        L.append(f"- 식: `{d[1]}`")
        L.append(f"- 산술 일치: {ok}/{len(lst)} · 정답 오류 {sum(1 for r in lst if r['ans_err'])} · 비현실 E {sum(1 for r in lst if r['realE'])} · 그림/지표 노출 {sum(1 for r in lst if r['leak2'])} · 근접 오답 {sum(1 for r in lst if r['close3'])}")
        L.append(f"- 판정: {d[2]}")
        L.append(f"- 권고: {d[3]}")
        L.append(f"- 멤버: {', '.join(r['id'] for r in lst)}")
        L.append("")
        # 멤버 표 (E 이슈가 있거나 가족 규모가 작을 때 전부, 아니면 이슈 있는 것만)
        show = [r for r in lst if r["ans_err"] or r["realE"] or r["leak"] or r["close3"] or r["rounding"] or r.get("geo") or r["realI"]]
        if sname in ("PPM_DISP", "THERM_BASE", "THERM_QMAX", "THERM_PTOT", "EM_J", "STACK_NMAX_A", "STACK_NMAX_I", "WASTE", "PCH", "CORE_TMAX", "RETICLE"):
            show = lst
        if show:
            L.append("| id | 올바른 식·대입 | 올바른 값 | 정답 키 | 판정 | 이슈 |")
            L.append("|---|---|---|---|---|---|")
            for r in show:
                iss = []
                if r["ans_err"]:
                    iss.append("**정답 오류**")
                iss += ["**E** " + x for x in r["realE"]]
                iss += ["I " + x for x in r["realI"]]
                if r["leak"]:
                    iss.append("노출 " + ", ".join(r["leak"]))
                if r["close3"]:
                    iss.append("근접 오답 " + "; ".join(r["close3"]))
                if r["rounding"]:
                    iss.append("반올림 " + r["rounding"])
                stt = {"OK": "일치", "NO_MATCH": "불일치", "KEY_WRONG": "키 오류", "MULTI": "정답 2개"}[r["st"]]
                if r.get("geo"):
                    stt = "근거 결함"
                L.append(f"| {r['id']} | {esc(r['f'])} | {correct_cell(r)} | {keytxt(r)} | {stt} | {esc(' / '.join(iss)) or '—'} |")
            L.append("")
    # 3. 노출
    if leak:
        L.append("## 3. 그림·지표 정답 노출 (문항별)")
        L.append("")
        L.append("| id | 노출 위치 | 권고 |")
        L.append("|---|---|---|")
        for r in leak:
            L.append(f"| {r['id']} | {esc('; '.join(r['leak2']))} | 결과값 대신 입력 조건만 그리거나 k=0 (STANDARDS 3.6) |")
        L.append("")
    if conv:
        L.append("## 4. N단↔간극 수 규약 위반")
        L.append("")
        L.append(", ".join(r["id"] for r in conv) + f" — {conv[0]['conv']}. 계산값은 '최상단 core–최하단 core 사이 N−1 간극' 으로 해석하면 성립합니다. 문구를 그 뜻으로 바꾸고 base 까지의 간극(N 개)과 구분해 쓰십시오.")
        L.append("")
    if extra_unsolved:
        L.append("## 5. 범위 밖 — 수치 회상형(계산 아님)")
        L.append("")
        L.append("다음 문항은 보기에 수치가 있지만 계산이 아니라 사실·업체 발표 회상입니다. NUM 재계산 대상이 아니므로 FACT(`docs/reviews/_facts.md`) 판정을 따르십시오: " + ", ".join(extra_unsolved))
        L.append("")
    open(fn, "w").write("\n".join(L) + "\n")
    return dict(n=n, ok=sum(1 for r in rs if r['st'] == 'OK'), ans=len(ansE), realE=len(realE), leak=len(leak), conv=len(conv), close=len(close))


summary = {}
doms = collections.defaultdict(list)
for r in rows:
    doms[r["dom"]].append(r)
uns = collections.defaultdict(list)
for c, i in U:
    uns[c].append(i)
for dom in sorted(set(list(doms) + list(uns))):
    summary[dom] = write_domain(dom, doms.get(dom, []), uns.get(dom, []))
pickle.dump((rows, summary), open("rows.pkl", "wb"))
for k, v in summary.items():
    print(k, v)
