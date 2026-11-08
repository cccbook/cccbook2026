# 06.4-信賴區間怎麼讀
# 由 06.4-信賴區間怎麼讀.md 抽出：以 python3.14 + PYTHONPATH 指向 rstatistics 執行

print()
print("=== 對照：方法層級 vs 單次結果層級 ===")
g4 = r.set_seed(2026)
ivs = []
for _ in range(B):
    s = g4.rnorm(n, mean=mu, sd=sigma)
    m = r.mean(s)
    se = r.sd(s) / math.sqrt(n)
    tc = r.qt(0.975, n - 1)
    ivs.append((m - tc * se, m + tc * se))

cov = sum(1 for lo, hi in ivs if lo <= mu <= hi)
print("【方法層級】這個程序反覆使用，長期覆蓋率約 0.95")
print(f"  本次 100 次實測：{cov}/100 = {cov/100:.2f}")
print()
print("【單次結果層級】這一個區間是固定的數字")
lo, hi = ivs[0]
print(f"  第 1 個區間 = [{lo:.4f}, {hi:.4f}]")
print(f"  真值 μ = {mu:.4f} 在這個區間裡嗎？{'在' if lo <= mu <= hi else '不在'}（不是『機率 95%』，是『是』或『不是』）")
print()
print("【結論】95% 描述的是『用這個方法做 100 次，約有 95 次會蓋住』，")
print("         而不是『這一個區間有 95% 的機率蓋住』。")
