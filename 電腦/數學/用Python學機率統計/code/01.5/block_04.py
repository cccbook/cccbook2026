# 01.5-用rstatistics看資料
# 由 01.5-用rstatistics看資料.md 抽出：以 python3.14 + PYTHONPATH 指向 rstatistics 執行

cat = ["偏輕" if x < 56 else ("標準" if x <= 68 else "偏重") for x in w]
print(r.table(cat))
