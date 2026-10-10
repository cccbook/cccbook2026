from sympy import symbols, Matrix, I, exp, diff, sqrt, simplify, eye, expand
from sympy.physics.quantum import Operator, Dagger, Commutator
from sympy.physics.quantum.constants import hbar

def demo_6_1_TDSE_verification():
    print("\n" + "="*60)
    print("### 6.1 時間相關薛丁格方程式 (TDSE) 驗證")
    print("="*60)
    
    # 定義符號: t (時間), E (能量), psi_0 (初始波函數常數)
    t = symbols('t', real=True)
    E = symbols('E', real=True)
    psi_0 = symbols('psi_0') # 假設這是一個空間部分的常數或函數
    
    # 假設系統處於一個能量本徵態 (Eigenstate)
    # 其波函數形式為: psi(t) = psi_0 * e^(-iEt/hbar)
    psi_t = psi_0 * exp(-I * E * t / hbar)
    
    print(f"假設波函數 psi(t): {psi_t}")
    
    # 驗證薛丁格方程式: i * hbar * d/dt |psi> = E |psi>
    # (註: 這裡 E 代表 H 作用在特徵態上的結果)
    
    # 左式: i * hbar * (d psi / dt)
    lhs = I * hbar * diff(psi_t, t)
    
    # 右式: H |psi> -> E * psi (因為是本徵態)
    rhs = E * psi_t
    
    print(f"左式 (時間微分項): {simplify(lhs)}")
    print(f"右式 (能量算子項): {rhs}")
    
    # 驗證兩者相等
    is_valid = simplify(lhs - rhs) == 0
    print(f"驗證結果: 方程式是否成立? {is_valid}")


def demo_6_2_hamiltonian_commutator():
    print("\n" + "="*60)
    print("### 6.2 哈密頓算子與對易關係")
    print("="*60)
    
    # 定義算子符號
    x = Operator('x')
    p = Operator('p')
    m, omega = symbols('m omega', positive=True)
    
    # 定義一維諧振子哈密頓算子 H
    # H = p^2 / 2m + 1/2 m omega^2 x^2
    H = p**2 / (2*m) + (m * omega**2 * x**2) / 2
    
    print(f"諧振子哈密頓算子 H: {H}")
    
    # 雖然 SymPy 難以直接顯示抽象算子的能量守恆
    # 但我們可以演示量子力學的核心：算子通常不對易 [x, p] != 0
    comm = Commutator(x, p)
    print(f"位置與動量的對易子 [x, p]: {comm}")
    print(f"根據正則對易關係，這應該等於 i*hbar (在計算期望值時會用到)")


def demo_6_3_time_evolution_operator():
    print("\n" + "="*60)
    print("### 6.3 時間演化算子 U(t) 與雙能階系統範例")
    print("="*60)
    
    # 為了具體計算 e^(-iHt)，我們使用矩陣表示法
    # 根據文中範例：雙能階系統 (Two-level system)
    # H = E|1><1| - E|2><2|
    # 在矩陣表示下 (基底 |1>=[1,0], |2>=[0,1]):
    # H = [[E, 0], [0, -E]]
    
    E = symbols('E', real=True)
    t = symbols('t', real=True)
    
    H_matrix = Matrix([
        [E, 0],
        [0, -E]
    ])
    
    print(f"哈密頓矩陣 H:\n{H_matrix}")
    
    # 1. 計算時間演化算子 U(t) = exp(-i * H * t / hbar)
    # 由於 H 是對角矩陣，指數運算就是對角線元素分別取指數
    # exp(diag(a, b)) = diag(exp(a), exp(b))
    U_t = exp(-I * H_matrix * t / hbar)
    
    print(f"\n時間演化算子 U(t) (矩陣形式):\n{U_t}")
    
    # 2. 驗證 U(t) 的么正性 (Unitarity): U_dagger * U = I
    U_dagger = Dagger(U_t) # 共軛轉置
    check_unitary = simplify(U_dagger * U_t)
    
    print(f"\n驗證么正性 U^dagger * U:\n{check_unitary}")
    print(f"是否等於單位矩陣? {check_unitary == eye(2)}")
    
    # 3. 演化初始狀態
    # 初始狀態 |psi(0)> = 1/sqrt(2) (|1> + |2>) -> 向量 [1/sqrt(2), 1/sqrt(2)]
    psi_0 = Matrix([1/sqrt(2), 1/sqrt(2)])
    
    print(f"\n初始狀態 |psi(0)>:\n{psi_0}")
    
    # 計算 |psi(t)> = U(t) |psi(0)>
    psi_t = U_t * psi_0
    
    print(f"\n演化後的狀態 |psi(t)> = U(t)|psi(0)>:")
    print(psi_t)
    
    # 4. 分析結果
    # 結果應該是 [1/sqrt(2) * e^(-iEt/h), 1/sqrt(2) * e^(iEt/h)]
    # 這對應於文中提到的相位因子演化
    print("\n[結果分析]")
    print("可以看到：")
    print("分量 1 (對應 |1>, 能量 E)  獲得相位因子 exp(-iEt/hbar)")
    print("分量 2 (對應 |2>, 能量 -E) 獲得相位因子 exp(+iEt/hbar)")

if __name__ == "__main__":
    demo_6_1_TDSE_verification()
    demo_6_2_hamiltonian_commutator()
    demo_6_3_time_evolution_operator()