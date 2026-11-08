# 09.5-預測與預測區間
# 由 09.5-預測與預測區間.md 抽出：以 python3.14 + PYTHONPATH 指向 rstatistics 執行

# --- 區塊 1 ---
import math
import rstatistics as r

WT = [2.620, 2.875, 2.320, 3.215, 3.440, 3.460, 3.570, 3.190, 3.150, 3.440,
      3.440, 4.070, 3.730, 3.780, 5.250, 5.424, 5.345, 2.200, 1.615, 1.835,
      2.465, 3.520, 3.435, 3.840, 3.845, 1.935, 2.140, 1.513, 3.170, 2.770,
      3.570, 2.780]
HP = [110.0, 110.0, 93.0, 110.0, 175.0, 105.0, 245.0, 62.0, 95.0, 123.0,
      123.0, 180.0, 180.0, 180.0, 205.0, 215.0, 230.0, 66.0, 52.0, 65.0,
      97.0, 150.0, 150.0, 245.0, 175.0, 66.0, 91.0, 113.0, 264.0, 175.0,
      335.0, 109.0]
MPG = [21.0, 21.0, 22.8, 21.4, 18.7, 18.1, 14.3, 24.4, 22.8, 19.2,
       17.8, 16.4, 17.3, 15.2, 10.4, 10.4, 14.7, 32.4, 30.4, 33.9,
       21.5, 15.5, 15.2, 13.3, 19.2, 27.3, 26.0, 30.4, 15.8, 19.7,
       15.0, 21.4]

# =============== 單元迴歸：CI vs PI ===============
m = r.lm(MPG, [WT], names=["wt"])
n = len(WT)
xb = r.mean(WT)
sxx = sum((xi - xb) ** 2 for xi in WT)
sd_res = (sum(e * e for e in m.residuals) / (n - 2)) ** 0.5
tcrit = r.qt(0.975, n - 2)

print("=== 資料範圍：wt 由 %.2f 到 %.2f，wt 平均 = %.4f ===" % (min(WT), max(WT), xb))
print("=== x0 = 3.0（資料範圍之內）===")
for x0 in [3.0]:
    h = 1.0 / n + (x0 - xb) ** 2 / sxx
    fit = m.coefficients[0] + m.coefficients[1] * x0
    hw_ci = tcrit * sd_res * math.sqrt(h)
    hw_pi = tcrit * sd_res * math.sqrt(1.0 + h)
    print("  h = %.6f, 擬合值 = %.4f" % (h, fit))
    print("  平均反應的 95%% CI : [%.4f, %.4f]  (半寬 %.4f)" % (fit - hw_ci, fit + hw_ci, hw_ci))
    print("  單一觀測的 95%% PI : [%.4f, %.4f]  (半寬 %.4f)" % (fit - hw_pi, fit + hw_pi, hw_pi))
print()
print("r.predict(..., interval='confidence')：")
print(r.predict(m, [[3.0]], interval="confidence"))
print("r.predict(..., interval='prediction')：")
print(r.predict(m, [[3.0]], interval="prediction"))

print()
print("=== 外插：x0 = 6.0, 8.0, 12.0（遠在資料範圍之外）===")
for x0 in [6.0, 8.0, 12.0]:
    h = 1.0 / n + (x0 - xb) ** 2 / sxx
    fit = m.coefficients[0] + m.coefficients[1] * x0
    hw_ci = tcrit * sd_res * math.sqrt(h)
    hw_pi = tcrit * sd_res * math.sqrt(1.0 + h)
    print("  x0 = %5.1f : 擬合值 %8.3f, CI 半寬 %8.3f, PI 半寬 %8.3f" % (x0, fit, hw_ci, hw_pi))
print()
print("r.predict(..., interval='confidence')：")
print(r.predict(m, [[6.0, 8.0, 12.0]], interval="confidence"))
print("r.predict(..., interval='prediction')：")
print(r.predict(m, [[6.0, 8.0, 12.0]], interval="prediction"))


# --- 區塊 2 ---
# ---------- 外插的視覺化：區間隨 x 遠離資料而爆開 ----------
grid = [1.0 + i * 0.25 for i in range(45)]      # 1.0 ~ 12.0
ci = r.predict(m, [grid], interval="confidence")
pi = r.predict(m, [grid], interval="prediction")
g = r.Graphics(width=7.2, height=5.0)
g.plot(WT, MPG, main="外插的危險：預測區間隨 x 遠離資料而爆開",
       xlab="車重 wt (1000 lbs)", ylab="每加侖里程 mpg",
       xlim=[1.0, 12.0], ylim=[0.0, 40.0], col="gray70")
g.lines(grid, ci.fit, col="black", lwd=2.0)
g.lines(grid, ci.lwr, col="blue", lwd=1.5)
g.lines(grid, ci.upr, col="blue", lwd=1.5)
g.lines(grid, pi.lwr, col="red", lwd=1.5)
g.lines(grid, pi.upr, col="red", lwd=1.5)
g.text(1.4, 36.0, "黑線：擬合值　藍線：平均反應 CI　紅線：單一觀測 PI", col="black")
g.save("img/09.5-extrapolation.svg")
print()
print("已存 09.5-extrapolation.svg")


# --- 區塊 3 ---
# =============== 多元迴歸 ===============
print()
print("=== 多元迴歸：mpg ~ wt + hp（mtcars, n = 32）===")
mm = r.lm(MPG, [WT, HP], names=["wt", "hp"])
print(mm.summary())

print("r.predict 新資料（wt = 3.0, hp = 150）：")
print(r.predict(mm, [[3.0], [150.0]], interval="confidence"))
print(r.predict(mm, [[3.0], [150.0]], interval="prediction"))

print("整批 32 台車的預測（只看前 5 筆）：")
pr = r.predict(mm, [WT, HP], interval="prediction")
for i in range(5):
    print("  第 %d 筆: fit = %7.3f, PI = [%7.3f, %7.3f]" % (i + 1, pr.fit[i], pr.lwr[i], pr.upr[i]))
