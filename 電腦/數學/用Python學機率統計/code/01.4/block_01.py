# 01.4-五數摘要與箱型圖
# 由 01.4-五數摘要與箱型圖.md 抽出：以 python3.14 + PYTHONPATH 指向 rstatistics 執行

import rstatistics as r

x = [97.0, 100.1, 92.4, 93.2, 105.9, 95.3, 106.6, 103.1, 99.8, 95.0,
     95.9, 98.3, 92.3, 98.7, 94.3, 140.0, 62.0]

print(r.fivenum(x))
print(r.quantile(x, [0.25, 0.5, 0.75]))
print(r.summary(x))
