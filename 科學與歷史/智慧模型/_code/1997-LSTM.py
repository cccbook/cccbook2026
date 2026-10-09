# 1997 - LSTM 長短期記憶 (Hochreiter & Schmidhuber)
# 對應本書: 1997-LSTM長短期記憶.md
# 公式: f,i,o 閘 + c_t = f⊙c_{t-1} + i⊙c̃ (加法高速通道, ∂c_t/∂c_{t-1}≈f 直通梯度)
# 展示: (1) numpy 手寫 LSTM cell 前向; (2) torch LSTM 學會「記住數十步前的字元」(合成 Reber 縮影)
import numpy as np
import torch
import torch.nn as nn


def sigmoid(z):
    return 1 / (1 + np.exp(-z))


def lstm_cell_numpy(x, h_prev, c_prev, P):
    """單步 LSTM 前向 (numpy 手寫, 展示閘門數學)."""
    z = np.concatenate([h_prev, x])
    f = sigmoid(P["Wf"] @ z + P["bf"])
    i = sigmoid(P["Wi"] @ z + P["bi"])
    c_tilde = np.tanh(P["Wc"] @ z + P["bc"])
    c = f * c_prev + i * c_tilde          # 加法! 梯度直通的關鍵
    o = sigmoid(P["Wo"] @ z + P["bo"])
    h = o * np.tanh(c)
    return h, c, {"f": f, "i": i, "o": o}


def main():
    rng = np.random.default_rng(0)
    d, hdim = 3, 4
    P = {k: rng.standard_normal((hdim, hdim + d)) * 0.5 for k in ["Wf", "Wi", "Wc", "Wo"]}
    P.update({k: np.zeros(hdim) for k in ["bf", "bi", "bc", "bo"]})
    P["bf"] += 1.0  # forget-bias trick: 初始多記少忘
    h, c = np.zeros(hdim), np.zeros(hdim)
    print("numpy LSTM cell: 輸入 5 步, 觀察遺忘閘 f≈1 時細胞狀態被保留")
    for t in range(5):
        x = rng.standard_normal(d)
        h, c, g = lstm_cell_numpy(x, h, c, P)
        print(f"  t={t} f={np.round(g['f'], 2)} |c|={np.linalg.norm(c):.2f}")

    # torch: 延遲回憶任務 -- 看到開頭符號(0/1), 經過 T 步雜訊後複述 (RNN 殺手, LSTM 拿手)
    torch.manual_seed(0)
    T, N = 15, 1000
    X = torch.randint(2, 4, (N, T))       # 其餘步為 2/3 雜訊
    X[:, 0] = torch.randint(0, 2, (N,))   # 首符號只有 0/1 (平衡兩類)
    y = X[:, 0].long()
    net = nn.Sequential(nn.Embedding(4, 8), nn.LSTM(8, 32, batch_first=True),
                        )
    lstm, clf = net[1], nn.Linear(32, 2)
    opt = torch.optim.Adam(list(lstm.parameters()) + list(clf.parameters()) + list(net[0].parameters()), lr=1e-2)
    for ep in range(30):
        opt.zero_grad()
        _, (hn, _) = lstm(net[0](X))
        loss = nn.CrossEntropyLoss()(clf(hn[-1]), y)
        loss.backward()
        opt.step()
    with torch.no_grad():
        _, (hn, _) = lstm(net[0](X))
        acc = (clf(hn[-1]).argmax(1) == y).float().mean().item()
    print(f"torch LSTM 延遲 {T} 步回憶準確率: {acc:.2f} (普通 RNN 在此任務≈0.5 猜測水平)")


if __name__ == "__main__":
    main()
