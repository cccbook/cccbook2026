#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""1976 Malliavin Delta（對應 wiki：Malliavin 微積分 / Bismut–Elworthy–Li Greeks）。
歐式 call：Delta = e^{-rT} E[Phi(S_T) * W_T/(S0*sigma*T)]（Malliavin 權重），
對照解析解 N(d1) 與 bump-and-revalue（共同亂數，h=1）。
S0=K=100, r=0.05, sigma=0.2, T=1。要求 Malliavin 相對誤差 < 2%。
只用 numpy（常態 CDF 用 math.erf），固定種子，不畫圖。
"""
import numpy as np
import time
from math import erf

t0 = time.time()
SEED = 1976
np.random.seed(SEED)

S0, K, r, sigma, T = 100.0, 100.0, 0.05, 0.2, 1.0
N = 1_000_000
h = 1.0

_v_erf = np.vectorize(erf)


def ncdf(x):
    return 0.5 * (1.0 + _v_erf(x / np.sqrt(2.0)))


d1 = (np.log(S0 / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
delta_exact = float(ncdf(d1))

Z = np.random.randn(N)
W = np.sqrt(T) * Z
grow = np.exp((r - 0.5 * sigma ** 2) * T + sigma * W)
ST = S0 * grow
pay = np.maximum(ST - K, 0.0)
disc = np.exp(-r * T)

delta_mal = float(disc * np.mean(pay * W / (S0 * sigma * T)))

# bump-and-revalue（共同亂數）
pay_up = np.maximum((S0 + h) * grow - K, 0.0)
pay_dn = np.maximum((S0 - h) * grow - K, 0.0)
delta_bump = float(disc * np.mean((pay_up - pay_dn) / (2 * h)))

rel_mal = abs(delta_mal - delta_exact) / delta_exact
rel_bump = abs(delta_bump - delta_exact) / delta_exact

print(f"[malliavin] seed={SEED} N={N} S0=K=100 r={r} sig={sigma} T={T}")
print(f"[malliavin] exact N(d1)={delta_exact:.6f}")
print(f"[malliavin] Malliavin ={delta_mal:.6f} relerr={rel_mal:.4%}")
print(f"[malliavin] bump(h={h})={delta_bump:.6f} relerr={rel_bump:.4%}")
print(f"[malliavin] elapsed {time.time()-t0:.2f}s")

assert rel_mal < 0.02, f"Malliavin relerr {rel_mal} exceeds 2%"
assert rel_bump < 0.03, f"bump relerr {rel_bump} exceeds 3%"
print(f"VERIFY: malliavin relerr={rel_mal:.4%}<2%, bump relerr={rel_bump:.4%} PASS")
