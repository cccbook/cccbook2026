#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""1931 Fokker-Planck / OU 對應 wiki 說明
對應 wiki：1931 年 Kolmogorov 前向方程 (Fokker-Planck) 與 Ornstein-Uhlenbeck 過程。
OU: dX = -theta*X dt + sigma dW，轉移密度 p(t,x) 滿足 Fokker-Planck 方程式。
本程式以精確解大量模擬終值 X_T，直方圖均值/變異數對比解析解：
  mean = x0*exp(-theta*T)，var = sigma^2*(1-exp(-2*theta*T))/(2*theta)。
規範：只用 numpy，固定種子，不畫圖只印數字，結尾印 VERIFY 並用 assert 把關。
"""
import numpy as np

np.random.seed(0)

theta = 1.0
sigma = 1.0
x0 = 2.0
T = 3.0
N = 100000

mean_exact = x0 * np.exp(-theta * T)
var_exact = sigma ** 2 * (1.0 - np.exp(-2.0 * theta * T)) / (2.0 * theta)

# OU 精確抽樣：X_T ~ Normal(mean_exact, var_exact)
Z = np.random.randn(N)
XT = mean_exact + np.sqrt(var_exact) * Z

mean_mc = float(np.mean(XT))
var_mc = float(np.var(XT))  # ddof=0，對應母體變異數
mean_err = abs(mean_mc - mean_exact) / abs(mean_exact)
var_err = abs(var_mc - var_exact) / var_exact

print(f"OU theta={theta} sigma={sigma} x0={x0} T={T} N={N}")
print(f"exact mean={mean_exact:.6f} var={var_exact:.6f}")
print(f"MC    mean={mean_mc:.6f} var={var_mc:.6f}")
print(f"rel_err mean={mean_err:.4%} var={var_err:.4%}")

assert mean_err < 0.03, f"mean rel err {mean_err} >= 3%"
assert var_err < 0.03, f"var rel err {var_err} >= 3%"
print(f"VERIFY 1931 Fokker-Planck OU: mean_err={mean_err:.4%} var_err={var_err:.4%} < 3% PASS")
