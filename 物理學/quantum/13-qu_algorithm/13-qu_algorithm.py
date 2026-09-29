from sympy import symbols, Matrix, I, sqrt, exp, pi, eye, gcd, pprint, simplify
from sympy.physics.quantum import represent, qapply, TensorProduct, Dagger
from sympy.physics.quantum.qubit import Qubit
# 修正：移除了未使用的 Swap
from sympy.physics.quantum.gate import H, X, Z, CNOT
from sympy.physics.quantum.qft import QFT

def demo_13_1_deutsch_jozsa():
    print("\n" + "="*60)
    print("### 13.1 德意志-喬薩演算法 (Deutsch-Jozsa)")
    print("="*60)
    print("目標：區分函數 f(x) 是常數函數 (Constant) 還是平衡函數 (Balanced)。")
    print("演示案例：單位元輸入 (n=1)。")
    
    # 準備初始狀態 |psi_0> = |0> (Input) |1> (Ancilla)
    # 我們需要 Ancilla 處於 |-> 態來產生 Phase Kickback
    psi_input = Qubit('0')
    psi_ancilla = Qubit('1')
    
    # 1. 初始化疊加態
    # 對 Input 作用 H -> |+>
    # 對 Ancilla 作用 H -> |->
    # 這裡的 H(0) 作用在單一 Qubit 上，我們需要手動組合
    state_input_super = qapply(H(0) * psi_input)
    state_ancilla_super = qapply(H(0) * psi_ancilla)
    state_super = TensorProduct(state_input_super, state_ancilla_super)

    # 為了運算方便，轉換為向量表示 (4維向量: |00>, |01>, |10>, |11>)
    # 注意 SymPy 的 Qubit 順序，這裡我們假設 TensorProduct(Input, Ancilla)
    vec_super = represent(state_super, nqubits=2)
    
    print(f"\n1. 初始化疊加態 (Input |+>, Ancilla |->):\n{vec_super.T}")

    # 定義 Oracle U_f 矩陣 (4x4)
    # Case A: 常數函數 f(x) = 0 (Oracle = Identity)
    U_constant = eye(4)
    
    # Case B: 平衡函數 f(x) = x (Oracle = CNOT, Input控制Ancilla)
    # 當 x=0, f(x)=0 (不翻轉); 當 x=1, f(x)=1 (翻轉) -> 平衡
    # CNOT 矩陣: [1 0 0 0; 0 1 0 0; 0 0 0 1; 0 0 1 0]
    # 對應基底順序 |00>, |01>, |10>, |11> (Input, Ancilla)
    U_balanced = Matrix([
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 0, 1],
        [0, 0, 1, 0]
    ])
    
    # 2. 演算法流程函數
    def run_dj(U_oracle, name):
        print(f"\n--- 測試: {name} ---")
        # 步驟 A: Oracle 作用
        post_oracle = U_oracle * vec_super
        
        # 步驟 B: 對 Input 位元再次作用 H 閘
        # 矩陣形式: H (x) I (只測量 Input，Ancilla 不動)
        h_matrix = represent(H(0), nqubits=1)
        i_matrix = eye(2)
        final_op = TensorProduct(h_matrix, i_matrix)
        
        final_state = final_op * post_oracle
        
        print(f"最終狀態向量:\n{final_state.T}")
        
        # 檢查 Input 位元 (前兩個分量對應 Input=|0>, 後兩個對應 Input=|1>)
        # 如果 Input=|0> (前兩項有值)，則為常數；若 Input=|1> (後兩項有值)，則為平衡
        # 這裡簡化檢查第一個分量
        if abs(final_state[0]) > 0.1 or abs(final_state[1]) > 0.1:
            print("測量結果: Input = |0>  => 判定為 [常數函數]")
        else:
            print("測量結果: Input = |1>  => 判定為 [平衡函數]")

    run_dj(U_constant, "常數函數 (Identity)")
    run_dj(U_balanced, "平衡函數 (CNOT)")


def demo_13_2_qft():
    print("\n" + "="*60)
    print("### 13.2 量子傅立葉變換 (QFT)")
    print("="*60)
    
    # 使用 3 個 Qubits
    n = 3
    N = 2**n
    print(f"演示 {n} Qubits 的 QFT 矩陣 (N={N})")
    
    # 1. 使用 SymPy 內建的 QFT 閘
    # QFT(起始bit, 結束bit)
    qft_gate = QFT(0, n)
    
    # 2. 取得矩陣表示
    # F_jk = (1/sqrt(N)) * omega^(j*k)
    qft_matrix = represent(qft_gate, nqubits=n)
    
    # 為了顯示漂亮，我們印出左上角 4x4 區域
    print(f"\nQFT 矩陣 (左上角 2x2 範例):")
    # omega = exp(2*pi*i / 8)
    print(qft_matrix[0:2, 0:2])
    
    print("\n驗證矩陣元素 F_{1,1}:")
    omega = exp(2*pi*I / N)
    element_11 = qft_matrix[1, 1]
    expected = omega**(1*1) / sqrt(N)
    
    print(f"矩陣值: {element_11}")
    print(f"公式值: {expected}")
    print(f"是否相符? {simplify(element_11 - expected) == 0}")
    
    # 3. 演示基底轉換
    # 將 |000> (即 |0>) 轉換 -> 均勻疊加態
    input_state = represent(Qubit('000'), nqubits=3)
    output_state = qft_matrix * input_state
    
    print(f"\nQFT|000> (應該是均勻疊加態):")
    # 顯示前幾項
    print(f"係數 (全為 1/sqrt(8)): {output_state[0]}, {output_state[1]} ...")


def demo_13_3_grover_search():
    print("\n" + "="*60)
    print("### 13.3 葛洛弗搜尋演算法 (Grover's Search)")
    print("="*60)
    
    # 演示 2 Qubits (N=4) 搜尋目標 |11> (index 3)
    N = 4
    target_idx = 3 # |11>
    
    print(f"搜尋空間 N={N}, 目標狀態 |11> (Index 3)")
    
    # 1. 初始化均勻疊加態 |s>
    # |s> = H|0> (x) H|0> = [0.5, 0.5, 0.5, 0.5]^T
    s_vec = Matrix([0.5, 0.5, 0.5, 0.5])
    print(f"\n1. 初始疊加態 |s>: {s_vec.T}")
    
    # 2. 定義 Oracle O
    # Oracle 翻轉目標態的相位: O|x> = -|x> if x=target else |x>
    # 對於 target=3，矩陣為 diag(1, 1, 1, -1)
    Oracle = eye(4)
    Oracle[target_idx, target_idx] = -1
    
    # 3. 定義擴散算符 D (Diffusion Operator)
    # D = 2|s><s| - I
    # |s><s| 是全是 0.25 的矩陣
    s_s_dagger = Matrix.ones(4, 4) * 0.25
    Diffusion = 2 * s_s_dagger - eye(4)
    
    print("\n2. 執行一次葛洛弗迭代 (Grover Iteration): G = D * O")
    
    # 步驟 A: Oracle 標記
    state_after_oracle = Oracle * s_vec
    print(f"   Oracle 後 (目標相位翻轉): {state_after_oracle.T}")
    
    # 步驟 B: 擴散 (對平均值翻轉)
    state_final = Diffusion * state_after_oracle
    
    print(f"   擴散 D 後 (振幅放大): {state_final.T}")
    
    print("\n[結果分析]")
    print(f"目標 |11> (Index 3) 的振幅: {state_final[3]}")
    print(f"測量機率: {state_final[3]**2}")
    print("對於 N=4，單次迭代即可達到 100% 機率找到目標。")


def demo_13_4_shor_period_finding():
    print("\n" + "="*60)
    print("### 13.4 秀爾演算法 (Shor's Algorithm) - 週期尋找原理")
    print("="*60)
    
    # 秀爾演算法的核心是尋找 f(x) = a^x mod M 的週期 r
    # 這裡我們模擬古典部分的算術與 QFT 的原理
    
    M = 15
    a = 7
    print(f"分解大數 M={M}, 選擇隨機數 a={a}")
    print(f"尋找 f(x) = {a}^x mod {M} 的週期 r...")
    
    # 1. 古典計算週期序列
    sequence = []
    x = 0
    while True:
        val = (a**x) % M
        if val in sequence:
            break
        sequence.append(val)
        x += 1
        
    r = len(sequence)
    print(f"\n模數序列: {sequence}")
    print(f"發現週期 r = {r}")
    print(f"驗證: {a}^{r} = {a**r} = {a**r % M} (mod {M})")
    
    # 2. 因數分解
    # 若 r 為偶數，計算 gcd(a^(r/2) +/- 1, M)
    if r % 2 == 0:
        factor1 = gcd(a**(r//2) - 1, M)
        factor2 = gcd(a**(r//2) + 1, M)
        print(f"\n[推導因數]")
        print(f"計算 GCD({a}^{r//2} - 1, {M}) = {factor1}")
        print(f"計算 GCD({a}^{r//2} + 1, {M}) = {factor2}")
        print(f"成功分解 {M} = {factor1} * {factor2}")
    else:
        print("週期 r 為奇數，需重新選擇 a。")
        
    print("\n[量子部分原理說明]")
    print("量子電腦透過 QPE (量子相位估計) 來找到 r。")
    print("QFT 矩陣會將週期性的振幅轉換為頻率空間的峰值。")
    print(f"對於週期 {r}，QFT 測量結果會集中在 N/r 的整數倍附近。")

if __name__ == "__main__":
    demo_13_1_deutsch_jozsa()
    demo_13_2_qft()
    demo_13_3_grover_search()
    demo_13_4_shor_period_finding()