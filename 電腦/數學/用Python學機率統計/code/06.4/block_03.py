# 06.4-信賴區間怎麼讀
# 由 06.4-信賴區間怎麼讀.md 抽出：以 python3.14 + PYTHONPATH 指向 rstatistics 執行

print()
print("=== 換不同 confidence level 看覆蓋率（每次 200 個區間）===")
for cl in (0.80, 0.90, 0.95, 0.99):
    g2 = r.set_seed(555)
    cov = 0
    R = 200
    for _ in range(R):
        s = g2.rnorm(n, mean=mu, sd=sigma)
        m = r.mean(s)
        se = r.sd(s) / math.sqrt(n)
        tc = r.qt(1 - (1 - cl) / 2, n - 1)
        if m - tc * se <= mu <= m + tc * se:
            cov += 1
    print(f"  confidence = {cl:.2f}: 覆蓋 {cov}/{R} = {cov/R:.3f}")
