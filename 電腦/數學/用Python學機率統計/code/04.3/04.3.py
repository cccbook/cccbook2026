# 04.3-指數與Gamma分配
# 由 04.3-指數與Gamma分配.md 抽出：以 python3.14 + PYTHONPATH 指向 rstatistics 執行

# --- 區塊 1 ---
import rstatistics as r

# 指數分配：r.dexp / r.pexp / r.qexp
print(r.dexp(1.0))                 # lambda=1，f(1) = e^-1
print(r.dexp(1.0, 2.0))            # lambda=2
print(r.pexp(3.0))                 # P(X<=3) = 1 - e^-3
print(r.qexp(0.5, 0.5))            # 中位數 = ln(2)/0.5

# 無記憶性：P(X>5) vs P(X>3+2 | X>3)
print(r.pexp(2.0, lower_tail=False))                     # P(X>2)
print(r.pexp(5.0, lower_tail=False) / r.pexp(3.0, lower_tail=False))  # P(X>5)/P(X>3)


# --- 區塊 2 ---
# Gamma：n 個 Exp(lambda) 之和 ~ Gamma(n, lambda)
print(r.dgamma(1.0, 1.0, 1.0))     # Gamma(1,1) = Exp(1)
print(r.dgamma(2.0, 2.0, 1.0))     # Gamma(2,1) 密度 x e^-x
print(r.pgamma(2.0, 3.0, 1.0))     # P(Gamma(3,1) <= 2)

# 模擬驗證：5 個 Exp(1) 相加 ~ Gamma(5, 1)
g = r.set_seed(42)
s = []
for _ in range(2000):
    e = g.rexp(5, 1.0)
    s.append(sum(e))
print(r.mean(s))                   # 理論 5
print(r.sd(s))                     # 理論 sqrt(5) ≈ 2.236


# --- 區塊 3 ---
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
g.save("img/04.3-gamma-shapes.svg")


# --- 區塊 4 ---
# 排隊例子：服務時間 Exp(0.5)（平均 2 分鐘），前 8 位客人
g = r.set_seed(101)
t = g.rexp(8, 0.5)
print([round(v, 2) for v in t])
print(r.mean(t))                  # 理論 1/0.5 = 2
print(r.pexp(2.0, 0.5))           # P(一位客人 2 分鐘內服務完)
