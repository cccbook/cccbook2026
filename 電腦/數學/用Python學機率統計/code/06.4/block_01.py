# 06.4-信賴區間怎麼讀
# 由 06.4-信賴區間怎麼讀.md 抽出：以 python3.14 + PYTHONPATH 指向 rstatistics 執行

import math
import rstatistics as r

mu, sigma, n = 50.0, 12.0, 30
B = 100
g = r.set_seed(2026)

print("=== 100 個 95% 信賴區間，看有多少個蓋住真值 μ = 50 ===")
intervals = []
cover = 0
for _ in range(B):
    s = g.rnorm(n, mean=mu, sd=sigma)
    m = r.mean(s)
    se = r.sd(s) / math.sqrt(n)
    tc = r.qt(0.975, n - 1)
    lo, hi = m - tc * se, m + tc * se
    intervals.append((lo, hi))
    if lo <= mu <= hi:
        cover += 1
print(f"蓋住真值的區間數 = {cover} / {B}（理論約 95）")
print("沒蓋住的區間：")
for i, (lo, hi) in enumerate(intervals):
    if not (lo <= mu <= hi):
        print(f"  第 {i+1:>3} 個：[{lo:.4f}, {hi:.4f}]")
print()
print("前 10 個區間：")
for i, (lo, hi) in enumerate(intervals[:10]):
    print(f"  {i+1:>3}: [{lo:.4f}, {hi:.4f}]  寬度 = {hi-lo:.4f}")
widths = [hi - lo for lo, hi in intervals]
print(f"平均寬度 = {r.mean(widths):.4f}，最小 = {min(widths):.4f}，最大 = {max(widths):.4f}")
