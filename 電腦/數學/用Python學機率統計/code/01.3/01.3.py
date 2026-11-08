# 01.3-離散與分位
# 由 01.3-離散與分位.md 抽出：以 python3.14 + PYTHONPATH 指向 rstatistics 執行

# --- 區塊 1 ---
import rstatistics as r

g = r.set_seed(7)
x = g.rnorm(10, mean=50, sd=5)
print([round(v, 2) for v in x])
print(r.var(x), r.sd(x))


# --- 區塊 2 ---
import rstatistics as r

for n in (3, 10, 100):
    g2 = r.set_seed(123)
    biased   = r.mean([(lambda v: sum((a - r.mean(v)) ** 2 for a in v) / n)(g2.rnorm(n, mean=10, sd=2))
                       for _ in range(5000)])
    g2 = r.set_seed(123)
    unbiased = r.mean([r.var(g2.rnorm(n, mean=10, sd=2)) for _ in range(5000)])
    print(n, biased, unbiased)


# --- 區塊 3 ---
print(r.IQR(x), r.mad(x), r.mad(x, constant=1.0))


# --- 區塊 4 ---
y = x + [500.0]
print(r.mean(y), r.sd(y), r.median(y), r.mad(y))


# --- 區塊 5 ---
z = r.scale(x)
print([round(v, 3) for v in z])
print(r.mean(z), r.sd(z))


# --- 區塊 6 ---
g = r.set_seed(3)
a = [round(v, 1) for v in g.rnorm(20, mean=170, sd=3)]
b = [round(v, 1) for v in g.rnorm(20, mean=170, sd=10)]
print(r.mean(a), r.sd(a))
print(r.mean(b), r.sd(b))


# --- 區塊 7 ---
g2 = r.set_seed(9)
n = 500
u = g2.rnorm(n)
v = g2.rnorm(n)
s_u, s_v = r.sd(u), r.sd(v)
s_uv = r.sd([ui + vi for ui, vi in zip(u, v)])
print(s_u ** 2, s_v ** 2, s_uv ** 2, s_u ** 2 + s_v ** 2)
