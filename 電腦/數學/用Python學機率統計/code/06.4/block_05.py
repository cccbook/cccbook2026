# 06.4-信賴區間怎麼讀
# 由 06.4-信賴區間怎麼讀.md 抽出：以 python3.14 + PYTHONPATH 指向 rstatistics 執行

print()
print("=== Bayesian 可信區間：後驗分布 95% 區間 ===")
# 先驗：mu ~ N(50, 20^2)，資料：n=30, x-bar=52.0, s=11.0
tau2 = 20.0 ** 2
sig2 = 11.0 ** 2
nn = 30
xbar = 52.0
post_var = 1.0 / (1.0 / tau2 + nn / sig2)
post_mean = post_var * (50.0 / tau2 + nn * xbar / sig2)
sd_post = math.sqrt(post_var)
lo = post_mean + r.qnorm(0.025) * sd_post
hi = post_mean + r.qnorm(0.975) * sd_post
print(f"先驗：mu ~ N(50, 20^2)；資料：n = {nn}, x-bar = {xbar}, s = 11")
print(f"後驗：mu ~ N({post_mean:.4f}, {sd_post:.4f}^2)")
print(f"後驗 95% 可信區間 = [{lo:.4f}, {hi:.4f}]")
print(f"對照：頻率派 95% t 區間 = [{xbar - r.qt(0.975, nn-1)*11.0/math.sqrt(nn):.4f}, {xbar + r.qt(0.975, nn-1)*11.0/math.sqrt(nn):.4f}]")
print("→ 先驗很寬（sd=20）時，後驗區間幾乎由資料決定，兩者接近；")
print("  先驗很窄（sd=2）時，後驗會被先驗拉回去。")
