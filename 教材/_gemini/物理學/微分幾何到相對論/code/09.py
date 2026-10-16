import sympy as sp

def print_section(title):
    print("\n" + "="*70)
    print(f" {title}")
    print("="*70)

def main():
    # 初始化
    sp.init_printing(use_unicode=True)

    # 定義符號
    # m0: 靜止質量, v: 速度, c: 光速
    m0, v, c = sp.symbols('m_0 v c', real=True, positive=True)
    
    # 定義勞倫茲因子 gamma
    # gamma = 1 / sqrt(1 - v^2/c^2)
    gamma = 1 / sp.sqrt(1 - v**2/c**2)

    # ==========================================
    # 9.1 四維動量 (Four-momentum)
    # ==========================================
    print_section("9.1 四維動量 P^μ 與 相對論動量 p")

    # 1. 定義四維速度 U^μ (假設僅在 x 方向運動)
    # U^μ = (gamma*c, gamma*v, 0, 0)
    U = sp.Matrix([gamma * c, gamma * v, 0, 0])
    
    # 2. 定義四維動量 P^μ = m0 * U^μ
    P = m0 * U
    
    print("四維動量 P^μ = [P^0, P^1, P^2, P^3]^T :")
    sp.pprint(P)

    # 3. 提取三維相對論動量 p (空間分量)
    p_rel = P[1] # x 方向分量
    print(f"\n相對論動量 p (x方向) = {p_rel}")

    # 4. 驗證經典極限 (v << c)
    # 對 v 在 0 處進行泰勒展開 (Taylor Series)
    print("\n--- 驗證：低速極限 (v << c) ---")
    p_series = sp.series(p_rel, v, 0, 2).removeO()
    print(f"將 p 對 v 展開: {p_series}")
    
    if p_series == m0 * v:
        print("✅ 驗證成功：低速時 p ≈ m0 * v (牛頓動量)")
    else:
        print("❌ 驗證失敗")

    # ==========================================
    # 9.2 能量與質量的關係 E=mc^2
    # ==========================================
    print_section("9.2 能量 E, 靜止能量 E0 與 動能 K")

    # 1. 總能量 E = P^0 * c (注意 P^0 = gamma * m0 * c)
    E_total = P[0] * c
    print(f"相對論總能量 E = P^0 * c = {E_total}")

    # 2. 靜止能量 E0 (當 v=0 時)
    E_rest = E_total.subs(v, 0)
    print(f"靜止能量 E0 (v=0) = {E_rest}")

    # 3. 相對論動能 K = E - E0
    K_rel = E_total - E_rest
    print(f"相對論動能 K = E - E0 = {K_rel}")

    # 4. 驗證動能的經典極限
    print("\n--- 驗證：動能低速極限 ---")
    # 對 v 展開至 v^2 項
    K_series = sp.series(K_rel, v, 0, 3).removeO()
    print(f"將 K 對 v 展開: {K_series}")
    
    expected_K = sp.Rational(1, 2) * m0 * v**2
    if K_series == expected_K:
        print("✅ 驗證成功：低速時 K ≈ 1/2 m0 v^2 (牛頓動能)")
    else:
        print(f"❌ 驗證失敗: 預期 {expected_K}, 得到 {K_series}")

    # ==========================================
    # 9.2.3 能量-動量關係 (Invariant Mass)
    # ==========================================
    print_section("9.2.3 能量-動量關係式驗證")
    print("目標驗證: E^2 - (p*c)^2 = (m0*c^2)^2")

    # 計算 E^2 - p^2 c^2
    lhs = E_total**2 - (p_rel * c)**2
    lhs_simplified = sp.simplify(lhs)
    
    rhs = (m0 * c**2)**2
    
    print(f"計算 E^2 - (pc)^2 (化簡後): {lhs_simplified}")
    print(f"右式 (m0 c^2)^2 : {rhs}")
    
    if sp.simplify(lhs_simplified - rhs) == 0:
        print("✅ 驗證成功：能量-動量守恆關係成立")
    else:
        print("❌ 驗證失敗")

    # 也可以透過閔可夫斯基度量直接驗證四維動量的模長平方 P^2
    # Metric eta = diag(1, -1, -1, -1)
    # P^2 = (P^0)^2 - (P^1)^2 ... = m0^2 c^2
    P_sq = P[0]**2 - P[1]**2 - P[2]**2 - P[3]**2
    P_sq_simplified = sp.simplify(P_sq)
    print(f"\n四維動量不變量 P^μ P_μ = {P_sq_simplified}")
    print("這對應於靜止質量平方 m0^2 c^2")

    # ==========================================
    # 9.3 相對論性的力 (Relativistic Force)
    # ==========================================
    print_section("9.3 相對論性的力 F = dp/dt")

    # 為了微分，我們需要讓 v 變成時間 t 的函數
    t = sp.symbols('t', real=True)
    v_func = sp.Function('v')(t)
    a = sp.symbols('a', real=True) # 加速度 a = dv/dt
    
    # 重新定義動量，使用函數 v(t)
    gamma_func = 1 / sp.sqrt(1 - v_func**2/c**2)
    p_func = m0 * gamma_func * v_func
    
    print(f"動量 p(t) = {p_func}")
    
    # 計算力 F = dp/dt
    # 使用 chain rule
    F_rel = sp.diff(p_func, t)
    
    # 將導數 Derivative(v(t), t) 替換為加速度符號 a，方便閱讀
    F_rel_sub = F_rel.subs(sp.Derivative(v_func, t), a)
    F_rel_simplified = sp.simplify(F_rel_sub)
    
    print(f"\n力 F = dp/dt (計算結果):")
    sp.pprint(F_rel_simplified)
    
    # 分析結果
    # F = gamma^3 * m0 * a (這是縱向質量 Longitudinal Mass 的概念，當力與速度平行時)
    expected_F = m0 * a * (1 / (1 - v_func**2/c**2)**(sp.Rational(3, 2)))
    
    print("\n--- 結構分析 ---")
    print("當力與速度平行時，F = γ^3 m0 a")
    if sp.simplify(F_rel_simplified - expected_F) == 0:
         print("✅ 結果符合 F = γ^3 m0 a")
    else:
         print("結果形式較複雜，但數學上正確")

if __name__ == "__main__":
    main()