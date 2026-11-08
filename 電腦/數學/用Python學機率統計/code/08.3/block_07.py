# 08.3-KS檢定與Shapiro-Wilk
# 由 08.3-KS檢定與Shapiro-Wilk.md 抽出：以 python3.14 + PYTHONPATH 指向 rstatistics 執行

import rstatistics as r

print("=== n 大時：微小的偏離也會顯著 ===")
for n in [30, 100, 300, 1000]:
    gg = r.set_seed(9)
    z = gg.rnorm(n)
    d1 = z
    d2 = [v + 0.15 * (v * v - 1.0) for v in z]
    hp = r.shapiro_test(d1)
    hq = r.shapiro_test(d2)
    print(f"  n = {n:5d}   常態: W = {hp.statistic:.4f}, p = {hp.p_value:.4g}   "
          f"微偏斜: W = {hq.statistic:.4f}, p = {hq.p_value:.4g}")
