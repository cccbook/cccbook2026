from sympy import symbols, Matrix, I, sqrt, exp, cos, sin, pi, simplify, eye
from sympy.physics.quantum import represent, qapply
from sympy.physics.quantum.qubit import Qubit
from sympy.physics.quantum.gate import X, Y, Z, H, S, T, CNOT

def demo_11_1_qubit_bloch_sphere():
    print("\n" + "="*60)
    print("### 11.1 量子位元與布洛赫球 (Bloch Sphere)")
    print("="*60)
    
    # 定義符號
    theta, phi = symbols('theta phi', real=True)
    
    # 1. 定義標準基底向量 (Computational Basis)
    ket_0 = Qubit('0')
    ket_1 = Qubit('1')
    
    print(f"基底 |0>: {represent(ket_0)}")
    print(f"基底 |1>: {represent(ket_1)}")
    
    # 2. 布洛赫球參數化表示
    # |psi> = cos(theta/2)|0> + e^(i*phi)sin(theta/2)|1>
    # 我們手動構建這個向量矩陣
    
    psi_bloch = cos(theta/2) * represent(ket_0) + \
                exp(I*phi) * sin(theta/2) * represent(ket_1)
    
    print(f"\n布洛赫球一般態向量:\n{psi_bloch}")
    
    # 3. 驗證特定角度
    # 北極 (theta=0) -> |0>
    psi_north = psi_bloch.subs(theta, 0)
    print(f"\n驗證北極 (theta=0):")
    print(f"{psi_north} (對應 |0>)")
    
    # 赤道 X軸方向 (theta=pi/2, phi=0) -> |+>
    psi_plus = psi_bloch.subs({theta: pi/2, phi: 0})
    print(f"\n驗證赤道點 (theta=pi/2, phi=0):")
    print(f"{psi_plus}")
    
    # 檢查是否等於 |+> = 1/sqrt(2) * [1, 1]^T
    is_plus = simplify(psi_plus - Matrix([1, 1])/sqrt(2)) == Matrix([0, 0])
    print(f"是否等於 |+> 態? {is_plus}")


def demo_11_2_unitary_gates():
    print("\n" + "="*60)
    print("### 11.2 單位元邏輯閘 (Pauli & Hadamard)")
    print("="*60)
    
    # 1. 印出包立矩陣 (X, Y, Z) 與 Hadamard (H) 的矩陣形式
    # represent(Gate(qubit_index), nqubits=1)
    
    mat_X = represent(X(0), nqubits=1)
    mat_Y = represent(Y(0), nqubits=1)
    mat_Z = represent(Z(0), nqubits=1)
    mat_H = represent(H(0), nqubits=1)
    
    print(f"X Gate:\n{mat_X}")
    print(f"Y Gate:\n{mat_Y}")
    print(f"Z Gate:\n{mat_Z}")
    print(f"H Gate:\n{mat_H}")
    
    # 2. 演示 H 閘作用：建立疊加態
    # H|0> -> |+> = (|0> + |1>)/sqrt(2)
    
    ket_0 = Qubit('0')
    
    # qapply 負責執行 "算子作用於狀態" 的運算
    # H(0) 代表作用在第 0 個 qubit 上的 H gate
    state_superposition = qapply(H(0) * ket_0)
    
    print(f"\n[H 閘作用演示]")
    print(f"初始態: |0>")
    print(f"作用後 (H|0>): {state_superposition}")
    
    # 轉成矩陣驗證數值
    print(f"矩陣形式: {represent(state_superposition)}")


def demo_11_3_phase_rotation():
    print("\n" + "="*60)
    print("### 11.3 相位閘 (S, T) 與轉動算子")
    print("="*60)
    
    # 1. 驗證相位閘關係: S = T^2, Z = S^2
    mat_S = represent(S(0), nqubits=1)
    mat_T = represent(T(0), nqubits=1)
    mat_Z = represent(Z(0), nqubits=1)
    
    print(f"T Gate:\n{mat_T}")
    print(f"S Gate:\n{mat_S}")
    
    print(f"\n驗證 T^2 == S ? {mat_T**2 == mat_S}")
    print(f"驗證 S^2 == Z ? {mat_S**2 == mat_Z}")
    
    # 2. 轉動算子 (Rotation Operator)
    # Rz(gamma) = exp(-i * gamma/2 * Z)
    # 我們利用矩陣指數函數來演示
    gamma = symbols('gamma', real=True)
    
    # 由於 Z 是對角矩陣 [1, 0; 0, -1]，其指數運算很簡單
    # exp(-i*g/2*Z) = [e^(-ig/2), 0; 0, e^(ig/2)]
    # 注意: SymPy 的 exp 對矩陣運算需要用 .exp() 但這裡我們手動建構或用 simplify
    
    # 直接使用矩陣指數定義: Rz = exp(-i * gamma/2 * Z_matrix)
    Rz_matrix = exp(-I * gamma / 2 * mat_Z)
    
    print(f"\nZ 軸轉動算子 Rz(gamma) (SymPy 自動計算矩陣指數):")
    # SymPy 的 Matrix.exp() 會嘗試計算
    # 這裡我們展示手動推導的結果驗證
    expected_Rz = Matrix([
        [exp(-I*gamma/2), 0],
        [0, exp(I*gamma/2)]
    ])
    print(expected_Rz)
    
    # 驗證特定角度: 旋轉 pi (180度) 應該差一個全域相位等於 Z
    # Rz(pi) = [-i, 0; 0, i] = -i * [1, 0; 0, -1] = -i * Z
    Rz_pi = expected_Rz.subs(gamma, pi)
    print(f"\n驗證 Rz(pi):")
    print(Rz_pi)
    print(f"是否等於 -i * Z ? {simplify(Rz_pi - (-I * mat_Z)) == Matrix.zeros(2,2)}")


def demo_11_4_universal_gates_cnot():
    print("\n" + "="*60)
    print("### 11.4 通用閘組與 CNOT (糾纏產生)")
    print("="*60)
    
    # 1. 檢視 CNOT 矩陣 (2-Qubit Gate, 4x4 Matrix)
    # SymPy CNOT(control, target)
    # 我們設定 CNOT(0, 1): Qubit 0 控制 Qubit 1 (注意 SymPy 的索引習慣)
    # 但為了符合標準矩陣表示 [1 0 0 0; 0 1 0 0; 0 0 0 1; 0 0 1 0]
    # 通常對應的是 |control, target>
    # 這裡我們使用 CNOT(1, 0) 代表高位(index 1)控制低位(index 0)
    
    cnot_gate = CNOT(1, 0)
    mat_cnot = represent(cnot_gate, nqubits=2)
    
    print(f"CNOT 矩陣 (Control=Q1, Target=Q0):\n{mat_cnot}")
    
    # 2. 產生貝爾態 (Bell State) / 糾纏態
    # 步驟: 
    #   1. 初始態 |00> (|q1 q0>)
    #   2. 對 Q1 施加 H 閘 -> (|00> + |10>)/sqrt(2)
    #   3. 施加 CNOT(1, 0) -> (|00> + |11>)/sqrt(2)
    
    # 初始態 |00>
    psi_0 = Qubit('00') 
    
    # 步驟 1: H 作用在 Qubit 1 (高位)
    step1 = qapply(H(1) * psi_0)
    print(f"\n步驟 1 (H on Q1): {step1}")
    
    # 步驟 2: CNOT (Q1 控制 Q0)
    step2 = qapply(CNOT(1, 0) * step1)
    print(f"步驟 2 (CNOT Q1->Q0): {step2}")
    
    # 轉換為向量檢視
    vec_bell = represent(step2, nqubits=2)
    print(f"\n最終貝爾態向量:\n{vec_bell}")
    print("可以看到只有第 1 項 (|00>) 和第 4 項 (|11>) 有值，形成糾纏。")

if __name__ == "__main__":
    demo_11_1_qubit_bloch_sphere()
    demo_11_2_unitary_gates()
    demo_11_3_phase_rotation()
    demo_11_4_universal_gates_cnot()