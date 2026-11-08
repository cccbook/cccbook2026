# 10.3-箱型圖Q-Q圖與ECDF
# 由 10.3-箱型圖Q-Q圖與ECDF.md 抽出：以 python3.14 + PYTHONPATH 指向 rstatistics 執行

import rstatistics as r

g = r.set_seed(11)
norm = [round(v, 4) for v in g.rnorm(60, 0.0, 1.0)]
heavy = [round(v, 4) for v in g.rt(60, df=3)]

def ecdf_poly(v):
    xs = sorted(v)
    n = len(v)
    px = [xs[0]]
    py = [0.0]
    for i in range(n):
        px.append(xs[i]); py.append((i + 1) / n)
        if i + 1 < n:
            px.append(xs[i + 1]); py.append((i + 1) / n)
    return px, py

gr = r.Graphics(width=10.0, height=5.0, mfrow=[1, 2])

for k, (name, v) in enumerate([("常態資料", norm), ("重尾資料 (t, df=3)", heavy)]):
    if k > 0:
        gr.next_panel()
    px, py = ecdf_poly(v)
    lo, hi = min(v), max(v)
    gr.plot_window([lo, hi], [0.0, 1.0])
    gr.title(f"{name} 的 ECDF 與理論常態 CDF", "x", "F(x)")
    xt = [t for t in r.pretty([lo, hi], 5) if lo <= t <= hi]
    gr.axis(1, xt, [f"{t:g}" for t in xt])
    yt = [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]
    gr.axis(2, yt, [f"{t:g}" for t in yt])
    gr.box()
    # 理論的標準常態 CDF
    ts = [lo + (hi - lo) * i / 200.0 for i in range(201)]
    gr.lines(ts, [r.pnorm(t, 0.0, 1.0) for t in ts], "blue", 1.5)
    # 經驗分布函數的階梯
    gr.lines(px, py, "black", 1.2)
    # KS 統計量：最大的垂直差距
    best = 0.0
    bx = 0.0
    for i, s in enumerate(sorted(v)):
        F = r.pnorm(s, 0.0, 1.0)
        d1 = abs((i + 1) / len(v) - F)
        d2 = abs(i / len(v) - F)
        if d1 > best:
            best = d1; bx = s
        if d2 > best:
            best = d2; bx = s
    Fy = sum(1 for u in v if u <= bx) / len(v)
    Ft = r.pnorm(bx, 0.0, 1.0)
    gr.segments([bx], [min(Fy, Ft)], [bx], [max(Fy, Ft)], "red", 1.5)
    gr.text(bx - 1.9, max(Fy, Ft) + 0.04, f"最大差距 D = {best:.3f}", col="red")
gr.save(\"img/10.3-ecdf.svg\")
print("已存 10.3-ecdf.svg")
