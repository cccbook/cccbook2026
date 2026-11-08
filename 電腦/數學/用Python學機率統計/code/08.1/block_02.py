# 08.1-為什麼需要非參數方法
# 由 08.1-為什麼需要非參數方法.md 抽出：以 python3.14 + PYTHONPATH 指向 rstatistics 執行

import rstatistics as r

# 三種母體下，「平均數估計」的穩定性：各抽 500 次、n=30
g = r.set_seed(7)
for name, gen in [("常態 N(0,1)", g.rnorm),
                  ("柯西（重尾）", g.rcauchy),
                  ("常態 + 10% 汙染 N(0,1)/N(0,25)", None)]:
    means, meds = [], []
    for _ in range(500):
        if gen is not None:
            x = gen(30)
        else:
            x = g.rnorm(30)
            for i in range(30):
                if g.runif(1)[0] < 0.1:
                    x[i] = x[i] * 5
        means.append(r.mean(x))
        meds.append(r.median(x))
    print(f"{name}")
    print(f"  平均數估計的標準差: {r.sd(means):.3f}   中位數估計的標準差: {r.sd(meds):.3f}")
