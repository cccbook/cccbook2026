"""1993 Heston 隨機波動率：全截斷 Euler 蒙地卡羅。
對應 wiki：Heston (1993) 閉式解 / 特徵函數定價；此處以蒙地卡羅驗證。
模型：dv = κ(θ-v)dt + ξ√v dWv, dS/S = r dt + √v dWs, Corr = ρ。
參數：S0=100, v0=0.04, κ=2, θ=0.04, ξ=0.3, ρ=-0.7；
定價參數：r=0.03, K=100, T=1.0（wiki 常見 ATM 基準）。
格式：變異數全截斷 v+ = max(v,0)；資產採 log-Euler
  S *= exp((r-0.5 v+)dt + √(v+ dt) Zs)，保證 S > 0。
驗證：同路徑 Call/Put 滿足 put-call parity
  C - P = S0 - K exp(-rT)，相對誤差(除以 S0) < 1%；
  且價格為正有限。
只用 numpy，固定種子，不畫圖。
"""
import numpy as np

rng = np.random.default_rng(1)
S0 = 100.0
v0 = 0.04
kappa = 2.0
theta = 0.04
xi = 0.3
rho = -0.7
r = 0.03
K = 100.0
T = 1.0
N = 100
dt = T / N
M = 100000

sqdt = np.sqrt(dt)
v = np.full(M, v0)
S = np.full(M, S0)
corr = np.sqrt(1.0 - rho ** 2)
for _ in range(N):
    z1 = rng.standard_normal(M)
    z2 = rng.standard_normal(M)
    zv = z1
    zs = rho * z1 + corr * z2
    vpos = np.maximum(v, 0.0)
    sqv = np.sqrt(vpos)
    v = v + kappa * (theta - vpos) * dt + xi * sqv * sqdt * zv
    S = S * np.exp((r - 0.5 * vpos) * dt + sqv * sqdt * zs)

disc = np.exp(-r * T)
C = float(np.mean(np.maximum(S - K, 0.0)) * disc)
P = float(np.mean(np.maximum(K - S, 0.0)) * disc)
lhs = C - P
rhs = S0 - K * np.exp(-r * T)
err = abs(lhs - rhs)
rel = err / S0

print(f"Call = {C:.6f}, Put = {P:.6f}")
print(f"parity LHS(C-P) = {lhs:.6f}, RHS = {rhs:.6f}")
print(f"abs_err = {err:.6f}, rel_err = {rel:.6f} (tol 0.01)")
print(f"VERIFY rel_parity_err={rel:.6f} C={C:.4f} P={P:.4f}")
assert np.isfinite(C) and np.isfinite(P), "價格非有限"
assert C > 0 and P > 0, "價格須為正"
assert rel < 0.01, f"put-call parity 誤差過大: {rel}"
