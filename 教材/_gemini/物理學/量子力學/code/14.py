from sympy import symbols, Matrix, sqrt, simplify, I, eye, diag
from sympy.physics.quantum import represent, qapply, TensorProduct, Dagger
from sympy.physics.quantum.density import Density  # 修正引入路徑
from sympy.physics.quantum.qubit import Qubit
from sympy.physics.quantum.gate import X, Z, H
from sympy.physics.quantum.operator import Operator

def demo_14_1_quantum_noise():
    print("\n" + "="*60)
    print("### 14.1 量子退相干與雜訊 (密度矩陣表示)")
    print("="*60)
    
    # 使用密度矩陣 (Density Matrix) 來描述混合態與雜訊
    # 初始純態: rho = |0><0|
    q0 = Qubit('0')
    rho_0 = Density([q0, 1.0]) # 機率 1.0 的純態
    
    print("1. 初始密度矩陣 rho (|0><0|):")
    mat_rho_0 = represent(rho_0, nqubits=1)
    print(mat_rho_0)
    
    # 模擬位元翻轉通道 (Bit-flip Channel)
    # rho' = (1-p) * rho + p * X * rho * X^dagger
    # 這代表有 p 的機率發生翻轉，(1-p) 機率保持原樣
    
    p = symbols('p', real=True) # 錯誤機率
    
    # 計算 X * rho * X^dagger
    # 在 SymPy Density 中，無法直接乘算子，我們轉為矩陣計算比較直觀
    X_mat = Matrix([[0, 1], [1, 0]])
    
    # 雜訊項
    term_noise = X_mat * mat_rho_0 * X_mat.H
    
    # 最終混合態
    rho_final = (1 - p) * mat_rho_0 + p * term_noise
    
    print(f"\n2. 經過位元翻轉通道後的混合態 rho':")
    print(rho_final)
    
    print("\n[結果分析]")
    print("對角線元素代表測量結果的機率。")
    print("P(0) =", rho_final[0,0], " (保持原樣的機率)")
    print("P(1) =", rho_final[1,1], " (發生翻轉的機率)")
    print("當 p=0.5 時，系統變為最大混合態 (完全隨機)。")


def demo_14_2_three_qubit_code():
    print("\n" + "="*60)
    print("### 14.2 量子糾錯碼：三位元位元翻轉碼")
    print("="*60)
    
    # 1. 編碼 (Encoding)
    # 邏輯 |0>_L -> |000>
    # 邏輯 |1>_L -> |111>
    # 我們以傳輸邏輯 |0>_L 為例
    psi_logical_0 = Qubit('000')
    print(f"1. 邏輯態 |0>_L 編碼為: {psi_logical_0}")
    
    # 2. 模擬錯誤發生 (Error Simulation)
    # 假設第一個位元 (SymPy index 2, 最左邊) 發生了 X 錯誤 (翻轉)
    # 狀態變為 |100>
    # 注意: SymPy Qubit('210') 的索引習慣
    error_gate = X(2) 
    psi_error = qapply(error_gate * psi_logical_0)
    
    print(f"2. 發生錯誤 (第1位元翻轉): {psi_error}")
    
    # 3. 錯誤偵測 (Syndrome Measurement)
    # 我們測量兩個穩定子 (Stabilizers): S1 = Z1*Z2, S2 = Z2*Z3
    # 在 SymPy 索引對應: 
    #   物理位元 1 (左) -> index 2
    #   物理位元 2 (中) -> index 1
    #   物理位元 3 (右) -> index 0
    # 因此 S1 check (2, 1), S2 check (1, 0)
    
    # 定義穩定子算符
    # S1 = Z(2) * Z(1) * I(0)
    # S2 = I(2) * Z(1) * Z(0)
    
    # 直接計算期望值 <psi| S |psi> 來模擬測量結果 (+1 或 -1)
    # 將狀態轉為矩陣以便計算
    vec_error = represent(psi_error, nqubits=3)
    
    # 構建 S1 矩陣: Z (x) Z (x) I
    mat_Z = Matrix([[1, 0], [0, -1]])
    mat_I = eye(2)
    mat_S1 = TensorProduct(mat_Z, TensorProduct(mat_Z, mat_I))
    mat_S2 = TensorProduct(mat_I, TensorProduct(mat_Z, mat_Z))
    
    # 計算症候 (Syndrome)
    # 期望值 <psi|S|psi> = vec^H * S * vec
    val_s1 = (vec_error.H * mat_S1 * vec_error)[0]
    val_s2 = (vec_error.H * mat_S2 * vec_error)[0]
    
    print(f"3. 穩定子測量結果 (Syndrome):")
    print(f"   S1 (Z1Z2): {val_s1}")
    print(f"   S2 (Z2Z3): {val_s2}")
    
    # 4. 修正 (Correction)
    # 判斷邏輯:
    # (+1, +1) -> 無錯
    # (-1, +1) -> 第 1 位元錯 (因為 S1 包含位元1, S2 不包含)
    # (-1, -1) -> 第 2 位元錯 (S1, S2 都包含位元2)
    # (+1, -1) -> 第 3 位元錯 (S2 包含位元3)
    
    print("   診斷: S1變號，S2正常 -> 判定為第 1 位元 (Index 2) 錯誤")
    
    correction_gate = X(2)
    psi_corrected = qapply(correction_gate * psi_error)
    
    print(f"4. 施加修正閘 X(2) 後的狀態: {psi_corrected}")
    
    # 驗證是否回到初始態
    # 使用 represent 轉換比較，因為 Qubit 物件有時包含未化簡算符
    is_restored = represent(psi_corrected) == represent(psi_logical_0)
    print(f"   糾錯是否成功? {is_restored}")


def demo_14_3_hardware_physics():
    print("\n" + "="*60)
    print("### 14.3 硬體實現：超導電路 (非線性諧振子)")
    print("="*60)
    print("比較理想諧振子 (Linear) 與約瑟夫森接面 (Non-linear) 的能階差異")
    
    n = symbols('n', integer=True, nonnegative=True) # 能階
    h_bar_omega = symbols('E_0', positive=True)      # 基礎能量單位
    alpha = symbols('alpha', positive=True)          # 非諧性參數 (Anharmonicity)
    
    # 1. 理想諧振子 (Harmonic Oscillator)
    # 能階公式: E_n = h_bar * omega * (n + 1/2)
    # 這裡忽略零點能，只看間距
    E_harmonic = h_bar_omega * n
    
    print(f"\n1. 理想諧振子能階 E_n = {E_harmonic}")
    
    # 計算能階間距 Delta E
    diff_01 = E_harmonic.subs(n, 1) - E_harmonic.subs(n, 0)
    diff_12 = E_harmonic.subs(n, 2) - E_harmonic.subs(n, 1)
    
    print(f"   E1 - E0 = {diff_01}")
    print(f"   E2 - E1 = {diff_12}")
    print("   結論: 能階間距相等，微波驅動時無法只激發 |0>->|1> 而不激發 |1>->|2>。")
    print("         (無法作為二能階 qubit 使用)")
    
    # 2. 超導 Transmon Qubit (引入非線性)
    # 近似公式 (Duffing Oscillator): E_n = E_0 * n - alpha/2 * n^2
    # 約瑟夫森接面提供了非線性電感
    E_transmon = h_bar_omega * n - (alpha / 2) * n**2
    
    print(f"\n2. 超導 Qubit 能階 (近似) E_n = {E_transmon}")
    
    diff_01_t = simplify(E_transmon.subs(n, 1) - E_transmon.subs(n, 0))
    diff_12_t = simplify(E_transmon.subs(n, 2) - E_transmon.subs(n, 1))
    
    print(f"   E1 - E0 = {diff_01_t}")
    print(f"   E2 - E1 = {diff_12_t}")
    
    # 計算兩者頻率差 (Anharmonicity)
    anharmonicity = simplify(diff_12_t - diff_01_t)
    print(f"   頻率差 (Anharmonicity) = {anharmonicity}")
    print("   結論: 能階間距不再相等。")
    print("         我們可以選用頻率 f_01 的微波，精確控制 |0> 與 |1> 之間的躍遷，")
    print("         而不會意外激發到 |2> 態。這就是人造原子的原理。")

if __name__ == "__main__":
    demo_14_1_quantum_noise()
    demo_14_2_three_qubit_code()
    demo_14_3_hardware_physics()