import sympy as sp
from sympy.vector import CoordSys3D, gradient, divergence, curl, laplacian, directional_derivative

def print_section(title):
    print("\n" + "="*60)
    print(f" {title}")
    print("="*60)

def main():
    # 初始化漂亮的數學輸出
    sp.init_printing(use_unicode=True)

    # 建立基本的直角座標系 'R' (Cartesian)
    # R.x, R.y, R.z 為座標變數
    # R.i, R.j, R.k 為單位基底向量
    R = CoordSys3D('R')

    # ==========================================
    # 2.1 梯度 (Gradient) ∇f
    # ==========================================
    print_section("2.1 梯度 (Gradient): 純量場的變化率")

    # 定義一個純量場 f (例如：電位或溫度)
    # 這裡使用 f = x^2 * y + z
    f = R.x**2 * R.y + R.z
    print(f"純量場 f = {f}")

    # 計算梯度 ∇f
    grad_f = gradient(f)
    print(f"梯度 ∇f = {grad_f}")
    print("   -> 幾何意義: 指向 f 增加最快的方向，且垂直於等值面")

    # 應用：方向導數 (Directional Derivative)
    # 定義一個方向向量 u = i + j (尚未歸一化)
    v = R.i + R.j
    # 計算 f 沿著 v 方向的導數
    # 注意: SymPy 的 directional_derivative 會處理方向向量
    dir_deriv = directional_derivative(f, v)
    print(f"f 在向量 (i+j) 方向上的方向導數 = {dir_deriv}")

    # ==========================================
    # 2.2 散度 (Divergence) ∇·F
    # ==========================================
    print_section("2.2 散度 (Divergence): 通量密度的測量")

    # 定義一個向量場 F (例如：輻射狀的場)
    # F = x*i + y*j + z*k
    F = R.x * R.i + R.y * R.j + R.z * R.k
    print(f"向量場 F = {F}")

    # 計算散度 ∇·F
    div_F = divergence(F)
    print(f"散度 ∇·F = {div_F}")
    
    # 判斷源或彙
    if div_F > 0:
        print("   -> 結果 > 0，表示該區域是 '源' (Source)，場線向外發散")
    elif div_F < 0:
        print("   -> 結果 < 0，表示該區域是 '彙' (Sink)，場線向內彙聚")
    else:
        print("   -> 結果 = 0，表示是無散場 (Solenoidal)")

    # ==========================================
    # 2.3 旋度 (Curl) ∇×G
    # ==========================================
    print_section("2.3 旋度 (Curl): 場的旋轉趨勢")

    # 定義一個旋轉的向量場 G (例如：剛體旋轉流體)
    # G = -y*i + x*j
    G = -R.y * R.i + R.x * R.j
    print(f"向量場 G = {G}")

    # 計算旋度 ∇×G
    curl_G = curl(G)
    print(f"旋度 ∇×G = {curl_G}")
    print("   -> 幾何意義: 指向旋轉軸方向 (這裡是 z 軸/k 方向)")

    # 驗證：保守場的旋度為 0
    # 我們知道梯度場是保守場，我們取上面的 grad_f 來測試
    curl_grad_f = curl(grad_f)
    print(f"驗證：梯度場 ∇f 的旋度 (∇×∇f) = {curl_grad_f}")
    print("   -> 物理意義: 靜電場(保守場)沒有旋轉特性")

    # ==========================================
    # 2.4 拉普拉斯算子 (Laplacian) ∇²
    # ==========================================
    print_section("2.4 拉普拉斯算子 (Laplacian) 與物理方程式")

    # 定義一個調和函數 (Harmonic Function) h
    # 拉普拉斯方程式要求 ∇²h = 0
    # 例子：h = x^2 - y^2 (馬鞍面)
    h = R.x**2 - R.y**2
    print(f"測試函數 h = {h}")

    # 計算拉普拉斯算子 ∇²h
    lap_h = laplacian(h)
    print(f"拉普拉斯運算結果 ∇²h = {lap_h}")
    print("   -> 結果為 0，滿足拉普拉斯方程式 (Laplace's Equation)")

    # 定義一個非調和函數 (例如電荷分佈)
    # p = x^2 + y^2 + z^2
    p = R.x**2 + R.y**2 + R.z**2
    print(f"\n測試函數 p = {p}")
    lap_p = laplacian(p)
    print(f"拉普拉斯運算結果 ∇²p = {lap_p}")
    print("   -> 結果不為 0，對應泊松方程式 (Poisson's Equation) 的源項")

    # ==========================================
    # 特殊座標系 (Coordinates Systems)
    # ==========================================
    print_section("補充：特殊座標系 (球座標 Spherical)")
    
    # 定義球座標系 'S'
    # S.r (半徑), S.theta (極角), S.phi (方位角)
    S = CoordSys3D('S', transformation='spherical')
    
    # 定義一個僅與半徑 r 有關的純量場 (例如點電荷電位 V = 1/r)
    # 注意：在 SymPy 中要避免除以 0，這裡演示數學形式
    V = 1 / S.r
    print(f"球座標純量場 V = {V}")

    # 計算梯度 (SymPy 會自動套用球座標的複雜公式)
    # 公式：(∂V/∂r) e_r + ...
    grad_V = gradient(V)
    print(f"球座標下的梯度 ∇V = {grad_V}")
    
    # 計算拉普拉斯 (SymPy 會自動套用球座標的複雜微分算子)
    # 公式：(1/r^2) * ∂/∂r(r^2 ∂V/∂r) ...
    lap_V = laplacian(V)
    print(f"球座標下的拉普拉斯 ∇²V = {lap_V}")
    print("   -> 對於 1/r 電位，除原點外，拉普拉斯值應為 0")

if __name__ == "__main__":
    main()