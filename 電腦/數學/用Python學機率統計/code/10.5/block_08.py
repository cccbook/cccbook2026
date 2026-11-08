# 10.5-完整案例
# 由 10.5-完整案例.md 抽出：以 python3.14 + PYTHONPATH 指向 rstatistics 執行

import rstatistics as r

g = r.set_seed(2026)
n = 60
day = [round(v, 3) for v in g.rnorm(n, 100.0, 6.0)]
night = [round(v, 3) for v in g.rnorm(n, 102.5, 6.0)]

print("=== var_equal=True（合併變異數）===")
tp = r.t_test(day, night, var_equal=True)
print(tp)

print()
print("=== 單邊 ===")
print("alternative='less'  :", r.t_test(day, night, alternative="less").p_value)
print("alternative='greater':", r.t_test(day, night, alternative="greater").p_value)

print()
print("=== 90% CI ===")
t90 = r.t_test(day, night, conf_level=0.90)
print("conf_int =", t90.conf_int)
