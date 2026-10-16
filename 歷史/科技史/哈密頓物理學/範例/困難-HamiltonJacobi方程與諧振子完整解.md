# 困難-Hamilton-Jacobi 方程與諧振子的完整解

## 題目
用 Hamilton-Jacobi 方法（1837）完整求解一維諧振子：
H = p²/2m + ½kx²，質量 m，角頻率 ω = √(k/m)。
並說明為什麼這個方法被量子力學的誕生（1925-1926）視為關鍵橋樑。

## 解說

### 第 1 步：Hamilton-Jacobi 方程是什麼？

Hamilton 在 1834-1835 年發現：把哈密頓量中的 p 換成「作用量函數的梯度」
p = ∂S/∂x，就得到一個偏微分方程：

$$H\left(x, \frac{\partial S}{\partial x}\right) = E$$

對諧振子而言：

$$\frac{1}{2m}\left(\frac{\partial S}{\partial x}\right)^2 + \frac{1}{2}m\omega^2 x^2 = E$$

**直觀理解**：S(x, t) 就像一張「地形圖」，等高線是 S 相同的點，
而粒子的軌道永遠垂直於等高線前進。解出 S，就解出了所有可能的軌道！
這就像光學中的「波前」：光線永遠垂直於波前——這個類比後來啟發了 Schrödinger。

### 第 2 步：分離變數

設 S(x, t) = W(x) − Et（時間部分可以先提出來，因為 H 不含 t）：

$$\frac{1}{2m}\left(\frac{dW}{dx}\right)^2 + \frac{1}{2}m\omega^2 x^2 = E$$

解出 dW/dx：

$$\frac{dW}{dx} = \pm\sqrt{2mE - m^2\omega^2 x^2}$$

積分（這是高中就會的三角代換積分，令 x = A sin θ，A = √(2E/mω²)）：

$$W(x) = \frac{E}{\omega}\left[\theta + \frac{1}{2}\sin 2\theta\right], \quad \theta = \sin^{-1}\!\left(\sqrt{\frac{m\omega^2}{2E}}\,x\right)$$

### 第 3 步：Jacobi 的神來一筆

Jacobi（1843）指出：把 W 當成「新座標」，令

$$\beta = \frac{\partial S}{\partial E} = \frac{\partial W}{\partial E} - t = \text{常數}$$

（這就是「正則變換」：換到一組讓運動變得超簡單的新座標。）

計算 ∂W/∂E 時注意 E 藏在 A 裡。結果整理後可得：

$$\cos\theta = \sin(\omega(\beta + t))$$

稍加整理就得到：

$$x(t) = A\sin(\omega t + \phi)$$

**一個再熟悉不過的答案**：諧振子做簡諧運動，振幅 A 由能量決定
（E = ½mω²A²），相位 φ 由初始條件決定。

### 第 4 步：這個方法為什麼重要？

Hamilton-Jacobi 理論的三個深遠影響：

1. **動作量 S 是主角**：粒子軌道 = S 的等高線的法線，
   就像光線 = 波前的法線。**力學和光學在數學上是同一回事！**

2. **通往波動力學**：Schrödinger（1926）正是把「粒子軌道是 S 的法線」
   升級為「S 其實是一個波的相位」，寫下波動方程。波前彎曲時光線近似仍成立，
   就像短波長時量子力學近似回到古典力學（WKB 近似）。

3. **通往矩陣力學**：Heisenberg（1925）注意到 H-J 理論中的「作用變數-角度變數」
   J, θ 天生帶有週期性，把 J 量子化（J = nh/2π）就得到能階：
   
   $$E_n = \left(n + \frac{1}{2}\right)\hbar\omega$$

   諧振子的能階是等間距的——這正是 Planck（1900）黑體輻射假設的根源！

### 第 5 步：總結——一條思想的長河

| 年份 | 人物 | 貢獻 |
|---|---|---|
| 1744 | Maupertuis | 最小作用量原理 |
| 1788 | Lagrange | 拉格朗日方程 |
| 1834 | Hamilton | 正則方程、作用量函數 S |
| 1837 | Hamilton & Jacobi | H-J 方程、正則變換 |
| 1900 | Planck | 作用變數量子化 J = nh/2π |
| 1925-26 | Heisenberg & Schrödinger | 矩陣力學與波動力學 |

**一句話總結**：Hamilton 把牛頓力學改寫成「能量與波前」的語言，
一百年後，這套語言直接變成了量子力學。你今天解的諧振子習題，
正是量子革命的起點。

## 重點整理
1. H-J 方程：H(x, ∂S/∂x) = E，解 S 就解出所有軌道
2. 分離變數 S = W(x) − Et，再由 ∂S/∂E = 常數得 x(t)
3. 諧振子答案 x = A sin(ωt + φ)，量子化後 Eₙ = (n+½)ℏω
4. S 的等高線 ↔ 光學波前：力學與光學同構，是量子力學的橋樑
