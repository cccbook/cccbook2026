# 10.2-直方圖與密度估計
# 由 10.2-直方圖與密度估計.md 抽出：以 python3.14 + PYTHONPATH 指向 rstatistics 執行

import rstatistics as r

print("n     Sturges  FD  Scott")
for n in [10, 20, 30, 50, 100, 200, 500, 1000, 5000]:
    gg = r.set_seed(7)
    z = gg.rnorm(n, 0.0, 1.0)
    row = []
    for b in ["Sturges", "FD", "Scott"]:
        row.append(len(r.hist_stats(z, breaks=b).counts))
    print(f"{n:5d}  {row[0]:5d} {row[1]:5d} {row[2]:5d}")
