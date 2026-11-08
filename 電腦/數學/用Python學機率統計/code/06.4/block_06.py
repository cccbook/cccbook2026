# 06.4-信賴區間怎麼讀
# 由 06.4-信賴區間怎麼讀.md 抽出：以 python3.14 + PYTHONPATH 指向 rstatistics 執行

print()
print("=== 先驗寬窄對後驗可信區間的影響 ===")
for tau in (20.0, 10.0, 5.0, 2.0):
    tau2 = tau * tau
    post_var = 1.0 / (1.0 / tau2 + nn / sig2)
    post_mean = post_var * (50.0 / tau2 + nn * xbar / sig2)
    sdp = math.sqrt(post_var)
    lo = post_mean + r.qnorm(0.025) * sdp
    hi = post_mean + r.qnorm(0.975) * sdp
    print(f"  先驗 N(50, {tau:g}^2): 後驗 N({post_mean:.4f}, {sdp:.4f}^2)，95% 可信區間 = [{lo:.4f}, {hi:.4f}]")
print("  頻率派 95% t 區間 = [{:.4f}, {:.4f}]".format(
    xbar - r.qt(0.975, nn-1)*11.0/math.sqrt(nn), xbar + r.qt(0.975, nn-1)*11.0/math.sqrt(nn)))
