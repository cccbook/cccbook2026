# 04.3-指數與Gamma分配
# 由 04.3-指數與Gamma分配.md 抽出：以 python3.14 + PYTHONPATH 指向 rstatistics 執行

import rstatistics as r

# 指數分配：r.dexp / r.pexp / r.qexp
print(r.dexp(1.0))                 # lambda=1，f(1) = e^-1
print(r.dexp(1.0, 2.0))            # lambda=2
print(r.pexp(3.0))                 # P(X<=3) = 1 - e^-3
print(r.qexp(0.5, 0.5))            # 中位數 = ln(2)/0.5

# 無記憶性：P(X>5) vs P(X>3+2 | X>3)
print(r.pexp(2.0, lower_tail=False))                     # P(X>2)
print(r.pexp(5.0, lower_tail=False) / r.pexp(3.0, lower_tail=False))  # P(X>5)/P(X>3)
