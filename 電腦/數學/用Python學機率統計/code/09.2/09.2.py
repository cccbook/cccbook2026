# 09.2-係數的估計與標準誤
# 由 09.2-係數的估計與標準誤.md 抽出：以 python3.14 + PYTHONPATH 指向 rstatistics 執行

# --- 區塊 1 ---
import rstatistics as r

HEIGHT = [58.0, 59.0, 60.0, 61.0, 62.0, 63.0, 64.0, 65.0, 66.0, 67.0,
          68.0, 69.0, 70.0, 71.0, 72.0]
WEIGHT = [115.0, 117.0, 120.0, 123.0, 126.0, 129.0, 132.0, 135.0, 139.0, 142.0,
          146.0, 150.0, 154.0, 159.0, 164.0]

m = r.lm(WEIGHT, [HEIGHT], names=["height"])
sm = m.summary()
print(sm)

# ---------- 手算：殘差變異數、標準誤、t 值、p 值 ----------
n = len(HEIGHT)
res = [yi - fi for yi, fi in zip(WEIGHT, m.fitted_values)]
rss = sum(e * e for e in res)
s2 = rss / (n - 2)
sd_res = s2 ** 0.5
xb = r.mean(HEIGHT)
yb = r.mean(WEIGHT)
sxx = sum((xi - xb) ** 2 for xi in HEIGHT)
se_b = sd_res / sxx ** 0.5
se_a = sd_res * (1.0 / n + xb * xb / sxx) ** 0.5
t_b = m.coefficients[1] / se_b
p_b = 2 * r.pt(abs(t_b), n - 2, lower_tail=False)

print("手算對照：")
print("  n = %d, 自由度 = %d" % (n, n - 2))
print("  RSS = %.4f" % rss)
print("  s² = RSS/(n-2) = %.4f, s = %.4f   (summary: %.4f)" % (s2, sd_res, sm.sigma))
print("  SE(b) = s/sqrt(Sxx) = %.5f   (summary: %.5f)" % (se_b, sm.std_errors[1]))
print("  SE(a) = s*sqrt(1/n+xbar^2/Sxx) = %.5f   (summary: %.5f)" % (se_a, sm.std_errors[0]))
print("  t(b) = %.4f   (summary: %.4f)" % (t_b, sm.t_values[1]))
print("  p(b) = %.4g   (summary: %.4g)" % (p_b, sm.p_values[1]))

# ---------- R² 與 cor 的關係 ----------
rho = r.cor(HEIGHT, WEIGHT)
print()
print("R² = %.6f" % sm.r_squared)
print("cor(x, y) = %.6f, cor² = %.6f" % (rho, rho * rho))
print("R² == cor² ? %s" % (abs(sm.r_squared - rho * rho) < 1e-12))

# ---------- 係數的信賴區間（概念，完整版在 9.5）----------
tcrit = r.qt(0.975, n - 2)
b = m.coefficients[1]
a = m.coefficients[0]
print()
print("95%% CI for 斜率 b: [%.4f, %.4f]" % (b - tcrit * se_b, b + tcrit * se_b))
print("95%% CI for 截距 a: [%.4f, %.4f]" % (a - tcrit * se_a, a + tcrit * se_a))
