# -*- coding: utf-8 -*-
"""2002 一維雙阱 well-tempered metadynamics 玩具版 (對應 wiki：計算模擬學 / 增強採樣・metadynamics)。

背景：Laio & Parrinello (2002) metadynamics；Barducci 等 (2008) well-tempered 版。
真實勢 V(x)=(x^2-1)^2，兩阱在 x=±1（等深），勢壘在 x=0 高 1.0。
以過阻尼 Langevin + 週期性高斯偏置 Vb(s) 做玩具模擬，重建自由能
F(s) = -(gamma/(gamma-1)) * Vb(s)，驗證兩阱等高 (ΔF < 0.5 kT) 且發生多次躍遷。

只用 numpy，固定種子。偏置放在均勻網格上（向量化高斯沉積 + 線性內插力）。
"""
import numpy as np

np.random.seed(2002)

# ---- 物理與演算法參數 ----
KT = 0.25          # kT
GAMMA = 5.0        # bias factor (T+dT)/T
SIGMA = 0.15       # 高斯寬
W0 = 0.02          # 初始 hill 高
DT = 0.01
NSTEPS = 400000
DEPOSIT_EVERY = 200
XMIN, XMAX, NBIN = -2.0, 2.0, 400
DX = (XMAX - XMIN) / NBIN
GRID = np.linspace(XMIN + DX / 2, XMAX - DX / 2, NBIN)


def V(x):
    return (x * x - 1.0) ** 2


def dVdx(x):
    return 4.0 * x * (x * x - 1.0)


def bias_force(x, vb):
    idx = int((x - XMIN) / DX - 0.5)
    idx = max(1, min(NBIN - 2, idx))
    return (vb[idx + 1] - vb[idx - 1]) / (2 * DX)


def bias_at(x, vb):
    f = (x - XMIN) / DX - 0.5
    i0 = int(np.floor(f))
    i0 = max(0, min(NBIN - 2, i0))
    t = f - i0
    return (1 - t) * vb[i0] + t * vb[i0 + 1]


def main():
    vb = np.zeros(NBIN)
    # 向量化高斯模板（沉積時平移對齊）
    off = np.arange(NBIN) * DX  # 距離模板用相對座標計算
    x = -1.0
    state = -1
    transitions = 0
    sq = np.sqrt(2 * KT * DT)
    dT_factor = (GAMMA - 1.0) * KT

    for step in range(NSTEPS):
        fb = bias_force(x, vb)
        x = x - (dVdx(x) + fb) * DT + sq * np.random.randn()
        # 反射邊界
        if x < XMIN:
            x = 2 * XMIN - x
        elif x > XMAX:
            x = 2 * XMAX - x
        # 躍遷計數（遲滯：±0.5）
        if x < -0.5:
            s = -1
        elif x > 0.5:
            s = 1
        else:
            s = state
        if s != state:
            # 只計左右阱之間的切換（經由中間區不計，需真的到對側）
            transitions += 1
            state = s
        # 沉積高斯（well-tempered 高度衰減）
        if (step + 1) % DEPOSIT_EVERY == 0:
            h = W0 * np.exp(-bias_at(x, vb) / dT_factor)
            vb += h * np.exp(-0.5 * ((GRID - x) / SIGMA) ** 2)

    # 自由能重建：F = -(gamma/(gamma-1)) Vb；阱底取值為 ±1 附近區間平均以抑制單點雜訊
    scale = GAMMA / (GAMMA - 1.0)
    Fest = -scale * vb
    F_left = float(Fest[(GRID > -1.2) & (GRID < -0.8)].mean())
    F_right = float(Fest[(GRID > 0.8) & (GRID < 1.2)].mean())
    dF = abs(F_left - F_right)
    dF_kT = dF / KT

    print(f"步數={NSTEPS}, 沉積 hills={(NSTEPS // DEPOSIT_EVERY)}, 躍遷次數={transitions}")
    print(f"F(-1)={F_left:.4f}, F(+1)={F_right:.4f}, ΔF={dF:.4f} = {dF_kT:.3f} kT")
    ok_trans = transitions >= 10
    ok_f = dF_kT < 0.5
    print(f"驗證: transitions>=10? {ok_trans} ; ΔF<0.5kT? {ok_f}")
    assert ok_trans, "躍遷次數不足"
    assert ok_f, "自由能兩阱不等高"
    print(f"VERIFICATION: transitions={transitions} dF_kT={dF_kT:.4f} PASS")


if __name__ == "__main__":
    main()
