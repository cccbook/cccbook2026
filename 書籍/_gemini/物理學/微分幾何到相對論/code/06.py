import sympy as sp

def print_section(title):
    print("\n" + "="*70)
    print(f" {title}")
    print("="*70)

def main():
    # 初始化
    sp.init_printing(use_unicode=True)

    # ==========================================
    # 0. 設定座標系與度量張量 (Metric Tensor)
    # ==========================================
    print_section("設定：史瓦西時空 (Schwarzschild Spacetime)")

    # 定義座標: t (時間), r (徑向), theta (極角), phi (方位角)
    t, r, theta, phi = sp.symbols('t r theta phi')
    coords = [t, r, theta, phi]
    coord_names = ['t', 'r', 'θ', 'φ']
    
    # 定義物理常數: rs (史瓦西半徑 = 2GM/c^2)
    rs = sp.symbols('r_s', real=True)

    # 定義度量張量 g_μν (Covariant Metric)
    # ds^2 = -(1-rs/r)dt^2 + (1-rs/r)^-1 dr^2 + r^2 dθ^2 + r^2 sin^2θ dφ^2
    g = sp.Matrix([
        [-(1 - rs/r), 0, 0, 0],
        [0, 1/(1 - rs/r), 0, 0],
        [0, 0, r**2, 0],
        [0, 0, 0, r**2 * sp.sin(theta)**2]
    ])

    # 計算逆度量張量 g^μν (Inverse Metric)
    g_inv = g.inv()

    print("度量張量 g_μν:")
    sp.pprint(g)

    # ==========================================
    # 6.1 克里斯多福符號 (Christoffel Symbols)
    # ==========================================
    print_section("6.1 克里斯多福符號 Γ^μ_αβ")
    print("公式: Γ^μ_αβ = 1/2 * g^μλ * (∂g_λα/∂x^β + ∂g_λβ/∂x^α - ∂g_αβ/∂x^λ)")

    dim = 4
    # 初始化 Gamma[mu][alpha][beta]
    Gamma = [[[0 for _ in range(dim)] for _ in range(dim)] for _ in range(dim)]

    # 計算迴圈
    for mu in range(dim):
        for alpha in range(dim):
            for beta in range(dim):
                res = 0
                for lam in range(dim): # lam = lambda
                    term = (sp.diff(g[lam, alpha], coords[beta]) +
                            sp.diff(g[lam, beta], coords[alpha]) -
                            sp.diff(g[alpha, beta], coords[lam]))
                    res += 0.5 * g_inv[mu, lam] * term
                Gamma[mu][alpha][beta] = sp.simplify(res)

    # 顯示非零項
    print("\n非零的 Christoffel 符號 (僅列出部分代表):")
    count = 0
    for mu in range(dim):
        for alpha in range(dim):
            for beta in range(dim):
                # 利用對稱性，只印出 alpha <= beta
                if Gamma[mu][alpha][beta] != 0 and alpha <= beta:
                    print(f"Γ^{coord_names[mu]}_({coord_names[alpha]},{coord_names[beta]}) = {Gamma[mu][alpha][beta]}")
                    count += 1
    
    # ==========================================
    # 6.1 應用：測地線方程式 (Geodesic Equation)
    # ==========================================
    print_section("6.1 應用：徑向測地線方程式")
    print("公式: d²x^μ/dτ² + Γ^μ_αβ (dx^α/dτ)(dx^β/dτ) = 0")
    
    # 我們以半徑 r 的方程式為例 (μ=1)
    # 假設物體只在赤道面運動 (theta = pi/2, dtheta/dtau = 0)
    # 變數: u^t = dt/dτ, u^r = dr/dτ, u^φ = dφ/dτ
    ut, ur, uphi = sp.symbols('u^t u^r u^phi')
    u_vec = [ut, ur, 0, uphi] # theta 分量為 0

    mu_r = 1 # index for r
    geo_eq_r = 0
    for alpha in range(dim):
        for beta in range(dim):
            geo_eq_r += Gamma[mu_r][alpha][beta] * u_vec[alpha] * u_vec[beta]
    
    geo_eq_r = sp.simplify(geo_eq_r)
    
    print(f"\n徑向加速度項 (d²r/dτ²) = - ({geo_eq_r})")
    print("-> 此方程式描述了重力如何影響半徑 r 的變化 (即引力吸引)")

    # ==========================================
    # 6.3 黎曼曲率張量 (Riemann Curvature Tensor)
    # ==========================================
    print_section("6.3 黎曼曲率張量 R^ρ_σ_μν")
    print("定義: R^ρ_σμν = ∂_μ Γ^ρ_νσ - ∂_ν Γ^ρ_μσ + Γ^ρ_μλ Γ^λ_νσ - Γ^ρ_νλ Γ^λ_μσ")

    # 初始化 Riemann[rho][sigma][mu][nu]
    # 注意：計算量較大，我們只計算幾個關鍵分量來展示
    # 我們計算 R^t_rtr (時間-半徑平面的曲率)
    
    def calc_riemann_component(rho, sigma, mu, nu):
        # Term 1: ∂_μ Γ^ρ_νσ
        t1 = sp.diff(Gamma[rho][nu][sigma], coords[mu])
        # Term 2: ∂_ν Γ^ρ_μσ
        t2 = sp.diff(Gamma[rho][mu][sigma], coords[nu])
        
        # Term 3 & 4: Summation over lambda
        t3 = 0
        t4 = 0
        for lam in range(dim):
            t3 += Gamma[rho][mu][lam] * Gamma[lam][nu][sigma]
            t4 += Gamma[rho][nu][lam] * Gamma[lam][mu][sigma]
            
        return sp.simplify(t1 - t2 + t3 - t4)

    # 計算 R^t_rtr (indices: 0, 1, 0, 1)
    # 這分量與潮汐力有關
    R_t_rtr = calc_riemann_component(0, 1, 0, 1) # rho=t, sigma=r, mu=t, nu=r
    
    print(f"\n計算特定分量 R^t_rtr:")
    print(f"R^t_rtr = {R_t_rtr}")
    
    # 補充：如果 rs = 0 (無質量)，則此項為 0 (平坦時空)
    print("\n物理意義:")
    print("此非零分量表示時空在時間與徑向方向上的彎曲。")
    print("這就是導致兩個在不同半徑的靜止時鐘速率不同的原因 (重力時間膨脹)。")

    # ==========================================
    # 6.2 里奇曲率張量 (Ricci Tensor) 與 真空解驗證
    # ==========================================
    print_section("6.2 里奇張量 R_μν 與 愛因斯坦方程式驗證")
    print("定義: R_μν = R^λ_μλν (黎曼張量的縮併)")
    
    print("\n正在計算 R_rr (徑向分量)... (請稍候)")
    
    # 計算 R_rr (indices: 1, 1)
    # R_rr = sum(R^λ_rλr) for λ in 0..3
    R_rr = 0
    mu_fixed = 1 # r
    nu_fixed = 1 # r
    
    for lam in range(dim):
        term = calc_riemann_component(lam, mu_fixed, lam, nu_fixed)
        R_rr += term
        
    R_rr = sp.simplify(R_rr)
    print(f"R_rr = {R_rr}")
    
    print("\n結果分析:")
    if R_rr == 0:
        print("✅ R_rr = 0。")
        print("這是正確的！史瓦西解是愛因斯坦場方程式的「真空解」。")
        print("在真空區域 (T_μν = 0)，里奇張量 R_μν 必須為 0。")
        print("雖然 R_μν = 0，但黎曼張量 R^ρ_σμν 不為 0 (如上所示)，表示時空仍是彎曲的(有潮汐力)。")
    else:
        print(f"計算結果不為 0: {R_rr}")

    # ==========================================
    # 6.4 比安基恆等式 (Bianchi Identity) 說明
    # ==========================================
    print_section("6.4 比安基恆等式")
    print("數學形式: ∇_λ R_ρσμν + ∇_μ R_ρσνλ + ∇_ν R_ρσλμ = 0")
    print("\n由於計算共變導數極為繁瑣，此處僅作概念說明：")
    print("此恆等式保證了愛因斯坦張量 G_μν = R_μν - 1/2 g_μν R 的散度為零 (∇^μ G_μν = 0)。")
    print("這對應到物理上的「能量-動量守恆定律」。")

if __name__ == "__main__":
    main()