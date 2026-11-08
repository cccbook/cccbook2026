# 10.4-函數曲線柱狀圖與圖例
# 由 10.4-函數曲線柱狀圖與圖例.md 抽出：以 python3.14 + PYTHONPATH 指向 rstatistics 執行

# --- 區塊 1 ---
import rstatistics as r

print("=== curve 的取樣 ===")
xs = []
ys = []
for i in range(101):
    xs.append(-3.0 + 6.0 * i / 100.0)
    ys.append(r.dnorm(xs[-1], 0.0, 1.0))
print("curve 的第一個點:", round(xs[0], 3), round(ys[0], 6))
print("curve 的中間點:", round(xs[50], 3), round(ys[50], 6))
print("curve 的最後一個點:", round(xs[-1], 3), round(ys[-1], 6))
print("dx =", round(xs[1] - xs[0], 4))
print("理論峰值 dnorm(0) =", round(r.dnorm(0.0), 6))


# --- 區塊 2 ---
import rstatistics as r

g = r.set_seed(21)
sim = g.rbinom(2000, 20, 0.25)
print("sim 前 20 筆 =", sim[:20])
vals = list(range(min(sim), max(sim) + 1))
counts = [0.0] * len(vals)
for v in sim:
    counts[vals.index(v)] += 1.0
emp = [c / 2000.0 for c in counts]
theo = [r.dbinom(k, 20, 0.25) for k in vals]
print("vals =", vals)
print("counts =", counts)
print("emp =", [round(v, 4) for v in emp])
print("theo =", [round(v, 4) for v in theo])
print("最大絕對差 =", round(max(abs(a - b) for a, b in zip(emp, theo)), 4))


# --- 區塊 3 ---
import rstatistics as r

g = r.set_seed(21)

sim = g.rbinom(2000, 20, 0.25)
vals = list(range(min(sim), max(sim) + 1))
counts = [0.0] * len(vals)
for v in sim:
    counts[vals.index(v)] += 1.0
emp = [c / 2000.0 for c in counts]
theo = [r.dbinom(k, 20, 0.25) for k in vals]

gr = r.Graphics(width=11.0, height=5.0, mfrow=[1, 2])

# 左：Binomial(20, 0.25)
gr.plot_window([-0.7, 12.4], [0.0, 0.235])
gr.title("離散型：B(20, 0.25) 理論機率 vs 模擬長條", "k", "P(X = k)")
xt = [v for v in r.pretty([-0.7, 12.4], 5) if -0.7 <= v <= 12.4]
gr.axis(1, xt, [f"{v:g}" for v in xt])
yt = [v for v in r.pretty([0.0, 0.235], 5) if 0.0 <= v <= 0.235]
gr.axis(2, yt, [f"{v:g}" for v in yt])
gr.box()
for i, k in enumerate(vals):
    gr.rect(float(k) - 0.4, 0.0, float(k) + 0.4, emp[i], "black", "lightgray")
gr.segments([float(k) for k in vals], [0.0] * len(vals), [float(k) for k in vals], theo, "red", 1.5)
gr.points([float(k) for k in vals], theo, pch=19, col="red")
gr.text(12.2, 0.215, "長條 = 模擬相對頻率", col="black", adj=-1.0)
gr.text(12.2, 0.192, "紅點 = 理論機率 P(X=k)", col="red", adj=-1.0)

# 右：N(0,1)
gr.next_panel()
x = [round(v, 4) for v in g.rnorm(2000, 0.0, 1.0)]
br = r.pretty([min(x), max(x)], 20, 1)
nb = len(br) - 1
hc = [0.0] * nb
for v in x:
    for i in range(nb):
        if v > br[i] and v <= br[i + 1]:
            hc[i] += 1.0
            break
hw = br[1] - br[0]
hd = [c / (2000.0 * hw) for c in hc]
gr.plot_window([br[0], br[-1]], [0.0, 0.47])
gr.title("連續型：N(0,1) 理論密度 vs 模擬直方圖", "x", "密度")
xt = [v for v in r.pretty([br[0], br[-1]], 5) if br[0] <= v <= br[-1]]
gr.axis(1, xt, [f"{v:g}" for v in xt])
yt = [v for v in r.pretty([0.0, 0.47], 5) if 0.0 <= v <= 0.47]
gr.axis(2, yt, [f"{v:g}" for v in yt])
gr.box()
for i in range(nb):
    gr.rect(br[i], 0.0, br[i + 1], hd[i], "black", "lightgray")
gr.curve("dnorm", br[0], br[-1], 0.0, 1.0, n=201, col="red", lwd=1.5)
gr.text(3.4, 0.44, "長條 = 模擬直方圖", col="black", adj=-1.0)
gr.text(3.4, 0.415, "紅線 = 理論密度 f(x)", col="red", adj=-1.0)

gr.save("img/10.4-curve-fit.svg")
print("已存 10.4-curve-fit.svg")


# --- 區塊 4 ---
import rstatistics as r

g = r.set_seed(31)
grp = ["早班", "午班", "晚班", "夜班"]
means = [97.4, 104.8, 108.3, 101.2]
ses = [0.98, 1.15, 1.21, 1.07]

gr = r.Graphics(width=8.0, height=5.5)
gr.barplot(means, grp, main="各班組平均產量", xlab="班組", ylab="平均產量 (公克)")
gr.save("/tmp/opencode/probe-bar.svg")
print("ok")


# --- 區塊 5 ---
import rstatistics as r

g = r.set_seed(31)
grp = ["早班", "午班", "晚班", "夜班"]
means = [97.4, 104.8, 108.3, 101.2]
ses = [0.98, 1.15, 1.21, 1.07]

gr = r.Graphics(width=8.5, height=6.0)
gr.plot_window([0.4, 4.6], [90.0, 112.0])
gr.title("各班組平均產量與 95% 信賴區間", "", "平均產量 (公克)")
gr.axis(1, [1.0, 2.0, 3.0, 4.0], grp)
yt = [v for v in r.pretty([90.0, 112.0], 5) if 90.0 <= v <= 112.0]
gr.axis(2, yt, [f"{v:g}" for v in yt])
gr.box()
for i, (m, se) in enumerate(zip(means, ses)):
    xc = float(i + 1)
    gr.rect(xc - 0.22, 90.0, xc + 0.22, m, "black", "lightgray")
    gr.segments([xc], [m - 1.96 * se], [xc], [m + 1.96 * se], "black", 1.2)
    gr.segments([xc - 0.08], [m - 1.96 * se], [xc + 0.08], [m - 1.96 * se], "black", 1.2)
    gr.segments([xc - 0.08], [m + 1.96 * se], [xc + 0.08], [m + 1.96 * se], "black", 1.2)
gr.abline(h=103.0, v=0.0, col="red")
gr.text(0.5, 103.4, "全部班組的平均 103.0", col="red")
gr.legend(0.55, 109.5, ["95% 信賴區間"])
gr.mtext("資料：某工廠兩班組的產品重量（模擬）", side=1, line=4, cex=0.8)
gr.save("/tmp/opencode/probe-bar2.svg")
print("ok")


# --- 區塊 6 ---
import rstatistics as r

gr = r.Graphics(width=6.0, height=4.5)
gr.plot_window([0.0, 10.0], [0.0, 10.0])
gr.title("legend 的位置")
gr.axis(1, [0.0, 5.0, 10.0], ["0", "5", "10"])
gr.axis(2, [0.0, 5.0, 10.0], ["0", "5", "10"])
gr.box()
gr.legend(1.0, 8.0, ["第一項", "第二項", "第三項"])
gr.save("/tmp/opencode/probe-legend.svg")
print("ok")


# --- 區塊 7 ---
import rstatistics as r

gr = r.Graphics(width=6.0, height=4.5)
gr.plot_window([0.0, 10.0], [0.0, 10.0])
gr.title("legend 的順序")
gr.axis(1, [0.0, 5.0, 10.0], ["0", "5", "10"])
gr.axis(2, [0.0, 5.0, 10.0], ["0", "5", "10"])
gr.box()
gr.legend(1.0, 8.0, ["第三項", "第二項", "第一項"])
gr.save("/tmp/opencode/probe-legend.svg")
print("ok")


# --- 區塊 8 ---
import rstatistics as r

g = r.set_seed(41)
x = [round(v, 4) for v in g.rnorm(50, 0.0, 1.0)]
t, s = r.qqnorm_coords(x)
qx = r.quantile(t, [0.25, 0.75])
qy = r.quantile(s, [0.25, 0.75])
slope = (qy[1] - qy[0]) / (qx[1] - qx[0])
icept = qy[0] - slope * qx[0]

gr = r.Graphics(width=6.5, height=6.0)
lo, hi = -3.0, 3.5
gr.plot_window([lo, hi], [lo, hi])
gr.title("Q-Q 圖與 95% 帶狀區", "理論分位數", "樣本分位數")
xt = [v for v in r.pretty([lo, hi], 5) if lo <= v <= hi]
gr.axis(1, xt, [f"{v:g}" for v in xt])
gr.axis(2, xt, [f"{v:g}" for v in xt])
gr.box()
# 95% 的參考帶（常態下 n=50 的近似 1.36/sqrt(n)），以 qqline 為中心
band = 1.36 / (50.0 ** 0.5)
bandx = [lo + (hi - lo) * i / 50.0 for i in range(51)]
mid = [icept + slope * v for v in bandx]
gr.polygon(bandx, [v + band for v in mid], "gray", "lightgray")
gr.polygon(bandx, [v - band for v in mid], "gray", "lightgray")
gr.lines([bandx[0], bandx[-1]], [mid[0], mid[-1]], "red")
gr.points(t, s, pch=1, col="black")
gr.save("/tmp/opencode/probe-band.svg")
print("band =", round(band, 4))
print("qqline slope =", round(slope, 4), " intercept =", round(icept, 4))
print("樣本 sd =", round(r.sd(x), 4), " 樣本 mean =", round(r.mean(x), 4))


# --- 區塊 9 ---
import rstatistics as r

gr = r.Graphics(width=6.5, height=5.0)
gr.plot_window([0.0, 10.0], [0.0, 10.0])
gr.title("用 polygon 畫箭頭")
gr.axis(1, [0.0, 5.0, 10.0], ["0", "5", "10"])
gr.axis(2, [0.0, 5.0, 10.0], ["0", "5", "10"])
gr.box()
gr.points([5.5], [7.0], pch=19, col="red")
gr.text(7.2, 7.0, "這個點是離群值", col="red", adj=1.0)
# 箭頭：尖端在 (6.3, 7.0)，尾端在 (7.0, 7.0)，翼在 x = 6.6
gr.polygon([6.3, 7.0, 6.6], [7.0, 7.15, 6.85], "red", "red")
gr.save("/tmp/opencode/probe-arrow.svg")
print("ok")


# --- 區塊 10 ---
import rstatistics as r

gr = r.Graphics(width=9.0, height=7.0, mfrow=[2, 2])
titles = ["左上", "右上", "左下", "右下"]
for k in range(4):
    if k > 0:
        gr.next_panel()
    gr.plot_window([0.0, 10.0], [0.0, 10.0])
    gr.title(titles[k])
    gr.axis(1, [0.0, 5.0, 10.0], ["0", "5", "10"])
    gr.axis(2, [0.0, 5.0, 10.0], ["0", "5", "10"])
    gr.box()
    gr.points([2.0 + k, 8.0 - k], [5.0 + k, 6.0 - k], pch=19)
gr.save("/tmp/opencode/probe-panels.svg")
print("ok")
