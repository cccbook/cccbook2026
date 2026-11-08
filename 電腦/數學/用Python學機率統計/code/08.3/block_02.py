# 08.3-KS檢定與Shapiro-Wilk
# 由 08.3-KS檢定與Shapiro-Wilk.md 抽出：以 python3.14 + PYTHONPATH 指向 rstatistics 執行

import rstatistics as r

g = r.set_seed(2024)
x = [round(v, 4) for v in g.rnorm(50, 10.0, 2.0)]
y = [round(v, 4) for v in g.rnorm(50, 10.5, 2.0)]

# ECDF 階梯函數的折線座標
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

def F(v, data):
    return sum(1 for u in data if u <= v) / len(data)

pts = sorted(set(x) | set(y))
best = 0.0; bpat = pts[0]
for p in pts:
    d = abs(F(p, x) - F(p, y))
    if d > best:
        best = d; bpat = p
fy1 = F(bpat, x); fy2 = F(bpat, y)

px1, py1 = ecdf_poly(x)
px2, py2 = ecdf_poly(y)

gr = r.Graphics(width=7.0, height=5.0)
gr.plot_window([min(x), max(y)], [0.0, 1.0])
gr.title("兩組經驗分布函數 (ECDF) 與 KS 統計量", "數值", "ECDF")
xt = [v for v in r.pretty([min(x), max(y)], 5) if min(x) <= v <= max(y)]
gr.axis(1, xt, [f"{v:g}" for v in xt])
yt = [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]
gr.axis(2, yt, [f"{v:g}" for v in yt])
gr.box()
gr.lines(px1, py1, "black")
gr.lines(px2, py2, "red")
gr.segments([bpat], [min(fy1, fy2)], [bpat], [max(fy1, fy2)], "blue", 1.5)
gr.points([bpat], [max(fy1, fy2)], pch=19, col="blue")
gr.text(bpat - 2.6, max(fy1, fy2) + 0.05, f"D = {best:.2f}", col="blue")
gr.legend(min(x) + 0.4, 0.25, ["y 的 ECDF (紅線)", "x 的 ECDF (黑線)"])
gr.save(\"img/08.3-ecdf-ks.svg\")
print("D =", round(best, 4), "在 t =", bpat, " F_x =", fy1, " F_y =", fy2)
