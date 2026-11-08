# 10.3-箱型圖Q-Q圖與ECDF
# 由 10.3-箱型圖Q-Q圖與ECDF.md 抽出：以 python3.14 + PYTHONPATH 指向 rstatistics 執行

import rstatistics as r

g = r.set_seed(11)
norm = [round(v, 4) for v in g.rnorm(60, 0.0, 1.0)]

gr = r.Graphics(width=6.0, height=5.0)
e = gr.ecdf(norm, main="g.ecdf 畫出的經驗分布函數", xlab="x", ylab="F(x)")
print("e =", e)
print("e.n =", e.n)
print("e.x[:5] =", [round(v, 4) for v in e.x[:5]])
print("e.y[:5] =", [round(v, 4) for v in e.y[:5]])
print("e.x[-3:] =", [round(v, 4) for v in e.x[-3:]])
print("e.y[-3:] =", [round(v, 4) for v in e.y[-3:]])
