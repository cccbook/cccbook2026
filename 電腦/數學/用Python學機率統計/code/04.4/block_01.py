# 04.4-正態分配
# 由 04.4-正態分配.md 抽出：以 python3.14 + PYTHONPATH 指向 rstatistics 執行

import rstatistics as r

# 68-95-99.7 法則（標準常態）
print(r.pnorm(1) - r.pnorm(-1))
print(r.pnorm(2) - r.pnorm(-2))
print(r.pnorm(3) - r.pnorm(-3))
