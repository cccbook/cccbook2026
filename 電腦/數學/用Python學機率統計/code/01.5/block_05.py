# 01.5-用rstatistics看資料
# 由 01.5-用rstatistics看資料.md 抽出：以 python3.14 + PYTHONPATH 指向 rstatistics 執行

print(r.rank(w)[:8])
z = r.scale(w)
print([round(v, 3) for v in z[:8]])
print(r.mean(z), r.sd(z))
