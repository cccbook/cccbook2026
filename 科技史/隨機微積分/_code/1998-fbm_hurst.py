"""1998 分數布朗運動 Hurst 估計（Cholesky 生成）。
對應 wiki：Mandelbrot–Van Ness (1968) fBM 定義；此處驗證自相似性
  Var B(t) = t^{2H}，即 log Var 對 log t 斜率 = 2H。
生成：時格 t_i = i/N (N=256，含 0 共 257 點)，
  共變異 C(s,t) = (s^{2H}+t^{2H}-|t-s|^{2H})/2，Cholesky L，路徑 = L z。
實驗：H = 0.1 與 0.7，各 500 條；逐 t 樣本變異數，
  線性迴歸 log Var ~ log t 得斜率，容忍 |slope - 2H| < 0.15。
只用 numpy，固定種子，不畫圖。
"""
import numpy as np

rng = np.random.default_rng(3)
N = 256
M = 500
Hs = (0.1, 0.7)
t = np.arange(N + 1) / N  # 含 0

slopes = {}
for H in Hs:
    p = 2.0 * H
    ti = t[:, None]
    tj = t[None, :]
    C = 0.5 * (ti ** p + tj ** p - np.abs(ti - tj) ** p)
    C += 1e-12 * np.eye(N + 1)  # 數值 jitter（H=0.1 時近奇異）
    L = np.linalg.cholesky(C)
    Z = rng.standard_normal((N + 1, M))
    paths = L @ Z  # (257, 500)
    var_t = np.var(paths[1:, :], axis=1, ddof=1)  # 去掉 t=0
    logt = np.log(t[1:])
    logv = np.log(var_t)
    slope, intercept = np.polyfit(logt, logv, 1)
    slopes[H] = float(slope)
    print(f"H = {H}: slope = {slope:.4f}, target 2H = {p:.4f}, err = {abs(slope - p):.4f}")

print(f"VERIFY slope_H01={slopes[0.1]:.4f} slope_H07={slopes[0.7]:.4f}")
assert abs(slopes[0.1] - 0.2) < 0.15, f"H=0.1 斜率偏差過大: {slopes[0.1]}"
assert abs(slopes[0.7] - 1.4) < 0.15, f"H=0.7 斜率偏差過大: {slopes[0.7]}"
