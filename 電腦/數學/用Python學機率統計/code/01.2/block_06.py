# 01.2-集中趨勢
# 由 01.2-集中趨勢.md 抽出：以 python3.14 + PYTHONPATH 指向 rstatistics 執行

g = r.Graphics(width=7.0, height=4.5)
cs = [x * 1.0 for x in range(25, 75)]
g.plot(cs, [sum((xi - c) ** 2 for xi in w) / 10000 for c in cs])
g.lines(cs, [sum(abs(xi - c) for xi in w) / 100 for c in cs])
g.title("兩種誤差總和的形狀（縮放後）", )
g.save(\"img/err_curves.svg\")
