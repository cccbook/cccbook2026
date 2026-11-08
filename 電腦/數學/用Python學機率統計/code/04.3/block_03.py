# 04.3-指數與Gamma分配
# 由 04.3-指數與Gamma分配.md 抽出：以 python3.14 + PYTHONPATH 指向 rstatistics 執行

import rstatistics as r

# 不同 shape 的 Gamma 密度
g = r.Graphics(width=5.5, height=4.2)
xs = [i * 0.1 for i in range(0, 121)]        # x = 0 .. 12
for shape, col in [(0.5, "gray"), (1.0, "darkred"), (2.0, "orange"), (5.0, "steelblue"), (10.0, "darkgreen")]:
    ys = [r.dgamma(x, shape, 1.0) for x in xs]
    if shape == 0.5:
        g.plot(xs, ys, type="l", main="Gamma(k, 1) 的密度", xlab="x", ylab="f(x)", col=col, lwd=2)
    else:
        g.lines(xs, ys, col=col, lwd=2)
g.text(7.5, 0.55, "k=0.5", 0.0, "gray", 10.0)
g.text(4.2, 0.62, "k=1", 0.0, "darkred", 10.0)
g.text(2.4, 0.42, "k=2", 0.0, "orange", 10.0)
g.text(4.5, 0.18, "k=5", 0.0, "steelblue", 10.0)
g.text(9.0, 0.125, "k=10", 0.0, "darkgreen", 10.0)
g.save(\"img/04.3-gamma-shapes.svg\")
