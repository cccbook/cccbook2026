# 08.1-為什麼需要非參數方法
# 由 08.1-為什麼需要非參數方法.md 抽出：以 python3.14 + PYTHONPATH 指向 rstatistics 執行

import rstatistics as r

g = r.set_seed(42)
x = [g.rnorm(1)[0] for _ in range(20)]
print("原始資料   :", [round(v, 3) for v in x])
print("平均數     :", round(r.mean(x), 3))
print("中位數     :", round(r.median(x), 3))

y = x + [100.0]          # 儀器壞點：多了一筆 100
print("加入 100 後")
print("平均數     :", round(r.mean(y), 3))
print("中位數     :", round(r.median(y), 3))
