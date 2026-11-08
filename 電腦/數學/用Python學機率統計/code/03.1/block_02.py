# 03.1-伯努利試驗與二項分配
# 由 03.1-伯努利試驗與二項分配.md 抽出：以 python3.14 + PYTHONPATH 指向 rstatistics 執行

# CDF 與分位數
print(r.pbinom(6, size=10, prob=0.5))    # P(Y <= 6)
print(r.qbinom(0.95, size=10, prob=0.5)) # 95% 分位數
