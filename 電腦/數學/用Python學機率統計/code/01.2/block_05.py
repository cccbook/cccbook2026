# 01.2-集中趨勢
# 由 01.2-集中趨勢.md 抽出：以 python3.14 + PYTHONPATH 指向 rstatistics 執行

import rstatistics as r

w = [28, 30, 32, 32, 35, 36, 38, 40, 42, 45, 48, 52, 55, 60, 220]

# 候選值：以 0.5 為步距掃過資料範圍
cands = [x + 0.5 * k for x in range(20, 61) for k in range(4)]

best_sq  = min(cands, key=lambda c: sum((xi - c) ** 2 for xi in w))
best_abs = min(cands, key=lambda c: sum(abs(xi - c) for xi in w))

print(best_sq, best_abs)
print(r.mean(w), r.median(w))
