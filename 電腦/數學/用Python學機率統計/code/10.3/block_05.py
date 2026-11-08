# 10.3-箱型圖Q-Q圖與ECDF
# 由 10.3-箱型圖Q-Q圖與ECDF.md 抽出：以 python3.14 + PYTHONPATH 指向 rstatistics 執行

import rstatistics as r

g = r.set_seed(11)
norm = [round(v, 4) for v in g.rnorm(60, 0.0, 1.0)]
t, s = r.qqnorm_coords(norm)
n = len(t)
mt = r.mean(t)
ms = r.mean(s)
slope = sum((a - mt) * (b - ms) for a, b in zip(t, s)) / sum((a - mt) ** 2 for a in t)
print("OLS slope =", round(slope, 6), " OLS intercept =", round(ms - slope * mt, 6))
print("樣本 sd =", round(r.sd(norm), 6), " 樣本 mean =", round(r.mean(norm), 6))
