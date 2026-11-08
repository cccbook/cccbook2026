# 09.3-模型診斷
# 由 09.3-模型診斷.md 抽出：以 python3.14 + PYTHONPATH 指向 rstatistics 執行

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
