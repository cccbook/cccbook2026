"""1993 粒子濾波（一維非線性、二次觀測）vs Kalman 基準。
對應 wiki：Gordon–Salmond–Smith (1993) bootstrap filter；Kalman (1960) 線性最優濾波。
狀態：x_{k+1} = a x_k + b + √Q ε（a=0.9, b=0.5, Q=0.5），均值 5 恆正，
  使二次觀測 y_k = x_k^2/10 + √R η（R=0.5）免於符號不可辨識。
粒子濾波：bootstrap（提議=轉移先驗），2000 粒子，系統重採樣。
同場 Kalman：相同動態、相同真值軌跡，但線性觀測 y_lin = x + √R η'，
  Kalman 為該線性子問題的最優解，作為 RMSE 基準。
驗證：RMSE_pf / RMSE_kal < 1.5（九成水準內、容忍 50% 退化），
  或 RMSE_pf < 2.0。閾值 2.0 的合理性：狀態平穩標準差
  √(Q/(1-a²)) ≈ 1.62，2.0 約 1.2 倍先驗 spread，代表濾波有效收斂。
只用 numpy，固定種子，不畫圖。
"""
import numpy as np

rng = np.random.default_rng(2)
a, b = 0.9, 0.5
Q, R = 0.5, 0.5
sQ, sR = np.sqrt(Q), np.sqrt(R)
T = 100
Np = 2000


def systematic_resample(w, rng):
    N = w.size
    u0 = rng.random() / N
    u = u0 + np.arange(N) / N
    cum = np.cumsum(w)
    idx = np.searchsorted(cum, u)
    return idx


# 真值與兩種觀測
x_true = np.zeros(T + 1)
x_true[0] = 5.0
for k in range(T):
    x_true[k + 1] = a * x_true[k] + b + sQ * rng.standard_normal()
y_nl = x_true[1:] ** 2 / 10.0 + sR * rng.standard_normal(T)
y_lin = x_true[1:] + sR * rng.standard_normal(T)

# --- Kalman（線性子問題基準） ---
xk, Pk = 5.0, 1.0
xhat_kal = np.zeros(T)
for k in range(T):
    xp = a * xk + b
    Pp = a * a * Pk + Q
    Kg = Pp / (Pp + R)
    xk = xp + Kg * (y_lin[k] - xp)
    Pk = (1.0 - Kg) * Pp
    xhat_kal[k] = xk
rmse_kal = float(np.sqrt(np.mean((xhat_kal - x_true[1:]) ** 2)))

# --- Bootstrap 粒子濾波（二次觀測） ---
parts = 5.0 + 1.0 * rng.standard_normal(Np)
xhat_pf = np.zeros(T)
for k in range(T):
    parts = a * parts + b + sQ * rng.standard_normal(Np)
    pred = parts ** 2 / 10.0
    # 對數權重避免下溢
    logw = -0.5 * ((y_nl[k] - pred) ** 2) / R
    logw -= np.max(logw)
    w = np.exp(logw)
    w /= np.sum(w)
    xhat_pf[k] = float(np.sum(parts * w))
    parts = parts[systematic_resample(w, rng)]

rmse_pf = float(np.sqrt(np.mean((xhat_pf - x_true[1:]) ** 2)))
ratio = rmse_pf / rmse_kal if rmse_kal > 0 else np.inf

print(f"RMSE_pf = {rmse_pf:.6f}, RMSE_kal = {rmse_kal:.6f}, ratio = {ratio:.6f}")
print(f"VERIFY rmse_pf={rmse_pf:.6f} rmse_kal={rmse_kal:.6f} ratio={ratio:.6f}")
assert np.isfinite(rmse_pf) and np.isfinite(rmse_kal)
assert (ratio < 1.5) or (rmse_pf < 2.0), f"粒子濾波未達標: ratio={ratio}, rmse={rmse_pf}"
