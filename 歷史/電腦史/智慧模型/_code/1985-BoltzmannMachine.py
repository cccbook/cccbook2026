# 1985 - Boltzmann 機器
# 對應本書: 1985-Boltzmann機器.md
# 公式: P(s_i=1) = 1/(1+exp(-ΔE_i/T)); Δw_ij = η(<s_i s_j>_data - <s_i s_j>_model)
# 展示: 4 可見單元學兩個模式的共現統計; 高溫亂走、低溫收斂 (模擬退火縮影)
import numpy as np


def sample_p(h):
    return 1.0 / (1.0 + np.exp(-h))


def gibbs_step(state, W, b, T):
    for i in np.random.permutation(len(state)):
        h = (W[i] @ state + b[i]) / T
        state[i] = 1 if np.random.rand() < sample_p(h) else -1
    return state


def cooccur(samples):
    return np.mean([np.outer(s, s) for s in samples], axis=0)


def main():
    rng = np.random.default_rng(0)
    np.random.seed(0)
    # 資料: 兩種模式等機率出現 (0/1 轉 ±1)
    data = [np.array([1, 1, -1, -1]), np.array([-1, -1, 1, 1])] * 50
    N = 4
    W = np.zeros((N, N))
    b = np.zeros(N)
    eta, T = 0.1, 1.0
    for epoch in range(60):
        # clamped (data) 統計
        Cd = cooccur(data)
        # free-running (model) 統計: 從隨機態 Gibbs 採樣
        fantasies = []
        for _ in range(50):
            s = rng.choice([-1, 1], size=N).astype(float)
            fantasies.append(gibbs_step(s, W, b, T).copy())
        Cm = cooccur(fantasies)
        dW = eta * (Cd - Cm)          # 核心: 資料共現推高權重, 幻想共現壓低權重
        dW[np.diag_indices(N)] = 0
        W += dW
    print("學到的 W (符號):\n", np.sign(W).astype(int))
    print("含義: (0,1) 與 (2,3) 內部正相關、兩群間負相關 = 記住兩個模式的共現結構")
    # 退火展示: 同一 W, 高溫 vs 低溫的翻轉機率
    print("T=10 時 P(翻轉|h=1):", round(float(sample_p(-1 / 10)), 3), "(近隨機亂走)")
    print("T=0.1 時 P(翻轉|h=1):", round(float(sample_p(-1 / 0.1)), 5), "(近確定性=Hopfield)")


if __name__ == "__main__":
    main()
