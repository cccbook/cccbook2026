# 03.5-期望值與變異數
# 由 03.5-期望值與變異數.md 抽出：以 python3.14 + PYTHONPATH 指向 rstatistics 執行

# --- 區塊 1 ---
import rstatistics as r

print(r.choose(10, 3))      # 二項 pmf 的係數
print(r.choose(52, 5))      # 5 張牌的發牌數
print(r.choose(42, 6))      # 6/42 樂透的組合數


# --- 區塊 2 ---
import rstatistics as r

g = r.set_seed(42)
N = 100000

def stats(xs):
    fx = list(map(float, xs))
    return r.mean(fx), r.var(fx)

rows = [
    ("Bin(10,0.5)",    5.0,    2.5,     stats(g.rbinom(N, 10, 0.5))),
    ("Pois(3)",        3.0,    3.0,     stats(g.rpois(N, 3.0))),
    ("Geom(0.3)",      7/3,    70/9,    stats(g.rgeom(N, 0.3))),
    ("NBin(2,0.3)",    14/3,   140/9,   stats(g.rnbinom(N, 2, 0.3))),
    ("Hyper(42,20,6)", 20/7,   1.3141,  stats(g.rhyper(N, 20, 22, 6))),
]

print(f"{'分配':>16} {'E 理論':>8} {'E 模擬':>8} {'Var 理論':>9} {'Var 模擬':>9}")
for name, te, tv, (sm, sv) in rows:
    print(f"{name:>16} {te:8.4f} {sm:8.4f} {tv:9.4f} {sv:9.4f}")


# --- 區塊 3 ---
g = r.set_seed(42)
xs = g.rpois(200000, 0.7)
fx = list(map(float, xs))
print(round(r.mean(fx), 4), round(r.var(fx), 4))   # Pois: 兩者應同為 0.7

# 超幾何校正因子：(N-n)/(N-1)
N, n, p = 1000, 20, 0.04
print(round((N - n) / (N - 1), 4), round(20 * p * (1 - p) * (N - n) / (N - 1) / (20 * p * (1 - p)), 4))
