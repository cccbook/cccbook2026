# 03.2 兩層網路手算 backprop，並用數值差分驗證梯度
# 網路：2 輸入 -> 2 隱藏 (tanh) -> 1 輸出，均方誤差
import numpy as np


def tanh(z):
    return np.tanh(z)


def forward(W1, b1, W2, b2, x):
    # 前向傳播，回傳輸出與中間量（反向時查表用）
    z1 = W1 @ x + b1
    a1 = tanh(z1)
    z2 = W2 @ a1 + b2
    return z2, (z1, a1)


def loss(z2, y):
    # 均方誤差 L = 1/2 (z2 - y)^2（回傳純量）
    return float(0.5 * np.sum((z2 - y) ** 2))


def backprop(W1, b1, W2, b2, x, y):
    # 反向傳播：鏈鎖律算所有梯度
    z2, (z1, a1) = forward(W1, b1, W2, b2, x)
    d2 = z2 - y                          # 輸出層誤差項（線性輸出）
    d1 = (W2.T @ d2) * (1 - a1 ** 2)     # 隱藏層誤差項：W^T delta 乘 tanh 導數
    gW2 = np.outer(d2, a1)               # delta * a^{(l-1)T}
    gb2 = d2
    gW1 = np.outer(d1, x)
    gb1 = d1
    return gW1, gb1, gW2, gb2


def numerical_grad(W1, b1, W2, b2, x, y, eps=1e-6):
    # 中心差分數值梯度：L(theta+eps) - L(theta-eps) / 2eps
    grads = []
    params = [W1, b1, W2, b2]
    for p_idx in range(4):
        g = np.zeros_like(params[p_idx])
        it = np.nditer(params[p_idx], flags=["multi_index"])
        for _ in it:
            idx = it.multi_index
            orig = params[p_idx][idx]
            params[p_idx][idx] = orig + eps
            lp = loss(forward(W1, b1, W2, b2, x)[0], y)
            params[p_idx][idx] = orig - eps
            lm = loss(forward(W1, b1, W2, b2, x)[0], y)
            params[p_idx][idx] = orig
            g[idx] = (lp - lm) / (2 * eps)
        grads.append(g)
    return grads


# ---- 設定參數與資料 ----
rng = np.random.default_rng(42)
W1 = rng.normal(size=(2, 2))
b1 = rng.normal(size=(2,))
W2 = rng.normal(size=(1, 2))
b2 = rng.normal(size=(1,))
x = np.array([1.0, -0.5])
y = np.array([0.3])

# ---- 前向與損失 ----
z2, (z1, a1) = forward(W1, b1, W2, b2, x)
print("=== 前向傳播 ===")
print("z1 =", z1, " a1 =", a1)
print("輸出 z2 =", z2, " 損失 L =", loss(z2, y))

# ---- 解析梯度（backprop）----
gW1, gb1, gW2, gb2 = backprop(W1, b1, W2, b2, x, y)
print()
print("=== 解析梯度（反向傳播）===")
print("dL/dW1 =\n", gW1)
print("dL/db1 =", gb1)
print("dL/dW2 =", gW2)
print("dL/db2 =", gb2)

# ---- 數值差分驗證 ----
ngW1, ngb1, ngW2, ngb2 = numerical_grad(W1, b1, W2, b2, x, y)
print()
print("=== 數值差分驗證（各參數最大差異）===")
for name, a, b in [("dL/dW1", gW1, ngW1), ("dL/db1", gb1, ngb1),
                   ("dL/dW2", gW2, ngW2), ("dL/db2", gb2, ngb2)]:
    print(f"{name}: 最大差異 = {np.max(np.abs(a - b)):.3e}")
print("（差異在 1e-9 級以下，驗證 backprop 實作正確）")

# ---- 更新一步，驗證損失下降（習題 1）----
eta = 0.5
W1 -= eta * gW1; b1 -= eta * gb1; W2 -= eta * gW2; b2 -= eta * gb2
z2_new, _ = forward(W1, b1, W2, b2, x)
print()
print("=== 學習率 0.5 更新一步後 ===")
print("新損失 L =", loss(z2_new, y), "（應比原本下降）")
