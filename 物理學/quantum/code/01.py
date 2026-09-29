from sympy import symbols, I, sqrt, expand
from sympy.physics.quantum import Bra, Ket, InnerProduct, OuterProduct, Dagger, qapply, represent
from sympy.physics.quantum.hilbert import ComplexSpace
# 關鍵修改：引入 Qubit 來取代通用的 Ket
from sympy.physics.quantum.qubit import Qubit 

def demo_vector_space():
    print("=== 1.1 向量空間與線性組合 ===")
    # 定義抽象的 Ket 向量 |0> 和 |1>
    k0 = Ket('0')
    k1 = Ket('1')
    
    # 定義複數純量 (I 是 SymPy 中的虛數單位 i)
    a = 3
    b = 2 + 5*I
    
    # 線性組合：au + bv
    psi = a * k0 + b * k1
    
    print(f"向量 |0>: {k0}")
    print(f"向量 |1>: {k1}")
    print(f"線性組合 |psi> = {psi}")
    print("-" * 30)

demo_vector_space()

def demo_inner_product():
    print("=== 1.2 內積與範數 ===")
    u = Ket('u')
    v = Ket('v')
    
    # 1. 定義內積 <u|v>
    ip = InnerProduct(Bra('u'), v)
    print(f"符號表示 <u|v>: {ip}")
    
    # 2. 共軛對稱性驗證: <u|v> 的共軛應該等於 <v|u>
    # Dagger() 函數負責計算共軛轉置
    ip_conjugate = Dagger(ip)
    print(f"<u|v> 的共軛: {ip_conjugate}")  # 輸出應為 <v|u>
    
    # 3. 計算範數 (Norm)
    # 假設我們有一個具體的向量 |psi> = 3|0> + 4i|1>
    # 這裡假設 |0> 和 |1> 是正交歸一的
    psi = 3 * Ket('0') + 4*I * Ket('1')
    
    # 計算 <psi|psi>
    # qapply 用於執行運算，將 Bra 作用在 Ket 上
    # 需要告訴 SymPy 這是量子位元空間 (Qubit)，或者手動展開
    dag_psi = Dagger(psi) # 自動轉為 Bra: 3<0| - 4i<1|
    
    print(f"向量 |psi>: {psi}")
    print(f"對應的 <psi|: {dag_psi}")
    
    # 計算內積 (長度的平方)
    norm_sq = dag_psi * psi
    # expand 用於展開代數式，假設 <0|0>=1, <1|1>=1, <0|1>=0
    # 在純符號運算中，我們通常使用 represent 來轉成矩陣計算數值，如下：
    
    print("-" * 30)

demo_inner_product()

def demo_hilbert_class():
    print("=== 1.3 希爾伯特空間物件 ===")
    # 定義一個 2 維的複數希爾伯特空間 C^2 (例如一個 Qubit)
    H = ComplexSpace(2)
    
    print(f"空間定義: {H}")
    print(f"空間維度: {H.dimension}")
    
    # 檢查向量是否屬於該空間 (概念演示)
    psi = Ket('psi')
    psi.hilbert_space = H
    print(f"向量 |psi> 所屬空間: {psi.hilbert_space}")
    print("-" * 30)

demo_hilbert_class()

def demo_hilbert_class():
    print("=== 1.3 希爾伯特空間物件 ===")
    # 定義一個 2 維的複數希爾伯特空間 C^2 (例如一個 Qubit)
    H = ComplexSpace(2)
    
    print(f"空間定義: {H}")
    print(f"空間維度: {H.dimension}")
    
    # 檢查向量是否屬於該空間 (概念演示)
    psi = Ket('psi')
    psi.hilbert_space = H
    print(f"向量 |psi> 所屬空間: {psi.hilbert_space}")
    print("-" * 30)

demo_hilbert_class()

def demo_dirac_notation():
    print("=== 1.4 狄拉克符號與矩陣表示 (修正版) ===")
    
    # 修正：使用 Qubit 物件，而不是通用的 Ket
    # Qubit('0') 預設對應到 [1, 0]^T
    # Qubit('1') 預設對應到 [0, 1]^T
    q0 = Qubit('0')
    q1 = Qubit('1')
    
    # 定義任意向量 |psi> = a|0> + b|1>
    a, b = symbols('a b')
    psi = a * q0 + b * q1
    
    print("1. Ket (列向量) 表示:")
    # represent 會自動辨識 Qubit 並將其轉為標準基底矩陣
    psi_matrix = represent(psi)
    print(psi_matrix) 
    # 輸出: Matrix([[a], [b]])
    
    print("\n2. Bra (行向量) 表示:")
    phi_bra = Dagger(psi) # 取共軛轉置變成 Bra
    phi_matrix = represent(phi_bra)
    print(phi_matrix)
    # 輸出: Matrix([[conjugate(a), conjugate(b)]])
    
    print("\n3. 外積 (Outer Product) 與算符:")
    # 投影算符 P = |0><0|
    # 注意：這裡的運算會自動處理矩陣維度
    P0 = OuterProduct(q0, Dagger(q0))
    print(f"算符 |0><0|: {P0}")
    
    # 將算符表示為矩陣
    P0_matrix = represent(P0)
    print("算符的矩陣形式:")
    print(P0_matrix)
    # 輸出: Matrix([[1, 0], [0, 0]])
    
    print("\n4. 單位分解驗證:")
    # P0 + P1 應該等於單位矩陣 I
    P1 = OuterProduct(q1, Dagger(q1))
    Identity_matrix = represent(P0 + P1)
    print("|0><0| + |1><1| =")
    print(Identity_matrix)
    print("-" * 30)

demo_dirac_notation()

