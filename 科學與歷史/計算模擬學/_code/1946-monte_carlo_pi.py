# -*- coding: utf-8 -*-
"""1946 Monte Carlo 估 pi（對應 wiki：計算模擬學 / Monte Carlo 方法）
在 [0,1]² 均勻投 N=2e5 點，落入 x²+y²≤1（1/4 圓）比例 p→pi/4，
pi_est=4·count/N。統計誤差標度 ~1/sqrt(N)，
理論標準差 4·sqrt(p(1-p)/N)≈1.64/sqrt(N)。
驗證 |est-pi|<0.01。
只用 numpy，固定種子。
"""
import numpy as np

np.random.seed(0)

N = 200000
xy = np.random.rand(N, 2)
inside = np.sum(xy[:, 0] ** 2 + xy[:, 1] ** 2 <= 1.0)
pi_est = 4.0 * inside / N
err = abs(pi_est - np.pi)
scale = 1.0 / np.sqrt(N)
p = np.pi / 4.0
theory_std = 4.0 * np.sqrt(p * (1.0 - p) / N)

print(f"N={N} inside={inside} pi_est={pi_est:.6f} true={np.pi:.6f} err={err:.6e}")
print(f"理論標度 1/sqrt(N)={scale:.6e}, 理論標準差≈{theory_std:.6e} (≈1.64/sqrt(N))")
print(f"err/(1/sqrt(N)) = {err / scale:.4f} (應為 O(1) 量級)")

# 驗證數字：理論值 vs 實測
ok = err < 0.01
ok_scale = err < 5.0 * scale
print(f"VERIFY err={err:.6e} (<0.01? {ok})")
print(f"VERIFY err={err:.6e} (<5/sqrt(N)={5*scale:.6e}? {ok_scale})")
assert ok, f"Monte Carlo 誤差太大: {err}"
assert ok_scale, f"誤差偏離 1/sqrt(N) 標度: {err / scale:.2f}σ單位"
print("PASS")
