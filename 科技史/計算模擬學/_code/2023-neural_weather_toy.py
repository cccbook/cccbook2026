# -*- coding: utf-8 -*-
"""2023 一維平流擴散「AI 天氣預報」玩具 (對應 wiki：計算模擬學 / AI 預報・GraphCast 等)。

背景：2023 年 GraphCast 等 AI 天氣模型以數據驅動超越傳統數值預報。
此處一維平流-擴散真值：u_t + c u_x = D u_xx + 隨機強迫（維持變異），
比較 (a) 持續性預報（明天=今天） vs (b) 線性迴歸「AI」（以 [u_{i-1},u_i,u_{i+1}] 預報下一時刻），
在測試段驗證 AI 的 RMSE 至少比持續性好 20%。

只用 numpy，固定種子。
"""
import numpy as np

np.random.seed(2023)

N = 32        # 格點數（週期邊界）
C = 0.4       # Courant 數 c*dt/dx
R = 0.04      # 擴散數 D*dt/dx^2
SIG = 0.05    # 隨機強迫強度
T = 2000      # 總步數
SPLIT = 1000  # 前半訓練、後半測試


def step(u):
    un = (u - C * (u - np.roll(u, 1)) + R * (np.roll(u, -1) - 2 * u + np.roll(u, 1)))
    un += SIG * np.random.randn(N)
    return un


def main():
    # 初值：正弦疊加
    x = np.arange(N)
    u = np.sin(2 * np.pi * x / N) + 0.5 * np.sin(4 * np.pi * x / N + 1.0)
    traj = np.zeros((T + 1, N))
    traj[0] = u
    for t in range(T):
        u = step(u)
        traj[t + 1] = u

    # 訓練：特徵 [u_{i-1}, u_i, u_{i+1}, 1] -> u_i(t+1)
    def build(seg):
        Xs, ys = [], []
        for t in range(seg.start, seg.stop):
            ut = traj[t]
            Xs.append(np.stack([np.roll(ut, 1), ut, np.roll(ut, -1),
                                np.ones(N)], axis=1))
            ys.append(traj[t + 1])
        return np.concatenate(Xs), np.concatenate(ys)

    Xtr, ytr = build(range(SPLIT))
    Xte, yte = build(range(SPLIT, T))
    w, *_ = np.linalg.lstsq(Xtr, ytr, rcond=None)

    # 測試段：持續性 vs AI
    persist_err2, ai_err2, cnt = 0.0, 0.0, 0
    for t in range(SPLIT, T):
        ut, unext = traj[t], traj[t + 1]
        persist_err2 += np.mean((unext - ut) ** 2)
        ai_pred = np.stack([np.roll(ut, 1), ut, np.roll(ut, -1),
                            np.ones(N)], axis=1) @ w
        ai_err2 += np.mean((unext - ai_pred) ** 2)
        cnt += 1
    rmse_p = float(np.sqrt(persist_err2 / cnt))
    rmse_ai = float(np.sqrt(ai_err2 / cnt))
    improve = (rmse_p - rmse_ai) / rmse_p

    print(f"真值: 1D 平流擴散 N={N}, C={C}, R={R}, 測試步數={cnt}")
    print(f"學得權重 ( stencil + bias ): {w}")
    print(f"持續性 RMSE = {rmse_p:.5f}")
    print(f"AI 線性迴歸 RMSE = {rmse_ai:.5f}")
    print(f"相對改進 = {improve * 100:.1f}% (要求 >= 20%)")
    assert improve >= 0.20, "AI 未顯著優於持續性"
    print(f"VERIFICATION: persist={rmse_p:.5f} ai={rmse_ai:.5f} improve={improve:.3f} PASS")


if __name__ == "__main__":
    main()
