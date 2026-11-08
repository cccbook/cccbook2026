# 10.2-直方圖與密度估計
# 由 10.2-直方圖與密度估計.md 抽出：以 python3.14 + PYTHONPATH 指向 rstatistics 執行

import rstatistics as r

g = r.set_seed(7)
x = [round(v, 4) for v in g.rnorm(200, 0.0, 1.0)]

h = r.hist_stats(x, breaks="Sturges")
d = r.density_stats(x, bw="nrd0", n=512)

lo, hi = h.breaks[0], h.breaks[-1]
dx = [v for v in d.x if lo <= v <= hi]
dy = [d.y[d.x.index(v)] for v in dx]

gr = r.Graphics(width=8.0, height=6.0)
gr.plot_window([lo, hi], [0.0, 0.45])
gr.title("常態資料的直方圖與核密度估計", "x", "密度")
xt = [v for v in r.pretty([lo, hi], 5) if lo <= v <= hi]
gr.axis(1, xt, [f"{v:g}" for v in xt])
yt = [v for v in r.pretty([0.0, 0.45], 5) if 0.0 <= v <= 0.45]
gr.axis(2, yt, [f"{v:g}" for v in yt])
gr.box()
for i in range(len(h.counts)):
    gr.rect(h.breaks[i], 0.0, h.breaks[i + 1], h.density[i], "black", "lightgray")
gr.lines(dx, dy, "red", 1.5)
xs = [lo + (hi - lo) * i / 200.0 for i in range(201)]
ys = [r.dnorm(v, 0.0, 1.0) for v in xs]
gr.lines(xs, ys, "blue", 1.0)
gr.text(-1.7, 0.41, "藍：N(0,1) 理論密度", col="blue")
gr.text(-1.7, 0.375, "紅：核密度估計 (KDE)", col="red")
gr.save(\"img/10.2-hist-density.svg\")
print("已存 10.2-hist-density.svg")
print("直方圖密度 =", [round(v, 4) for v in h.density])
print("密度估計 bw =", d.bw, " 峰值 =", round(max(d.y), 4))
print("理論 N(0,1) 峰值 =", round(r.dnorm(0.0), 4))
print("樣本 sd =", round(r.sd(x), 4), " 樣本 mean =", round(r.mean(x), 4))
