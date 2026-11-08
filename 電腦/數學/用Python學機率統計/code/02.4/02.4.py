# 02.4-獨立性與貝氏定理
# 由 02.4-獨立性與貝氏定理.md 抽出：以 python3.14 + PYTHONPATH 指向 rstatistics 執行

# --- 區塊 1 ---
import rstatistics as r

g = r.set_seed(3)
N = 1_000_000
d = g.sample_from(list(range(1, 7)), size=N, replace=True)

# 事件 A：偶數 {2,4,6}；事件 B：奇數 {1,3,5}（兩事件互斥）
A = [x % 2 == 0 for x in d]
B = [x % 2 == 1 for x in d]
AB = [a and b for a, b in zip(A, B)]

pA, pB, pAB = sum(A)/N, sum(B)/N, sum(AB)/N
print(f"P(A)={pA:.4f}  P(B)={pB:.4f}  P(A∩B)={pAB:.4f}")
print(f"互斥：P(A∩B) = {pAB:.4f} ≈ 0")
print(f"若獨立應有 P(A)P(B) = {pA*pB:.4f} ≠ 0 → 互斥但絕不獨立！")

# 事件 C：{2,3}。P(C)=1/3, P(A∩C)=P({2})=1/6 = P(A)P(C)
C = [x in (2, 3) for x in d]
AC = sum(1 for a, c in zip(A, C) if a and c)/N
pC = sum(C)/N
print(f"\nA 與 C：P(A)P(C) = {pA*pC:.4f},  P(A∩C) = {AC:.4f}  → 相等，獨立")


# --- 區塊 2 ---
import rstatistics as r

g = r.set_seed(42)
N = 1_000_000

# 疾病篩檢：盛行率 1/1000，靈敏度 0.99，特異度 0.99
prev, sens, spec = 1/1000, 0.99, 0.99

# 每人先決定是否患病，再決定篩檢結果
u = g.runif(N)
sick = [1 if x < prev else 0 for x in u]

u2 = g.runif(N)
pos = 0
pos_sick = 0
for s, t in zip(sick, u2):
    threshold = sens if s == 1 else 1 - spec
    if t < threshold:
        pos += 1
        if s == 1:
            pos_sick += 1

print(f"檢測陽性的比例           = {pos/N:.5f}")
print(f"陽性中真正患病的比例     = {pos_sick/pos:.5f}")
print(f"貝氏定理理論值           = {(0.99*0.001)/(0.99*0.001+0.01*0.999):.5f}")
