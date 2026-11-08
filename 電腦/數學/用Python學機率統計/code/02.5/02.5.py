# 02.5-隨機變數
# 由 02.5-隨機變數.md 抽出：以 python3.14 + PYTHONPATH 指向 rstatistics 執行

# --- 區塊 1 ---
import rstatistics as r

# 擲兩枚銅板，隨機變數 X = 正面次數，pmf 與 CDF
g = r.set_seed(5)
N = 1_000_000
h1 = g.rbinom(N, 1, 0.5)
h2 = g.rbinom(N, 1, 0.5)
X = [a + b for a, b in zip(h1, h2)]

counts = [0, 0, 0]
for x in X:
    counts[x] += 1

print("k   pmf 模擬   pmf 理論   CDF 模擬   CDF 理論")
cdf_sim = 0.0
for k in range(3):
    pmf_sim = counts[k] / N
    pmf_th = r.dbinom(k, 2, 0.5)
    cdf_sim += pmf_sim
    cdf_th = r.pbinom(k, 2, 0.5)
    print(f"{k}   {pmf_sim:.4f}     {pmf_th:.4f}     {cdf_sim:.4f}     {cdf_th:.4f}")

mean_sim = r.mean([float(x) for x in X])
var_sim = r.var([float(x) for x in X])
mean_th = sum(k * r.dbinom(k, 2, 0.5) for k in range(3))
var_th = sum((k - 1.0)**2 * r.dbinom(k, 2, 0.5) for k in range(3))
print(f"\nE[X]  模擬 = {mean_sim:.5f}   理論 = {mean_th:.5f}")
print(f"Var[X] 模擬 = {var_sim:.5f}   理論 = {var_th:.5f}")


# --- 區塊 2 ---
import rstatistics as r

g = r.set_seed(88)
N = 1_000_000

# 連續隨機變數：X ~ Uniform(0, 1)，驗證 E[aX+b] = a E[X] + b
X = g.runif(N, 0.0, 1.0)
a, b = 3.0, -2.0
Y = [a * x + b for x in X]

print(f"E[X]  模擬 = {r.mean(X):.5f}   理論 = 0.50000")
print(f"E[Y]  模擬 = {r.mean(Y):.5f}")
print(f"a*E[X]+b 理論 = {a*0.5+b:.5f}   （= {a}*E[X] + ({b})）")
print(f"Var[X] 模擬 = {r.var(X):.5f}   理論 = 0.08333")
print(f"Var[Y] 模擬 = {r.var(Y):.5f}   理論 = {a*a*0.5*0.5*2/6:.5f}（= a^2 Var[X]）")


# --- 區塊 3 ---
import rstatistics as r

g = r.set_seed(1234)

# 用蒙地卡羅估 E[sqrt(U)]，U ~ Uniform(0,1)；理論值 = 積分 ∫√x dx = 2/3
for N in (10**3, 10**4, 10**5, 10**6):
    u = g.runif(N, 0.0, 1.0)
    est = r.mean([x**0.5 for x in u])
    print(f"N = {N:>8}: 估計 = {est:.5f}   理論 = {2/3:.5f}   誤差 = {abs(est-2/3):.5f}")
