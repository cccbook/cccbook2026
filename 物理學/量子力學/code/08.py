from sympy import symbols, diff, Function, I, simplify, Matrix, sqrt, Abs, eye
from sympy.physics.quantum import Dagger
from sympy.physics.quantum.constants import hbar

def demo_8_1_canonical_commutation():
    print("\n" + "="*60)
    print("### 8.1 對易子物理意義：推導正則對易關係 [x, p]")
    print("="*60)
    
    # 定義座標 x 與任意波函數 psi(x)
    x = symbols('x', real=True)
    psi = Function('psi')(x)
    
    print(f"測試波函數: {psi}")
    
    # 1. 定義算符的作用方式
    # 位置算符 X_op: 乘上 x
    def X_op(f):
        return x * f
    
    # 動量算符 P_op: -i * hbar * d/dx
    def P_op(f):
        return -I * hbar * diff(f, x)
    
    # 2. 計算 [x, p] psi = (xp - px) psi
    # 先算 xp psi (先作用 p，再作用 x)
    term_xp = X_op(P_op(psi))
    
    # 再算 px psi (先作用 x，再作用 p)
    # 注意微分的連鎖律: d/dx (x * psi) = psi + x * dpsi/dx
    term_px = P_op(X_op(psi))
    
    print(f"\n1. xp|psi> = {term_xp}")
    print(f"2. px|psi> = {simplify(term_px)}")
    
    # 3. 相減得到對易子結果
    commutator_action = simplify(term_xp - term_px)
    
    print(f"\n3. [x, p]|psi> = (xp - px)|psi> = {commutator_action}")
    
    # 4. 提取算符 (除去 psi)
    # 修正：直接除以 psi 來提取算符值，這是最直觀的方法
    result = simplify(commutator_action / psi)
    
    print(f"\n結論: [x, p] = {result}")
    print("證得正則對易關係: [x, p] = i * hbar")


def demo_8_2_uncertainty_principle():
    print("\n" + "="*60)
    print("### 8.2 廣義不確定性原理驗證 (使用自旋矩陣)")
    print("="*60)
    
    # 使用 Pauli 矩陣作為算符 A 和 B (自旋算符 sigma_x, sigma_y)
    # 這些是有限維矩陣，方便計算標準差
    Sx = Matrix([[0, 1], [1, 0]])       # Sigma X
    Sy = Matrix([[0, -I], [I, 0]])      # Sigma Y
    Sz = Matrix([[1, 0], [0, -1]])      # Sigma Z (用於對易子檢查)
    
    # 選擇一個狀態向量 |psi>
    # 我們選 Sz 的特徵向量 |0> = [1, 0]^T
    psi = Matrix([1, 0])
    
    print(f"算符 A (Sigma X):\n{Sx}")
    print(f"算符 B (Sigma Y):\n{Sy}")
    print(f"狀態向量 |psi>:\n{psi}")
    
    # 定義計算期望值的函數 <O> = <psi|O|psi>
    def expectation(op, state):
        return (state.H * op * state)[0]
    
    # 定義計算標準差的函數 delta O = sqrt(<O^2> - <O>^2)
    def uncertainty(op, state):
        exp_op = expectation(op, state)
        exp_op2 = expectation(op * op, state)
        # 變異數 = <O^2> - <O>^2
        variance = exp_op2 - exp_op**2
        return sqrt(simplify(variance))

    # 1. 計算不確定性 Delta A 和 Delta B
    dA = uncertainty(Sx, psi)
    dB = uncertainty(Sy, psi)
    
    print(f"\n[左式] 不確定性乘積:")
    print(f"  <A> = {expectation(Sx, psi)}")
    print(f"  Delta A = {dA}")
    print(f"  Delta B = {dB}")
    print(f"  Delta A * Delta B = {dA * dB}")
    
    # 2. 計算對易子 [A, B] 的期望值
    comm = Sx * Sy - Sy * Sx
    exp_comm = expectation(comm, psi)
    
    print(f"\n[右式] 對易子下界:")
    print(f"  [A, B] = \n{comm}")
    print(f"  (註: 理論上 [Sx, Sy] = 2i*Sz)")
    print(f"  <[A, B]> = {exp_comm}")
    
    # 3. 驗證不等式: dA * dB >= 1/2 * |<[A, B]>|
    limit = simplify(Abs(exp_comm) / 2)
    print(f"  1/2 * |<[A, B]>| = {limit}")
    
    check = (dA * dB) >= limit
    print(f"\n驗證結果: {dA * dB} >= {limit} ? {check}")


def demo_8_3_simultaneous_eigenstates():
    print("\n" + "="*60)
    print("### 8.3 相容觀測量與共同特徵基底")
    print("="*60)
    
    # 定義兩個可對易的矩陣 A, B (對角矩陣必定對易)
    # A = diag(1, 2)
    # B = diag(3, 4)
    A = Matrix([[1, 0], [0, 2]])
    B = Matrix([[3, 0], [0, 4]])
    
    print(f"矩陣 A:\n{A}")
    print(f"矩陣 B:\n{B}")
    
    # 1. 檢查是否對易
    comm = A * B - B * A
    is_commuting = comm == Matrix.zeros(2, 2)
    print(f"\n檢查 [A, B] == 0 ? {is_commuting}")
    
    if is_commuting:
        print("A 與 B 是相容觀測量 (Compatible Observables)。")
    
    # 2. 尋找 A 的特徵向量
    # eigenvects() 回傳 [(eigenval, multiplicity, [vectors]), ...]
    eigen_A = A.eigenvects()
    
    print(f"\nA 的特徵向量:")
    vecs_A = []
    for val, mult, vecs in eigen_A:
        v = vecs[0]
        vecs_A.append(v)
        print(f"  lambda_A={val}: {v.T}")
        
    # 3. 驗證這些向量同時也是 B 的特徵向量
    print(f"\n驗證 A 的特徵向量是否也是 B 的特徵向量:")
    
    for v in vecs_A:
        # 計算 B|v>
        Bv = B * v
        # 檢查 B|v> 是否等於 常數 * |v>
        # 這裡我們直接觀察 Bv 的元素
        
        print(f"  對於向量 |v>={v.T}:")
        print(f"    B|v> = {Bv.T}")
        
        # 數學驗證
        # 找出對應的特徵值 (假設 v 非零)
        eigenval_B = 0
        if v[0] != 0: eigenval_B = Bv[0] / v[0]
        elif v[1] != 0: eigenval_B = Bv[1] / v[1]
        
        check = simplify(B * v - eigenval_B * v) == Matrix.zeros(2, 1)
        print(f"    它是 B 的特徵向量嗎 (特徵值 {eigenval_B})? {check}")

if __name__ == "__main__":
    demo_8_1_canonical_commutation()
    demo_8_2_uncertainty_principle()
    demo_8_3_simultaneous_eigenstates()