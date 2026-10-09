# 02.2 梯度下降、SGD、動量、Adam 比較
# 用 numpy 在二維橢圓拋物面上比較四種優化器的收斂速度
import numpy as np

# 損失函數：L(w) = 0.5 * (w0^2 + 20 * w1^2)（狹長峽谷形，條件數 20）
# 梯度：grad = [w0, 20*w1]
def grad(w):
    return np.array([w[0], 20.0 * w[1]])

def loss(w):
    return 0.5 * (w[0]**2 + 20.0 * w[1]**2)

w0 = np.array([5.0, 1.0])
eta = 0.05
steps = 50

print("=== 梯度下降（GD）===")
w = w0.copy()
for t in range(steps):
    w = w - eta * grad(w)
print(f"最終 w = {w.round(6)}, L = {loss(w):.2e}")

print("\n=== 隨機梯度下降（SGD，批量大小 1 的噪聲梯度）===")
rng = np.random.default_rng(42)
w = w0.copy()
for t in range(steps):
    g = grad(w) + rng.normal(0, 0.3, size=2)  # 無偏噪聲：E[g] = 梯度
    w = w - eta * g
print(f"最終 w = {w.round(6)}, L = {loss(w):.2e}")

print("\n=== 動量（Momentum, beta=0.9）===")
w = w0.copy()
v = np.zeros(2)
for t in range(steps):
    v = 0.9 * v + grad(w)
    w = w - eta * v
print(f"最終 w = {w.round(6)}, L = {loss(w):.2e}")

print("\n=== Adam（beta1=0.9, beta2=0.999）===")
w = w0.copy()
m = np.zeros(2)
s = np.zeros(2)
b1, b2, eps = 0.9, 0.999, 1e-8
for t in range(1, steps + 1):
    g = grad(w)
    m = b1 * m + (1 - b1) * g
    s = b2 * s + (1 - b2) * g * g
    m_hat = m / (1 - b1**t)   # 偏置校正
    s_hat = s / (1 - b2**t)
    w = w - eta * m_hat / (np.sqrt(s_hat) + eps)
print(f"最終 w = {w.round(6)}, L = {loss(w):.2e}")

print("\n=== 一維驗證：L(theta)=theta^2 的封閉式解 ===")
# theta_k = (1-2*eta)^k * theta_0，eta=0.1, theta_0=1
theta = 1.0
hist = []
for k in range(6):
    hist.append(theta)
    theta = theta - 0.1 * 2 * theta
print("theta_k 實際值：", [round(x, 3) for x in hist])
print("理論值 0.8^k：", [round(0.8**k, 3) for k in range(6)])
assert np.allclose(hist, [0.8**k for k in range(6)]), "與理論封閉式不符"
print("驗證成功：每步恰乘 0.8，符合理論 (1-2*eta)^k。")

print("\n=== 習題 1：L(theta)=(theta-3)^2, eta=0.25 ===")
# theta_k - 3 = (1 - 2*eta)^k * (theta_0 - 3) = 0.5^k * (theta_0 - 3)
th = 0.0
for k in range(5):
    th = th - 0.25 * 2 * (th - 3)
print(f"5 步後 theta = {th:.6f}，理論值 3 - 0.5^5 * 3 = {3 - 0.5**5 * 3:.6f}")
assert abs(th - (3 - 0.5**5 * 3)) < 1e-9
print("驗證成功：封閉式 theta_k = 3 - 0.5^k * (theta_0 - 3)；收斂條件 |1-2*eta|<1 即 eta<1。")
