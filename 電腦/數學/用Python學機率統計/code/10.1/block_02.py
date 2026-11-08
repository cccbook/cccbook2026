# 10.1-裝置與版面
# 由 10.1-裝置與版面.md 抽出：以 python3.14 + PYTHONPATH 指向 rstatistics 執行

import rstatistics as r

g = r.set_seed(42)
x = [round(v, 3) for v in g.rnorm(30, 50.0, 5.0)]
y = [round(v, 3) for v in g.rnorm(30, 50.0, 5.0)]
y = [round(a + 0.35 * (b - 50.0), 3) for a, b in zip(y, x)]
print("x[:8] =", x[:8])
print("y[:8] =", y[:8])

gr = r.Graphics(width=7.0, height=5.0)
gr.plot(x, y, type="p", main="親自設定的散佈圖", xlab="X", ylab="Y")
print("plot 之後 usr =", [round(v, 4) for v in gr.usr])
print("資料範圍 x =", [min(x), max(x)], " y =", [min(y), max(y)])
print("x 軸外擴量 =", round(gr.usr[0] - min(x), 4), "/", round(gr.usr[1] - max(x), 4))
print("y 軸外擴量 =", round(gr.usr[2] - min(y), 4), "/", round(gr.usr[3] - max(y), 4))
print("plot_rect =", [round(v, 2) for v in gr.plot_rect])
print("device_x(min(x)) =", round(gr.device_x(min(x)), 2))
print("device_x(max(x)) =", round(gr.device_x(max(x)), 2))
print("user_x(device_x(50)) =", round(gr.user_x(gr.device_x(50.0)), 6))
gr.save(\"img/10.1-scatter.svg\")
print("已存 10.1-scatter.svg")
