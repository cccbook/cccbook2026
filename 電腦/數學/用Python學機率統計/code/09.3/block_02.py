# 09.3-模型診斷
# 由 09.3-模型診斷.md 抽出：以 python3.14 + PYTHONPATH 指向 rstatistics 執行

AX = [
    [10.00, 8.00, 13.00, 9.00, 11.00, 14.00, 6.00, 4.00, 12.00, 7.00, 5.00],
    [10.00, 8.00, 13.00, 9.00, 11.00, 14.00, 6.00, 4.00, 12.00, 7.00, 5.00],
    [10.00, 8.00, 13.00, 9.00, 11.00, 14.00, 6.00, 4.00, 12.00, 7.00, 5.00],
    [8.00, 8.00, 8.00, 8.00, 8.00, 8.00, 8.00, 19.00, 8.00, 8.00, 8.00],
]
AY = [
    [8.04, 6.95, 7.58, 8.81, 8.33, 9.96, 7.24, 4.26, 10.84, 4.82, 5.68],
    [9.14, 8.14, 8.74, 8.77, 9.26, 8.10, 6.13, 3.10, 9.13, 7.26, 4.74],
    [7.46, 6.77, 12.74, 7.11, 7.81, 8.84, 6.08, 5.39, 8.15, 6.42, 5.73],
    [6.58, 5.76, 7.71, 8.84, 8.47, 7.04, 5.25, 12.50, 5.56, 7.91, 6.89],
]

print("Anscombe 四重奏：四組資料的 OLS 摘要")
print("組別   截距      斜率       R^2       調整 R^2   s")
for i in range(4):
    m = r.lm(AY[i], [AX[i]], names=["x"])
    sm = m.summary()
    print("  %d   %7.3f  %7.3f   %7.4f   %7.4f   %6.3f" %
          (i + 1, sm.estimates[0], sm.estimates[1], sm.r_squared, sm.adj_r_squared, sm.sigma))

gr = r.Graphics(width=7.5, height=7.0, mfrow=[2, 2])
for i in range(4):
    m = r.lm(AY[i], [AX[i]], names=["x"])
    b0 = m.coefficients[0]
    b1 = m.coefficients[1]
    gr.plot(AX[i], AY[i], main="Anscombe 組 %d" % (i + 1), xlab="x", ylab="y",
            col="black", xlim=[2.0, 15.0], ylim=[2.0, 15.0])
    xs = [2.0 + k * 13.0 / 40.0 for k in range(41)]
    gr.lines(xs, [b0 + b1 * xv for xv in xs], col="red", lwd=2.0)
    if i < 3:
        gr.next_panel()
gr.save(\"img/09.3-anscombe.svg\")
