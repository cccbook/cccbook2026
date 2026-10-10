#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""1982 OU 逆時倒播（對應 wiki：Anderson 逆時 SDE / score-based 生成模型溯源）。
前向 OU：dX = -a*X dt + sig*dW，X0 ~ N(mu0=2, v0=1)，跑至 T=2（近似平穩）。
邊際解析：m(t)=mu0*e^{-at}，v(t)=e^{-2at}*v0 + sig^2/(2a)*(1-e^{-2at})，
score = -(x-m(t))/v(t)。
逆時（Anderson）：dY = [-f + g^2*score] dtau + g*dWbar
              = [a*Y - sig^2*(Y-m(t))/v(t)] dtau + sig*dWbar，t=T-tau。
以 X_T 樣本為 Y_0 倒播回 tau=T，驗證重建均值/變異數 ≈ (mu0, v0)，誤差 < 8%。
只用 numpy，固定種子，不畫圖。
"""
import numpy as np
import time

t0 = time.time()
SEED = 1982
np.random.seed(SEED)

a, sig = 1.0, 1.0
mu0, v0 = 2.0, 1.0
T = 2.0
dt = 0.01
nsteps = int(round(T / dt))
M = 100_000


def m_v(t):
    e1 = np.exp(-a * t)
    return mu0 * e1, np.exp(-2 * a * t) * v0 + sig ** 2 / (2 * a) * (1 - np.exp(-2 * a * t))


# 前向（精確轉移）
X = mu0 + np.sqrt(v0) * np.random.randn(M)
efd = np.exp(-a * dt)
sfd = sig * np.sqrt((1 - np.exp(-2 * a * dt)) / (2 * a))
for _ in range(nsteps):
    X = X * efd + sfd * np.random.randn(M)

mT, vT = m_v(T)
print(f"[revOU] fwd: mean={np.mean(X):.5f} (target {mT:.5f}), "
      f"var={np.var(X):.5f} (target {vT:.5f})")

# 逆時倒播
Y = X.copy()
sq = np.sqrt(dt)
for k in range(nsteps):
    t = T - k * dt
    m, v = m_v(t)
    drift = a * Y - sig ** 2 * (Y - m) / v
    Y = Y + drift * dt + sig * sq * np.random.randn(M)

mean_r, var_r = float(np.mean(Y)), float(np.var(Y))
rel_mean = abs(mean_r - mu0) / abs(mu0)
rel_var = abs(var_r - v0) / v0

print(f"[revOU] seed={SEED} M={M} dt={dt} steps={nsteps} a={a} sig={sig} T={T}")
print(f"[revOU] recon: mean={mean_r:.5f} (target {mu0:.4f}, relerr {rel_mean:.4%})")
print(f"[revOU] recon: var ={var_r:.5f} (target {v0:.4f}, relerr {rel_var:.4%})")
print(f"[revOU] elapsed {time.time()-t0:.2f}s")

assert rel_mean < 0.08, f"mean relerr {rel_mean} exceeds 8%"
assert rel_var < 0.08, f"var relerr {rel_var} exceeds 8%"
print(f"VERIFY: reverse_ou mean_relerr={rel_mean:.4%}, var_relerr={rel_var:.4%} <8% PASS")
