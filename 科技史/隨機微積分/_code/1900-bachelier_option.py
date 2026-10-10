# 對應 wiki：1900 年 Bachelier 算術布朗與選擇權定價（Bachelier 模型）
# 說明：S_T = S0 + sigma*sqrt(T)*Z；看漲 payoff = max(S_T-K,0)；
# 封閉解 C = sigma*sqrt(T)*(phi(d) - d*Phi(-d))，d=(S0-K)/(sigma*sqrt(T))，
# 其中 phi 標準常態 pdf，Phi 為 cdf（僅用 numpy 以 A&S 近似實作 cdf，不用 scipy/matplotlib/math）。
import numpy as np

SEED = 1900
S0 = 100.0
SIGMA = 15.0
T = 1.0
K = 100.0
M = 200_000


def phi(x):
    x = np.asarray(x, dtype=np.float64)
    return np.exp(-0.5 * x * x) / np.sqrt(2.0 * np.pi)


def Phi(x):
    # Abramowitz & Stegun 7.1.26，僅用 numpy（exp/sqrt），精度 ~1e-7
    x = float(x)
    a1 = 0.254829592
    a2 = -0.284496736
    a3 = 1.421413741
    a4 = -1.453152027
    a5 = 1.061405429
    p = 0.3275911
    z = x / float(np.sqrt(2.0))
    sgn = 1.0 if z >= 0.0 else -1.0
    az = abs(z)
    t = 1.0 / (1.0 + p * az)
    tau = (((((a5 * t + a4) * t) + a3) * t + a2) * t + a1) * t * float(np.exp(-az * az))
    erfz = sgn * (1.0 - tau)
    return 0.5 * (1.0 + erfz)


rng = np.random.default_rng(SEED)
Z = rng.standard_normal(M)
ST = S0 + SIGMA * float(np.sqrt(T)) * Z
payoff = np.maximum(ST - K, 0.0)
price_mc = float(payoff.mean())
se = float(payoff.std(ddof=1) / np.sqrt(M))

d = (S0 - K) / (SIGMA * float(np.sqrt(T)))
price_closed = float(SIGMA * float(np.sqrt(T)) * (float(phi(d)) - d * Phi(-d)))
# 標準形式交叉核對：C = (S0-K)*Phi(d) + sigma*sqrt(T)*phi(d)
price_std = float((S0 - K) * Phi(d) + SIGMA * float(np.sqrt(T)) * float(phi(d)))

rel_err = abs(price_mc - price_closed) / price_closed

print(f"S0={S0} sigma={SIGMA} T={T} K={K} M={M}")
print(f"d={d:.6f} phi(d)={float(phi(d)):.6f} Phi(d)={Phi(d):.6f}")
print(f"closed(Bachelier)={price_closed:.6f} std_form={price_std:.6f}")
print(f"mc_price={price_mc:.6f} se={se:.6f}")
print(f"rel_err={rel_err:.6f} (tol 0.01)")

assert rel_err < 0.01, f"Bachelier rel_err {rel_err} >= 1%"
print(f"VERIFY 1900-bachelier_option PASS mc={price_mc:.4f} closed={price_closed:.4f} rel_err={rel_err:.4%}")
