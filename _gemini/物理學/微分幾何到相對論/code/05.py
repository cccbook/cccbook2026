import sympy as sp

def print_section(title):
    print("\n" + "="*70)
    print(f" {title}")
    print("="*70)

def main():
    # 初始化
    sp.init_printing(use_unicode=True)

    # ==========================================
    # 5.1 & 5.2 座標變換與雅可比矩陣
    # ==========================================
    print_section("5.1 & 5.2 座標變換：直角 -> 極座標")

    # 定義座標變數
    # 原始座標 (Cartesian) x, y (僅作標記用)
    # 新座標 (Polar) r, theta
    r, theta = sp.symbols('r theta', real=True, positive=True)

    # 定義座標變換函數 (這是表達式，含有 r 和 theta)
    x_expr = r * sp.cos(theta)
    y_expr = r * sp.sin(theta)

    print(f"變換關係: x = {x_expr}, y = {y_expr}")

    # 計算雅可比矩陣 (Jacobian Matrix) J_mu_nu = dx^mu / dx'^nu
    # 【修正重點】：這裡必須放入變換後的表達式 [x_expr, y_expr]，而不是符號 [x, y]
    coords_expr = sp.Matrix([x_expr, y_expr]) 
    coords_new = sp.Matrix([r, theta])
    
    # 計算 Jacobian: d(x_expr)/d(r), d(x_expr)/d(theta) ...
    J = coords_expr.jacobian(coords_new)
    
    print("\n雅可比矩陣 J (基底變換矩陣):")
    sp.pprint(J)
    
    # ==========================================
    # 5.3 度量張量 (Metric Tensor) g_mu_nu
    # ==========================================
    print_section("5.3 度量張量 g_μν (極座標)")

    # 在直角座標系中，度量張量是單位矩陣 (歐幾里得空間)
    g_cartesian = sp.eye(2) 

    # 利用張量變換規則計算極座標下的度量張量
    # g'_ab = J^T * g * J  (矩陣形式的變換)
    # 通用的坐標變換公式 g_new = J.T * g_old * J
    g_polar = sp.simplify(J.T * g_cartesian * J)

    print("極座標下的度量張量 g_μν:")
    sp.pprint(g_polar)
    print("-> 對角線元素為 1 和 r^2，這就是為何線元 ds^2 = dr^2 + r^2 dθ^2")

    # 計算逆度量張量 g^μν (Inverse Metric)
    # 用於升降指標
    g_polar_inv = g_polar.inv()
    print("\n逆度量張量 g^μν:")
    sp.pprint(g_polar_inv)

    # ==========================================
    # 5.4 克里斯托費爾符號 (Christoffel Symbols)
    # ==========================================
    print_section("5.4 克里斯托費爾符號 Γ^λ_μν")
    print("公式: Γ^λ_μν = 1/2 * g^λσ * (∂g_σμ/∂x^ν + ∂g_σν/∂x^μ - ∂g_μν/∂x^σ)")

    # 定義一個函數來計算 Gamma
    # 輸入: metric (矩陣), inverse_metric (矩陣), coords (列表)
    def calculate_christoffel(g, g_inv, variables):
        dim = len(variables)
        # 初始化 3維陣列 (列表的列表的列表) 來儲存 Gamma[lambda][mu][nu]
        Gamma = [[[0 for _ in range(dim)] for _ in range(dim)] for _ in range(dim)]
        
        for lam in range(dim): # 上標 lambda
            for mu in range(dim): # 下標 mu
                for nu in range(dim): # 下標 nu
                    sum_term = 0
                    for sigma in range(dim): # 虛擬指標 sigma 求和
                        # ∂g_σμ / ∂x^ν
                        term1 = sp.diff(g[sigma, mu], variables[nu])
                        # ∂g_σν / ∂x^μ
                        term2 = sp.diff(g[sigma, nu], variables[mu])
                        # - ∂g_μν / ∂x^σ
                        term3 = -sp.diff(g[mu, nu], variables[sigma])
                        
                        sum_term += 0.5 * g_inv[lam, sigma] * (term1 + term2 + term3)
                    
                    Gamma[lam][mu][nu] = sp.simplify(sum_term)
        return Gamma

    # 計算極座標的 Gamma
    Gamma_polar = calculate_christoffel(g_polar, g_polar_inv, [r, theta])

    # 顯示非零項
    print("\n非零的 Christoffel 符號:")
    coords_str = ['r', 'θ']
    for lam in range(2):
        for mu in range(2):
            for nu in range(2):
                val = Gamma_polar[lam][mu][nu]
                if val != 0:
                    print(f"Γ^{coords_str[lam]}_({coords_str[mu]},{coords_str[nu]}) = {val}")

    print("\n物理意義:")
    print("Γ^r_(θ,θ) = -r : 對應離心力項 (centrifugal force)")
    print("Γ^θ_(r,θ) = 1/r : 對應柯氏力項 (Coriolis force) 的一部分")

    # ==========================================
    # 5.4 應用：共變導數 (Covariant Derivative)
    # ==========================================
    print_section("5.4 應用：向量場的共變導數 ∇_ν V^μ")
    
    # 定義一個反變向量場 V = (V^r, V^theta)
    # 假設 V^r = r, V^theta = 0 (徑向流出的向量場)
    Vr = r
    Vtheta = 0
    V_vec = [Vr, Vtheta]
    
    print(f"考慮向量場 V^μ = ({Vr}, {Vtheta})")

    # 計算 ∇_θ V^θ (theta 方向分量對 theta 的共變導數)
    # 公式: ∇_ν V^μ = ∂V^μ/∂x^ν + Γ^μ_λν V^λ
    # 我們只算其中一個分量作為示範: ∇_theta V^theta
    
    mu = 1 # theta index (上標)
    nu = 1 # theta index (下標，微分方向)
    
    # 1. 普通偏導數部分 ∂V^θ / ∂θ
    partial_deriv = sp.diff(V_vec[mu], coords_new[nu])
    
    # 2. 連線修正項 Γ^θ_λθ * V^λ
    connection_term = 0
    for lam in range(2):
        connection_term += Gamma_polar[mu][lam][nu] * V_vec[lam]
        
    covariant_deriv = sp.simplify(partial_deriv + connection_term)
    
    print(f"\n計算分量 ∇_θ V^θ:")
    print(f"普通偏導數項 ∂V^θ/∂θ = {partial_deriv}")
    print(f"連線修正項 Γ^θ_λθ V^λ = {connection_term}")
    print(f"共變導數結果 ∇_θ V^θ = {covariant_deriv}")
    
    # 散度是共變導數的縮併: ∇_μ V^μ = ∇_r V^r + ∇_θ V^θ
    # 我們再算一下 ∇_r V^r
    mu2, nu2 = 0, 0 # r, r
    term1_r = sp.diff(V_vec[mu2], coords_new[nu2]) # ∂r/∂r = 1
    term2_r = sum([Gamma_polar[mu2][lam][nu2] * V_vec[lam] for lam in range(2)]) # Γ^r_rr * V^r + ... = 0
    cov_r = term1_r + term2_r
    
    print(f"\n驗證散度 (Divergence) ∇_μ V^μ:")
    print(f"∇_r V^r = {cov_r}")
    print(f"∇_θ V^θ = {covariant_deriv}")
    print(f"總散度 = {cov_r + covariant_deriv}")
    print("在平直空間極座標中，徑向場 V=r 的散度應為 (1/r)∂(r*V^r)/∂r = (1/r)∂(r^2)/∂r = 2")
    print("這裡我們得到的結果是 1 + 1/r * r = 2，驗證成功！")

if __name__ == "__main__":
    main()