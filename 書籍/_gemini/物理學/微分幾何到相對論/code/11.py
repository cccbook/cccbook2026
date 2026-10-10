import sympy as sp

def print_section(title):
    print("\n" + "="*70)
    print(f" {title}")
    print("="*70)

def main():
    # 初始化
    sp.init_printing(use_unicode=True)

    # ==========================================
    # 10.1 弱等效原理 (WEP) 的代數演示
    # ==========================================
    print_section("10.1 弱等效原理：質量相消")
    
    # 定義符號
    # m_g: 重力質量, m_i: 慣性質量, g_field: 重力場強度, F: 力, a: 加速度
    m_g, m_i, g_field = sp.symbols('m_g m_i g')
    
    # 1. 重力 F_g = m_g * g
    F_g = m_g * g_field
    
    # 2. 牛頓第二定律 F = m_i * a
    # a = F / m_i
    acc = F_g / m_i
    
    print(f"重力 F_g = {F_g}")
    print(f"加速度 a = F_g / m_i = {acc}")
    
    # 3. 弱等效原理條件: m_g = m_i
    acc_equivalence = acc.subs(m_g, m_i)
    
    print(f"在 WEP (m_g = m_i) 下，加速度 a = {acc_equivalence}")
    print("-> 加速度與質量無關，所有物體以相同方式下落。")

    # ==========================================
    # 10.2 & 10.3 加速參考系 (Rindler Metric)
    # 這是演示等效原理最經典的幾何模型
    # ==========================================
    print_section("10.2 重力的幾何描述：Rindler 時空 (加速參考系)")
    
    # 定義座標: T (Rindler 時間), X (Rindler 空間), g_acc (固有加速度)
    T, X = sp.symbols('T X', real=True)
    g_acc = sp.symbols('a', real=True, positive=True) # 固有加速度常數

    # Rindler 度量: ds^2 = -(a*X)^2 dT^2 + dX^2
    # 注意：這裡 X > 0，且通常 a*X 對應重力勢能項
    # 這是描述一個以固有加速度 a 在平坦時空中運動的觀察者所看到的幾何
    
    # 定義 Rindler 度量張量 g_mu_nu
    # coords = [T, X]
    metric_rindler = sp.Matrix([
        [-(g_acc * X)**2, 0],
        [0, 1]
    ])
    metric_inv = metric_rindler.inv()
    
    print("Rindler 度量張量 g_μν (二維時空):")
    sp.pprint(metric_rindler)
    
    # ==========================================
    # 計算克里斯多福符號 Γ^λ_μν
    # ==========================================
    print("\n計算 Christoffel 符號 Γ^λ_μν...")
    
    coords = [T, X]
    coord_names = ['T', 'X']
    dim = 2
    
    # 初始化 Gamma[lambda][mu][nu]
    Gamma = [[[0 for _ in range(dim)] for _ in range(dim)] for _ in range(dim)]

    for lam in range(dim):
        for mu in range(dim):
            for nu in range(dim):
                res = 0
                for sigma in range(dim):
                    term = (sp.diff(metric_rindler[sigma, mu], coords[nu]) +
                            sp.diff(metric_rindler[sigma, nu], coords[mu]) -
                            sp.diff(metric_rindler[mu, nu], coords[sigma]))
                    res += 0.5 * metric_inv[lam, sigma] * term
                Gamma[lam][mu][nu] = sp.simplify(res)

    # 顯示非零項
    for lam in range(dim):
        for mu in range(dim):
            for nu in range(dim):
                if Gamma[lam][mu][nu] != 0:
                    print(f"Γ^{coord_names[lam]}_({coord_names[mu]},{coord_names[nu]}) = {Gamma[lam][mu][nu]}")

    # Γ^X_TT = a^2 * X
    # 這項在測地線方程式中產生了 "重力" 效果

    # ==========================================
    # 10.3 測地線方程式 (Geodesic Equation)
    # ==========================================
    print_section("10.3 測地線方程式：重力不是力，是幾何")
    
    # 考慮一個「靜止」在 Rindler 座標系中的物體 (dX/dtau = 0, dT/dtau != 0)
    # 我們看看它是否有「座標加速度」
    
    # 四維速度 U = [u^T, u^X]
    uT, uX = sp.symbols('u^T u^X')
    
    # 測地線方程式: d^2x^lam/dtau^2 = - Gamma^lam_mu_nu * u^mu * u^nu
    
    # 我們關注 X 方向的加速度 (lam = 1)
    acc_X = 0
    lam_X = 1 # index for X
    
    for mu in range(dim):
        for nu in range(dim):
            acc_X += -Gamma[lam_X][mu][nu] * uT * uT # 假設 uX=0 (瞬間靜止)
            # 因為我們只看 u^X = 0 的瞬間，所以含有 uX 的項都為 0
    
    acc_X = sp.simplify(acc_X)
    
    print(f"對於瞬間靜止 (u^X=0) 的粒子，其 X 方向座標加速度 d²X/dτ²:")
    print(f"a_X = {acc_X}")
    
    print("\n物理意義解析:")
    print("1. 結果不為 0 (除非 X=0)。")
    print("2. 粒子雖然「瞬間靜止」，但會自動產生加速度 (向 X=0 掉落)。")
    print("3. 這就是我們感受到的「重力」，在幾何上它來自非零的 Christoffel 符號 Γ^X_TT。")
    print("4. 在此加速系中，沒有「外力」作用，粒子只是遵循時空彎曲(由座標變換引起)的測地線。")

    # ==========================================
    # 補充：閔可夫斯基時空對比 (平坦時空)
    # ==========================================
    print_section("對比：平坦閔可夫斯基時空 (Minkowski)")
    
    # 平坦度量 g = diag(-1, 1) (在直角座標)
    # 所有 Christoffel 符號均為 0
    print("在慣性系 (t, x) 中，g_μν 是常數矩陣，所有 Γ^λ_μν = 0。")
    print("測地線方程式變為 d²x/dτ² = 0 -> 等速直線運動。")
    print("Rindler 座標只是對平坦時空做了一個非線性變換，")
    print("這展示了「座標系的選擇」如何產生「假想的重力場」。")

if __name__ == "__main__":
    main()