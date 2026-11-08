# 01.2-集中趨勢
# 由 01.2-集中趨勢.md 抽出：以 python3.14 + PYTHONPATH 指向 rstatistics 執行

import rstatistics as r

w = [28, 30, 32, 32, 35, 36, 38, 40, 42, 45, 48, 52, 55, 60, 220]

print("mean   =", r.mean(w))
print("median =", r.median(w))
print("wmean  =", r.weighted_mean(w, [1] * 15))    # 等權重 → 退化成普通平均
