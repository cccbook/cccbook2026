# -*- coding: utf-8 -*-
"""1768 Euler 法（對應 wiki：計算模擬學 / Euler 顯式法解 ODE）
解 y'=y, y(0)=1 到 t=1（真解 y=e^t, y(1)=e），步長 h=0.1/0.01/0.001，
顯式 Euler：y_{k+1} = y_k + h·y_k。整體誤差為 O(h)，故 h 縮小 10 倍、
誤差亦縮小約 10 倍。驗證相鄰誤差比約 10 倍（8~12 內）。
只用 numpy，固定種子。
"""
import numpy as np

np.random.seed(0)

exact = np.e  # y(1) = e
hs = [0.1, 0.01, 0.001]
errs = []
for h in hs:
    n = int(round(1.0 / h))
    y = 1.0
    for _ in range(n):
        y = y + h * y
    err = abs(y - exact)
    errs.append(err)
    print(f"h={h:<6g} steps={n:>5d} y1={y:.8f} exact={exact:.8f} err={err:.6e}")

r1 = errs[0] / errs[1]
r2 = errs[1] / errs[2]
print(f"err ratio (0.1/0.01)   = {r1:.4f} (理論 O(h) 比值≈10)")
print(f"err ratio (0.01/0.001) = {r2:.4f} (理論 O(h) 比值≈10)")

# 驗證數字：理論值 vs 實測
ok1 = 8.0 < r1 < 12.0
ok2 = 8.0 < r2 < 12.0
print(f"VERIFY r1={r1:.4f} (8<r1<12? {ok1}), VERIFY r2={r2:.4f} (8<r2<12? {ok2})")
assert ok1, f"誤差比 r1 偏離 O(h) 預期: {r1}"
assert ok2, f"誤差比 r2 偏離 O(h) 預期: {r2}"
print("PASS")
