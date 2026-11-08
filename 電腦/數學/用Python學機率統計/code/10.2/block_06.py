# 10.2-直方圖與密度估計
# 由 10.2-直方圖與密度估計.md 抽出：以 python3.14 + PYTHONPATH 指向 rstatistics 執行

import rstatistics as r

g = r.set_seed(7)
x = [round(v, 4) for v in g.rnorm(200, 0.0, 1.0)]

print("=== 不同頻寬 ===")
for bw in [0.1, 0.2, 0.3, 0.5, 0.8, 1.2]:
    dd = r.density_stats(x, bw=bw, n=512)
    print(f"  bw={bw:4.1f}  max density = {max(dd.y):.4f}  at x = {dd.x[dd.y.index(max(dd.y))]:+.3f}")
