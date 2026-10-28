#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""1960 一維 Kalman 濾波（對應 wiki：Kalman 濾波 / 1960 年 Kalman 論文）。
狀態：x_{k+1} = x_k + w_k, w ~ N(0, Q)（隨機漫步）；
觀測：y_k = x_k + v_k, v ~ N(0, R)。
跑 500 步 Kalman 遞迴，驗證：
  (1) 濾波 RMSE 比 raw 觀測 RMSE 低三成以上（rmse_kf < 0.7*rmse_raw）；
  (2) 數值增益 K_500 吻合穩態理論增益 K_inf（誤差 < 1e-9）。
只用 numpy，固定種子，不畫圖。
"""
import numpy as np
import time

t0 = time.time()
SEED = 1960
np.random.seed(SEED)

Q = 1.0
R = 4.0
n = 500
x0 = 0.0
P0 = 1.0

w = np.sqrt(Q) * np.random.randn(n)
v = np.sqrt(R) * np.random.randn(n)
x_true = x0 + np.cumsum(w)          # x_k, k=1..n
y = x_true + v

# Kalman 遞迴
x_hat = 0.0
P = P0
K_last = 0.0
ests = np.empty(n)
for k in range(n):
    P_pred = P + Q
    K = P_pred / (P_pred + R)
    x_hat = x_hat + K * (y[k] - x_hat)
    P = (1.0 - K) * P_pred
    ests[k] = x_hat
    K_last = K

# 理論穩態：P = (-Q + sqrt(Q^2+4QR))/2，P_pred = P+Q，K_inf = P_pred/(P_pred+R)
P_inf = (-Q + np.sqrt(Q ** 2 + 4 * Q * R)) / 2.0
K_inf = (P_inf + Q) / (P_inf + Q + R)

rmse_raw = float(np.sqrt(np.mean((y - x_true) ** 2)))
rmse_kf = float(np.sqrt(np.mean((ests - x_true) ** 2)))
ratio = rmse_kf / rmse_raw
gain_err = abs(K_last - K_inf)

print(f"[kalman] seed={SEED} steps={n} Q={Q} R={R}")
print(f"[kalman] RMSE_raw={rmse_raw:.5f} RMSE_kf={rmse_kf:.5f} ratio={ratio:.4f} (need <0.7)")
print(f"[kalman] K_last={K_last:.10f} K_inf={K_inf:.10f} abserr={gain_err:.2e}")
print(f"[kalman] elapsed {time.time()-t0:.2f}s")

assert rmse_kf < 0.7 * rmse_raw, f"KF not 30% better: {rmse_kf} vs raw {rmse_raw}"
assert gain_err < 1e-9, f"steady gain mismatch: {K_last} vs {K_inf}"
print(f"VERIFY: kalman ratio={ratio:.4f}<0.7, gain_err={gain_err:.1e} PASS")
