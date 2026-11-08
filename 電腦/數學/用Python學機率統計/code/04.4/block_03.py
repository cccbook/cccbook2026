# 04.4-正態分配
# 由 04.4-正態分配.md 抽出：以 python3.14 + PYTHONPATH 指向 rstatistics 執行

import rstatistics as r

g = r.set_seed(42)
h = g.rnorm(5, mu, sd)
print([round(v, 2) for v in h])
