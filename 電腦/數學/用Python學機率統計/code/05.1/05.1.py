# 05.1-隨機樣本與抽樣分布
# 由 05.1-隨機樣本與抽樣分布.md 抽出：以 python3.14 + PYTHONPATH 指向 rstatistics 執行

# --- 區塊 1 ---
import rstatistics as r

def ascii_hist(x, nb=24, width=60):
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
        print(f"{m:7.2f} |{bar} {c}")

# ---- 母體：N(50, 12^2)，抽 10000 組樣本看 xbar 的分布 ----
g = r.set_seed(101)
mu, sigma = 50.0, 12.0
n = 30
B = 10000
xbars = []
s2s = []
for _ in range(B):
    s = g.rnorm(n, mean=mu, sd=sigma)
    xbars.append(r.mean(s))
    s2s.append(r.var(s))

print(f"母體: mu={mu}, sigma={sigma}, 樣本大小 n={n}, 重複 B={B} 次")
print(f"xbar 的平均 = {r.mean(xbars):.4f}  (理論值 mu = {mu})")
print(f"xbar 的 sd  = {r.sd(xbars):.4f}  (理論值 sigma/sqrt(n) = {sigma/(n**0.5):.4f})")
print(f"單一觀察值 X 的 sd = {r.sd(g.rnorm(5000, mean=mu, sd=sigma)):.4f}  (理論值 sigma = {sigma})")
print()
print("xbar 的直方圖：")
ascii_hist(xbars, nb=24)
print()
print("單一樣本 X 的直方圖（同比例尺對照，取前 10000 個）：")
ascii_hist(g.rnorm(10000, mean=mu, sd=sigma), nb=24)
