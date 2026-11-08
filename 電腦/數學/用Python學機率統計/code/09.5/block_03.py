# 09.5-預測與預測區間
# 由 09.5-預測與預測區間.md 抽出：以 python3.14 + PYTHONPATH 指向 rstatistics 執行

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
