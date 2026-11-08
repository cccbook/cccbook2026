# 10.3-箱型圖Q-Q圖與ECDF
# 由 10.3-箱型圖Q-Q圖與ECDF.md 抽出：以 python3.14 + PYTHONPATH 指向 rstatistics 執行

import rstatistics as r

g = r.set_seed(11)
a = [round(v, 4) for v in g.rnorm(40, 100.0, 8.0)]
b = [round(v, 4) for v in g.rnorm(40, 108.0, 8.0)]
c = [round(v, 4) for v in g.rnorm(40, 104.0, 14.0)]

grp = [("A 早班", a), ("B 晚班", b), ("C 混合", c)]
stats = [r.boxplot_stats(v) for _, v in grp]

for (name, v), s in zip(grp, stats):
    print(f"{name}: 五數 = {[round(q,3) for q in s.stats]}  鬚線內 = [{s.stats[0]:.3f}, {s.stats[4]:.3f}]  離群 = {[round(o,3) for o in s.out]}")

lo = min(s.stats[0] for s in stats)
hi = max(s.stats[4] for s in stats)

gr = r.Graphics(width=8.5, height=5.5)
gr.plot_window([0.4, 3.6], [lo, hi])
gr.title("三組產量的並排箱型圖", "", "產品重量 (公克)")
xt = [1.0, 2.0, 3.0]
gr.axis(1, xt, ["A 早班", "B 晚班", "C 混合"])
yt = [v for v in r.pretty([lo, hi], 5) if lo <= v <= hi]
gr.axis(2, yt, [f"{v:g}" for v in yt])
gr.box()

for i, ((name, v), s) in enumerate(zip(grp, stats)):
    xc = float(i + 1)
    bw = 0.22
    # 鬚線
    gr.segments([xc], [s.stats[0]], [xc], [s.stats[1]], "black")
    gr.segments([xc], [s.stats[3]], [xc], [s.stats[4]], "black")
    gr.segments([xc - bw / 2], [s.stats[0]], [xc + bw / 2], [s.stats[0]], "black")
    gr.segments([xc - bw / 2], [s.stats[4]], [xc + bw / 2], [s.stats[4]], "black")
    # 箱子
    gr.rect(xc - bw / 2, s.stats[1], xc + bw / 2, s.stats[3], "black", "lightgray")
    # 中位數
    gr.segments([xc - bw / 2], [s.stats[2]], [xc + bw / 2], [s.stats[2]], "black", 2.0)
    # 離群點
    for o in s.out:
        gr.points([xc], [o], pch=1, col="black")
    # 中位數信賴區間
    gr.segments([xc + bw / 2 + 0.04], [s.conf[0]], [xc + bw / 2 + 0.04], [s.conf[1]], "red", 1.5)
gr.save(\"img/10.3-box-groups.svg\")
print("已存 10.3-box-groups.svg")
