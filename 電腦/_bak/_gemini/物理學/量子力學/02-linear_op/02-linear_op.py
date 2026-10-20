from sympy import Matrix, symbols, I, simplify, eye, sqrt
from sympy.physics.quantum import Dagger, OuterProduct, represent
from sympy.physics.quantum.qubit import Qubit

def demo_2_1_linear_transformation():
    print("\n" + "="*50)
    print("### 2.1 線性變換 (Linear Transformation) 與算子")
    print("="*50)
    
    # 1. 定義一個線性算子 T (矩陣形式)
    # 使用 2x2 矩陣範例
    T = Matrix([
        [2, 3],
        [1, 4]
    ])
    
    # 定義向量 u, v 與純量 a
    u = Matrix([1, 2])
    v = Matrix([3, -1])
    a = 5
    
    print(f"算子 T:\n{T}")
    print(f"向量 u: {u.T}")
    print(f"向量 v: {v.T}")
    
    # 2. 驗證加法性: T(u + v) = T(u) + T(v)
    lhs_add = T * (u + v)
    rhs_add = T * u + T * v
    print(f"\n[驗證加法性]")
    print(f"  T(u+v): {lhs_add.T}")
    print(f"  Tu+Tv : {rhs_add.T}")
    print(f"  結果相符? {lhs_add == rhs_add}")
    
    # 3. 驗證齊次性: T(au) = aT(u)
    lhs_homo = T * (a * u)
    rhs_homo = a * (T * u)
    print(f"\n[驗證齊次性]")
    print(f"  T(au) : {lhs_homo.T}")
    print(f"  aT(u) : {rhs_homo.T}")
    print(f"  結果相符? {lhs_homo == rhs_homo}")


def demo_2_2_adjoint_operators():
    print("\n" + "="*50)
    print("### 2.2 伴隨算子 (Adjoint) 與自伴算子")
    print("="*50)

    # 1. 定義一個複數矩陣 A (Hermitian 範例)
    # 矩陣 A:
    # [ 1      1+i ]
    # [ 1-i    2   ]
    A = Matrix([
        [1,      1 + I],
        [1 - I,  2]
    ])
    print(f"矩陣 A:\n{A}")

    # 2. 計算伴隨算子 (共軛轉置 A^H)
    # SymPy 中使用 .H 屬性
    A_adjoint = A.H
    print(f"\nA 的伴隨算子 A^H:\n{A_adjoint}")

    # 3. 驗證自伴性質 (Hermitian): A = A^H
    is_self_adjoint = A == A_adjoint
    print(f"A 是否為自伴算子? {is_self_adjoint}")

    # 4. 驗證內積性質: <Ax, y> = <x, A^H y>
    # 定義測試向量
    x = Matrix([1, I])
    y = Matrix([2, 1])

    # 在矩陣表示法中，內積 <u, v> 通常定義為 u^H * v
    # 左式: <Ax, y> = (Ax)^H * y
    lhs = (A * x).H * y
    
    # 右式: <x, A^H y> = x^H * (A_adjoint * y)
    rhs = x.H * (A_adjoint * y)

    print(f"\n[驗證內積移項性質 <Ax, y> = <x, A^H y>]")
    print(f"  左式 <Ax, y> : {simplify(lhs[0])}")
    print(f"  右式 <x, A^H y>: {simplify(rhs[0])}")
    print(f"  驗證成功? {simplify(lhs - rhs) == Matrix([0])}")


def demo_2_3_projection_operators():
    print("\n" + "="*50)
    print("### 2.3 投影算子 (Projection) 與恆等分解")
    print("="*50)
    
    # 使用量子模組的 Qubit 來建立直觀的投影算子
    # |0> 對應 [1, 0]^T
    # |1> 對應 [0, 1]^T
    q0 = Qubit('0')
    q1 = Qubit('1')
    
    # 1. 建立正交投影算子
    # P0 = |0><0|
    # P1 = |1><1|
    P0_op = OuterProduct(q0, Dagger(q0))
    P1_op = OuterProduct(q1, Dagger(q1))
    
    # 將算子轉為矩陣以便運算
    P0 = represent(P0_op)
    P1 = represent(P1_op)
    
    print(f"投影算子 P0 (矩陣):\n{P0}")
    print(f"投影算子 P1 (矩陣):\n{P1}")
    
    # 2. 驗證冪等性 (Idempotency): P^2 = P
    print(f"\n[驗證冪等性]")
    print(f"  P0 * P0 == P0 ? {P0 * P0 == P0}")
    print(f"  P1 * P1 == P1 ? {P1 * P1 == P1}")
    
    # 3. 驗證正交性: P0 * P1 = 0
    print(f"\n[驗證正交性]")
    print(f"  P0 * P1 == 0 ? {P0 * P1 == Matrix.zeros(2, 2)}")

    # 4. 恆等分解 (Resolution of Identity): sum(Pi) = I
    I_sum = P0 + P1
    I_target = eye(2) # 2x2 單位矩陣
    
    print(f"\n[驗證恆等分解 sum(Pi) = I]")
    print(f"  P0 + P1:\n{I_sum}")
    print(f"  驗證成功? {I_sum == I_target}")


def demo_2_4_spectral_theory():
    print("\n" + "="*50)
    print("### 2.4 譜理論 (Spectral Theory) 與譜分解")
    print("="*50)

    # 定義一個自伴矩陣 (以 Pauli-X 閘為例)
    # T = [0, 1]
    #     [1, 0]
    T = Matrix([
        [0, 1],
        [1, 0]
    ])
    print(f"原始算子 T:\n{T}")

    # 1. 計算特徵值與特徵向量
    # eigenvects() 返回列表: [(特徵值, 重數, [特徵向量]), ...]
    eigen_data = T.eigenvects()
    
    print("\n[計算特徵系統]")
    
    # 用來重建矩陣的累加變數
    T_reconstructed = Matrix.zeros(2, 2)
    
    for i, (val, mult, vecs) in enumerate(eigen_data):
        vec = vecs[0] # 取出特徵向量
        
        # *** 關鍵步驟 ***
        # 譜分解公式 T = sum(lambda * |v><v|) 要求特徵向量必須歸一化 (長度為1)
        vec_norm = vec.normalized()
        
        print(f"  {i+1}. 特徵值 lambda: {val}")
        print(f"     特徵向量 v (未歸一): {vec.T}")
        print(f"     特徵向量 e (歸一化): {vec_norm.T}")
        
        # 建立投影算子 Pi = |e><e|
        # 矩陣乘法: (2x1) * (1x2) = (2x2)
        Pi = vec_norm * vec_norm.H 
        
        # 根據譜定理累加: lambda * Pi
        T_reconstructed += val * Pi
        
    print(f"\n[譜分解結果]")
    print(f"重建後的矩陣 T_rec = sum(lambda_i * P_i):\n{T_reconstructed}")
    
    # 驗證
    print(f"與原矩陣相等? {T == T_reconstructed}")


if __name__ == "__main__":
    # 依序執行所有範例
    demo_2_1_linear_transformation()
    demo_2_2_adjoint_operators()
    demo_2_3_projection_operators()
    demo_2_4_spectral_theory()