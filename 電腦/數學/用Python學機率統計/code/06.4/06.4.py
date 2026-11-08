# 06.4-信賴區間怎麼讀
# 由 06.4-信賴區間怎麼讀.md 抽出：以 python3.14 + PYTHONPATH 指向 rstatistics 執行

# --- 區塊 1 ---
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


# --- 區塊 2 ---
print()
print("=== 畫區間圖：100 條橫線疊在真值線上 ===")
g3 = r.set_seed(2026)
ivs = []
for _ in range(B):
    s = g3.rnorm(n, mean=mu, sd=sigma)
    m = r.mean(s)
    se = r.sd(s) / math.sqrt(n)
    tc = r.qt(0.975, n - 1)
    ivs.append((m - tc * se, m + tc * se))

gr = r.Graphics(width=8.0, height=9.0)
gr.plot([35, 65], [0, 0], type="n", xlab="區間端點", ylab="模擬次數", xlim=[35, 65], ylim=[0, B + 2])
x0, y0, x1, y1 = [], [], [], []
rx0, ry0, rx1, ry1 = [], [], [], []
for i, (lo, hi) in enumerate(ivs):
    y = i + 1
    if lo <= mu <= hi:
        x0.append(lo); y0.append(y); x1.append(hi); y1.append(y)
    else:
        rx0.append(lo); ry0.append(y); rx1.append(hi); ry1.append(y)
gr.segments(x0, y0, x1, y1, col="black", lwd=1)
if rx0:
    gr.segments(rx0, ry0, rx1, ry1, col="red", lwd=2)
gr.segments([mu], [0], [mu], [B + 2], col="blue", lwd=2)
gr.text(50, B + 6, f"沒蓋住真值的 {B - cover} 個用紅色標出", adj=0.5)
gr.title(main="100 個 95% 信賴區間（真值 μ = 50，藍線）")
gr.save("img/06.4-ci-coverage.svg")
print("已存 06.4-ci-coverage.svg")


# --- 區塊 3 ---
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


# --- 區塊 4 ---
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


# --- 區塊 5 ---
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


# --- 區塊 6 ---
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
