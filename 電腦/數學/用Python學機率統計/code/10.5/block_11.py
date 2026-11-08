# 10.5-完整案例
# 由 10.5-完整案例.md 抽出：以 python3.14 + PYTHONPATH 指向 rstatistics 執行

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
