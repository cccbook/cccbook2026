# 10.1-裝置與版面
# 由 10.1-裝置與版面.md 抽出：以 python3.14 + PYTHONPATH 指向 rstatistics 執行

import rstatistics as r

g = r.set_seed(42)
x = [round(v, 3) for v in g.rnorm(30, 50.0, 5.0)]
y = [round(v, 3) for v in g.rnorm(30, 50.0, 5.0)]
y = [round(a + 0.35 * (b - 50.0), 3) for a, b in zip(y, x)]

gr = r.Graphics(width=7.0, height=5.0)
gr.plot_window([30.0, 70.0], [30.0, 70.0])      # ① 設使用者座標
gr.title("手動組裝的散佈圖", "X", "Y")             # ② 標題與軸標籤
xt = [v for v in r.pretty([30.0, 70.0], 5) if 30.0 <= v <= 70.0]
gr.axis(1, xt, [f"{v:g}" for v in xt])            # ③ 底部座標軸
yt = [v for v in r.pretty([30.0, 70.0], 5) if 30.0 <= v <= 70.0]
gr.axis(2, yt, [f"{v:g}" for v in yt])            # ④ 左側座標軸
gr.box()                                          # ⑤ 畫框
gr.points(x, y, pch=1, col="black")               # ⑥ 資料點
gr.abline(h=50.0, v=50.0, col="gray")             # ⑦ 參考線
gr.legend(32.0, 68.0, ["樣本點"])                  # ⑧ 圖例
gr.save(\"img/10.1-scatter.svg\")                        # 覆寫成「低階圖元組裝版」
print("已存 10.1-scatter.svg")
print("usr =", [round(v, 3) for v in gr.usr])
