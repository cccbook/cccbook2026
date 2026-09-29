from sympy import symbols, Matrix, sqrt, solve, expand
from sympy.physics.quantum import TensorProduct, Ket, represent
from sympy.physics.quantum.qubit import Qubit

def demo_4_1_tensor_construction():
    print("\n" + "="*60)
    print("### 4.1 複合系統的空間構建 (性質驗證)")
    print("="*60)
    
    # 定義抽象的向量 (Kets) 與純量
    v1 = Ket('v1')
    v2 = Ket('v2')
    w = Ket('w')
    c = symbols('c')
    
    print("定義向量 v1, v2 \in V, w \in W, 純量 c")
    
    # 1. 驗證純量乘法的結合律: c(v \otimes w) = (cv) \otimes w = v \otimes (cw)
    # SymPy 的 TensorProduct 會自動處理純量的提取
    
    tp_original = c * TensorProduct(v1, w)
    tp_scalar_v = TensorProduct(c * v1, w)
    tp_scalar_w = TensorProduct(v1, c * w)
    
    print(f"\n[性質 1: 純量乘法]")
    print(f"  c * (v1 x w) : {tp_original}")
    print(f"  (c*v1) x w   : {tp_scalar_v}")
    print(f"  v1 x (c*w)   : {tp_scalar_w}")
    
    # 檢查是否相等 (SymPy 會自動化簡標準形式)
    check1 = (tp_original == tp_scalar_v) and (tp_original == tp_scalar_w)
    print(f"  驗證結果: {check1}")
    
    # 2. 驗證分配律: (v1 + v2) \otimes w = v1 \otimes w + v2 \otimes w
    print(f"\n[性質 2: 分配律]")
    
    expr_left = TensorProduct(v1 + v2, w)
    # 使用 expand(tensor=True) 來展開張量積
    expr_expanded = expand(expr_left, tensor=True)
    
    expr_right = TensorProduct(v1, w) + TensorProduct(v2, w)
    
    print(f"  左式 (v1 + v2) x w (展開前): {expr_left}")
    print(f"  左式 (展開後)              : {expr_expanded}")
    print(f"  右式 v1 x w + v2 x w       : {expr_right}")
    print(f"  驗證結果: {expr_expanded == expr_right}")


def demo_4_2_kronecker_product():
    print("\n" + "="*60)
    print("### 4.2 克羅內克積 (Kronecker Product) 矩陣計算")
    print("="*60)
    
    # 1. 向量的克羅內克積
    # u = [u1, u2]^T, v = [v1, v2]^T
    u1, u2, v1, v2 = symbols('u1 u2 v1 v2')
    u_vec = Matrix([u1, u2])
    v_vec = Matrix([v1, v2])
    
    # 計算 u (tensor) v
    # TensorProduct 可以直接作用於 SymPy Matrix 物件
    uv_prod = TensorProduct(u_vec, v_vec)
    
    print("向量 u:")
    print(u_vec)
    print("向量 v:")
    print(v_vec)
    print("\n向量張量積 u x v (結果應為 4x1):")
    print(uv_prod)
    
    # 2. 矩陣的克羅內克積
    # 定義 2x2 矩陣 A 和 B
    A = Matrix([[1, 2], [3, 4]])
    B = Matrix([[0, 5], [6, 7]])
    
    print(f"\n矩陣 A:\n{A}")
    print(f"矩陣 B:\n{B}")
    
    AB_prod = TensorProduct(A, B)
    
    print("\n矩陣張量積 A x B (結果應為 4x4 分塊矩陣):")
    print(AB_prod)
    
    # 驗證其中一個元素，例如左上角的區塊應該是 1 * B = B
    # 右下角區塊應該是 4 * B = [0, 20; 24, 28]
    print("\n驗證右下角區塊 (應該是 4 * B):")
    print(AB_prod[2:4, 2:4])


def demo_4_3_entanglement_proof():
    print("\n" + "="*60)
    print("### 4.3 糾纏態 (Entangled States) 與不可分離證明")
    print("="*60)
    
    # 1. 定義貝爾態 (Bell State) |Phi+>
    # |Phi+> = 1/sqrt(2) * (|00> + |11>)
    # 使用 Qubit 物件建立
    bell_state = (Qubit('00') + Qubit('11'))/sqrt(2)
    
    # 將其轉換為矩陣 (向量) 形式表示 [1/sqrt(2), 0, 0, 1/sqrt(2)]^T
    # represent 會將 Qubit 轉為 column matrix
    bell_matrix = represent(bell_state)
    
    print("目標狀態 (Bell State |Phi+>):")
    print(bell_matrix)
    
    # 2. 嘗試構建一個一般形式的可分離態 (Separable State)
    # 設 |a> = [a0, a1]^T, |b> = [b0, b1]^T
    # 可分離態 = |a> x |b>
    
    a0, a1, b0, b1 = symbols('a0 a1 b0 b1')
    vec_a = Matrix([a0, a1])
    vec_b = Matrix([b0, b1])
    
    separable_state = TensorProduct(vec_a, vec_b)
    
    print("\n一般可分離態 (|a> x |b>):")
    print(separable_state)
    
    # 3. 建立方程組並嘗試求解
    # 我們要求: separable_state == bell_matrix
    print("\n試圖解方程組 (尋找是否存在 a0, a1, b0, b1)...")
    
    equations = [
        separable_state[0] - bell_matrix[0], # a0*b0 = 1/sqrt(2)
        separable_state[1] - bell_matrix[1], # a0*b1 = 0
        separable_state[2] - bell_matrix[2], # a1*b0 = 0
        separable_state[3] - bell_matrix[3]  # a1*b1 = 1/sqrt(2)
    ]
    
    for i, eq in enumerate(equations):
        print(f"  Eq {i+1}: {eq} = 0")
        
    # 使用 SymPy 的 solve 解方程式
    solution = solve(equations, [a0, a1, b0, b1])
    
    print(f"\n求解結果: {solution}")
    
    # 判斷
    if not solution:
        print("結論: 無解 (空集合)。")
        print("證明: 不存在任何向量 a, b 使得 |a> x |b> = |Phi+>。")
        print("因此，|Phi+> 是一個糾纏態。")
    else:
        print("結論: 找到解，該狀態是可分離的。")

if __name__ == "__main__":
    demo_4_1_tensor_construction()
    demo_4_2_kronecker_product()
    demo_4_3_entanglement_proof()