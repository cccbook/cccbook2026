# 07.5-檢定與信賴區間的對偶
# 由 07.5-檢定與信賴區間的對偶.md 抽出：以 python3.14 + PYTHONPATH 指向 rstatistics 執行

# --- 區塊 1 ---
import rstatistics as r
x = [499.8,493.1,498.2,497.2,494.8,487.0,494.5,493.3,498.1,
     495.6,495.9,494.5,496.7,496.7,486.9,503.3]

bad = 0
for k in range(400):
    mu0 = 488.0 + k * 0.05          # 488.00, 488.05, ..., 507.95
    t = r.t_test(x, mu=mu0)
    lo, hi = t.conf_int
    inside = (lo <= mu0 <= hi)       # mu0 在 95% CI 內？
    sig = (t.p_value < 0.05)        # 雙尾檢定顯著？
    if inside == sig:               # 兩者一致才對
        bad += 1
print("不一致的 mu0 個數:", bad)


# --- 區塊 2 ---
print("=== 單尾 less ===")
bad = 0
for k in range(400):
    mu0 = 488.0 + k * 0.05
    t = r.t_test(x, mu=mu0, alternative='less')
    lo, hi = t.conf_int              # 單邊 CI: (-inf, hi]
    if (mu0 > hi) != (t.p_value < 0.05):
        bad += 1
print("不一致的 mu0 個數:", bad)

print("=== 單尾 greater ===")
bad = 0
for k in range(400):
    mu0 = 488.0 + k * 0.05
    t = r.t_test(x, mu=mu0, alternative='greater')
    lo, hi = t.conf_int              # 單邊 CI: [lo, inf)
    if (mu0 < lo) != (t.p_value < 0.05):
        bad += 1
print("不一致的 mu0 個數:", bad)


# --- 區塊 3 ---
A = [12.1,12.4,11.9,12.3,12.0,12.2,11.8,12.5,12.1,12.0,11.9,12.3]
B = [9.8,11.6,12.9,10.4,11.2,13.1,9.5,12.4,10.8,11.7]

print("=== 兩樣本 Welch：掃 mu0（平均差）===")
bad = 0
for k in range(200):
    mu0 = -0.5 + k * 0.02
    t = r.t_test(A, B, mu=mu0)
    lo, hi = t.conf_int
    if (lo <= mu0 <= hi) == (t.p_value < 0.05):
        bad += 1
print("不一致個數:", bad)

before = [148,132,141,155,129,138,150,144,136,147,133,142]
after  = [132,124,128,140,120,130,138,135,126,136,125,130]
print("=== 配對 t 檢定：掃 mu0（平均差）===")
bad = 0
for k in range(200):
    mu0 = 5.0 + k * 0.05
    t = r.t_test(before, after, paired=True, mu=mu0)
    lo, hi = t.conf_int
    if (lo <= mu0 <= hi) == (t.p_value < 0.05):
        bad += 1
print("不一致個數:", bad)


# --- 區塊 4 ---
print("=== 比例檢定：掃 p0 ===")
bad = 0
for xi in range(0, 101):
    for p0 in [i/100 for i in range(1, 100)]:
        b = r.prop_test(xi, 100, p0)
        lo, hi = b.conf_int
        if (lo <= p0 <= hi) == (b.p_value < 0.05):
            bad += 1
print("不一致個數:", bad)


# --- 區塊 5 ---
print("mu0      p-value      95% CI                mu0 在 CI 內?  p<0.05?")
for mu0 in [490.0, 493.0, 493.139, 495.35, 497.561, 500.0]:
    t = r.t_test(x, mu=mu0)
    lo, hi = t.conf_int
    print(f"{mu0:7.3f}  {t.p_value:.6f}  [{lo:.3f}, {hi:.3f}]   {str(lo<=mu0<=hi):>10}  {str(t.p_value<0.05):>6}")


# --- 區塊 6 ---
for mu0 in [495.0, 497.1685, 497.2, 500.0]:
    t = r.t_test(x, mu=mu0, alternative='less')
    lo, hi = t.conf_int
    print(f"{mu0:8.4f}  p={t.p_value:.6f}  CI=({lo}, {hi:.4f}]  拒絕? {t.p_value<0.05}")


# --- 區塊 7 ---
print("=== 精確二項：掃 p0 ===")
bad = []
for xi in range(0, 101):
    for p0 in [i/100 for i in range(1, 100)]:
        b = r.binom_test(xi, 100, p0)
        lo, hi = b.conf_int
        if (lo <= p0 <= hi) == (b.p_value < 0.05):
            bad.append((xi, p0))
print("不一致個數:", len(bad), " 前 5 個:", bad[:5])


# --- 區塊 8 ---
b = r.binom_test(12, 100, 0.2)
print("p =", b.p_value)
print("CI =", b.conf_int)
print("0.2 在 CI 內？", b.conf_int[0] <= 0.2 <= b.conf_int[1])


# --- 區塊 9 ---
t = r.t_test(x, mu=500, conf_level=0.90)
print(t.conf_int)          # 90% CI
t2 = r.t_test(x, mu=500, conf_level=0.95)
print(t2.conf_int)         # 95% CI


# --- 區塊 10 ---
t_less = r.t_test(x, mu=500, alternative='less')
print("單尾 p =", t_less.p_value, " 單邊 CI =", t_less.conf_int)
