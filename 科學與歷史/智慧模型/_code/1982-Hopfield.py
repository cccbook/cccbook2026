# 1982 - Hopfield 網路能量函數
# 對應本書: 1982-Hopfield網路能量函數.md
# 公式: s_i <- sign(Σ_j w_ij s_j - θ_i); E = -1/2 Σ w_ij s_i s_j + Σ θ_i s_i (每次更新 ΔE ≤ 0)
# Hebb 儲存: w_ij = (1/N) Σ_μ ξ_i^μ ξ_j^μ ; 容量 p_max ≈ 0.138N
# 展示: 帶噪線索自動補全為記憶 (內容定址), 並印出能量單調下降
import numpy as np


def energy(s, W, theta=0.0):
    return -0.5 * s @ W @ s + theta * s.sum()


def main():
    rng = np.random.default_rng(0)
    xi = np.array([[1, 1, 1, 1, -1, -1, -1, -1],      # 記憶 A (書中範例)
                   [1, -1, 1, -1, 1, -1, 1, -1]], float)  # 記憶 B
    N = xi.shape[1]
    W = (xi.T @ xi) / N
    np.fill_diagonal(W, 0)
    cue = np.array([1, 1, -1, 1, -1, -1, -1, 1], float)  # 2 位錯的殘缺線索
    print("記憶A:", xi[0].astype(int).tolist())
    print("線索 :", cue.astype(int).tolist(), "(含2位錯誤)")
    s = cue.copy()
    E_prev = energy(s, W)
    print(f"  t=0 E={E_prev:.3f} s={s.astype(int).tolist()}")
    for t in range(1, 6):
        order = rng.permutation(N)          # 非同步更新
        for i in order:
            s[i] = 1 if W[i] @ s >= 0 else -1
        E = energy(s, W)
        assert E <= E_prev + 1e-9, "能量必須不增!"
        print(f"  t={t} E={E:.3f} s={s.astype(int).tolist()}")
        E_prev = E
    print("補全為記憶A:", bool(np.array_equal(s, xi[0])),
          f"(容量上限 p_max≈{0.138 * N:.1f} 個模式, 此處存 2 個)")


if __name__ == "__main__":
    main()
