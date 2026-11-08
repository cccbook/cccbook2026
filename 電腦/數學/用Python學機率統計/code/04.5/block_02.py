# 04.5-Beta分配與組合的分布
# 由 04.5-Beta分配與組合的分布.md 抽出：以 python3.14 + PYTHONPATH 指向 rstatistics 執行

import rstatistics as r

# Beta 密度形狀
print(r.dbeta(0.5, 1.0, 1.0))      # Beta(1,1) = 均勻 U(0,1)，密度恆 1
print(r.dbeta(0.3, 2.0, 5.0))
print(r.pbeta(0.5, 2.0, 5.0))      # CDF

g = r.set_seed(42)
print(g.rbeta(3, 2.0, 5.0))        # 亂數在 RNG 上

# r.beta(a,b)：B 函數常數；1/B(2,5) = 30 是密度前的常數
print(r.beta(2.0, 5.0))
print(1.0 / r.beta(2.0, 5.0))
