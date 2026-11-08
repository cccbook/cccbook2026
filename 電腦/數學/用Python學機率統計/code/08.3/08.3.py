# 08.3-KS檢定與Shapiro-Wilk
# 由 08.3-KS檢定與Shapiro-Wilk.md 抽出：以 python3.14 + PYTHONPATH 指向 rstatistics 執行

# --- 區塊 1 ---
import rstatistics as r

g = r.set_seed(2024)
x = [round(v, 4) for v in g.rnorm(50, 10.0, 2.0)]
y = [round(v, 4) for v in g.rnorm(50, 10.5, 2.0)]
print("x（前 10 筆）:", x[:10])
print("y（前 10 筆）:", y[:10])
print()

def F(v, data):
    return sum(1 for u in data if u <= v) / len(data)

pts = sorted(set(x) | set(y))
print("斷點處的 ECDF 差 |F_x - F_y|（只看前後各 10 個斷點）：")
best = 0.0
bpat = 0.0
for i, p in enumerate(pts):
    d = abs(F(p, x) - F(p, y))
    if d > best:
        best = d
        bpat = p
    if i < 10 or i >= len(pts) - 10:
        print(f"  t = {p:8.4f}   F_x = {F(p,x):.4f}   F_y = {F(p,y):.4f}   |diff| = {d:.4f}")
print("最大距離 D =", round(best, 6), " 出現在 t =", round(bpat, 4))


# --- 區塊 2 ---
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
gr.save("img/08.3-ecdf-ks.svg")
print("D =", round(best, 4), "在 t =", bpat, " F_x =", fy1, " F_y =", fy2)


# --- 區塊 3 ---
import rstatistics as r

g = r.set_seed(2024)
x = [round(v, 4) for v in g.rnorm(50, 10.0, 2.0)]
y = [round(v, 4) for v in g.rnorm(50, 10.5, 2.0)]

h = r.ks_test(x, y)
print(h)
print("  h.method         =", h.method)
print("  h.statistic_name =", h.statistic_name)
print("  h.statistic      =", h.statistic)
print("  h.p_value        =", h.p_value)
print("  h.alternative    =", h.alternative)
print()

print("alternative='less'    :", r.ks_test(x, y, alternative="less").p_value)
print("alternative='greater' :", r.ks_test(x, y, alternative="greater").p_value)
print("exact=False（漸近近似）:", r.ks_test(x, y, exact=False).p_value)
print()
h_exact = r.ks_test(x, y)
h_asym = r.ks_test(x, y, exact=False)
print("精確 p =", h_exact.p_value)
print("漸近 p =", h_asym.p_value)
print("兩者相差 =", abs(h_exact.p_value - h_asym.p_value))


# --- 區塊 4 ---
import rstatistics as r
import math

g = r.set_seed(2024)
x = [round(v, 4) for v in g.rnorm(50, 10.0, 2.0)]
xs = sorted(x)
n = len(xs)
dplus = 0.0
dminus = 0.0
for i in range(n):
    F = r.pnorm(xs[i], 10.0, 2.0)
    dplus = max(dplus, (i + 1) / n - F)
    dminus = max(dminus, F - i / n)
D = max(dplus, dminus)
print("單樣本 KS（x 對 N(10,2)）手算：D+ =", round(dplus, 6), " D- =", round(dminus, 6), " D =", round(D, 6))
print("漸近 p 值（手算）= 2*exp(-2*n*D^2) =", round(2 * math.exp(-2 * n * D * D), 6))


# --- 區塊 5 ---
import rstatistics as r

# 資料：某零件的量測值
g = r.set_seed(5)
x = [round(v, 4) for v in g.rnorm(30, 50.0, 3.0)]
print("常態母體的 30 筆資料：", x)
h = r.shapiro_test(x)
print(h)
print("  h.method         =", h.method)
print("  h.statistic_name =", h.statistic_name)
print("  h.statistic      =", h.statistic)
print("  h.p_value        =", h.p_value)
print()

# 明顯右偏的資料
y = [round(v, 4) for v in g.rexp(30, rate=0.1)]
print("指數分布（右偏）的 30 筆資料：", y)
print(r.shapiro_test(y))


# --- 區塊 6 ---
import rstatistics as r

print("=== 偏斜程度固定，n 變大 ===")
for n in [20, 50, 100, 200, 500]:
    gg = r.set_seed(9)
    z = gg.rnorm(n)
    d2 = [v + 0.6 * (v * v - 1.0) for v in z]
    hq = r.shapiro_test(d2)
    print(f"  n = {n:5d}   W = {hq.statistic:.4f}, p = {hq.p_value:.4g}")


# --- 區塊 7 ---
import rstatistics as r

print("=== n 大時：微小的偏離也會顯著 ===")
for n in [30, 100, 300, 1000]:
    gg = r.set_seed(9)
    z = gg.rnorm(n)
    d1 = z
    d2 = [v + 0.15 * (v * v - 1.0) for v in z]
    hp = r.shapiro_test(d1)
    hq = r.shapiro_test(d2)
    print(f"  n = {n:5d}   常態: W = {hp.statistic:.4f}, p = {hp.p_value:.4g}   "
          f"微偏斜: W = {hq.statistic:.4f}, p = {hq.p_value:.4g}")


# --- 區塊 8 ---
import rstatistics as r

g = r.set_seed(5)
x = [round(v, 4) for v in g.rnorm(30, 50.0, 3.0)]
y = [round(v, 4) for v in g.rexp(30, rate=0.1)]

def qq_draw(v, title, path):
    # 標準化，讓 Q-Q 圖的兩個軸同尺度
    m = r.mean(v)
    s = r.sd(v)
    z = [(q - m) / s for q in v]
    t, sm = r.qqnorm_coords(z)
    lo = min(min(t), min(sm))
    hi = max(max(t), max(sm))
    gr = r.Graphics(width=6.0, height=6.0)
    gr.plot(t, sm, type="p", main=title, xlab="理論分位數（常態）", ylab="樣本分位數（標準化）",
            xlim=[lo, hi], ylim=[lo, hi])
    qx = r.quantile(t, [0.25, 0.75])
    qy = r.quantile(sm, [0.25, 0.75])
    slope = (qy[1] - qy[0]) / (qx[1] - qx[0])
    icept = qy[0] - slope * qx[0]
    gr.lines([t[0], t[len(t) - 1]], [icept + slope * t[0], icept + slope * t[len(t) - 1]], "red")
    gr.save(path)
    print("已存", path)

qq_draw(x, "常態資料的 Q-Q 圖", "08.3-qq-normal.svg")
qq_draw(y, "指數資料的 Q-Q 圖", "08.3-qq-exponential.svg")
