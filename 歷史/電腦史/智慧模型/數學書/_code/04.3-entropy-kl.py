# -*- coding: utf-8 -*-
# 04.3 熵、KL 散度與資訊理論：硬幣範例、Gibbs 不等式、PPL 驗證
# 只用 numpy
import numpy as np


def entropy(p, base=2.0):
    # Shannon 熵 H(p) = -sum p log p（base=2 得 bit，=e 得 nat）
    p = np.asarray(p, dtype=float)
    p = p[p > 0]  # 去掉零機率（0 log 0 := 0）
    log = np.log2 if base == 2.0 else np.log
    return float(-np.sum(p * log(p)))


def cross_entropy(p, q, base=2.0):
    # 交叉熵 H(p,q) = -sum p log q
    p, q = np.asarray(p, float), np.asarray(q, float)
    log = np.log2 if base == 2.0 else np.log
    return float(-np.sum(p * log(q)))


def kl(p, q, base=2.0):
    # KL 散度 D(p||q) = H(p,q) - H(p)
    return cross_entropy(p, q, base) - entropy(p, base)

# --- 1. 章節範例：公正硬幣 p=(0.5,0.5)，模型 q=(0.9,0.1) ---
p = [0.5, 0.5]
q = [0.9, 0.1]
H = entropy(p)
Hpq = cross_entropy(p, q)
D = kl(p, q)
print("=== 章節範例（bit）===")
print(f"H(p) = {H:.4f} bit（公正硬幣最難猜）")
print(f"H(p,q) = {Hpq:.4f} bit")
print(f"D(p||q) = {D:.4f} bit（= H(p,q) - H(p)，多花的驚訝量）")
assert abs(D - (Hpq - H)) < 1e-12
assert D >= 0  # Gibbs 不等式

# --- 2. 習題 2：反向 KL 不對稱 ---
D_rev = kl(q, p)
print("\n=== 習題 2：KL 不對稱 ===")
print(f"D(p||q) = {D:.4f} bit")
print(f"D(q||p) = {D_rev:.4f} bit")
print(f"兩者不等（{D:.4f} != {D_rev:.4f}）——KL 不是距離，是單向散度")

# --- 3. 習題 1：均勻分布熵最大（n=4，隨機抽 5 個分布比較） ---
rng = np.random.default_rng(1)
print("\n=== 習題 1：均勻分布熵最大（n=4，上限 log2(4)=2 bit）===")
u = np.ones(4) / 4
print(f"均勻分布 H = {entropy(u):.4f} bit")
for i in range(5):
    r = rng.dirichlet(np.ones(4))
    print(f"隨機分布 {np.round(r, 3)} H = {entropy(r):.4f} bit（<= 2）")
    assert entropy(r) <= np.log2(4) + 1e-12

# --- 4. 習題 3：交叉熵 = 負對數概似；PPL = exp(H) ---
# 玩具：真實單點分布 p=(1,0)（觀測到第一個結果），模型 q=(0.6,0.4)
print("\n=== 習題 3：交叉熵 = 負對數概似；困惑度 ===")
p_onehot, q_model = [1.0, 0.0], [0.6, 0.4]
ce = cross_entropy(p_onehot, q_model, base=np.e)
print(f"交叉熵 H(p,q) = {ce:.4f} nat；-log(0.6) = {-np.log(0.6):.4f} nat（兩者相同）")
assert abs(ce - (-np.log(0.6))) < 1e-12
for H_nat in [2.0, 0.8109]:
    print(f"H = {H_nat} nat -> PPL = exp(H) = {np.exp(H_nat):.4f}")
print("PPL = 7.3891 表示每步約 7.4 個等機率選項的不確定性")
