# 03.1 用 ReLU 階梯逼近 sin(x)——數值驗證泛近似定理
# 以及驗證：多層線性網路塌縮為單層
import numpy as np


def relu(x):
    # ReLU 活化函數：max(0, x)
    return np.maximum(0.0, x)


def staircase(x, M):
    # 用 M 段「斜坡加平台」階梯逼近目標函數
    # 每段：ReLU(x - t_k) - ReLU(x - t_{k+1}) 的縮放版
    # 具體做法：在節點 t_k 處放 ReLU 基底，用相鄰節點斜率差當係數
    edges = np.linspace(0, np.pi, M + 1)   # 分段邊界
    h = edges[1] - edges[0]                # 段寬
    y = np.zeros_like(x)
    # 節點上的目標值 g(t_k)
    g = np.sin(edges)
    # 分段線性插值的 ReLU 基底表示（telescoping）：
    # f(x) = g_0 + c_0 ReLU(x - t_0) + sum_{k=1}^{M-1} c_k ReLU(x - t_k) - s_{M-1} ReLU(x - t_M)
    # 其中 s_k 是第 k 段斜率，c_k = s_k - s_{k-1}（相鄰段斜率差，c_0 = s_0），
    # 這樣第 k 段上的總斜率 = sum_{j<=k} c_j = s_k；最後一項把尾巴截平成平台
    slopes = np.diff(g) / h                      # 各段斜率 s_k
    coef = np.diff(np.concatenate([[0.0], slopes]))  # c_k = s_k - s_{k-1}
    y = g[0] + np.zeros_like(x)
    for k in range(M):
        y = y + coef[k] * relu(x - edges[k])
    y = y - slopes[-1] * relu(x - edges[M])
    return y


print("=== ReLU 階梯逼近 sin(x)，[0, pi] 上的最大誤差 ===")
x = np.linspace(0, np.pi, 2000)
for M in [1, 2, 4, 8, 16, 32, 64]:
    err = np.max(np.abs(staircase(x, M) - np.sin(x)))
    print(f"M = {M:3d} 段階梯，最大誤差 = {err:.6f}")

print()
print("=== 習題 1 驗證：兩個 ReLU 表達 |x| ===")
xs = np.array([-2.0, -0.5, 0.0, 0.5, 2.0])
abs_relu = relu(xs) + relu(-xs)
print("x        =", xs)
print("ReLU表達 =", abs_relu)
print("|x|      =", np.abs(xs))
print("最大誤差 =", np.max(np.abs(abs_relu - np.abs(xs))))

print()
print("=== 多層線性網路塌縮驗證（無活化函數）===")
rng = np.random.default_rng(0)
x = rng.normal(size=(5, 1))
W1 = rng.normal(size=(4, 5))
W2 = rng.normal(size=(3, 4))
two_layer = W2 @ (W1 @ x)          # 兩層線性
one_layer = (W2 @ W1) @ x          # 等價單層 W' = W2 W1
print("兩層與單層輸出最大差異 =", np.max(np.abs(two_layer - one_layer)))
print("（機器精度級，證明無活化函數時深層只是白疊）")
