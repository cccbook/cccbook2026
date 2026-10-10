# 07.1 兩狀態迷宮價值迭代收斂驗證
# 驗證壓縮映射：每步誤差應乘上 gamma
# 只用 numpy

import numpy as np

gamma = 0.9

# 狀態 A=0, B=1；動作「走」：A->B 得 r=1，B->A 得 r=0
# 貝爾曼期望算子 T^pi（pi 恆走）：
#   V(A) <- 1 + gamma * V(B)
#   V(B) <- 0 + gamma * V(A)
T = lambda V: np.array([1 + gamma * V[1], 0 + gamma * V[0]])

# 解析解：V(A) = 1/(1-gamma^2), V(B) = gamma/(1-gamma^2)
V_star = np.array([1 / (1 - gamma**2), gamma / (1 - gamma**2)])
print("解析解        V* =", np.round(V_star, 4))

# 價值迭代 V_{k+1} = T V_k，從 V0 = 0 出發
V = np.zeros(2)
print("\n價值迭代（V0 = 0）：")
prev_err = None
for k in range(1, 13):
    V = T(V)
    err = np.max(np.abs(V - V_star))
    ratio = err / prev_err if prev_err else float("nan")
    print(f"k={k:2d}  V = {np.round(V, 4)}  誤差={err:.6f}  誤差比={ratio:.4f}")
    prev_err = err

print("\n結論：誤差比趨近 gamma =", gamma, "——壓縮映射的幾何收斂。")

# 順帶驗證習題 1：gamma = 0.5 時的前三步
gamma = 0.5
V = np.zeros(2)
print("\n習題（gamma = 0.5）前三步：")
for k in range(1, 4):
    V = np.array([1 + gamma * V[1], gamma * V[0]])
    print(f"k={k}  V = {np.round(V, 4)}  （解析解 {1/(1-gamma**2):.4f}, {gamma/(1-gamma**2):.4f}）")
