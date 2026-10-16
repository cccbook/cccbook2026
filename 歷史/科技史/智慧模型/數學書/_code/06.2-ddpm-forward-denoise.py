# -*- coding: utf-8 -*-
# 06.2 擴散模型：1D DDPM 前向加噪 + 封閉式驗證 + 簡單去噪軌跡
import numpy as np

# 一維資料 x0 = 2，常數噪聲計畫 beta = 0.1
x0 = 2.0
beta = 0.1
T = 10
rng = np.random.default_rng(0)

# --- 1. 逐步前向（離散版）：x_t = sqrt(1-beta) x_{t-1} + sqrt(beta) eps ---
x = x0
mean_traj = []
x_noisy_traj = []
for t in range(1, T + 1):
    eps = rng.normal()
    x = np.sqrt(1 - beta) * x + np.sqrt(beta) * eps
    x_noisy_traj.append(x)
    mean_traj.append(np.sqrt(1 - beta) ** t * x0)  # 理論均值

# 封閉式：alpha_t = (1-beta)^t，E[x_t] = sqrt(alpha_t) x0，Var = 1 - alpha_t
print("逐步前向（含隨機噪聲）與理論均值對照：")
print(f"{'t':>3} {'隨機軌跡 x_t':>12} {'理論均值':>12}")
for t, (xt, mu) in enumerate(zip(x_noisy_traj, mean_traj), start=1):
    print(f"{t:>3} {xt:>12.4f} {mu:>12.4f}")

# --- 2. 蒙地卡羅驗證封閉式：x_t ~ N(sqrt(alpha_t) x0, 1 - alpha_t) ---
t = T
alpha_t = (1 - beta) ** t
n = 200000
samples = np.sqrt(alpha_t) * x0 + np.sqrt(1 - alpha_t) * rng.normal(size=n)
print(f"\nt={T} 封閉式驗證（蒙地卡羅 {n} 次）：")
print(f"  實測均值 = {samples.mean():.4f}，理論 sqrt(alpha_t)*x0 = {np.sqrt(alpha_t)*x0:.4f}")
print(f"  實測方差 = {samples.var():.4f}，理論 1-alpha_t = {1-alpha_t:.4f}")
print("  t 越大，均值越接近 0、方差越接近 1——趨於標準高斯 N(0,1)")

# --- 3. 簡單去噪：已知 x_t 與 x0，反推噪聲 eps = (x_t - sqrt(alpha_t) x0)/sqrt(1-alpha_t) ---
xt = x_noisy_traj[-1]
eps_hat = (xt - np.sqrt(alpha_t) * x0) / np.sqrt(1 - alpha_t)
print(f"\n去噪目標驗證：由 x_t={xt:.4f} 反推噪聲，eps = {eps_hat:.4f}")
print(f"  分數函數 -eps/sqrt(1-alpha_t) = {-eps_hat/np.sqrt(1-alpha_t):.4f}")
