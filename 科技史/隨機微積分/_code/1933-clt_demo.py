#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""1933 CLT 對應 wiki 說明
對應 wiki：1933 年 Kolmogorov 公理化與中央極限定理 (Lindeberg-Levy)。
Exp(1) 母體 mean=1 var=1，標準化樣本均值 Z = sqrt(n)*(Xbar-1) -> N(0,1)。
本程式 n=500、2 萬次重複，驗證偏度 |skew|<0.1 且 P(|Z|<1.96)≈0.95 誤差<0.01。
規範：只用 numpy，固定種子，不畫圖只印數字，結尾印 VERIFY 並用 assert 把關。
"""
import numpy as np

np.random.seed(0)

n = 500
M = 20000

# Exp(1) 抽樣：(M, n) 矩陣，約 1000 萬個樣本
X = np.random.exponential(scale=1.0, size=(M, n))
Xbar = np.mean(X, axis=1)
Z = np.sqrt(n) * (Xbar - 1.0)

zmean = float(np.mean(Z))
zstd = float(np.std(Z))
skew = float(np.mean(((Z - zmean) / zstd) ** 3))
cover = float(np.mean(np.abs(Z) < 1.96))

print(f"CLT Exp(1) n={n} M={M}")
print(f"Z mean={zmean:.5f} std={zstd:.5f} skew={skew:.5f}")
print(f"P(|Z|<1.96)={cover:.5f} (theory 0.95)")

assert abs(skew) < 0.1, f"|skew|={abs(skew)} >= 0.1"
assert abs(cover - 0.95) < 0.01, f"|cover-0.95|={abs(cover-0.95)} >= 0.01"
print(f"VERIFY 1933 CLT: |skew|={abs(skew):.4f}<0.1 cover={cover:.4f} err={abs(cover-0.95):.4f}<0.01 PASS")
