# 10.5-完整案例
# 由 10.5-完整案例.md 抽出：以 python3.14 + PYTHONPATH 指向 rstatistics 執行

import rstatistics as r

g = r.set_seed(2026)
n = 60
day = [round(v, 3) for v in g.rnorm(n, 100.0, 6.0)]
night = [round(v, 3) for v in g.rnorm(n, 102.5, 6.0)]

tt = r.t_test(day, night)
diff = tt.estimate[0] - tt.estimate[1]
lo_ci = tt.conf_int[0]
hi_ci = tt.conf_int[1]
se = (r.sd(day) ** 2 / len(day) + r.sd(night) ** 2 / len(night)) ** 0.5

gr = r.Graphics(width=9.0, height=5.5)
gr.plot_window([-6.5, 1.5], [0.0, 1.0])
gr.title("平均重量差（日班 − 夜班）的 95% 信賴區間")
xt = [v for v in r.pretty([-6.5, 1.5], 5) if -6.5 <= v <= 1.5]
gr.axis(1, xt, [f"{v:g}" for v in xt])
gr.axis(2, [0.0, 1.0], [""])
gr.box()
# 0 的參考線（垂直）
gr.segments([0.0], [0.0], [0.0], [1.0], "gray")
# 信賴區間
gr.segments([lo_ci], [0.42], [hi_ci], [0.42], "black", 2.5)
gr.segments([lo_ci], [0.33], [lo_ci], [0.51], "black", 2.5)
gr.segments([hi_ci], [0.33], [hi_ci], [0.51], "black", 2.5)
# 點估計
gr.segments([diff], [0.22], [diff], [0.62], "red", 3.5)
gr.text(-6.2, 0.82, f"點估計 = {diff:.3f}（紅線）", col="red")
gr.text(-6.2, 0.68, f"95% CI = [{lo_ci:.3f}, {hi_ci:.3f}]（黑線）", col="black")
gr.text(-6.2, 0.56, f"SE = {se:.4f}   t = {tt.statistic:.4f}   df = {tt.parameter[0]:.2f}", col="black")
gr.text(-6.2, 0.44, f"p = {tt.p_value:.5f} < 0.05", col="black")
gr.text(-6.2, 0.14, "灰線 = 0（無差異的虛無假設）", col="gray")
gr.mtext("信賴區間不包含 0，故拒絕 H0: 平均差 = 0", side=1, line=4, cex=0.85)
gr.save(\"img/10.5-ci.svg\")
print("已存 10.5-ci.svg")
print("diff =", round(diff, 5), " CI =", [round(lo_ci, 5), round(hi_ci, 5)], " se =", round(se, 5))
