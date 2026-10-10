import sympy as sp

def print_section(title):
    print("\n" + "="*70)
    print(f" {title}")
    print("="*70)

def main():
    # 初始化漂亮的數學輸出
    sp.init_printing(use_unicode=True)

    # 定義基本符號
    # c: 光速, t: 時間, x, y, z: 空間座標
    c, t, x, y, z = sp.symbols('c t x y z', real=True)
    dt, dx, dy, dz = sp.symbols('dt dx dy dz', real=True)

    # ==========================================
    # 8.2 閔可夫斯基度量 (Minkowski Metric)
    # ==========================================
    print_section("8.2 閔可夫斯基度量 eta_mu_nu")
    
    # 採用書中的「時類約定」 (diag(1, -1, -1, -1))
    eta = sp.Matrix([
        [1,  0,  0,  0],
        [0, -1,  0,  0],
        [0,  0, -1,  0],
        [0,  0,  0, -1]
    ])
    
    print("閔可夫斯基度量張量 η_μν (時類約定):")
    sp.pprint(eta)

    # 定義四維位移向量 dx^μ (Contravariant)
    dx_upper = sp.Matrix([c*dt, dx, dy, dz])
    print("\n四維位移向量 dx^μ (上標):")
    sp.pprint(dx_upper)

    # 降低指標 (Lowering Indices): dx_μ = η_μν * dx^ν
    dx_lower = eta * dx_upper
    print("\n降低指標後的向量 dx_μ (下標):")
    sp.pprint(dx_lower)

    # 計算時空間隔 ds^2 = dx_μ * dx^μ
    # 這是兩個向量的點積 (dot product)
    ds_squared = sp.simplify(dx_lower.dot(dx_upper))
    print(f"\n時空間隔 ds^2 = {ds_squared}")

    # ==========================================
    # 8.3 因果結構 (Causal Structure)
    # ==========================================
    print_section("8.3 因果結構分析範例")

    def analyze_interval(delta_t, delta_x, c_val=1.0):
        """分析兩事件之間的因果關係"""
        # 計算數值化的 ds^2 = (c*dt)^2 - dx^2
        val_ds2 = (c_val * delta_t)**2 - delta_x**2
        
        print(f"事件間隔: cΔt = {c_val*delta_t}, Δx = {delta_x}")
        print(f"計算得 ds^2 = {val_ds2}")
        
        if val_ds2 > 0:
            relation = "時類間隔 (Timelike) -> 具有因果關係"
            # 計算原時 d_tau = sqrt(ds^2) / c
            tau = sp.sqrt(val_ds2) / c_val
            extra = f"物體經歷的原時 Δτ = {tau}"
        elif val_ds2 == 0:
            relation = "零類/光類間隔 (Null/Lightlike) -> 光速傳遞"
            extra = "事件位在光錐上"
        else:
            relation = "空間類間隔 (Spacelike) -> 無因果關係"
            extra = "沒有訊息能從事件 A 傳到事件 B"
            
        print(f"結果: {relation}")
        print(f"說明: {extra}\n")

    # 範例 1: 訊號從 A 傳到 B (低於光速)
    print("範例 [1]: Δt = 5s, Δx = 3光秒")
    analyze_interval(5, 3)

    # 範例 2: 光訊號
    print("範例 [2]: Δt = 4s, Δx = 4光秒")
    analyze_interval(4, 4)

    # 範例 3: 遙遠的事件 (超光速要求)
    print("範例 [3]: Δt = 1s, Δx = 10光秒")
    analyze_interval(1, 10)

    # ==========================================
    # 8.1 四維速度與四維動量預覽
    # ==========================================
    print_section("8.1 四維向量應用：四維速度 U^μ")
    
    # 假設一個物體在 x 方向以速度 v 運動
    v = sp.symbols('v', real=True)
    # 勞倫茲因子 gamma
    gamma = 1 / sp.sqrt(1 - (v/c)**2)
    
    # 四維速度 U^μ = (gamma*c, gamma*v_x, gamma*v_y, gamma*v_z)
    U_upper = sp.Matrix([gamma*c, gamma*v, 0, 0])
    print("在 x 方向運動的四維速度 U^μ:")
    sp.pprint(U_upper)
    
    # 驗證 U^μ * U_μ = c^2 (不變量)
    U_lower = eta * U_upper
    U_squared = sp.simplify(U_lower.dot(U_upper))
    print(f"\n驗證四維速度的模長 U^μ U_μ (應為 c^2):")
    sp.pprint(U_squared)

if __name__ == "__main__":
    main()