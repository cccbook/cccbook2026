# 09.5-預測與預測區間
# 由 09.5-預測與預測區間.md 抽出：以 python3.14 + PYTHONPATH 指向 rstatistics 執行

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
g.save(\"img/09.5-extrapolation.svg\")
print()
print("已存 09.5-extrapolation.svg")
