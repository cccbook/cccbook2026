# 08.3-KS檢定與Shapiro-Wilk
# 由 08.3-KS檢定與Shapiro-Wilk.md 抽出：以 python3.14 + PYTHONPATH 指向 rstatistics 執行

import rstatistics as r

# 資料：某零件的量測值
g = r.set_seed(5)
x = [round(v, 4) for v in g.rnorm(30, 50.0, 3.0)]
print("常態母體的 30 筆資料：", x)
h = r.shapiro_test(x)
print(h)
print("  h.method         =", h.method)
print("  h.statistic_name =", h.statistic_name)
print("  h.statistic      =", h.statistic)
print("  h.p_value        =", h.p_value)
print()

# 明顯右偏的資料
y = [round(v, 4) for v in g.rexp(30, rate=0.1)]
print("指數分布（右偏）的 30 筆資料：", y)
print(r.shapiro_test(y))
