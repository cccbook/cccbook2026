# 10.4-函數曲線柱狀圖與圖例
# 由 10.4-函數曲線柱狀圖與圖例.md 抽出：以 python3.14 + PYTHONPATH 指向 rstatistics 執行

import rstatistics as r

g = r.set_seed(31)
grp = ["早班", "午班", "晚班", "夜班"]
means = [97.4, 104.8, 108.3, 101.2]
ses = [0.98, 1.15, 1.21, 1.07]

gr = r.Graphics(width=8.0, height=5.5)
gr.barplot(means, grp, main="各班組平均產量", xlab="班組", ylab="平均產量 (公克)")
gr.save("/tmp/opencode/probe-bar.svg")
print("ok")
