# -*- coding: utf-8 -*-
"""0230 Archimedes 夾擊 pi（對應 wiki：計算模擬學 / 阿基米德窮竭法求 pi）
圓半徑=1：內接正 n 邊形周長=2n·sin(pi/n)，外切正 n 邊形周長=2n·tan(pi/n)，
故下界 L=n·sin(pi/n) < pi < n·tan(pi/n)=上界 U。
取 n=6,12,24,48,96（倍增），驗證 n=96 時 3.1408 < pi < 3.1429。
只用 numpy，固定種子。
"""
import numpy as np

np.random.seed(0)

ns = [6, 12, 24, 48, 96]
print(f"{'n':>5} {'lower=n sin(pi/n)':>20} {'upper=n tan(pi/n)':>20} {'width':>12}")
results = {}
for n in ns:
    lower = n * np.sin(np.pi / n)
    upper = n * np.tan(np.pi / n)
    results[n] = (lower, upper)
    print(f"{n:>5d} {lower:>20.10f} {upper:>20.10f} {upper - lower:>12.2e}")

lo96, hi96 = results[96]
print(f"true pi = {np.pi:.10f}")
print(f"96邊: 下界={lo96:.6f} (理論下界→pi), 上界={hi96:.6f}")

# 驗證數字：理論值 vs 實測
ok_lo = lo96 > 3.1408
ok_hi = hi96 < 3.1429
ok_bracket = (lo96 < np.pi < hi96)
print(f"VERIFY lower96={lo96:.6f} (>3.1408? {ok_lo})")
print(f"VERIFY upper96={hi96:.6f} (<3.1429? {ok_hi})")
print(f"VERIFY bracket: {lo96:.6f} < pi={np.pi:.6f} < {hi96:.6f} ? {ok_bracket}")
assert ok_lo, f"下界不夠緊: {lo96}"
assert ok_hi, f"上界不夠緊: {hi96}"
assert ok_bracket, "pi 不在夾擊區間內"
print("PASS")
