# 10.3-箱型圖Q-Q圖與ECDF
# 由 10.3-箱型圖Q-Q圖與ECDF.md 抽出：以 python3.14 + PYTHONPATH 指向 rstatistics 執行

import rstatistics as r

g = r.set_seed(11)
norm = [round(v, 4) for v in g.rnorm(60, 0.0, 1.0)]
heavy = [round(v, 4) for v in g.rt(60, df=3)]

for name, v in [("常態", norm), ("重尾 t(3)", heavy)]:
    t, s = r.qqnorm_coords(v)
    print(f"--- {name} ---")
    print("  理論分位前三:", [round(q, 4) for q in t[:3]], " 樣本分位前三:", [round(q, 4) for q in s[:3]])
    print("  理論分位後三:", [round(q, 4) for q in t[-3:]], " 樣本分位後三:", [round(q, 4) for q in s[-3:]])
    qx = r.quantile(t, [0.25, 0.75])
    qy = r.quantile(s, [0.25, 0.75])
    slope = (qy[1] - qy[0]) / (qx[1] - qx[0])
    icept = qy[0] - slope * qx[0]
    print(f"  qqline: slope = {slope:.4f}, intercept = {icept:.4f}")
    print(f"  樣本 sd = {r.sd(v):.4f}")
    print(f"  左端 (i=1): 理論 {t[0]:.3f} 樣本 {s[0]:.3f} 差距 {s[0]-t[0]:+.3f}")
    print(f"  右端 (i=n): 理論 {t[-1]:.3f} 樣本 {s[-1]:.3f} 差距 {s[-1]-t[-1]:+.3f}")
    hs = r.shapiro_test(v)
    print(f"  Shapiro: W = {hs.statistic:.4f}, p = {hs.p_value:.4g}")
