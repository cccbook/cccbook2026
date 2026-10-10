# 對應 wiki：1827 年 Brown 運動 / 隨機漫步與擴散（MSD = 4Dt 二維）
# 說明：二維隨機漫步，每維增量 ~ N(0, 2D·dt)，D=1, dt=1；
# 理論 MSD(t) = 4Dt。取中段 t_mid=N//2 驗證，避免起點暫態與終點單一樣本偏差。
# 僅用 numpy，固定種子，不畫圖只印數字。
import numpy as np

SEED = 1827
D = 1.0
DT = 1.0
N = 20000
N_PATHS = 2000
T_MID = N // 2  # 中段
BATCH = 200  # 分批產生，控制記憶體

rng = np.random.default_rng(SEED)
sigma_1d = float(np.sqrt(2.0 * D * DT))

sum_r2 = 0.0
sum_r2_sq = 0.0
for start in range(0, N_PATHS, BATCH):
    b = min(BATCH, N_PATHS - start)
    dx = rng.normal(0.0, sigma_1d, size=(b, T_MID))
    dy = rng.normal(0.0, sigma_1d, size=(b, T_MID))
    x = dx.sum(axis=1)
    y = dy.sum(axis=1)
    r2 = x * x + y * y
    sum_r2 += float(r2.sum())
    sum_r2_sq += float((r2 ** 2).sum())

msd = sum_r2 / N_PATHS
expected = 4.0 * D * (T_MID * DT)
rel_err = abs(msd - expected) / expected
var_r2 = sum_r2_sq / N_PATHS - msd ** 2
se = float(np.sqrt(max(var_r2, 0.0) / N_PATHS))

print(f"N={N} n_paths={N_PATHS} D={D} dt={DT} t_mid={T_MID}")
print(f"expected_MSD=4Dt={expected:.6f}")
print(f"sample_MSD={msd:.6f} se={se:.6f}")
print(f"rel_err={rel_err:.6f} (tol 0.05)")

assert rel_err < 0.05, f"MSD rel_err {rel_err} >= 5%"
print(f"VERIFY 1827-brownian_msd PASS msd={msd:.4f} expected={expected:.4f} rel_err={rel_err:.4%}")
