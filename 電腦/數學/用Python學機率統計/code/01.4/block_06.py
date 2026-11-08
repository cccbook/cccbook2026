# 01.4-五數摘要與箱型圖
# 由 01.4-五數摘要與箱型圖.md 抽出：以 python3.14 + PYTHONPATH 指向 rstatistics 執行

import rstatistics as r

g = r.set_seed(21)
day = [round(v, 1) for v in g.rnorm(30, 100, 3)]
night = [round(v, 1) for v in g.rnorm(30, 104, 3)]
for name, d in (("白班", day), ("夜班", night)):
    st = r.boxplot_stats(d)
    print(name, st.stats, "out:", st.out)
