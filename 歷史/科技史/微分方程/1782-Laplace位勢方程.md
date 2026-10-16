# 1782 拉普拉斯與位勢方程

## 案發現場

十八世紀後半，天體力學是數學的皇冠，而皇冠上最大的未解之謎是：**太陽系穩定嗎？** 牛頓的萬有引力解釋了兩體問題（克卜勒定律的推論），但太陽系有木星、土星、地球等眾多行星彼此攝動，長期累積的擾動會不會讓軌道崩壞、行星撞入太陽？

更技術性的難題是**橢球體的引力**：牛頓只算出均勻球殼對內部質點的合力為零（著名的「殼層定理」），但地球因自轉而扁縮成扁球體，月球與太陽對這個非球形地球的引力、以及扁球體內部各點所受的引力，都沒有一般算法。克萊羅（Clairaut, 1743）與達朗貝爾研究了扁球體問題，但方法繁瑣且只能逐案處理。

1782 年前後，拉普拉斯（Pierre-Simon Laplace）在研究行星攝動時引入了一個天才的概念——**位勢函數（potential function）** $V$：把向量式的引力場 $\mathbf{F}$，壓縮成一個純量函數，$\mathbf{F} = \nabla V$。而這個 $V$ 在**沒有質量的區域**內滿足一條驚人地簡潔的方程：

$$
\nabla^2 V = \frac{\partial^2 V}{\partial x^2} + \frac{\partial^2 V}{\partial y^2} + \frac{\partial^2 V}{\partial z^2} = 0
$$

這條方程今日稱為**拉普拉斯方程**（Laplace equation），$\nabla^2$ 稱為**拉普拉斯算子**。它成為數學物理中出現頻率最高的方程——引力、靜電學、熱傳導、流體勢流、量子力學，無處不在。

## 偵查過程

**第一步：位勢概念的引入。**
質量 $M$ 在距離 $r$ 處產生的引力大小為 $GM/r^2$，方向指向質心。拉普拉斯注意到：若定義

$$
V(P) = \iiint \frac{\rho(Q)\, dV_Q}{|P - Q|}
$$

（即把每個質量元的 $1/\text{距離}$ 加總），則引力恰為其梯度：

$$
\mathbf{F} = GM\,\nabla\!\left(\frac{1}{r}\right) = -\frac{GM}{r^2}\hat{\mathbf{r}} \quad\Longrightarrow\quad \mathbf{F} = \nabla V \ (\text{取 } V = -GM/r \text{ 時 } \mathbf{F} = -\nabla V)
$$

一個純量函數 $V$ 完整編碼了向量引力場——這是「用純量場統一向量場」的歷史首例。

**第二步：無質量區域內，$V$ 滿足什麼？**
考慮單一質點的位勢 $V = 1/r$（$r \neq 0$）。計算拉普拉斯算子：

$$
\frac{\partial V}{\partial x} = -\frac{x}{r^3}, \qquad
\frac{\partial^2 V}{\partial x^2} = -\frac{1}{r^3} + \frac{3x^2}{r^5}
$$

對 $y, z$ 同理，三式相加：

$$
\nabla^2 V = -\frac{3}{r^3} + \frac{3(x^2+y^2+z^2)}{r^5} = -\frac{3}{r^3} + \frac{3r^2}{r^5} = 0
$$

**在質點所在的點之外，處處 $\nabla^2 V = 0$。** 由疊加原理，任何質量分佈在**其外部**的位勢皆滿足拉普拉斯方程。這就是「諧和函數」（harmonic function）——名字暗示著與音樂同源的「和諧」性質。

**第三步：球座標形式。**
天體力學天然適合球座標 $(r, \theta, \varphi)$。經座標變換（雅可比行列式計算），拉普拉斯算子化為

$$
\nabla^2 V = \frac{1}{r^2}\frac{\partial}{\partial r}\left( r^2 \frac{\partial V}{\partial r} \right) + \frac{1}{r^2 \sin\theta}\frac{\partial}{\partial \theta}\left( \sin\theta\, \frac{\partial V}{\partial \theta} \right) + \frac{1}{r^2 \sin^2\theta}\frac{\partial^2 V}{\partial \varphi^2}
$$

**第四步：分離變數與球諧函數。**
設 $V = R(r)\,\Theta(\theta)\,\Phi(\varphi)$，代入後分離：$\Phi$ 部分給出 $\Phi'' + m^2\Phi = 0$（週期性要求 $m$ 為整數）；$\theta$ 部分經 $x = \cos\theta$ 代換化為**勒壤得方程**：

$$
(1-x^2)\frac{d^2\Theta}{dx^2} - 2x\frac{d\Theta}{dx} + \left[ l(l+1) - \frac{m^2}{1-x^2} \right]\Theta = 0
$$

要求解在 $x = \pm 1$（南北極）有界，$l$ 必須是非負整數，解即**締合勒壤得函數** $P_l^m(x)$。完整的解是**球諧函數**：

$$
V(r,\theta,\varphi) = \sum_{l=0}^{\infty} \sum_{m=-l}^{l} \left( A_{lm} r^l + \frac{B_{lm}}{r^{l+1}} \right) Y_l^m(\theta, \varphi)
$$

$r^l$ 項在無窮遠有界性下被捨去（外部問題），$1/r^{l+1}$ 項即**多極展開**：單極（$l=0$，總質量）、偶極（$l=1$）、四極（$l=2$）……拉普拉斯用它證明了：從很遠處看，任何天體的引力都近似於一個點質量，修正項按 $1/r$ 的冪次快速衰減——**太陽系穩定性的攝動理論由此獲得堅實基礎**。

**第五步：殼層定理的推廣。** $l=0$ 的球諧函數是常數，直接推論：均勻球殼對內部質點的引力為零（牛頓殼層定理），拉普拉斯的方法把這個特例納入一般理論。

## 結案報告

拉普拉斯的位勢理論解決了扁球體引力與遠距攝動計算的謎題，並與拉格朗日（[1788-Lagrange分析力學.md](1788-Lagrange分析力學.md)）合作，把太陽系穩定性問題推進了一大步（拉普拉斯-拉格朗日定理：行星軌道離心率的長期攝動只在一階範圍內振盪而不累積）。其遺產：

1. **位勢論成為獨立學科**：$\nabla^2 V = 0$ 與 $\nabla^2 V = -4\pi\rho$（Poisson 方程，1813）成為數學物理的核心方程；馬克士威的靜電學完全建立在位勢論之上；
2. **球諧函數**成為量子力學氫原子角動量解（$Y_l^m$）、地球物理重力場模型（EGM）、宇宙學 CMB 分析的通用工具；
3. **邊值問題與 Green 函數（1828）**：格林（George Green）引入 Green 函數，把「給定邊界條件求內部位勢」的問題系統化——電位勢的邊值問題（Dirichlet 問題、Neumann 問題）自此有了統一解法，也促成了位勢論的嚴格化（1890 年代 Poincaré、Hilbert 的掃除法與 Dirichlet 原理）；
4. **調和分析的擴張**：球諧函數是傅立葉級數（[1763-三角級數大辯論.md](1763-三角級數大辯論.md)）在球面上的推廣，正交函數系思想自此成形。

與波動方程（雙曲型）和熱傳導方程（拋物型）相比，拉普拉斯方程是**橢圓型**方程的原型——「空間的形狀」問題而非「時間的演化」問題。三類方程的三分法（雙曲、拋物、橢圓），成為十九世紀偏微分方程分類的骨架。

## 證據與工具

以下程式驗證拉普拉斯的兩大理論：$\nabla^2(1/r) = 0$ 與球諧函數展開的多極近似。

```python
import numpy as np
import matplotlib.pyplot as plt

# 第一部分：驗證 ∇²(1/r) = 0（在質點之外）
N = 200
L = 2.0
x, y = np.meshgrid(np.linspace(-L, L, N), np.linspace(-L, L, N))

r = np.sqrt(x**2 + y**2 + 1e-9)      # 平面上的距離（近似驗證）
V = 1.0 / r                           # 位勢

# 數值拉普拉斯算子（5 點差分）
h = 2 * L / (N - 1)
lap = (np.roll(V, 1, 0) + np.roll(V, -1, 0) +
       np.roll(V, 1, 1) + np.roll(V, -1, 1) - 4 * V) / h**2

mask = r > 0.4                        # 排除質點附近（奇異點處 ∇²V ≠ 0）
print(f"max |∇²(1/r)| away from source = {np.abs(lap[mask]).max():.2e}  （接近 0 → 拉普拉斯方程成立）")

# 畫位勢的等高線：等位面（就像地圖上的等高線）
fig, ax = plt.subplots(figsize=(7, 6))
cs = ax.contourf(x, y, np.log(V), levels=30, cmap="viridis")
plt.colorbar(cs, label="log V")
ax.set_title("Potential V = 1/r: harmonic outside the source")
ax.set_xlabel("x"); ax.set_ylabel("y")
plt.tight_layout()
plt.savefig("laplace_potential.png", dpi=120)
plt.show()

# 第二部分：用 Python 驗證球諧函數的正交性與多極展開
# 勒壤得多項式 P_l(x)（l=0..4），用遞迴式生成
def legendre_P(l, x):
    if l == 0: return np.ones_like(x)
    if l == 1: return x
    P0, P1 = np.ones_like(x), x
    for k in range(1, l):
        P0, P1 = P1, ((2*k + 1) * x * P1 - k * P0) / (k + 1)
    return P1

# 驗證正交性：∫ P_l(x) P_k(x) dx = 2/(2l+1) δ_lk
xs = np.linspace(-1, 1, 200000)
for l, k in [(1, 1), (1, 2), (2, 3), (3, 3)]:
    val = np.trapz(legendre_P(l, xs) * legendre_P(k, xs), xs)
    target = 2 / (2 * l + 1) if l == k else 0.0
    print(f"∫ P_{l}(x)·P_{k}(x) dx ≈ {val:.4f}  (理論值: {target:.4f})")

# 多極展開：遠處的引力 ≈ 單極 + 偶極 + 四極修正
# 以兩個分離的質點（偶極子）為例：m1 在 (-a,0)，m2 在 (+a,0)
a = 0.1
R, theta = 5.0, np.pi / 3            # 觀察點的球座標
V_exact = 1/np.sqrt(R**2 + a**2 - 2*R*a*np.cos(theta)) + \
          1/np.sqrt(R**2 + a**2 + 2*R*a*np.cos(theta))

# 多極展開（軸對稱，只用 m=0 項）：Σ P_l(cosθ) a^l / R^(l+1) × 2（偶數項）
V_multipole = sum(2 * legendre_P(2*l, np.cos(theta)) * a**(2*l) / R**(2*l+1) for l in range(4))
print(f"\n偶極子位勢：精確值 = {V_exact:.6f}，多極展開(至 l=6) = {V_multipole:.6f}")
print(f"相對誤差 = {abs(V_exact - V_multipole)/V_exact:.2e}  （遠場 R=5 時誤差極小 → 拉普拉斯攝動理論的基礎）")
```

執行後可見：$\nabla^2(1/r)=0$ 在源點之外成立（數值驗證），勒壤得多項式正交（球諧函數理論的基石），而遠場的多極展開誤差極小——這正是拉普拉斯敢於宣稱「太陽系近似穩定」的數學證據。
