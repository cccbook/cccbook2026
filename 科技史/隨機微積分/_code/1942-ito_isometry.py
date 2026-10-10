#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""1942 Ito 等距對應 wiki 說明
對應 wiki：1942 年 Ito 積分與 Ito 等距 E[(int_0^1 W dW)^2] = int_0^1 E[W^2]dt = 1/2。
int_0^1 W dW 以左端點黎曼和逼近 = (W_1^2-1)/2，均值 0、變異數 1/2。
右端點和則均值 1，展示 Ito 抉擇（非預測被積函數會改變期望）。
規範：只用 numpy，固定種子，不畫圖只印數字，結尾印 VERIFY 並用 assert 把關。
"""
import numpy as np

np.random.seed(7)

Npaths = 50000
Nsteps = 500
h = 1.0 / Nsteps
sqh = np.sqrt(h)

W = np.zeros(Npaths)
I_left = np.zeros(Npaths)
I_right = np.zeros(Npaths)

for _ in range(Nsteps):
    dW = sqh * np.random.randn(Npaths)
    I_left += W * dW
    I_right += (W + dW) * dW
    W += dW

mean_left = float(np.mean(I_left))
var_left = float(np.var(I_left))
mean_right = float(np.mean(I_right))

print(f"Ito int_0^1 W dW left-sum Npaths={Npaths} Nsteps={Nsteps}")
print(f"left  mean={mean_left:.5f} (theory 0) var={var_left:.5f} (theory 0.5)")
print(f"right mean={mean_right:.5f} (theory 1.0)")

assert abs(mean_left) < 0.01, f"|mean_left|={abs(mean_left)} >= 0.01"
assert abs(var_left - 0.5) / 0.5 < 0.05, f"var rel err={abs(var_left-0.5)/0.5} >= 5%"
assert abs(mean_right - 1.0) < 0.05, f"right mean {mean_right} not ~1"
print(f"VERIFY 1942 Ito isometry: mean={mean_left:.5f} var={var_left:.5f} right_mean={mean_right:.5f} PASS")
