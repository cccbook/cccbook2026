# 1960 - ADALINE 自適應線性元件 (Widrow-Hoff, LMS / delta rule)
# 對應本書: 1960-ADALINE自適應線性元件.md
# 公式: y = w·x (線性), Δw = η (t - w·x) x ; 收斂條件 0 < η < 2/λmax
import numpy as np
import torch


def main():
    # 書中範例: 目標 ≈ 2x
    X = np.array([[1, 1], [1, 2], [1, 3]], float)  # 含 bias 常數項
    t = np.array([2.1, 3.9, 6.2])
    R = X.T @ X
    lmax = np.linalg.eigvalsh(R).max()
    print(f"自相關矩陣最大特徵值 λmax={lmax:.2f}, 收斂要求 η < {2 / lmax:.3f}")

    w = np.zeros(2)
    eta = 0.1
    for _ in range(30):
        for xi, ti in zip(X, t):
            w += eta * (ti - w @ xi) * xi   # LMS: delta rule (隨機梯度下降始祖)
    E = np.sum((t - X @ w) ** 2) / 2
    print("numpy LMS 30輪後: w =", np.round(w, 2), "E =", round(float(E), 4))

    # torch 對照: 同一 LMS 更新用 tensor 做, 並與最小二乘閉式解比較
    Xt = torch.tensor(X, dtype=torch.float32)
    tt = torch.tensor(t, dtype=torch.float32)
    closed = torch.linalg.lstsq(Xt, tt).solution
    print("最小二乘閉式解:", torch.round(closed, decimals=2).tolist(),
          "(LMS 逼近此解 = 在二次碗上滑到碗底)")


if __name__ == "__main__":
    main()
