import sympy as sp

def print_section(title):
    print("\n" + "="*70)
    print(f" {title}")
    print("="*70)

def main():
    # 初始化
    sp.init_printing(use_unicode=True)

    # 定義符號
    # t, x, y, z: 靜止系 S 的座標
    # v: S' 相對於 S 的速度
    # c: 光速
    t, x, y, z = sp.symbols('t x y z', real=True)
    v, c = sp.symbols('v c', real=True, positive=True)
    
    # 定義勞倫茲因子 (Lorentz Factor) gamma
    # gamma = 1 / sqrt(1 - v^2/c^2)
    gamma = sp.symbols('gamma', real=True, positive=True)
    gamma_def = 1 / sp.sqrt(1 - v**2/c**2)

    # ==========================================
    # 7.2 勞倫茲轉換 (Lorentz Transformation)
    # ==========================================
    print_section("7.2 勞倫茲轉換 (Lorentz Transformation)")

    # 1. 定義轉換公式 (從 S -> S')
    # t' = gamma * (t - v*x/c^2)
    # x' = gamma * (x - v*t)
    t_prime = gamma * (t - v * x / c**2)
    x_prime = gamma * (x - v * t)
    y_prime = y
    z_prime = z

    print(f"定義勞倫茲因子 γ = {gamma_def}")
    print("\n轉換公式 (S -> S'):")
    print(f"t' = {t_prime}")
    print(f"x' = {x_prime}")
    print(f"y' = {y_prime}")
    print(f"z' = {z_prime}")

    # 2. 驗證光速不變原理 (Spacetime Interval Invariance)
    # 檢查 s^2 = c^2*t^2 - x^2 - y^2 - z^2 是否等於 s'^2
    # 根據書中 7.2.1，光訊號滿足 x^2 + y^2 + z^2 - c^2t^2 = 0
    print("\n--- 驗證：時空區間不變性 ---")
    
    # 計算 S 系的區間 (使用 -+++ 符號慣例或是書中的 x^2 - c^2t^2)
    # 這裡我們計算 x^2 + y^2 + z^2 - c^2*t^2
    interval_S = x**2 + y**2 + z**2 - c**2 * t**2
    
    # 計算 S' 系的區間 (代入上面的轉換公式)
    interval_S_prime = x_prime**2 + y_prime**2 + z_prime**2 - c**2 * t_prime**2
    
    # 將 gamma 替換回其定義式以便化簡
    interval_S_prime_subs = interval_S_prime.subs(gamma, gamma_def)
    simplified_interval = sp.simplify(interval_S_prime_subs)
    
    print(f"S  系區間: {interval_S}")
    print(f"S' 系區間 (化簡後): {simplified_interval}")
    
    if sp.simplify(interval_S - simplified_interval) == 0:
        print("✅ 驗證成功：時空區間是不變量 (x^2 - c^2t^2 = x'^2 - c^2t'^2)")
    else:
        print("❌ 驗證失敗")

    # 3. 矩陣形式
    print("\n--- 勞倫茲轉換矩陣 Λ ---")
    # 定義四維向量 X = [ct, x, y, z]^T (這是標準的四維形式)
    # 注意：書中公式針對 t 和 x，若寫成矩陣通常會用 ct 作為第0分量以保持單位一致
    # 這裡我們展示對應 t, x 的轉換矩陣
    Lambda = sp.Matrix([
        [gamma, -gamma*v/c**2, 0, 0],
        [-gamma*v, gamma, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ])
    print("轉換矩陣 [t, x, y, z]^T -> [t', x', y', z']^T :")
    sp.pprint(Lambda)

    # ==========================================
    # 7.3.1 時間膨脹 (Time Dilation)
    # ==========================================
    print_section("7.3.1 時間膨脹 (Time Dilation)")

    # 設定情境：時鐘靜止在 S' 系 (動系)
    # 兩個事件發生在 S' 的同一地點: dx' = 0
    dt_prime = sp.symbols('Delta_t\'', real=True) # 原時
    dx_prime = 0 
    
    # 我們需要逆轉換 (S' -> S) 來找 S 系的時間 dt
    # t = gamma * (t' + v*x'/c^2)
    # 因為是線性變換，差分形式也成立: dt = gamma * (dt' + v*dx'/c^2)
    dt_S = gamma * (dt_prime + v * dx_prime / c**2)
    
    print(f"條件: 在 S' 系中位置不變 (Δx' = 0), 時間間隔為 Δt' (原時)")
    print(f"推導 S 系觀測到的時間間隔 Δt:")
    print(f"Δt = {dt_S}")
    print("結論: 因為 γ >= 1，所以 Δt >= Δt' (動鐘變慢)")

    # ==========================================
    # 7.3.2 長度收縮 (Length Contraction)
    # ==========================================
    print_section("7.3.2 長度收縮 (Length Contraction)")

    # 設定情境：尺靜止在 S' 系，原長為 L' = dx'
    # S 系觀測者測量長度 L = dx，必須「同時」測量兩端 -> dt = 0
    L_prime = sp.symbols('L\'', real=True, positive=True) # 原長
    L = sp.symbols('L', real=True, positive=True)         # 觀測長度
    
    # 使用勞倫茲轉換 x' = gamma * (x - v*t)
    # 差分形式: dx' = gamma * (dx - v*dt)
    
    # 1. 寫出方程式
    dt_measurement = 0 # 同時測量
    eq_length = sp.Eq(L_prime, gamma * (L - v * dt_measurement))
    
    print(f"條件: 尺靜止於 S' (原長 L'), S 系同時測量兩端 (Δt=0)")
    print(f"根據轉換公式 x' = γ(x - vt):")
    sp.pprint(eq_length)
    
    # 2. 解出 L
    sol_L = sp.solve(eq_length, L)[0]
    print(f"\n解出 S 系測得的長度 L:")
    print(f"L = {sol_L}")
    print("結論: 因為 1/γ <= 1，所以 L <= L' (動尺變短)")

    # ==========================================
    # 7.3.3 同時性的相對性 (Relativity of Simultaneity)
    # ==========================================
    print_section("7.3.3 同時性的相對性")

    # 設定情境：在 S' 系中同時發生的兩件事 (dt' = 0)
    # 但發生在不同地點 (dx' != 0)
    dt_prime_simul = 0
    dx_prime_simul = sp.symbols('Delta_x\'', real=True) # 兩事件距離
    
    # 使用逆轉換求 S 系的時間差 dt
    # dt = gamma * (dt' + v*dx'/c^2)
    dt_simul_S = gamma * (dt_prime_simul + v * dx_prime_simul / c**2)
    
    print(f"條件: S' 系中兩事件同時發生 (Δt' = 0), 距離為 Δx'")
    print(f"計算 S 系中這兩事件的時間差 Δt:")
    print(f"Δt = {dt_simul_S}")
    print("結論: 若 Δx' != 0，則 Δt != 0。")
    print("     在一個參考系中同時的事，在另一個參考系中不再同時。")

if __name__ == "__main__":
    main()