#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""1951 Ito GBM 對應 wiki 說明
對應 wiki：1951 年 Ito 引理，GBM dS = mu*S dt + sigma*S dW。
Ito 公式給精確解 S_T = S0*exp((mu-sigma^2/2)T + sigma*W_T)，故 E[S_T]=S0*exp(mu*T)。
若誤用常微分鏈鎖律（漏掉 -sigma^2/2）則 S_wrong = S0*exp(mu*T+sigma*W_T)，期望系統性偏高 e^{sigma^2 T/2} 倍。
規範：只用 numpy，固定種子，不畫圖只印數字，結尾印 VERIFY 並用 assert 把關。
"""
import numpy as np

np.random.seed(5)

S0 = 100.0
mu = 0.1
sigma = 0.3
T = 1.0
N = 300000

W = np.sqrt(T) * np.random.randn(N)
S_correct = S0 * np.exp((mu - 0.5 * sigma ** 2) * T + sigma * W)
S_wrong = S0 * np.exp(mu * T + sigma * W)  # 誤用常微分鏈鎖律：少了 -sigma^2/2

mean_correct = float(np.mean(S_correct))
mean_wrong = float(np.mean(S_wrong))
exact = S0 * np.exp(mu * T)
rel_err = abs(mean_correct - exact) / exact
wrong_bias = (mean_wrong - exact) / exact
theory_wrong_factor = np.exp(0.5 * sigma ** 2 * T) - 1.0

print(f"GBM S0={S0} mu={mu} sigma={sigma} T={T} N={N}")
print(f"exact E[S_T]={exact:.4f}")
print(f"correct MC mean={mean_correct:.4f} rel_err={rel_err:.4%}")
print(f"wrong   MC mean={mean_wrong:.4f} bias=+{wrong_bias:.2%} (theory +{theory_wrong_factor:.2%})")

assert rel_err < 0.01, f"correct rel err {rel_err} >= 1%"
assert wrong_bias > 0.03, f"wrong bias {wrong_bias} not systematically high"
print(f"VERIFY 1951 Ito GBM: correct_err={rel_err:.4%}<1% wrong_bias=+{wrong_bias:.2%}>3% PASS")
