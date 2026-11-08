# 10.5-完整案例
# 由 10.5-完整案例.md 抽出：以 python3.14 + PYTHONPATH 指向 rstatistics 執行

import rstatistics as r

g = r.set_seed(2026)
n = 60
day = [round(v, 3) for v in g.rnorm(n, 100.0, 6.0)]
night = [round(v, 3) for v in g.rnorm(n, 102.5, 6.0)]

grp = [("日班", day), ("夜班", night)]
stats = [r.boxplot_stats(v) for _, v in grp]
lo = min(s.stats[0] for s in stats)
hi = max(s.stats[4] for s in stats)

gr = r.Graphics(width=8.0, height=5.5)
gr.plot_window([0.4, 2.6], [lo, hi])
gr.title("兩班組產品重量的並排箱型圖", "", "產品重量 (公克)")
gr.axis(1, [1.0, 2.0], ["日班", "夜班"])
yt = [v for v in r.pretty([lo, hi], 5) if lo <= v <= hi]
gr.axis(2, yt, [f"{v:g}" for v in yt])
gr.box()
for i, ((name, v), s) in enumerate(zip(grp, stats)):
    xc = float(i + 1)
    bw = 0.24
    gr.segments([xc], [s.stats[0]], [xc], [s.stats[1]], "black")
    gr.segments([xc], [s.stats[3]], [xc], [s.stats[4]], "black")
    gr.segments([xc - bw / 2], [s.stats[0]], [xc + bw / 2], [s.stats[0]], "black")
    gr.segments([xc - bw / 2], [s.stats[4]], [xc + bw / 2], [s.stats[4]], "black")
    gr.rect(xc - bw / 2, s.stats[1], xc + bw / 2, s.stats[3], "black", "lightgray")
    gr.segments([xc - bw / 2], [s.stats[2]], [xc + bw / 2], [s.stats[2]], "black", 2.0)
    for o in s.out:
        gr.points([xc], [o], pch=1, col="black")
    gr.segments([xc + bw / 2 + 0.05], [s.conf[0]], [xc + bw / 2 + 0.05], [s.conf[1]], "red", 1.5)
gr.text(0.55, hi - 4.0, "紅線：中位數的 95% 信賴區間", col="red")
gr.mtext("n = 60 / 班；資料為模擬產生", side=1, line=4, cex=0.8)
gr.save(\"img/10.5-boxplot.svg\")
print("已存 10.5-boxplot.svg")
for (name, v), s in zip(grp, stats):
    print(f"{name}: 五數 = {[round(q,3) for q in s.stats]} conf = {[round(q,3) for q in s.conf]}")
