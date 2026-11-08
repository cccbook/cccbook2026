# 10.4-函數曲線柱狀圖與圖例
# 由 10.4-函數曲線柱狀圖與圖例.md 抽出：以 python3.14 + PYTHONPATH 指向 rstatistics 執行

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
