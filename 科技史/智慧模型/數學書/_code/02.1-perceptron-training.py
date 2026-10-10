# 02.1 感知器訓練循環收斂驗證
# 用 numpy 實現感知器演算法，驗證 Novikoff 收斂定理的上界
import numpy as np

def perceptron_train(X, y, eta=1.0, max_updates=1000):
    """感知器演算法：w <- w + eta*y*x，僅當分錯時更新"""
    n = X.shape[1]
    w = np.zeros(n)
    b = 0.0
    updates = 0
    epochs = 0
    while epochs < max_updates:
        epochs += 1
        errors = 0
        for xi, yi in zip(X, y):
            if yi * (w @ xi + b) <= 0:   # 分錯
                w = w + eta * yi * xi
                b = b + eta * yi
                updates += 1
                errors += 1
        if errors == 0:
            return w, b, updates
    return w, b, updates

print("=== 章節範例：兩點分類 ===")
X = np.array([[1.0, 1.0], [-1.0, -1.0]])
y = np.array([1, -1])
w, b, k = perceptron_train(X, y)
print(f"收斂權重 w = {w}, b = {b}, 更新次數 k = {k}")
# 驗證 Novikoff 上界：R^2 / gamma^2
R = np.max(np.linalg.norm(X, axis=1))
w_star = np.array([1, 1]) / np.linalg.norm(np.array([1, 1]))  # 與章節範例一致的單位分離向量
gamma = min(yi * (w_star @ xi) for xi, yi in zip(X, y))
print(f"R = {R:.4f}, gamma = {gamma:.4f}, 上界 R^2/gamma^2 = {R**2/gamma**2:.0f}")
assert k <= R**2 / gamma**2, "違反 Novikoff 上界"
print("驗證成功：更新次數不超過理論上界。")

print("\n=== 習題 1：分類 {(2,1),+1}, {(-2,-1),-1} ===")
X2 = np.array([[2.0, 1.0], [-2.0, -1.0]])
y2 = np.array([1, -1])
w2, b2, k2 = perceptron_train(X2, y2)
print(f"收斂權重 w = {w2}, b = {b2}, 更新次數 k = {k2}")
print(f"分類檢查：sgn(w·(2,1)+b)={np.sign(w2@X2[0]+b2):+.0f}, sgn(w·(-2,-1)+b)={np.sign(w2@X2[1]+b2):+.0f}")

print("\n=== 較大資料集：15 個隨機可分點 ===")
rng = np.random.default_rng(0)
X3 = rng.uniform(-2, 2, size=(15, 2))
w_true = np.array([2.0, -1.0])
y3 = np.sign(X3 @ w_true).astype(int)
w3, b3, k3 = perceptron_train(X3, y3)
R3 = np.max(np.linalg.norm(X3, axis=1))
g3 = min(yi * (w_true @ xi) / np.linalg.norm(w_true) for xi, yi in zip(X3, y3))
print(f"收斂 w = {w3.round(3)}, b = {b3:.3f}, 更新次數 k = {k3}")
print(f"上界 R^2/gamma^2 = {(R3**2/g3**2):.1f}")
assert k3 <= R3**2 / g3**2, "違反 Novikoff 上界"
print("驗證成功：隨機可分資料的更新次數同樣不超過上界。")
