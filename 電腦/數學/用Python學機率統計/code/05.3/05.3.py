# 05.3-大數法則與蒙地卡羅方法
# 由 05.3-大數法則與蒙地卡羅方法.md 抽出：以 python3.14 + PYTHONPATH 指向 rstatistics 執行

# --- 區塊 1 ---
import math
import rstatistics as r

# ---- (1) LLN：擲公平骰子的樣本平均收斂 ----
g = r.set_seed(3)
rolls = [float(v) for v in g.sample(6, 10000, replace=True)]  # 1..6
print("擲公平骰子，樣本平均隨 n 變化（母體平均 = 3.5）：")
running = 0.0
for n, v in enumerate(rolls, 1):
    running += v
    if n in (10, 100, 1000, 10000):
        print(f"  n = {n:5d}   xbar = {running/n:.4f}")

# ---- (2) Buffon 投針 (1777) 估 pi ----
print()
L = 1.0   # 針長
D = 2.0   # 平行線間距（>= L）
N = 200000
g = r.set_seed(11)
hits = 0
for _ in range(N):
    x = g.runif(1, 0.0, D / 2)[0]        # 針中點到最近線的距離
    theta = g.runif(1, 0.0, math.pi / 2)[0]
    if x <= (L / 2) * math.sin(theta):
        hits += 1
pi_hat = (2 * L * N) / (D * hits)
print(f"Buffon 投針 N={N}: 相交 {hits} 次, 估計 pi = {pi_hat:.4f}")


# --- 區塊 2 ---
import math
import rstatistics as r

def quarter_circle(N, seed):
    g = r.set_seed(seed)
    hits = 0
    for _ in range(N):
        x = g.runif(1, 0.0, 1.0)[0]
        y = g.runif(1, 0.0, 1.0)[0]
        if x * x + y * y <= 1.0:
            hits += 1
    return 4.0 * hits / N

print("=== 四分之一圓法估 pi ===")
for N in (1000, 10000, 100000, 1000000):
    print(f"N = {N:8d}   pi_hat = {quarter_circle(N, 5):.4f}   誤差 = {abs(quarter_circle(N, 5) - math.pi):.4f}")

# ---- 蒙地卡羅估積分 ∫0^1 e^x dx = e - 1 ----
print()
print("=== 蒙地卡羅估積分 I = ∫_0^1 e^x dx = e - 1 ≈ 1.718282 ===")
def mc_integral(N, seed):
    g = r.set_seed(seed)
    tot = 0.0
    for _ in range(N):
        tot += math.exp(g.runif(1, 0.0, 1.0)[0])
    return tot / N

for N in (1000, 10000, 100000, 1000000):
    print(f"N = {N:8d}   I_hat = {mc_integral(N, 8):.6f}   誤差 = {abs(mc_integral(N, 8) - (math.e - 1)):.6f}")

# ---- 誤差 ~ 1/sqrt(N) 的驗證：重複 500 次估同一積分，看各 N 的標準差 ----
print()
print("=== 誤差標準差 vs 1/sqrt(N)（每個 N 重複 500 次，seed 1..500）===")
for N in (1000, 10000, 100000):
    errs = []
    for seed in range(1, 501):
        errs.append(mc_integral(N, seed) - (math.e - 1))
    sd = r.sd(errs)
    print(f"N = {N:7d}: 誤差的 sd = {sd:.6f}   0.5/sqrt(N) = {0.5/N**0.5:.6f}   比值 = {sd*N**0.5:.4f}")
