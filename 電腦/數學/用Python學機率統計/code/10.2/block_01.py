# 10.2-直方圖與密度估計
# 由 10.2-直方圖與密度估計.md 抽出：以 python3.14 + PYTHONPATH 指向 rstatistics 執行

import rstatistics as r

g = r.set_seed(7)
x = [round(v, 4) for v in g.rnorm(200, 0.0, 1.0)]
print("n =", len(x), " mean =", round(r.mean(x), 4), " sd =", round(r.sd(x), 4))
print("range =", [round(min(x), 4), round(max(x), 4)])
