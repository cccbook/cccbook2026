# 10.2-直方圖與密度估計
# 由 10.2-直方圖與密度估計.md 抽出：以 python3.14 + PYTHONPATH 指向 rstatistics 執行

import rstatistics as r

g = r.set_seed(7)
x = [round(v, 4) for v in g.rnorm(200, 0.0, 1.0)]
d = r.density_stats(x, bw="nrd0", n=512)
b = d.bw
print("min(x) - 3*bw =", round(min(x) - 3 * b, 4), " max(x) + 3*bw =", round(max(x) + 3 * b, 4))
print("再往外 4*bw:", round(min(x) - 7 * b, 4), round(max(x) + 7 * b, 4))
print("實際 d.x[0] =", d.x[0], " d.x[-1] =", d.x[-1])
