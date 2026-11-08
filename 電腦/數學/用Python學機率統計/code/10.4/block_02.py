# 10.4-函數曲線柱狀圖與圖例
# 由 10.4-函數曲線柱狀圖與圖例.md 抽出：以 python3.14 + PYTHONPATH 指向 rstatistics 執行

import rstatistics as r

g = r.set_seed(21)
sim = g.rbinom(2000, 20, 0.25)
print("sim 前 20 筆 =", sim[:20])
vals = list(range(min(sim), max(sim) + 1))
counts = [0.0] * len(vals)
for v in sim:
    counts[vals.index(v)] += 1.0
emp = [c / 2000.0 for c in counts]
theo = [r.dbinom(k, 20, 0.25) for k in vals]
print("vals =", vals)
print("counts =", counts)
print("emp =", [round(v, 4) for v in emp])
print("theo =", [round(v, 4) for v in theo])
print("最大絕對差 =", round(max(abs(a - b) for a, b in zip(emp, theo)), 4))
