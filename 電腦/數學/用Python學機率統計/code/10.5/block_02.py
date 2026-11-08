# 10.5-完整案例
# 由 10.5-完整案例.md 抽出：以 python3.14 + PYTHONPATH 指向 rstatistics 執行

import rstatistics as r

g = r.set_seed(2026)
n = 60
day = [round(v, 3) for v in g.rnorm(n, 100.0, 6.0)]
night = [round(v, 3) for v in g.rnorm(n, 102.5, 6.0)]

print("=== 描述統計 ===")
for name, v in [("日班", day), ("夜班", night)]:
    s = r.summary(v)
    print(f"--- {name} ---")
    print(s)
    print("  mean =", round(r.mean(v), 4), " sd =", round(r.sd(v), 4),
          " median =", r.median(v), " IQR =", round(r.IQR(v), 4))
    print("  離群值 =", [round(o, 3) for o in r.boxplot_stats(v).out])
