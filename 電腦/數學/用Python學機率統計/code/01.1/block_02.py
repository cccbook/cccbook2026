# 01.1-從母體到樣本
# 由 01.1-從母體到樣本.md 抽出：以 python3.14 + PYTHONPATH 指向 rstatistics 執行

g = r.set_seed(42)
means = [r.mean(g.rnorm(30, mean=170.0, sd=7.0)) for _ in range(1000)]

print(r.mean(means))                  # 1000 個 x̄ 的平均
print(r.sd(means))                    # x̄ 的波動幅度
print(7.0 / (30 ** 0.5))              # 理論值：σ/√n
print(min(means), max(means))         # 最倒霉與最幸運的樣本
