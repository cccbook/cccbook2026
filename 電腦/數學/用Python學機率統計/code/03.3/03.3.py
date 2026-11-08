# 03.3-幾何與負二項分配
# 由 03.3-幾何與負二項分配.md 抽出：以 python3.14 + PYTHONPATH 指向 rstatistics 執行

# --- 區塊 1 ---
import rstatistics as r

pmf = [r.dgeom(k, 0.3) for k in range(5)]
print([round(x, 5) for x in pmf])
print(r.pgeom(2, 0.3))   # 前 3 趟之內（含）就開張：P(X <= 2)


# --- 區塊 2 ---
g = r.set_seed(42)
n = 100000
xs = g.rgeom(n, 0.3)

cnt = {}
for x in xs:
    cnt[int(x)] = cnt.get(int(x), 0) + 1
for k in range(6):
    print(k, round(r.dgeom(k, 0.3), 5), round(cnt.get(k, 0) / n, 5))

fx = list(map(float, xs))
print(r.mean(fx), r.var(fx))   # 理論 (1-p)/p = 2.3333、(1-p)/p^2 = 7.7778


# --- 區塊 3 ---
g = r.set_seed(42)
n = 1000000
big = g.rgeom(n, 0.3)          # 失敗次數
surv = [x for x in big if x >= 3]      # 已失敗 >= 3 次（X >= 3）
wait = [x - 3 for x in surv]           # 之後又等了幾次
print(len(surv), r.mean(list(map(float, wait))))
print((1 - 0.3) ** 3)                  # P(X >= 3)，理論存活率


# --- 區塊 4 ---
import rstatistics as r

pmf = [r.dnbinom(k, size=2, prob=0.3) for k in range(6)]
print([round(x, 5) for x in pmf])
print(r.pnbinom(3, size=2, prob=0.3))   # 6 趟內（失敗 <= 3）完成 2 次成交

g = r.set_seed(42)
xs = g.rnbinom(100000, size=2, prob=0.3)
cnt = {}
for x in xs:
    cnt[int(x)] = cnt.get(int(x), 0) + 1
for k in range(6):
    print(k, round(r.dnbinom(k, 2, 0.3), 5), round(cnt.get(k, 0) / 100000, 5))

fx = list(map(float, xs))
print(r.mean(fx), r.var(fx))   # 理論 r(1-p)/p = 4.6667、r(1-p)/p^2 = 15.5556
