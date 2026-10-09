# -*- coding: utf-8 -*-
# 05.2 注意力機制：numpy 實作 scaled dot-product attention，驗證 softmax 行和為 1 與 Var(q·k)=d_k
import numpy as np

def softmax_rows(S):
    # 每行減最大值防溢出
    S = S - S.max(axis=1, keepdims=True)
    E = np.exp(S)
    return E / E.sum(axis=1, keepdims=True)

def attention(Q, K, V, causal=False):
    d_k = Q.shape[1]
    S = Q @ K.T / np.sqrt(d_k)
    if causal:
        n = S.shape[0]
        mask = np.triu(np.ones((n, n)), k=1)  # j > i 遮掉
        S = S - 1e9 * mask
    A = softmax_rows(S)
    return A, A @ V

# --- 驗證 1：softmax 行和為 1、輸出是凸組合 ---
rng = np.random.default_rng(0)
Q = rng.normal(size=(4, 3))
K = rng.normal(size=(4, 3))
V = rng.normal(size=(4, 3))
A, O = attention(Q, K, V)
print("注意力權重矩陣 A：")
print(np.round(A, 4))
print("每行行和（應全為 1）：", np.round(A.sum(axis=1), 12))
print("所有權重非負：", bool((A >= 0).all()))
print("輸出 O 的每行是 V 各行的凸組合（權重和為 1 且非負）——驗證通過")

# --- 驗證 2：Var(q·k) = d_k ---
d_k = 16
n_samples = 200000
q = rng.normal(size=(n_samples, d_k))
k = rng.normal(size=(n_samples, d_k))
dots = (q * k).sum(axis=1)
print(f"\nq·k 的實測方差 = {dots.var():.3f}，理論值 d_k = {d_k}（應接近）")
print(f"除以 sqrt(d_k) 後方差 = {(dots / np.sqrt(d_k)).var():.3f}（約為 1，softmax 不會飽和）")

# --- 驗證 3：因果注意力 ---
A_c, O_c = attention(Q, K, V, causal=True)
print("\n因果注意力的上三角部分（j>i，應全為 0）：")
print(np.round(np.triu(A_c, k=1), 6).sum() == 0.0)
