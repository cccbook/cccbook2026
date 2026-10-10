# -*- coding: utf-8 -*-
"""1967 Verlet 積分器：諧振子能量穩定性
對應 wiki：Loup Verlet (1967) 經典分子動力學積分器；比較顯式 Euler vs 速度 Verlet。
諧振子 m=k=1, omega=1，跑 100 週期 (T=200*pi)，dt=0.02。
驗證：Verlet 相對能量漂移 < 1e-3（辛積分器能量有界），Euler 發散（能量暴增）。
只用 numpy，固定種子。
"""
import numpy as np

np.random.seed(0)

# 參數
omega = 1.0
T_total = 200.0 * np.pi  # 100 週期
dt = 0.02
nsteps = int(round(T_total / dt))
x0, v0 = 1.0, 0.0
E0 = 0.5 * (v0 ** 2 + omega ** 2 * x0 ** 2)


def run_euler(x0, v0, dt, nsteps):
    x, v = x0, v0
    for _ in range(nsteps):
        # 顯式 Euler：先用舊速度/加速度更新
        a = -omega ** 2 * x
        x = x + v * dt
        v = v + a * dt
    E = 0.5 * (v ** 2 + omega ** 2 * x ** 2)
    return x, v, E


def run_verlet(x0, v0, dt, nsteps):
    x, v = x0, v0
    for _ in range(nsteps):
        a = -omega ** 2 * x
        x = x + v * dt + 0.5 * a * dt * dt
        a_new = -omega ** 2 * x
        v = v + 0.5 * (a + a_new) * dt
    E = 0.5 * (v ** 2 + omega ** 2 * x ** 2)
    return x, v, E


xe, ve, Ee = run_euler(x0, v0, dt, nsteps)
xv, vv, Ev = run_verlet(x0, v0, dt, nsteps)

drift_euler = abs(Ee - E0) / E0
drift_verlet = abs(Ev - E0) / E0

print(f"steps={nsteps} dt={dt} T={T_total:.3f} (100 periods)")
print(f"E0={E0:.6f}")
print(f"Euler:  E_final={Ee:.6e} rel_drift={drift_euler:.6e}")
print(f"Verlet: E_final={Ev:.6e} rel_drift={drift_verlet:.6e}")

# 驗證數字
ok_verlet = drift_verlet < 1e-3
ok_euler = drift_euler > 1.0  # 發散：能量至少翻倍（實際大數百倍）
print(f"VERIFY verlet_drift={drift_verlet:.3e} (<1e-3? {ok_verlet})")
print(f"VERIFY euler_drift={drift_euler:.3e} (diverged>1? {ok_euler})")
assert ok_verlet, f"Verlet drift too large: {drift_verlet}"
assert ok_euler, f"Euler did not diverge: {drift_euler}"
print("PASS")
