# 07.2 REINFORCE 單狀態兩動作策略上升
# 驗證：策略梯度上升使 pi(a1) -> 1，且 baseline 不改變期望但降低方差
# 只用 numpy

import numpy as np

rng = np.random.default_rng(0)

def sigmoid(x):
    return 1.0 / (1.0 + np.exp(-x))

# 單狀態，動作 a1=1（獎勵 +1）、a2=0（獎勵 -1），pi(a1) = sigmoid(theta)
# log pi 的梯度：選 a1 時 1-sigmoid(theta)；選 a2 時 -sigmoid(theta)
def reinforce(theta0=0.0, eta=1.0, n_steps=200, batch=50, use_baseline=False):
    theta = theta0
    for _ in range(n_steps):
        grads, rewards = [], []
        for _ in range(batch):
            a = 1 if rng.random() < sigmoid(theta) else 0
            g = (1 - sigmoid(theta)) if a == 1 else (-sigmoid(theta))
            grads.append(g)
            rewards.append(1.0 if a == 1 else -1.0)
        if use_baseline:
            # 方差最佳 baseline：b* = E[g^2 r] / E[g^2]（batch 估計）
            g2 = np.array(grads) ** 2
            b = np.mean(g2 * np.array(rewards)) / np.mean(g2)
        else:
            b = 0.0
        theta += eta * np.mean([g * (r - b) for g, r in zip(grads, rewards)])
    return theta, sigmoid(theta)

# 理論：梯度 = E[grad log pi * r]，其期望等於 dJ/dtheta = 2*s*(1-s)（見上）。
theta, pi1 = reinforce(use_baseline=False)
print("REINFORCE（無 baseline）：theta =", round(theta, 3), " pi(a1) =", round(pi1, 4))

theta_b, pi1_b = reinforce(use_baseline=True)
print("REINFORCE（有 baseline）：theta =", round(theta_b, 3), " pi(a1) =", round(pi1_b, 4))

# 理論：J(theta) = 2*sigmoid(theta) - 1，dJ/dtheta = 2*s*(1-s)（sigmoid 導數）。
# theta 收斂到 +inf（pi -> 1）——策略單調走向總選好動作。
for t in [0.0, 1.0, 2.0]:
    numerical = (2 * sigmoid(t + 1e-6) - 1 - (2 * sigmoid(t - 1e-6) - 1)) / 2e-6
    theory = 2 * sigmoid(t) * (1 - sigmoid(t))
    print(f"theta={t}: 數值 dJ/dtheta = {numerical:.4f}  理論 2*s*(1-s) = {theory:.4f}")

# baseline 方差比較：估計梯度 g*(r-b) 的樣本方差
def grad_variance(theta=1.0, n=20000, use_baseline=False):
    s = sigmoid(theta)
    samples, b_star = [], None
    if use_baseline:
        # 理論最佳 baseline：b* = E[g^2 r]/E[g^2] = 1 - 2s（單狀態例）
        b_star = 1 - 2 * s
    for _ in range(n):
        a = 1 if rng.random() < s else 0
        g = (1 - s) if a == 1 else (-s)
        r = 1.0 if a == 1 else -1.0
        b = b_star if use_baseline else 0.0
        samples.append(g * (r - b))
    return np.var(samples)

print("\n梯度估計方差（theta=1）：")
v0 = grad_variance(use_baseline=False)
v1 = grad_variance(use_baseline=True)
print("  無 baseline：", round(v0, 4))
print("  有最佳 baseline b* = 1-2σ(θ) ≈", round(1 - 2 * sigmoid(1.0), 4), "：", round(v1, 6), "（方差大幅降低）")
