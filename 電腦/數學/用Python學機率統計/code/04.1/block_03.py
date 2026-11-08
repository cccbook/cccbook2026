# 04.1-密度函數與累計分配
# 由 04.1-密度函數與累計分配.md 抽出：以 python3.14 + PYTHONPATH 指向 rstatistics 執行

import rstatistics as r

# 均勻分配的密度與 CDF 曲線
g = r.Graphics(width=7.0, height=3.5, mfrow=[1, 2])

# 左圖：密度（自畫線段，因為 dunif 是分段常數）
g.plot([0, 2], [0, 1.2], type="n", main="dunif(x, 0, 1)", xlab="x", ylab="密度")
xs = [-0.4, 0.0, 0.0, 1.0, 1.0, 1.4]
ys = [0.0, 0.0, 1.0, 1.0, 0.0, 0.0]
g.lines(xs, ys, col="steelblue", lwd=2)
g.next_panel()
# 右圖：CDF
g.plot([0, 2], [0, 1.1], type="n", main="punif(x, 0, 1)", xlab="x", ylab="F(x)")
g.lines([-0.4, 0.0], [0.0, 0.0], col="darkred", lwd=2)
g.lines([0.0, 1.0], [0.0, 1.0], col="darkred", lwd=2)
g.lines([1.0, 1.4], [1.0, 1.0], col="darkred", lwd=2)
g.save(\"img/04.1-dunif-punif.svg\")

# curve() 的用法：畫標準常態密度（之後幾節會常用）
g2 = r.Graphics(width=4.5, height=4.0)
g2.plot([0, 0], [0, 0], type="n", main="dnorm(x)", xlab="x", ylab="")
g2.curve("dnorm", -4, 4, col="steelblue", lwd=2)
g2.save(\"img/04.1-dnorm-curve.svg\")
