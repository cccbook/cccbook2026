# 09.3-模型診斷
# 由 09.3-模型診斷.md 抽出：以 python3.14 + PYTHONPATH 指向 rstatistics 執行

# --- 區塊 1 ---
import math
import rstatistics as r

g = r.set_seed(42)

# ---------- 四種有問題的資料 ----------
# (1) 曲線：真實關係是二次的，卻用直線去 fit
x1 = [float(i) for i in range(1, 21)]
y1 = [0.5 * xi + 6.0 * math.sin(xi / 3.0) + g.rnorm(1)[0] for xi in x1]

# (2) 異方差：變異數隨 x 增大
x2 = [float(i) for i in range(1, 31)]
y2 = [2.0 * xi + g.rnorm(1)[0] * math.sqrt(xi) for xi in x2]

# (3) 離群點：只有一筆資料被污染
x3 = [float(i) for i in range(1, 21)]
y3 = [1.0 + 2.0 * xi + g.rnorm(1)[0] for xi in x3]
y3[10] = y3[10] + 14.0

# (4) 槓桿點：x 遠離其他資料，y 卻剛好落在直線上
x4 = [float(i) for i in range(1, 21)]
y4 = [1.0 + 2.0 * xi + g.rnorm(1)[0] for xi in x4]
x4.append(26.0)
y4.append(1.0 + 2.0 * 26.0)

cases = [
    ("曲線（模型形式錯誤）", x1, y1, "09.3-a-curvature.svg"),
    ("異方差（變異數不齊）", x2, y2, "09.3-b-heteroscedastic.svg"),
    ("離群點（單筆污染）", x3, y3, "09.3-c-outlier.svg"),
    ("槓桿點（x 極端）", x4, y4, "09.3-d-leverage.svg"),
]

for name, xx, yy, fn in cases:
    m = r.lm(yy, [xx], names=["x"])
    res = [a - b for a, b in zip(yy, m.fitted_values)]
    fitted = m.fitted_values
    lo = min(res + [0.0])
    hi = max(res + [0.0])
    pad = 0.2 * (hi - lo)
    gr = r.Graphics(width=5.0, height=4.2)
    gr.plot(fitted, res, main=name, xlab="擬合值 fitted", ylab="殘差 residual",
            xlim=[min(fitted) - 0.5, max(fitted) + 0.5], ylim=[lo - pad, hi + pad],
            col="black")
    gr.abline(h=0.0, col="red", lwd=1.5)
    gr.save(fn)
    print("%-22s 殘差和 = %+.4f, 殘差平方和 = %.4f, s = %.4f" %
          (name, sum(res), sum(e * e for e in res), (sum(e * e for e in res) / (len(xx) - 2)) ** 0.5))


# --- 區塊 2 ---
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
gr.save("img/09.3-anscombe.svg")
