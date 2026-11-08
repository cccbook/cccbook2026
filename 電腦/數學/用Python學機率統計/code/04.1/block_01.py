# 04.1-密度函數與累計分配
# 由 04.1-密度函數與累計分配.md 抽出：以 python3.14 + PYTHONPATH 指向 rstatistics 執行

import rstatistics as r

# 均勻分配 U(0,1)：密度與 CDF
print(r.dunif(0.3, 0, 1))          # 密度：區間內恆為 1
print(r.dunif(3.0, 2, 5))          # U(2,5)：密度 = 1/3
print(r.punif(0.7, 0, 1))          # CDF：P(X <= 0.7)
print(r.punif(4.0, 2, 5) - r.punif(2.5, 2, 5))  # P(2.5 < X <= 4)
print(r.qunif(0.5, 2, 5))          # 中位數
print(r.qunif(0.25, 2, 5))         # 第一四分位數
