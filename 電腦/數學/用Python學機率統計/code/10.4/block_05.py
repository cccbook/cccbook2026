# 10.4-函數曲線柱狀圖與圖例
# 由 10.4-函數曲線柱狀圖與圖例.md 抽出：以 python3.14 + PYTHONPATH 指向 rstatistics 執行

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
