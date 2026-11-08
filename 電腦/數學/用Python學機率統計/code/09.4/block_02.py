# 09.4-變異數分析
# 由 09.4-變異數分析.md 抽出：以 python3.14 + PYTHONPATH 指向 rstatistics 執行

import rstatistics as r

g2 = r.set_seed(2024)
y2 = []
grp2 = []
for name in ["A", "B", "C"]:
    for _ in range(20):
        y2.append(g2.rnorm(1)[0] + 10.0)
        grp2.append(name)
y2[40] = 70.0        # C 組的一個離群值
print()
print("離群值的影響：")
print("  各組平均數: %.3f %.3f %.3f" % (r.mean(y2[0:20]), r.mean(y2[20:40]), r.mean(y2[40:60])))
print("  各組中位數: %.3f %.3f %.3f" % (r.median(y2[0:20]), r.median(y2[20:40]), r.median(y2[40:60])))
a2 = r.aov(y2, grp2, formula="y ~ g")
print()
print(a2.summary())
print()
print(r.kruskal_test(y2, grp2))
