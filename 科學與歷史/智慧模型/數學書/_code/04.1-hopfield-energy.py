# 04.1 Hopfield 網路：儲存模式、雜訊回憶、能量追蹤
# 驗證能量單調下降定理
import numpy as np

rng = np.random.default_rng(7)
N = 64  # 神經元數


def energy(s, W):
    # E = -1/2 s^T W s（W 對稱、無自環）
    return -0.5 * s @ W @ s


# ---- 用 Hebb 律儲存一個隨機模式 ----
pattern = rng.choice([-1, 1], size=N)
W = np.outer(pattern, pattern) / N      # W_ij = x_i x_j / n
np.fill_diagonal(W, 0.0)                # 無自環

print("=== 儲存模式 ===")
print("模式能量 E =", energy(pattern, W))
h = W @ pattern
stable = np.all(np.sign(h) == pattern)
print("模式是否穩定（sgn(Ws) = s）：", stable)

# ---- 製造雜訊版：翻轉 15% 位元 ----
noise_idx = rng.choice(N, size=int(0.15 * N), replace=False)
noisy = pattern.copy()
noisy[noise_idx] *= -1
wrong0 = np.sum(noisy != pattern)
print()
print("=== 輸入雜訊版 ===")
print("翻轉位元數 =", wrong0, "/", N, " 雜訊版能量 E =", energy(noisy, W))

# ---- 非同步更新直到收斂，追蹤能量 ----
s = noisy.copy()
E_prev = energy(s, W)
print()
print("=== 非同步更新（能量應單調下降）===")
print(f"步 0: 能量 = {E_prev:.3f}")
for step in range(1, 200):
    i = rng.integers(N)                 # 隨機挑一個神經元
    h_i = W[i] @ s
    s[i] = 1 if h_i >= 0 else -1        # sgn 更新
    E = energy(s, W)
    if E != E_prev:                     # 有變化才印
        print(f"步 {step}: 能量 = {E:.3f}")
    if E > E_prev:
        print("警告：能量上升，違反單調下降定理！")
    if np.array_equal(s, pattern):
        print(f"步 {step}: 能量 = {E:.3f}")
        break
    E_prev = E

# ---- 回憶結果 ----
correct = np.sum(s == pattern)
print()
print("=== 回憶結果 ===")
print(f"回憶正確率 = {correct}/{N} = {correct / N:.0%}")
print("最終能量 =", energy(s, W), "（與原模式能量相同即收斂到谷底）")
