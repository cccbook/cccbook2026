"""OU 參數極大似然估計（精確離散，最小平方即 MLE）。
對應 wiki：Vasicek / OU 過程 dX = θ(μ-X)dt + σdW；
  精確離散 X_{k+1} = μ + φ(X_k-μ) + √q ε，
  φ = exp(-θdt), q = σ²(1-exp(-2θdt))/(2θ)。
  高斯 AR(1) 下 OLS 即 MLE（漂移參數），σ 由殘差變異還原。
設定：θ=0.8, μ=1.0, σ=0.5, dt=0.01, N=20000 (T=200)。
驗證：θ̂、σ̂ 相對誤差 < 10%（μ̂ 相對誤差 < 10% 參考）。
只用 numpy，固定種子，不畫圖。
"""
import numpy as np

rng = np.random.default_rng(4)
theta, mu, sigma = 0.8, 1.0, 0.5
dt = 0.01
N = 20000

phi = np.exp(-theta * dt)
q = sigma ** 2 * (1.0 - np.exp(-2.0 * theta * dt)) / (2.0 * theta)
sq = np.sqrt(q)
X = np.zeros(N + 1)
X[0] = mu
eps = rng.standard_normal(N)
for k in range(N):
    X[k + 1] = mu + phi * (X[k] - mu) + sq * eps[k]

x0, x1 = X[:-1], X[1:]
mx0, mx1 = float(np.mean(x0)), float(np.mean(x1))
a_hat = float(np.mean((x0 - mx0) * (x1 - mx1)) / np.mean((x0 - mx0) ** 2))
b_hat = mx1 - a_hat * mx0
resid = x1 - (a_hat * x0 + b_hat)
q_hat = float(np.mean(resid ** 2))
theta_hat = float(-np.log(a_hat) / dt)
mu_hat = float(b_hat / (1.0 - a_hat))
sigma_hat = float(np.sqrt(q_hat * 2.0 * theta_hat / (1.0 - np.exp(-2.0 * theta_hat * dt))))

e_th = abs(theta_hat - theta) / theta
e_mu = abs(mu_hat - mu) / abs(mu)
e_sg = abs(sigma_hat - sigma) / sigma
print(f"true: θ={theta} μ={mu} σ={sigma}")
print(f"hat : θ={theta_hat:.5f} μ={mu_hat:.5f} σ={sigma_hat:.5f}")
print(f"rel err: θ={e_th:.4%} μ={e_mu:.4%} σ={e_sg:.4%} (tol 10%)")
print(f"VERIFY theta_hat={theta_hat:.5f} sigma_hat={sigma_hat:.5f} e_th={e_th:.4f} e_sg={e_sg:.4f}")
assert e_th < 0.10, f"θ 還原誤差過大: {e_th}"
assert e_sg < 0.10, f"σ 還原誤差過大: {e_sg}"
assert e_mu < 0.10, f"μ 還原誤差過大: {e_mu}"
