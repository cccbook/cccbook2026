# 01.1-從母體到樣本
# 由 01.1-從母體到樣本.md 抽出：以 python3.14 + PYTHONPATH 指向 rstatistics 執行

g4 = r.set_seed(5)
p_hat = [x / 1000 for x in g4.rbinom(1000, 1000, 0.5)]   # n=1000 的民調，真支持度 50%
print(r.mean(p_hat), r.sd(p_hat), (0.25 / 1000) ** 0.5)
