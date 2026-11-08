# 02.2-事件與機率
# 由 02.2-事件與機率.md 抽出：以 python3.14 + PYTHONPATH 指向 rstatistics 執行

# --- 區塊 1 ---
import rstatistics as r

g = r.set_seed(2026)
N = 1_000_000

# 丟兩顆骰子，事件 A：和為 7；事件 B：至少一顆為 6
d1 = g.sample_from(list(range(1, 7)), size=N, replace=True)
d2 = g.sample_from(list(range(1, 7)), size=N, replace=True)

hits_A = sum(1 for a, b in zip(d1, d2) if a + b == 7)
hits_B = sum(1 for a, b in zip(d1, d2) if a == 6 or b == 6)
hits_AB = sum(1 for a, b in zip(d1, d2) if a + b == 7 and (a == 6 or b == 6))
hits_union = sum(1 for a, b in zip(d1, d2) if a + b == 7 or a == 6 or b == 6)

pA, pB, pAB = hits_A / N, hits_B / N, hits_AB / N
print(f"P(A)  模擬 = {pA:.6f}   理論 = {6/36:.6f}")
print(f"P(B)  模擬 = {pB:.6f}   理論 = {11/36:.6f}")
print(f"P(A∩B) 模擬 = {pAB:.6f}   理論 = {2/36:.6f}")
print(f"廣義加法：P(A∪B) 模擬 = {hits_union/N:.6f}")
print(f"          P(A)+P(B)-P(A∩B) = {pA+pB-pAB:.6f}   理論 = {15/36:.6f}")
print(f"估計誤差量級 1/sqrt(N) = {1/N**0.5:.6f}")


# --- 區塊 2 ---
import rstatistics as r

# 生日問題：n 個人至少兩人同天生日的機率
def birthday_theory(n):
    p_no = 1.0
    for i in range(n):
        p_no *= (365 - i) / 365
    return 1 - p_no

g = r.set_seed(7)
N = 100_000
for n in (23, 30, 50):
    cnt = 0
    for _ in range(N):
        bdays = g.sample_from(list(range(365)), size=n, replace=True)
        if len(set(bdays)) < n:
            cnt += 1
    est = cnt / N
    th = birthday_theory(n)
    print(f"n = {n:2d}: 模擬 = {est:.4f}   理論 = {th:.4f}   差 = {abs(est-th):.4f}")
