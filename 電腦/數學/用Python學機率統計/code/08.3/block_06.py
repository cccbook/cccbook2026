# 08.3-KS檢定與Shapiro-Wilk
# 由 08.3-KS檢定與Shapiro-Wilk.md 抽出：以 python3.14 + PYTHONPATH 指向 rstatistics 執行

import rstatistics as r

print("=== 偏斜程度固定，n 變大 ===")
for n in [20, 50, 100, 200, 500]:
    gg = r.set_seed(9)
    z = gg.rnorm(n)
    d2 = [v + 0.6 * (v * v - 1.0) for v in z]
    hq = r.shapiro_test(d2)
    print(f"  n = {n:5d}   W = {hq.statistic:.4f}, p = {hq.p_value:.4g}")
