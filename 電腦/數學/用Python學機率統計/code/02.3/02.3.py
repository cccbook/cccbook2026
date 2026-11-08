# 02.3-條件機率與乘法法則
# 由 02.3-條件機率與乘法法則.md 抽出：以 python3.14 + PYTHONPATH 指向 rstatistics 執行

# --- 區塊 1 ---
import rstatistics as r

# 乘法法則模擬：不回復抽牌，連抽兩張都是 A
g = r.set_seed(11)
N = 1_000_000
deck = ['A']*4 + ['notA']*48

hits_first = 0
hits_both = 0
for _ in range(N):
    c1, c2 = g.sample_from(deck, size=2, replace=False)
    if c1 == 'A':
        hits_first += 1
        if c2 == 'A':
            hits_both += 1

p_first = hits_first / N
p_both = hits_both / N
p_second_given_first = hits_both / hits_first
print(f"P(第一張A)           模擬 = {p_first:.5f}  理論 = {4/52:.5f}")
print(f"P(兩張都A)           模擬 = {p_both:.5f}  理論 = {4/52 * 3/51:.5f}")
print(f"P(第二張A | 第一張A) 模擬 = {p_second_given_first:.5f}  理論 = {3/51:.5f}")
print(f"乘法法則檢查: {p_first:.5f} x {p_second_given_first:.5f} = {p_first*p_second_given_first:.5f}")


# --- 區塊 2 ---
import rstatistics as r

g = r.set_seed(21)
N = 1_000_000
bag1 = ['R']*3 + ['W']*2
bag2 = ['R']*1 + ['W']*4

red = 0
for _ in range(N):
    coin = g.sample_from(['1', '2'], size=1, replace=True)[0]
    bag = bag1 if coin == '1' else bag2
    if g.sample_from(bag, size=1, replace=True)[0] == 'R':
        red += 1
print(f"P(紅) 模擬 = {red/N:.5f}   理論 = 0.40000")
