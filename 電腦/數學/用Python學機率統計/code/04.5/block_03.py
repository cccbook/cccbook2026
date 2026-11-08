# 04.5-Beta分配與組合的分布
# 由 04.5-Beta分配與組合的分布.md 抽出：以 python3.14 + PYTHONPATH 指向 rstatistics 執行

import rstatistics as r

# 數值積分（梯形法）：∫ dbeta(x; 2, 5) dx 應為 1
def trap(f, a, b, n):
    h = (b - a) / n
    s = 0.5 * (f(a) + f(b))
    for i in range(1, n):
        s += f(a + i * h)
    return s * h

f = lambda x: r.dbeta(x, 2.0, 5.0)
print(trap(f, 0.0, 1.0, 1000))
print(trap(f, 0.0, 1.0, 20))
