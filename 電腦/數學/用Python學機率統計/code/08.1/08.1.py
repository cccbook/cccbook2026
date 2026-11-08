# 08.1-為什麼需要非參數方法
# 由 08.1-為什麼需要非參數方法.md 抽出：以 python3.14 + PYTHONPATH 指向 rstatistics 執行

# --- 區塊 1 ---
import rstatistics as r

g = r.set_seed(42)
x = [g.rnorm(1)[0] for _ in range(20)]
print("原始資料   :", [round(v, 3) for v in x])
print("平均數     :", round(r.mean(x), 3))
print("中位數     :", round(r.median(x), 3))

y = x + [100.0]          # 儀器壞點：多了一筆 100
print("加入 100 後")
print("平均數     :", round(r.mean(y), 3))
print("中位數     :", round(r.median(y), 3))


# --- 區塊 2 ---
import rstatistics as r

# 三種母體下，「平均數估計」的穩定性：各抽 500 次、n=30
g = r.set_seed(7)
for name, gen in [("常態 N(0,1)", g.rnorm),
                  ("柯西（重尾）", g.rcauchy),
                  ("常態 + 10% 汙染 N(0,1)/N(0,25)", None)]:
    means, meds = [], []
    for _ in range(500):
        if gen is not None:
            x = gen(30)
        else:
            x = g.rnorm(30)
            for i in range(30):
                if g.runif(1)[0] < 0.1:
                    x[i] = x[i] * 5
        means.append(r.mean(x))
        meds.append(r.median(x))
    print(f"{name}")
    print(f"  平均數估計的標準差: {r.sd(means):.3f}   中位數估計的標準差: {r.sd(meds):.3f}")


# --- 區塊 3 ---
import rstatistics as r

xs = [(-5 + 10 * i / 200) for i in range(201)]
yn = [r.dnorm(x) for x in xs]
yc = [r.dcauchy(x) for x in xs]
g = r.Graphics(width=7.0, height=4.5)
g.plot(xs, yn)
g.lines(xs, yc, "red")
g.legend(-4.5, 0.42, ["常態 N(0,1)", "柯西 Cauchy(0,1)"])
g.save("img/08.1-tails.svg")


# --- 區塊 4 ---
import rstatistics as r

z = [2.5, 1.0, 4.0, 2.5, 8.0]
print(r.rank(z))
