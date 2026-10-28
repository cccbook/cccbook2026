# 對應 wiki：1906 年 Markov 鏈 / 平穩分佈（Chapman-Kolmogorov、遍歷性）
# 說明：二態鏈 P=[[0.7,0.3],[0.4,0.6]]；解析平穩分佈 pi 滿足 pi=piP，
# 得 pi0=0.4/(0.3+0.4)=4/7, pi1=3/7；以 10 萬步模擬頻率對照，誤差 < 0.01。
# 僅用 numpy，固定種子，不畫圖只印數字。
import numpy as np

SEED = 1906
P = np.array([[0.7, 0.3], [0.4, 0.6]], dtype=np.float64)
N = 100_000

# 解析平穩分佈（留數法）：pi0 = P10/(P01+P10)
pi0 = P[1, 0] / (P[0, 1] + P[1, 0])
pi = np.array([pi0, 1.0 - pi0])

rng = np.random.default_rng(SEED)
U = rng.random(N)
state = 0
c0 = 0
for u in U:
    # 依目前狀態決定下一狀態
    p_stay = P[state, state]
    if u < p_stay:
        pass  # 留在原態
    else:
        state = 1 - state
    if state == 0:
        c0 += 1
freq = np.array([c0 / N, 1.0 - c0 / N])
abs_err = np.abs(freq - pi)
max_err = float(abs_err.max())

print(f"P={P.tolist()} N={N}")
print(f"analytic_pi=[{pi[0]:.6f}, {pi[1]:.6f}]")
print(f"empirical_freq=[{freq[0]:.6f}, {freq[1]:.6f}]")
print(f"abs_err=[{abs_err[0]:.6f}, {abs_err[1]:.6f}] max_err={max_err:.6f} (tol 0.01)")

assert max_err < 0.01, f"Markov stationary max_err {max_err} >= 0.01"
print(f"VERIFY 1906-markov_stationary PASS freq0={freq[0]:.4f} pi0={pi[0]:.4f} max_err={max_err:.5f}")
