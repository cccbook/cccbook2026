# -*- coding: utf-8 -*-
"""1956 一維 Poisson P1 有限元素 (對應 wiki: 計算模擬學 / 有限元素法)
只用 numpy,固定種子。-u''=1,u(0)=u(1)=0,N=50 線性元。
驗證:與解析解 x(1-x)/2 的最大誤差 < 1e-3。
"""
import numpy as np

np.random.seed(0)
N = 50
h = 1.0 / N
n_in = N - 1  # 內點數

# 剛度矩陣 (1/h)*tridiag(-1,2,-1),載重全為 h (f=1)
diag = np.full(n_in, 2.0 / h)
off = np.full(n_in - 1, -1.0 / h)
A = np.diag(diag) + np.diag(off, 1) + np.diag(off, -1)
F = np.full(n_in, h * 1.0)

u_in = np.linalg.solve(A, F)
x_in = np.linspace(h, 1.0 - h, n_in)
u_exact = x_in * (1 - x_in) / 2.0
err = float(np.max(np.abs(u_in - u_exact)))
ok = err < 1e-3
print(f"N={N}, h={h:.4f}, max_err={err:.6e} (驗證 <1e-3: {'PASS' if ok else 'FAIL'})")
print(f"VERIFY: max_err={err:.10f}")
assert ok, "FEM 誤差過大"
print("ALL CHECKS PASS")
