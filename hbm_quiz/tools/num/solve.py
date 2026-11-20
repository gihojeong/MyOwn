"""NUM 재계산 엔진: 문항 유형별 solver 로 정답값을 다시 계산해 정답 키·오답 구별·현실 범위·그림 노출을 검사한다."""
import math, json, re, collections, sys
from load import *

F = r"([-+]?\d[\d,]*\.?\d*)"


def fnum(s):
    return float(s.replace(",", ""))


def g(pat, t, n=1, flags=0):
    m = re.search(pat, t, flags)
    if not m:
        return None
    if n == 1:
        return fnum(m.group(1))
    return tuple(fnum(m.group(i)) for i in range(1, n + 1))


def optnums(o):
    s = o.replace("−", "-")
    return [fnum(x) for x in re.findall(r"(?<![A-Za-z\d])[-+]?\d[\d,]*\.?\d*", s) if re.search(r"\d", x)]


def decimals(o):
    m = re.search(r"\d[\d,]*\.(\d+)", o)
    return len(m.group(1)) if m else 0


SOLVERS = []


def solver(name, domains, pat):
    def deco(fn):
        SOLVERS.append((name, domains, re.compile(pat, re.S), fn))
        return fn
    return deco


# 결과 dict: v (기대값 float 또는 tuple), unit, f (식·대입 문자열), real (현실성 경고 list), pick (옵션→값 추출 함수, 기본 첫 숫자)
# 선택: judge (판정 문자열: 정답 옵션에 들어 있어야 할 문구), tol

def R(v, unit, f, real=None, pick=None, judge=None, tol=None, note=None, exact=False):
    return dict(v=v, unit=unit, f=f, real=real or [], pick=pick, judge=judge, tol=tol, note=note, exact=exact)


# ---------------- TSV ----------------
@solver("TSV_R", ("TSV",), r"TSV.*(비저항|ρL/A).*저항")
def s_tsv_r(t, q):
    d = g(r"직경\s*(?:이\s*)?" + F + r"\s*µm", t) or g(r"직경이\s*" + F, t)
    L = g(r"(?:길이|깊이)\s*(?:가|이)?\s*" + F + r"\s*µm", t)
    rho = g(F + r"\s*×\s*10⁻⁸\s*Ω·m", t) or g(F + r"×10⁻⁸", t)
    if None in (d, L, rho):
        return None
    A = math.pi * (d * 1e-6) ** 2 / 4
    Rv = rho * 1e-8 * L * 1e-6 / A * 1e3
    real = [f"I: TSV 길이 {L:g} µm — HBM core die(30–60 µm) 관통 길이보다 김(base die 또는 '일반 TSV' 로 명시)"] if L > 60 else []
    return R(Rv, "mΩ", real=real, f=f"R = ρL/(πd²/4) = {rho}e-8 × {L}e-6 ÷ (π×({d}e-6)²/4) = {Rv:.2f} mΩ")


@solver("TSV_AR2", ("TSV",), r"조건 A 는 직경")
def s_ar2(t, q):
    a = g(r"조건 A 는 직경\s*" + F + r"\s*µm\s*·\s*깊이\s*" + F, t, 2)
    b = g(r"조건 B 는 직경\s*" + F + r"\s*µm\s*·\s*깊이\s*" + F, t, 2)
    ra, rb = a[1] / a[0], b[1] / b[0]
    return R((ra, rb), "", f"A = {a[1]}/{a[0]} = {ra:g}, B = {b[1]}/{b[0]} = {rb:g}", pick=lambda o: tuple(x for x in optnums(o) if x not in (1.0,))[:2] if 'A 가' in o[:5] else None)


@solver("TSV_AR", ("TSV",), r"aspect ratio 로 옳은")
def s_ar(t, q):
    if "개선 조건은" in t:
        d, h = g(r"개선 조건은 직경\s*" + F + r"\s*µm\s*·\s*깊이\s*" + F, t, 2)
    else:
        d = g(r"직경\s*" + F + r"\s*µm", t); h = g(r"깊이\s*" + F + r"\s*µm", t)
    ar = h / d
    real = []
    if h > 60:
        real.append(f"I: 깊이 {h:g} µm — HBM core die(30–60 µm) 기준으로 깊음(base die·일반 TSV 로 명시)")
    if ar > 20:
        real.append(f"I: AR {ar:g}:1 — 양산 TSV(약 10:1 내외, 연구 20:1 미만) 범위를 넘음")
    return R(ar, ":1", f"AR = 깊이 ÷ 직경 = {h:g} ÷ {d:g} = {ar:g}", real=real)


@solver("CTE_DIFF", ("TSV",), r"열팽창계수는 약.*길이\s*[\d.]+\s*µm 구간")
def s_cte(t, q):
    a1 = g(r"열팽창계수는 약\s*" + F, t); a2 = g(r"Si 는 약\s*" + F, t)
    L = g(r"길이\s*" + F + r"\s*µm 구간", t); dT = g(r"온도가\s*" + F + r"\s*K 올라", t)
    v = (a1 - a2) * 1e-6 * dT * L * 1e3
    return R(v, "nm", f"ΔL = (α₁−α_Si)·ΔT·L = ({a1}−{a2})e-6 × {dT:g} × {L:g}e3 nm = {v:.1f} nm")


@solver("CTE_DIA", ("TSV",), r"직경 기준으로 대략")
def s_cte_dia(t, q):
    v = (16.5 - 2.7) * 1e-6 * 225 * 5000
    return R(v, "nm", f"(16.5−2.7)e-6 × 225 K × 5,000 nm = {v:.1f} nm")


# ---------------- BUMP ----------------
@solver("IMC_FWD", ("BUMP",), r"시간 보관한 시료의 IMC 두께가(?!.*계수 k 를 구하고 1000).*시간 보관 후 IMC 두께가")
def s_imc_fwd(t, q):
    T, t1, x1 = g(F + r"\s*°C 에서\s*" + F + r"\s*시간 보관한 시료의 IMC 두께가\s*" + F, t, 3)
    t2, lim = g(F + r"\s*시간 보관 후 IMC 두께가\s*" + F, t, 2)
    nexp = g(r"t\^" + F, t) or 0.5
    k = x1 / t1 ** nexp; x2 = k * t2 ** nexp
    real = []
    if x2 > 10: real.append(f"I: 예측 IMC {x2:.1f} µm — µbump solder 두께(수~십수 µm)를 넘어 full-IMC 상태, 설정 재검토")
    return R(x2, "µm", f"k = {x1} ÷ {t1:g}^{nexp} = {k:.4f}; x({t2:g} h) = k·{t2:g}^{nexp} = {x2:.2f} µm (규격 {lim:g} µm)", real=real)


@solver("IMC_FWD_A1", ("BUMP",), r"계수 k 를 구하고 1000 시간에서의 두께")
def s_imc_a1(t, q):
    t1, x1 = g(F + r"\s*시간 보관한 시료의 IMC 두께가\s*" + F, t, 2)
    k = x1 / math.sqrt(t1); x2 = k * math.sqrt(1000)
    return R(x2, "µm", f"k = {x1}/√{t1:g} = {k:.3f}; x = k√1000 = {x2:.2f} µm", pick=lambda o: (optnums(o)[2] if len(optnums(o)) >= 3 else None))


@solver("IMC_INV", ("BUMP",), r"최대 유지 시간을 역산")
def s_imc_inv(t, q):
    T, t1, x1 = g(F + r"\s*°C 에서\s*" + F + r"\s*시간 보관한 시료의 IMC 두께가\s*" + F, t, 3)
    lim = g(r"IMC 두께가\s*" + F + r"\s*µm 를 넘지", t)
    nexp = g(r"t\^" + F, t) or 0.5
    k = x1 / t1 ** nexp; tt = (lim / k) ** (1 / nexp)
    return R(tt, "h", f"k = {x1}/{t1:g}^{nexp} = {k:.4f}; t = (x/k)^(1/{nexp}) = ({lim:g}/{k:.4f})² = {tt:.0f} h")


@solver("IMC_KT", ("BUMP",), r"성장 계수 k 는")
def s_imc_kt(t, q):
    k = g(r"성장 계수 k 는\s*" + F, t); tt = g(r"제품을\s*" + F + r"\s*시간", t)
    x = k * math.sqrt(tt)
    return R(x, "µm", f"x = k√t = {k} × √{tt:g} = {x:.2f} µm")


@solver("EM_J", ("BUMP",), r"(전류 밀도|전류밀도).*(kA/cm²|얼마|가까운 값)")
def s_em(t, q):
    d = g(r"(?:직경|지름)\s*(?:이\s*)?" + F + r"\s*µm", t) or g(r"지름이\s*" + F, t)
    I = None
    m = re.search(F + r"\s*(mA|A)\s*의 (?:직류|전류)", t)
    if m:
        I = fnum(m.group(1)) * (1e-3 if m.group(2) == "mA" else 1)
    if d is None or I is None:
        return None
    A = math.pi * (d * 1e-4) ** 2 / 4
    j = I / A / 1e3
    real = []
    if j >= 50 or I >= 0.1:
        real.append(f"E: pillar 당 {I*1e3:.0f} mA · 평균 {j:.0f} kA/cm² — µbump 당 전류 수십 mA 이하·EM 시험 영역 10 kA/cm² 급(STANDARDS 2.4)을 크게 넘음")
    elif j > 15 or I > 0.05:
        real.append(f"I: pillar 당 {I*1e3:.0f} mA · 평균 {j:.1f} kA/cm² — 실사용 기준으론 EM 가속시험 수준(설정 의도 명시 권장)")
    return R(j, "kA/cm²", f"j = I ÷ (πd²/4) = {I:g} A ÷ (π×({d:g}e-4 cm)²/4 = {A:.3e} cm²) = {j:.2f} kA/cm²", real=real)


# ---------------- SAW ----------------
@solver("SAW_GAIN", ("SAW",), r"scribe lane 폭은")
def s_saw(t, q):
    a = g(r"한 변\s*" + F + r"\s*mm", t); W = g(F + r"\s*mm wafer", t)
    l1 = g(r"scribe lane 폭은\s*" + F, t); l2 = g(F + r"\s*µm 까지 줄이는", t)
    Aw = math.pi * (W / 2) ** 2
    n1 = Aw / (a + l1 / 1000) ** 2; n2 = Aw / (a + l2 / 1000) ** 2
    # 해설은 정수 die 수의 차를 쓴다
    d_int = math.floor(n2) - math.floor(n1)
    pct = (n2 / n1 - 1) * 100
    return R(d_int, "개", f"N = π·{W/2:g}² ÷ (a+lane)²: {n1:.1f} → {n2:.1f} (정수 {math.floor(n1)} → {math.floor(n2)}), 증가 {d_int}개 ({pct:.2f} %)",
             pick=lambda o: optnums(o)[0], tol=0.0)


# ---------------- COW ----------------
@solver("PPM_DISP", ("COW",), r"ppm 만큼 다르면")
def s_ppm(t, q):
    ppm = g(F + r"\s*ppm 만큼", t); r = g(r"반지름\s*" + F + r"\s*mm 지점", t); tol = g(r"허용치는\s*±\s*" + F, t)
    v = r * 1e6 * ppm * 1e-6  # nm
    judge = "이내" if v <= tol else "벗어"
    real = []
    if r > 15:
        real.append(f"E: 반지름 {r:g} mm — HBM die(한 변 약 10–13 mm, 반경 ≤ 약 8 mm)가 아닌 wafer 규모(W2W)의 반경. D2W HBM 문항이면 die 반경으로 설정")
    return R(v, "nm", f"Δ = r × ε = {r:g} mm × {ppm:g}×10⁻⁶ = {r:g}×10⁶ nm × {ppm:g}×10⁻⁶ = {v:g} nm (허용 ±{tol:g} nm → {'허용치 이내' if v<=tol else '허용치 초과'})",
             real=real, judge=judge)


@solver("PITCH_DENS", ("COW",), r"pitch 를\s*[\d.]+\s*µm 까지 줄일|pitch 가\s*[\d.]+\s*µm 에서\s*[\d.]+\s*µm 로 줄 때")
def s_pitch(t, q):
    p1 = g(r"pitch 는\s*" + F, t) or g(r"pitch 가\s*" + F, t)
    p2 = g(r"pitch 를\s*" + F, t) or g(r"에서\s*" + F + r"\s*µm 로 줄 때", t)
    v = (p1 / p2) ** 2
    real = []
    if p2 < 20 and "bump pitch" in t and "hybrid" not in t:
        real.append(f"I: 목표 pitch {p2:g} µm — solder µbump 로는 비현실(µbump 25–55 µm), 10 µm 이하는 HCB 영역. '차세대 공법=HCB' 명시 권장")
    return R(v, "배", f"(p₁/p₂)² = ({p1:g}/{p2:g})² = {v:.2f}", real=real)


@solver("PAD_OVERLAP", ("COW",), r"겹치는 면적은 설계 면적의 몇 퍼센트")
def s_overlap(t, q):
    a = g(r"한 변이\s*" + F + r"\s*nm", t); e = g(r"각각\s*" + F + r"\s*nm", t)
    v = (1 - e / a) ** 2 * 100
    return R(v, "%", f"((a−e)/a)² = ((({a:g}−{e:g})/{a:g})² = {v:.2f} %")


@solver("CONTACTS", ("COW",), r"접합 계면이\s*[\d]+\s*개")
def s_contacts(t, q):
    io = g(r"I/O 는\s*" + F, t); r = g(r"약\s*" + F + r"\s*배로 잡혔", t); n = g(r"접합 계면이\s*" + F, t)
    per = io * r
    v = per * n
    real = [f"I: 계면당 접점 {per:,.0f} 개 — 실제 HBM 계면 접점(TSV·µbump)은 수천~1만 개 이상(전원·접지 다수)으로 배율 {r:g} 은 낮게 잡힘(참고)"] if r < 3 else []
    return R(v, "개", f"{io:g} × {r:g} × {n:g} = {v:,.0f} 개 (해설은 계면당 값을 반올림 후 곱함: {round(per):,} × {n:g} = {round(per)*n:,.0f})", real=real, tol=0.005)


@solver("MUF_TIME", ("COW",), r"충전 시간은 간극에 반비례")
def s_muf(t, q):
    g1, g2 = g(r"간극을\s*" + F + r"\s*µm 에서\s*" + F, t, 2)
    v = g1 / g2
    return R(v, "배", f"t ∝ 1/h → t₂/t₁ = {g1:g}/{g2:g} = {v:.2f} 배", note="물리 주의: Washburn 류 모세관 충전 t ≈ 3μL²/(γ h cosθ) 이면 1/h 비례가 맞음(평판 간극). 지문에 가정으로 명시되어 있어 계산은 성립")


# ---------------- SIP ----------------
@solver("STACK_H16", ("SIP",), r"core die\s*\d+장과 base die 1장을 쌓는 구성에서 die 한 장의 두께는")
def s_h16(t, q):
    n = g(r"core die\s*" + F + r"장과", t); td = g(r"die 한 장의 두께는\s*" + F, t); gp = g(r"간극은 한 곳당\s*" + F, t); lim = g(r"상한은\s*" + F, t)
    h = td * (n + 1) + gp * n
    return R(h, "µm", f"H = {td:g}×({n:g}+1) + {gp:g}×{n:g} = {h:g} µm (상한 {lim:g} → {'이내' if h<=lim else '초과'})",
             judge=("넘지 않" if h <= lim else "넘"), real=(["16단 + base 모두 40 µm 이상: 현실 범위(core 30–60, base 50–100) 안"] if False else []))


@solver("STACK_NMAX_A", ("SIP",), r"쌓을 수 있는 최대 core die 수를 구합니다")
def s_nmax_a(t, q):
    td = g(r"die 한 장의 두께가\s*" + F, t); gp = g(r"간극이 한 곳당\s*" + F, t); lim = g(r"상한은\s*" + F, t)
    n = math.floor((lim - td) / (td + gp))
    real = []
    if n > 16:
        real.append(f"E: 최대 {n} 단 — JEDEC 최대 16-Hi 를 넘는 값; base die 를 core 와 같은 {td:g} µm 로 둔 것도 비현실(base 50–100 µm)")
    return R(n, "장", f"{td:g}(n+1) + {gp:g}n ≤ {lim:g} → n ≤ ({lim:g}−{td:g})/({td:g}+{gp:g}) = {(lim-td)/(td+gp):.2f} → {n}", real=real)


@solver("STACK_NMAX_I", ("SIP",), r"쌓을 수 있는 core die 의 최대 장수")
def s_nmax_i(t, q):
    lim = g(r"상한이\s*" + F, t); b = g(r"base die 두께는\s*" + F, t); c = g(r"core die 는 한 장당\s*" + F, t); gp = g(r"접합 간극은\s*" + F, t)
    n = math.floor((lim - b) / (c + gp))
    real = []
    if n > 16:
        real.append(f"E: 최대 {n} 단 — JEDEC 최대 16-Hi 를 넘음(상부 mold·두께 산포 미반영). 결과가 16 이하가 되도록 die 두께·간극 상향 또는 '가상 구성' 명시")
    return R(n, "단", f"n ≤ ({lim:g}−{b:g})/({c:g}+{gp:g}) = {(lim-b)/(c+gp):.2f} → {n}", real=real)


@solver("CORE_TMAX", ("SIP",), r"core die 한 장의 두께를 얼마 이하로")
def s_tmax(t, q):
    lim = g(r"상한\s*" + F, t); b = g(r"base die 는\s*" + F, t); gp = g(r"간극은 die 사이마다\s*" + F, t); n = g(r"core die\s*" + F + r"\s*장을 쌓으면", t)
    v = (lim - b - n * gp) / n
    real = []
    if v > 60:
        real.append(f"I: 허용 core 두께 {v:.1f} µm — 현실 core 30–60 µm 범위 밖(8단은 높이 제약이 아님). 12/16단으로 바꾸면 의미 있는 판단이 됨")
    return R(v, "µm", f"t ≤ ({lim:g} − {b:g} − {n:g}×{gp:g}) ÷ {n:g} = {v:.2f} µm", real=real, tol=0.002)


@solver("STACK_H", ("SIP",), r"base die\s*[\d.]+\s*µm 위에\s*[\d.]+\s*µm 두께의 core die 를")
def s_h(t, q):
    b, c, n = g(r"base die\s*" + F + r"\s*µm 위에\s*" + F + r"\s*µm 두께의 core die 를\s*" + F, t, 3)
    gp = g(r"간극은\s*" + F, t); lim = g(r"상한\s*" + F, t)
    h = b + n * (c + gp)
    real = []
    if h < lim * 0.75:
        real.append(f"I: 높이 {h:g} µm 로 상한 {lim:g} µm 의 {h/lim*100:.0f} % — 네 보기 모두 '상한 안' 이라 판정 부분이 변별력 없음(설정 수정: 판정이 갈리도록 단수·두께 조정)")
    return R(h, "µm", f"H = {b:g} + {n:g}×({c:g}+{gp:g}) = {h:g} µm (상한 {lim:g})", real=real)


@solver("DIE_GAP_PAD", ("SIP", "THERM"), r"backside pad 보유")
def s_dgp(t, q):
    n = g(F + r"단 HBM", t)
    v = (n + 1, n, n)
    return R(v, "", f"die = {n:g}+1 = {n+1:g}, 간극 = {n:g} (base–core1 포함), pad 보유 = {n:g} (base 포함, 최상단 core 제외)",
             pick=lambda o: tuple(optnums(o)[:3]) if len(optnums(o)) >= 3 else None)


@solver("RETICLE", ("SIP",), r"reticle\)은 약\s*26 × 33 mm.*정사각형 부품")
def s_ret(t, q):
    m = g(r"'" + F + r"× reticle'", t); s = g(r"한 변이\s*" + F + r"\s*mm 인 정사각형", t)
    A = 26 * 33 * m; n = math.floor(A / s ** 2)
    real = []
    # 실제 배치(행·열 정수) 개수
    nrc = None
    return R((A, n), "mm²/개", f"A = 26×33×{m:g} = {A:,.0f} mm²; 개수 ≤ ⌊{A:,.0f} ÷ {s:g}²⌋ = {n}",
             pick=lambda o: tuple(optnums(o)[:2]) if len(optnums(o)) >= 2 else None, tol=0.01,
             note="면적 나눗셈 상한 — 실제 정사각 배치는 행·열 정수 제약으로 더 적다(예: 26×33 에 8 mm → 3×4=12개)")


@solver("RETICLE55", ("SIP",), r"5\.5× reticle")
def s_ret55(t, q):
    A = 26 * 33 * 5.5
    return R(A, "mm²", f"26×33×5.5 = {A:,.0f} mm²", tol=0.01)


# ---------------- THERM ----------------
def gap_R(t):
    L = re.findall(r"([A-Za-z가-힣 ()]+?)\s*" + F + r"\s*µm\s*\(\s*" + F + r"\s*W/mK\)", t)
    return [(nm.strip(), fnum(a), fnum(k)) for nm, a, k in L]


@solver("THERM_BASE", ("THERM",), r"1차원 정상상태로 단순화해 평가.*옳은 판단")
def s_tbase(t, q):
    N = g(F + r"단 스택", t); layers = gap_R(t); qf = g(r"열유속은\s*" + F, t); tt = g(r"온도는 방열 조건에 의해\s*" + F, t); lim = g(r"상한은\s*" + F, t)
    Rg = sum(a * 1e-6 / k for _, a, k in layers)
    dT = qf * 1e6 * Rg
    v11 = tt + dT * (N - 1); v12 = tt + dT * N
    real = []
    if v11 > 105:
        real.append(f"E: 최하단 core {v11:.0f} °C — DRAM 상한(85/95/105 °C)을 크게 넘는 비현실 결과(STANDARDS 2.4: 설정 자체 수정)")
    if tt >= lim:
        real.append(f"I: 최상단이 이미 상한({tt:g} ≥ {lim:g} °C) — 계산 없이 판정 가능, 변별력 없음")
    return R(v11, "°C", f"R_gap = Σt/k = {Rg:.3e} m²K/W; ΔT_gap = {qf}e6 × R = {dT:.2f} K; 최하단 core = {tt:g} + {N-1:g}×{dT:.2f} = {v11:.1f} °C (base 까지 {N:g} 간극이면 {v12:.1f} °C)",
             real=real)


@solver("THERM_QMAX", ("THERM",), r"허용 가능한 최대 열유속")
def s_qmax(t, q):
    N = g(F + r"단 스택", t); layers = gap_R(t); top = g(r"접합부 온도가\s*" + F, t); lim = g(r"상한\s*" + F, t)
    ng = g(r"적은\s*" + F + r"개", t) or N - 1
    Rg = sum(a * 1e-6 / k for _, a, k in layers)
    qv = (lim - top) / ng / Rg / 1e6
    qN = (lim - top) / N / Rg / 1e6
    real = []
    if N > 16:
        real.append(f"E: {N:g}단 — JEDEC 최대 16-Hi 초과(가상 구성 명시 또는 16단 이하로)")
    if qv < 0.08:
        real.append(f"I: 허용 열유속 {qv*100:.1f} W/cm² — 실제 HBM 열유속(수십 W/cm² 급, 15–25 W/cm² 보도)보다 한 자릿수 작아 결론 비현실")
    return R(qv, "W/mm²", f"R_gap = {Rg:.3e}; q = (T_lim−T_top)/(간극 {ng:g}·R) = ({lim:g}−{top:g})/({ng:g}×{Rg:.3e}) = {qv*1e6:.3g} W/m² = {qv:.3f} W/mm² (간극 {N:g} 개 규약이면 {qN:.3f})",
             real=real, tol=0.2)


@solver("THERM_PTOT", ("THERM",), r"평면 치수가.*총 발열량")
def s_ptot(t, q):
    a, b = g(r"평면 치수가\s*" + F + r"\s*×\s*" + F, t, 2); qf = g(r"열유속이\s*" + F, t)
    P = a * b * qf
    real = []
    if P > 35:
        real.append(f"E: 스택당 {P:.0f} W — 보고 범위(스택당 15–30 W)를 넘음; 열유속 {qf*100:g} W/cm² 도 상한(약 25 W/cm²) 초과")
    if a * b > 150:
        real.append(f"I: 평면 {a:g}×{b:g} mm = {a*b:.0f} mm² — HBM 스택 상면(약 75–120 mm²)보다 큼")
    return R(P, "W", f"P = q·A = {qf} × {a:g}×{b:g} = {qf} × {a*b:.1f} = {P:.1f} W", real=real)


@solver("TIM_DT", ("THERM",), r"TIM 의 (두께|열전도율)|TIM 두께")
def s_tim(t, q):
    dt = g(F + r"\s*µm (?:더 )?두꺼워", t); k = g(r"열전도율은\s*" + F, t); A = g(r"면적은\s*" + F + r"\s*cm²", t); P = g(r"전력은\s*" + F, t)
    if None in (dt, k, A, P):
        return None
    v = P * dt * 1e-6 / (k * A * 1e-4)
    return R(v, "°C", f"ΔT = P·Δt/(kA) = {P:g} × {dt:g}e-6 ÷ ({k:g} × {A:g}e-4) = {v:.2f} °C")


@solver("HEATFLUX", ("THERM",), r"열유속은 cm² 기준|열유속은 얼마")
def s_flux(t, q):
    P = g(F + r"\s*W 를 소비하는", t) or g(r"전력\s*" + F + r"\s*W", t); A = g(r"면적이\s*" + F + r"\s*mm²", t) or g(r"면적\s*" + F + r"\s*mm²", t)
    v = P / (A / 100)
    return R(v, "W/cm²", pick=lambda o: (optnums(o)[0]*100 if "W/mm²" in o else optnums(o)[0]), f=f"q = P/A = {P:g} W ÷ {A/100:g} cm² = {v:.2f} W/cm²", real=([f"I: {v:.1f} W/cm² — 보고 범위 15–25 W/cm² 밖"] if not 10 <= v <= 30 else []))


@solver("COOL_BUDGET", ("THERM",), r"냉각수 온도에서 접합부까지 허용되는 온도 상승 예산은 얼마입니까")
def s_cool(t, q):
    tin = g(r"입구 온도는\s*" + F, t); d = g(r"이미\s*" + F + r"\s*°C 올라", t); lim = g(r"상한은\s*" + F, t)
    v = lim - tin - d
    return R(v, "°C", f"{lim:g} − ({tin:g} + {d:g}) = {v:g} °C")


@solver("MOD_POWER", ("THERM",), r"메모리만으로 cold plate 가 빼내야 하는 열은 얼마")
def s_mod(t, q):
    n = g(r"HBM 스택이\s*" + F, t); p = g(r"스택 하나가\s*" + F, t)
    v = n * p
    real = []
    if n <= 3:
        real.append(f"I: 모듈당 {n:g} 스택 — 문항 자체 해설이 인용한 4–8 스택 범위보다 작음(참고)")
    return R(v, "W", f"{n:g} × {p:g} = {v:g} W", real=real)


@solver("TTSV_DT", ("THERM",), r"열저항을\s*[\d.]+\s*% 낮췄")
def s_ttsv(t, q):
    p = g(r"열저항을\s*" + F + r"\s*%", t); d = g(r"온도차는\s*" + F + r"\s*°C", t)
    v = d * (1 - p / 100)
    return R(v, "°C", f"ΔT' = {d:g} × (1 − {p:g}/100) = {v:.2f} °C",
             real=([f"I: die 한 간극의 ΔT {d:g} °C — 1D 모델의 간극당 수 K 수준보다 큼(구간 정의 명시 필요, 참고)"] if d >= 15 else []))


@solver("IFACE_DT", ("THERM",), r"면적 기준 열저항이\s*[\d.]+\s*mm²·K/W 로 측정")
def s_iface(t, q):
    r = g(r"열저항이\s*" + F, t); qf = g(r"열유속은\s*" + F + r"\s*W/cm²", t)
    v = r * qf / 100
    return R(v, "°C", f"ΔT = R″·q = {r:g} mm²K/W × {qf:g}/100 W/mm² = {v:.3f} °C")


@solver("IFACE_RATIO", ("THERM",), r"계면 온도차 비율")
def s_ir(t, q):
    return R(1.2 / 4.2, "배", "1.2/4.2 = 0.286")


@solver("COOL56", ("THERM",), r"HBM 구간 냉각수 온도를 56 °C")
def s_c56(t, q):
    return R(29, "°C", "85 − 56 = 29 °C")


@solver("MODRANGE", ("THERM",), r"모듈 전체의 HBM 전력 범위")
def s_mr(t, q):
    return R((60, 240), "W", "4×15 = 60, 8×30 = 240 W", pick=lambda o: tuple(optnums(o)[:2]))


# ---------------- DRAM / PROD ----------------
@solver("BW", ("DRAM",), r"Gb/s 로 동작.*총 대역폭은 얼마")
def s_bw(t, q):
    w = g(F + r"\s*bit 폭", t); s = g(r"전송 속도는\s*" + F, t); n = g(r"같은 스택이\s*" + F, t)
    v = w * s / 8 * n
    real = []
    gen = re.search(r"HBM(\d)(E?)", t)
    gens = gen.group(0) if gen else ""
    if gens == "HBM4" and w != 2048: real.append("E: HBM4 인데 I/O 폭이 2,048 bit 가 아님")
    if gens in ("HBM3", "HBM3E") and w != 1024: real.append(f"E: {gens} 인데 I/O 폭 {w:g} bit")
    if gens == "HBM3" and s > 6.4: real.append(f"E: HBM3 JEDEC 최대 6.4 Gb/s 초과({s:g})")
    if gens == "HBM4" and s < 6.4: real.append(f"I: HBM4 핀 속도 {s:g} Gb/s — JEDEC 8 Gb/s 대비 낮은 가정(명시 필요)")
    return R(v, "GB/s", f"{w:g} bit × {s:g} Gb/s ÷ 8 × {n:g} = {v:,.1f} GB/s", real=real, tol=0.01)


@solver("PCH", ("DRAM",), r"독립 채널로 나뉩니다")
def s_pch(t, q):
    w = g(r"인터페이스 폭이\s*" + F, t); c = g(F + r"\s*개의 독립 채널", t); p = g(r"다시\s*" + F + r"\s*개의 pseudo", t)
    v = (w / c, c * p)
    real = []
    known = {(1024, 8, 2), (1024, 16, 2), (2048, 32, 2)}
    if (w, c, p) not in known:
        real.append(f"E: '{w:g} bit · {c:g} 채널 · pseudo {p:g}' — 실재하지 않는 구성에 'HBM 스택' 이름 사용(STANDARDS 2.2 금지) → '가상의 메모리 인터페이스' 로 명시하거나 실제 세대 구성 사용")
    return R(v, "", f"채널 폭 = {w:g}/{c:g} = {w/c:g} bit, pseudo channel = {c:g}×{p:g} = {c*p:g}", real=real,
             pick=lambda o: tuple(optnums(o)[:2]) if len(optnums(o)) >= 2 else None)


@solver("ECC", ("DRAM",), r"보호 비트를 덧붙입니다")
def s_ecc(t, q):
    d = g(r"데이터\s*" + F + r"\s*bit 마다", t); p = g(F + r"\s*bit 의 보호", t)
    v = p / d * 100
    return R(v, "%", f"{p:g} ÷ {d:g} = {v:.2f} %")


@solver("RETENTION", ("DRAM",), r"보존 시간\(retention\)이")
def s_ret(t, q):
    T0, t0 = g(F + r"\s*°C 에서\s*" + F + r"\s*ms", t, 2); dT = g(r"온도가\s*" + F + r"\s*°C 오를 때마다", t); T1 = g(r"접합부 온도가\s*" + F, t)
    v = t0 / 2 ** ((T1 - T0) / dT)
    real = []
    t85 = t0 / 2 ** ((85 - T0) / dT)
    if t85 < 64:
        real.append(f"I: 이 모델로 85 °C 보존 {t85:.1g} ms < tREFW 64 ms — 정상 셀 가정과 모순(기준 보존 시간을 수백 ms~s 로)")
    return R(v, "ms", f"t = {t0:g} ÷ 2^(({T1:g}−{T0:g})/{dT:g}) = {v:.2f} ms", real=real)


@solver("CAPACITY", ("PROD",), r"모듈 전체의 메모리 용량은 byte")
def s_cap(t, q):
    d = g(F + r"\s*Gb 밀도", t); n = g(r"core die 를\s*" + F + r"\s*장", t); s = g(r"한 모듈에\s*" + F + r"\s*개", t)
    v = d * n / 8 * s
    real = []
    if d < 16:
        real.append(f"I: die {d:g} Gb — HBM3E/HBM4 의 24/32 Gb 대비 구세대 밀도(HBM2E 급, 참고)")
    if n not in (4, 8, 12, 16):
        real.append(f"E: {n:g}단 — 규격 단수(4/8/12/16)가 아님")
    return R(v, "GB", f"{d:g} Gb × {n:g} ÷ 8 × {s:g} = {v:g} GB", real=real)


@solver("BW_HBM4MAX", ("PROD",), r"표준 최대 조건에서 한 스택이 낼 수 있는 대역폭")
def s_bw4(t, q):
    return R(2.048, "TB/s", "2048 × 8 ÷ 8 = 2,048 GB/s ≈ 2 TB/s", tol=0.03)


@solver("CAP_HBM4MAX", ("PROD",), r"표준이 허용하는 최대 조합")
def s_c4(t, q):
    return R(64, "GB", "32 Gb × 16 ÷ 8 = 64 GB", pick=lambda o: optnums(o)[-1])


@solver("CAP_16HI", ("PROD",), r"16-Hi 48 GB")
def s_c16(t, q):
    return R(48, "GB", "24 Gb × 16 ÷ 8 = 48 GB", pick=lambda o: optnums(o)[-1] if 'Gb ×' in o else None)


# ---------------- MET ----------------
@solver("STACK_YIELD", ("MET",), r"양품일 확률은 대략 얼마입니까\?")
def s_sy(t, q):
    p = g(r"양품률이\s*" + F, t); y = g(r"접합 공정의 수율이\s*" + F, t); n = g(r"core die\s*" + F + r"\s*장을 쌓으므로", t)
    v = (p / 100) ** n * (y / 100) ** n * 100
    real = []
    if p < 97:
        real.append(f"I: KGD 양품률 {p:g} % 를 선별 없이 쌓는 설정 — 실제 공정은 KGD 선별 후 적층(문항 취지상 허용, 참고)")
    return R(v, "%", f"{p/100:g}^{n:g} × {y/100:g}^{n:g} = {v:.2f} %", real=real)


@solver("STACK_YIELD12", ("MET",), r"12단 스택을 조립하는데 core die 단품 양품률은")
def s_sy12(t, q):
    v = 0.98 ** 12 * 0.995 ** 12 * 100
    return R(v, "%", f"0.98¹² × 0.995¹² (접합 12회: base–core1 포함) = {v:.1f} % (해설의 11회 적용 시 {0.98**12*0.995**11*100:.1f} %)", tol=0.01)


@solver("TESTER", ("MET",), r"병렬 사이트 수가|병렬 사이트가")
def s_tester(t, q):
    s = g(r"병렬 사이트 수가\s*" + F, t) or g(r"병렬 사이트가\s*" + F, t)
    tt = g(r"시험 시간이\s*" + F + r"\s*초", t)
    N = g(F + r"\s*개를 (?:모두 )?시험", t)
    rounds = math.ceil(N / s); v = rounds * tt / 60
    return R(v, "분", f"⌈{N:g}/{s:g}⌉ = {rounds} 회전 × {tt:g} s = {rounds*tt:g} s = {v:g} 분",
             pick=lambda o: (optnums(o)[0] * 60 + (optnums(o)[1] if len(optnums(o)) > 1 else 0)) if '시간' in o else optnums(o)[0] if optnums(o) else None)


@solver("WASTE", ("MET",), r"헛되이 더 쌓게 되는 die 는 평균 몇 장")
def s_waste(t, q):
    m = g(r"core die 를\s*" + F + r"\s*장 쌓을 때마다", t); N = g(F + r"단 스택", t)
    v = (m - 1) / 2
    real = []
    if m == 1:
        real.append("E: 1 장마다 검사 → 낭비 0 장(자명). 보기 '평균 0.0 장' 과 '0 장' 이 같은 값이라 정답 2개")
    return R(v, "장", exact=True, f=f"구간 m={m:g} 장 안 균등 발생 → 평균 (m−1)/2 = {v:g} 장", real=real)


# ---------------- FA ----------------
@solver("TC_FAIL", ("FA",), r"cycle 까지 진행하며 누적 고장률을 기록")
def s_tc(t, q):
    pts = re.findall(F + r"\s*cycle 에서\s*" + F + r"\s*%", t)
    crit = g(r"판정 기준은\s*\d+\s*cycle 시점의 누적 고장률\s*" + F, t) or g(r"누적 고장률\s*" + F + r"\s*% 이하", t)
    last = fnum(pts[-1][1]) if pts else None
    judge = "만족" if last is not None and crit is not None and last <= crit else "벗어"
    return R(last, "%", f"1000 cycle 누적 {last:g} % vs 기준 {crit:g} % → {'만족' if judge=='만족' else '초과'}", judge=judge,
             real=["I: 판정 기준 '누적 고장률 n % 이하' 는 JEDEC 판정 기준이 아님(STANDARDS 2.3: JESD47 은 lot×77, 0 fail) → '사내 기준' 명시 필요"],
             pick=lambda o: None)


@solver("HCB_OVL", ("COW",), r"정렬 허용치를\s*±\s*[\d.]+\s*nm 로 설정")
def s_ovl(t, q):
    tol = g(r"허용치를\s*±\s*" + F, t); m = g(r"평균 오차가\s*" + F, t)
    judge = "벗어" if m > tol else "이내"
    return R(m, "nm", f"평균 오차 {m:g} nm vs 허용 ±{tol:g} nm → {'초과' if m>tol else '이내'}", judge=judge, pick=lambda o: None)
