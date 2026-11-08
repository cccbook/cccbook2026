# 08.2-Wilcoxon檢定
# 由 08.2-Wilcoxon檢定.md 抽出：以 python3.14 + PYTHONPATH 指向 rstatistics 執行

# --- 區塊 1 ---
import rstatistics as r

before = [62.0, 71.0, 58.0, 80.0, 66.0, 75.0, 69.0, 72.0, 64.0, 77.0]
after = [71.0, 78.0, 65.0, 84.0, 72.0, 81.0, 74.0, 79.0, 70.0, 83.0]

d = [after[i] - before[i] for i in range(len(before))]
ab = [abs(v) for v in d]
rk = r.rank(ab)
for i in range(len(d)):
    print(f"  d[{i+1}] = {d[i]:5.1f}   |d| = {ab[i]:4.1f}   名次 = {rk[i]:4.1f}   符號 = {'+' if d[i] > 0 else '-'}")
V = sum(rk[i] for i in range(len(d)) if d[i] > 0)
print("V+ =", V, "   零假設下的期望 E[V+] = n(n+1)/4 =", len(d) * (len(d) + 1) / 4)


# --- 區塊 2 ---
import rstatistics as r

before = [62.0, 71.0, 58.0, 80.0, 66.0, 75.0, 69.0, 72.0, 64.0, 77.0]
after = [71.0, 78.0, 65.0, 84.0, 72.0, 81.0, 74.0, 79.0, 70.0, 83.0]

h = r.wilcox_test(after, before, paired=True)
print(h)
print("  h.method         =", h.method)
print("  h.statistic_name =", h.statistic_name)
print("  h.statistic      =", h.statistic)
print("  h.p_value        =", h.p_value)
print("  h.alternative    =", h.alternative)
print("  h.null_name      =", h.null_name)


# --- 區塊 3 ---
import rstatistics as r

g1 = [23.0, 25.0, 28.0, 22.0, 26.0, 24.0, 27.0, 21.0]
g2 = [30.0, 32.0, 29.0, 33.0, 31.0, 35.0, 34.0, 28.0]
both = g1 + g2
rk2 = r.rank(both)
print("g1 =", g1)
print("g2 =", g2)
print("合併後的名次   :", rk2)
print("g1 的名次和 W =", sum(rk2[:len(g1)]))
print()

h2 = r.wilcox_test(g1, g2)
print(h2)
print("  h2.method =", h2.method, "  h2.statistic_name =", h2.statistic_name)


# --- 區塊 4 ---
import rstatistics as r

g1 = [23.0, 25.0, 28.0, 22.0, 26.0, 24.0, 27.0, 21.0]
g2 = [30.0, 32.0, 29.0, 33.0, 31.0, 35.0, 34.0, 28.0]

print("alternative='less'      :", r.wilcox_test(g1, g2, alternative="less").p_value)
print("alternative='greater'    :", r.wilcox_test(g1, g2, alternative="greater").p_value)
print("exact=False（正態近似）   :", r.wilcox_test(g1, g2, exact=False).p_value)
print("correct=False（不校正）  :", r.wilcox_test(g1, g2, exact=False, correct=False).p_value)


# --- 區塊 5 ---
import rstatistics as r

N = 2000
alpha = 0.05
n = 20

def sim(gen, delta, add_outlier):
    gt = 0; gw = 0
    for _ in range(N):
        x = gen(n)
        y = [v + delta for v in gen(n)]
        if add_outlier:
            j = int(gen(1)[0] * n) % n
            y = list(y)
            y[j] = y[j] + 12.0 * (1 if gen(1)[0] > 0.5 else -1)
        gt += (r.t_test(x, y).p_value < alpha)
        gw += (r.wilcox_test(x, y, exact=False).p_value < alpha)
    return gt / N, gw / N

print(f"重複次數 N = {N}，每組 n = {n}，水準 alpha = {alpha}")
print("（模擬用大樣本近似 exact=False，與 R 的 wilcox.test(exact=FALSE) 相同）")
print()

g = r.set_seed(11)
a = sim(lambda k: g.rnorm(k), 0.8, False)
print(f"情境 A（常態 N(0,1)，y 比 x 多 0.8sd）  t 檢定力 = {a[0]:.3f}   Wilcoxon 檢定力 = {a[1]:.3f}   差 = {a[0]-a[1]:+.3f}")

g = r.set_seed(11)
b = sim(lambda k: g.rnorm(k), 0.8, True)
print(f"情境 B（常態 + 1 個離群值，同樣位移）     t 檢定力 = {b[0]:.3f}   Wilcoxon 檢定力 = {b[1]:.3f}   差 = {b[0]-b[1]:+.3f}")

g = r.set_seed(11)
c = sim(lambda k: g.rnorm(k), 0.0, False)
print(f"情境 C（兩組相同，常態）                t 型一誤差 = {c[0]:.3f}   Wilcoxon 型一誤差 = {c[1]:.3f}")

g = r.set_seed(11)
d = sim(lambda k: g.rnorm(k), 0.0, True)
print(f"情境 D（兩組相同，含離群值）            t 型一誤差 = {d[0]:.3f}   Wilcoxon 型一誤差 = {d[1]:.3f}")
