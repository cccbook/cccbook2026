# 10.5-完整案例
# 由 10.5-完整案例.md 抽出：以 python3.14 + PYTHONPATH 指向 rstatistics 執行

import rstatistics as r

g = r.set_seed(2026)
n = 60
day = [round(v, 3) for v in g.rnorm(n, 100.0, 6.0)]
night = [round(v, 3) for v in g.rnorm(n, 102.5, 6.0)]

grp = [("日班", day), ("夜班", night)]

gr = r.Graphics(width=10.0, height=5.0, mfrow=[1, 2])
for k, (name, v) in enumerate(grp):
    if k > 0:
        gr.next_panel()
    t, s = r.qqnorm_coords(v)
    m = r.mean(v)
    sd = r.sd(v)
    z = [(q - m) / sd for q in v]
    tz, sz = r.qqnorm_coords(z)
    l, h = min(min(tz), min(sz)), max(max(tz), max(sz))
    gr.plot_window([l, h], [l, h])
    gr.title(f"{name}的標準化 Q-Q 圖", "理論分位數（標準常態）", "樣本分位數")
    xt = [q for q in r.pretty([l, h], 5) if l <= q <= h]
    gr.axis(1, xt, [f"{q:g}" for q in xt])
    gr.axis(2, xt, [f"{q:g}" for q in xt])
    gr.box()
    gr.lines([l, h], [l, h], "red")
    gr.points(tz, sz, pch=1, col="black")
    hs = r.shapiro_test(v)
    gr.text(0.15, -1.95, f"Shapiro-Wilk: W = {hs.statistic:.4f}", col="black")
    gr.text(0.15, -2.25, f"p = {hs.p_value:.3f} > 0.05（不拒絕常態）", col="black")
gr.save(\"img/10.5-qq.svg\")
print("已存 10.5-qq.svg")
