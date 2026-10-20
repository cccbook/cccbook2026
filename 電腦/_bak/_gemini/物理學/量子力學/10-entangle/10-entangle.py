# 修正引入位置
from sympy import symbols, Matrix, sqrt, simplify, I, eye
from sympy.physics.quantum import represent, Dagger, TensorProduct
from sympy.physics.quantum.qubit import Qubit

def demo_10_1_EPR_paradox():
    print("\n" + "="*60)
    print("### 10.1 EPR 悖論與糾纏態 (The Singlet State)")
    print("="*60)
    
    # 1. 定義 EPR 對 (Singlet State): |Psi-> = (|01> - |10>) / sqrt(2)
    # 這是自旋總和為 0 的態
    psi_minus = (Qubit('01') - Qubit('10')) / sqrt(2)
    
    print(f"EPR 糾纏態 (Dirac 符號):\n{psi_minus}")
    
    # 2. 轉換為矩陣 (向量) 形式
    # 基底順序通常為: |00>, |01>, |10>, |11>
    # 對應向量應為: [0, 1/sqrt(2), -1/sqrt(2), 0]^T
    psi_vec = represent(psi_minus)
    
    print(f"\n狀態向量 (矩陣形式):\n{psi_vec}")
    
    print("\n[說明]")
    print("這是一個最大糾纏態。若測量第一個量子位元得到 |0> (向量第二分量)，")
    print("則第二個量子位元必然坍縮為 |1>。兩者存在完美的反相關。")


def demo_10_2_Bell_inequality():
    print("\n" + "="*60)
    print("### 10.2 貝爾不等式 (CHSH) 驗證")
    print("="*60)
    
    # 為了方便數值計算，我們直接使用矩陣運算
    # 定義包立矩陣
    sigma_x = Matrix([[0, 1], [1, 0]])
    sigma_z = Matrix([[1, 0], [0, -1]])
    
    # 1. 設定測量方向 (Alice 與 Bob)
    # 這些角度是已知能最大化違反 CHSH 不等式的設定
    # Alice 的觀測量: A = Z, A' = X
    A = sigma_z
    A_prime = sigma_x
    
    # Bob 的觀測量 (旋轉 45 度):
    # B = (Z + X) / sqrt(2)
    # B' = (Z - X) / sqrt(2)
    B = (sigma_z + sigma_x) / sqrt(2)
    B_prime = (sigma_z - sigma_x) / sqrt(2)
    
    # 2. 建構 CHSH 算子: S = A(x)B - A(x)B' + A'(x)B + A'(x)B'
    # 注意: 這裡的 (x) 是張量積 (Tensor Product)
    term1 = TensorProduct(A, B)
    term2 = TensorProduct(A, B_prime)
    term3 = TensorProduct(A_prime, B)
    term4 = TensorProduct(A_prime, B_prime)
    
    # CHSH 算子 S
    S_operator = term1 - term2 + term3 + term4
    
    # 3. 計算在糾纏態下的期望值 <Psi- | S | Psi->
    # 使用 10.1 定義的 singlet 態向量
    psi_vec = Matrix([0, 1/sqrt(2), -1/sqrt(2), 0]) # |Psi->
    
    # 期望值 = <psi| S |psi>
    expectation_value = (Dagger(psi_vec) * S_operator * psi_vec)[0]
    expectation_value = simplify(expectation_value)
    
    print(f"CHSH 算子 S 的期望值 <S>:")
    print(f"數值計算結果: {expectation_value}")
    print(f"近似值: {expectation_value.evalf()}")
    
    print("\n[結論]")
    print(f"古典極限 (定域實在論) 的最大值為 2。")
    print(f"量子力學計算結果為 2*sqrt(2) ≈ 2.828。")
    print(f"違反了貝爾不等式，證明了量子非定域性。")


def demo_10_3_quantum_teleportation():
    print("\n" + "="*60)
    print("### 10.3 量子傳送 (Quantum Teleportation) 原理演示")
    print("="*60)
    
    # 定義傳送目標態 |phi> = a|0> + b|1>
    a, b = symbols('alpha beta')
    phi_C = a * Matrix([1, 0]) + b * Matrix([0, 1])
    
    print(f"1. 待傳送的未知狀態 |phi>_C: [{a}, {b}]^T")
    
    # 定義共享糾纏對 |Phi+>_AB = (|00> + |11>) / sqrt(2)
    # 矩陣形式: [1, 0, 0, 1]^T / sqrt(2)
    Phi_plus_AB = Matrix([1, 0, 0, 1]) / sqrt(2)
    
    # 2. 系統總狀態 |Psi>_CAB = |phi>_C (x) |Phi+>_AB
    # 這是一個 2 * 4 = 8 維的向量
    psi_total = TensorProduct(phi_C, Phi_plus_AB)
    
    # 3. 模擬 Alice 的貝爾測量 (Bell Measurement)
    # Alice 測量她手中的 C 和 A (前兩個 Qubits)
    # 我們定義四個貝爾基底 (針對 C, A)
    # 為了運算，我們需要將這些基底擴展到 3 Qubit 空間 (tensor Identity on B)
    
    # 定義 2-Qubit 貝爾基底矩陣
    bell_bases = {
        'Phi+': Matrix([1, 0, 0, 1]) / sqrt(2),
        'Phi-': Matrix([1, 0, 0, -1]) / sqrt(2),
        'Psi+': Matrix([0, 1, 1, 0]) / sqrt(2),
        'Psi-': Matrix([0, 1, -1, 0]) / sqrt(2)
    }
    
    # 定義 Bob 需要做的修正操作 (Pauli Gates)
    recovery_ops = {
        'Phi+': eye(2),                       # I (不做事)
        'Phi-': Matrix([[1, 0], [0, -1]]),    # Z
        'Psi+': Matrix([[0, 1], [1, 0]]),     # X
        'Psi-': Matrix([[0, -1], [1, 0]]) * I # iY (相當於 ZX) -> 簡化視為 X then Z
    }
    
    print("\n2. Alice 進行貝爾測量，系統坍縮...")
    
    # 遍歷四種可能的測量結果
    for name, basis_vec in bell_bases.items():
        # 建構投影算子 Projector = |Bell><Bell|_CA (x) I_B
        # 這裡我們用更代數的方法：計算內積 <Bell_CA | Psi_Total>
        # 這會剩下 Bob 的狀態 (未歸一化)
        
        # 為了計算 <Bell_CA | Psi_CAB>，我們需要技巧性地處理索引
        # 我們把總狀態重塑為 4x2 矩陣 (Rows=CA, Cols=B)
        # 那麼 Project_result_B = (Bell_basis^dagger * Reshaped_State)^T
        
        psi_reshaped = psi_total.reshape(4, 2) # 將 8x1 變成 4x2
        
        # 投影: <Bell|_CA * |Psi>_CAB  --> 剩下 Bob 的向量 (1x2 row -> transpose to col)
        # 結果包含機率幅 (係數)
        bob_state_unnormalized = (Dagger(basis_vec) * psi_reshaped).T
        
        # 歸一化並提取係數 (忽略 1/2 機率因子)
        bob_state = simplify(bob_state_unnormalized * 2) 
        
        print(f"\n--- 假設 Alice 測得: |{name}> ---")
        print(f"Bob 手中的坍縮狀態 (未修正): {bob_state.T}")
        
        # 4. Bob 進行修正
        op = recovery_ops[name]
        # 修正後的狀態 = Op * Bob_state
        final_state = simplify(op * bob_state)
        
        # 檢查是否回到 |phi> = [a, b]
        check = simplify(final_state - phi_C)
        is_success = (check == Matrix([0, 0]))
        
        op_name = "I" if name=='Phi+' else ("Z" if name=='Phi-' else ("X" if name=='Psi+' else "X and Z"))
        print(f"Bob 施加閘: {op_name}")
        print(f"修正後狀態: {final_state.T}")
        print(f"傳送成功? {is_success}")

if __name__ == "__main__":
    demo_10_1_EPR_paradox()
    demo_10_2_Bell_inequality()
    demo_10_3_quantum_teleportation()