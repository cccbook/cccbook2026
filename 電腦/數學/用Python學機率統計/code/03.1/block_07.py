# 03.1-伯努利試驗與二項分配
# 由 03.1-伯努利試驗與二項分配.md 抽出：以 python3.14 + PYTHONPATH 指向 rstatistics 執行

# 100 個環節、單一故障率 1%，至少一處故障
print(1 - (1 - 0.01) ** 100)                    # 公式
print(r.pbinom(0, 100, 0.01, lower_tail=False)) # P(Y > 0)，rstatistics 內建
