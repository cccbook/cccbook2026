# 10.1-裝置與版面
# 由 10.1-裝置與版面.md 抽出：以 python3.14 + PYTHONPATH 指向 rstatistics 執行

# --- 區塊 1 ---
import rstatistics as r

gr = r.Graphics(width=7.0, height=5.0)
print("mar =", gr.mar)
print("mgp =", gr.mgp)
print("cex =", gr.cex, " pch =", gr.pch, " lwd =", gr.lwd)
print("mfrow =", gr.mfrow)
print("usr（尚未 plot，預設）=", gr.usr)


# --- 區塊 2 ---
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
gr.save("img/10.1-scatter.svg")
print("已存 10.1-scatter.svg")


# --- 區塊 3 ---
import rstatistics as r

print("=== r.pretty 的示範 ===")
for rng in ([1.0, 20.0], [0.0, 1.0], [3.14159, 3.14160], [-0.5, 0.5], [0.0, 97.3]):
    print(f"  pretty({rng}, 5) =", r.pretty(list(rng), 5))
print("  pretty([1,20], 4) =", r.pretty([1.0, 20.0], 4))
print("  pretty([1,20], 8) =", r.pretty([1.0, 20.0], 8))
print("  pretty([1,20], 10) =", r.pretty([1.0, 20.0], 10))


# --- 區塊 4 ---
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
gr.save("img/10.1-scatter.svg")                        # 覆寫成「低階圖元組裝版」
print("已存 10.1-scatter.svg")
print("usr =", [round(v, 3) for v in gr.usr])
