# -*- coding: utf-8 -*-
"""1926 一維無限深阱有限差分（對應 wiki：計算模擬學 / Schrödinger 方程數值解）
阱寬 L=1（x∈[0,1]，ħ=m=1），真解本徵值 E_n=n²pi²/2。
內點 N=200，dx=1/(N+1)，H=-0.5·Laplacian 三對角矩陣
(diag=1/dx², offdiag=-1/(2dx²))，eigh 求本徵值，
驗證前三個相對誤差 <2%。
只用 numpy，固定種子。
"""
import numpy as np

np.random.seed(0)

N = 200
L = 1.0
dx = L / (N + 1)
diag_val = 1.0 / dx / dx
off_val = -0.5 / dx / dx
H = np.zeros((N, N))
np.fill_diagonal(H, diag_val)
idx = np.arange(N - 1)
H[idx, idx + 1] = off_val
H[idx + 1, idx] = off_val

evals = np.linalg.eigvalsh(H)  # 已由小到大排序
print(f"N={N} dx={dx:.6f}, 前五數值本徵值:")
for n in range(1, 6):
    theory = (n ** 2) * np.pi ** 2 / 2.0
    num = float(evals[n - 1])
    rel = abs(num - theory) / theory
    print(f"  n={n}: numeric={num:.6f} theory={theory:.6f} rel_err={rel:.6e}")

# 驗證數字：理論值 vs 實測（前三）
oks = []
for n in (1, 2, 3):
    theory = (n ** 2) * np.pi ** 2 / 2.0
    num = float(evals[n - 1])
    rel = abs(num - theory) / theory
    ok = rel < 0.02
    oks.append(ok)
    print(f"VERIFY E{n}: numeric={num:.6f} vs theory={theory:.6f}, rel={rel:.3e} (<2%? {ok})")
assert all(oks), "前三本徵值誤差超過 2%"
print("PASS")
