# 08.3-KS檢定與Shapiro-Wilk
# 由 08.3-KS檢定與Shapiro-Wilk.md 抽出：以 python3.14 + PYTHONPATH 指向 rstatistics 執行

import rstatistics as r

g = r.set_seed(2024)
x = [round(v, 4) for v in g.rnorm(50, 10.0, 2.0)]
y = [round(v, 4) for v in g.rnorm(50, 10.5, 2.0)]

h = r.ks_test(x, y)
print(h)
print("  h.method         =", h.method)
print("  h.statistic_name =", h.statistic_name)
print("  h.statistic      =", h.statistic)
print("  h.p_value        =", h.p_value)
print("  h.alternative    =", h.alternative)
print()

print("alternative='less'    :", r.ks_test(x, y, alternative="less").p_value)
print("alternative='greater' :", r.ks_test(x, y, alternative="greater").p_value)
print("exact=False（漸近近似）:", r.ks_test(x, y, exact=False).p_value)
print()
h_exact = r.ks_test(x, y)
h_asym = r.ks_test(x, y, exact=False)
print("精確 p =", h_exact.p_value)
print("漸近 p =", h_asym.p_value)
print("兩者相差 =", abs(h_exact.p_value - h_asym.p_value))
