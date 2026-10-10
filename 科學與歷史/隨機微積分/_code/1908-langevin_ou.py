# 對應 wiki：1908 年 Langevin 方程 / Ornstein-Uhlenbeck 過程（漲落-耗散）
# 說明：OU dX = -theta*X*dt + sigma*dW，theta=1.5, sigma=0.8；
# 採精確離散 X_{n+1} = e^{-theta dt} X_n + sqrt(sigma^2/(2theta)(1-e^{-2theta dt})) Z；
# 平穩變異數 sigma^2/(2theta)，均值 0。驗證變異數誤差 < 5% 且均值 ~= 0。
# 僅用 numpy，固定種子，不畫圖只印數字。
import numpy as np

SEED = 1908
THETA = 1.5
SIGMA = 0.8
DT = 0.01
N = 300_000
BURN = 20_000

rng = np.random.default_rng(SEED)
a = float(np.exp(-THETA * DT))
target_var = SIGMA ** 2 / (2.0 * THETA)
step_var = target_var * (1.0 - float(np.exp(-2.0 * THETA * DT)))
step_sd = float(np.sqrt(step_var))

Z = rng.standard_normal(N)
x = np.empty(N, dtype=np.float64)
v = 0.0
for n in range(N):
    v = a * v + step_sd * float(Z[n])
    x[n] = v

seg = x[BURN:]
m = float(seg.mean())
vhat = float(seg.var(ddof=0))
rel_err = abs(vhat - target_var) / target_var

print(f"OU theta={THETA} sigma={SIGMA} dt={DT} N={N} burn={BURN}")
print(f"target_var={target_var:.6f} sample_var={vhat:.6f} rel_err={rel_err:.6f} (tol 0.05)")
print(f"sample_mean={m:.6f} (tol |mean|<0.03)")

assert rel_err < 0.05, f"OU var rel_err {rel_err} >= 5%"
assert abs(m) < 0.03, f"OU mean {m} not ~= 0"
print(f"VERIFY 1908-langevin_ou PASS var={vhat:.4f} target={target_var:.4f} mean={m:.5f}")
