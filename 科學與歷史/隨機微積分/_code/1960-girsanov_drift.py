#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""1960 Girsanov 漂移變換（對應 wiki：Girsanov 定理 / 測度變換與漂移）。
P 下 W_T ~ N(0, T)。取 theta=0.7，題目指定的似然比
    L = exp(-theta*W_T - theta^2*T/2)      （= dP_-/dP，-theta 漂移的 RN 導數）
+theta 漂移測度 Q 的 RN 導數為 D = exp(+theta*W_T - theta^2*T/2)
= exp(-theta^2*T)/L。驗證：
  (1) E_P[L] ≈ 1 且 E_P[D] ≈ 1（指數鞅性），
  (2) E_Q[W_T] = E_P[D*W_T] ≈ theta*T。
只用 numpy，固定種子，不畫圖。
"""
import numpy as np
import time

t0 = time.time()
SEED = 1960
np.random.seed(SEED)

theta = 0.7
T = 1.0
N = 1_000_000

W = np.sqrt(T) * np.random.randn(N)
L = np.exp(-theta * W - 0.5 * theta ** 2 * T)   # 題目指定的 L
D = np.exp(theta * W - 0.5 * theta ** 2 * T)    # dQ/dP（+theta 漂移）
EL = float(np.mean(L))
ED = float(np.mean(D))
EQ_W = float(np.mean(D * W))                    # E_Q[W_T]
target = theta * T
err_EL = abs(EL - 1.0)
err_ED = abs(ED - 1.0)
rel_err = abs(EQ_W - target) / target

print(f"[girsanov] seed={SEED} N={N} theta={theta} T={T}")
print(f"[girsanov] E_P[L]      = {EL:.6f}  (target 1, abserr {err_EL:.2e})")
print(f"[girsanov] E_P[D]      = {ED:.6f}  (target 1, abserr {err_ED:.2e})")
print(f"[girsanov] E_Q[W_T]    = {EQ_W:.6f}  (target theta*T={target:.4f}, relerr {rel_err:.4%})")
print(f"[girsanov] elapsed {time.time()-t0:.2f}s")

assert err_EL < 0.01, f"E[L]={EL} deviates from 1"
assert err_ED < 0.02, f"E[D]={ED} deviates from 1"
assert rel_err < 0.05, f"E_Q[W_T]={EQ_W} vs {target} exceeds 5%"
print(f"VERIFY: girsanov E[L]={EL:.5f}≈1, E_Q[W_T]={EQ_W:.5f}≈theta*T={target:.4f} PASS")
