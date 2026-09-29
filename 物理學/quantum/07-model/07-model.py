from sympy import symbols, sin, diff, integrate, exp, sqrt, pi, oo, simplify, Function, I, solve
from sympy.physics.quantum import Dagger, Commutator, qapply, represent
# 修正引入：使用正確的類別名稱 BosonFockKet, BosonFockBra
from sympy.physics.quantum.boson import BosonOp, BosonFockKet, BosonFockBra
from sympy.physics.quantum.operator import Operator
from sympy.physics.quantum.constants import hbar

def demo_7_1_infinite_well():
    print("\n" + "="*60)
    print("### 7.1 無限深位能井 (Infinite Square Well)")
    print("="*60)
    
    # 定義符號
    # x: 位置, L: 井寬, m: 質量, n: 量子數 (正整數)
    x = symbols('x', real=True)
    L = symbols('L', positive=True, real=True)
    m = symbols('m', positive=True, real=True)
    n = symbols('n', integer=True, positive=True)
    
    # 1. 定義波函數 psi_n(x) = sqrt(2/L) * sin(n*pi*x/L)
    psi = sqrt(2/L) * sin(n * pi * x / L)
    print(f"波函數 psi_{n}(x): {psi}")
    
    # 2. 驗證歸一化條件 (Normalization)
    # 積分範圍 0 到 L
    norm_integral = integrate(psi**2, (x, 0, L))
    print(f"歸一化積分 <psi|psi>: {simplify(norm_integral)}")
    print("(結果為 1 表示波函數已歸一化)")
    
    # 3. 驗證薛丁格方程式並求能量 E
    # TISE: -hbar^2 / 2m * d^2/dx^2 psi = E * psi
    
    # 計算二階微分
    d2_psi = diff(psi, x, 2)
    
    # 左式: 動能算子作用
    kinetic_term = -hbar**2 / (2*m) * d2_psi
    
    print(f"\n動能算子作用結果:\n{simplify(kinetic_term)}")
    
    # 我們希望 kinetic_term = E * psi
    # E = kinetic_term / psi
    E_eigen = simplify(kinetic_term / psi)
    
    print(f"\n推導出的能量本徵值 E_{n}:")
    print(E_eigen)
    print("這與公式 E = n^2 * pi^2 * hbar^2 / (2mL^2) 完全一致。")


def demo_7_2_harmonic_oscillator_ladder():
    print("\n" + "="*60)
    print("### 7.2 量子諧振子 (Quantum Harmonic Oscillator) - 階梯算子法")
    print("="*60)
    
    # 定義算子名稱 'a'
    a = BosonOp('a') 
    ad = Dagger(a)   # a_dagger (升算子)
    
    # 定義物理常數
    omega = symbols('omega', real=True, positive=True)
    
    # 1. 驗證對易關係 [a, a_dagger] = 1
    comm = Commutator(a, ad)
    print(f"階梯算子對易子 [a, a^dagger]:")
    # doit() 會執行對易子的計算
    print(f"  {comm} = {comm.doit()}")
    
    # 2. 定義哈密頓算子 H = hbar * omega * (a^dagger * a + 1/2)
    H = hbar * omega * (ad * a + 1/2)
    print(f"\n哈密頓算子 H: {H}")
    
    # 3. 計算能量本徵值
    # 使用粒子數態 (Fock State) |n>
    # 修正：使用 BosonFockKet
    n = symbols('n', integer=True, nonnegetive=True)
    ket_n = BosonFockKet(n)
    
    print(f"作用在態向量 |n> 上: H|n>")
    
    # qapply 會執行算子作用: a|n> = sqrt(n)|n-1>, ad|n> = sqrt(n+1)|n+1>
    # 這裡 ad * a |n> 會變成 n |n>
    action_result = qapply(H * ket_n)
    
    print(f"運算結果: {action_result}")
    
    # 提取本徵值 (係數)
    print(f"\n由此可見能量本徵值 E_n = hbar * omega * (n + 1/2)")
    
    # 4. 演示升降算子作用
    print("\n[演示升降算子作用]")
    print(f"  a |n>       = {qapply(a * ket_n)}")
    print(f"  a^dagger |n> = {qapply(ad * ket_n)}")


def demo_7_3_quantum_tunneling():
    print("\n" + "="*60)
    print("### 7.3 隧道效應 (Quantum Tunneling)")
    print("="*60)
    
    # 定義符號
    x = symbols('x', real=True)
    m = symbols('m', positive=True)
    E = symbols('E', positive=True)   # 粒子能量
    V0 = symbols('V0', positive=True) # 位能障礙高度
    a = symbols('a', positive=True)   # 障礙寬度
    
    # 1. 定義位能障礙內部的波數 (Wave number) kappa
    # 當 E < V0 時，動能為負，波數變為虛數，導致指數衰減
    kappa = sqrt(2 * m * (V0 - E)) / hbar
    print(f"衰減常數 kappa: {kappa}")
    
    # 2. 定義障礙內的波函數形式 (忽略反射波 B項，只看穿透趨勢)
    # psi_in(x) ~ exp(-kappa * x)
    psi_barrier = exp(-kappa * x)
    
    print(f"障礙內波函數形式 (x > 0): {psi_barrier}")
    
    # 3. 驗證其滿足薛丁格方程式 (在位能 V0 區域)
    # LHS = -hbar^2/2m * d^2/dx^2 psi + V0 * psi
    # RHS = E * psi
    
    lhs = -hbar**2 / (2*m) * diff(psi_barrier, x, 2) + V0 * psi_barrier
    rhs = E * psi_barrier
    
    # 驗證 LHS - RHS 是否為 0
    check = simplify(lhs - rhs)
    print(f"\n驗證薛丁格方程式 (LHS - RHS): {check}")
    print("(結果為 0 代表該指數函數是方程式的解)")
    
    # 4. 計算穿透率 T 的近似公式 (WKB近似)
    T_approx = exp(-2 * kappa * a)
    
    print(f"\n穿透率近似公式 T (WKB近似):")
    print(T_approx)
    
    # 數值代入範例
    print("\n[數值範例]")
    vals = {m: 1, E: 1, V0: 5, hbar: 1, a: 1} # 隨意單位
    kappa_val = kappa.subs(vals).evalf()
    T_val = T_approx.subs(vals).evalf()
    
    print(f"  假設參數: m=1, E=1, V0=5, h=1, 寬度 a=1")
    print(f"  衰減常數 kappa數值: {kappa_val:.4f}")
    print(f"  穿透機率 T數值: {T_val:.6f}")

if __name__ == "__main__":
    demo_7_1_infinite_well()
    demo_7_2_harmonic_oscillator_ladder()
    demo_7_3_quantum_tunneling()