from sympy import symbols, Matrix, I, sqrt, exp, cos, sin, pi, simplify, eye, trace, det
from sympy.physics.quantum.constants import hbar

def demo_9_1_spin_quantization():
    print("\n" + "="*60)
    print("### 9.1 斯特恩-革拉赫實驗：自旋算符與量化")
    print("="*60)
    
    # 定義自旋 Z 方向算符 Sz
    # Sz = (hbar/2) * [1, 0; 0, -1]
    Sz = (hbar / 2) * Matrix([
        [1, 0],
        [0, -1]
    ])
    
    print(f"自旋算符 Sz:\n{Sz}")
    
    # 計算本徵值 (Eigenvalues)
    # 預期結果應為 +hbar/2 與 -hbar/2
    eigenvals = Sz.eigenvals()
    
    print(f"\nSz 的本徵值 (Eigenvalues):")
    for val, mult in eigenvals.items():
        print(f"  數值: {val} (重數: {mult})")
    print("這對應了實驗中觀察到的離散分裂：自旋向上與自旋向下。")

def demo_9_2_pauli_matrices():
    print("\n" + "="*60)
    print("### 9.2 鮑立矩陣 (Pauli Matrices) 性質驗證")
    print("="*60)
    
    # 定義鮑立矩陣
    sigma_x = Matrix([[0, 1], [1, 0]])
    sigma_y = Matrix([[0, -I], [I, 0]])
    sigma_z = Matrix([[1, 0], [0, -1]])
    
    print(f"Sigma X:\n{sigma_x}")
    print(f"Sigma Y:\n{sigma_y}")
    print(f"Sigma Z:\n{sigma_z}")
    
    # 1. 驗證代數關係: sigma_i^2 = I
    print(f"\n[驗證性質 1] 平方等於單位矩陣 (sigma^2 = I)")
    sq_x = sigma_x**2
    sq_y = sigma_y**2
    sq_z = sigma_z**2
    identity = eye(2)
    
    print(f"  X^2 == I ? {sq_x == identity}")
    print(f"  Y^2 == I ? {sq_y == identity}")
    print(f"  Z^2 == I ? {sq_z == identity}")
    
    # 2. 驗證對易關係: [sigma_x, sigma_y] = 2i * sigma_z
    print(f"\n[驗證性質 2] 對易關係 [Sx, Sy] = 2iSz")
    comm_xy = sigma_x * sigma_y - sigma_y * sigma_x
    target = 2 * I * sigma_z
    
    print(f"  [Sx, Sy] 計算結果:\n{comm_xy}")
    print(f"  是否等於 2iSz ? {comm_xy == target}")
    
    # 3. 驗證跡 (Trace) 為 0
    print(f"\n[驗證性質 3] Trace 為 0")
    print(f"  Tr(Sx) = {trace(sigma_x)}")
    print(f"  Tr(Sy) = {trace(sigma_y)}")
    print(f"  Tr(Sz) = {trace(sigma_z)}")
    
    # 4. 驗證行列式 (Determinant) 為 -1
    print(f"\n[驗證性質 4] 行列式為 -1")
    print(f"  Det(Sx) = {det(sigma_x)}")
    print(f"  Det(Sy) = {det(sigma_y)}")
    print(f"  Det(Sz) = {det(sigma_z)}")

def demo_9_3_bloch_sphere():
    print("\n" + "="*60)
    print("### 9.3 量子位元與布洛赫球 (Bloch Sphere) 表示")
    print("="*60)
    
    # 定義角度符號
    theta = symbols('theta', real=True)
    phi = symbols('phi', real=True)
    
    # 定義基底向量 |0> 和 |1>
    ket_0 = Matrix([1, 0])
    ket_1 = Matrix([0, 1])
    
    # 定義布洛赫球參數化的通用量子態
    # |psi> = cos(theta/2)|0> + e^(i*phi)sin(theta/2)|1>
    psi_bloch = cos(theta/2) * ket_0 + exp(I*phi) * sin(theta/2) * ket_1
    
    print(f"布洛赫球通用態向量 |psi(theta, phi)>:")
    print(psi_bloch)
    
    print("\n[驗證特殊點映射]")
    
    # 1. 北極點 (North Pole): theta = 0
    # 應該對應到 |0> = [1, 0]^T
    psi_north = psi_bloch.subs(theta, 0)
    print(f"1. 北極點 (theta=0):")
    print(f"   {psi_north}  => 對應態 |0>")
    
    # 2. 南極點 (South Pole): theta = pi
    # 應該對應到 e^(i*phi) * |1> (忽略全域相位後即為 |1>)
    psi_south = psi_bloch.subs(theta, pi)
    print(f"2. 南極點 (theta=pi):")
    print(f"   {psi_south}")
    print(f"   (注意: e^(i*phi) 是全域相位，物理上等同於 |1> = [0, 1]^T)")
    
    # 3. 赤道點 (Equator): theta = pi/2, phi = 0
    # 應該對應到 |+> = 1/sqrt(2) (|0> + |1>)
    psi_plus = psi_bloch.subs({theta: pi/2, phi: 0})
    print(f"3. 赤道點 (theta=pi/2, phi=0):")
    print(f"   {psi_plus}")
    
    # 驗證是否等於 1/sqrt(2) * [1, 1]^T
    target_plus = Matrix([1, 1]) / sqrt(2)
    print(f"   是否等於 |+> ? {simplify(psi_plus - target_plus) == Matrix([0,0])}")

if __name__ == "__main__":
    demo_9_1_spin_quantization()
    demo_9_2_pauli_matrices()
    demo_9_3_bloch_sphere()