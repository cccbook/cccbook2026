# 01.5-用rstatistics看資料
# 由 01.5-用rstatistics看資料.md 抽出：以 python3.14 + PYTHONPATH 指向 rstatistics 執行

import rstatistics as r

g = r.set_seed(2026)
w = [round(v, 1) for v in g.rnorm(28, mean=62, sd=8)]
print(w)
