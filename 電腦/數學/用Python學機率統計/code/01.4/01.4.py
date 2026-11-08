# 01.4-五數摘要與箱型圖
# 由 01.4-五數摘要與箱型圖.md 抽出：以 python3.14 + PYTHONPATH 指向 rstatistics 執行

# --- 區塊 1 ---
import rstatistics as r

x = [97.0, 100.1, 92.4, 93.2, 105.9, 95.3, 106.6, 103.1, 99.8, 95.0,
     95.9, 98.3, 92.3, 98.7, 94.3, 140.0, 62.0]

print(r.fivenum(x))
print(r.quantile(x, [0.25, 0.5, 0.75]))
print(r.summary(x))


# --- 區塊 2 ---
y = [97.0, 100.1, 92.4, 93.2, 105.9, 95.3, 106.6, 103.1]

print(r.fivenum(y))
print(r.quantile(y, [0.25, 0.5, 0.75], type=7))


# --- 區塊 3 ---
q1, q3 = r.quantile(x, [0.25])[0], r.quantile(x, [0.75])[0]
iqr = q3 - q1
lo, hi = q1 - 1.5 * iqr, q3 + 1.5 * iqr
print(q1, q3, iqr, lo, hi)
print(sorted(v for v in x if v < lo or v > hi))
inl = sorted(v for v in x if lo <= v <= hi)
print(inl[0], inl[-1])


# --- 區塊 4 ---
st = r.boxplot_stats(x)
print(st.stats)      # [鬚下, Q1, 中位數, Q3, 鬚上]
print(st.out)        # 離群值


# --- 區塊 5 ---
g = r.Graphics(width=6.0, height=4.0)
g.boxplot(x, main="產品尺寸 (mm)", ylab="mm")
g.save("img/box_product.svg")


# --- 區塊 6 ---
import rstatistics as r

g = r.set_seed(21)
day = [round(v, 1) for v in g.rnorm(30, 100, 3)]
night = [round(v, 1) for v in g.rnorm(30, 104, 3)]
for name, d in (("白班", day), ("夜班", night)):
    st = r.boxplot_stats(d)
    print(name, st.stats, "out:", st.out)
