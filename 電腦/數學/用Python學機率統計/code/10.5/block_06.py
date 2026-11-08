# 10.5-完整案例
# 由 10.5-完整案例.md 抽出：以 python3.14 + PYTHONPATH 指向 rstatistics 執行

import rstatistics as r

g = r.set_seed(2026)
n = 60
day = [round(v, 3) for v in g.rnorm(n, 100.0, 6.0)]
night = [round(v, 3) for v in g.rnorm(n, 102.5, 6.0)]

tt = r.t_test(day, night)
print(tt)
print("  statistic =", tt.statistic)
print("  p_value =", tt.p_value)
print("  conf_int =", tt.conf_int)
print("  estimate =", tt.estimate)
print("  df =", tt.parameter)
