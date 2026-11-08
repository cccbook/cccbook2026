# 03.4-超幾何分配
# 由 03.4-超幾何分配.md 抽出：以 python3.14 + PYTHONPATH 指向 rstatistics 執行

# --- 區塊 1 ---
import rstatistics as r

for k in range(4):
    print(k, round(r.dhyper(k, m=20, n=22, k=6), 6))
print("至少一顆紅：", 1 - r.phyper(0, 20, 22, 6))
print("95% 分位數：", r.qhyper(0.95, 20, 22, 6))


# --- 區塊 2 ---
import rstatistics as r

N, K, n = 1000, 40, 20
print(1 - r.phyper(1, K, N - K, n))                    # 不放回（真實）
print(1 - r.pbinom(1, n, K / N))                       # 放回（二項近似）
print(n * K / N * (1 - K / N) * (N - n) / (N - 1))     # 超幾何變異數
print(n * K / N * (1 - K / N))                         # 二項變異數


# --- 區塊 3 ---
import rstatistics as r

for N in [50, 500, 5000, 50000]:
    m = round(N * 0.4)
    diffs = [abs(r.dhyper(k, m, N - m, 6) - r.dbinom(k, 6, 0.4)) for k in range(7)]
    print(f"N={N:<6} max|dhyper - dbinom| = {max(diffs):.2e}")


# --- 區塊 4 ---
g = r.set_seed(42)
xs = g.rhyper(100000, 20, 22, 6)

cnt = {}
for x in xs:
    cnt[int(x)] = cnt.get(int(x), 0) + 1
for k in range(4):
    print(k, round(r.dhyper(k, 20, 22, 6), 5), round(cnt.get(k, 0) / 100000, 5))

fx = list(map(float, xs))
print(r.mean(fx), r.var(fx))
print(6 * 20 / 42, 6 * (20/42) * (1 - 20/42) * (36/41))   # 理論 E、Var
