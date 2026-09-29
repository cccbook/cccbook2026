from sympy import symbols, Matrix, I, sqrt, exp, integrate, oo, pi, simplify, eye, expand, conjugate
from sympy.functions import Abs

def demo_3_1_orthonormal_basis():
    print("\n" + "="*60)
    print("### 3.1 正交規範基底 (Orthonormal Basis) 與完備性")
    print("="*60)
    
    # 1. 定義一組二維空間的基底向量
    # 這裡選擇一組旋轉 45 度的基底，它們是正交且歸一的
    # |e1> = [1/sqrt(2), 1/sqrt(2)]^T
    # |e2> = [1/sqrt(2), -1/sqrt(2)]^T
    val = 1/sqrt(2)
    e1 = Matrix([val, val])
    e2 = Matrix([val, -val])
    
    print(f"基底向量 |e1>:\n{e1}")
    print(f"基底向量 |e2>:\n{e2}")
    
    # 2. 驗證正交歸一性 (Orthonormality): <ei|ej> = delta_ij
    # 注意：在矩陣運算中 <u|v> 等同於 u.H * v (u 的共軛轉置 乘 v)
    print(f"\n[驗證正交歸一性]")
    print(f"  <e1|e1>: {simplify(e1.H * e1)[0]} (應為 1)")
    print(f"  <e2|e2>: {simplify(e2.H * e2)[0]} (應為 1)")
    print(f"  <e1|e2>: {simplify(e1.H * e2)[0]} (應為 0)")
    
    # 3. 驗證完備性關係 (Completeness Relation)
    # sum(|ei><ei|) = I
    # 外積計算: |e><e| = e * e.H
    P1 = e1 * e1.H
    P2 = e2 * e2.H
    Identity_sum = simplify(P1 + P2)
    
    print(f"\n[驗證完備性 sum(|ei><ei|) = I]")
    print(f"  |e1><e1| + |e2><e2|:\n{Identity_sum}")
    print(f"  是否等於單位矩陣? {Identity_sum == eye(2)}")

    # 4. 投影分解演示
    # 任意向量 v 分解: v = <e1|v>|e1> + <e2|v>|e2>
    v = Matrix([2, 5])
    c1 = (e1.H * v)[0] # 係數 c1 = <e1|v> (投影分量)
    c2 = (e2.H * v)[0] # 係數 c2 = <e2|v>
    
    # 重組向量
    v_reconstructed = simplify(c1 * e1 + c2 * e2)
    print(f"\n[投影分解驗證]")
    print(f"  原向量 v: {v.T}")
    print(f"  分量 c1=<e1|v>: {c1}")
    print(f"  分量 c2=<e2|v>: {c2}")
    print(f"  重建向量 (c1|e1> + c2|e2>): {v_reconstructed.T}")


def demo_3_2_unitary_transformation():
    print("\n" + "="*60)
    print("### 3.2 么正變換 (Unitary Transformation)")
    print("="*60)

    # 1. 定義一個么正矩陣 U
    # 使用著名的 Hadamard Gate 矩陣 (常規化係數 1/sqrt(2))
    # 它代表了一種旋轉與反射的組合
    U = Matrix([
        [1, 1],
        [1, -1]
    ]) / sqrt(2)
    
    print(f"矩陣 U (Hadamard):\n{U}")
    
    # 2. 驗證么正性質: U^dagger * U = I
    U_dagger = U.H
    check_unitary = simplify(U_dagger * U)
    
    print(f"\n[驗證么正性 U^dagger U = I]")
    print(f"  U^dagger * U:\n{check_unitary}")
    
    # 3. 驗證保持內積性質: <Uu|Uv> = <u|v>
    # 定義兩個向量
    u = Matrix([1, 0])
    v = Matrix([I, 1]) # 包含複數 I
    
    # 變換後的向量
    u_prime = U * u
    v_prime = U * v
    
    # 計算內積
    # 原始內積 <u|v>
    inner_original = (u.H * v)[0]
    # 變換後內積 <u'|v'>
    inner_transformed = simplify((u_prime.H * v_prime)[0])
    
    print(f"\n[驗證保持內積 <Uu|Uv> = <u|v>]")
    print(f"  原始內積 <u|v>    : {inner_original}")
    print(f"  變換後內積 <u'|v'>: {inner_transformed}")
    print(f"  兩者相等? {inner_original == inner_transformed}")


def demo_3_3_function_space_L2():
    print("\n" + "="*60)
    print("### 3.3 函數空間作為向量空間 (L^2)")
    print("="*60)
    
    x = symbols('x', real=True)
    
    # 定義兩個函數 (視為無限維向量)
    # f(x) = e^(-x^2) (高斯函數, 偶函數)
    # g(x) = x * e^(-x^2) (奇函數)
    f = exp(-x**2)
    g = x * exp(-x**2)
    
    print(f"函數 (向量) f(x) = {f}")
    print(f"函數 (向量) g(x) = {g}")
    
    # 1. 計算內積 <f|g> = integral(f* g dx)
    # 注意：第一個函數要取共軛 conjugate(f)，雖然這裡是實函數沒差
    # 積分範圍：負無限到正無限 (oo)
    inner_fg = integrate(conjugate(f) * g, (x, -oo, oo))
    
    print(f"\n[計算內積 <f|g>]")
    print(f"  積分結果: {inner_fg}")
    print("  (註：結果為 0 表示這兩個函數在 L2 空間中正交)")
    
    # 2. 計算範數 (Norm) ||f|| = sqrt(<f|f>)
    norm_sq_f = integrate(conjugate(f) * f, (x, -oo, oo))
    norm_f = sqrt(norm_sq_f)
    
    print(f"\n[計算範數 ||f||]")
    print(f"  <f|f> (長度平方): {norm_sq_f}")
    print(f"  ||f|| (長度): {norm_f}")
    
    # 3. 驗證平方可積條件 (Finite Norm)
    print(f"  是否有限 (屬於 L2 空間)? {norm_f.is_finite}")


def demo_3_4_fourier_transform():
    print("\n" + "="*60)
    print("### 3.4 傅立葉變換 (Fourier Transform) 與基底變換")
    print("="*60)
    
    x, k = symbols('x k', real=True)
    a = symbols('a', positive=True) # 定義一個正實數參數
    
    # 定義函數 f(x) = e^(-a*x^2) (高斯函數)
    f_x = exp(-a * x**2)
    print(f"原始函數 (位置基底) f(x): {f_x}")
    
    # 1. 執行傅立葉變換
    # 根據文中定義: F(k) = <k|f> = integral( f(x) * (1/sqrt(2pi) * e^(-ikx)) dx )
    # 變換核 (Kernel) 為 <k|x> 的共軛，即 e^(-ikx) / sqrt(2pi)
    
    kernel = exp(-I * k * x) / sqrt(2 * pi)
    
    print("\n[執行基底變換: 位置 x -> 動量 k]")
    print("  計算積分 integral( f(x) * e^(-ikx)/sqrt(2pi) dx )...")
    
    # 執行符號積分
    f_k = integrate(f_x * kernel, (x, -oo, oo))
    
    # 簡化結果
    f_k = simplify(f_k)
    
    print(f"  變換結果 (動量基底) f_tilde(k): {f_k}")
    print("  (註：這顯示高斯函數的傅立葉變換仍為高斯函數)")
    
    # 2. 驗證 Parseval 定理 (能量守恆 / 么正性)
    # integral(|f(x)|^2) 應該等於 integral(|f(k)|^2)
    # 為了計算方便，我們將 a 設為 1 進行數值驗證
    print(f"\n[驗證 Parseval 定理 (設 a=1)]")
    
    f_x_sub = f_x.subs(a, 1)
    f_k_sub = f_k.subs(a, 1)
    
    # 計算位置空間總機率 (能量)
    norm_x = integrate(Abs(f_x_sub)**2, (x, -oo, oo))
    
    # 計算動量空間總機率 (能量)
    norm_k = integrate(Abs(f_k_sub)**2, (k, -oo, oo))
    
    print(f"  位置空間總能量 <f|f>: {norm_x}")
    print(f"  動量空間總能量 <F|F>: {norm_k}")
    print(f"  能量是否守恆? {simplify(norm_x - norm_k) == 0}")

if __name__ == "__main__":
    demo_3_1_orthonormal_basis()
    demo_3_2_unitary_transformation()
    demo_3_3_function_space_L2()
    demo_3_4_fourier_transform()