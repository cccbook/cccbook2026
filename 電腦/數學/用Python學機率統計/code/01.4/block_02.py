# 01.4-五數摘要與箱型圖
# 由 01.4-五數摘要與箱型圖.md 抽出：以 python3.14 + PYTHONPATH 指向 rstatistics 執行

y = [97.0, 100.1, 92.4, 93.2, 105.9, 95.3, 106.6, 103.1]

print(r.fivenum(y))
print(r.quantile(y, [0.25, 0.5, 0.75], type=7))
