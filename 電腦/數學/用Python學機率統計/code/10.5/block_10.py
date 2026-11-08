# 10.5-完整案例
# 由 10.5-完整案例.md 抽出：以 python3.14 + PYTHONPATH 指向 rstatistics 執行

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

gr.save(\"img/10.5-traps.svg\")
print("已存 10.5-traps.svg")
print("A = 100.1, B = 103.2, 差距 =", round(103.2 - 100.1, 4))
print("(a) 截斷後：差距 3.1 佔軸範圍 7.0 的", round(3.1 / 7.0 * 100, 1), "%")
print("(b) 從 0 開始：差距 3.1 佔軸範圍 110.0 的", round(3.1 / 110.0 * 100, 1), "%")
print("視覺誇大倍數 =", round((3.1 / 7.0) / (3.1 / 110.0), 1), "倍")
