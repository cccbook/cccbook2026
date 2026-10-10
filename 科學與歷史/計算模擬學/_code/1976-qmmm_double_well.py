# -*- coding: utf-8 -*-
"""1976 QM/MM 玩具模型：一維雙阱 + Langevin 採樣
對應 wiki：Warshel & Levitt (1976) QM/MM 多尺度；玩具實現左阱諧波近似(MM)+右阱精確(QM)。
真勢 V(x)=(x^2-1)^2，極小在 ±1；模型勢：左阱盆地內 (|x+1|<0.5) 用
V_MM=4(x+1)^2（在 -1 處二階泰勒，MM 區），其餘（含能障與右阱）用
V_QM=(x^2-1)^2（QM 區）。MM 區取阱底盆地 |x+1|<0.25（泰勒準確範圍），
能障對稱高度 1.0，過阻尼 Langevin 採樣驗證兩阱佔比≈1:1（誤差<0.1）。
註：若左半軸全用諧波，左能障高達 4.0 會把粒子鎖死，故 MM 只用於阱底盆地、
能障區共用精確勢，這正是 QM/MM 分區精神（反應中心精確、環境近似）。
只用 numpy，固定種子。
"""
import numpy as np

np.random.seed(0)

kT = 0.5
dt = 0.01
NSTEP = 300000
BURN = 30000


def qm_force(xi):
    return -4.0 * xi * (xi ** 2 - 1.0)


def mm_force(xi):
    return -8.0 * (xi + 1.0)


def force(x):
    # MM 盆地 (|x+1|<0.25) / 其餘 QM，純 numpy 向量化
    f = np.empty_like(x)
    m = np.abs(x + 1.0) < 0.25
    m = m & (x < 0)
    f[m] = -8.0 * (x[m] + 1.0)
    xr = x[~m]
    f[~m] = -4.0 * xr * (xr ** 2 - 1.0)
    return f


# 預先產生雜訊（向量化加速，<10 秒）
noise = np.random.randn(NSTEP)
x = np.empty(NSTEP, dtype=float)
x[0] = -1.0
sdt = np.sqrt(2.0 * kT * dt)
for i in range(1, NSTEP):
    # 單步 Euler-Maruyama：左阱底用 MM 諧波力，其餘用 QM 精確力
    xi = x[i - 1]
    if xi < 0 and abs(xi + 1.0) < 0.25:
        f = -8.0 * (xi + 1.0)  # MM
    else:
        f = -4.0 * xi * (xi ** 2 - 1.0)  # QM
    x[i] = xi + f * dt + sdt * noise[i]

xs = x[BURN:]
fL = float(np.mean(xs < 0))
fR = float(np.mean(xs >= 0))
err = abs(fL - 0.5)
print(f"kT={kT} dt={dt} nstep={NSTEP} burn={BURN}")
print(f"frac_left={fL:.4f} frac_right={fR:.4f}")
print(f"VERIFY |frac_left-0.5|={err:.4f} (<0.1? {err < 0.1})")
assert err < 0.1, f"well occupation biased: {fL} vs 0.5"
print("PASS")
