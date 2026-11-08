# 10.2-直方圖與密度估計
# 由 10.2-直方圖與密度估計.md 抽出：以 python3.14 + PYTHONPATH 指向 rstatistics 執行

import rstatistics as r

g = r.set_seed(7)
x = [round(v, 4) for v in g.rnorm(200, 0.0, 1.0)]

h = r.hist_stats(x, breaks="Sturges")
print("counts =", h.counts)
print("density =", [round(v, 5) for v in h.density])
print("sum(counts) =", sum(h.counts), " sum(density)*寬 =", round(sum(v * (h.breaks[1]-h.breaks[0]) for v in h.density), 10))
