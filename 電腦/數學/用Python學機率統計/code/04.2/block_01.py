# 04.2-均勻分配
# 由 04.2-均勻分配.md 抽出：以 python3.14 + PYTHONPATH 指向 rstatistics 執行

import rstatistics as r

g = r.set_seed(42)
u = g.runif(5)
print(u)
