#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""1975 Milstein 強收斂階（對應 wiki：Milstein 方法 / Euler–Maruyama 強誤差階）。
SDE：dX = -X^3 dt + X dW（漂移 a=-x^3，擴散 b=x，b'=1，
Milstein 修正項 0.5*b*b'*(dW^2-dt) = 0.5*X*((dW)^2-dt) 明顯非零）。
無解析解，故以細網格 Milstein 解為參考解 X_ref，
同一組布朗路徑下比較 dt=[0.04,0.02,0.01,0.005] 的強誤差
  E|X_T^{scheme} - X_ref|，log-log 斜率 Milstein 應 ≈1.0。
只用 numpy，固定種子，不畫圖。
"""
import numpy as np
import time

t0 = time.time()
SEED = 1975
np.random.seed(SEED)

X0, T = 0.5, 1.0
M = 8000
N_fine = 1600
dt_fine = T / N_fine
dts = np.array([0.04, 0.02, 0.01, 0.005])


def step_euler(x, dw, dt):
    return x - x ** 3 * dt + x * dw


def step_milstein(x, dw, dt):
    return x - x ** 3 * dt + x * dw + 0.5 * x * (dw ** 2 - dt)


# 同一路徑：先產生細網格增量
dW_fine = np.sqrt(dt_fine) * np.random.randn(M, N_fine)

# 參考解：細網格 Milstein
X_ref = np.full(M, X0)
for j in range(N_fine):
    X_ref = step_milstein(X_ref, dW_fine[:, j], dt_fine)

err_e, err_m = [], []
for dt in dts:
    Nc = int(round(T / dt))
    block = N_fine // Nc
    dW = dW_fine.reshape(M, Nc, block).sum(axis=2)  # 同路徑粗化
    Xe = np.full(M, X0)
    Xm = np.full(M, X0)
    for j in range(Nc):
        dw = dW[:, j]
        Xe = step_euler(Xe, dw, dt)
        Xm = step_milstein(Xm, dw, dt)
    err_e.append(float(np.mean(np.abs(Xe - X_ref))))
    err_m.append(float(np.mean(np.abs(Xm - X_ref))))

err_e = np.array(err_e)
err_m = np.array(err_m)
slope_e = float(np.polyfit(np.log(dts), np.log(err_e), 1)[0])
slope_m = float(np.polyfit(np.log(dts), np.log(err_m), 1)[0])

print(f"[milstein] seed={SEED} M={M} SDE dX=-X^3*dt+X*dW X0={X0} T={T} N_fine={N_fine}")
for dt, ee, em in zip(dts, err_e, err_m):
    print(f"[milstein] dt={dt:.4f} Euler_err={ee:.6f} Milstein_err={em:.6f}")
print(f"[milstein] slope Euler={slope_e:.3f} (expect ~0.5), Milstein={slope_m:.3f} (expect ~1.0)")
print(f"[milstein] elapsed {time.time()-t0:.2f}s")

assert 0.8 <= slope_m <= 1.2, f"Milstein slope {slope_m} not in [0.8,1.2]"
print(f"VERIFY: milstein slope={slope_m:.3f} in [0.8,1.2] PASS")
