# 03.1-伯努利試驗與二項分配
# 由 03.1-伯努利試驗與二項分配.md 抽出：以 python3.14 + PYTHONPATH 指向 rstatistics 執行

print(r.choose(10, 3))   # C(10,3) = 120
print(r.choose(10, 3) * 0.5**10)   # 應等於 dbinom(3, 10, 0.5)
