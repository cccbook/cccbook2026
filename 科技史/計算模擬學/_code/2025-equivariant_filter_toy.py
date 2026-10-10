# -*- coding: utf-8 -*-
"""2025 3D 點雲等變濾波演示 (對應 wiki：計算模擬學 / 等變神經網路・NequIP/MACE)。

核心思想：MACE / NequIP 的等變訊息 = 徑向函數 R(|x|) × 球諧 Y_l^m(x̂)，
l=1 時 Y ∝ x/r（向量），旋轉下按向量變換。線性濾波
F({x}) = Σ_j φ(r_j) x_j h_j（φ 為徑向函數，h_j 為不變標量特徵）
滿足 F(Rx) = R F(x)。本玩具以隨機旋轉 R 驗證等變性誤差 < 1e-10。

只用 numpy，固定種子。
"""
import numpy as np

np.random.seed(2025)

NPTS = 8


def radial(r):
    return np.exp(-0.5 * (r / 0.5) ** 2)  # 高斯徑向函數


def cloud_filter(X, h):
    """X: (N,3), h: (N,) -> (3,) 向量輸出。"""
    r = np.linalg.norm(X, axis=1, keepdims=True)  # (N,1)
    return (radial(r) * X * h[:, None]).sum(axis=0)


def random_rotation():
    A = np.random.randn(3, 3)
    Q, R = np.linalg.qr(A)
    if np.linalg.det(Q) < 0:
        Q[:, 0] = -Q[:, 0]
    return Q


def main():
    X = np.random.uniform(-1, 1, size=(NPTS, 3))
    h = np.random.randn(NPTS)
    R = random_rotation()
    Xr = X @ R.T  # 旋轉點雲

    F = cloud_filter(X, h)
    Fr = cloud_filter(Xr, h)
    expect = R @ F
    err = float(np.linalg.norm(Fr - expect))

    print(f"點數={NPTS}, 濾波 F=Σ φ(r) x h（徑向×l=1 球諧向量）")
    print(f"F(x)   = {F}")
    print(f"F(Rx)  = {Fr}")
    print(f"R F(x) = {expect}")
    print(f"等變誤差 ||F(Rx)-R F(x)|| = {err:.3e} (要求 < 1e-10)")
    assert err < 1e-10, "等變性失敗"
    print(f"VERIFICATION: equiv_err={err:.3e} PASS")
    print("說明: MACE/NequIP 即以此類 R(r)×Y_l^m 為基底堆疊高階張量積，保證旋轉等變。")


if __name__ == "__main__":
    main()
