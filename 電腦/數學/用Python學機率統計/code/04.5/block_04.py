# 04.5-Beta分配與組合的分布
# 由 04.5-Beta分配與組合的分布.md 抽出：以 python3.14 + PYTHONPATH 指向 rstatistics 執行

import rstatistics as r

# 分配圖鑑：lnorm / logis / weibull / cauchy
g2 = r.Graphics(width=7.0, height=7.0, mfrow=[2, 2])
xs = [i * 0.1 for i in range(0, 61)]       # 0..6
ys = [r.dlnorm(x, 0.0, 0.7) for x in xs]
g2.plot(xs, ys, type="l", main="dlnorm(0, 0.7)", xlab="x", ylab="", col="steelblue", lwd=2)
ys = [r.dlogis(x, 0.0, 1.0) for x in xs]
g2.next_panel()
g2.plot(xs, ys, type="l", main="dlogis(0, 1)", xlab="x", ylab="", col="darkred", lwd=2)
ys = [r.dweibull(x, 1.5, 2.0) for x in xs]
g2.next_panel()
g2.plot(xs, ys, type="l", main="dweibull(1.5, 2)", xlab="x", ylab="", col="darkgreen", lwd=2)
ys = [r.dcauchy(x, 0.0, 1.0) for x in xs]
g2.next_panel()
g2.plot(xs, ys, type="l", main="dcauchy(0, 1)", xlab="x", ylab="", col="orange", lwd=2)
g2.save(\"img/04.5-gallery.svg\")
