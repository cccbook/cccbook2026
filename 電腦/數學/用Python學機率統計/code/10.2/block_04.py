# 10.2-直方圖與密度估計
# 由 10.2-直方圖與密度估計.md 抽出：以 python3.14 + PYTHONPATH 指向 rstatistics 執行

import rstatistics as r

g = r.set_seed(7)
x = [round(v, 4) for v in g.rnorm(200, 0.0, 1.0)]

def bin_count(x, br):
    counts = [0.0] * (len(br) - 1)
    for v in x:
        for i in range(len(br) - 1):
            lo, hi = br[i], br[i + 1]
            if (v > lo and v <= hi) or (i == 0 and v >= lo and v <= hi):
                counts[i] += 1.0
                break
    return counts

gr = r.Graphics(width=9.0, height=7.0, mfrow=[2, 2])
for k, nb in enumerate([5, 10, 20, 40]):
    br = r.pretty([min(x), max(x)], nb, 1)
    counts = bin_count(x, br)
    if k > 0:
        gr.next_panel()
    gr.plot_window([br[0], br[-1]], [0.0, max(counts)])
    gr.title(f"{len(counts)} 箱（寬 {br[1]-br[0]:.2f}）", "x", "頻數")
    xt = [v for v in r.pretty([br[0], br[-1]], 5) if br[0] <= v <= br[-1]]
    gr.axis(1, xt, [f"{v:g}" for v in xt])
    yt = [v for v in r.pretty([0.0, max(counts)], 5) if 0.0 <= v <= max(counts)]
    gr.axis(2, yt, [f"{v:g}" for v in yt])
    gr.box()
    for i in range(len(counts)):
        gr.rect(br[i], 0.0, br[i + 1], counts[i], "black", "lightgray")
gr.save(\"img/10.2-bins.svg\")
print("已存 10.2-bins.svg")
