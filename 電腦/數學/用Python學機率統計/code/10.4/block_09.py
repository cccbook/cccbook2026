# 10.4-函數曲線柱狀圖與圖例
# 由 10.4-函數曲線柱狀圖與圖例.md 抽出：以 python3.14 + PYTHONPATH 指向 rstatistics 執行

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
