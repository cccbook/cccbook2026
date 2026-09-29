from sympy import symbols, Matrix, sqrt, simplify, solve
from sympy.physics.quantum import represent, qapply
from sympy.physics.quantum.qubit import Qubit
from sympy.physics.quantum.gate import H, CNOT, X

def demo_12_1_cnot_matrix():
    print("\n" + "="*60)
    print("### 12.1 受控非閘 (CNOT) 的矩陣形式與運算")
    print("="*60)
    
    # 1. 檢視 CNOT 矩陣
    # 在 SymPy 中，Qubit('10') 的索引: 1 是 index 1 (高位), 0 是 index 0 (低位)
    # 標準 CNOT 通常指高位控制低位，即 CNOT(1, 0)
    cnot_gate = CNOT(1, 0)
    cnot_matrix = represent(cnot_gate, nqubits=2)
    
    print(f"CNOT 矩陣 (控制位元=1, 目標位元=0):\n{cnot_matrix}")
    
    # 2. 作用於一般狀態向量
    # |psi> = a|00> + b|01> + c|10> + d|11>
    a, b, c, d = symbols('a b c d')
    
    # 建立一般態
    psi = a*Qubit('00') + b*Qubit('01') + c*Qubit('10') + d*Qubit('11')
    
    print(f"\n作用前狀態:\n{psi}")
    
    # 執行 CNOT
    # CNOT 邏輯: 當高位為 1 時，翻轉低位
    # |10> (高位1, 低位0) -> |11>
    # |11> (高位1, 低位1) -> |10>
    psi_prime = qapply(cnot_gate * psi)
    
    print(f"\n作用後狀態:\n{psi_prime}")
    print("可以看到 |10> 與 |11> 的係數 (c 與 d) 發生了交換。")


def demo_12_2_bell_state_generation():
    print("\n" + "="*60)
    print("### 12.2 利用 CNOT 產生貝爾態 (Bell States)")
    print("="*60)
    
    # 目標：產生 |Phi+> = (|00> + |11>) / sqrt(2)
    
    # 1. 初始狀態 |00>
    psi_0 = Qubit('00')
    print(f"1. 初始狀態: {psi_0}")
    
    # 2. 對第一個位元 (index 1) 作用 H 閘
    # H(1) 代表作用在高位元
    psi_1 = qapply(H(1) * psi_0)
    print(f"2. 作用 H 閘後: {psi_1}")
    
    # 3. 作用 CNOT (控制:1, 目標:0)
    psi_bell = qapply(CNOT(1, 0) * psi_1)
    print(f"3. 作用 CNOT 後 (貝爾態): {psi_bell}")
    
    # 驗證矩陣形式
    vec_bell = represent(psi_bell, nqubits=2)
    print(f"\n貝爾態向量形式:\n{vec_bell}")
    
    # 額外演示：產生 |Psi+> = (|01> + |10>) / sqrt(2)
    # 初始態需為 |01> (即 |0>_c |1>_t)
    psi_psi_plus = qapply(CNOT(1, 0) * H(1) * Qubit('01'))
    print(f"\n額外演示 |Psi+>: {psi_psi_plus}")


def demo_12_3_quantum_parallelism():
    print("\n" + "="*60)
    print("### 12.3 量子並行性 (Quantum Parallelism)")
    print("="*60)
    
    # 設定一個簡單的函數 f(x) = x
    # 對應的么正算符 U_f: |x>|y> -> |x>|y XOR f(x)>
    # 若 f(x) = x，則 |x>|y> -> |x>|y XOR x>，這正是 CNOT 閘的行為
    
    print("定義函數 f(x) = x")
    print("對應的 Oracle U_f 即為 CNOT 閘")
    
    # 1. 準備輸入態
    # Register 1 (Input x): 處於疊加態 H|0> = |+>
    # Register 2 (Target y): 處於 |0>
    # 總狀態 |psi_in> = |+>|0> = (|00> + |10>) / sqrt(2)
    # (注意: Qubit('10') 這裡指 Input=1, Target=0)
    
    psi_in = qapply(H(1) * Qubit('00'))
    print(f"\n輸入狀態 (Input為疊加態): {psi_in}")
    
    # 2. 執行並行運算 (一次 U_f)
    # U_f = CNOT(1, 0)
    psi_out = qapply(CNOT(1, 0) * psi_in)
    
    print(f"輸出狀態: {psi_out}")
    
    print("\n[結果分析]")
    print("輸入項 1: |00> (x=0, y=0) -> |0>|0 XOR f(0)> = |00> (因為 f(0)=0)")
    print("輸入項 2: |10> (x=1, y=0) -> |1>|0 XOR f(1)> = |11> (因為 f(1)=1)")
    print("結論: 輸出態同時包含了 f(0) 與 f(1) 的資訊。")


def demo_12_4_no_cloning_theorem():
    print("\n" + "="*60)
    print("### 12.4 無複製原理 (No-cloning Theorem) 證明")
    print("="*60)
    
    # 這是一個反證法的代數驗證
    # 假設存在複製算符 U 使得:
    # <psi|phi> = <psi|s| U^dag U |phi|s> (左式)
    # <psi|psi> <phi|phi>                 (右式)
    
    # 定義內積的值 x = <psi|phi>
    x = symbols('x')
    
    print("設 x = <psi|phi>")
    print("根據么正性推導，複製過程必須滿足: x = x^2")
    
    # 求解方程式 x = x^2
    solutions = solve(x - x**2, x)
    
    print(f"\n方程式 x - x^2 = 0 的解: {solutions}")
    
    print("\n[證明結論]")
    print(f"內積 <psi|phi> 只能是 {solutions[0]} 或 {solutions[1]}。")
    print("1. 若內積為 0: 表示兩狀態正交 (Orthogonal)。")
    print("2. 若內積為 1: 表示兩狀態相同。")
    print("因此，無法複製任意的一般量子態 (其內積可能為 0 到 1 之間的任意值)。")

if __name__ == "__main__":
    demo_12_1_cnot_matrix()
    demo_12_2_bell_state_generation()
    demo_12_3_quantum_parallelism()
    demo_12_4_no_cloning_theorem()