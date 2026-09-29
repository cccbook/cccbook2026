import sympy as sp
import matplotlib.pyplot as plt
import numpy as np

def print_section(title):
    print("\n" + "="*70)
    print(f" {title}")
    print("="*70)

def main():
    # 初始化
    sp.init_printing(use_unicode=True)

    # ==========================================
    # 12.1 史瓦西解 (Schwarzschild Solution)
    # ==========================================
    print_section("12.1 史瓦西度量：幾何結構")

    # 定義符號
    t, r, theta, phi = sp.symbols('t r theta phi')
    rs = sp.symbols('r_s', real=True, positive=True) # 史瓦西半徑
    c = sp.symbols('c', real=True, positive=True)    # 光速
    
    # 史瓦西度量張量 g_μν
    # ds^2 = -(1-rs/r)c^2dt^2 + (1-rs/r)^-1 dr^2 + r^2 dθ^2 + r^2 sin^2θ dφ^2
    g = sp.Matrix([
        [-(1 - rs/r)*c**2, 0, 0, 0],
        [0, 1/(1 - rs/r), 0, 0],
        [0, 0, r**2, 0],
        [0, 0, 0, r**2 * sp.sin(theta)**2]
    ])
    
    # 計算逆度量 g^μν
    g_inv = g.inv()
    
    print("史瓦西度量張量 g_μν:")
    sp.pprint(g)
    
    print("\n逆度量張量 g^μν:")
    sp.pprint(g_inv)

    # ==========================================
    # 計算克里斯多福符號 (用於光線偏折)
    # ==========================================
    print("\n計算 Christoffel 符號 Γ^r_tt 與 Γ^r_rr (關鍵分量)...")
    
    coords = [t, r, theta, phi]
    
    def get_gamma(lam, mu, nu):
        res = 0
        for sigma in range(4):
            term = (sp.diff(g[sigma, mu], coords[nu]) +
                    sp.diff(g[sigma, nu], coords[mu]) -
                    sp.diff(g[mu, nu], coords[sigma]))
            res += 0.5 * g_inv[lam, sigma] * term
        return sp.simplify(res)

    # Γ^r_tt : 描述時間流逝對徑向加速度的影響 (重力吸引)
    Gamma_r_tt = get_gamma(1, 0, 0)
    print(f"Γ^r_tt = {Gamma_r_tt}")
    
    # Γ^r_rr : 描述空間彎曲對徑向加速度的影響
    Gamma_r_rr = get_gamma(1, 1, 1)
    print(f"Γ^r_rr = {Gamma_r_rr}")

    # ==========================================
    # 12.3 重力透鏡：光線偏折 (Deflection of Light)
    # ==========================================
    print_section("12.3 重力透鏡：有效位能分析")
    
    # 在赤道面 (theta = pi/2) 上，光子運動方程式可以簡化為一維有效位能問題
    # (dr/dλ)^2 + V_eff(r) = E^2
    # 對於光子，V_eff(r) = (L^2/r^2) * (1 - rs/r)
    
    L = sp.symbols('L', real=True) # 角動量
    V_eff = (L**2 / r**2) * (1 - rs/r)
    
    print(f"光子的有效位能 V_eff(r) = {V_eff}")
    
    # 繪製有效位能圖 (假設 L=1, rs=1)
    # 這能直觀展示光線為何會被「吸引」甚至落入黑洞
    r_vals = np.linspace(1.1, 10, 100) # r > rs
    # rs = 1, L = 4 (足夠大的角動量以避免直接掉入)
    V_vals = [(4**2 / rv**2) * (1 - 1/rv) for rv in r_vals]
    
    plt.figure(figsize=(8, 5))
    plt.plot(r_vals, V_vals, label=r'Effective Potential $V_{eff}(r)$')
    plt.axvline(x=1.5, color='r', linestyle='--', label='Photon Sphere ($r=1.5r_s$)')
    plt.title('Effective Potential for Photons in Schwarzschild Metric')
    plt.xlabel('Radius $r$ ($r_s$)')
    plt.ylabel('Potential $V$')
    plt.legend()
    plt.grid(True)
    # plt.show() # 在本地運行時可取消註解以顯示圖形
    print("-> 已生成有效位能圖 (需 GUI 顯示)。")
    print("-> 紅色虛線 r=1.5rs 處是「光子球 (Photon Sphere)」，光線在此處可做圓周運動。")

    # ==========================================
    # 12.2 黑洞與事件視界 (Event Horizon)
    # ==========================================
    print_section("12.2 黑洞：光錐的傾倒")
    
    # 觀察 g_tt 和 g_rr 在 r -> rs 時的行為
    print(f"g_tt (r -> rs) = {sp.limit(g[0,0], r, rs)}")
    print(f"g_rr (r -> rs) = {sp.limit(g[1,1], r, rs)}")
    
    print("\n物理意義：")
    print("1. g_tt -> 0 : 時間在視界處似乎「停止」(對於遠處觀察者)。")
    print("2. g_rr -> ∞ : 徑向距離在視界處變得無限大 (座標奇點)。")
    
    # 光錐方程式: ds^2 = 0 (只考慮徑向光線 dθ=dφ=0)
    # 0 = g_tt dt^2 + g_rr dr^2
    # (dr/dt)^2 = - g_tt / g_rr = (1 - rs/r)^2 * c^2
    # 光速斜率 dr/dt = +/- c(1 - rs/r)
    
    slope = c * (1 - rs/r)
    print(f"\n徑向光速 dr/dt = ± {slope}")
    print("-> 當 r -> rs 時，光速 dr/dt -> 0。")
    print("-> 這表示光錐逐漸變窄並在視界處「閉合」，光線無法逃離。")

    # ==========================================
    # 12.4 重力波 (Gravitational Waves)
    # ==========================================
    print_section("12.4 重力波：弱場近似")

    # 在弱場極限下，g_μν = η_μν + h_μν
    # 愛因斯坦場方程式簡化為波動方程: □ h_μν = 0
    # □ = -∂^2/∂(ct)^2 + ∇^2
    
    # 定義一個沿 z 軸傳播的平面重力波解
    # h_xx = -h_yy = A * cos(omega * (t - z/c))
    # 這對應於 "+" 偏振模式
    z_coord = z
    A, omega = sp.symbols('A omega', real=True)
    
    # 波相位 phase = omega(t - z/c)
    phase = omega * (t - z_coord/c)
    h_xx = A * sp.cos(phase)
    
    print(f"假設重力波擾動 h_xx = {h_xx}")
    
    # 驗證它滿足波動方程
    # d^2/dz^2 - (1/c^2) d^2/dt^2
    wave_eq = sp.diff(h_xx, z_coord, 2) - (1/c**2) * sp.diff(h_xx, t, 2)
    
    print(f"\n代入波動算子 □ h_xx:")
    print(f"∂²h/∂z² - (1/c²)∂²h/∂t² = {sp.simplify(wave_eq)}")
    
    if sp.simplify(wave_eq) == 0:
        print("✅ 驗證成功：此擾動滿足波動方程式，以光速 c 傳播。")

if __name__ == "__main__":
    main()