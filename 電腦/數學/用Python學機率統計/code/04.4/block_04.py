# 04.4-正態分配
# 由 04.4-正態分配.md 抽出：以 python3.14 + PYTHONPATH 指向 rstatistics 執行

import rstatistics as r

# 常態密度：不同 mu/sd 的曲線
g = r.Graphics(width=5.5, height=4.2)
xs = [i * 0.1 for i in range(-50, 71)]     # x = -5 .. 7
for mu, sd, col in [(0.0, 1.0, "steelblue"), (2.0, 0.6, "darkred"), (2.0, 1.8, "orange")]:
    ys = [r.dnorm(x, mu, sd) for x in xs]
    if mu == 0.0:
        g.plot(xs, ys, type="l", main="dnorm(x, mu, sd)", xlab="x", ylab="f(x)", col=col, lwd=2)
    else:
        g.lines(xs, ys, col=col, lwd=2)
g.save(\"img/04.4-dnorm-curves.svg\")

# qqnorm 概念預告：常態樣本的 QQ 圖
g2 = r.set_seed(42)
x = g2.rnorm(100, 165.0, 7.0)
g3 = r.Graphics(width=4.5, height=4.5)
g3.qqnorm(x, main="100 個常態樣本的 QQ 圖")
g3.qqline(x)
g3.save(\"img/04.4-qqnorm.svg\")
