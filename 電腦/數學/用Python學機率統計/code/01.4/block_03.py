# 01.4-五數摘要與箱型圖
# 由 01.4-五數摘要與箱型圖.md 抽出：以 python3.14 + PYTHONPATH 指向 rstatistics 執行

q1, q3 = r.quantile(x, [0.25])[0], r.quantile(x, [0.75])[0]
iqr = q3 - q1
lo, hi = q1 - 1.5 * iqr, q3 + 1.5 * iqr
print(q1, q3, iqr, lo, hi)
print(sorted(v for v in x if v < lo or v > hi))
inl = sorted(v for v in x if lo <= v <= hi)
print(inl[0], inl[-1])
