"""2021 一維雙峰擴散生成：去噪分數匹配 + 多退火 Langevin。
對應 wiki：Song–Ermon (2019) NCSN 去噪分數匹配、Song et al. (2021)
  Score-based SDE / 退火 Langevin 動力學。
資料：0.5 N(-2, 0.4²) + 0.5 N(+2, 0.4²)。
模型：score s(x) = Φ(x) w，Φ 為 K=40 RBF 特徵
  φ_j = exp(-(x-c_j)²/(2h²))，c 均勻分佈 [-4,4]，h=0.3，
  外加線性項 x 與常數項 1（共 K+2 維）以修正 RBF 在尾部→0、
  導致 Langevin 缺乏內拉力而樣本外偏的問題；
  以 numpy 手刻去噪分數匹配（DSM）閉式 ridge 解學各噪聲位準的 score：
  min_w E‖F(x̃)w + (x̃-x)/σ²‖²，x̃ = x + σε（RBF 懲罰 1.0，線性/常數 0.1）。
採樣：噪聲位準 [1.0, 0.7, 0.4, 0.2, 0.1] 由大到小退火，
  每位準 Langevin 100 步，步長 α=0.1σ²（score 截幅 ±20，狀態截幅 ±5），5000 點。
驗證：雙峰比例 |P(x>0)-0.5| < 0.1；兩峰均值 ≈ ±2 誤差 < 0.2；
  直方圖峰谷比 > 2（峰窗 ±[1.25,2.75] 對中央谷）。
只用 numpy，固定種子，不畫圖。
"""
import numpy as np

rng = np.random.default_rng(5)

# ---- 資料 ----
N_TRAIN = 10000
SIG_DATA = 0.4
comp = (rng.random(N_TRAIN) < 0.5).astype(float)  # 0 -> -2, 1 -> +2
x_data = np.where(comp < 0.5, -2.0, 2.0) + SIG_DATA * rng.standard_normal(N_TRAIN)

# ---- RBF + 線性/常數 ----
K = 40
centers = np.linspace(-4.0, 4.0, K)
h = 0.3


def feat_mat(x):
    d = x[:, None] - centers[None, :]
    Phi = np.exp(-0.5 * (d / h) ** 2)
    return np.column_stack([Phi, x, np.ones_like(x)])


# ---- 各噪聲位準 DSM ridge ----
sigmas = [1.0, 0.7, 0.4, 0.2, 0.1]
LAM = 1.0
Ws = []
for sg in sigmas:
    eps = rng.standard_normal(N_TRAIN)
    xt = x_data + sg * eps
    F = feat_mat(xt)  # (N, K+2)
    tgt = -eps / sg  # -(x̃-x)/σ²
    P = np.eye(K + 2) * LAM
    P[K, K] = 0.1
    P[K + 1, K + 1] = 0.1
    w = np.linalg.solve(F.T @ F + P, F.T @ tgt)
    Ws.append(w)

# ---- 退火 Langevin 採樣 ----
M_S = 5000
x = 2.0 * rng.standard_normal(M_S)  # N(0, 4) 初始化
STEPS = 100
for sg, w in zip(sigmas, Ws):
    alpha = 0.1 * sg ** 2
    sqa = np.sqrt(alpha)
    for _ in range(STEPS):
        s = feat_mat(x) @ w
        s = np.clip(s, -20.0, 20.0)
        x = x + 0.5 * alpha * s + sqa * rng.standard_normal(M_S)
        x = np.clip(x, -5.0, 5.0)

frac_pos = float(np.mean(x > 0))
ratio_err = abs(frac_pos - 0.5)
pos = x[x > 0]
neg = x[x <= 0]
mean_pos = float(np.mean(pos)) if pos.size else np.nan
mean_neg = float(np.mean(neg)) if neg.size else np.nan

# 峰谷比：32 bins 於 [-4, 4]
counts, edges = np.histogram(x, bins=32, range=(-4.0, 4.0))
mid = (edges[:-1] + edges[1:]) / 2
peak_l = float(np.max(counts[(mid >= -2.75) & (mid <= -1.25)]))
peak_r = float(np.max(counts[(mid >= 1.25) & (mid <= 2.75)]))
valley = float(counts[np.argmin(np.abs(mid - 0.0))])
pv_ratio = float(min(peak_l, peak_r) / max(valley, 1.0))

print(f"frac_pos = {frac_pos:.4f} (err {ratio_err:.4f}, tol 0.1)")
print(f"mean_neg = {mean_neg:.4f} (target -2, tol 0.2)")
print(f"mean_pos = {mean_pos:.4f} (target +2, tol 0.2)")
print(f"peak_l = {peak_l:.0f}, peak_r = {peak_r:.0f}, valley = {valley:.0f}, pv_ratio = {pv_ratio:.3f} (tol > 2)")
print(f"VERIFY frac_pos={frac_pos:.4f} mean_neg={mean_neg:.4f} mean_pos={mean_pos:.4f} pv={pv_ratio:.3f}")
assert ratio_err < 0.1, f"雙峰比例偏差過大: {frac_pos}"
assert abs(mean_pos - 2.0) < 0.2, f"右峰均值偏差: {mean_pos}"
assert abs(mean_neg + 2.0) < 0.2, f"左峰均值偏差: {mean_neg}"
assert pv_ratio > 2.0, f"峰谷比不足: {pv_ratio}"
