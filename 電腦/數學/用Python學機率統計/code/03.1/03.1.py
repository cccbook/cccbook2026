# 03.1-伯努利試驗與二項分配
# 由 03.1-伯努利試驗與二項分配.md 抽出：以 python3.14 + PYTHONPATH 指向 rstatistics 執行

# --- 區塊 1 ---
import rstatistics as r

# 丟 10 次公正銅板，各種正面次數的機率
pmf = [r.dbinom(k, size=10, prob=0.5) for k in range(11)]
print([round(x, 4) for x in pmf])


# --- 區塊 2 ---
# CDF 與分位數
print(r.pbinom(6, size=10, prob=0.5))    # P(Y <= 6)
print(r.qbinom(0.95, size=10, prob=0.5)) # 95% 分位數


# --- 區塊 3 ---
print(r.choose(10, 3))   # C(10,3) = 120
print(r.choose(10, 3) * 0.5**10)   # 應等於 dbinom(3, 10, 0.5)


# --- 區塊 4 ---
import rstatistics as r

g = r.set_seed(42)
n = 100000
xs = g.rbinom(n, size=10, prob=0.5)

cnt = {}
for x in xs:
    cnt[int(x)] = cnt.get(int(x), 0) + 1

ks = list(range(11))
theo = [r.dbinom(k, size=10, prob=0.5) for k in ks]
sim = [cnt.get(k, 0) / n for k in ks]

print(f"{'k':>2} {'理論 pmf':>10} {'模擬頻率':>10} {'差':>10}")
for k, t, s in zip(ks, theo, sim):
    print(f"{k:>2} {t:>10.4f} {s:>10.4f} {s - t:>10.4f}")


# --- 區塊 5 ---
g2 = r.Graphics(width=7.0, height=4.5)
g2.barplot(theo, [str(k) for k in ks])          # 理論值長條
for i, t in enumerate(theo):
    g2.rect(i + 0.6, 0, 0.8, sim[i])            # 模擬頻率描邊
g2.save("img/binom_pmf_sim.svg")


# --- 區塊 6 ---
fx = list(map(float, xs))
print(r.mean(fx))   # 理論 np = 5
print(r.var(fx))    # 理論 np(1-p) = 2.5


# --- 區塊 7 ---
# 100 個環節、單一故障率 1%，至少一處故障
print(1 - (1 - 0.01) ** 100)                    # 公式
print(r.pbinom(0, 100, 0.01, lower_tail=False)) # P(Y > 0)，rstatistics 內建
