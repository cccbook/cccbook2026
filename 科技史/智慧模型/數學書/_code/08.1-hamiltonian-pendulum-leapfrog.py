# 08.1 單擺哈密頓方程：leapfrog vs Euler 積分能量漂移比較
# H = p^2/(2 m l^2) + m g l (1 - cos q)，取 m=l=1, g=1
# 只用 numpy

import numpy as np

def H(q, p):
    return p**2 / 2 + (1 - np.cos(q))

def dHdq(q):
    return np.sin(q)  # d/dq [1-cos q] = sin q

def dHdp(p):
    return p

def euler(q0, p0, dt, n):
    q, p = q0, p0
    energies = [H(q, p)]
    for _ in range(n):
        q_new = q + dt * dHdp(p)
        p = p - dt * dHdq(q)
        q = q_new
        energies.append(H(q, p))
    return q, p, np.array(energies)

def leapfrog(q0, p0, dt, n):
    q, p = q0, p0
    energies = [H(q, p)]
    for _ in range(n):
        p_half = p - dt / 2 * dHdq(q)
        q = q + dt * dHdp(p_half)
        p = p_half - dt / 2 * dHdq(q)
        energies.append(H(q, p))
    return q, p, np.array(energies)

q0, p0, dt, n = 1.0, 0.0, 0.1, 1000
E0 = H(q0, p0)
print(f"初始能量 E0 = {E0:.6f}，dt = {dt}，積分 {n} 步\n")

_, _, E_euler = euler(q0, p0, dt, n)
_, _, E_leap = leapfrog(q0, p0, dt, n)

print(f"Euler    最終能量 = {E_euler[-1]:.6f}  能量漂移 = {E_euler[-1]-E0:+.6f}")
print(f"Leapfrog 最終能量 = {E_leap[-1]:.6f}  能量漂移 = {E_leap[-1]-E0:+.6f}")
print(f"\nEuler    能量範圍：[{E_euler.min():.4f}, {E_euler.max():.4f}]（單調漂移、越盪越高）")
print(f"Leapfrog 能量範圍：[{E_leap.min():.4f}, {E_leap.max():.4f}]（有界振盪、不散逸）")

# 驗證斜對稱：a^T J a = 0（習題 1）
rng = np.random.default_rng(0)
J = np.array([[0, 1], [-1, 0]])
a = rng.normal(size=2)
print(f"\n驗證 a^T J a：a = {np.round(a, 3)}，a^T J a = {a @ J @ a:.2e}（≈ 0，斜對稱）")
