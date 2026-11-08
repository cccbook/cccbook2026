# 10.5-完整案例
# 由 10.5-完整案例.md 抽出：以 python3.14 + PYTHONPATH 指向 rstatistics 執行

import rstatistics as r

g = r.set_seed(2026)
n = 60
day = [round(v, 3) for v in g.rnorm(n, 100.0, 6.0)]
night = [round(v, 3) for v in g.rnorm(n, 102.5, 6.0)]

print("=== 正態性 ===")
for name, v in [("日班", day), ("夜班", night)]:
    h = r.shapiro_test(v)
    print(f"{name}: W = {h.statistic:.5f}, p = {h.p_value:.5f}")
    t, s = r.qqnorm_coords(v)
    qx = r.quantile(t, [0.25, 0.75])
    qy = r.quantile(s, [0.25, 0.75])
    slope = (qy[1] - qy[0]) / (qx[1] - qx[0])
    icept = qy[0] - slope * qx[0]
    print(f"   qqline slope = {slope:.4f} intercept = {icept:.4f} (sd={r.sd(v):.4f}, mean={r.mean(v):.4f})")
