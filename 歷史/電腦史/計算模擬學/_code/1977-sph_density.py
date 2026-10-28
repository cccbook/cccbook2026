# -*- coding: utf-8 -*-
"""1977 SPH 密度估計：一維三次樣條核
對應 wiki：Lucy (1977) / Gingold-Monaghan SPH；一維三次樣條核做密度估計。
64 粒子按正弦密度 rho(x)=1+A*sin(2πx), A=0.2 分層取樣（分位數），週期域 [0,1)。
m=1/64，h=0.03，週期最小映像。驗證 SPH vs 真值 L2 誤差 < 0.05。只用 numpy，固定種子。
"""
import numpy as np

np.random.seed(0)

N = 64
A = 0.2
h = 0.03
m = 1.0 / N


def rho_true(x):
    return 1.0 + A * np.sin(2.0 * np.pi * x)


def cdf(x):
    # C(x)=x + A*(1-cos(2πx))/(2π)
    return x + A * (1.0 - np.cos(2.0 * np.pi * x)) / (2.0 * np.pi)


# 分層分位數反演 CDF（單調）求粒子位置
targets = (np.arange(N) + 0.5) / N
pos = np.empty(N)
for i, t in enumerate(targets):
    lo, hi = 0.0, 1.0
    for _ in range(60):
        mid = 0.5 * (lo + hi)
        if cdf(mid) < t:
            lo = mid
        else:
            hi = mid
    pos[i] = 0.5 * (lo + hi)
pos = np.sort(pos)


def W1d(r, h):
    # 一維三次樣條核（含 1/h 歸一）
    q = np.abs(r) / h
    w = np.zeros_like(q)
    m1 = q < 1.0
    m2 = (~m1) & (q < 2.0)
    w[m1] = (2.0 / 3.0 - q[m1] ** 2 + 0.5 * q[m1] ** 3) / h
    w[m2] = ((2.0 - q[m2]) ** 3 / 6.0) / h
    return w


# 週期最小映像成對距離 (N,N)，向量化
dx = pos[:, None] - pos[None, :]
dx = dx - np.round(dx)  # 映到 [-0.5, 0.5)
K = W1d(dx, h)
rho_est = m * np.sum(K, axis=1)
rt = rho_true(pos)
err_l2 = float(np.sqrt(np.mean((rho_est - rt) ** 2)))
err_rel = float(err_l2 / np.mean(rt))
print(f"N={N} A={A} h={h} m={m:.6f}")
print(f"rho_true mean={np.mean(rt):.4f} est mean={np.mean(rho_est):.4f}")
print(f"max|err|={np.max(np.abs(rho_est - rt)):.4f}")
print(f"VERIFY L2={err_l2:.5f} rel={err_rel:.5f} (<0.05? {err_l2 < 0.05})")
assert err_l2 < 0.05, f"SPH L2 error too large: {err_l2}"
print("PASS")
