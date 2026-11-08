# 10.4-函數曲線柱狀圖與圖例
# 由 10.4-函數曲線柱狀圖與圖例.md 抽出：以 python3.14 + PYTHONPATH 指向 rstatistics 執行

import rstatistics as r

g = r.set_seed(21)

sim = g.rbinom(2000, 20, 0.25)
vals = list(range(min(sim), max(sim) + 1))
counts = [0.0] * len(vals)
for v in sim:
    counts[vals.index(v)] += 1.0
emp = [c / 2000.0 for c in counts]
theo = [r.dbinom(k, 20, 0.25) for k in vals]

gr = r.Graphics(width=11.0, height=5.0, mfrow=[1, 2])

# 左：Binomial(20, 0.25)
gr.plot_window([-0.7, 12.4], [0.0, 0.235])
gr.title("離散型：B(20, 0.25) 理論機率 vs 模擬長條", "k", "P(X = k)")
xt = [v for v in r.pretty([-0.7, 12.4], 5) if -0.7 <= v <= 12.4]
gr.axis(1, xt, [f"{v:g}" for v in xt])
yt = [v for v in r.pretty([0.0, 0.235], 5) if 0.0 <= v <= 0.235]
gr.axis(2, yt, [f"{v:g}" for v in yt])
gr.box()
for i, k in enumerate(vals):
    gr.rect(float(k) - 0.4, 0.0, float(k) + 0.4, emp[i], "black", "lightgray")
gr.segments([float(k) for k in vals], [0.0] * len(vals), [float(k) for k in vals], theo, "red", 1.5)
gr.points([float(k) for k in vals], theo, pch=19, col="red")
gr.text(12.2, 0.215, "長條 = 模擬相對頻率", col="black", adj=-1.0)
gr.text(12.2, 0.192, "紅點 = 理論機率 P(X=k)", col="red", adj=-1.0)

# 右：N(0,1)
gr.next_panel()
x = [round(v, 4) for v in g.rnorm(2000, 0.0, 1.0)]
br = r.pretty([min(x), max(x)], 20, 1)
nb = len(br) - 1
hc = [0.0] * nb
for v in x:
    for i in range(nb):
        if v > br[i] and v <= br[i + 1]:
            hc[i] += 1.0
            break
hw = br[1] - br[0]
hd = [c / (2000.0 * hw) for c in hc]
gr.plot_window([br[0], br[-1]], [0.0, 0.47])
gr.title("連續型：N(0,1) 理論密度 vs 模擬直方圖", "x", "密度")
xt = [v for v in r.pretty([br[0], br[-1]], 5) if br[0] <= v <= br[-1]]
gr.axis(1, xt, [f"{v:g}" for v in xt])
yt = [v for v in r.pretty([0.0, 0.47], 5) if 0.0 <= v <= 0.47]
gr.axis(2, yt, [f"{v:g}" for v in yt])
gr.box()
for i in range(nb):
    gr.rect(br[i], 0.0, br[i + 1], hd[i], "black", "lightgray")
gr.curve("dnorm", br[0], br[-1], 0.0, 1.0, n=201, col="red", lwd=1.5)
gr.text(3.4, 0.44, "長條 = 模擬直方圖", col="black", adj=-1.0)
gr.text(3.4, 0.415, "紅線 = 理論密度 f(x)", col="red", adj=-1.0)

gr.save(\"img/10.4-curve-fit.svg\")
print("已存 10.4-curve-fit.svg")
