# 06.4-信賴區間怎麼讀
# 由 06.4-信賴區間怎麼讀.md 抽出：以 python3.14 + PYTHONPATH 指向 rstatistics 執行

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
gr.save(\"img/06.4-ci-coverage.svg\")
print("已存 06.4-ci-coverage.svg")
