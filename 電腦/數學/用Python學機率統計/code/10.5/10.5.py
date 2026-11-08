# 10.5-完整案例
# 由 10.5-完整案例.md 抽出：以 python3.14 + PYTHONPATH 指向 rstatistics 執行

# --- 區塊 1 ---
import rstatistics as r

g = r.set_seed(2026)
n = 60
day = [round(v, 3) for v in g.rnorm(n, 100.0, 6.0)]
night = [round(v, 3) for v in g.rnorm(n, 102.5, 6.0)]
print("n 每組 =", n)
print("day 前 10 =", day[:10])
print("night 前 10 =", night[:10])


# --- 區塊 2 ---
import rstatistics as r

g = r.set_seed(2026)
n = 60
day = [round(v, 3) for v in g.rnorm(n, 100.0, 6.0)]
night = [round(v, 3) for v in g.rnorm(n, 102.5, 6.0)]

print("=== 描述統計 ===")
for name, v in [("日班", day), ("夜班", night)]:
    s = r.summary(v)
    print(f"--- {name} ---")
    print(s)
    print("  mean =", round(r.mean(v), 4), " sd =", round(r.sd(v), 4),
          " median =", r.median(v), " IQR =", round(r.IQR(v), 4))
    print("  離群值 =", [round(o, 3) for o in r.boxplot_stats(v).out])


# --- 區塊 3 ---
import rstatistics as r

g = r.set_seed(2026)
n = 60
day = [round(v, 3) for v in g.rnorm(n, 100.0, 6.0)]
night = [round(v, 3) for v in g.rnorm(n, 102.5, 6.0)]

grp = [("日班", day), ("夜班", night)]
stats = [r.boxplot_stats(v) for _, v in grp]
lo = min(s.stats[0] for s in stats)
hi = max(s.stats[4] for s in stats)

gr = r.Graphics(width=8.0, height=5.5)
gr.plot_window([0.4, 2.6], [lo, hi])
gr.title("兩班組產品重量的並排箱型圖", "", "產品重量 (公克)")
gr.axis(1, [1.0, 2.0], ["日班", "夜班"])
yt = [v for v in r.pretty([lo, hi], 5) if lo <= v <= hi]
gr.axis(2, yt, [f"{v:g}" for v in yt])
gr.box()
for i, ((name, v), s) in enumerate(zip(grp, stats)):
    xc = float(i + 1)
    bw = 0.24
    gr.segments([xc], [s.stats[0]], [xc], [s.stats[1]], "black")
    gr.segments([xc], [s.stats[3]], [xc], [s.stats[4]], "black")
    gr.segments([xc - bw / 2], [s.stats[0]], [xc + bw / 2], [s.stats[0]], "black")
    gr.segments([xc - bw / 2], [s.stats[4]], [xc + bw / 2], [s.stats[4]], "black")
    gr.rect(xc - bw / 2, s.stats[1], xc + bw / 2, s.stats[3], "black", "lightgray")
    gr.segments([xc - bw / 2], [s.stats[2]], [xc + bw / 2], [s.stats[2]], "black", 2.0)
    for o in s.out:
        gr.points([xc], [o], pch=1, col="black")
    gr.segments([xc + bw / 2 + 0.05], [s.conf[0]], [xc + bw / 2 + 0.05], [s.conf[1]], "red", 1.5)
gr.text(0.55, hi - 4.0, "紅線：中位數的 95% 信賴區間", col="red")
gr.mtext("n = 60 / 班；資料為模擬產生", side=1, line=4, cex=0.8)
gr.save("img/10.5-boxplot.svg")
print("已存 10.5-boxplot.svg")
for (name, v), s in zip(grp, stats):
    print(f"{name}: 五數 = {[round(q,3) for q in s.stats]} conf = {[round(q,3) for q in s.conf]}")


# --- 區塊 4 ---
import rstatistics as r

g = r.set_seed(2026)
n = 60
day = [round(v, 3) for v in g.rnorm(n, 100.0, 6.0)]
night = [round(v, 3) for v in g.rnorm(n, 102.5, 6.0)]

print("=== 正態性 ===")
for name, v in [("日班", day), ("夜班", night)]:
    h = r.shapiro_test(v)
    print(f"{name}: W = {h.statistic:.5f}, p = {h.p_value:.5f}")
    t, s = r.qqnorm_coords(v)
    qx = r.quantile(t, [0.25, 0.75])
    qy = r.quantile(s, [0.25, 0.75])
    slope = (qy[1] - qy[0]) / (qx[1] - qx[0])
    icept = qy[0] - slope * qx[0]
    print(f"   qqline slope = {slope:.4f} intercept = {icept:.4f} (sd={r.sd(v):.4f}, mean={r.mean(v):.4f})")


# --- 區塊 5 ---
import rstatistics as r

g = r.set_seed(2026)
n = 60
day = [round(v, 3) for v in g.rnorm(n, 100.0, 6.0)]
night = [round(v, 3) for v in g.rnorm(n, 102.5, 6.0)]

grp = [("日班", day), ("夜班", night)]

gr = r.Graphics(width=10.0, height=5.0, mfrow=[1, 2])
for k, (name, v) in enumerate(grp):
    if k > 0:
        gr.next_panel()
    t, s = r.qqnorm_coords(v)
    m = r.mean(v)
    sd = r.sd(v)
    z = [(q - m) / sd for q in v]
    tz, sz = r.qqnorm_coords(z)
    l, h = min(min(tz), min(sz)), max(max(tz), max(sz))
    gr.plot_window([l, h], [l, h])
    gr.title(f"{name}的標準化 Q-Q 圖", "理論分位數（標準常態）", "樣本分位數")
    xt = [q for q in r.pretty([l, h], 5) if l <= q <= h]
    gr.axis(1, xt, [f"{q:g}" for q in xt])
    gr.axis(2, xt, [f"{q:g}" for q in xt])
    gr.box()
    gr.lines([l, h], [l, h], "red")
    gr.points(tz, sz, pch=1, col="black")
    hs = r.shapiro_test(v)
    gr.text(0.15, -1.95, f"Shapiro-Wilk: W = {hs.statistic:.4f}", col="black")
    gr.text(0.15, -2.25, f"p = {hs.p_value:.3f} > 0.05（不拒絕常態）", col="black")
gr.save("img/10.5-qq.svg")
print("已存 10.5-qq.svg")


# --- 區塊 6 ---
import rstatistics as r

g = r.set_seed(2026)
n = 60
day = [round(v, 3) for v in g.rnorm(n, 100.0, 6.0)]
night = [round(v, 3) for v in g.rnorm(n, 102.5, 6.0)]

tt = r.t_test(day, night)
print(tt)
print("  statistic =", tt.statistic)
print("  p_value =", tt.p_value)
print("  conf_int =", tt.conf_int)
print("  estimate =", tt.estimate)
print("  df =", tt.parameter)


# --- 區塊 7 ---
import rstatistics as r

g = r.set_seed(2026)
n = 60
day = [round(v, 3) for v in g.rnorm(n, 100.0, 6.0)]
night = [round(v, 3) for v in g.rnorm(n, 102.5, 6.0)]

m1, m2 = r.mean(day), r.mean(night)
s1, s2 = r.sd(day), r.sd(night)
n1, n2 = len(day), len(night)
diff = m1 - m2
v1 = s1**2 / n1
v2 = s2**2 / n2
se_w = (v1 + v2) ** 0.5
dfw = (v1 + v2) ** 2 / (v1**2 / (n1 - 1) + v2**2 / (n2 - 1))
t = diff / se_w
print("m1 =", round(m1, 5), " m2 =", round(m2, 5), " diff =", round(diff, 5))
print("s1 =", round(s1, 5), " s2 =", round(s2, 5))
print("v1 =", round(v1, 6), " v2 =", round(v2, 6))
print("se_welch =", round(se_w, 5), " df =", round(dfw, 4), " t =", round(t, 5))
print("p（用 pt 查表）=", r.pt(abs(t), dfw, lower_tail=False) * 2)
crit = r.qt(0.975, dfw)
print("t crit (0.975) =", round(crit, 5))
print("CI =", [round(diff - crit * se_w, 5), round(diff + crit * se_w, 5)])


# --- 區塊 8 ---
import rstatistics as r

g = r.set_seed(2026)
n = 60
day = [round(v, 3) for v in g.rnorm(n, 100.0, 6.0)]
night = [round(v, 3) for v in g.rnorm(n, 102.5, 6.0)]

print("=== var_equal=True（合併變異數）===")
tp = r.t_test(day, night, var_equal=True)
print(tp)

print()
print("=== 單邊 ===")
print("alternative='less'  :", r.t_test(day, night, alternative="less").p_value)
print("alternative='greater':", r.t_test(day, night, alternative="greater").p_value)

print()
print("=== 90% CI ===")
t90 = r.t_test(day, night, conf_level=0.90)
print("conf_int =", t90.conf_int)


# --- 區塊 9 ---
import rstatistics as r

g = r.set_seed(2026)
n = 60
day = [round(v, 3) for v in g.rnorm(n, 100.0, 6.0)]
night = [round(v, 3) for v in g.rnorm(n, 102.5, 6.0)]

tt = r.t_test(day, night)
diff = tt.estimate[0] - tt.estimate[1]
lo_ci = tt.conf_int[0]
hi_ci = tt.conf_int[1]
se = (r.sd(day) ** 2 / len(day) + r.sd(night) ** 2 / len(night)) ** 0.5

gr = r.Graphics(width=9.0, height=5.5)
gr.plot_window([-6.5, 1.5], [0.0, 1.0])
gr.title("平均重量差（日班 − 夜班）的 95% 信賴區間")
xt = [v for v in r.pretty([-6.5, 1.5], 5) if -6.5 <= v <= 1.5]
gr.axis(1, xt, [f"{v:g}" for v in xt])
gr.axis(2, [0.0, 1.0], [""])
gr.box()
# 0 的參考線（垂直）
gr.segments([0.0], [0.0], [0.0], [1.0], "gray")
# 信賴區間
gr.segments([lo_ci], [0.42], [hi_ci], [0.42], "black", 2.5)
gr.segments([lo_ci], [0.33], [lo_ci], [0.51], "black", 2.5)
gr.segments([hi_ci], [0.33], [hi_ci], [0.51], "black", 2.5)
# 點估計
gr.segments([diff], [0.22], [diff], [0.62], "red", 3.5)
gr.text(-6.2, 0.82, f"點估計 = {diff:.3f}（紅線）", col="red")
gr.text(-6.2, 0.68, f"95% CI = [{lo_ci:.3f}, {hi_ci:.3f}]（黑線）", col="black")
gr.text(-6.2, 0.56, f"SE = {se:.4f}   t = {tt.statistic:.4f}   df = {tt.parameter[0]:.2f}", col="black")
gr.text(-6.2, 0.44, f"p = {tt.p_value:.5f} < 0.05", col="black")
gr.text(-6.2, 0.14, "灰線 = 0（無差異的虛無假設）", col="gray")
gr.mtext("信賴區間不包含 0，故拒絕 H0: 平均差 = 0", side=1, line=4, cex=0.85)
gr.save("img/10.5-ci.svg")
print("已存 10.5-ci.svg")
print("diff =", round(diff, 5), " CI =", [round(lo_ci, 5), round(hi_ci, 5)], " se =", round(se, 5))


# --- 區塊 10 ---
import rstatistics as r

v = [98.2, 101.5, 99.8, 103.2, 100.1, 97.6]

gr = r.Graphics(width=10.0, height=4.8, mfrow=[1, 2])

# (a) 截斷 y 軸：柱子的長度不再與數值成比例
gr.plot_window([0.4, 2.6], [97.0, 104.0])
gr.title("(a) 截斷 y 軸：差異被誇大", "", "值")
gr.axis(1, [1.0, 2.0], ["A", "B"])
yt = [97.0, 99.0, 101.0, 103.0]
gr.axis(2, yt, [f"{t:g}" for t in yt])
gr.box()
gr.rect(0.75, 97.0, 1.25, 100.1, "black", "lightgray")
gr.rect(1.75, 97.0, 2.25, 103.2, "black", "lightgray")
gr.text(1.0, 97.2, "A = 100.1", col="black")
gr.text(2.0, 97.2, "B = 103.2", col="black")
gr.text(1.5, 103.4, "差距只有 3.1，卻佔了半個畫面", col="red")

# (b) 正確：y 軸從 0 開始，柱長與數值成比例
gr.next_panel()
gr.plot_window([0.4, 2.6], [0.0, 110.0])
gr.title("(b) 正確：y 軸從 0 開始", "", "值")
gr.axis(1, [1.0, 2.0], ["A", "B"])
yt2 = [0.0, 25.0, 50.0, 75.0, 100.0]
gr.axis(2, yt2, [f"{t:g}" for t in yt2])
gr.box()
gr.rect(0.75, 0.0, 1.25, 100.1, "black", "lightgray")
gr.rect(1.75, 0.0, 2.25, 103.2, "black", "lightgray")
gr.text(1.0, 5.0, "A = 100.1", col="black")
gr.text(2.0, 5.0, "B = 103.2", col="black")

gr.save("img/10.5-traps.svg")
print("已存 10.5-traps.svg")
print("A = 100.1, B = 103.2, 差距 =", round(103.2 - 100.1, 4))
print("(a) 截斷後：差距 3.1 佔軸範圍 7.0 的", round(3.1 / 7.0 * 100, 1), "%")
print("(b) 從 0 開始：差距 3.1 佔軸範圍 110.0 的", round(3.1 / 110.0 * 100, 1), "%")
print("視覺誇大倍數 =", round((3.1 / 7.0) / (3.1 / 110.0), 1), "倍")


# --- 區塊 11 ---
import rstatistics as r

g = r.set_seed(61)
a = [round(v, 3) for v in g.rnorm(40, 100.0, 5.0)]
b = [round(v, 3) for v in g.rnorm(40, 50.0, 8.0)]
print("a 與 b 的相關係數 =", round(r.cor(a, b), 4))

# 誠實的做法：兩個面板，共用 x 軸
gr = r.Graphics(width=9.0, height=4.5, mfrow=[1, 2])
gr.plot([float(i) for i in range(len(a))], a, type="p", main="面板 1：變數 A", xlab="時間", ylab="A")
gr.next_panel()
gr.plot([float(i) for i in range(len(b))], b, type="p", main="面板 2：變數 B", xlab="時間", ylab="B")
gr.save("/tmp/opencode/trap-panels.svg")
print("ok")
