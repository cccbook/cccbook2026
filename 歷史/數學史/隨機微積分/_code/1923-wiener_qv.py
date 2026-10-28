# 對應 wiki：1923 年 Wiener 過程（二次變差 [W]_T = T、Levy 模數連續性）
# 說明：T=1 切 N=20000 等分，h=T/N；每條路徑 QV = sum(dW^2)，理論均值 T；
# 200 條平均驗證誤差 < 3%。另驗 max|dW| ~ sqrt(2h log(1/h)) 量級（比值落於 [0.5, 2)）。
# 僅用 numpy，固定種子，不畫圖只印數字。
import numpy as np

SEED = 1923
T = 1.0
N = 20_000
M = 200

rng = np.random.default_rng(SEED)
h = T / N
sd = float(np.sqrt(h))
dW = rng.normal(0.0, sd, size=(M, N))
qv = np.sum(dW ** 2, axis=1)
qv_mean = float(qv.mean())
qv_std = float(qv.std(ddof=1))
rel_err = abs(qv_mean - T) / T

mx = np.max(np.abs(dW), axis=1)
mx_mean = float(mx.mean())
scale = float(np.sqrt(2.0 * h * np.log(1.0 / h)))
ratio = mx_mean / scale

print(f"T={T} N={N} M={M} h={h:.8f}")
print(f"QV_mean={qv_mean:.6f} QV_std={qv_std:.6f} target={T:.6f} rel_err={rel_err:.6f} (tol 0.03)")
print(f"max|dW|_mean={mx_mean:.6f} scale=sqrt(2h log(1/h))={scale:.6f} ratio={ratio:.4f} (tol [0.5,2.0])")

assert rel_err < 0.03, f"Wiener QV rel_err {rel_err} >= 3%"
assert 0.5 < ratio < 2.0, f"max|dW| ratio {ratio} not order-one"
print(f"VERIFY 1923-wiener_qv PASS qv={qv_mean:.4f} target={T:.4f} ratio={ratio:.3f}")
