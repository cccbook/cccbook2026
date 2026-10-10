# 08.2 一維隱空間規劃：窮舉 + CEM（交叉熵方法）
# 動力學 e_{t+1} = e_t + a_t，代價 c(e, a) = 0.1 + e^2，規劃兩步
# 只用 numpy

import numpy as np

# 窮舉四條軌跡（從 e0 = 2）
def total_cost(e0, actions, T=2):
    e = e0
    c = 0.0
    for t in range(T):
        a = actions[t]
        c += 0.1 + e**2  # 當前狀態代價 + 步進代價
        e = e + a
    c += 0.1 + e**2  # 末端狀態代價
    return c

e0 = 2.0
print("窮舉（e0 = 2，規劃兩步）：")
best = None
for a0 in (-1, 1):
    for a1 in (-1, 1):
        c = total_cost(e0, (a0, a1))
        print(f"  ({a0:+d}, {a1:+d}) 總代價 = {c:.2f}")
        if best is None or c < best[1]:
            best = ((a0, a1), c)
print(f"最優行動 a0* = {best[0][0]:+d}（總代價 {best[1]:.2f}）")

# CEM：連續動作版，a ~ N(mu, sigma)，迭代收斂
rng = np.random.default_rng(0)
mu, sigma, n_samples, elite_frac, n_iter = 0.0, 2.0, 100, 0.1, 10
print(f"\nCEM（初始 mu={mu}, sigma={sigma}，每輪抽 {n_samples} 條）：")
for it in range(n_iter):
    actions = rng.normal(mu, sigma, size=(n_samples, 2))
    costs = np.array([total_cost(e0, a) for a in actions])
    n_elite = max(1, int(n_samples * elite_frac))
    elite = actions[np.argsort(costs)[:n_elite]]
    mu, sigma = elite.mean(axis=0), elite.std(axis=0) + 1e-6
    if it % 2 == 0 or it == n_iter - 1:
        print(f"  迭代 {it}: 最優代價 = {costs.min():.4f}  mu = {np.round(mu, 3)}")

print(f"\nCEM 收斂到 a ≈ {np.round(mu, 3)}（連續動作版最優：a0 ≈ -2、a1 ≈ 0，一步跳到目標附近）——分布收斂到高獎區。")
