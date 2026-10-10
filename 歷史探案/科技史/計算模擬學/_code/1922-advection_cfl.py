# -*- coding: utf-8 -*-
"""1922 線性平流與 CFL 條件（對應 wiki：計算模擬學 / Courant 平流穩定性）
一維線性平流 u_t + c·u_x = 0, c=1，週期域 [0,1)，初值高斯包
u(x,0)=exp(-((x-0.3)/0.05)²)。真解為整體平移 u(x,t)=u0(x-c·t mod 1)。
迎風法 CFL=c·dt/dx=0.5（≤1 穩定）；FTCS 中心差放大因子
|G|=sqrt(1+C²sin²(k·dx))>1 恆不穩定。跑 T=2.0（包繞兩圈回到原位），
印 L2 誤差，驗證迎風穩定、FTCS 爆掉。
只用 numpy，固定種子。
"""
import numpy as np

np.random.seed(0)

N = 200
L = 1.0
dx = L / N
c = 1.0
CFL = 0.5
dt = CFL * dx / c
T = 2.0
steps = int(round(T / dt))
dt = T / steps
CFL = c * dt / dx
x = np.arange(N) * dx
sigma, x0 = 0.05, 0.3


def u0(xv):
    return np.exp(-(((xv - x0) / sigma) ** 2))


def exact(xv, t):
    return u0((xv - c * t) % L)


u_init = u0(x)
uex = exact(x, T)

# 迎風法（upwind, CFL<=1 穩定）
u_up = u_init.copy()
with np.errstate(over="ignore", invalid="ignore"):
    for _ in range(steps):
        u_up = u_up - CFL * (u_up - np.roll(u_up, 1))
l2_up = float(np.sqrt(np.mean((u_up - uex) ** 2)))

# FTCS 中心差（無條件不穩定）
u_ct = u_init.copy()
with np.errstate(over="ignore", invalid="ignore"):
    for _ in range(steps):
        u_ct = u_ct - CFL / 2.0 * (np.roll(u_ct, -1) - np.roll(u_ct, 1))
with np.errstate(invalid="ignore"):
    if np.all(np.isfinite(u_ct)):
        l2_ct = float(np.sqrt(np.mean((u_ct - uex) ** 2)))
        cmax = float(np.max(np.abs(u_ct)))
    else:
        l2_ct = float("inf")
        cmax = float("inf")

gmax = float(np.sqrt(1.0 + CFL ** 2))  # |G| 最大值 (sin=±1)
print(f"N={N} dx={dx:.5f} dt={dt:.2e} CFL={CFL:.3f} steps={steps} T={T}")
print(f"理論: 迎風 CFL≤1 穩定；FTCS |G|max={gmax:.4f}>1 恆不穩定")
print(f"upwind L2 err = {l2_up:.6e}")
print(f"FTCS   L2 err = {l2_ct:.6e} (max|u|={cmax:.3e}, 初值 max=1)")

# 驗證數字：理論值 vs 實測
ok_up = np.isfinite(l2_up) and (l2_up < 0.3)
ok_ct = (not np.isfinite(l2_ct)) or (l2_ct > 1.0) or (l2_ct > 10.0 * l2_up)
print(f"VERIFY upwind_L2={l2_up:.3e} (<0.3 穩定? {ok_up})")
print(f"VERIFY ftcs_L2={l2_ct:.3e} (爆掉>1 或 >10×迎風? {ok_ct})")
assert ok_up, f"迎風法誤差異常: {l2_up}"
assert ok_ct, f"FTCS 未觀察到不穩定: {l2_ct} vs upwind {l2_up}"
print("PASS")
