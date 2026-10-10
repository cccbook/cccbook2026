#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""1973 Black-Scholes 蒙地卡羅（對應 wiki：Black-Scholes 模型 / 1973 年 BS 論文）。
S0=100, K=100, r=0.05, sigma=0.2, T=1。風險中性下
  S_T = S0*exp((r-s^2/2)T + s*sqrt(T)*Z)。
用 30 萬條路徑估 call/put，驗證：
  (1) MC call 與 BS 封閉解相對誤差 < 1%；
  (2) put-call parity：C_mc - P_mc ≈ S0 - K*exp(-rT)。
只用 numpy（常態 CDF 用 math.erf），固定種子，不畫圖。
"""
import numpy as np
import time
from math import erf

t0 = time.time()
SEED = 1973
np.random.seed(SEED)

S0, K, r, sigma, T = 100.0, 100.0, 0.05, 0.2, 1.0
M = 300_000

_v_erf = np.vectorize(erf)


def ncdf(x):
    return 0.5 * (1.0 + _v_erf(x / np.sqrt(2.0)))


d1 = (np.log(S0 / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
d2 = d1 - sigma * np.sqrt(T)
C_bs = float(S0 * ncdf(d1) - K * np.exp(-r * T) * ncdf(d2))
P_bs = float(C_bs - (S0 - K * np.exp(-r * T)))  # parity 反解

Z = np.random.randn(M)
ST = S0 * np.exp((r - 0.5 * sigma ** 2) * T + sigma * np.sqrt(T) * Z)
disc = np.exp(-r * T)
C_mc = float(disc * np.mean(np.maximum(ST - K, 0.0)))
P_mc = float(disc * np.mean(np.maximum(K - ST, 0.0)))

parity_theory = S0 - K * np.exp(-r * T)
parity_mc = C_mc - P_mc
rel_call = abs(C_mc - C_bs) / C_bs
parity_err = abs(parity_mc - parity_theory)

print(f"[bsmc] seed={SEED} M={M} S0={S0} K={K} r={r} sig={sigma} T={T}")
print(f"[bsmc] call: MC={C_mc:.5f} BS={C_bs:.5f} relerr={rel_call:.4%}")
print(f"[bsmc] put : MC={P_mc:.5f} BS={P_bs:.5f} relerr={abs(P_mc-P_bs)/P_bs:.4%}")
print(f"[bsmc] parity: MC_diff={parity_mc:.5f} theory={parity_theory:.5f} abserr={parity_err:.5f}")
print(f"[bsmc] elapsed {time.time()-t0:.2f}s")

assert rel_call < 0.01, f"call relerr {rel_call} exceeds 1%"
assert parity_err < 0.15, f"parity abserr {parity_err} too large"
print(f"VERIFY: bsmc call_relerr={rel_call:.4%}<1%, parity_err={parity_err:.4f} PASS")
