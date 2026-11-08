# 01.5-用rstatistics看資料
# 由 01.5-用rstatistics看資料.md 抽出：以 python3.14 + PYTHONPATH 指向 rstatistics 執行

g1 = r.Graphics(width=7.0, height=4.5)
g1.hist(w, main="班上體重分布", xlab="體重 (kg)")
g1.save(\"img/w_hist.svg\")

g2 = r.Graphics(width=7.0, height=4.5)
g2.boxplot(w, main="班上體重箱型圖", ylab="kg")
g2.save(\"img/w_box.svg\")
