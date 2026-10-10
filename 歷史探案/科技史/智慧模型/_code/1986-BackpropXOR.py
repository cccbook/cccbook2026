# 1986 - 反向傳播演算法 (Rumelhart-Hinton-Williams)
# 對應本書: 1986-反向傳播演算法.md
# 公式: ∂L/∂W1 = (∂L/∂ŷ)(∂ŷ/∂a)(∂a/∂z)(∂z/∂W1); 誤差 δ 倒傳: dz = (d @ W2) * a * (1-a)
# 展示: 2-2-1 sigmoid 網路, 手寫 numpy 反向傳播破解 XOR (書中程式完整可跑版)
import numpy as np
import torch


def sigmoid(z):
    return 1 / (1 + np.exp(-z))


def main():
    X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]], float)
    y = np.array([0, 1, 1, 0], float)
    rng = np.random.default_rng(0)
    W1, b1 = rng.standard_normal((2, 2)), np.zeros(2)
    W2, b2 = rng.standard_normal(2), np.zeros(1)
    lr = 0.5
    for step in range(3000):
        a = sigmoid(X @ W1 + b1)            # 隱藏層
        p = sigmoid(a @ W2 + b2)            # 輸出
        d = (p - y) * p * (1 - p)           # 輸出誤差訊號 δ
        dz = (np.outer(d, W2)) * a * (1 - a)  # 倒傳回隱藏層 (鏈鎖律)
        W2 -= lr * (a.T @ d)
        b2 -= lr * d.sum()
        W1 -= lr * (X.T @ dz)
        b1 -= lr * dz.sum(axis=0)
    a = sigmoid(X @ W1 + b1)
    p = sigmoid(a @ W2 + b2)
    print("numpy 手寫反向傳播 XOR 輸出:", np.round(p, 2).tolist(), "(目標 [0,1,1,0])")
    print("Minsky-Papert 死刑判決:", "撤銷 -- 隱藏層把 XOR 攤平成線性可分" if
          all((p[i] > 0.9 if y[i] else p[i] < 0.1) for i in range(4)) else "未收斂")

    # torch 對照: 同一結構交給 autograd (反向傳播 = reverse-mode 自動微分)
    torch.manual_seed(0)
    net = torch.nn.Sequential(torch.nn.Linear(2, 2), torch.nn.Sigmoid(),
                              torch.nn.Linear(2, 1), torch.nn.Sigmoid())
    opt = torch.optim.SGD(net.parameters(), lr=5.0)
    Xt = torch.tensor(X, dtype=torch.float32)
    yt = torch.tensor(y, dtype=torch.float32).view(-1, 1)
    for _ in range(5000):
        opt.zero_grad()
        loss = torch.nn.functional.mse_loss(net(Xt), yt)
        loss.backward()   # <-- 這一行就是反向傳播
        opt.step()
    with torch.no_grad():
        out = [round(float(v), 2) for v in net(Xt).ravel()]
        print("torch autograd XOR 輸出:", out)


if __name__ == "__main__":
    main()
