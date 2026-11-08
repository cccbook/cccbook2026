# 10.5-完整案例
# 由 10.5-完整案例.md 抽出：以 python3.14 + PYTHONPATH 指向 rstatistics 執行

import rstatistics as r

g = r.set_seed(2026)
n = 60
day = [round(v, 3) for v in g.rnorm(n, 100.0, 6.0)]
night = [round(v, 3) for v in g.rnorm(n, 102.5, 6.0)]

m1, m2 = r.mean(day), r.mean(night)
s1, s2 = r.sd(day), r.sd(night)
n1, n2 = len(day), len(night)
diff = m1 - m2
v1 = s1**2 / n1
v2 = s2**2 / n2
se_w = (v1 + v2) ** 0.5
dfw = (v1 + v2) ** 2 / (v1**2 / (n1 - 1) + v2**2 / (n2 - 1))
t = diff / se_w
print("m1 =", round(m1, 5), " m2 =", round(m2, 5), " diff =", round(diff, 5))
print("s1 =", round(s1, 5), " s2 =", round(s2, 5))
print("v1 =", round(v1, 6), " v2 =", round(v2, 6))
print("se_welch =", round(se_w, 5), " df =", round(dfw, 4), " t =", round(t, 5))
print("p（用 pt 查表）=", r.pt(abs(t), dfw, lower_tail=False) * 2)
crit = r.qt(0.975, dfw)
print("t crit (0.975) =", round(crit, 5))
print("CI =", [round(diff - crit * se_w, 5), round(diff + crit * se_w, 5)])
