# 01.1-從母體到樣本
# 由 01.1-從母體到樣本.md 抽出：以 python3.14 + PYTHONPATH 指向 rstatistics 執行

for n in (5, 30, 300):
    g3 = r.RNG(1)                       # 每種 n 用同一顆種子，公平比較
    ms = [r.mean(g3.rnorm(n, mean=170.0, sd=7.0)) for _ in range(1000)]
    print(n, r.mean(ms), r.sd(ms), 7.0 / (n ** 0.5))
