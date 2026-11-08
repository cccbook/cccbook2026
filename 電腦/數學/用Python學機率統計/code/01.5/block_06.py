# 01.5-用rstatistics看資料
# 由 01.5-用rstatistics看資料.md 抽出：以 python3.14 + PYTHONPATH 指向 rstatistics 執行

g = r.set_seed(2026)
w = [round(v, 1) for v in g.rnorm(28, mean=62, sd=8)]
w2 = w + [130.0]
print(r.mean(w), r.sd(w))
print(r.mean(w2), r.sd(w2))
print(r.median(w2), r.mad(w2))
st = r.boxplot_stats(w2)
print(st.out)
