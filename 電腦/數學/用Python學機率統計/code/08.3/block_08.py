# 08.3-KS檢定與Shapiro-Wilk
# 由 08.3-KS檢定與Shapiro-Wilk.md 抽出：以 python3.14 + PYTHONPATH 指向 rstatistics 執行

import rstatistics as r

g = r.set_seed(5)
x = [round(v, 4) for v in g.rnorm(30, 50.0, 3.0)]
y = [round(v, 4) for v in g.rexp(30, rate=0.1)]

def qq_draw(v, title, path):
    # 標準化，讓 Q-Q 圖的兩個軸同尺度
    m = r.mean(v)
    s = r.sd(v)
    z = [(q - m) / s for q in v]
    t, sm = r.qqnorm_coords(z)
    lo = min(min(t), min(sm))
    hi = max(max(t), max(sm))
    gr = r.Graphics(width=6.0, height=6.0)
    gr.plot(t, sm, type="p", main=title, xlab="理論分位數（常態）", ylab="樣本分位數（標準化）",
            xlim=[lo, hi], ylim=[lo, hi])
    qx = r.quantile(t, [0.25, 0.75])
    qy = r.quantile(sm, [0.25, 0.75])
    slope = (qy[1] - qy[0]) / (qx[1] - qx[0])
    icept = qy[0] - slope * qx[0]
    gr.lines([t[0], t[len(t) - 1]], [icept + slope * t[0], icept + slope * t[len(t) - 1]], "red")
    gr.save(path)
    print("已存", path)

qq_draw(x, "常態資料的 Q-Q 圖", "08.3-qq-normal.svg")
qq_draw(y, "指數資料的 Q-Q 圖", "08.3-qq-exponential.svg")
