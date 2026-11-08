# 10.2-直方圖與密度估計
# 由 10.2-直方圖與密度估計.md 抽出：以 python3.14 + PYTHONPATH 指向 rstatistics 執行

# --- 區塊 1 ---
import rstatistics as r

g = r.set_seed(7)
x = [round(v, 4) for v in g.rnorm(200, 0.0, 1.0)]
print("n =", len(x), " mean =", round(r.mean(x), 4), " sd =", round(r.sd(x), 4))
print("range =", [round(min(x), 4), round(max(x), 4)])


# --- 區塊 2 ---
import rstatistics as r

g = r.set_seed(7)
x = [round(v, 4) for v in g.rnorm(200, 0.0, 1.0)]

h = r.hist_stats(x, breaks="Sturges")
print("counts =", h.counts)
print("density =", [round(v, 5) for v in h.density])
print("sum(counts) =", sum(h.counts), " sum(density)*寬 =", round(sum(v * (h.breaks[1]-h.breaks[0]) for v in h.density), 10))


# --- 區塊 3 ---
import rstatistics as r

print("n     Sturges  FD  Scott")
for n in [10, 20, 30, 50, 100, 200, 500, 1000, 5000]:
    gg = r.set_seed(7)
    z = gg.rnorm(n, 0.0, 1.0)
    row = []
    for b in ["Sturges", "FD", "Scott"]:
        row.append(len(r.hist_stats(z, breaks=b).counts))
    print(f"{n:5d}  {row[0]:5d} {row[1]:5d} {row[2]:5d}")


# --- 區塊 4 ---
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
gr.save("img/10.2-bins.svg")
print("已存 10.2-bins.svg")


# --- 區塊 5 ---
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


# --- 區塊 6 ---
import rstatistics as r

g = r.set_seed(7)
x = [round(v, 4) for v in g.rnorm(200, 0.0, 1.0)]

print("=== 不同頻寬 ===")
for bw in [0.1, 0.2, 0.3, 0.5, 0.8, 1.2]:
    dd = r.density_stats(x, bw=bw, n=512)
    print(f"  bw={bw:4.1f}  max density = {max(dd.y):.4f}  at x = {dd.x[dd.y.index(max(dd.y))]:+.3f}")


# --- 區塊 7 ---
import rstatistics as r

g = r.set_seed(7)
x = [round(v, 4) for v in g.rnorm(200, 0.0, 1.0)]
d = r.density_stats(x, bw="nrd0", n=512)
b = d.bw
print("min(x) - 3*bw =", round(min(x) - 3 * b, 4), " max(x) + 3*bw =", round(max(x) + 3 * b, 4))
print("再往外 4*bw:", round(min(x) - 7 * b, 4), round(max(x) + 7 * b, 4))
print("實際 d.x[0] =", d.x[0], " d.x[-1] =", d.x[-1])


# --- 區塊 8 ---
import rstatistics as r

g = r.set_seed(7)
x = [round(v, 4) for v in g.rnorm(200, 0.0, 1.0)]

h = r.hist_stats(x, breaks="Sturges")
d = r.density_stats(x, bw="nrd0", n=512)

lo, hi = h.breaks[0], h.breaks[-1]
dx = [v for v in d.x if lo <= v <= hi]
dy = [d.y[d.x.index(v)] for v in dx]

gr = r.Graphics(width=8.0, height=6.0)
gr.plot_window([lo, hi], [0.0, 0.45])
gr.title("常態資料的直方圖與核密度估計", "x", "密度")
xt = [v for v in r.pretty([lo, hi], 5) if lo <= v <= hi]
gr.axis(1, xt, [f"{v:g}" for v in xt])
yt = [v for v in r.pretty([0.0, 0.45], 5) if 0.0 <= v <= 0.45]
gr.axis(2, yt, [f"{v:g}" for v in yt])
gr.box()
for i in range(len(h.counts)):
    gr.rect(h.breaks[i], 0.0, h.breaks[i + 1], h.density[i], "black", "lightgray")
gr.lines(dx, dy, "red", 1.5)
xs = [lo + (hi - lo) * i / 200.0 for i in range(201)]
ys = [r.dnorm(v, 0.0, 1.0) for v in xs]
gr.lines(xs, ys, "blue", 1.0)
gr.text(-1.7, 0.41, "藍：N(0,1) 理論密度", col="blue")
gr.text(-1.7, 0.375, "紅：核密度估計 (KDE)", col="red")
gr.save("img/10.2-hist-density.svg")
print("已存 10.2-hist-density.svg")
print("直方圖密度 =", [round(v, 4) for v in h.density])
print("密度估計 bw =", d.bw, " 峰值 =", round(max(d.y), 4))
print("理論 N(0,1) 峰值 =", round(r.dnorm(0.0), 4))
print("樣本 sd =", round(r.sd(x), 4), " 樣本 mean =", round(r.mean(x), 4))
