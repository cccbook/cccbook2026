# 01.2 Hebb 律與聯想記憶驗證
# 用 numpy 實現外積儲存（Hebb 律），儲存模式後輸入殘缺版回憶
# 並驗證正交模式雜訊項為零
import numpy as np

def hebb_store(patterns, eta=1.0):
    """Hebb 律：W = eta * sum 外積"""
    n = patterns[0].shape[0]
    W = np.zeros((n, n))
    for x in patterns:
        W += eta * np.outer(x, x)
    return W

def recall(W, v, steps=5):
    """回憶：反覆套用 W 並取符號，直到穩定"""
    v = v.astype(float)
    for _ in range(steps):
        v_new = np.sign(W @ v)
        v_new[v_new == 0] = 1
        if np.array_equal(v_new, v):
            break
        v = v_new
    return v

print("=== 範例：儲存兩個模式（章節內的例子）===")
x1 = np.array([1, 1, -1])
x2 = np.array([-1, 1, 1])
W = hebb_store([x1, x2])
print("W =\n", W)
v = np.array([1, 0, -1])  # 殘缺版（第二位遺失）
r = recall(W, v)
print(f"輸入殘缺向量 {v}，回憶出 {r}")
assert np.array_equal(r, x1), "回憶失敗"
print("回憶成功：遺失的位元被補回，想起模式一。")

print("\n=== 習題 1：儲存 (1,-1,1) 與 (1,1,-1) ===")
p1 = np.array([1, -1, 1])
p2 = np.array([1, 1, -1])
W2 = hebb_store([p1, p2])
print("W =\n", W2)
v2 = np.array([0, -1, 1])  # 第一位未知
r2 = recall(W2, v2)
print(f"輸入 {v2}，回憶出 {r2}")
target = p1 if np.array_equal(r2, p1) else p2
print(f"回憶出的模式：{target}")

print("\n=== 習題 2：正交模式的雜訊項恰為零 ===")
# 構造四個兩兩正交的 ±1 模式（Hadamard 列）
H = np.array([[ 1,  1,  1,  1],
              [ 1,  1, -1, -1],
              [ 1, -1,  1, -1],
              [ 1, -1, -1,  1]])
W3 = hebb_store(list(H))
print("兩兩正交內積矩陣 H H^T / n =\n", H @ H.T / 4)
# 驗證：W x^(nu) = n x^(nu)，雜訊項為零
for i in range(4):
    Wx = W3 @ H[i]
    assert np.allclose(Wx, 4 * H[i]), "正交性雜訊不為零"
print("驗證成功：對每個模式 W x = n·x，雜訊項（交叉干涉）恰為零。")
