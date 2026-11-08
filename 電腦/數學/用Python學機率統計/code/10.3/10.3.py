# 10.3-箱型圖Q-Q圖與ECDF
# 由 10.3-箱型圖Q-Q圖與ECDF.md 抽出：以 python3.14 + PYTHONPATH 指向 rstatistics 執行

# --- 區塊 1 ---
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


# --- 區塊 2 ---
import rstatistics as r

g = r.set_seed(11)
a = [round(v, 4) for v in g.rnorm(40, 100.0, 8.0)]
b = [round(v, 4) for v in g.rnorm(40, 108.0, 8.0)]
c = [round(v, 4) for v in g.rnorm(40, 104.0, 14.0)]

grp = [("A 早班", a), ("B 晚班", b), ("C 混合", c)]
stats = [r.boxplot_stats(v) for _, v in grp]

for (name, v), s in zip(grp, stats):
    print(f"{name}: 五數 = {[round(q,3) for q in s.stats]}  鬚線內 = [{s.stats[0]:.3f}, {s.stats[4]:.3f}]  離群 = {[round(o,3) for o in s.out]}")

lo = min(s.stats[0] for s in stats)
hi = max(s.stats[4] for s in stats)

gr = r.Graphics(width=8.5, height=5.5)
gr.plot_window([0.4, 3.6], [lo, hi])
gr.title("三組產量的並排箱型圖", "", "產品重量 (公克)")
xt = [1.0, 2.0, 3.0]
gr.axis(1, xt, ["A 早班", "B 晚班", "C 混合"])
yt = [v for v in r.pretty([lo, hi], 5) if lo <= v <= hi]
gr.axis(2, yt, [f"{v:g}" for v in yt])
gr.box()

for i, ((name, v), s) in enumerate(zip(grp, stats)):
    xc = float(i + 1)
    bw = 0.22
    # 鬚線
    gr.segments([xc], [s.stats[0]], [xc], [s.stats[1]], "black")
    gr.segments([xc], [s.stats[3]], [xc], [s.stats[4]], "black")
    gr.segments([xc - bw / 2], [s.stats[0]], [xc + bw / 2], [s.stats[0]], "black")
    gr.segments([xc - bw / 2], [s.stats[4]], [xc + bw / 2], [s.stats[4]], "black")
    # 箱子
    gr.rect(xc - bw / 2, s.stats[1], xc + bw / 2, s.stats[3], "black", "lightgray")
    # 中位數
    gr.segments([xc - bw / 2], [s.stats[2]], [xc + bw / 2], [s.stats[2]], "black", 2.0)
    # 離群點
    for o in s.out:
        gr.points([xc], [o], pch=1, col="black")
    # 中位數信賴區間
    gr.segments([xc + bw / 2 + 0.04], [s.conf[0]], [xc + bw / 2 + 0.04], [s.conf[1]], "red", 1.5)
gr.save("img/10.3-box-groups.svg")
print("已存 10.3-box-groups.svg")


# --- 區塊 3 ---
import rstatistics as r

print("=== ppoints ===")
print("ppoints(10) =", [round(v, 4) for v in r.ppoints(10)])
print("ppoints(5)  =", [round(v, 4) for v in r.ppoints(5)])
print("ppoints(60) 的前後三個 =", [round(v, 4) for v in r.ppoints(60)[:3]], [round(v, 4) for v in r.ppoints(60)[-3:]])


# --- 區塊 4 ---
import rstatistics as r

g = r.set_seed(11)
norm = [round(v, 4) for v in g.rnorm(60, 0.0, 1.0)]
heavy = [round(v, 4) for v in g.rt(60, df=3)]

for name, v in [("常態", norm), ("重尾 t(3)", heavy)]:
    t, s = r.qqnorm_coords(v)
    print(f"--- {name} ---")
    print("  理論分位前三:", [round(q, 4) for q in t[:3]], " 樣本分位前三:", [round(q, 4) for q in s[:3]])
    print("  理論分位後三:", [round(q, 4) for q in t[-3:]], " 樣本分位後三:", [round(q, 4) for q in s[-3:]])
    qx = r.quantile(t, [0.25, 0.75])
    qy = r.quantile(s, [0.25, 0.75])
    slope = (qy[1] - qy[0]) / (qx[1] - qx[0])
    icept = qy[0] - slope * qx[0]
    print(f"  qqline: slope = {slope:.4f}, intercept = {icept:.4f}")
    print(f"  樣本 sd = {r.sd(v):.4f}")
    print(f"  左端 (i=1): 理論 {t[0]:.3f} 樣本 {s[0]:.3f} 差距 {s[0]-t[0]:+.3f}")
    print(f"  右端 (i=n): 理論 {t[-1]:.3f} 樣本 {s[-1]:.3f} 差距 {s[-1]-t[-1]:+.3f}")
    hs = r.shapiro_test(v)
    print(f"  Shapiro: W = {hs.statistic:.4f}, p = {hs.p_value:.4g}")


# --- 區塊 5 ---
import rstatistics as r

g = r.set_seed(11)
norm = [round(v, 4) for v in g.rnorm(60, 0.0, 1.0)]
t, s = r.qqnorm_coords(norm)
n = len(t)
mt = r.mean(t)
ms = r.mean(s)
slope = sum((a - mt) * (b - ms) for a, b in zip(t, s)) / sum((a - mt) ** 2 for a in t)
print("OLS slope =", round(slope, 6), " OLS intercept =", round(ms - slope * mt, 6))
print("樣本 sd =", round(r.sd(norm), 6), " 樣本 mean =", round(r.mean(norm), 6))


# --- 區塊 6 ---
import rstatistics as r

g = r.set_seed(11)
norm = [round(v, 4) for v in g.rnorm(60, 0.0, 1.0)]
heavy = [round(v, 4) for v in g.rt(60, df=3)]

gr = r.Graphics(width=10.0, height=5.0, mfrow=[1, 2])

# 面板 1：常態
gr.qqnorm(norm, main="常態資料的 Q-Q 圖", xlab="理論分位數", ylab="樣本分位數")
gr.qqline(norm, col="red")

# 面板 2：重尾
gr.next_panel()
gr.qqnorm(heavy, main="重尾資料 (t, df=3) 的 Q-Q 圖", xlab="理論分位數", ylab="樣本分位數")
gr.qqline(heavy, col="red")

gr.save("img/10.3-qqnorm.svg")
print("已存 10.3-qqnorm.svg")


# --- 區塊 7 ---
import rstatistics as r

g = r.set_seed(11)
norm = [round(v, 4) for v in g.rnorm(60, 0.0, 1.0)]

gr = r.Graphics(width=6.0, height=5.0)
e = gr.ecdf(norm, main="g.ecdf 畫出的經驗分布函數", xlab="x", ylab="F(x)")
print("e =", e)
print("e.n =", e.n)
print("e.x[:5] =", [round(v, 4) for v in e.x[:5]])
print("e.y[:5] =", [round(v, 4) for v in e.y[:5]])
print("e.x[-3:] =", [round(v, 4) for v in e.x[-3:]])
print("e.y[-3:] =", [round(v, 4) for v in e.y[-3:]])


# --- 區塊 8 ---
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
gr.save("img/10.3-ecdf.svg")
print("已存 10.3-ecdf.svg")
