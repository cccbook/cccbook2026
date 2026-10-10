# 對應 wiki：1905 年 Einstein 擴散（MSD = 2Dt）與 Ornstein-Uhlenbeck 過程
# 說明：一維 OU dx = -gamma*x*dt + sqrt(2D)*dW，gamma=2, D=0.5；
# 平穩變異數 D/gamma；短時滯下 MSD(tau) ~= 2D*tau（Einstein 擴散）。
# 以精確離散跑至平穩，取小 tau1/tau2 的 MSD 斜率驗證 ~= 2D，誤差 < 8%。
# 僅用 numpy，固定種子，不畫圖只印數字。
import numpy as np

SEED = 1905
GAMMA = 2.0
D = 0.5
DT = 0.001
N = 300_000  # 總步數 (T=300)，夠長以達平穩並壓低 MC 誤差
BURN = 50_000  # 前段丟棄
K1 = 10  # tau1 = 0.01
K2 = 30  # tau2 = 0.03

rng = np.random.default_rng(SEED)
a = float(np.exp(-GAMMA * DT))
q = float((D / GAMMA) * (1.0 - np.exp(-2.0 * GAMMA * DT)))
s = float(np.sqrt(q))

Z = rng.standard_normal(N)
xs = np.empty(N, dtype=np.float64)
x = 0.0
for n in range(N):
    x = a * x + s * float(Z[n])
    xs[n] = x

seg = xs[BURN:]
tau1 = K1 * DT
tau2 = K2 * DT
msd1 = float(np.mean((seg[K1:] - seg[:-K1]) ** 2))
msd2 = float(np.mean((seg[K2:] - seg[:-K2]) ** 2))
slope = (msd2 - msd1) / (tau2 - tau1)
target = 2.0 * D
rel_err = abs(slope - target) / target

print(f"OU gamma={GAMMA} D={D} dt={DT} N={N} burn={BURN}")
print(f"tau1={tau1:.4f} MSD1={msd1:.6f} tau2={tau2:.4f} MSD2={msd2:.6f}")
print(f"slope={slope:.6f} target_2D={target:.6f}")
print(f"rel_err={rel_err:.6f} (tol 0.08)")

assert rel_err < 0.08, f"Einstein slope rel_err {rel_err} >= 8%"
print(f"VERIFY 1905-einstein_diffusion PASS slope={slope:.4f} target={target:.4f} rel_err={rel_err:.4%}")
