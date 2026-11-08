# 01.4-五數摘要與箱型圖
# 由 01.4-五數摘要與箱型圖.md 抽出：以 python3.14 + PYTHONPATH 指向 rstatistics 執行

g = r.Graphics(width=6.0, height=4.0)
g.boxplot(x, main="產品尺寸 (mm)", ylab="mm")
g.save(\"img/box_product.svg\")
