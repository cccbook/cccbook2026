# -*- coding: utf-8 -*-
"""1957 二維硬碟氣體 (對應 wiki: 計算模擬學 / Alder-Wainwright 硬球分子動力學)
只用 numpy,固定種子。事件驅動簡化版:小步 MD + 彈性碰撞,N=64。
驗證:直接兩球碰撞函數的總動量/動能相對誤差 < 1e-9 (動能守恆)。
"""
import numpy as np

np.random.seed(0)
N = 64
Lbox = 10.0
R = 0.2
dt = 0.01
STEPS = 2000

def collide_pair(v1, v2, x1, x2):
    """等質量彈性碰撞,沿連心線交換法向分量。回傳 (v1', v2')。"""
    n = x1 - x2
    d = float(np.linalg.norm(n))
    if d == 0.0:
        return v1.copy(), v2.copy()
    n = n / d
    p = float(np.dot(v1 - v2, n))
    if p >= 0:
        return v1.copy(), v2.copy()  # 正在分離,不碰撞
    return v1 - p * n, v2 + p * n

# --- 直接兩球碰撞驗證 (動量/動能守恆) ---
v1 = np.array([1.0, 0.3])
v2 = np.array([-0.7, -0.2])
x1 = np.array([-0.5, 0.0])
x2 = np.array([0.5, 0.1])
P0 = v1 + v2
K0 = 0.5 * (np.dot(v1, v1) + np.dot(v2, v2))
w1, w2 = collide_pair(v1, v2, x1, x2)
P1 = w1 + w2
K1 = 0.5 * (np.dot(w1, w1) + np.dot(w2, w2))
errP = float(np.linalg.norm(P1 - P0) / max(1e-300, np.linalg.norm(P0)))
errK = abs(K1 - K0) / max(1e-300, abs(K0))

# 第二組:隨機斜碰撞
np.random.seed(1)
ok2 = True
errP2 = errK2 = 0.0
for _ in range(5):
    a = np.random.rand(2) * 2 - 1
    b = np.random.rand(2) * 2 - 1
    xa = np.random.rand(2)
    xb = xa + (np.random.rand(2) - 0.5)
    c1, c2 = collide_pair(a, b, xa, xb)
    eP = float(np.linalg.norm((c1 + c2) - (a + b)) / max(1e-300, np.linalg.norm(a + b)))
    KA = 0.5 * (np.dot(a, a) + np.dot(b, b))
    KB = 0.5 * (np.dot(c1, c1) + np.dot(c2, c2))
    eK = abs(KB - KA) / max(1e-300, abs(KA))
    errP2 = max(errP2, eP); errK2 = max(errK2, eK)
np.random.seed(0)

# --- N=64 小步 MD 演示 (牆面彈性反射 + 重疊對彈性碰撞) ---
pos = np.random.rand(N, 2) * (Lbox - 2 * R) + R
vel = (np.random.rand(N, 2) - 0.5) * 2.0
K_init = 0.5 * float(np.sum(vel * vel))
for _ in range(STEPS):
    pos = pos + vel * dt
    # 牆面反射
    for d in range(2):
        lo = pos[:, d] < R
        hi = pos[:, d] > Lbox - R
        vel[lo, d] = np.abs(vel[lo, d])
        vel[hi, d] = -np.abs(vel[hi, d])
        pos[:, d] = np.clip(pos[:, d], R, Lbox - R)
    # 對碰撞 (O(N^2),N=64 可接受)
    for i in range(N):
        for j in range(i + 1, N):
            dx = pos[i] - pos[j]
            if float(np.dot(dx, dx)) < (2 * R) ** 2:
                vi, vj = collide_pair(vel[i], vel[j], pos[i], pos[j])
                vel[i], vel[j] = vi, vj
                # 位置分開避免黏連
                dist = float(np.linalg.norm(dx)) + 1e-12
                overlap = 2 * R - dist
                nrm = dx / dist
                pos[i] += 0.5 * overlap * nrm
                pos[j] -= 0.5 * overlap * nrm
K_final = 0.5 * float(np.sum(vel * vel))
drift = abs(K_final - K_init) / abs(K_init)

ok = (errK < 1e-9) and (errP < 1e-9) and (errK2 < 1e-9) and (errP2 < 1e-9)
print(f"兩球碰撞: dP/P={errP:.3e}, dK/K={errK:.3e} (驗證 <1e-9: {'PASS' if (errK<1e-9 and errP<1e-9) else 'FAIL'})")
print(f"隨機5組最大: dP/P={errP2:.3e}, dK/K={errK2:.3e}")
print(f"N=64 MD {STEPS}步: K_init={K_init:.4f}, K_final={K_final:.4f}, drift={drift:.3e}")
print(f"VERIFY: errP={errP:.6e}, errK={errK:.6e}, drift={drift:.6e}")
assert ok, "碰撞不守恆"
print("ALL CHECKS PASS")
