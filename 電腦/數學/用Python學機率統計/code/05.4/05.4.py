# 05.4-卡方t與F分配的來源
# 由 05.4-卡方t與F分配的來源.md 抽出：以 python3.14 + PYTHONPATH 指向 rstatistics 執行

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
        if c == 0: continue
        m = lo + (i + 0.5) * step
        bar = "#" * max(1, round(width * c / mx))
        print(f"{m:8.2f} |{bar} {c}")

B = 20000

# ---- (1) 卡方：df 個獨立標準常態的平方和，自己從 rnorm 拼 ----
print("=== 卡方：從 3 個獨立標準常態的平方和造出 chisq(df=3) ===")
g = r.set_seed(21)
chi = []
for _ in range(B):
    z1, z2, z3 = g.rnorm(3)
    chi.append(z1*z1 + z2*z2 + z3*z3)
print(f"平均 = {r.mean(chi):.3f} (理論 df = 3)，變異數 = {r.var(chi):.3f} (理論 2*df = 6)")
ascii_hist(chi, nb=18)

print()
print("=== 卡方：從 10 個獨立標準常態的平方和造出 chisq(df=10) ===")
g = r.set_seed(21)
chi10 = []
for _ in range(B):
    zs = g.rnorm(10)
    chi10.append(sum(z*z for z in zs))
print(f"平均 = {r.mean(chi10):.3f} (理論 10)，變異數 = {r.var(chi10):.3f} (理論 20)")
ascii_hist(chi10, nb=18)

# ---- (2) t：正態 / sqrt(卡方/df) ----
print()
print("=== t：Z / sqrt(W/3)，Z~N(0,1)、W~chisq(3) 獨立，造出 t(3) ===")
g = r.set_seed(22)
tv = []
for _ in range(B):
    z = g.rnorm(1)[0]
    w = sum(x*x for x in g.rnorm(3))
    tv.append(z / math.sqrt(w / 3))
print(f"平均 = {r.mean(tv):.4f} (理論 0)，sd = {r.sd(tv):.4f} (理論 sqrt(df/(df-2)) = {math.sqrt(3/1):.4f})")
print("t(3) 與標準常態的尾部對照（|t| 超過 c 的比例）：")
for c in (1.96, 3.0, 5.0):
    emp = sum(1 for v in tv if abs(v) > c) / B
    print(f"  c = {c:4.2f}:  模擬 {emp:.4f}   標準常態 {2*(1-r.pnorm(c)):.4f}   t(3) {2*(1-r.pt(c, 3)):.4f}")

# ---- (3) F：兩個卡方之比 ----
print()
print("=== F：(W1/3) / (W2/7)，W1~chisq(3)、W2~chisq(7) 獨立，造出 F(3,7) ===")
g = r.set_seed(23)
fv = []
for _ in range(B):
    w1 = sum(x*x for x in g.rnorm(3))
    w2 = sum(x*x for x in g.rnorm(7))
    fv.append((w1/3) / (w2/7))
print(f"平均 = {r.mean(fv):.4f} (理論 df2/(df2-2) = {7/5:.4f})")
print(f"超過 4.35 的比例 = {sum(1 for v in fv if v > 4.35)/B:.4f}  (理論 1 - pf(4.35,3,7) = {1-r.pf(4.35, 3, 7):.4f})")


# --- 區塊 2 ---
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
        if c == 0: continue
        m = lo + (i + 0.5) * step
        bar = "#" * max(1, round(width * c / mx))
        print(f"{m:8.2f} |{bar} {c}")

B = 20000

print("=== 驗證 (n-1)S^2/sigma^2 ~ chisq(n-1)：母體 N(50,12^2)，n=10 ===")
g = r.set_seed(24)
mu, sigma, n = 50.0, 12.0, 10
stat = []
for _ in range(B):
    s = g.rnorm(n, mean=mu, sd=sigma)
    stat.append((n-1) * r.var(s) / sigma**2)
print(f"平均 = {r.mean(stat):.4f} (理論 n-1 = 9)")
print(f"落在 [qchisq(0.025,9), qchisq(0.975,9)] = [{r.qchisq(0.025, 9):.4f}, {r.qchisq(0.975, 9):.4f}] 的比例 = {sum(1 for v in stat if r.qchisq(0.025,9) <= v <= r.qchisq(0.975,9))/B:.4f} (理論 0.95)")
ascii_hist(stat, nb=16)
