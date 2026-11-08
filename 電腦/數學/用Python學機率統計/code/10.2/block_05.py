# 10.2-直方圖與密度估計
# 由 10.2-直方圖與密度估計.md 抽出：以 python3.14 + PYTHONPATH 指向 rstatistics 執行

import rstatistics as r

g = r.set_seed(7)
x = [round(v, 4) for v in g.rnorm(200, 0.0, 1.0)]

d = r.density_stats(x, bw="nrd0", n=512)
print("bw =", d.bw)
print("n =", d.n)
print("x[0], x[-1] =", d.x[0], d.x[-1])
print("max(y) =", max(d.y), " at x =", d.x[d.y.index(max(d.y))])
print("sum(y)*dx =", round(sum(d.y) * (d.x[-1] - d.x[0]) / (len(d.x) - 1), 6))

print()
print("=== bw.nrd0 的組成 ===")
s = r.sd(x)
iq = r.IQR(x)
print("sd =", s, " IQR =", round(iq, 4), " IQR/1.34 =", round(iq / 1.34, 4))
print("min(sd, IQR/1.34) =", min(s, iq / 1.34))
print("0.9 * that * n^(-0.2) =", 0.9 * min(s, iq / 1.34) * len(x) ** -0.2)
print("n^(-0.2) =", len(x) ** -0.2)
