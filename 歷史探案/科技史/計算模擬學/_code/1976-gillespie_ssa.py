# -*- coding: utf-8 -*-
"""1976 Gillespie SSA：出生-死亡過程
對應 wiki：Gillespie (1976) Stochastic Simulation Algorithm，Doob-Gillespie。
模型：X -> X+1 速率 lambda=2（恆定出生），X -> X-1 速率 mu*X, mu=1。
定常分佈 Poisson(lambda/mu)，均值=2。SSA 跑 20000 反應，時間加權均值驗證誤差<0.15。
只用 numpy，固定種子。
"""
import numpy as np

np.random.seed(0)

lam = 2.0
mu = 1.0
N_REACT = 20000
BURN = 1000  # 捨去前 1000 反應


def run_ssa():
    x = 0  # 初值
    t = 0.0
    xs = np.empty(N_REACT, dtype=float)
    taus = np.empty(N_REACT, dtype=float)
    for i in range(N_REACT):
        a1 = lam
        a2 = mu * x
        a0 = a1 + a2
        u1 = np.random.rand()
        u2 = np.random.rand()
        tau = -np.log(u1) / a0
        taus[i] = tau
        xs[i] = x
        t += tau
        if u2 < a1 / a0:
            x += 1
        else:
            x = max(0, x - 1)
    return xs, taus


xs, taus = run_ssa()
# 時間加權均值（捨 burn-in）
w = taus[BURN:]
v = xs[BURN:]
mean_tw = float(np.sum(v * w) / np.sum(w))
mean_plain = float(np.mean(v))
target = lam / mu
err = abs(mean_tw - target)
print(f"reactions={N_REACT} burn={BURN}")
print(f"time_weighted_mean={mean_tw:.5f} plain_mean={mean_plain:.5f} target={target}")
print(f"final_X={xs[-1]:.0f} total_time={np.sum(taus):.2f}")
print(f"VERIFY mean={mean_tw:.5f} target=2.0 err={err:.5f} (<0.15? {err < 0.15})")
assert err < 0.15, f"mean error too large: {err}"
print("PASS")
