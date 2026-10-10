# -*- coding: utf-8 -*-
"""1963 Lorenz 蝴蝶效應 (對應 wiki: 計算模擬學 / 混沌與奇異吸引子)
只用 numpy,固定種子。sigma=10,rho=28,beta=8/3,RK4 dt=0.01 跑 50 時間單位。
兩條初值差 1e-8 的軌跡,驗證 20 時間後分離 > 1 (混沌發散)。
"""
import numpy as np

np.random.seed(0)
sigma, rho, beta = 10.0, 28.0, 8.0 / 3.0
dt = 0.01
T = 50.0
steps = int(T / dt)
split_step = int(20.0 / dt)

def f(s):
    x, y, z = s
    return np.array([sigma * (y - x), x * (rho - z) - y, x * y - beta * z])

def rk4(s):
    k1 = f(s); k2 = f(s + 0.5 * dt * k1)
    k3 = f(s + 0.5 * dt * k2); k4 = f(s + dt * k3)
    return s + dt * (k1 + 2 * k2 + 2 * k3 + k4) / 6.0

s1 = np.array([-8.0, 8.0, 27.0])  # 已在奇異吸引子上,20 時間內即可見指數發散
s2 = s1 + np.array([1e-8, 0.0, 0.0])
sep20 = None
for i in range(steps):
    s1 = rk4(s1); s2 = rk4(s2)
    if i + 1 == split_step:
        sep20 = float(np.linalg.norm(s2 - s1))
sep_final = float(np.linalg.norm(s2 - s1))
ok = sep20 > 1.0
print(f"初值差 1e-8, t=20 分離={sep20:.4f} (驗證 >1: {'PASS' if ok else 'FAIL'}), t=50 分離={sep_final:.4f}")
print(f"VERIFY: sep20={sep20:.6f}, sep_final={sep_final:.6f}")
assert ok, "未觀察到混沌發散"
print("ALL CHECKS PASS")
