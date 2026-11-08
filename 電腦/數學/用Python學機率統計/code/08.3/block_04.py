# 08.3-KS檢定與Shapiro-Wilk
# 由 08.3-KS檢定與Shapiro-Wilk.md 抽出：以 python3.14 + PYTHONPATH 指向 rstatistics 執行

import rstatistics as r
import math

g = r.set_seed(2024)
x = [round(v, 4) for v in g.rnorm(50, 10.0, 2.0)]
xs = sorted(x)
n = len(xs)
dplus = 0.0
dminus = 0.0
for i in range(n):
    F = r.pnorm(xs[i], 10.0, 2.0)
    dplus = max(dplus, (i + 1) / n - F)
    dminus = max(dminus, F - i / n)
D = max(dplus, dminus)
print("單樣本 KS（x 對 N(10,2)）手算：D+ =", round(dplus, 6), " D- =", round(dminus, 6), " D =", round(D, 6))
print("漸近 p 值（手算）= 2*exp(-2*n*D^2) =", round(2 * math.exp(-2 * n * D * D), 6))
