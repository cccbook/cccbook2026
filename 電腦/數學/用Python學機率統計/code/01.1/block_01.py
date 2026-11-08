# 01.1-從母體到樣本
# 由 01.1-從母體到樣本.md 抽出：以 python3.14 + PYTHONPATH 指向 rstatistics 執行

import rstatistics as r

g = r.set_seed(42)
pop = g.rnorm(10000, mean=170.0, sd=7.0)   # 上帝視角：整個母體

print(r.mean(pop), r.sd(pop))
