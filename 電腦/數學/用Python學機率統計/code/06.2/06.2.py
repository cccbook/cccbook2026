# 06.2-平均值的信賴區間
# 由 06.2-平均值的信賴區間.md 抽出：以 python3.14 + PYTHONPATH 指向 rstatistics 執行

# --- 區塊 1 ---
import math
import rstatistics as r

mu, sigma = 50.0, 12.0

print("=== 1. z 區間（sigma 已知）：重複抽樣 1000 次看覆蓋率 ===")
B = 1000
g = r.set_seed(2024)
n = 25
z = r.qnorm(0.975)
cover = 0
widths = []
for _ in range(B):
    s = g.rnorm(n, mean=mu, sd=sigma)
    m = r.mean(s)
    lo, hi = m - z * sigma / math.sqrt(n), m + z * sigma / math.sqrt(n)
    if lo <= mu <= hi:
        cover += 1
    widths.append(hi - lo)
print(f"n = {n}, z = {z:.4f}, 1000 次中覆蓋真值的次數 = {cover}（覆蓋率 {cover/B:.3f}，理論 0.950）")
print(f"平均區間寬度 = {r.mean(widths):.4f}（理論 2*z*sigma/sqrt(n) = {2*z*sigma/math.sqrt(n):.4f}）")


# --- 區塊 2 ---
print()
print("=== 2. t 區間（sigma 未知，用 S 取代）：覆蓋率比較 ===")
for n in (5, 10, 25, 100):
    g = r.set_seed(300 + n)
    cover_z = 0
    cover_t = 0
    for _ in range(B):
        s = g.rnorm(n, mean=mu, sd=sigma)
        m = r.mean(s)
        sd = r.sd(s)
        se = sd / math.sqrt(n)
        zz = r.qnorm(0.975)
        tt = r.qt(0.975, n - 1)
        if m - zz * sigma / math.sqrt(n) <= mu <= m + zz * sigma / math.sqrt(n):
            cover_z += 1
        if m - tt * se <= mu <= m + tt * se:
            cover_t += 1
    print(f"  n = {n:>3}: z 區間覆蓋率 = {cover_z/B:.3f}   t 區間覆蓋率 = {cover_t/B:.3f}")


# --- 區塊 3 ---
print()
print("=== 2b. 母體非常態（右偏 Gamma）時，z 區間 vs t 區間 ===")
g = r.set_seed(999)
for n in (5, 10, 20, 40):
    cz = 0
    ct = 0
    for _ in range(B):
        s = g.rgamma(n, shape=4.0, scale=5.0)   # 平均 20、右偏
        m = r.mean(s)
        sd = r.sd(s)
        se = sd / math.sqrt(n)
        zz = r.qnorm(0.975)
        tt = r.qt(0.975, n - 1)
        if m - zz * sd / math.sqrt(n) <= 20.0 <= m + zz * sd / math.sqrt(n):
            cz += 1
        if m - tt * se <= 20.0 <= m + tt * se:
            ct += 1
    print(f"  n = {n:>3}: 用 S 當 sigma 的 z 區間覆蓋率 = {cz/B:.3f}   t 區間覆蓋率 = {ct/B:.3f}")


# --- 區塊 4 ---
print()
print("=== 3. 區間寬度如何隨 n 與信心水準改變 ===")
n = 25
sd = 12.0
print(f"  （用 S = {sd} 估 sigma，n = {n}）")
print(f"  {'confidence':>10} {'z_crit':>8} {'half-width':>11} {'full width':>11} {'n 需幾倍':>9}")
for cl in (0.80, 0.90, 0.95, 0.99):
    a = 1 - cl
    zc = r.qnorm(1 - a / 2)
    tc = r.qt(1 - a / 2, n - 1)
    hw_z = zc * sd / math.sqrt(n)
    hw_t = tc * sd / math.sqrt(n)
    print(f"  {cl:>10.2f} {zc:>8.4f} {hw_z:>11.4f} {2*hw_z:>11.4f} {1:>9.1f}")
print()
print("  想要寬度減半（n 固定不變），信心水準要降到多少？")
for cl in (0.80, 0.90, 0.95, 0.99):
    zc = r.qnorm(1 - (1 - cl) / 2)
    print(f"    {cl:.2f} 的區間寬度是 95% 區間的 {(zc/1.959964)**2:.3f} 倍")
print()
print("  n 要加倍，寬度才會乘上 1/sqrt(2) = 0.7071")
for n2 in (25, 50, 100, 200, 400, 800):
    hw = 1.959964 * sd / math.sqrt(n2)
    print(f"    n = {n2:>4}: 95% t 區間半寬 ≈ {hw:>7.4f}，全寬 ≈ {2*hw:>7.4f}")


# --- 區塊 5 ---
print()
print("=== 4. r.t_test 的區間輸出 ===")
g = r.set_seed(42)
x = g.rnorm(30, mean=52.0, sd=11.0)
for cl in (0.90, 0.95, 0.99):
    h = r.t_test(x, conf_level=cl)
    print(f"--- conf_level = {cl} ---")
    print(h)
    print(f"  estimate = {h.estimate[0]:.5f}，conf_int = [{h.conf_int[0]:.5f}, {h.conf_int[1]:.5f}]，寬度 = {h.conf_int[1]-h.conf_int[0]:.5f}")
    print()


# --- 區塊 6 ---
print("=== 4b. 手算驗證 t 區間的寬度 ===")
s = r.sd(x)
n = len(x)
for cl in (0.90, 0.95, 0.99):
    tc = r.qt(1 - (1 - cl) / 2, n - 1)
    hw = tc * s / math.sqrt(n)
    h = r.t_test(x, conf_level=cl)
    print(f"  conf_level={cl}: 手算 [{r.mean(x)-hw:.5f}, {r.mean(x)+hw:.5f}]，程式 [{h.conf_int[0]:.5f}, {h.conf_int[1]:.5f}]，一致 = {abs(r.mean(x)-hw-h.conf_int[0]) < 1e-6}")
print(f"  （S = {s:.5f}，n = {n}，df = {n-1}）")


# --- 區塊 7 ---
print()
print("=== 5. 覆蓋率：1000 次重複抽樣的 95% t 區間（n = 30）===")
g = r.set_seed(777)
n = 30
cover = 0
for _ in range(B):
    s = g.rnorm(n, mean=mu, sd=sigma)
    m = r.mean(s)
    se = r.sd(s) / math.sqrt(n)
    tc = r.qt(0.975, n - 1)
    if m - tc * se <= mu <= m + tc * se:
        cover += 1
print(f"覆蓋率 = {cover}/{B} = {cover/B:.3f}（理論 0.950）")
