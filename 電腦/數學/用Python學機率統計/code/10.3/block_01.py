# 10.3-箱型圖Q-Q圖與ECDF
# 由 10.3-箱型圖Q-Q圖與ECDF.md 抽出：以 python3.14 + PYTHONPATH 指向 rstatistics 執行

import rstatistics as r

g = r.set_seed(11)
a = [round(v, 4) for v in g.rnorm(40, 100.0, 8.0)]
b = [round(v, 4) for v in g.rnorm(40, 108.0, 8.0)]
c = [round(v, 4) for v in g.rnorm(40, 104.0, 14.0)]

for name, v in [("A", a), ("B", b), ("C", c)]:
    s = r.summary(v)
    print(name, "mean =", round(r.mean(v), 3), "sd =", round(r.sd(v), 3),
          "median =", r.median(v), "IQR =", round(r.IQR(v), 3))

print()
for name, v in [("A", a), ("B", b), ("C", c)]:
    bs = r.boxplot_stats(v)
    print(f"{name}: stats = {[round(q,3) for q in bs.stats]}  conf = {[round(q,3) for q in bs.conf]}  out = {len(bs.out)}")
