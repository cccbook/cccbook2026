# 01.5-用rstatistics看資料
# 由 01.5-用rstatistics看資料.md 抽出：以 python3.14 + PYTHONPATH 指向 rstatistics 執行

# --- 區塊 1 ---
import rstatistics as r

g = r.set_seed(2026)
w = [round(v, 1) for v in g.rnorm(28, mean=62, sd=8)]
print(w)


# --- 區塊 2 ---
print(r.summary(w))


# --- 區塊 3 ---
g1 = r.Graphics(width=7.0, height=4.5)
g1.hist(w, main="班上體重分布", xlab="體重 (kg)")
g1.save("img/w_hist.svg")

g2 = r.Graphics(width=7.0, height=4.5)
g2.boxplot(w, main="班上體重箱型圖", ylab="kg")
g2.save("img/w_box.svg")


# --- 區塊 4 ---
cat = ["偏輕" if x < 56 else ("標準" if x <= 68 else "偏重") for x in w]
print(r.table(cat))


# --- 區塊 5 ---
print(r.rank(w)[:8])
z = r.scale(w)
print([round(v, 3) for v in z[:8]])
print(r.mean(z), r.sd(z))


# --- 區塊 6 ---
g = r.set_seed(2026)
w = [round(v, 1) for v in g.rnorm(28, mean=62, sd=8)]
w2 = w + [130.0]
print(r.mean(w), r.sd(w))
print(r.mean(w2), r.sd(w2))
print(r.median(w2), r.mad(w2))
st = r.boxplot_stats(w2)
print(st.out)
