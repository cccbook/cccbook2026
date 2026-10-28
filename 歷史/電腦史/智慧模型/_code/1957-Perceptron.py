# 1957 - Perceptron 感知器 (Rosenblatt)
# 對應本書: 1957-Perceptron感知器.md
# 公式: y = H(w·x - θ), Δw = η (t - y) x
# 展示: 保證學會 AND (線性可分), 學不會 XOR; 同時用 torch 版對照
import numpy as np
import torch

X_and = np.array([[0, 0], [0, 1], [1, 0], [1, 1]], float)
t_and = np.array([0, 0, 0, 1])
X_xor = X_and
t_xor = np.array([0, 1, 1, 0])


def train_perceptron(X, t, eta=0.5, epochs=20):
    w = np.zeros(X.shape[1])
    b = 0.0
    for ep in range(epochs):
        err = 0
        for xi, ti in zip(X, t):
            y = 1 if w @ xi - b > 0 else 0
            w += eta * (ti - y) * xi
            b -= eta * (ti - y)
            err += abs(ti - y)
        if err == 0:
            return w, b, ep + 1
    return w, b, epochs


def predict(X, w, b):
    return np.array([1 if w @ xi - b > 0 else 0 for xi in X])


def main():
    np.random.seed(0)
    torch.manual_seed(0)
    for name, X, t in [("AND(線性可分)", X_and, t_and), ("XOR(線性不可分)", X_xor, t_xor)]:
        w, b, ep = train_perceptron(X, t)
        pred = predict(X, w, b)
        print(f"{name}: 收斂於第 {ep} 輪, w={np.round(w,2)}, b={round(b,2)}, "
              f"預測={pred.tolist()}, 正確={bool(np.array_equal(pred, t))}")
    # torch 對照: 單層線性 + step, 在 AND 上一步到位驗證
    print("torch 驗證 AND 點積:", (torch.tensor([1.0, 1.0]) @ torch.tensor([1.0, 1.0])).item(),
          "> 1.5 即激發 (M-P/感知器同源)")


if __name__ == "__main__":
    main()
