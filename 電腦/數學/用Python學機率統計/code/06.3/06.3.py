# 06.3-比例的信賴區間
# 由 06.3-比例的信賴區間.md 抽出：以 python3.14 + PYTHONPATH 指向 rstatistics 執行

# --- 區塊 1 ---
import math
import rstatistics as r

z975 = r.qnorm(0.975)
print(f"z_(0.975) = {z975:.6f}\n")


def wald(x, n):
    ph = x / n
    se = math.sqrt(ph * (1 - ph) / n)
    return ph - z975 * se, ph + z975 * se


def wilson(x, n):
    ph = x / n
    z2 = z975 * z975
    den = 1 + z2 / n
    cen = (ph + z2 / (2 * n)) / den
    half = z975 * math.sqrt(ph * (1 - ph) / n + z2 / (4 * n * n)) / den
    return cen - half, cen + half


print("=== 1. Wald 與 Wilson 區間公式（同一組資料）===")
cases = [
    (40, 100, 0.40),
    (5, 100, 0.05),
    (0, 30, 0.00),
    (1, 30, 0.0333),
    (30, 30, 1.00),
    (15, 30, 0.50),
    (480, 1000, 0.48),
]
print(f"{'x':>5} {'n':>6} {'p-hat':>7} {'Wald':>22} {'Wilson':>22}")
for x, n, p in cases:
    w = wald(x, n)
    wi = wilson(x, n)
    print(f"{x:>5} {n:>6} {p:>7.4f} [{w[0]:>9.4f}, {w[1]:>9.4f}] [{wi[0]:>9.4f}, {wi[1]:>9.4f}]")
print("→ Wald 在 x=0 或 x=n 時會給出退化的 [0, 0] 或 [1, 1]；Wilson 永遠落在 [0,1] 且保有寬度")


# --- 區塊 2 ---
print()
print("=== 2. r.prop_test 的區間輸出（Wald + 連續性校正）===")
for x, n in ((40, 100), (5, 100)):
    h = r.prop_test(x, n)
    print(f"--- prop_test(x={x}, n={n}) ---")
    print(h)
    print(f"  conf_int = [{h.conf_int[0]:.7f}, {h.conf_int[1]:.7f}]，estimate = {h.estimate[0]:.7f}")
    print()


# --- 區塊 3 ---
print()
print("=== 2b. r.binom_test 的 Clopper-Pearson 精確區間 ===")
for x, n in ((40, 100), (5, 100), (0, 30)):
    h = r.binom_test(x, n)
    print(f"--- binom_test(x={x}, n={n}) ---")
    print(h)
    print(f"  conf_int = [{h.conf_int[0]:.7f}, {h.conf_int[1]:.7f}]")
    print()


# --- 區塊 4 ---
print()
print("=== 3. 覆蓋率比較：Wald vs Wilson ===")
B = 2000


def coverage(p_true, n, reps=B, seed=99):
    g = r.set_seed(seed)
    cw = 0
    ci = 0
    for _ in range(reps):
        x = sum(g.rbinom(n, 1, p_true))
        w = wald(x, n)
        wi = wilson(x, n)
        if w[0] <= p_true <= w[1]:
            cw += 1
        if wi[0] <= p_true <= wi[1]:
            ci += 1
    return cw / reps, ci / reps


print(f"{'p_true':>7} {'n':>6} {'Wald 覆蓋率':>12} {'Wilson 覆蓋率':>14}")
for p_true, n in ((0.5, 30), (0.5, 100), (0.5, 500),
                  (0.1, 10), (0.1, 30), (0.1, 100),
                  (0.02, 20), (0.02, 100),
                  (0.9, 20), (0.9, 30)):
    cw, ci = coverage(p_true, n)
    print(f"{p_true:>7.2f} {n:>6} {cw:>12.3f} {ci:>14.3f}")
print("（理論都應接近 0.95；Wald 在 n 小或 p 極端時會嚴重失準）")


# --- 區塊 5 ---
print()
print("=== 4. n 要多大才能把比例估在 ±3% 以內？ ===")
print("   （用最保守的 p-hat = 0.5，因為 p(1-p) 在 0.5 最大）")
for cl in (0.95, 0.99):
    zc = r.qnorm(1 - (1 - cl) / 2)
    for eps in (0.03, 0.05, 0.02):
        n = zc**2 * 0.25 / eps**2
        print(f"  信心水準 {cl:.2f}、誤差 ±{eps:.0%}：n >= {math.ceil(n)}")
print()
print("   若已知母體比例 p = 0.2，所需 n 更小：")
zc = z975
for eps in (0.03, 0.05):
    n = zc**2 * 0.2 * 0.8 / eps**2
    print(f"    信心水準 0.95、誤差 ±{eps:.0%}：n >= {math.ceil(n)}")


# --- 區塊 6 ---
print()
print("=== 4b. 驗證：n = 1068 時的實際覆蓋率 ===")
g = r.set_seed(1212)
n = 1068
cw = 0
ci = 0
R = 500
for _ in range(R):
    x = sum(g.rbinom(n, 1, 0.5))
    w = wald(x, n)
    wi = wilson(x, n)
    if w[0] <= 0.5 <= w[1]:
        cw += 1
    if wi[0] <= 0.5 <= wi[1]:
        ci += 1
print(f"p_true = 0.5, n = {n}: Wald 覆蓋率 = {cw/R:.3f}，Wilson 覆蓋率 = {ci/R:.3f}")
print(f"區間半寬約 = {z975*math.sqrt(0.25/n):.4f}（目標 0.03）")


# --- 區塊 7 ---
print()
print("=== 5. 同一個 p-hat=0.4，n 不同時 Wald 與 Wilson 的長度 ===")
print(f"{'n':>6} {'Wald 寬度':>12} {'Wilson 寬度':>13} {'Wald 下限':>11} {'Wilson 下限':>13}")
for n in (10, 20, 50, 100, 500, 2000):
    x = round(0.4 * n)
    w = wald(x, n)
    wi = wilson(x, n)
    print(f"{n:>6} {w[1]-w[0]:>12.4f} {wi[1]-wi[0]:>13.4f} {w[0]:>11.4f} {wi[0]:>13.4f}")
