# -*- coding: utf-8 -*-
# 05.3 RoPE：二維旋轉矩陣，驗證內積只依賴相對位置、旋轉矩陣正交性
import numpy as np

def rot(phi):
    # 二維旋轉矩陣 R(phi)
    c, s = np.cos(phi), np.sin(phi)
    return np.array([[c, -s],
                     [s,  c]])

def apply_rope_2d(v, pos, theta):
    # d=2：位置 pos 的向量旋轉 pos*theta
    return rot(pos * theta) @ v

theta = np.pi / 6  # 30 度
v = np.array([1.0, 0.0])  # 詞向量

# --- 驗證 1：旋轉矩陣正交性 R^T R = I ---
for phi in [0.3, 1.0, 2.5]:
    R = rot(phi)
    print(f"phi={phi}: R^T R 與 I 的最大偏差 = {np.abs(R.T @ R - np.eye(2)).max():.2e}")

# --- 驗證 2：內積只依賴相對位置 m - n ---
print("\n同一對詞放在不同絕對位置（相對位置固定為 2）：")
for m in [0, 1, 5, 10]:
    n = m + 2
    q = apply_rope_2d(v, m, theta)
    k = apply_rope_2d(v, n, theta)
    print(f"  m={m}, n={n}: (R q)·(R k) = {q @ k:.6f}")
print("內積不隨絕對位置改變——只依賴相對位置 n - m")

# --- 驗證 3：內積 = cos(角度差) ---
m, n = 1, 3
q = apply_rope_2d(v, m, theta)
k = apply_rope_2d(v, n, theta)
rel = (n - m) * theta
print(f"\nm=1, n=3（角度差 60 度）：")
print(f"  直接旋轉法：(R q)·(R k) = {q @ k:.6f}")
print(f"  相對位置法：v·R({rel:.4f}) v = cos(60°) = {v @ rot(rel) @ v:.6f}")
print("兩法一致，且等於 cos(角度差)——RoPE 的本質")
