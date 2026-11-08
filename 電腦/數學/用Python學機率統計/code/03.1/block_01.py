# 03.1-伯努利試驗與二項分配
# 由 03.1-伯努利試驗與二項分配.md 抽出：以 python3.14 + PYTHONPATH 指向 rstatistics 執行

import rstatistics as r

# 丟 10 次公正銅板，各種正面次數的機率
pmf = [r.dbinom(k, size=10, prob=0.5) for k in range(11)]
print([round(x, 4) for x in pmf])
