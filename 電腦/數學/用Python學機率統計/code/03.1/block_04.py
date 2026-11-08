# 03.1-伯努利試驗與二項分配
# 由 03.1-伯努利試驗與二項分配.md 抽出：以 python3.14 + PYTHONPATH 指向 rstatistics 執行

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
