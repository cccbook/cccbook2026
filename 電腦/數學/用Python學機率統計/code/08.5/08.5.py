# 08.5-Kruskal-Wallis檢定
# 由 08.5-Kruskal-Wallis檢定.md 抽出：以 python3.14 + PYTHONPATH 指向 rstatistics 執行

# --- 區塊 1 ---
import rstatistics as r

g = r.set_seed(2024)
a = g.rnorm(20, 5.0, 1.0)
b = g.rnorm(20, 6.5, 1.0)
c = g.rnorm(20, 6.0, 1.0)
x = a + b + c
grp = ["A"] * 20 + ["B"] * 20 + ["C"] * 20

print("各組摘要：")
for name, v in [("A", a), ("B", b), ("C", c)]:
    print(f"  {name}: n={len(v)}  mean={r.mean(v):.3f}  median={r.median(v):.3f}")
print()

# 手算 H
allv = a + b + c
rk = r.rank(allv)
groups = ["A", "B", "C"]
n = len(allv)
print("合併後的名次（依組）：")
sums = []
counts = []
for gname in groups:
    rs = [rk[i] for i in range(n) if grp[i] == gname]
    print(f"  {gname}: {rs}")
    sums.append(sum(rs))
    counts.append(len(rs))
print("各組名次和 R_i =", sums)
print("各組人數 n_i =", counts)
k = 3
H = 12.0 / (n * (n + 1)) * sum(sums[i] ** 2 / counts[i] for i in range(k)) - 3.0 * (n + 1)
print("H =", round(H, 6))


# --- 區塊 2 ---
import rstatistics as r

g = r.set_seed(2024)
a = g.rnorm(20, 5.0, 1.0)
b = g.rnorm(20, 6.5, 1.0)
c = g.rnorm(20, 6.0, 1.0)
x = a + b + c
grp = ["A"] * 20 + ["B"] * 20 + ["C"] * 20

h = r.kruskal_test(x, grp)
print(h)
print("  h.method         =", h.method)
print("  h.statistic_name =", h.statistic_name)
print("  h.statistic      =", h.statistic)
print("  h.parameter      =", h.parameter)
print("  h.p_value        =", h.p_value)


# --- 區塊 3 ---
import rstatistics as r

g = r.set_seed(2024)
x = g.rnorm(20, 5.0, 1.0) + g.rnorm(20, 6.5, 1.0) + g.rnorm(20, 6.0, 1.0)
grp = ["A"] * 20 + ["B"] * 20 + ["C"] * 20

m = r.aov(x, grp)
print(m)
print()
print(m.summary())


# --- 區塊 4 ---
import rstatistics as r

N = 2000
alpha = 0.05
n = 20

def sim(gen, delta, add_outlier):
    ga = 0; gk = 0
    for _ in range(N):
        x = gen(n)
        y = [v + delta for v in gen(n)]
        z = [v + delta for v in gen(n)]
        if add_outlier:
            j = int(gen(1)[0] * n) % n
            y = list(y)
            y[j] = y[j] + 12.0 * (1 if gen(1)[0] > 0.5 else -1)
        a = r.aov(x + y + z, ["A"] * n + ["B"] * n + ["C"] * n)
        ga += (a.p < alpha)
        gk += (r.kruskal_test(x + y + z, ["A"] * n + ["B"] * n + ["C"] * n).p_value < alpha)
    return ga / N, gk / N

print(f"重複次數 N = {N}，每組 n = {n}，水準 alpha = {alpha}")
print()
g = r.set_seed(31)
a = sim(lambda k: g.rnorm(k), 0.8, False)
print(f"情境 A（常態，三組各差 0.8sd）  ANOVA 檢定力 = {a[0]:.3f}   Kruskal-Wallis 檢定力 = {a[1]:.3f}")
g = r.set_seed(31)
b = sim(lambda k: g.rnorm(k), 0.8, True)
print(f"情境 B（常態 + 1 個離群值）      ANOVA 檢定力 = {b[0]:.3f}   Kruskal-Wallis 檢定力 = {b[1]:.3f}")


# --- 區塊 5 ---
import rstatistics as r

g = r.set_seed(2024)
a = g.rnorm(20, 5.0, 1.0)
b = g.rnorm(20, 6.5, 1.0)
c = g.rnorm(20, 6.0, 1.0)
x = a + b + c
grp = ["A"] * 20 + ["B"] * 20 + ["C"] * 20

pairs = [("A", "B"), ("A", "C"), ("B", "C")]
ps = []
print("=== 事後兩兩 Wilcoxon ===")
for g1, g2 in pairs:
    x1 = [x[i] for i in range(len(x)) if grp[i] == g1]
    x2 = [x[i] for i in range(len(x)) if grp[i] == g2]
    h = r.wilcox_test(x1, x2, exact=False)
    ps.append(h.p_value)
    print(f"  {g1} vs {g2}: W = {h.statistic:.1f}, p = {h.p_value:.5f}")
print("  原始 p 值:", ps)
print()
for m in ["bonferroni", "holm", "BH"]:
    print(f"  p_adjust(method='{m}'):", [round(v, 8) for v in r.p_adjust(ps, method=m)])


# --- 區塊 6 ---
import rstatistics as r

gg = r.set_seed(7)
d1 = gg.rnorm(10, 5.0, 1.0)
d2 = gg.rnorm(30, 6.0, 1.0)
y = d1 + d2
gy = ["小組"] * 10 + ["大組"] * 30
print(r.kruskal_test(y, gy))
print()
print(r.wilcox_test(d1, d2, exact=False))
