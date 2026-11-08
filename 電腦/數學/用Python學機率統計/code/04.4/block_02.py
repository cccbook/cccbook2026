# 04.4-正態分配
# 由 04.4-正態分配.md 抽出：以 python3.14 + PYTHONPATH 指向 rstatistics 執行

# 標準化：身高 175cm，mu=165, sd=7  ->  z
mu, sd = 165.0, 7.0
x = 175.0
z = (x - mu) / sd
print(z)
print(r.pnorm(z))                       # 標準化後
print(r.pnorm(x, mu, sd))               # 直接算，結果相同
print(r.pnorm(x, mu, sd, lower_tail=False) * 100)  # P(X>175) 百分比

# qnorm：由機率反解分位數
print(r.qnorm(0.5))                     # 中位數
print(r.qnorm(0.975))                   # 95% 信賴區間的臨界值
print(r.qnorm(0.975) * sd + mu)         # 還原回身長尺度
