# 01.4-五數摘要與箱型圖
# 由 01.4-五數摘要與箱型圖.md 抽出：以 python3.14 + PYTHONPATH 指向 rstatistics 執行

st = r.boxplot_stats(x)
print(st.stats)      # [鬚下, Q1, 中位數, Q3, 鬚上]
print(st.out)        # 離群值
