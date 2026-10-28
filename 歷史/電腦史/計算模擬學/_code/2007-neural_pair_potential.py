# -*- coding: utf-8 -*-
"""2007 以 numpy 手刻小 MLP 擬合 1D Morse 勢 (對應 wiki：計算模擬學 / 機器學習勢・Behler-Parrinello)。

背景：Behler & Parrinello (2007) 用神經網路擬合勢能面。
此處玩具版：Morse 勢 V(x)=D(1-exp(-a(x-re)))^2，MLP 結構 1-16-16-1 (tanh)，
全手刻反向傳播 + Adam 訓練 2000 步。驗證測試 RMSE<0.02、力 RMSE<0.1。

只用 numpy，固定種子。
"""
import numpy as np

np.random.seed(2007)

# Morse 參數
D, A, RE = 1.0, 1.5, 1.0
NTR, NTE = 200, 100
H1 = H2 = 16
STEPS = 2000
LR = 0.01


def morse(x):
    return D * (1.0 - np.exp(-A * (x - RE))) ** 2


def morse_force(x):
    e = np.exp(-A * (x - RE))
    return -2 * D * A * (1 - e) * e  # F = -dV/dx


def init(n_in, n_out):
    return np.random.randn(n_in, n_out) * np.sqrt(1.0 / n_in)


def forward(xn, P):
    W1, b1, W2, b2, W3, b3 = P
    z1 = xn @ W1 + b1
    a1 = np.tanh(z1)
    z2 = a1 @ W2 + b2
    a2 = np.tanh(z2)
    out = a2 @ W3 + b3
    return out, (xn, z1, a1, z2, a2)


def main():
    xtr = np.random.uniform(0.4, 3.0, NTR)
    xte = np.random.uniform(0.4, 3.0, NTE)
    ytr = morse(xtr)
    yte = morse(xte)

    # 標準化（用訓練集統計）
    xm, xs = xtr.mean(), xtr.std()
    ym, ys = ytr.mean(), ytr.std()
    XTR = ((xtr - xm) / xs).reshape(-1, 1)
    YTR = ((ytr - ym) / ys).reshape(-1, 1)
    XTE = ((xte - xm) / xs).reshape(-1, 1)

    W1, b1 = init(1, H1), np.zeros(H1)
    W2, b2 = init(H1, H2), np.zeros(H2)
    W3, b3 = init(H2, 1), np.zeros(1)
    P = [W1, b1, W2, b2, W3, b3]
    # Adam 狀態
    m = [np.zeros_like(p) for p in P]
    v = [np.zeros_like(p) for p in P]
    b1a, b2a, eps = 0.9, 0.999, 1e-8

    N = NTR
    for t in range(1, STEPS + 1):
        out, (xn, z1, a1, z2, a2) = forward(XTR, P)
        err = (out - YTR) / N  # d(MSE)/d out（含 1/N；MSE=mean(err^2) 的梯度為 2*.../N，此處合併常數由 lr 吸收）
        # 反傳
        dW3 = a2.T @ (2 * err)
        db3 = (2 * err).sum(axis=0)
        da2 = (2 * err) @ W3.T
        dz2 = da2 * (1 - a2 ** 2)
        dW2 = a1.T @ dz2
        db2 = dz2.sum(axis=0)
        da1 = dz2 @ W2.T
        dz1 = da1 * (1 - a1 ** 2)
        dW1 = xn.T @ dz1
        db1 = dz1.sum(axis=0)
        grads = [dW1, db1, dW2, db2, dW3, db3]
        for i in range(len(P)):
            m[i] = b1a * m[i] + (1 - b1a) * grads[i]
            v[i] = b2a * v[i] + (1 - b2a) * grads[i] ** 2
            mh = m[i] / (1 - b1a ** t)
            vh = v[i] / (1 - b2a ** t)
            P[i] -= LR * mh / (np.sqrt(vh) + eps)

    W1, b1, W2, b2, W3, b3 = P

    def predict(x):
        xn = ((x - xm) / xs).reshape(-1, 1)
        out, _ = forward(xn, P)
        return (out.ravel() * ys + ym)

    pred_te = predict(xte)
    rmse = float(np.sqrt(np.mean((pred_te - yte) ** 2)))
    # 力：MLP 數值微分 vs 解析力
    h = 1e-4
    f_pred = -(predict(xte + h) - predict(xte - h)) / (2 * h)
    f_true = morse_force(xte)
    frmse = float(np.sqrt(np.mean((f_pred - f_true) ** 2)))

    print(f"MLP 1-16-16-1 tanh, Adam {STEPS} 步, lr={LR}")
    print(f"測試能量 RMSE = {rmse:.5f} (要求 < 0.02)")
    print(f"測試力 RMSE   = {frmse:.5f} (要求 < 0.1)")
    ok = (rmse < 0.02) and (frmse < 0.1)
    assert ok, "精度未達標"
    print(f"VERIFICATION: rmse={rmse:.5f} force_rmse={frmse:.5f} PASS")


if __name__ == "__main__":
    main()
