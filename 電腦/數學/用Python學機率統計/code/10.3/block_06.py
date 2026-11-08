# 10.3-箱型圖Q-Q圖與ECDF
# 由 10.3-箱型圖Q-Q圖與ECDF.md 抽出：以 python3.14 + PYTHONPATH 指向 rstatistics 執行

import rstatistics as r

g = r.set_seed(11)
norm = [round(v, 4) for v in g.rnorm(60, 0.0, 1.0)]
heavy = [round(v, 4) for v in g.rt(60, df=3)]

gr = r.Graphics(width=10.0, height=5.0, mfrow=[1, 2])

# 面板 1：常態
gr.qqnorm(norm, main="常態資料的 Q-Q 圖", xlab="理論分位數", ylab="樣本分位數")
gr.qqline(norm, col="red")

# 面板 2：重尾
gr.next_panel()
gr.qqnorm(heavy, main="重尾資料 (t, df=3) 的 Q-Q 圖", xlab="理論分位數", ylab="樣本分位數")
gr.qqline(heavy, col="red")

gr.save(\"img/10.3-qqnorm.svg\")
print("已存 10.3-qqnorm.svg")
