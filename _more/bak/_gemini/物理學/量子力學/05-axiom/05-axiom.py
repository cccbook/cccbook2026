from sympy import symbols, integrate, diff, exp, oo, I, sqrt, pi, conjugate, simplify, Abs, solve
# 修正：將 qapply 加入到這裡的引用列表中
from sympy.physics.quantum import Ket, Bra, Dagger, represent, qapply
from sympy.physics.quantum.qubit import Qubit
import random # 確保 random 模組被引用

def demo_5_1_state_normalization():
    print("\n" + "="*60)
    print("### 5.1 狀態公設：波函數歸一化 (Normalization)")
    print("="*60)
    
    # 定義變數
    x = symbols('x', real=True)
    alpha = symbols('alpha', positive=True) # 寬度參數
    N = symbols('N', positive=True)         # 待求的歸一化常數
    
    # 1. 定義一個未歸一化的高斯波函數
    # psi(x) = N * e^(-alpha * x^2 / 2)
    psi = N * exp(-alpha * x**2 / 2)
    
    print(f"原始波函數 psi(x): {psi}")
    
    # 2. 計算全空間機率積分: integral(|psi|^2) dx = 1
    # 這裡 psi 是實函數，所以 |psi|^2 = psi^2
    probability_density = conjugate(psi) * psi
    total_prob = integrate(probability_density, (x, -oo, oo))
    
    print(f"全空間總機率積分結果 (含 N): {total_prob}")
    
    # 3. 求解 N 使得總機率為 1
    # solve 函數回傳的是列表
    sol_N = solve(total_prob - 1, N)[0]
    
    print(f"求解歸一化常數 N: {sol_N}")
    
    # 4. 寫出歸一化後的波函數
    psi_normalized = psi.subs(N, sol_N)
    print(f"歸一化後的波函數: {psi_normalized}")


def demo_5_2_observables_as_operators():
    print("\n" + "="*60)
    print("### 5.2 物理量公設：算子 (Operators)")
    print("="*60)
    
    x = symbols('x', real=True)
    hbar = symbols('hbar', real=True, positive=True)
    alpha = symbols('alpha', positive=True)
    
    # 使用歸一化的高斯波函數 (常數係數簡化處理)
    # psi = (alpha/pi)^(1/4) * e^(-alpha * x^2 / 2)
    norm_const = (alpha / pi)**(1/4)
    psi = norm_const * exp(-alpha * x**2 / 2)
    
    print(f"波函數 psi(x): {psi}")
    
    # 1. 位置算子 x_hat 作用: x * psi
    op_x_psi = x * psi
    print(f"位置算子作用 (x * psi): {op_x_psi}")
    
    # 2. 動量算子 p_hat 作用: -i * hbar * d/dx
    # 使用 diff 進行微分
    op_p_psi = -I * hbar * diff(psi, x)
    
    print(f"動量算子作用 (-ihbar * d/dx psi):")
    print(simplify(op_p_psi))
    
    # 3. 驗證動量期望值 <p> = <psi | p_hat | psi>
    # 對於實數高斯波函數，平均動量應為 0
    expectation_p = integrate(conjugate(psi) * op_p_psi, (x, -oo, oo))
    
    print(f"動量期望值 <p>: {expectation_p}")
    print("(結果為 0 符合預期，因為波函數是靜止的高斯波包)")


def demo_5_3_measurement_born_rule():
    print("\n" + "="*60)
    print("### 5.3 測量公設：波恩定則 (Born Rule)")
    print("="*60)
    
    # 我們使用離散的 Qubit 系統來演示，這比積分更直觀
    # 定義基底 |0> 和 |1>
    q0 = Qubit('0')
    q1 = Qubit('1')
    
    # 1. 建立一個疊加態 (Superposition State)
    # |psi> = c1|0> + c2|1>
    # 例如：|psi> = 1/2 |0> + sqrt(3)/2 |1>
    c1 = 1/2
    c2 = sqrt(3)/2
    psi = c1 * q0 + c2 * q1
    
    print(f"量子態 |psi>: {psi}")
    
    # 2. 計算機率幅 (Probability Amplitudes)
    # 機率幅 A_0 = <0|psi>, A_1 = <1|psi>
    # Dagger(q0) 產生 Bra <0|
    amp_0 = Dagger(q0) * psi
    amp_1 = Dagger(q1) * psi
    
    # qapply 將 Bra 作用在 Ket 上並計算內積
    # 由於已在全域引用 qapply，這裡可以直接使用
    val_0 = qapply(amp_0)
    val_1 = qapply(amp_1)
    
    print(f"測量結果為 '0' 的機率幅: {val_0}")
    print(f"測量結果為 '1' 的機率幅: {val_1}")
    
    # 3. 應用波恩定則計算機率 P = |Amplitude|^2
    prob_0 = Abs(val_0)**2
    prob_1 = Abs(val_1)**2
    
    print(f"測得 '0' 的機率 P(0): {prob_0}")
    print(f"測得 '1' 的機率 P(1): {prob_1}")
    print(f"總機率: {prob_0 + prob_1}")


def demo_5_4_collapse():
    print("\n" + "="*60)
    print("### 5.4 測量後的坍縮 (Collapse)")
    print("="*60)
    
    # 沿用上一節的態
    c1 = 1/2
    c2 = sqrt(3)/2
    psi_initial = c1 * Qubit('0') + c2 * Qubit('1')
    
    print("【測量前】")
    print(f"系統狀態: {psi_initial}")
    print("系統處於 |0> 與 |1> 的疊加態。")
    
    print("\n... 進行測量 (模擬) ...")
    
    # 這裡我們用程式邏輯模擬"上帝擲骰子"的過程
    # 產生 0 到 1 之間的隨機數
    r = random.random()
    
    # 根據波恩定則的機率決定結果 (P(0)=0.25, P(1)=0.75)
    measurement_result = None
    psi_collapsed = None
    
    # 為了教學演示的一致性，我們這裡手動顯示兩種情況，而不是真隨機
    # 情境 A: 測到 0
    print("\n--- 情境 A: 假設測量儀器顯示結果為 '0' ---")
    measurement_result = 0
    # 坍縮：狀態瞬間變為 |0>
    psi_collapsed = Qubit('0')
    print(f"【測量後】")
    print(f"測量結果: {measurement_result}")
    print(f"坍縮後的波函數: {psi_collapsed}")
    print(f"係數 c1 變為 1，c2 變為 0。")
    
    # 再次測量驗證
    # 修正：確保 qapply 在這裡也能被調用
    prob_after = Abs(qapply(Dagger(Qubit('0')) * psi_collapsed))**2
    print(f"若立即再次測量，得到 '0' 的機率為: {prob_after} (100%)")

    # 情境 B: 測到 1
    print("\n--- 情境 B: 假設測量儀器顯示結果為 '1' ---")
    measurement_result = 1
    # 坍縮：狀態瞬間變為 |1>
    psi_collapsed = Qubit('1')
    print(f"【測量後】")
    print(f"測量結果: {measurement_result}")
    print(f"坍縮後的波函數: {psi_collapsed}")

if __name__ == "__main__":
    demo_5_1_state_normalization()
    demo_5_2_observables_as_operators()
    demo_5_3_measurement_born_rule()
    demo_5_4_collapse()