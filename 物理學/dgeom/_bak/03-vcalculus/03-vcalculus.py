import sympy as sp
from sympy.vector import CoordSys3D, curl, divergence, gradient, vector_integrate, ParametricRegion

def print_section(title):
    print("\n" + "="*70)
    print(f" {title}")
    print("="*70)

def main():
    # 初始化
    sp.init_printing(use_unicode=True)
    
    # 建立直角座標系 'N'
    # N.x, N.y, N.z 為座標變數
    # N.i, N.j, N.k 為單位基底向量
    N = CoordSys3D('N')
    
    # 定義一些通用符號
    t = sp.symbols('t')  # 參數 t (用於線積分)
    r, theta, phi = sp.symbols('r theta phi', real=True, positive=True) # 用於極座標/球座標參數化

    # ==========================================
    # 3.1 線積分 (Line Integral) - 功 (Work)
    # ==========================================
    print_section("3.1 線積分：計算向量場做的功")

    # 定義向量場 F (力場)
    # F = -y*i + x*j (一個典型的旋轉場/非保守場)
    F = -N.y * N.i + N.x * N.j
    print(f"向量場 F = {F}")

    # 定義路徑 C: 單位圓的四分之一 (從 (1,0) 到 (0,1))
    # 參數化: x = cos(t), y = sin(t), z = 0,  0 <= t <= pi/2
    curve_C = ParametricRegion((sp.cos(t), sp.sin(t), 0), (t, 0, sp.pi/2))
    
    print("路徑 C: 單位圓的第一象限弧段 (0 <= t <= pi/2)")

    # 計算線積分 (功) ∫ F · dr
    # vector_integrate 會自動處理 F · dr 的點積與參數代換
    work_done = vector_integrate(F, curve_C)
    
    print(f"計算結果 (功) W = ∫ F · dr = {work_done}")
    print(f"   -> 驗證: 在此場中逆時針移動，力與位移同向，做正功 (pi/2)")

    # ==========================================
    # 3.4 格林定理 (Green's Theorem) 驗證
    # ==========================================
    print_section("3.4 格林定理：∮ F·dr = ∬ (∇×F)·k dA")
    print("驗證對象：沿著單位圓完整一圈的環流量 vs 圓盤內的旋度積分")

    # 1. 左式：線積分 (環流量 Circulation)
    # 路徑: 完整單位圓, 0 <= t <= 2*pi
    circle_path = ParametricRegion((sp.cos(t), sp.sin(t), 0), (t, 0, 2*sp.pi))
    
    circulation = vector_integrate(F, circle_path)
    print(f"\n[左式] 環流量 ∮ F · dr = {circulation}")

    # 2. 右式：面積分 (旋度通量)
    # 計算旋度 curl F
    curl_F = curl(F)
    print(f"[中間] F 的旋度 ∇×F = {curl_F}")
    # 也就是 (0, 0, 2)，方向垂直於 xy 平面，大小為 2
    
    # 定義區域 D: 單位圓盤
    # 參數化: x = r*cos(theta), y = r*sin(theta)
    # r 從 0 到 1, theta 從 0 到 2*pi
    disk_region = ParametricRegion((r*sp.cos(theta), r*sp.sin(theta), 0), 
                                   (r, 0, 1), (theta, 0, 2*sp.pi))
    
    # 計算面積分 ∬ (∇×F) · dA
    # 注意：vector_integrate 在曲面上運算時，計算的是通量 (Flux)
    flux_curl = vector_integrate(curl_F, disk_region)
    print(f"[右式] 旋度的面積分 ∬ (∇×F) · dA = {flux_curl}")

    if circulation == flux_curl:
        print("\n✅ 格林定理驗證成功！ (2*pi == 2*pi)")
    else:
        print("\n❌ 驗證失敗")

    # ==========================================
    # 3.6 高斯散度定理 (Divergence Theorem) 驗證
    # ==========================================
    print_section("3.6 散度定理：∯ F·dS = ∭ (∇·F) dV")
    print("驗證對象：穿出球體的總通量 vs 球體內部的散度總和")

    # 定義一個向外發散的場 F_div
    # F = x*i + y*j + z*k
    F_div = N.x * N.i + N.y * N.j + N.z * N.k
    print(f"向量場 F = {F_div}")

    # 定義幾何參數: 半徑 R 的球體
    R_val = 2 # 設定半徑為 2
    
    # --- 右式：體積分 (Volume Integral) ---
    # 計算散度 ∇·F
    div_F = divergence(F_div)
    print(f"\n[中間] F 的散度 ∇·F = {div_F}") # 預期結果 1+1+1 = 3
    
    # 定義體積區域 V: 球體
    # 使用球座標參數化:
    # x = r sin(phi) cos(theta)
    # y = r sin(phi) sin(theta)
    # z = r cos(phi)
    sphere_volume = ParametricRegion(
        (r*sp.sin(phi)*sp.cos(theta), r*sp.sin(phi)*sp.sin(theta), r*sp.cos(phi)),
        (r, 0, R_val), (phi, 0, sp.pi), (theta, 0, 2*sp.pi)
    )
    
    # 計算體積分 ∭ (∇·F) dV
    # 注意：SymPy 在此需要純量積分，我們直接積分散度值
    volume_integral = vector_integrate(div_F, sphere_volume)
    print(f"[右式] 散度的體積分 ∭ (∇·F) dV = {volume_integral}")
    
    # 手算驗證: 散度為3，球體積 4/3 * pi * r^3
    # 3 * (4/3 * pi * 2^3) = 32 * pi
    
    # --- 左式：面積分 (Surface Flux) ---
    # 定義邊界表面 S: 球殼 (r 固定為 R_val)
    sphere_surface = ParametricRegion(
        (R_val*sp.sin(phi)*sp.cos(theta), R_val*sp.sin(phi)*sp.sin(theta), R_val*sp.cos(phi)),
        (phi, 0, sp.pi), (theta, 0, 2*sp.pi)
    )
    
    # 計算通量 ∯ F · dS
    flux_integral = vector_integrate(F_div, sphere_surface)
    print(f"[左式] 穿出表面的總通量 ∯ F · dS = {flux_integral}")

    if volume_integral == flux_integral:
        print("\n✅ 高斯散度定理驗證成功！ (32*pi == 32*pi)")
    else:
        print("\n❌ 驗證失敗")

if __name__ == "__main__":
    main()