# 10.4-函數曲線柱狀圖與圖例
# 由 10.4-函數曲線柱狀圖與圖例.md 抽出：以 python3.14 + PYTHONPATH 指向 rstatistics 執行

import rstatistics as r

print("=== curve 的取樣 ===")
xs = []
ys = []
for i in range(101):
    xs.append(-3.0 + 6.0 * i / 100.0)
    ys.append(r.dnorm(xs[-1], 0.0, 1.0))
print("curve 的第一個點:", round(xs[0], 3), round(ys[0], 6))
print("curve 的中間點:", round(xs[50], 3), round(ys[50], 6))
print("curve 的最後一個點:", round(xs[-1], 3), round(ys[-1], 6))
print("dx =", round(xs[1] - xs[0], 4))
print("理論峰值 dnorm(0) =", round(r.dnorm(0.0), 6))
