# 10.4-函數曲線柱狀圖與圖例
# 由 10.4-函數曲線柱狀圖與圖例.md 抽出：以 python3.14 + PYTHONPATH 指向 rstatistics 執行

import rstatistics as r

g = r.set_seed(41)
x = [round(v, 4) for v in g.rnorm(50, 0.0, 1.0)]
t, s = r.qqnorm_coords(x)
qx = r.quantile(t, [0.25, 0.75])
qy = r.quantile(s, [0.25, 0.75])
slope = (qy[1] - qy[0]) / (qx[1] - qx[0])
icept = qy[0] - slope * qx[0]

gr = r.Graphics(width=6.5, height=6.0)
lo, hi = -3.0, 3.5
gr.plot_window([lo, hi], [lo, hi])
gr.title("Q-Q 圖與 95% 帶狀區", "理論分位數", "樣本分位數")
xt = [v for v in r.pretty([lo, hi], 5) if lo <= v <= hi]
gr.axis(1, xt, [f"{v:g}" for v in xt])
gr.axis(2, xt, [f"{v:g}" for v in xt])
gr.box()
# 95% 的參考帶（常態下 n=50 的近似 1.36/sqrt(n)），以 qqline 為中心
band = 1.36 / (50.0 ** 0.5)
bandx = [lo + (hi - lo) * i / 50.0 for i in range(51)]
mid = [icept + slope * v for v in bandx]
gr.polygon(bandx, [v + band for v in mid], "gray", "lightgray")
gr.polygon(bandx, [v - band for v in mid], "gray", "lightgray")
gr.lines([bandx[0], bandx[-1]], [mid[0], mid[-1]], "red")
gr.points(t, s, pch=1, col="black")
gr.save("/tmp/opencode/probe-band.svg")
print("band =", round(band, 4))
print("qqline slope =", round(slope, 4), " intercept =", round(icept, 4))
print("樣本 sd =", round(r.sd(x), 4), " 樣本 mean =", round(r.mean(x), 4))
