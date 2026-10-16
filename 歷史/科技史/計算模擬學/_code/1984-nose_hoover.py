# -*- coding: utf-8 -*-
"""1984 Nosé-Hoover 恆溫器：一維諧振子
對應 wiki：Nosé (1984) / Hoover 確定性恆溫器；單恆溫器鏈 (M=1) 採樣正則系綜。
m=k=kB=1，目標 T=1.0，Q=1.0，dt=0.005 跑 2e5 步（Trotter 分裂積分）。
驗證：後半段時間平均動能 <p^2/2> ≈ T/2=0.5（誤差<0.1）。只用 numpy，固定種子。
"""
import numpy as np

np.random.seed(0)

T0 = 1.0
Q = 1.0
dt = 0.005
NSTEP = 200000

x = 0.0
v = 1.0  # 初動能即 0.5，落在目標等分配上
zeta = 0.0

ke_sum = 0.0
ke2_sum = 0.0
count = 0
half = NSTEP // 2
for i in range(NSTEP):
    # --- Trotter 分裂：zeta 半步 ---
    zeta += 0.5 * dt * (v * v - T0) / Q
    # --- 恆溫器半步（精確摩擦因子） ---
    s = np.exp(-0.5 * dt * zeta)
    v *= s
    # --- 諧振子 velocity-Verlet 半步 ---
    v += -0.5 * dt * x
    x += dt * v
    v += -0.5 * dt * x
    # --- 恆溫器半步 ---
    v *= s
    # --- zeta 半步 ---
    zeta += 0.5 * dt * (v * v - T0) / Q
    if i >= half:
        ke = 0.5 * v * v
        ke_sum += ke
        ke2_sum += ke * ke
        count += 1

avg_ke = ke_sum / count
target = T0 / 2.0
err = abs(avg_ke - target)
print(f"T0={T0} Q={Q} dt={dt} nstep={NSTEP}")
print(f"avg_KE(second half)={avg_ke:.5f} target={target:.5f} err={err:.5f}")
print(f"VERIFY |avgKE-0.5|={err:.5f} (<0.1? {err < 0.1})")
assert err < 0.1, f"Nosé-Hoover avg KE off: {avg_ke}"
print("PASS")
