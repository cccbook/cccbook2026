"""1990 線性 BSDE：最小平方蒙地卡羅 (LSMC) vs 解析解。
對應 wiki：Pardoux–Peng (1990) BSDE 解存在唯一；線性 BSDE 顯式解
  Y_t = E[ ξ * exp(-r(T-t)) | F_t ]（此處 f = -rY, b = 0）。
本檔：終值 ξ = sin(W_T), T = 1, r = 0.05, W 為標準布朗運動。
解析：E[sin(W_T)|F_t] = sin(W_t) exp(-(T-t)/2)，故
  Y_t = sin(W_t) exp(-(r+0.5)(T-t))，特別 Y_0 = 0。
數值：向後 Euler 隱式格式 Y_k = E[Y_{k+1}|F_k] / (1+r dt)，
條件期望以 W_k 的 5 次多項式基函數最小平方迴歸近似。
驗證：Y_0 真值為 0，「誤差 < 2%」採絕對誤差 |Y0_hat| < 0.02
（尺度：ξ∈[-1,1]，2% 尺度即 0.02）；另檢 t=0.5 路徑 RMSE < 0.05。
只用 numpy，固定種子，不畫圖。
"""
import numpy as np

rng = np.random.default_rng(0)
r = 0.05
T = 1.0
N = 20
dt = T / N
M = 100000
DEG = 5

dW = np.sqrt(dt) * rng.standard_normal((M, N))
W = np.zeros((M, N + 1))
W[:, 1:] = np.cumsum(dW, axis=1)

Y_next = np.sin(W[:, N])
Y_at_half = None
HALF_K = N // 2  # t = 0.5

for k in range(N - 1, 0, -1):
    Wk = W[:, k]
    X = np.vander(Wk, DEG + 1, increasing=True)  # [1, w, ..., w^5]
    beta, *_ = np.linalg.lstsq(X, Y_next, rcond=None)
    Yk = (X @ beta) / (1.0 + r * dt)
    if k == HALF_K:
        Y_at_half = Yk.copy()
    Y_next = Yk  # Y_1 的各路徑估計

Y0_hat = float(np.mean(Y_next) / (1.0 + r * dt))
Y0_true = 0.0
abs_err = abs(Y0_hat - Y0_true)

# t = 0.5 解析解對照（非退化檢驗）
t_half = HALF_K * dt
Y_true_half = np.sin(W[:, HALF_K]) * np.exp(-(r + 0.5) * (T - t_half))
rmse_half = float(np.sqrt(np.mean((Y_at_half - Y_true_half) ** 2)))

print(f"Y0_true = {Y0_true:.6f}")
print(f"Y0_lsmc = {Y0_hat:.6f}")
print(f"abs_err_Y0 = {abs_err:.6f} (tol 0.02)")
print(f"RMSE@t=0.5 = {rmse_half:.6f} (tol 0.05)")
print(f"VERIFY Y0_abs_err={abs_err:.6f} rmse_half={rmse_half:.6f}")
assert abs_err < 0.02, f"Y0 誤差過大: {abs_err}"
assert rmse_half < 0.05, f"t=0.5 RMSE 過大: {rmse_half}"
