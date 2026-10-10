# -*- coding: utf-8 -*-
"""1964 二維 Lennard-Jones 分子動力學 (對應 wiki: 計算模擬學 / 平衡態 MD)
只用 numpy,固定種子。N=64,Verlet(NVE)跑 2000 步。
驗證:總能量漂移 < 2% 且徑向分佈第一峰約在 r≈1.1σ。
"""
import numpy as np

np.random.seed(0)
N = 64
Lbox = 8.0
dt = 0.005
STEPS = 2000
RC = 2.5
# shift 使截斷處能量連續
UCUT = 4.0 * ((1.0 / RC) ** 12 - (1.0 / RC) ** 6)

def forces_and_pe(pos):
    d = pos[:, None, :] - pos[None, :, :]       # (N,N,2)
    d -= Lbox * np.round(d / Lbox)              # 最小鏡像
    r2 = np.sum(d * d, axis=-1)
    np.fill_diagonal(r2, np.inf)
    mask = r2 < RC * RC
    inv2 = np.zeros_like(r2)
    inv2[mask] = 1.0 / r2[mask]
    inv6 = inv2 ** 3
    inv12 = inv6 ** 2
    pe = float(np.sum(4.0 * (inv12 - inv6) - UCUT * mask)) / 2.0
    fmag = np.zeros_like(r2)
    fmag[mask] = 24.0 * (2.0 * inv12[mask] - inv6[mask]) * inv2[mask]
    F = np.sum(fmag[:, :, None] * d, axis=1)
    return F, pe

# 方格初位 (8x8,間距 1.0),隨機初速去質心並定標至 T≈1
n_side = 8
grid = np.array([[i % n_side, i // n_side] for i in range(N)], dtype=float)
pos = (grid + 0.5) * (Lbox / n_side)
vel = np.random.rand(N, 2) - 0.5
vel -= vel.mean(axis=0)
ke0_target = N * 1.0  # 2D: T=KE/N,目標 T=1
scale = np.sqrt(ke0_target / (0.5 * float(np.sum(vel * vel))))
vel *= scale

acc, pe = forces_and_pe(pos)
ke = 0.5 * float(np.sum(vel * vel))
E0 = ke + pe
for _ in range(STEPS):
    pos = pos + vel * dt + 0.5 * acc * dt * dt
    pos = np.mod(pos, Lbox)
    acc_new, pe = forces_and_pe(pos)
    vel = vel + 0.5 * (acc + acc_new) * dt
    acc = acc_new
ke = 0.5 * float(np.sum(vel * vel))
E1 = ke + pe
drift = abs(E1 - E0) / abs(E0)

# 徑向分佈:末態對距離直方圖,找 [0.8,2.0] 內第一峰
d = pos[:, None, :] - pos[None, :, :]
d -= Lbox * np.round(d / Lbox)
dist = np.sqrt(np.sum(d * d, axis=-1))
iu = np.triu_indices(N, 1)
rr = dist[iu]
bins = np.linspace(0.0, 4.0, 81)
hist, edges = np.histogram(rr, bins=bins)
cent = 0.5 * (edges[:-1] + edges[1:])
lo = int(0.8 / 0.05); hi = int(2.0 / 0.05)
seg = hist[lo:hi]
peak_idx = lo + int(np.argmax(seg))
r_peak = float(cent[peak_idx])
ok_e = drift < 0.02
ok_r = 0.9 < r_peak < 1.4
print(f"E0={E0:.4f}, E1={E1:.4f}, drift={drift*100:.4f}% (驗證 <2%: {'PASS' if ok_e else 'FAIL'})")
print(f"RDF 第一峰 r={r_peak:.3f}σ (驗證約 1.1: {'PASS' if ok_r else 'FAIL'})")
print(f"VERIFY: drift={drift:.6f}, r_peak={r_peak:.6f}")
assert ok_e, "能量漂移過大"
assert ok_r, "RDF 第一峰偏離 1.1σ"
print("ALL CHECKS PASS")
