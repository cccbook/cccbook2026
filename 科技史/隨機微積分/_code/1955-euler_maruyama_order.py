#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""1955 Euler-Maruyama 強收斂階對應 wiki 說明
對應 wiki：1955 年 Skorokhod / Euler-Maruyama 方法，強階 0.5（弱階 1.0）。
註：OU 為加性噪音，EM 強階實際是 1.0（與 Milstein 重合），無法展示 0.5；
本程式改用同樣有精確解的 GBM（乘性噪音 dS = mu*S dt + sigma*S dW），
以同布朗路徑比較 EM 終值強誤差 e(h) = (E|S_T - S^h_T|^2)^{1/2} ~ C*h^{0.5}。
h=[0.04,0.02,0.01] 共用布朗增量，精確解 S_T = S0*exp((mu-s^2/2)T + s*W_T)，
log-log 斜率約 0.5。
規範：只用 numpy，固定種子，不畫圖只印數字，結尾印 VERIFY 並用 assert 把關。
"""
import numpy as np

np.random.seed(11)

mu = 0.5
sigma = 1.0
S0 = 1.0
T = 1.0
h_list = [0.04, 0.02, 0.01]
h_ref = 0.001
M = 20000

N_ref = int(round(T / h_ref))
dW_fine = np.sqrt(h_ref) * np.random.randn(M, N_ref)
W_T = dW_fine.sum(axis=1)
S_exact = S0 * np.exp((mu - 0.5 * sigma ** 2) * T + sigma * W_T)

errors = []
for h in h_list:
    k = int(round(h / h_ref))
    N_c = int(round(T / h))
    dW_c = dW_fine.reshape(M, N_c, k).sum(axis=2)
    S = np.full(M, S0)
    for j in range(N_c):
        S = S + mu * S * h + sigma * S * dW_c[:, j]
    err = float(np.sqrt(np.mean((S - S_exact) ** 2)))
    errors.append(err)
    print(f"h={h:.3f} N={N_c} strong_err={err:.6f}")

logh = np.log(h_list)
loge = np.log(errors)
slope = float(np.polyfit(logh, loge, 1)[0])
print(f"errors={['%.6f' % e for e in errors]}")
print(f"log-log slope={slope:.4f} (theory 0.5)")

assert 0.35 <= slope <= 0.65, f"slope {slope} outside [0.35, 0.65]"
print(f"VERIFY 1955 Euler-Maruyama strong order: slope={slope:.4f} in [0.35,0.65] PASS")
