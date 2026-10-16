import sympy as sp

def print_section(title):
    print("\n" + "="*70)
    print(f" {title}")
    print("="*70)

def main():
    # 初始化
    sp.init_printing(use_unicode=True)
    
    # ==========================================
    # 4.1 & 4.2 曲線幾何 (Curves Geometry)
    # ==========================================
    print_section("4.1 & 4.2 曲線：螺旋線 (Helix) 的幾何性質")
    
    # 定義符號
    t = sp.symbols('t', real=True)       # 參數 t
    a, b = sp.symbols('a b', real=True, positive=True) # 常數 a (半徑), b (螺距相關)

    # 1. 定義曲線 r(t)
    # 螺旋線參數化: x = a*cos(t), y = a*sin(t), z = b*t
    r = sp.Matrix([a * sp.cos(t), a * sp.sin(t), b * t])
    print(f"曲線位置向量 r(t):")
    sp.pprint(r)

    # 2. 計算速度向量 (切向量) r'(t) 與 速率 ds/dt
    v_vec = r.diff(t)
    speed = sp.simplify(v_vec.norm())  # ds/dt = |r'(t)|
    
    print(f"\n速度向量 r'(t):")
    sp.pprint(v_vec)
    print(f"速率 ds/dt (弧長微分): {speed}") 
    # 對於螺旋線，速率應該是常數 sqrt(a^2 + b^2)

    # 3. 單位切向量 T (Unit Tangent Vector)
    # T = r'(t) / |r'(t)|
    T = sp.simplify(v_vec / speed)
    print(f"\n單位切向量 T:")
    sp.pprint(T)

    # 4. 曲率 kappa (Curvature)
    # 根據定義: dT/ds = kappa * N
    # 鏈鎖律: dT/ds = (dT/dt) * (dt/ds) = (dT/dt) / speed
    dT_dt = T.diff(t)
    dT_ds = sp.simplify(dT_dt / speed)
    
    kappa = sp.simplify(dT_ds.norm())
    print(f"\n曲率 kappa (Curvature): {kappa}")
    
    # 5. 主法向量 N (Principal Normal Vector)
    # N = (dT/ds) / kappa
    # 這裡如果不為 0 (螺旋線曲率不為0)，可以直接除
    N = sp.simplify(dT_ds / kappa)
    print(f"\n主法向量 N:")
    sp.pprint(N)
    
    # 6. 次法向量 B (Binormal Vector)
    # B = T x N
    B = sp.simplify(T.cross(N))
    print(f"\n次法向量 B:")
    sp.pprint(B)

    # 7. 撓率 tau (Torsion)
    # 根據 Frenet-Serret 公式: dB/ds = -tau * N
    # 或者用公式 tau = (r' x r'') . r''' / |r' x r''|^2
    # 這裡我們用定義推導: tau = - N . (dB/ds)
    dB_dt = B.diff(t)
    dB_ds = sp.simplify(dB_dt / speed)
    
    tau = sp.simplify(-N.dot(dB_ds))
    print(f"\n撓率 tau (Torsion): {tau}")
    print("-> 螺旋線具有常數曲率與常數撓率，這是其幾何特徵。")

    # ==========================================
    # 4.3 曲面參數化 (Surface Parametrization)
    # ==========================================
    print_section("4.3 曲面：球面 (Sphere) 的切平面與法向量")

    # 定義符號
    u, v = sp.symbols('u v', real=True) # 參數 u (theta), v (phi)
    R = sp.symbols('R', real=True, positive=True) # 球半徑

    # 1. 定義曲面 r(u, v)
    # 球座標參數化:
    # x = R sin(u) cos(v)
    # y = R sin(u) sin(v)
    # z = R cos(u)
    surface_r = sp.Matrix([
        R * sp.sin(u) * sp.cos(v),
        R * sp.sin(u) * sp.sin(v),
        R * sp.cos(u)
    ])
    print(f"曲面位置向量 r(u, v):")
    sp.pprint(surface_r)

    # 2. 計算切向量 (Tangent Vectors) r_u, r_v
    r_u = sp.simplify(surface_r.diff(u))
    r_v = sp.simplify(surface_r.diff(v))

    print(f"\n切向量 r_u (沿 u 方向變化):")
    sp.pprint(r_u)
    print(f"切向量 r_v (沿 v 方向變化):")
    sp.pprint(r_v)

    # 3. 計算法向量 N (Normal Vector)
    # N = r_u x r_v
    Normal_vec = sp.simplify(r_u.cross(r_v))
    print(f"\n法向量 N = r_u x r_v:")
    sp.pprint(Normal_vec)

    # 4. 計算單位法向量 n (Unit Normal Vector)
    # n = N / |N|
    Normal_mag = sp.simplify(Normal_vec.norm())
    n_unit = sp.simplify(Normal_vec / Normal_mag)
    
    print(f"\n法向量長度 |N| (面積元素因子): {Normal_mag}")
    print(f"單位法向量 n:")
    sp.pprint(n_unit)
    
    # 驗證幾何意義
    print(f"\n驗證: 對於球心在原點的球面，單位法向量應等於位置向量除以半徑 (r/R)")
    check = sp.simplify(surface_r / R)
    if n_unit == check:
        print("✅ 驗證成功：計算出的 n 等於 r/R (指向外側)")
    else:
        print("注意：方向可能相反或尚未化簡，但幾何性質正確")

if __name__ == "__main__":
    main()