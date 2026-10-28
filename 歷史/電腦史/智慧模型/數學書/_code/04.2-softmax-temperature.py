# 04.2 softmax 溫度掃描：T 從 0.1 到 10 的機率變化
# 以及習題 2：兩狀態例子中 P(+1)=0.99 的溫度
import numpy as np


def softmax(z, T):
    # 有溫度的 softmax：e^{z/T} / sum e^{z'/T}
    z = np.asarray(z, dtype=float) / T
    e = np.exp(z - np.max(z))   # 減 max 防溢出，不影響結果
    return e / e.sum()


print("=== softmax 溫度掃描，logits z = (2, 1, 0.5) ===")
z = [2.0, 1.0, 0.5]
for T in [0.1, 0.2, 0.5, 1.0, 2.0, 5.0, 10.0]:
    p = softmax(z, T)
    print(f"T = {T:5.1f}: P = {p[0]:.4f} / {p[1]:.4f} / {p[2]:.4f}  （總和 = {p.sum():.4f}）")

print()
print("觀察：T -> 0 機率集中在最大 logit（貪心）；T -> inf 趨近均勻（1/3 各一）")
p_inf = softmax(z, 1e6)
print("T = 1e6 時 P =", np.round(p_inf, 4), "（趨近均勻）")

print()
print("=== 習題 2：兩狀態例子，E(+1)=0, E(-1)=4，求 P(+1)=0.99 的 T ===")
# P(+1) = 1 / (1 + e^{-4/T}) = 0.99  =>  T = 4 / ln(99)
T_star = 4.0 / np.log(99.0)
print(f"解析解 T = 4 / ln(99) = {T_star:.4f}")
# 數值驗證
for T in [T_star - 0.01, T_star, T_star + 0.01]:
    p_plus = 1.0 / (1.0 + np.exp(-4.0 / T))
    print(f"T = {T:.4f}: P(+1) = {p_plus:.6f}")
print("（T < 0.87 時 P(+1) > 0.99——低溫就是幾乎確定）")

print()
print("=== 對照：本章範例兩狀態在各溫度的 P(+1) ===")
for T in [1.0, 2.0, 10.0]:
    p_plus = 1.0 / (1.0 + np.exp(-4.0 / T))
    print(f"T = {T:5.1f}: P(+1) = {p_plus:.4f}")
