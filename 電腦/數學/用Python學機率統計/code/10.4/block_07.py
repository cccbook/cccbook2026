# 10.4-函數曲線柱狀圖與圖例
# 由 10.4-函數曲線柱狀圖與圖例.md 抽出：以 python3.14 + PYTHONPATH 指向 rstatistics 執行

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
