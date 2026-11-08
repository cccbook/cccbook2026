# 03.2-卜松分配
# 由 03.2-卜松分配.md 抽出：以 python3.14 + PYTHONPATH 指向 rstatistics 執行

# --- 區塊 1 ---
import rstatistics as r

for n, p in [(100, 0.1), (1000, 0.01), (10000, 0.001)]:
    lam = n * p                      # 固定為 10
    diffs = [abs(r.dbinom(k, n, p) - r.dpois(k, lam)) for k in range(10)]
    print(f"n={n:6d}  p={p:<6}  max|差| = {max(diffs):.2e}")


# --- 區塊 2 ---
import rstatistics as r

# 普魯士騎兵 1875-1894：死亡 k 匹人數（0 到 4 匹馬踢死）的軍團-年數
deaths = [0, 1, 2, 3, 4]
counts = [144, 91, 32, 11, 2]
tot = sum(counts)                                # 280 個軍團-年
lam = sum(k * c for k, c in zip(deaths, counts)) / tot   # 0.7

print(f"死亡數  觀察次數  觀察頻率   Pois(0.7) 理論")
for k, c in zip(deaths, counts):
    print(f"  {k}      {c:>4}    {c/tot:.4f}     {r.dpois(k, 0.7):.4f}")
print(f"  5+      {0:>4}    0.0000     {1 - r.ppois(4, 0.7):.5f}")


# --- 區塊 3 ---
g = r.set_seed(42)
n = 200000
xs = g.rpois(n, lambda_=0.7)

cnt = {}
for x in xs:
    cnt[int(x)] = cnt.get(int(x), 0) + 1
for k in range(6):
    print(k, round(r.dpois(k, 0.7), 5), round(cnt.get(k, 0) / n, 5))

fx = list(map(float, xs))
print(r.mean(fx), r.var(fx))   # 理論皆為 0.7


# --- 區塊 4 ---
import rstatistics as r

lam = 8.3
print(r.ppois(11, lam))          # P(Y <= 11)：一處理得完的機率
print(1 - r.ppois(11, lam))      # 超載機率
print(r.qpois(0.95, lam))        # 95% 分位數：容量該設多少？
