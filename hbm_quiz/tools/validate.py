#!/usr/bin/env python3
"""HBM quiz item validator (EA 소유).

docs/agents/STANDARDS.md 의 규칙 중 기계 판정이 가능한 것을 검사한다.

사용법
  python3 tools/validate.py                      # 전 분야 검사 → docs/reviews/_auto_latest.md
  python3 tools/validate.py --domain TSV         # 한 분야만, 문항별 이슈를 stdout 에 출력
  python3 tools/validate.py --domain TSV --codes E_EXP_SHORT,W_OPT_ODD_END
  python3 tools/validate.py --out docs/reviews/_auto_baseline.md
  python3 tools/validate.py --json issues.json   # 기계 판독용 전체 이슈
  python3 tools/validate.py --domain TSV --gate  # 분야 에이전트 완료 게이트 (차단 E 0건이면 exit 0; PHASE2_E 는 제외)

심각도
  E  = 반드시 수정 (게이트 차단)
  W  = 검토 후 수정 또는 사유 기록 (문항에 "vx": ["W_CODE", ...] 로 면제 가능, 사유는 docs/reviews/CODE.md)
  I  = 참고 (EA 일괄 처리 대상이거나 사실 확인 필요 표시)

문항 단위 면제: 레코드에 "vx": ["E_K1_FIG_NUM", ...] 를 두면 해당 코드는 집계에서 제외된다
(E 코드 면제는 E_K1_FIG_NUM, E_FAMILY_OVER 처럼 휴리스틱 판정인 것만 허용 — WAIVABLE_E 참조).
"""
import argparse, collections, glob, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LV_NAME = {"B": "초급", "I": "중급", "A": "고급"}
CIRC = "①②③④"
# EA 가 Phase 2 에서 일괄 처리하는 E 코드: 보고는 하되 분야 에이전트 게이트(--gate)는 막지 않는다.
PHASE2_E = {"E_JOSA_CIRC"}
WAIVABLE_E = {"E_K1_FIG_NUM", "E_FAMILY_OVER", "E_CALC_NO_WORK", "E_STYLE_PLAIN", "E_EXP_REF_ANSWER", "E_FIG_TOPIC"}

# ───────────────────────── 그림 템플릿 스키마 ─────────────────────────
# keys: template.html 이 읽는 params. q: 그림에 수치로 그려지는 키(k=1 이면 지문과 일치해야 함)
FIG = {
    "f_tsv": dict(keys="ar depth_um dia_um fill scallop scallopPitch scallopDepth barrier overburden taper hideResult note flag hideLabels",
                  q="ar depth_um dia_um", enums={"fill": ["good", "void", "seam", "pinch"]}),
    "f_cmp": dict(keys="nA nB densA densB dish_nm erosion_nm note flag hideLabels", q="densA densB dish_nm erosion_nm"),
    "f_bs": dict(keys="step defect ox1 sin ox2 ni_um notes note flag", q="ox1 sin ox2",
                 enums={"defect": ["none", "undercut", "residue"], "step": list(range(8))}),
    "f_bump": dict(keys="imc_um pillar_um solder_um niBarrier kirkendall em j_kA temp k hours tmax ymax hideLabels hideResult bullet note flag",
                   q="imc_um pillar_um solder_um temp"),
    "f_saw": dict(keys="method kerf_um haz_um chip_um notes bullet note flag", q="kerf_um",
                  enums={"method": ["blade", "lg", "stealth", "plasma", "deeplaser", "dbg"]}),
    "f_bond": dict(keys="method pitch_um gap_um voids filler_trap nonwet dish bullet note flag hideTable hideNotes", q="pitch_um gap_um",
                   enums={"method": ["ncf", "mrmuf", "hcb"]}),
    "f_warp": dict(keys="ref sign mag_um temp tg hideNames hideResult note flag", q="mag_um tg",
                   enums={"ref": ["bump-down", "beol-up"], "sign": [1, -1]}),
    "f_sip": dict(keys="type nHBM lines msg bullet note flag", q="nHBM",
                  enums={"type": ["cowos-s", "cowos-r", "cowos-l", "emib", "emib-t"], "nHBM": [1, 2, 3, 4, 5, 6, 7, 8]}),
    "f_therm": dict(keys="n core q_Wmm2 tTop limit layers hideResult note flag", q="n q_Wmm2 tTop limit"),
    "f_fa": dict(keys="tech depth hot fov_um dz zpeak feats note flag", q="",
                 enums={"tech": ["lit", "obirch", "eotpr", "xrm"]}),
    "f_rel": dict(keys="seq cur fails crit hint xlab xmax ymax tcCycles bullet note flag", q="crit"),
    "f_stack": dict(keys="n highlight gap_um h_um limit_um hideResult bullet note flag hideFormula", q="n gap_um h_um limit_um",
                    enums={"highlight": [None, "height", "midcore", "base", "gap", "topcore"]}),
    "f_hcb": dict(keys="pitch_um tol_nm off_nm dish_nm hideResult bullet note flag", q="pitch_um tol_nm off_nm dish_nm"),
    "f_plot": dict(keys="title x y series marks bullets note flag", q=""),
    "f_film": dict(keys="layers roles bullets flags note flag", q=""),
    "f_note": dict(keys="title points ask flag", q=""),
    "f_table": dict(keys="title unit cols rows hl hlRow hlCol notes note flag", q=""),
    "f_wafermap": dict(keys="title grid values pattern scale bin marks bullets seed note flag", q="",
                       enums={"pattern": ["edge", "center", "ring", "notch", "random", "quadrant"]}),
}
for v in FIG.values():
    v["keys"] = set(v["keys"].split())
    v["q"] = set(v["q"].split())
    v.setdefault("enums", {})

# k=1 에서 해당 수치가 '지문에 등장하는 물리량' 인지 판단하는 문맥어. 문맥어가 지문에 있는데 그림 값이
# 지문 숫자에 없으면 불일치(E), 문맥어가 없으면 '지문에 없는 추가 수치'(W).
K1_CTX = {
    ("f_tsv", "depth_um"): r"깊이|길이|두께", ("f_tsv", "dia_um"): r"직경|지름|Ø",
    ("f_cmp", "densA"): r"density|밀도", ("f_cmp", "densB"): r"density|밀도",
    ("f_cmp", "dish_nm"): r"dishing|파였|함몰", ("f_cmp", "erosion_nm"): r"erosion|낮아|내려",
    ("f_bs", "ox1"): r"SiO", ("f_bs", "sin"): r"SiN", ("f_bs", "ox2"): r"희생|SiO",
    ("f_bump", "imc_um"): r"IMC", ("f_bump", "pillar_um"): r"pillar.{0,10}(높이|두께)", ("f_bump", "solder_um"): r"solder.{0,10}(높이|두께)",
    ("f_bump", "temp"): r"°C", ("f_saw", "kerf_um"): r"kerf|절단 폭|scribe",
    ("f_bond", "pitch_um"): r"pitch|피치", ("f_bond", "gap_um"): r"간극|gap",
    ("f_warp", "mag_um"): r"warpage|변위|휨", ("f_warp", "tg"): r"Tg|유리 전이|glass",
    ("f_sip", "nHBM"): r"HBM\s?\d+\s?(개|stack|스택)|\d+\s?(개|stack|스택)의? HBM",
    ("f_therm", "n"): r"\d+\s?단|\d+-?high", ("f_therm", "q_Wmm2"): r"W/mm|W/cm|열유속",
    ("f_therm", "tTop"): r"°C", ("f_therm", "limit"): r"상한|한계|이하",
    ("f_rel", "crit"): r"판정|기준",
    ("f_stack", "n"): r"\d+\s?단|\d+-?high|core die\s?\d+", ("f_stack", "gap_um"): r"간극|gap",
    ("f_stack", "h_um"): r"높이", ("f_stack", "limit_um"): r"상한|규격",
    ("f_hcb", "pitch_um"): r"pitch|피치", ("f_hcb", "tol_nm"): r"허용|±", ("f_hcb", "off_nm"): r"어긋|오차|overlay|정렬",
    ("f_hcb", "dish_nm"): r"dishing|recess|함몰",
}
# 지문이 특정 공법·기법을 지칭하는데 그림이 다른 것을 그리면 주제 불일치
TOPIC_KW = {
    "f_fa": {"tech": {"lit": r"lock-?in|LIT\b|thermograph", "obirch": r"OBIRCH", "eotpr": r"EOTPR|TDR", "xrm": r"X-?ray|XRM|CT\b|tomograph"}},
    "f_saw": {"method": {"stealth": r"stealth", "plasma": r"plasma", "dbg": r"DBG|dicing before grinding|half-?cut",
                         "lg": r"laser groov|grooving", "deeplaser": r"full-?cut laser|deep laser|레이저 풀컷", "blade": r"blade|블레이드"}},
    "f_bond": {"method": {"ncf": r"NCF", "mrmuf": r"MR-?MUF|MUF", "hcb": r"hybrid|HCB|하이브리드"}},
    "f_sip": {"type": {"cowos-s": r"CoWoS-S", "cowos-r": r"CoWoS-R", "cowos-l": r"CoWoS-L", "emib-t": r"EMIB-T", "emib": r"EMIB(?!-T)"}},
}
WEAK_OPT = re.compile(r"(규정으로|규정에|규칙으로 정해|관행|장비 일정|장비가 비어|장비가 하나|재고|가격이 비싸|비용이 (가장 )?(저렴|싸)|색상|외관|포장|무게가|기록을 남기|기록 때문|보관 때문|작업자|담당 조직|조직이|일정을 맞|시장 점유율|발표 횟수|소음)")
META_METRIC_LABELS = {"난이도", "묻는 것", "세부 주제", "핵심어"}
PARTICLES = ["으로", "에서", "에게", "부터", "까지", "처럼", "보다", "은", "는", "이", "가", "을", "를", "의", "에", "와", "과", "로", "도", "만"]
STOP = set("이 그 저 것 수 등 및 또는 때 위 중 더 각 한 두 세 있다 없다 한다 된다 하는 되는 있는 없는 대한 위한 통해 따라 경우 가장 무엇 무엇입니까 다음 판단 적절한 옳은 것은 것을 이유는 이유".split())
ABSOLUTE = re.compile(r"(항상|절대|전혀|반드시|무조건|오직|어떤 경우에도|100\s?%|완전히 무관|만으로 충분)")
NEG_WORDS = re.compile(r"(틀|아니|아닙니다|반대|무관|과장|오류|거리가 멀|맞지 않|맞지않|근거가 없|해당하지 않|관계없|잘못|사실과 다|부적절|설명하지 못|모순|배제)")
POS_WORDS = re.compile(r"(정답|옳|맞습니다|타당합니다|적절합니다)")
CALC_Q = re.compile(r"(얼마|몇\s?(장|개|배|%|퍼센트|µm|nm|°C|시간|cycle)|계산|구하|환산|추정하면|산출|몇 단|최대 core die 수)")
CALC_WORK = re.compile(r"(=|×|÷|\*|/|√|≈|곱|나누|빼|더하|합은|차는|비례)")
PLACEHOLDER = re.compile(r"(\bundefined\b|\bNaN\b|\bNone\b|\bnull\b|\bTODO\b|\bTBD\b|XXX|\?\?|\{[a-z_]+\}|[Ll]orem)")
DOUBLE_Q = re.compile(r"(라고? 하는가|인가|는가|을까|ㄹ까|인지)\s*(무엇|어느 것|얼마)입니까")
PLAIN_END = re.compile(r"(?<![니])(다|이다|한다|된다|있다|없다|않다|크다|작다|같다|높다|낮다)\.(?=\s|$)")
FACT_WATCH = [
    (re.compile(r"HBM3E[^.。]{0,50}JEDEC|JEDEC[^.。]{0,50}HBM3E"), "HBM3E 를 JEDEC 표준 세대처럼 기술 (HBM3E 는 JESD238 계열 확장·업체 사양, 수치 출처 확인)"),
    (re.compile(r"HBM4[^.。]{0,40}1,?024\s?-?\s?(bit|비트)|1,?024\s?-?\s?(bit|비트)[^.。]{0,20}HBM4"), "HBM4 와 1024-bit 동시 언급 (JESD270-4: 2048-bit)"),
    (re.compile(r"HBM4[^.。]{0,60}(16|8)\s?(개 )?채널|(16|8)\s?(개 )?채널[^.。]{0,30}HBM4"), "HBM4 채널 수 (JESD270-4: 32 채널 · 64 pseudo channel)"),
    (re.compile(r"HBM3[^E4][^.。]{0,60}(8)\s?(개 )?채널"), "HBM3 채널 수 (JESD238: 16 채널 · 32 pseudo channel)"),
    (re.compile(r"(9\.2|9\.6|9\.8|10|11|12)\s?Gb/s[^.。]{0,40}(JEDEC|표준)"), "핀 속도 수치를 JEDEC 값으로 기술 (HBM3 6.4, HBM4 8 Gb/s 가 JEDEC 기준; 그 이상은 업체 사양)"),
    (re.compile(r"(720|775)\s?µm"), "패키지 높이 (HBM3/3E 720 µm, HBM4 775 µm) — 세대와 일치하는지 확인"),
    (re.compile(r"JES?D\s?\d+[A-Z\-\d]*|J-STD-\d+"), "표준 문서 번호 — 번호·조건이 정확한지 확인"),
    (re.compile(r"(TB/s|GB/s)"), "대역폭 수치 — 폭 × 속도 ÷ 8 과 일치하는지 확인"),
]

# 영문 용어의 한글 독음 받침 유무 (1=받침 있음 → 이/은/을/과, 0=없음 → 가/는/를/와). 독음이 갈리는 용어는 넣지 않는다.
EN_BATCHIM = {"void": 0, "kerf": 0, "warpage": 0, "residue": 0, "delamination": 1, "crack": 1, "short": 0, "open": 1,
              "seed": 0, "bump": 0, "pitch": 0, "coverage": 0, "underfill": 1, "imc": 0, "tsv": 0, "cmp": 0, "ncf": 0,
              "die": 0, "wafer": 0, "seam": 1, "scallop": 1, "dishing": 1, "erosion": 1, "reflow": 0, "chipping": 1,
              "pad": 0, "pillar": 0, "solder": 0, "flux": 0, "barrier": 0, "liner": 0, "interposer": 0, "entrapment": 0,
              "non-wet": 1, "non-bonding": 1, "bonding": 1, "overlay": 0, "bridge": 0, "dicing": 1, "stress": 0,
              "tape": 0, "glue": 0, "debonding": 1, "reveal": 1, "hcb": 0, "kgd": 0, "leakage": 0, "retention": 1,
              "refresh": 0, "channel": 1, "buffer": 0, "base": 0, "hbm": 1, "dram": 1, "tg": 0, "emc": 0, "muf": 0,
              "tcb": 0, "sicn": 1, "smile": 1, "cry": 0, "lid": 0, "tim": 1, "ecc": 0, "phy": 0}
EN_JOSA = re.compile(r"(?<![A-Za-z])([A-Za-z][A-Za-z\-]*)\s?(이|가|은|는|을|를|과|와)(?=[\s,.)])")
TOK = re.compile(r"[A-Za-z][A-Za-z0-9\-/]*|\d+(?:\.\d+)?|[가-힣]+")
NUM = re.compile(r"(?<![A-Za-z])[-−]?\d[\d,]*(?:\.\d+)?")


JOSA_SPACE_RX = re.compile(r"[A-Za-z0-9)%µ°] (가|이|는|은|를|을|의|에|와|과|로|으로|에서|에는|에도|까지|부터|보다|처럼|만|도)(?=[\s,.)])")
FORMULA_TAIL = re.compile(r"[=≈×÷][^가-힣]*$")


def josa_space_hits(text):
    """영문·숫자 + 공백 + 조사. 단, 직전 한글 이후 구간에 = ≈ × ÷ 가 있으면(수식 바로 뒤) 예외 —
    LAYOUT_RULES §2 · STANDARDS 3.4 의 '수식과 한글은 띄어 쓴다' 규칙. Phase 2 정규화도 이 함수 기준."""
    out = []
    for m in JOSA_SPACE_RX.finditer(text or ""):
        if FORMULA_TAIL.search(text[:m.start() + 1]):
            continue
        out.append(m)
    return out


def strip_particle(t):
    for p in PARTICLES:
        if len(t) > len(p) + 1 and t.endswith(p):
            return t[: -len(p)]
    return t


def toks(s):
    out = []
    for t in TOK.findall(s or ""):
        t = strip_particle(t.lower())
        if len(t) >= 2 and t not in STOP:
            out.append(t)
    return out


def nums(s):
    out = set()
    for m in NUM.findall(s or ""):
        try:
            v = float(m.replace(",", "").replace("−", "-"))
        except ValueError:
            continue
        out.add(round(v, 6))
    return out


def stem_of(q, join):
    if q.get("stem") is not None:
        return q["stem"]
    j = q.get("j") or 0
    jj = join[j] if 0 <= j < len(join) else ""
    return (q.get("ctx") or "") + jj + (q.get("qt") or "")


def core_of(q):
    """중복 판정용 핵심 텍스트: 공유 ctx 는 제외한다."""
    return q.get("stem") if q.get("stem") is not None else (q.get("qt") or "")


def norm(s):
    s = (s or "").lower()
    s = re.sub(r"\d", "0", s)
    return re.sub(r"[\s\W_]+", "", s)


def normx(s):
    return re.sub(r"[\s\W_]+", "", (s or "").lower())


def fam_key(s):
    s = re.sub(r"[\d.,]+", "#", s or "")
    return re.sub(r"\s+", "", s)


def leaves(v):
    """fig params 안의 모든 문자열/숫자 리프."""
    if isinstance(v, dict):
        for x in v.values():
            yield from leaves(x)
    elif isinstance(v, list):
        for x in v:
            yield from leaves(x)
    else:
        yield v


# ───────────────────────── 문항 단위 검사 ─────────────────────────
def check_item(q, code, join, issues, legacy=()):
    def add(c, msg=""):
        if c in set(q.get("vx") or []) and (c[0] != "E" or c in WAIVABLE_E):
            return
        issues.append({"id": q.get("id", "?"), "d": code, "lv": q.get("lv", "?"), "code": c, "msg": msg})

    # 스키마
    req = ["id", "lv", "title", "opts", "a", "exp", "k", "fig", "metrics"]
    for f in req:
        if f not in q:
            add("E_SCHEMA_MISSING", f)
    if any(f not in q for f in req):
        return
    if q.get("stem") is None and not (q.get("ctx") and q.get("qt")):
        add("E_SCHEMA_STEM", "stem 또는 ctx+qt 필요")
    if q.get("stem") is not None and (q.get("ctx") or q.get("qt")):
        add("E_SCHEMA_STEM", "stem 과 ctx/qt 동시 존재")
    if q["lv"] not in LV_NAME:
        add("E_SCHEMA_LV", q["lv"])
    m = re.fullmatch(r"([A-Z]+)-([BIA])-(\d{4})", str(q["id"]))
    if not m:
        add("E_ID_FORMAT", q["id"])
    else:
        if m.group(1) != code and m.group(1) not in legacy:
            add("E_ID_FORMAT", "분야 코드 불일치 (이관 문항이면 파일의 legacy_prefix 에 원 코드 등록)")
        if m.group(2) != q["lv"]:
            add("E_ID_LV", f"id {m.group(2)} vs lv {q['lv']}")
    if "j" in q and not (isinstance(q["j"], int) and 0 <= q["j"] < len(join)):
        add("E_SCHEMA_J", str(q.get("j")))
    opts = q["opts"]
    if not (isinstance(opts, list) and len(opts) == 4 and all(isinstance(o, str) and o.strip() for o in opts)):
        add("E_SCHEMA_OPTS", "보기 4개, 빈 보기 금지")
        return
    if len(set(o.strip() for o in opts)) < 4:
        add("E_OPT_DUP", "같은 보기 중복")
    if q["a"] not in (0, 1, 2, 3):
        add("E_SCHEMA_A", str(q["a"]))
        return
    if q["k"] not in (0, 1):
        add("E_SCHEMA_K", str(q["k"]))
    if not (isinstance(q["metrics"], list) and all(isinstance(x, list) and len(x) == 3 and all(isinstance(y, str) for y in x) for x in q["metrics"])):
        add("E_SCHEMA_METRICS", "[[아이콘,라벨,값],...] 문자열 3원소")
    if not (isinstance(q["fig"], list) and len(q["fig"]) == 2 and isinstance(q["fig"][1], dict)):
        add("E_SCHEMA_FIG", "[name, {params}]")
        return
    for f in ("title", "exp"):
        if not isinstance(q[f], str) or not q[f].strip():
            add("E_SCHEMA_EMPTY", f)
            return

    stem = stem_of(q, join)
    core = core_of(q)
    title, exp, a = q["title"], q["exp"], q["a"]
    ans = opts[a]
    alltext = " ".join([title, stem, exp] + opts + [x[2] for x in q["metrics"]])

    if PLACEHOLDER.search(alltext):
        add("E_PLACEHOLDER", PLACEHOLDER.search(alltext).group(0))

    # 문법 · 문체
    if DOUBLE_Q.search(stem):
        add("E_DOUBLE_Q", DOUBLE_Q.search(stem).group(0))
    for fld, s in (("exp", exp), ("stem", stem)):
        for mm in re.finditer(r"([①②③④])(으로|은|는|이|가|을|를|과|와|로)(?![가-힣])", s):
            n, j = mm.groups()
            odd = n in "①③"  # 일·삼 → 받침 있음 / 이·사 → 받침 없음
            ok = {"은": odd, "이": odd, "을": odd, "과": odd, "으로": odd,
                  "는": not odd, "가": not odd, "를": not odd, "와": not odd, "로": True}[j]
            if not ok:
                add("E_JOSA_CIRC", f"{fld}: {n}{j}")
    for fld, s_ in (("title", title), ("stem", stem), ("exp", exp), ("opts", " / ".join(opts))):
        for mm in EN_JOSA.finditer(s_):
            w, j = mm.group(1).lower(), mm.group(2)
            if w in EN_BATCHIM:
                need1 = EN_BATCHIM[w] == 1
                if (j in "이은을과") != need1:
                    add("E_JOSA_EN", f"{fld}: '{mm.group(0).strip()}'")
        mm = re.search(r"([A-Za-z가-힣][\w\-]{1,})\((\1)\)", s_)
        if mm:
            add("E_TEXT_DUP_PAREN", f"{fld}: {mm.group(0)}")
        mm = re.search(r"[가-힣](을|를|에|으로)입니다", s_)
        if mm:
            add("E_GRAMMAR_TRUNC", f"{fld}: '…{s_[max(0, mm.start() - 12):mm.end()]}' (문장 절단·조립 흔적)")
    pe = PLAIN_END.findall(exp) + PLAIN_END.findall(stem)
    if pe:
        add("E_STYLE_PLAIN", "합니다체 아님: …" + "/".join(sorted(set(x for x in pe)))[:40])
    if "?" not in stem and not stem.rstrip().endswith(("입니까", "니까")):
        add("W_STEM_NO_QMARK", stem[-30:])
    if q.get("j") is not None and q.get("ctx"):
        add("I_TEMPLATE_JOIN", join[q["j"]].strip() if 0 <= q["j"] < len(join) else "")

    # 제목
    t = title.strip()
    if t.endswith("…") or t.endswith("..."):
        add("E_TITLE_TRUNC", t)
    if len(t) > 36:
        add("W_TITLE_LEN", f"{len(t)}자")
    elif len(t) < 8:
        add("W_TITLE_LEN", f"{len(t)}자")
    if re.search(r"(입니까|니까|\?)\s*…?$", t):
        add("W_TITLE_QUESTION", t)
    an_ = normx(ans)
    if 3 <= len(an_) <= 30 and an_ in normx(t) and not any(normx(opts[i]) in normx(t) for i in range(4) if i != a):
        add("W_TITLE_LEAK", "제목에 정답 보기 문구가 들어 있음")
    if t.rstrip("…").strip() and t.rstrip("…").strip() in core and len(t) > 15:
        add("W_TITLE_COPY", "제목이 질문 문장 복사")

    # 해설
    if "[근거]" in exp:
        add("I_EXP_SRC_TAG", "일괄 부착된 [근거] 꼬리표 (EA Phase 2 제거; 문항 고유 출처만 본문에 남김)")
        exp = exp.split("[근거]")[0].strip()
    if len(exp) < 40:
        add("E_EXP_SHORT", f"{len(exp)}자")
    body = re.sub(r"[①②③④]+(은|는|이|가)?", "", exp)
    if len(body.strip()) < 25 and re.search(r"[①②③④]", exp):
        add("E_EXP_ONLY_REFS", exp)
    sents = re.split(r"(?<=[.다요])\s+", exp)
    for s in sents:
        refs = set(re.findall(r"[①②③④]", s))
        if CIRC[a] in refs and NEG_WORDS.search(s) and not POS_WORDS.search(s):
            add("E_EXP_REF_ANSWER", f"정답 {CIRC[a]} 를 오답처럼 서술: {s[:50]}")
        mm = re.search(r"정답은\s*([①②③④])", s)
        if mm and mm.group(1) != CIRC[a]:
            add("E_EXP_REF_ANSWER", f"'정답은 {mm.group(1)}' vs a={CIRC[a]}")
        if len(refs) == 1:
            n = CIRC.index(next(iter(refs)))
            st = set(toks(re.sub(r"[①②③④]", "", s)))
            sc = [len(st & set(toks(o))) for o in opts]
            best = max(range(4), key=lambda i: sc[i])
            if sc[n] == 0 and sc[best] >= 2 and best != n:
                add("W_EXP_REF_MISMATCH", f"{CIRC[n]} 문장이 {CIRC[best]} 보기 내용과 더 일치")
    et = set(toks(exp))
    it_ = set(toks(stem + " " + " ".join(opts) + " " + title))
    plain = [x for x in re.split(r"(?<=[.])\s+", exp) if x.strip() and not re.search(r"[①②③④]", x)]
    first = set(toks(plain[0])) if plain else set()
    if len(first) >= 4 and not (first & it_):
        add("W_EXP_OFFTOPIC", "해설 첫 문장이 문항 어휘와 전혀 겹치지 않음 (다른 문항 해설 혼입 의심)")
    addressed = 0
    for i, o in enumerate(opts):
        if i == a:
            continue
        ot = set(toks(o))
        if CIRC[i] in exp or (ot and len(ot & et) / len(ot) >= 0.5):
            addressed += 1
    if addressed < 3:
        add("W_EXP_DISTRACTORS", f"오답 {addressed}/3 만 해설에서 다룸")
    if CALC_Q.search(core) or all(re.match(r"^[\s약~≈]*[-+]?[\d,]*\.?\d", o) for o in opts):
        if not CALC_WORK.search(exp):
            add("E_CALC_NO_WORK", "계산 문항인데 해설에 대입·계산 과정이 없음")

    # 보기 단서
    L = [len(o) for o in opts]
    other = [L[i] for i in range(4) if i != a]
    if L[a] > 1.25 * max(other) and L[a] - max(other) >= 4:
        add("W_OPT_LONGEST", f"정답 {L[a]}자 vs 오답 최장 {max(other)}자")
    ends = [re.sub(r"[\s.]+$", "", o)[-2:] for o in opts]
    oe = [ends[i] for i in range(4) if i != a]
    if len(set(oe)) == 1 and ends[a] != oe[0]:
        add("W_OPT_ODD_END", f"오답 3개는 '…{oe[0]}', 정답만 '…{ends[a]}'")
    absd = [i for i in range(4) if i != a and ABSOLUTE.search(opts[i])]
    if absd and not ABSOLUTE.search(ans):
        add("W_OPT_ABSOLUTE", "절대어(항상·전혀·반드시 등)가 오답에만 있음")
    pend = [o.rstrip().endswith(".") for o in opts]
    if sum(pend) == 3 and not pend[a] or sum(pend) == 1 and pend[a]:
        add("W_OPT_PUNCT", "정답만 마침표 유무가 다름")
    elif 0 < sum(pend) < 4:
        add("W_OPT_FORM_MIX", "보기 마침표·종결 형식이 섞임")
    weak = [i for i in range(4) if i != a and WEAK_OPT.search(opts[i])]
    if weak:
        add("W_OPT_WEAK", "기술적으로 무의미한 오답(규정·비용·장비 일정·색상 등): " + ", ".join(CIRC[i] for i in weak))
    if any(re.search(r"(위의 모든|모두 옳|모두 맞|모두 해당|해당 없음|정답 없음)", o) for o in opts):
        add("W_OPT_ALL_ABOVE", "'모두/해당 없음' 형 보기")
    st = set(toks(core))
    ov = [len(set(toks(o)) & st) for o in opts]
    if ov[a] >= 3 and ov[a] >= 2 * max(ov[i] for i in range(4) if i != a) + 1:
        add("W_OPT_STEM_ECHO", "정답만 지문 어휘를 크게 반복")

    # metrics
    labels = [x[1] for x in q["metrics"]]
    meta = [l for l in labels if l in META_METRIC_LABELS]
    if "난이도" in labels or len(meta) >= 2:
        add("E_META_METRICS", "metrics 에 난이도/묻는 것/세부 주제/핵심어 등 메타 정보")
    elif meta:
        add("W_META_METRICS", ",".join(meta))
    lvm = [x[2] for x in q["metrics"] if x[1] == "난이도"]
    if lvm and lvm[0] != LV_NAME.get(q["lv"]):
        add("E_META_LV_MISMATCH", f"metrics 난이도 {lvm[0]} vs lv {q['lv']}")

    # 그림
    name, p = q["fig"]
    spec = FIG.get(name)
    if not spec:
        add("E_FIG_UNKNOWN", name)
        return
    for kk in p:
        if kk not in spec["keys"]:
            add("W_FIG_UNKNOWN_KEY", f"{name}.{kk}")
    for kk, vals in spec["enums"].items():
        if kk in p and p[kk] not in vals:
            add("E_FIG_ENUM", f"{name}.{kk}={p[kk]!r}")
    if name == "f_tsv" and all(isinstance(p.get(x), (int, float)) for x in ("ar", "depth_um", "dia_um")) and p["dia_um"]:
        r = p["depth_um"] / p["dia_um"]
        if abs(r - p["ar"]) > max(0.6, 0.05 * r):
            add("E_FIG_INTERNAL", f"f_tsv ar {p['ar']} ≠ depth/dia {r:.1f}")
    if name == "f_plot":
        for ax in ("x", "y"):
            a_ = p.get(ax)
            if not (isinstance(a_, dict) and all(z in a_ for z in ("min", "max", "ticks"))):
                add("E_FIG_PLOT_AXIS", ax)
    if name == "f_therm" and p.get("layers") is not None:
        if not all(isinstance(l, list) and len(l) == 3 and isinstance(l[1], (int, float)) and isinstance(l[2], (int, float)) and l[2] > 0 for l in p["layers"]):
            add("E_FIG_PARAM", "f_therm.layers = [[이름, 두께µm, k], ...]")
    if name == "f_note" and len(p.get("points") or []) > 4:
        add("W_FIG_PARAM", "f_note.points 는 4개까지만 그려짐")
    if name == "f_table":
        if len(p.get("cols") or []) > 5 or len(p.get("rows") or []) > 7 or any(len(r) > 5 for r in (p.get("rows") or [])):
            add("E_FIG_PARAM", "f_table ≤ 7행 × 5열")
    if name == "f_therm" and p.get("layers") and len(p["layers"]) > 5:
        add("E_FIG_PARAM", "f_therm.layers ≤ 5행")
    if name == "f_stack" and isinstance(p.get("n"), int) and p.get("h_um") and p.get("limit_um"):
        pass
    figtext = " ".join(str(x) for x in leaves(p) if isinstance(x, str))
    figtext += " " + " ".join(x[2] + " " + x[1] for x in q["metrics"])
    an = norm(ans)
    if len(an) >= 8 and an in norm(figtext):
        add("W_FIG_LEAK", "정답 보기 문구가 그림/지표에 그대로 노출")
    else:
        at = set(toks(ans))
        ft = set(toks(figtext))
        if len(at) >= 3 and len(at & ft) / len(at) >= 0.75:
            add("W_FIG_LEAK", "정답 보기 어휘 대부분이 그림/지표에 노출")

    # 그림 주제(공법·기법) 불일치
    for pk, kwmap in TOPIC_KW.get(name, {}).items():
        hit = {val for val, rx in kwmap.items() if re.search(rx, core, re.I)}
        if len(hit) == 1 and p.get(pk) not in hit and p.get(pk) is not None:
            add("E_FIG_TOPIC" if q["k"] == 1 else "W_FIG_TOPIC",
                f"지문은 {next(iter(hit))} 인데 그림 {name}.{pk}={p.get(pk)}")

    # k=1 수치 일치
    sn = nums(stem)
    ansn = nums(ans) - sn
    hide = bool(p.get("hideResult"))
    # ── LAYOUT_RULES §3–4 연동 규칙 (DA Phase 1 기본값 변경) ──
    txt = stem + " " + " ".join(opts) + " " + exp
    if name == "f_bond" and p.get("method") == "hcb":
        if re.search(r"dishing|디싱|recess|함몰", stem + " " + " ".join(opts) + " " + exp, re.I) and p.get("dish") is not True:
            add("E_FIG_DISH_OPTIN", "hcb 상황도가 dishing 을 다루는데 dish:true 없음 (DA 기본값 변경: dishing 은 opt-in)")
        if "gap_um" in p:
            add("W_FIG_PARAM", "f_bond hcb 에는 gap_um 을 주지 않는다(표시 안 함)")
    if name == "f_sip":
        mm = re.search(r"(2,?048|1,?024)\s?(개|선|bit|비트)", stem + " " + " ".join(opts))
        if mm and p.get("lines") != int(mm.group(1).replace(",", "")):
            add("E_FIG_SIP_LINES", f"지문의 {mm.group(1)} 배선을 그림에 표시하려면 lines:{mm.group(1).replace(',', '')} 필요(기본은 숫자 없음)")
    if name == "f_warp" and p.get("sign") in (1, -1):
        names = {"Cry": 1, "Smile": -1}
        for nm_, sg in names.items():
            if re.search(nm_, ans, re.I) and not re.search("Cry" if nm_ == "Smile" else "Smile", ans, re.I) and p["sign"] != sg and q["k"] == 1:
                add("E_FIG_WARP_NAME", f"확정 규약: sign {p['sign']} 은 {'Cry(∩)' if p['sign'] == 1 else 'Smile(∪)'} 인데 정답은 {nm_}")
    # 이름을 스스로 표시하는 템플릿(DA 2026-11-21 opt-out): 정답이 그 이름이면 숨김 키 필요
    if name == "f_warp" and re.search(r"Cry|Smile", ans) and not re.search(r"Cry|Smile", stem) and not (p.get("hideNames") or hide):
        add("W_FIG_NAME_LEAK", "정답이 Smile/Cry 명칭인데 f_warp 가 이름을 표시 → hideNames:true")
    if name == "f_bump" and p.get("kirkendall") and re.search(r"Kirkendall", ans, re.I) and not re.search(r"Kirkendall", stem, re.I) and not (p.get("hideLabels") or hide):
        add("W_FIG_NAME_LEAK", "정답이 Kirkendall 인데 f_bump 가 결함 이름을 표시 → hideLabels:true")
    # f_bond 는 공법 비교표·공법 식별 주석을 그린다(2026-11-21): 정답이 공법명·표 문구면 hideTable/hideNotes 검토 (정보 코드)
    if name == "f_bond" and re.search(r"TC-?NCF|MR-?MUF|HCB|hybrid|하이브리드|SiCN|일괄 reflow|상온|filler", ans, re.I) and not re.search(r"TC-?NCF|MR-?MUF|HCB|hybrid|하이브리드", stem, re.I) and not (p.get("hideTable") and p.get("hideNotes")):
        add("I_FIG_BOND_LEAK", "정답이 공법명·공법 특징인데 f_bond 가 비교표·식별 주석을 표시 → hideTable/hideNotes:true 검토")
    if q["k"] == 1 and name in ("f_stack", "f_therm", "f_hcb", "f_tsv") and not hide:
        need = False
        if name == "f_stack" and (CALC_Q.search(core) or re.search(r"높이|단수|장수|간극 수|판정", core)) and re.search(r"(µm|장|단|개|초과|넘)", ans):
            need = True
        if name == "f_therm" and re.search(r"°C|K\b|온도|ΔT", ans):
            need = True
        if name == "f_hcb" and "tol_nm" in p and re.search(r"초과|이내|벗어|허용", ans):
            need = True
        if name == "f_tsv" and re.search(r"aspect|AR", core) and re.search(r"\d\s?:\s?1", ans):
            need = True
        if need:
            add("E_FIG_HIDE_RESULT", f"{name} 가 계산·판정 결과를 그림에 표시 → hideResult:true 필요")
    # 텍스트 길이 (LAYOUT_RULES §1)
    lastq = [x for x in re.split(r"(?<=[.?])\s+", (q.get("qt") or stem).strip()) if x.strip()]
    if lastq and len(lastq[-1]) > 90:
        add("W_QT_LONG", f"질문(마지막 문장) {len(lastq[-1])}자 > 90")
    lim = 700 if code == "MIX" and q.get("ctx") else 520
    if len(stem) > lim:
        add("W_STEM_LEN", f"지문 {len(stem)}자 > {lim}")
    if any(len(o) > 60 for o in opts):
        add("W_OPT_LEN", "보기 60자 초과")
    if len(exp) > 600:
        add("W_EXP_LEN", f"해설 {len(exp)}자 > 600")
    for x in q["metrics"]:
        if len(x[1]) > 12 or len(x[2]) > 16:
            add("W_METRIC_LEN", f"지표 label ≤12 / value ≤16: {x[1]}={x[2]}")
            break
    mm = re.search(r"[=≈×÷]\s?[-−]?[\d.,]+(?:e-?\d+)?(?:\s?[A-Za-zµ°%/²³·]+)?(?<!\s)(?![개장단배회번분초시층행열곳])[가-힣]", exp)
    if mm:
        add("W_EXP_FORMULA_SPACE", f"수식과 한글을 띄어 쓸 것: '{mm.group(0)}'")
    if re.search(r"×\s?10\^", exp):
        add("W_EXP_FORMULA_SPACE", "지수는 e-3 표기(×10^ 금지)")
    if q["k"] == 1:
        bad, extra, leak = [], [], []
        pq = dict(p)
        if name == "f_therm" and "core" in p:
            pq["n"] = p["core"]  # DA Phase 1: core = core die 수(n = core+1). 지문의 N단과 비교
        for kk in spec["q"]:
            ctx_rx = K1_CTX.get((name, kk))
            if name == "f_hcb" and kk in ("off_nm", "tol_nm", "dish_nm") and kk not in pq:
                continue  # DA 2026-11-21: f_hcb 패널은 opt-in — 키가 없으면 그리지 않는다(기본값 없음)
            if hide and (name, kk) == ("f_stack", "h_um"):
                continue  # hideResult 면 높이 칸이 "?" 로 그려져 h_um 은 표시되지 않는다(생략·값 모두 무관)
            if kk not in pq:
                if ctx_rx and re.search(ctx_rx, stem, re.I):
                    bad.append(f"{kk}=기본값")
                continue
            v = pq[kk]
            if isinstance(v, bool) or not isinstance(v, (int, float)):
                continue
            if name == "f_tsv" and kk == "ar":
                continue  # 지문은 직경·깊이만 주고 AR 을 묻는 경우가 많다
            rv = round(float(v), 6)
            if rv in sn:
                continue
            if rv in ansn:
                if not (hide and (name, kk) in (("f_stack", "h_um"), ("f_tsv", "ar"))):
                    leak.append(f"{kk}={v}")
            elif ctx_rx and re.search(ctx_rx, stem, re.I):
                bad.append(f"{kk}={v}")
            else:
                extra.append(f"{kk}={v}")
        if name == "f_therm" and p.get("layers"):
            for l in p["layers"]:
                for v in l[1:]:
                    if isinstance(v, (int, float)) and round(float(v), 6) not in sn:
                        (bad if re.search(r"W/mK|열전도", stem) else extra).append(f"layer {l[0]}={v}")
        if leak:
            add("E_FIG_ANSWER_LEAK", "그림 수치가 정답 보기 값을 그대로 보여 줌: " + ", ".join(leak))
        if bad:
            add("E_K1_FIG_NUM", "지문 조건과 다른 그림 수치: " + ", ".join(bad[:5]))
        if extra:
            add("W_K1_FIG_EXTRA", "지문에 없는 수치가 그림에 표시됨: " + ", ".join(extra[:5]))
        mbad = []
        for x in q["metrics"]:
            for v in nums(x[2]):
                if v not in sn and v not in (0, 1, 2) and not (x[1] in ("정의",)):
                    mbad.append(f"{x[1]}={x[2]}")
                    break
        if mbad:
            add("W_K1_METRIC_NUM", "지표 수치가 지문에 없음: " + ", ".join(mbad[:4]))
    else:
        if re.search(r"(그림|도면|상황도)(에|은|과|의|을|처럼|에서)", stem):
            add("W_FIG_REF_K0", "지문이 그림을 지칭하지만 k=0(주제도)")
        if name == "f_tsv" and p.get("fill") in ("void", "seam", "pinch") and not re.search(r"(void|seam|pinch|공동|빈 공간|공극|이음)", stem + " ".join(opts), re.I):
            add("W_FIG_K0_DEFECT", f"주제도에 문항과 무관한 결함({p['fill']})이 그려짐")

    # 사실 확인 표시
    for rx, why in FACT_WATCH:
        mm = rx.search(stem + " " + " ".join(opts) + " " + exp)
        if mm:
            add("I_FACT_WATCH", f"{why} :: '{mm.group(0)[:40]}'")
    if re.search(r"μ", alltext):
        add("I_UNIT_MU", "그리스 문자 μ 대신 µ(U+00B5) 사용")
    if re.search(r"\d\s?um\b", alltext):
        add("I_UNIT_UM", "um → µm")
    if josa_space_hits(stem + " " + exp):
        add("I_JOSA_SPACE", "영문·숫자 뒤 조사 띄어 씀 (EA Phase 2 일괄; 수식 바로 뒤는 예외)")


# ───────────────────────── 집합 검사 ─────────────────────────
def shingles(s, n=5):
    s = norm(s)
    return {s[i:i + n] for i in range(max(1, len(s) - n + 1))}


def near_dups(Q, thr=0.80):
    sh = [shingles(core_of(q) + "|" + "|".join(sorted(q["opts"]))) for q in Q]
    inv = collections.defaultdict(list)
    for i, s in enumerate(sh):
        for g in s:
            inv[g].append(i)
    cnt = collections.Counter()
    for g, lst in inv.items():
        if 1 < len(lst) <= 80:
            for x in range(len(lst)):
                for y in range(x + 1, len(lst)):
                    cnt[(lst[x], lst[y])] += 1
    out = []
    for (i, j), c in cnt.items():
        if c < 0.4 * min(len(sh[i]), len(sh[j])):
            continue
        inter = len(sh[i] & sh[j])
        jac = inter / (len(sh[i]) + len(sh[j]) - inter)
        if jac >= thr:
            out.append((i, j, jac))
    return out


LEGACY = {}


def load(domain=None):
    meta = json.load(open(os.path.join(ROOT, "data/_meta.json"), encoding="utf8"))
    files = sorted(glob.glob(os.path.join(ROOT, "data/[0-9]*.json")))
    allq, per = [], {}
    for f in files:
        d = json.load(open(f, encoding="utf8"))
        per[d["code"]] = (os.path.basename(f), d)
        LEGACY[d["code"]] = tuple(d.get("legacy_prefix") or ())
        for q in d["questions"]:
            allq.append((d["code"], q))
    return meta, per, allq


def run(domain=None):
    meta, per, allq = load()
    join = meta["join"]
    issues = []
    ids = collections.Counter(q.get("id") for _, q in allq)
    for code, q in allq:
        if domain and code != domain:
            continue
        check_item(q, code, join, issues, LEGACY.get(code, ()))
        if ids[q.get("id")] > 1:
            issues.append({"id": q["id"], "d": code, "lv": q.get("lv"), "code": "E_ID_DUP", "msg": "id 중복"})
    # 중복 · 근중복 (전 분야 대상으로 계산, 보고는 해당 분야만)
    Q = [q for _, q in allq if isinstance(q.get("opts"), list)]
    C = [c for c, q in allq if isinstance(q.get("opts"), list)]
    exact = collections.defaultdict(list)
    for i, q in enumerate(Q):
        exact[normx(core_of(q)) + "|" + "|".join(sorted(normx(o) for o in q["opts"]))].append(i)
    for k, lst in exact.items():
        for i in lst[1:]:
            if domain and C[i] != domain:
                continue
            issues.append({"id": Q[i]["id"], "d": C[i], "lv": Q[i]["lv"], "code": "E_DUP_EXACT", "msg": "동일 문항: " + Q[lst[0]]["id"]})
    nd = near_dups(Q)
    seen_exact = {i for lst in exact.values() for i in lst[1:]}
    fk = [fam_key(core_of(q)) for q in Q]
    best = {}
    for i, j, jac in nd:
        if j in seen_exact or i in seen_exact or (C[i] == C[j] and fk[i] == fk[j]):
            continue
        x, y = (j, i) if Q[j]["id"] > Q[i]["id"] else (i, j)   # 뒤 id 쪽에 표시
        if x not in best or jac > best[x][1]:
            best[x] = (y, jac)
    for x, (y, jac) in best.items():
        if domain and C[x] != domain:
            continue
        if "W_NEAR_DUP" in (Q[x].get("vx") or []):
            continue
        code = "W_NEAR_DUP" if C[x] == C[y] else "W_NEAR_DUP_X"
        issues.append({"id": Q[x]["id"], "d": C[x], "lv": Q[x]["lv"], "code": code, "msg": f"{Q[y]['id']} 와 유사도 {jac:.2f}"})
    # 수치만 바꾼 템플릿 가족: 분야 내 4개째부터 E
    fam = collections.defaultdict(list)
    for i, q in enumerate(Q):
        fam[(C[i], fam_key(core_of(q)))].append(i)
    families = []
    for (c, k), lst in fam.items():
        if len(lst) > 1:
            families.append((c, len(lst), [Q[i]["id"] for i in lst], k[:80]))
        if len(lst) > 3:
            for i in lst[3:]:
                if domain and C[i] != domain:
                    continue
                if "E_FAMILY_OVER" in (Q[i].get("vx") or []):
                    continue
                issues.append({"id": Q[i]["id"], "d": C[i], "lv": Q[i]["lv"], "code": "E_FAMILY_OVER",
                               "msg": f"수치만 다른 동형 문항 {len(lst)}개 (대표 {Q[lst[0]]['id']}) — 가족당 3개 이하"})
    return meta, per, allq, issues, families


def pos_table(allq, domain=None):
    t = collections.defaultdict(lambda: [0, 0, 0, 0])
    for c, q in allq:
        if domain and c != domain:
            continue
        if q.get("a") in (0, 1, 2, 3):
            t[(c, q["lv"])][q["a"]] += 1
    return t


def report_md(meta, per, allq, issues, families, domain=None):
    codes = [c for c in per if not domain or c == domain]
    lvs = ["B", "I", "A"]
    byd = collections.defaultdict(collections.Counter)
    bydl = collections.defaultdict(collections.Counter)
    items_with_e = collections.defaultdict(set)
    for it in issues:
        byd[it["d"]][it["code"]] += 1
        bydl[(it["d"], it["lv"])][it["code"][0]] += 1
        if it["code"][0] == "E":
            items_with_e[it["d"]].add(it["id"])
    nq = collections.Counter(c for c, _ in allq)
    nql = collections.Counter((c, q.get("lv")) for c, q in allq)
    out = []
    out.append(f"# 자동 검사 리포트 {'(' + domain + ')' if domain else ''}\n")
    out.append("생성: `python3 tools/validate.py` · 규칙: `docs/agents/STANDARDS.md` · 심각도 E=필수 수정, W=검토, I=참고/EA 일괄\n")
    tot = collections.Counter(it["code"][0] for it in issues)
    out.append(f"- 문항 수: {sum(nq[c] for c in codes)} · 이슈: E {tot['E']} / W {tot['W']} / I {tot['I']}")
    out.append(f"- E 이슈가 1건 이상인 문항: {sum(len(items_with_e[c]) for c in codes)}\n")
    out.append("## 1. 분야 × 난이도 요약 (문항 수 / E 건수 / W 건수)\n")
    out.append("| 분야 | 문항 | E 문항 | " + " | ".join(f"{LV_NAME[l]} n·E·W" for l in lvs) + " |")
    out.append("|---|---|---|" + "---|" * len(lvs))
    for c in codes:
        cells = []
        for l in lvs:
            cc = bydl[(c, l)]
            cells.append(f"{nql[(c, l)]} · {cc['E']} · {cc['W']}")
        out.append(f"| {c} | {nq[c]} | {len(items_with_e[c])} | " + " | ".join(cells) + " |")
    out.append("\n## 2. 정답 위치 분포 (①/②/③/④, 목표 각 25% ± 3%)\n")
    out.append("| 분야 | 난이도 | n | ① | ② | ③ | ④ | 판정 |")
    out.append("|---|---|---|---|---|---|---|---|")
    pt = pos_table(allq, domain)
    gl = [0, 0, 0, 0]
    for c in codes:
        for l in lvs:
            v = pt[(c, l)]
            n = sum(v)
            if not n:
                continue
            gl = [gl[i] + v[i] for i in range(4)]
            pct = [100 * x / n for x in v]
            ok = all(22 <= x <= 28 for x in pct)
            out.append(f"| {c} | {LV_NAME[l]} | {n} | " + " | ".join(f"{x:.0f}%" for x in pct) + f" | {'OK' if ok else '편향'} |")
    n = sum(gl) or 1
    out.append(f"| **전체** | | {sum(gl)} | " + " | ".join(f"{100 * x / n:.1f}% ({x})" for x in gl) + " | |")
    out.append("\n## 3. 이슈 코드별 건수 (분야별)\n")
    allcodes = sorted({it["code"] for it in issues}, key=lambda x: ("EWI".index(x[0]), x))
    out.append("| 코드 | 합계 | " + " | ".join(codes) + " |")
    out.append("|---|---|" + "---|" * len(codes))
    for k in allcodes:
        row = [byd[c][k] for c in codes]
        out.append(f"| {k} | {sum(row)} | " + " | ".join(str(x) if x else "·" for x in row) + " |")
    out.append("\n## 4. 수치만 바꾼 동형 문항 가족 (분야 내, 크기 ≥ 4)\n")
    out.append("| 분야 | 크기 | 대표 id | 패턴 (숫자→#) |")
    out.append("|---|---|---|---|")
    fams = sorted([f for f in families if f[1] >= 4 and (not domain or f[0] == domain)], key=lambda x: -x[1])
    for c, k, ids, pat in fams[:60]:
        out.append(f"| {c} | {k} | {ids[0]} | {pat.replace('|', '/')} |")
    surplus = collections.Counter()
    for c, k, ids, pat in families:
        if k > 3:
            surplus[c] += k - 3
    out.append(f"\n가족 초과분(4번째 이후) 합계: {sum(surplus.values())} — " + ", ".join(f"{c} {v}" for c, v in surplus.most_common()))
    out.append("\n## 5. 이슈 코드 설명\n")
    for k, v in CODE_DOC.items():
        out.append(f"- `{k}` — {v}")
    return "\n".join(out) + "\n"


CODE_DOC = {
    "E_SCHEMA_*": "필드 누락·형식 오류 (opts 4개, a 0–3, k 0/1, metrics [[아이콘,라벨,값]], fig [name,{params}])",
    "E_ID_FORMAT / E_ID_LV / E_ID_DUP": "id 는 CODE-LV-NNNN, lv 와 일치, 전역 유일",
    "E_PLACEHOLDER": "undefined/NaN/TODO/{var} 등 생성 흔적",
    "E_DOUBLE_Q": "'…라 하는가 무엇입니까' 같은 이중 의문형",
    "E_JOSA_CIRC": "①은 ②는 ③은 ④는 / ①이 ②가 / ①을 ②를 / ①과 ②와 규칙 위반",
    "E_STYLE_PLAIN": "지문·해설에 해라체 종결(…다.) — 합니다체로 통일",
    "E_TITLE_TRUNC": "제목이 … 로 잘림",
    "E_EXP_SHORT / E_EXP_ONLY_REFS": "해설 40자 미만 또는 '②①④은 근거가 아니다' 식 번호 나열",
    "E_EXP_REF_ANSWER": "해설이 정답 번호를 오답처럼 서술하거나 '정답은 ③' 이 a 와 불일치",
    "E_CALC_NO_WORK": "계산 문항인데 해설에 대입·계산식이 없음",
    "E_META_METRICS": "metrics 에 난이도·묻는 것·세부 주제·핵심어 같은 메타 정보 (지표는 지문 조건이어야 함)",
    "E_FIG_UNKNOWN / E_FIG_ENUM / E_FIG_PARAM / E_FIG_PLOT_AXIS": "그림 템플릿·params 형식 오류",
    "E_FIG_INTERNAL": "그림 params 내부 모순 (예: f_tsv ar ≠ depth/dia)",
    "E_K1_FIG_NUM": "k=1 인데 지문이 다루는 물리량의 그림 수치가 지문 값과 다르거나 기본값으로 그려짐",
    "E_FIG_ANSWER_LEAK": "k=1 그림 수치가 정답 보기의 값을 그대로 보여 줌 (계산 문항의 답 노출)",
    "E_FIG_TOPIC / W_FIG_TOPIC": "지문이 지칭하는 공법·기법과 그림 템플릿 분기가 다름 (k=1 이면 E)",
    "W_K1_FIG_EXTRA": "k=1 그림에 지문에 없는 수치가 표시됨 (지문에 추가하거나 그림에서 제거)",
    "E_JOSA_EN": "영문 용어 + 조사 불일치 (한글 독음 받침 기준: seam→이/은/을, void·kerf·warpage→가/는/를; 사전 EN_BATCHIM)",
    "E_TEXT_DUP_PAREN": "'IMC(IMC)' 같은 치환 흔적",
    "E_GRAMMAR_TRUNC": "'…층을입니다' 처럼 문장을 잘라 붙인 흔적",
    "W_OPT_WEAK": "규정·비용·장비 일정·색상 등 기술적으로 무의미해 바로 소거되는 오답",
    "W_EXP_OFFTOPIC": "해설 첫 문장이 문항과 무관 (다른 문항 해설 혼입 의심)",
    "E_FIG_HIDE_RESULT": "k=1 계산·판정 문항인데 f_stack/f_therm/f_hcb/f_tsv 에 hideResult:true 없음 (LAYOUT_RULES §3)",
    "E_FIG_DISH_OPTIN": "f_bond hcb 상황도가 dishing 을 다루는데 dish:true 없음 (DA 기본값 변경)",
    "W_FIG_NAME_LEAK": "정답 명칭(Smile/Cry, Kirkendall)을 그림이 표시 — hideNames/hideLabels 필요 (DA 2026-11-21)",
    "E_FIG_SIP_LINES": "f_sip 지문이 1,024/2,048 배선을 말하는데 lines 값 없음·불일치 (DA 기본값 변경)",
    "E_FIG_WARP_NAME": "f_warp sign 과 정답 명칭 불일치 (확정 규약: sign 1 = ∩ = Cry, −1 = ∪ = Smile)",
    "W_QT_LONG / W_STEM_LEN / W_OPT_LEN / W_EXP_LEN / W_METRIC_LEN": "LAYOUT_RULES §1 길이 상한 (질문 마지막 문장 90, 지문 520(MIX ctx 700), 보기 60, 해설 600, 지표 label 12·value 16)",
    "W_EXP_FORMULA_SPACE": "해설 수식 뒤 한글을 붙여 씀 / ×10^ 사용 (LAYOUT_RULES §2)",
    "W_OPT_PUNCT / W_OPT_FORM_MIX": "정답만 마침표 유무가 다름 / 보기 종결 형식 혼재",
    "I_EXP_SRC_TAG": "일괄 부착된 '[근거] …' 꼬리표 — EA Phase 2 에서 제거",
    "E_DUP_EXACT": "핵심 텍스트+보기 동일 문항",
    "E_FAMILY_OVER": "수치만 바꾼 동형 문항이 분야 내 3개 초과",
    "W_NEAR_DUP / W_NEAR_DUP_X": "근중복 (5-gram Jaccard ≥ 0.80, _X 는 타 분야와)",
    "W_TITLE_LEN / W_TITLE_QUESTION / W_TITLE_COPY": "제목 8–36자, 의문문 금지, 질문 복사 금지",
    "W_TITLE_LEAK": "제목에 정답 보기 문구가 그대로 들어 있음",
    "W_STEM_NO_QMARK": "지문에 물음 문장이 없음",
    "W_EXP_DISTRACTORS": "해설이 오답 3개를 모두 다루지 않음",
    "W_EXP_REF_MISMATCH": "해설의 ①–④ 참조가 다른 보기 내용과 일치 (번호 어긋남 의심)",
    "W_OPT_LONGEST": "정답이 오답 최장보다 25% 이상 김",
    "W_OPT_ODD_END": "오답 3개의 어미가 같고 정답만 다름 (형식 단서)",
    "W_OPT_ABSOLUTE": "절대어가 오답에만 있음 (소거 단서)",
    "W_OPT_ALL_ABOVE": "'모두 옳다/해당 없음' 보기",
    "W_OPT_STEM_ECHO": "정답만 지문 어휘를 반복 (연상 단서)",
    "W_META_METRICS": "metrics 에 메타 라벨 1개",
    "W_FIG_LEAK": "정답 문구가 그림·지표에 노출",
    "W_K1_METRIC_NUM": "k=1 지표 수치가 지문에 없음",
    "W_FIG_REF_K0": "지문이 '그림' 을 지칭하는데 k=0",
    "W_FIG_K0_DEFECT": "주제도에 문항과 무관한 결함이 그려짐",
    "W_FIG_UNKNOWN_KEY": "템플릿이 읽지 않는 params 키",
    "I_FACT_WATCH": "사실 확인 필요 표현 (세대·표준 번호·수치)",
    "I_FIG_BOND_LEAK": "f_bond 비교표·식별 주석이 공법명·특징 정답을 노출할 수 있음 — hideTable/hideNotes (DA 2026-11-21)",
    "I_TEMPLATE_JOIN": "ctx+join+qt 조립형 (지문 연관성 수동 확인 대상)",
    "I_JOSA_SPACE / I_UNIT_*": "띄어쓰기·단위 표기 — EA Phase 2 일괄 정리",
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--domain")
    ap.add_argument("--codes", help="쉼표 구분 코드 필터 (접두 일치)")
    ap.add_argument("--out", help="markdown 리포트 경로")
    ap.add_argument("--json", help="전체 이슈 JSON 경로")
    ap.add_argument("--gate", action="store_true", help="E 이슈가 있으면 exit 1")
    ap.add_argument("--quiet", action="store_true")
    a = ap.parse_args()
    meta, per, allq, issues, families = run(a.domain)
    if a.codes:
        pre = [x.strip() for x in a.codes.split(",")]
        issues_f = [it for it in issues if any(it["code"].startswith(p) for p in pre)]
    else:
        issues_f = issues
    if a.json:
        json.dump(issues_f, open(a.json, "w", encoding="utf8"), ensure_ascii=False, indent=0)
    out = a.out or (None if a.domain else os.path.join(ROOT, "docs/reviews/_auto_latest.md"))
    if out:
        os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
        open(out, "w", encoding="utf8").write(report_md(meta, per, allq, issues, families, a.domain))
    if a.domain and not a.quiet:
        try:
            for it in sorted(issues_f, key=lambda x: (x["id"], x["code"])):
                print(f"{it['id']}\t{it['code']}\t{it['msg']}")
        except BrokenPipeError:  # | head 등으로 잘린 경우
            sys.stderr.close()
            os._exit(0)
    tot = collections.Counter(it["code"][0] for it in issues)
    print(f"[validate] {a.domain or 'ALL'}: E {tot['E']} / W {tot['W']} / I {tot['I']}" + (f" → {out}" if out else ""), file=sys.stderr)
    blocking = [it for it in issues if it["code"][0] == "E" and it["code"] not in PHASE2_E]
    if a.gate:
        print(f"[gate] 차단 E {len(blocking)} 건 (Phase 2 일괄 대상 {', '.join(sorted(PHASE2_E))} 제외)", file=sys.stderr)
        if blocking:
            sys.exit(1)


if __name__ == "__main__":
    main()
