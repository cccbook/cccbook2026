# 2006 - 深度信念網路 DBN: RBM + 對比散度 CD-1 + 貪婪逐層堆疊
# 對應本書: 2006-Hinton深度信念網路.md
# 公式: P(h_j=1|v)=σ(c_j+Σ_i v_i w_ij); Δw_ij = η(<v_i h_j>_data - <v_i h_j>_1)
# 展示: numpy 兩層 RBM 貪婪堆疊 -- 第1層學橫條/直條, 第2層學「哪一類」, 逐層重建誤差皆下降
import numpy as np


def sigmoid(z):
    return 1 / (1 + np.exp(-z))


def train_rbm(X, nh, lr=0.5, epochs=30, seed=0, binary=True):
    """CD-1 訓練單層 RBM, 回傳 (W, b, c, 重建誤差)."""
    rng = np.random.default_rng(seed)
    nv = X.shape[1]
    W = rng.normal(0, 0.1, (nv, nh))
    b, c = np.zeros(nv), np.zeros(nh)
    for _ in range(epochs):
        h_prob = sigmoid(X @ W + c)                       # <vh>_data
        h = (rng.random(h_prob.shape) < h_prob).astype(float)
        v1_prob = sigmoid(h @ W.T + b)                    # Gibbs 一步 (CD-1)
        v1 = (rng.random(v1_prob.shape) < v1_prob).astype(float)
        h1_prob = sigmoid(v1 @ W + c)                     # <vh>_1
        W += lr * (X.T @ h_prob - v1.T @ h1_prob) / len(X)
        b += lr * (X - v1).mean(0)
        c += lr * (h_prob - h1_prob).mean(0)
    recon_p = sigmoid(sigmoid(X @ W + c) @ W.T + b)
    recon = (recon_p > 0.5).astype(float) if binary else recon_p
    return W, b, c, float(((recon - X) ** 2).mean())


def main():
    rng = np.random.default_rng(0)
    # 資料: 6-bit 橫條 (前3全1) 與直條 (後3全1) 加雜訊 -- RBM 的玩具世界
    horiz = np.array([1, 1, 1, 0, 0, 0])
    vert = np.array([0, 0, 0, 1, 1, 1])
    X = np.array([(horiz if i % 2 == 0 else vert) ^ (rng.random(6) < 0.1)
                  for i in range(400)]).astype(float)
    # 第1層: 從像素學特徵
    W1, b1, c1, err1 = train_rbm(X, nh=4, seed=1)
    print(f"第1層 RBM(6->4): 重建誤差={err1:.3f} (隨機猜≈0.5)")
    print("學到的特徵 (W每列≈橫條/直條偵測器):\n", np.round(W1, 1))
    # 第2層: 把第1層的隱藏表徵當新資料 -- 貪婪逐層 (greedy layer-wise)
    H1 = sigmoid(X @ W1 + c1)
    W2, b2, c2, err2 = train_rbm(H1, nh=2, seed=2, binary=False)
    print(f"第2層 RBM(4->2): 重建誤差={err2:.3f} (在特徵空間再壓縮)")
    H2 = sigmoid(H1 @ W2 + c2)
    # 第2層表徵應把兩類分開: 類內距離 << 類間距離
    d_in = np.abs(H2[0::2] - H2[0]).mean() + np.abs(H2[1::2] - H2[1]).mean()
    d_out = np.abs(H2[0::2].mean(0) - H2[1::2].mean(0)).mean()
    print(f"頂層表徵: 類內散佈={d_in:.3f}, 類間距離={d_out:.3f} "
          f"({'分開 -- 深層學到類別' if d_out > d_in else '未分開'})")
    print("結論: 逐層預訓練把深網初值放在好位置 -- 2006 年深網第一次訓得動")


if __name__ == "__main__":
    main()
