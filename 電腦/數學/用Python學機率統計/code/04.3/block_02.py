# 04.3-指數與Gamma分配
# 由 04.3-指數與Gamma分配.md 抽出：以 python3.14 + PYTHONPATH 指向 rstatistics 執行

# Gamma：n 個 Exp(lambda) 之和 ~ Gamma(n, lambda)
print(r.dgamma(1.0, 1.0, 1.0))     # Gamma(1,1) = Exp(1)
print(r.dgamma(2.0, 2.0, 1.0))     # Gamma(2,1) 密度 x e^-x
print(r.pgamma(2.0, 3.0, 1.0))     # P(Gamma(3,1) <= 2)

# 模擬驗證：5 個 Exp(1) 相加 ~ Gamma(5, 1)
g = r.set_seed(42)
s = []
for _ in range(2000):
    e = g.rexp(5, 1.0)
    s.append(sum(e))
print(r.mean(s))                   # 理論 5
print(r.sd(s))                     # 理論 sqrt(5) ≈ 2.236
