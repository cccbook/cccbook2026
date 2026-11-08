# 02.1-隨機試驗與樣本空間
# 由 02.1-隨機試驗與樣本空間.md 抽出：以 python3.14 + PYTHONPATH 指向 rstatistics 執行

# --- 區塊 1 ---
from itertools import product

# 樣本空間：兩顆骰子（區分先後，共 36 個結果）
S = list(product(range(1, 7), repeat=2))
print("樣本空間大小 |S| =", len(S))
print("前 6 個元素:", S[:6])

# 事件 A：點數和為 7
A = [(a, b) for (a, b) in S if a + b == 7]
print("A（和為7）:", A)

# 事件 B：至少一顆是 6
B = [(a, b) for (a, b) in S if a == 6 or b == 6]
print("B（含6）的元素個數:", len(B), "例:", B[:4])

def P(E):
    return len(E) / len(S)

print("P(A) =", P(A))
print("P(B) =", P(B))
print("P(A 和 B) =", P([e for e in S if e in A and e in B]))
print("P(A 或 B) =", P([e for e in S if e in A or e in B]))


# --- 區塊 2 ---
from itertools import product

# 比數 2:1，A 需再贏 1 局、B 需 2 局；每局 A 獲勝機率 1/2
wins = 0
total = 0
for games in product("AB", repeat=2):        # 最多再打 2 局的所有劇本
    a_wins = games.count("A")
    if a_wins >= 1:                          # A 先湊到 3 勝
        wins += 1
    total += 1
print(wins, "/", total, "=", wins / total)
