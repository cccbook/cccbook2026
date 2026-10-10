#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""1979 CRR 二項樹（對應 wiki：Cox-Ross-Rubinstein 二項式模型 / 1979 年 CRR 論文）。
參數 S0=K=100, r=0.05, sigma=0.2, T=1（歐式 call）。
u=exp(s*sqrt(dt)), d=1/u, p=(exp(r*dt)-d)/(u-d)，向量化倒推。
比較 N=[50,200,800] 相對 BS 封閉解的誤差：要求誤差遞減且 N=800 誤差 < 0.5%。
只用 numpy（常態 CDF 用 math.erf），固定種子，不畫圖。
"""
import numpy as np
import time
from math import erf

t0 = time.time()
SEED = 1979
np.random.seed(SEED)

S0, K, r, sigma, T = 100.0, 100.0, 0.05, 0.2, 1.0
Ns = [50, 200, 800]

_v_erf = np.vectorize(erf)


def ncdf(x):
    return 0.5 * (1.0 + _v_erf(x / np.sqrt(2.0)))


d1 = (np.log(S0 / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
d2 = d1 - sigma * np.sqrt(T)
C_bs = float(S0 * ncdf(d1) - K * np.exp(-r * T) * ncdf(d2))


def crr_call(N):
    dt = T / N
    u = np.exp(sigma * np.sqrt(dt))
    d = 1.0 / u
    p = (np.exp(r * dt) - d) / (u - d)
    disc = np.exp(-r * dt)
    j = np.arange(N + 1)
    ST = S0 * (u ** j) * (d ** (N - j))
    V = np.maximum(ST - K, 0.0)
    for _ in range(N, 0, -1):
        V = disc * (p * V[1:] + (1.0 - p) * V[:-1])
    return float(V[0])


prices, rels = [], []
for N in Ns:
    c = crr_call(N)
    rel = abs(c - C_bs) / C_bs
    prices.append(c)
    rels.append(rel)
    print(f"[crr] N={N:4d} price={c:.5f} BS={C_bs:.5f} relerr={rel:.4%}")

print(f"[crr] elapsed {time.time()-t0:.2f}s")

assert rels[0] > rels[1] > rels[2], f"errors not decreasing: {rels}"
assert rels[2] < 0.005, f"N=800 relerr {rels[2]} exceeds 0.5%"
print(f"VERIFY: crr relerrs={[f'{e:.4%}' for e in rels]} decreasing, N=800<0.5% PASS")
