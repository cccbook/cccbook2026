# -*- coding: utf-8 -*-
"""1822 熱方程顯式 FTCS（對應 wiki：計算模擬學 / Fourier 熱傳與顯式差分）
一維熱方程 u_t = α u_xx, x∈[0,1], Dirichlet u=0 邊界，初值 sin(pi·x)，
真解 u=sin(pi·x)·exp(-pi²αt)。顯式 FTCS：r=α·dt/dx²，穩定條件 r≤0.5。
穩定例 r=0.4 驗證 t=0.1 誤差<1e-3；不穩定例 r=0.6 展示爆掉。
只用 numpy，固定種子。
"""
import numpy as np

np.random.seed(0)

alpha = 1.0
nx = 101
L = 1.0
dx = L / (nx - 1)
x = np.linspace(0.0, L, nx)
t_final = 0.1


def run_ftcs(r, t_final):
    dt = r * dx * dx / alpha
    steps = int(round(t_final / dt))
    dt = t_final / steps  # 微調使恰好到 t_final
    r_eff = alpha * dt / dx / dx
    u = np.sin(np.pi * x)
    u[0] = 0.0
    u[-1] = 0.0
    with np.errstate(over="ignore", invalid="ignore"):
        for _ in range(steps):
            u[1:-1] = u[1:-1] + r_eff * (u[2:] - 2.0 * u[1:-1] + u[:-2])
    return u, steps, dt, r_eff


def exact_sol(t):
    return np.sin(np.pi * x) * np.exp(-np.pi ** 2 * alpha * t)


# 穩定：r=0.4
u_st, steps_st, dt_st, r_st = run_ftcs(0.4, t_final)
uex = exact_sol(t_final)
err_st = float(np.max(np.abs(u_st - uex)))
print(f"stable r={r_st:.4f} dx={dx:.4f} dt={dt_st:.2e} steps={steps_st}")
print(f"  max|u_num-u_exact| = {err_st:.6e} (理論衰減 e^-pi²αt={np.exp(-np.pi**2*alpha*t_final):.6f})")

# 不穩定：r=0.6
u_un, steps_un, dt_un, r_un = run_ftcs(0.6, t_final)
with np.errstate(invalid="ignore"):
    blown = (not np.all(np.isfinite(u_un))) or (float(np.nanmax(np.abs(u_un))) > 1e3)
    umax = float(np.nanmax(np.abs(u_un))) if np.any(np.isfinite(u_un)) else float("inf")
print(f"unstable r={r_un:.4f} dx={dx:.4f} dt={dt_un:.2e} steps={steps_un}")
print(f"  max|u| = {umax:.6e} (初值 max=1, 穩定應衰減至~0.37；遠大於此即爆掉)")

# 驗證數字：理論值 vs 實測
ok_stable = err_st < 1e-3
print(f"VERIFY stable_err={err_st:.3e} (<1e-3? {ok_stable})")
print(f"VERIFY unstable_max={umax:.3e} (blowup>1e3或inf/nan? {blown})")
assert ok_stable, f"穩定 FTCS 誤差太大: {err_st}"
assert blown, f"r=0.6 未觀察到不穩定爆掉: max={umax}"
print("PASS")
