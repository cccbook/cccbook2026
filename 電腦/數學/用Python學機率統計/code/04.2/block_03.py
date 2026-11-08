# 04.2-均勻分配
# 由 04.2-均勻分配.md 抽出：以 python3.14 + PYTHONPATH 指向 rstatistics 執行

import math
import rstatistics as r

g = r.set_seed(42)
u = g.runif(5000)
x = [-math.log(v) for v in u]        # 反變換法造出 Exp(1)

g2 = r.Graphics(width=5.5, height=4.2)
g2.hist(x, main="-ln(U) 的直方圖 vs 指數密度", xlab="x", ylab="密度", freq=False, breaks="FD", xlim=[0, 7])
g2.curve("dexp", 0, 7, col="darkred", lwd=2)
g2.save(\"img/04.2-inverse-transform.svg\")
