# 01.1-從母體到樣本
# 由 01.1-從母體到樣本.md 抽出：以 python3.14 + PYTHONPATH 指向 rstatistics 執行

# --- 區塊 1 ---
import rstatistics as r

g = r.set_seed(42)
pop = g.rnorm(10000, mean=170.0, sd=7.0)   # 上帝視角：整個母體

print(r.mean(pop), r.sd(pop))


# --- 區塊 2 ---
g = r.set_seed(42)
means = [r.mean(g.rnorm(30, mean=170.0, sd=7.0)) for _ in range(1000)]

print(r.mean(means))                  # 1000 個 x̄ 的平均
print(r.sd(means))                    # x̄ 的波動幅度
print(7.0 / (30 ** 0.5))              # 理論值：σ/√n
print(min(means), max(means))         # 最倒霉與最幸運的樣本


# --- 區塊 3 ---
g2 = r.Graphics(width=7.0, height=4.5)
g2.hist(means, main="1000 個樣本平均數的分布", xlab="樣本平均數 (cm)")
g2.save("img/sampling_dist.svg")


# --- 區塊 4 ---
for n in (5, 30, 300):
    g3 = r.RNG(1)                       # 每種 n 用同一顆種子，公平比較
    ms = [r.mean(g3.rnorm(n, mean=170.0, sd=7.0)) for _ in range(1000)]
    print(n, r.mean(ms), r.sd(ms), 7.0 / (n ** 0.5))


# --- 區塊 5 ---
g4 = r.set_seed(5)
p_hat = [x / 1000 for x in g4.rbinom(1000, 1000, 0.5)]   # n=1000 的民調，真支持度 50%
print(r.mean(p_hat), r.sd(p_hat), (0.25 / 1000) ** 0.5)


# --- 區塊 6 ---
g5 = r.set_seed(42)
print(g5.runif(2))
