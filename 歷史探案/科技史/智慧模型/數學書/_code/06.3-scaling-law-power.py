# -*- coding: utf-8 -*-
# 06.3 規模法則：冪律外推 + 多步推理正確率 p^n 表格
import numpy as np

# --- 1. 冪律損失外推：L(N) = 8 * N^(-0.076) ---
alpha_N = 0.076
print("冪律損失 L(N) = 8 * N^(-0.076)：")
print(f"{'N':>10} {'L':>8}")
Ns = [1e8, 1e9, 1e10, 1e11]
Ls = [8 * n ** (-alpha_N) for n in Ns]
for n, L in zip(Ns, Ls):
    print(f"{n:>10.0e} {L:>8.3f}")
print(f"規模 x10，損失乘 10^-0.076 = {10 ** (-alpha_N):.4f}（每個比值應相同——平滑可外推）")
print(f"相鄰比值檢查：{Ls[0]/Ls[1]:.4f}, {Ls[1]/Ls[2]:.4f}, {Ls[2]/Ls[3]:.4f}")

# 用小模型量測的參數外推大模型
n_small, L_small = 1e9, 8 * 1e9 ** (-alpha_N)
n_big = 1e11
L_pred = L_small * (n_small / n_big) ** alpha_N
print(f"外推：N=1e9 量得 L={L_small:.3f}，預測 N=1e11 的 L = {L_pred:.3f}")

# --- 2. 多步推理的相乘效應：總正確率 = p^n ---
print("\n多步推理正確率 p^n 表格：")
steps = [5, 10, 20, 30, 50]
ps = [0.90, 0.95, 0.99, 0.998]
header = "  p\\n  " + "".join(f"{n:>8}" for n in steps)
print(header)
for p in ps:
    row = f"{p:>6} " + "".join(f"{p ** n:>8.3f}" for n in steps)
    print(row)
print("\n觀察：p=0.90 時 30 步任務幾乎必敗（0.042）；p 升到 0.998 後變 0.942。")
print("每步只改善一點，長鏈任務卻從失敗跳到成功——湧現的相乘解釋")

# --- 3. 湧現的階梯：全對才得分的度量 ---
print("\n『全對才得分』的階梯效應：")
for p in [0.90, 0.95, 0.99, 0.998]:
    acc20 = p ** 20
    flag = "湧現！" if acc20 > 0.5 else "      "
    print(f"  p={p}: 20 步全對率 = {acc20:.3f} {flag}")
