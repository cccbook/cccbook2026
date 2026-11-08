# 08.1-為什麼需要非參數方法
# 由 08.1-為什麼需要非參數方法.md 抽出：以 python3.14 + PYTHONPATH 指向 rstatistics 執行

import rstatistics as r

xs = [(-5 + 10 * i / 200) for i in range(201)]
yn = [r.dnorm(x) for x in xs]
yc = [r.dcauchy(x) for x in xs]
g = r.Graphics(width=7.0, height=4.5)
g.plot(xs, yn)
g.lines(xs, yc, "red")
g.legend(-4.5, 0.42, ["常態 N(0,1)", "柯西 Cauchy(0,1)"])
g.save(\"img/08.1-tails.svg\")
