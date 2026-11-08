# 04.5-Beta分配與組合的分布
# 由 04.5-Beta分配與組合的分布.md 抽出：以 python3.14 + PYTHONPATH 指向 rstatistics 執行

# --- 區塊 1 ---
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
g.save("img/04.5-beta-shapes.svg")


# --- 區塊 2 ---
import rstatistics as r

# Beta 密度形狀
print(r.dbeta(0.5, 1.0, 1.0))      # Beta(1,1) = 均勻 U(0,1)，密度恆 1
print(r.dbeta(0.3, 2.0, 5.0))
print(r.pbeta(0.5, 2.0, 5.0))      # CDF

g = r.set_seed(42)
print(g.rbeta(3, 2.0, 5.0))        # 亂數在 RNG 上

# r.beta(a,b)：B 函數常數；1/B(2,5) = 30 是密度前的常數
print(r.beta(2.0, 5.0))
print(1.0 / r.beta(2.0, 5.0))


# --- 區塊 3 ---
import rstatistics as r

# 數值積分（梯形法）：∫ dbeta(x; 2, 5) dx 應為 1
def trap(f, a, b, n):
    h = (b - a) / n
    s = 0.5 * (f(a) + f(b))
    for i in range(1, n):
        s += f(a + i * h)
    return s * h

f = lambda x: r.dbeta(x, 2.0, 5.0)
print(trap(f, 0.0, 1.0, 1000))
print(trap(f, 0.0, 1.0, 20))


# --- 區塊 4 ---
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
g2.save("img/04.5-gallery.svg")


# --- 區塊 5 ---
print(r.pcauchy(1) - r.pcauchy(-1))
print(r.pnorm(1) - r.pnorm(-1))
