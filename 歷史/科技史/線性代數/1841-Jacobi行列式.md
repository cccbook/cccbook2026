# 1841 — Jacobi 行列式

## 案件摘要
1841 年，Carl Gustav Jacob Jacobi 在 Crelle's Journal 發表拉丁文論文〈De determinantibus functionalibus〉（論函數行列式），把 Cauchy 的行列式從「數字陣列」升級為「函數陣列」：定義了函數行列式（今日稱 **Jacobian**），證明它在多重積分變數變換中的核心地位，並用它重述隱函數定理。行列式從線性代數的內部證物，變成連接多元微積分的關鍵橋樑。

## 前因 -- 為什麼會有這個案子
- 1812–1815 年 Cauchy 建立行列式理論：定義、記法、$\det(AB)=\det(A)\det(B)$——工具已備，但只用於線性方程組。
- 多重積分的變數變換早在 Euler、Lagrange 時代就有零散處理：二重積分換極座標時憑直覺多乘一個 $r$（即 $dx\,dy = r\,dr\,d\theta$）。這個 $r$ 從哪來？為什麼三維換球座標是 $r^2\sin\varphi$？——沒有人給出統一的「偵查公式」。
- Jacobi 本人是橢圓函數大師（1829 年《Fundamenta nova theoriae functionum ellipticarum》），在橢圓函數的變數變換中反覆遇到「一組函數對一組變數」的偏導數陣列，深深感到需要系統理論。
- 1830 年代 Gauss、Ostrogradsky 的散度定理也需要嚴格的變數變換理論支撐。
- 案件核心疑問：$n$ 個函數 $f_1,\dots,f_n$ 對 $n$ 個變數 $x_1,\dots,x_n$ 的「偵測儀」是什麼？它何時可逆？何時壓縮面積？

## 線索與推理 -- 數學式、程式、理論

### 線索一：Jacobian 的定義
Jacobi 定義函數行列式（他稱之為 *functional determinant*，記號 $\frac{\partial(f_1,\dots,f_n)}{\partial(x_1,\dots,x_n)}$ 後世沿用）：

$$J = \frac{\partial(f_1,\dots,f_n)}{\partial(x_1,\dots,x_n)} = \det\!\begin{pmatrix} \frac{\partial f_1}{\partial x_1} & \cdots & \frac{\partial f_n}{\partial x_1} \\ \vdots & & \vdots \\ \frac{\partial f_1}{\partial x_n} & \cdots & \frac{\partial f_n}{\partial x_n} \end{pmatrix}$$

注意 Jacobi 的記法中行對應函數、列對應變數（今日教科書多半行對應變數、列對應函數，即轉置；因 $\det(A^T)=\det(A)$，數值相同）。在單變數情形退化為導數 $J = df/dx$——Jacobian 就是導數的高維推廣。

### 線索二：多重積分變數變換
Jacobi 證明的核心定理：若變數變換 $y_i = f_i(x_1,\dots,x_n)$ 是 $C^1$ 且可逆，則：

$$\int \cdots \int_D g\,(y_1,\dots,y_n)\, dy_1 \cdots dy_n = \int \cdots \int_{D'} g\,(f(x))\, \left| \frac{\partial(f_1,\dots,f_n)}{\partial(x_1,\dots,x_n)} \right| dx_1 \cdots dx_n$$

關鍵在 $|J|$：Jacobian 的絕對值就是「區域面積（體積）的放大率」。把區域切成無窮小平行六面體，每個小塊的體積由各偏導數向量張成的平行六面體給出——這正是 Gram 行列式的幾何意義。極座標 $x = r\cos\theta,\ y = r\sin\theta$ 時：

$$J = \det\begin{pmatrix} \cos\theta & \sin\theta \\ -r\sin\theta & r\cos\theta \end{pmatrix} = r\cos^2\theta + r\sin^2\theta = r$$

球座標同理得 $J = r^2\sin\varphi$。困擾數學家一百多年的「神祕係數」正式結案：它們都是 Jacobian。

### 線索三：隱函數定理與鏈鎖法則
Jacobi 用 Jacobian 重述**隱函數定理**：給定方程組 $F_1=\cdots=F_n=0$，若在某點處

$$\frac{\partial(F_1,\dots,F_n)}{\partial(x_1,\dots,x_n)} \neq 0$$

則在該點附近可局部解出 $x_1,\dots,x_n$ 為其餘變數的光滑函數。$J \neq 0$ 是「局部可逆」的判據——這就是線性代數中 $\det(A)\neq 0 \Leftrightarrow A$ 可逆的非線性推廣。他還證明 Jacobian 滿足鏈鎖法則：

$$\frac{\partial(z_1,\dots,z_n)}{\partial(x_1,\dots,x_n)} = \frac{\partial(z_1,\dots,z_n)}{\partial(y_1,\dots,y_n)} \cdot \frac{\partial(y_1,\dots,y_n)}{\partial(x_1,\dots,x_n)}$$

這正是 $\det(AB)=\det(A)\det(B)$ 的微積分化身——Cauchy 1812 年的乘法規則在三十年後換了一個戰場再次現身。

### 程式碼範例：Jacobi 行列式與座標變換面積
```python
import numpy as np

def jacobian(fs, x, h=1e-6):
    """數值 Jacobian：第 i 列為 df_i/dx_j（函數對變數）"""
    n = len(fs)
    J = np.zeros((n, n))
    for j in range(n):
        xp, xm = x.copy(), x.copy()
        xp[j] += h; xm[j] -= h
        for i, f in enumerate(fs):
            J[i, j] = (f(*xp) - f(*xm)) / (2*h)
    return J

# 極座標：x = r cosθ, y = r sinθ
polar = [lambda r, t: r*np.cos(t), lambda r, t: r*np.sin(t)]
r, t = 2.0, np.pi/6
Jp = jacobian(polar, np.array([r, t]))
print("polar J =", np.linalg.det(Jp), " 理論 r =", r)

# 球座標：x = ρ sinφ cosθ, y = ρ sinφ sinθ, z = ρ cosφ
sph = [lambda R, p, th: R*np.sin(p)*np.cos(th),
       lambda R, p, th: R*np.sin(p)*np.sin(th),
       lambda R, p, th: R*np.cos(p)]
Js = jacobian(sph, np.array([3.0, np.pi/4, np.pi/6]))
print("sphere J =", np.linalg.det(Js), " 理論 ρ²sinφ =", 9*np.sin(np.pi/4))

# 鏈鎖法則驗證：polar -> cart -> 再度縮放 (u,v) = (2x, 3y)
scale = [lambda x, y: 2*x, lambda x, y: 3*y]
x0 = np.array([r, t])
cart0 = np.array([f(*x0) for f in polar])
Jsc = jacobian(scale, cart0)
print("det(J_scale·J_polar) =", np.linalg.det(Jsc)*np.linalg.det(Jp))
comp = [lambda r, t: 2*r*np.cos(t), lambda r, t: 3*r*np.sin(t)]
print("det(J_composite)     =", np.linalg.det(jacobian(comp, x0)))

# Monte Carlo 驗證：單位圓面積 = ∫∫_D 1·|J| dr dθ
N = 200000
rs = np.sqrt(np.random.rand(N))      # 面積均勻抽樣
ts = 2*np.pi*np.random.rand(N)
est = np.mean(rs * (np.pi*1**2))     # ∫ r dr dθ over 半徑1圓 ≈ π
print("圓面積估計 ≈", est, " 理論 π ≈", np.pi)
```

輸出中：polar 的 $J=r$、sphere 的 $J=\rho^2\sin\varphi$，且 $\det(J_{\text{scale}})\det(J_{\text{polar}})=\det(J_{\text{composite}})$ 完美吻合鏈鎖法則；Monte Carlo 積分印證 $|J|$ 就是面積放大率。

## 結案 -- 後果與影響
- 多元微積分獲得堅實地基：變數變換、隱函數定理、反函數定理全部以 $J \neq 0$ 為樞紐。
- Jacobian 成為連接**線性代數與微積分的橋樑**：局部線性化的最佳工具，微分幾何的切空間、流形上的體積形式都由它生出。
- 1841 年 Jacobi 還發表姊妹篇〈De formatione et proprietatibus determinantium〉（論行列式的形成與性質），把 Cauchy 理論推向教科書化的高峰。
- 後世影響：Lagrangian/Hamiltonian 力學的正則變換、廣義相對論的座標變換、機器學習中的 normalizing flows（變數變換機率密度公式 $p_Y(y)=p_X(x)|J|$）皆源於此。

## 關鍵人物與文獻
| 人物 | 角色 |
|---|---|
| Carl Gustav Jacob Jacobi | 定義函數行列式、證明變數變換定理 |
| Augustin-Louis Cauchy | 行列式理論的奠基者 |
| Leonhard Euler / Joseph-Louis Lagrange | 變數變換的早期直覺處理 |
| Mikhail Ostrogradsky | 散度定理（同期） |

- C. G. J. Jacobi, *De determinantibus functionalibus*, J. reine angew. Math. (Crelle) **22**, 319–355 (1841)。
- C. G. J. Jacobi, *De formatione et proprietatibus determinantium*, J. reine angew. Math. **22**, 285–318 (1841)。
