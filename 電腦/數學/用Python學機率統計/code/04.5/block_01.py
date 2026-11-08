# 04.5-Beta分配與組合的分布
# 由 04.5-Beta分配與組合的分布.md 抽出：以 python3.14 + PYTHONPATH 指向 rstatistics 執行

import rstatistics as r

g = r.Graphics(width=5.5, height=4.2)
xs = [i * 0.005 for i in range(1, 200)]    # x = 0.005 .. 0.995
for a, b, col in [(1.0, 1.0, "gray"), (2.0, 2.0, "darkred"), (2.0, 5.0, "steelblue"), (5.0, 5.0, "darkgreen"), (8.0, 2.0, "orange")]:
    ys = [r.dbeta(x, a, b) for x in xs]
    if a == 1.0:
        g.plot(xs, ys, type="l", main="Beta(a, b) 的密度", xlab="x", ylab="f(x)", ylim=[0, 3], col=col, lwd=2)
    else:
        g.lines(xs, ys, col=col, lwd=2)
g.text(0.30, 1.12, "1,1", 0.0, "gray", 10.0)
g.text(0.56, 1.62, "2,2", 0.0, "darkred", 10.0)
g.text(0.13, 1.75, "2,5", 0.0, "steelblue", 10.0)
g.text(0.50, 2.62, "5,5", 0.0, "darkgreen", 10.0)
g.text(0.82, 1.65, "8,2", 0.0, "orange", 10.0)
g.save(\"img/04.5-beta-shapes.svg\")
