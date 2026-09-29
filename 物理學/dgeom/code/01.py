import sympy as sp
from sympy.vector import CoordSys3D, divergence, curl, gradient

def print_section(title):
    print("\n" + "="*60)
    print(f" {title}")
    print("="*60)

def main():
    # 初始化漂亮的數學輸出 (若在 Jupyter Notebook 中可顯示 LaTeX)
    sp.init_printing(use_unicode=True)

    # ==========================================
    # 1.1 座標系的回顧 (Coordinate Systems)
    # ==========================================
    print_section("1.1 座標系的回顧：驗證轉換關係")

    # 定義符號
    x, y, z = sp.symbols('x y z', real=True)
    r, phi = sp.symbols('r phi', real=True, positive=True)
    R, theta = sp.symbols('R theta', real=True, positive=True)

    # --- 1.1.2 圓柱座標 (Cylindrical) ---
    print("--- 驗證圓柱座標轉換 (Cylindrical) ---")
    # 定義轉換公式
    x_cyl = r * sp.cos(phi)
    y_cyl = r * sp.sin(phi)
    
    print(f"定義 x = {x_cyl}")
    print(f"定義 y = {y_cyl}")
    
    # 驗證 x^2 + y^2 是否等於 r^2
    lhs_cyl = x_cyl**2 + y_cyl**2
    simplified_cyl = sp.simplify(lhs_cyl)
    print(f"計算 x^2 + y^2 = {lhs_cyl}")
    print(f"化簡後結果: {simplified_cyl} (驗證成功)\n")

    # --- 1.1.3 球座標 (Spherical) ---
    print("--- 驗證球座標轉換 (Spherical) ---")
    # 定義轉換公式
    x_sph = R * sp.sin(theta) * sp.cos(phi)
    y_sph = R * sp.sin(theta) * sp.sin(phi)
    z_sph = R * sp.cos(theta)
    
    # 驗證 x^2 + y^2 + z^2 是否等於 R^2
    lhs_sph = x_sph**2 + y_sph**2 + z_sph**2
    simplified_sph = sp.simplify(lhs_sph)
    print(f"計算 x^2 + y^2 + z^2 化簡後結果: {simplified_sph} (驗證成功)")

    # ==========================================
    # 1.2 純量場 (Scalar Fields)
    # ==========================================
    print_section("1.2 純量場：定義與等位面")

    # 建立一個直角座標系系統 'N'
    # N.x, N.y, N.z 代表空間中的座標變數，N.i, N.j, N.k 代表單位向量
    N = CoordSys3D('N')

    # 定義一個純量場 T (例如：溫度場)
    # 假設溫度 T 與距離原點的平方成反比 (或者簡單的二次函數)
    # 這裡我們用 T = 100 - (x^2 + y^2 + z^2)
    T = 100 - (N.x**2 + N.y**2 + N.z**2)

    print(f"定義純量場 T(x,y,z) = {T}")

    # --- 1.2.1 計算特定點的數值 ---
    point_dict = {N.x: 1, N.y: 2, N.z: 2}
    T_val = T.subs(point_dict)
    print(f"在點 (1, 2, 2) 的溫度值: {T_val}")

    # --- 1.2.2 等位面 (Level Surfaces) ---
    C = sp.symbols('C')
    print(f"等溫面方程式: {T} = {C}")
    print("(這在幾何上表示一系列同心球殼)")

    # 預告：計算梯度 (Gradient) - 純量場的變化率
    grad_T = gradient(T)
    print(f"\n[預告 第2章] T 的梯度 (Gradient): {grad_T}")

    # ==========================================
    # 1.3 向量場 (Vector Fields)
    # ==========================================
    print_section("1.3 向量場：定義與散度、旋度")

    # 定義一個向量場 F
    # 例子：一個繞著 z 軸旋轉的流體場 (類似漩渦)
    # F = -y*i + x*j
    F = -N.y * N.i + N.x * N.j + 0 * N.k

    print(f"定義向量場 F = {F}")
    
    # --- 1.3.2 向量場的大小 (Magnitude) ---
    magnitude_F = sp.sqrt(F.dot(F)) # 向量與自己的內積開根號
    print(f"向量場的大小 |F| = {magnitude_F}")

    # --- 1.3.3 散度與旋度 (Divergence and Curl) ---
    print("\n--- 微分運算子預覽 (第 2 章重點) ---")
    
    # 計算散度 (Divergence): 描述場的發散程度
    div_F = divergence(F)
    print(f"散度 (Divergence) ∇·F = {div_F}")
    print("   -> 結果為 0，表示流體不可壓縮 (沒有源頭也沒有匯點)")

    # 計算旋度 (Curl): 描述場的旋轉趨勢
    curl_F = curl(F)
    print(f"旋度 (Curl) ∇×F = {curl_F}")
    print("   -> 結果為 2*k，表示場沿著 z 軸 (k) 方向旋轉")

if __name__ == "__main__":
    main()