#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""1949 Feynman-Kac 熱方程對應 wiki 說明
對應 wiki：1949 年 Feynman-Kac 公式，拋物 PDE 以布朗期望表示。
熱方程 u_t = (1/2) u_xx，初值 u(0,x)=cos(x)，解 u(T,x)=E[cos(x+W_T)]=cos(x)*exp(-T/2)。
本程式 x=1.0、T=0.5，MC 驗證約 e^{-0.25}cos(1)，相對誤差<1%。
規範：只用 numpy，固定種子，不畫圖只印數字，結尾印 VERIFY 並用 assert 把關。
"""
import numpy as np

np.random.seed(3)

x = 1.0
T = 0.5
N = 600000

WT = np.sqrt(T) * np.random.randn(N)
payoff = np.cos(x + WT)
u_mc = float(np.mean(payoff))
u_exact = float(np.cos(x) * np.exp(-T / 2.0))
rel_err = abs(u_mc - u_exact) / abs(u_exact)

print(f"Heat Feynman-Kac x={x} T={T} N={N}")
print(f"exact u={u_exact:.6f} (=cos(1)*exp(-0.25))")
print(f"MC    u={u_mc:.6f} rel_err={rel_err:.4%}")

assert rel_err < 0.01, f"rel err {rel_err} >= 1%"
print(f"VERIFY 1949 Feynman-Kac heat: u_mc={u_mc:.6f} exact={u_exact:.6f} err={rel_err:.4%}<1% PASS")
