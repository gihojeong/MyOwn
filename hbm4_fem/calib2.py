"""Tg 연화 모델(soft) 로 T0b 2점 → 실측 25/230 °C 동시 재현 여부 확인."""
import stack as S, fem2
from multiprocessing import Pool
JOBS = {f"V_{st}_soft{t}": S.case("hbm3e", 12, st, soft=True, t0b=float(t)) for st in ("design", "micron") for t in (400, 250)}
def one(n): R = fem2.run(n, JOBS[n]); return n, R[25]["w_dram"], R[230]["w_dram"]
if __name__ == "__main__":
    with Pool(4) as p:
        for n, a, b in p.imap_unordered(one, JOBS): print(f"{n}: 25°C {a:+.2f}  230°C {b:+.2f}", flush=True)
