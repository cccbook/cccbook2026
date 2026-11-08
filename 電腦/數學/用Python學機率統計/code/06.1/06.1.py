# 06.1-點估計
# 由 06.1-點估計.md 抽出：以 python3.14 + PYTHONPATH 指向 rstatistics 執行

# --- 區塊 1 ---
import math
import rstatistics as r


def ascii_hist(x, nb=20, width=60):
    lo, hi = min(x), max(x)
    step = (hi - lo) / nb
    counts = [0] * nb
    for v in x:
        counts[min(nb - 1, int((v - lo) / step))] += 1
    mx = max(counts)
    for i, c in enumerate(counts):
        if c == 0:
            continue
        m = lo + (i + 0.5) * step
        bar = "#" * max(1, round(width * c / mx))
        print(f"{m:8.2f} |{bar} {c}")


B = 20000
mu, sigma = 50.0, 12.0

print("=== 母體 N(50, 12^2)：重複抽樣，看 x-bar 的抽樣分布如何隨 n 收斂 ===")
print(f"{'n':>4} {'mean(x-bar)':>12} {'bias':>10} {'sd(x-bar)':>10} {'sd/sigma':>9} {'RMSE':>8}")
for n in (1, 2, 5, 10, 25, 100):
    g = r.set_seed(100 + n)
    means = [r.mean(g.rnorm(n, mean=mu, sd=sigma)) for _ in range(B)]
    bias = r.mean(means) - mu
    sd = r.sd(means)
    rmse = math.sqrt(r.mean([(v - mu) ** 2 for v in means]))
    print(f"{n:>4} {r.mean(means):>12.4f} {bias:>10.4f} {sd:>10.4f} {sd/sigma:>9.4f} {rmse:>8.4f}")
print(f"理論：sd(x-bar) = sigma/sqrt(n)；n=1 時 {sigma/math.sqrt(1):.4f}，n=25 時 {sigma/math.sqrt(25):.4f}")


# --- 區塊 2 ---
print()
print("=== n = 1, 5, 25 的 x-bar 抽樣分布直方圖 ===")
for n in (1, 5, 25):
    g = r.set_seed(200 + n)
    means = [r.mean(g.rnorm(n, mean=mu, sd=sigma)) for _ in range(B)]
    print(f"--- n = {n} (sd = {r.sd(means):.3f}) ---")
    ascii_hist(means, nb=16)


# --- 區塊 3 ---
print()
print("=== 樣本變異數為什麼要除 n-1？（呼應 1.3 / 5.4）===")
g = r.set_seed(7)
s2n = []
s2m1 = []
for _ in range(B):
    s = g.rnorm(20, mean=mu, sd=sigma)
    m = r.mean(s)
    ss = sum((v - m) ** 2 for v in s)
    s2n.append(ss / 20)
    s2m1.append(ss / 19)
print(f"母體 sigma^2 = {sigma**2}")
print(f"  S2_n   (除以 n=20)  : mean = {r.mean(s2n):8.4f}  bias = {r.mean(s2n)-sigma**2:8.4f}  MSE = {r.mean([(v-sigma**2)**2 for v in s2n]):9.4f}")
print(f"  S2_(n-1)(除以 n-1=19): mean = {r.mean(s2m1):8.4f}  bias = {r.mean(s2m1)-sigma**2:8.4f}  MSE = {r.mean([(v-sigma**2)**2 for v in s2m1]):9.4f}")
print(f"  理論：MSE(S2_(n-1)) = 2*sigma^4/(n-1) = {2*sigma**4/19:.4f}，MSE(S2_n) = sigma^4*(2n-1)/n^2 = {sigma**4*39/400:.4f}")
print("  → 除以 n-1 才是對 sigma^2 的不偏估計（偏差剛好抵掉 1/(n-1) 的修正）")
print("  → 但 MSE 比較是另一回事：S2_n 雖然有偏，MSE 卻比較小！")


# --- 區塊 4 ---
print()
print("=== 取捨一：不偏但變異大 vs 微偏但集中 ===")
print("(a) 對稱常態母體估 mu：x-bar（不偏）vs 中位數（也幾乎不偏，但變異較大）")
n = 25
g = r.set_seed(31)
em = []
ed = []
for _ in range(B):
    s = g.rnorm(n, mean=mu, sd=sigma)
    em.append(r.mean(s))
    ed.append(r.median(s))
print(f"  n = {n}, 母體 N({mu}, {sigma}^2)")
print(f"    x-bar  : bias = {r.mean(em)-mu:>8.4f}  sd = {r.sd(em):>7.4f}  RMSE = {math.sqrt(r.mean([(v-mu)**2 for v in em])):>7.4f}")
print(f"    median : bias = {r.mean(ed)-mu:>8.4f}  sd = {r.sd(ed):>7.4f}  RMSE = {math.sqrt(r.mean([(v-mu)**2 for v in ed])):>7.4f}")
print(f"    理論 sd(median) = 1.2533*sigma/sqrt(n) = {1.2533*sigma/math.sqrt(n):.4f}")


# --- 區塊 5 ---
print("(b) 微偏但更集中：估 sigma^2 用 S2_n（除以 n）還是 S2_(n-1)（除以 n-1）？")
print("    n = 20，S2_n 的偏誤是 -sigma^2/n，但 MSE 反而比較小")
for nn in (5, 10, 20, 50):
    g = r.set_seed(60 + nn)
    a = []
    b = []
    for _ in range(B):
        s = g.rnorm(nn, mean=mu, sd=sigma)
        m = r.mean(s)
        ss = sum((v - m) ** 2 for v in s)
        a.append(ss / nn)
        b.append(ss / (nn - 1))
    mse_a = r.mean([(v - sigma**2) ** 2 for v in a])
    mse_b = r.mean([(v - sigma**2) ** 2 for v in b])
    print(f"    n = {nn:>3}: S2_n   bias = {r.mean(a)-sigma**2:>8.4f}  MSE = {mse_a:>10.4f}")
    print(f"           S2_(n-1) bias = {r.mean(b)-sigma**2:>8.4f}  MSE = {mse_b:>10.4f}   (MSE 較小的是 S2_n: {mse_a < mse_b})")
print("    理論：MSE(S2_(n-1)) = 2*sigma^4/(n-1)，MSE(S2_n) = sigma^4*(2n-1)/n^2")
print(f"          n=20 時分別是 {2*sigma**4/19:.4f} 與 {sigma**4*39/400:.4f} → S2_n 的 MSE 比較小")


# --- 區塊 6 ---
print()
print("=== 取捨二：右偏母體上，平均數 vs 中位數誰更有效？ ===")
g = r.set_seed(11)
xs = g.rexp(20000, rate=1.0 / 20.0)
true_med = 20.0 * math.log(2)
print(f"母體（指數，平均 20）：mean = {r.mean(xs):.3f}，median = {r.median(xs):.3f}，真中位數 = {true_med:.4f}")
for n in (10, 30):
    g = r.set_seed(300 + n)
    est_mean = []
    est_med = []
    for _ in range(B):
        s = g.rexp(n, rate=1.0 / 20.0)
        est_mean.append(r.mean(s))
        est_med.append(r.median(s))
    print(f"  n = {n}:")
    print(f"    x-bar  (目標 20.0000): bias = {r.mean(est_mean)-20.0:>8.4f}  sd = {r.sd(est_mean):>7.4f}  RMSE = {math.sqrt(r.mean([(v-20.0)**2 for v in est_mean])):>7.4f}")
    print(f"    median (目標 {true_med:.4f}): bias = {r.mean(est_med)-true_med:>8.4f}  sd = {r.sd(est_med):>7.4f}  RMSE = {math.sqrt(r.mean([(v-true_med)**2 for v in est_med])):>7.4f}")
print("  → 估『平均』用 x-bar 有效（不偏且 sd 小）；估『中位數』用樣本中位數（不偏但 O(1/n) 微偏、sd 略大）")
print("  → 真正在意的是目標參數是什麼：想估平均就別用中位數去湊")
