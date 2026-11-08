# 04.3-指數與Gamma分配
# 由 04.3-指數與Gamma分配.md 抽出：以 python3.14 + PYTHONPATH 指向 rstatistics 執行

# 排隊例子：服務時間 Exp(0.5)（平均 2 分鐘），前 8 位客人
g = r.set_seed(101)
t = g.rexp(8, 0.5)
print([round(v, 2) for v in t])
print(r.mean(t))                  # 理論 1/0.5 = 2
print(r.pexp(2.0, 0.5))           # P(一位客人 2 分鐘內服務完)
