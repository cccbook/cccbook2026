# 1799 — Gauss 代數基本定理

## 案件摘要
1799 年，年僅 21 歲的 Carl Friedrich Gauss 在赫爾姆施泰特大學提交博士論文，題為〈每一個單變數整有理函數都可分解為一次或二次實因式的新證明〉——這就是**代數基本定理**（Fundamental Theorem of Algebra）的第一次嚴肅證明：$n$ 次多項式在複數域 $\mathbb{C}$ 中必有 $n$ 個根（計重數）。Gauss 的方法前所未有：他不依賴代數公理的信仰，而是訴諸**幾何與連續性**。虛數自 Cardano 的「心理折磨」、Bombelli 的「野蠻想法」、Euler 的「分析公民」以來，終於在這篇論文中獲得完整的合法性。

## 前因 -- 為什麼會有這個案子
- **1608 年 Peter Roth、1629 年 Albert Girard**：先後**猜測** $n$ 次方程有 $n$ 個根；Girard 明確寫下「次數等於根的數目」，但無證明。
- **1637 年 Descartes**：符號法則只能給出正負根數的上界，離完整定理甚遠。
- **1746 年 d'Alembert 的證明**：第一個「證明」嘗試，思路是把方程 $f(z)=0$ 化為最小化問題，證明 $|f(z)|$ 可達到下確界並在該處為零。但 d'Alembert 依賴了一個未證明的引理（如今稱 d'Alembert 引理：若 $|f(z_0)|$ 極小且不為零，則可找到 $|f|$ 更小的點——此引理本身需要連續性論證），證明有漏洞。
- **Euler（1749）、Lagrange（1772）、Laplace（1795）**：都提出過證明，但都隱含假設「多項式可完全分解」或「根的存在性」——用待證的結論證待證的結論，循環論證。
- **虛數的地位爭議**：從 Cardano 到 Euler 兩百五十年間，「虛數是否存在」始終是哲學爭議。若代數基本定理說「$n$ 次方程有 $n$ 根」，而根可能是虛數，那麼證明就必須回答：虛數到底是什麼？在哪裡？

案子就在這團疑雲中成形：兩百年來無人能給出無懈可擊的證明，21 歲的 Gauss 決定親手結案。

## 線索與推理 -- 數學式、程式、理論

### 線索一：定理的陳述與「實因式」的巧思
代數基本定理（Gauss 版本）：任何 $n$ 次實係數多項式

$$f(z) = a_n z^n + a_{n-1}z^{n-1} + \cdots + a_1 z + a_0, \qquad a_n \neq 0$$

都可分解為一次與二次**實係數**因式的乘積。等價地，$f$ 在 $\mathbb{C}$ 中恰有 $n$ 個根（計重數）。

Gauss 的巧思在於「實因式」：他避開了「虛數是否存在」的哲學爭議——虛根成對出現 $z, \bar{z}$，共軛配對相乘得實二次因式 $(x-z)(x-\bar{z}) = x^2 - 2\,\text{Re}(z)x + |z|^2$。Bombelli 在 1572 年觀察到的「共軛成對」現象，在這裡成為定理的架構支柱。

### 線索二：Gauss 的幾何化——把複數畫在平面上
Gauss 的核心策略：把複數 $z = x + iy$ 看作**平面上的點**（今日稱 Gauss 平面／複數平面），把多項式拆成實部與虛部：

$$f(z) = u(x,y) + i\,v(x,y)$$

則方程 $f(z) = 0$ 等價於兩條曲線的交點：

$$u(x,y) = 0 \quad\text{與}\quad v(x,y) = 0$$

Gauss 證明：這兩條平面曲線的分支（代數曲線的弧）**必然**相交——他仔細分析曲線在無窮遠處的行為，證明每條曲線的分支以特定角度衝向無窮遠，而 $u=0$ 與 $v=0$ 的分支交錯排列，故在有限平面上必有一個交點。這個交點就是 $f$ 的根。

### 線索三：Gauss 對 d'Alembert 漏洞的批評
Gauss 在論文開頭逐一剖析前人證明：d'Alembert、Euler、Lagrange 的論證都「假設了它們要證明的東西」——特別是 d'Alembert 依賴的極小值引理需要**連續函數在緊緻集合上達到極值**的拓撲事實（當時尚未嚴格化，要等到 Weierstrass 時代）。Gauss 批評的正是這一點：代數問題的證明不能建立在不嚴格的分析之上。諷刺的是，Gauss 自己的第一個證明也用了連續性論證（曲線相交），嚴格化同樣要等後世補完——但 Gauss 的框架是正確的。

### 線索四：Gauss 一生的四個證明
Gauss 終其一生給出四個證明：
1. **1799 年**（博士論文）：幾何式——實部虛部曲線必相交。
2. **1816 年**：用根的對稱函數與連續性，證明 $|f(z)|$ 極小值存在且為零。
3. **1816 年**（第二篇同年的證明）：用位勢論與 Brouwer 不動點式的論證（先驅）。
4. **1849 年**（博士論文五十週年紀念）：重訪 1799 年的幾何證明，補強論證。

現代教科書最常見的證明（用 Liouville 定理：$f$ 是多項式故有界全純函數必為常數，若 $f$ 無根則 $1/f$ 有界全純，矛盾；或用 $|f(z)|\to\infty$ 加最小模原理加 d'Alembert 引理）則是 19 世紀複分析的結晶。

### 程式碼範例：複數平面的 numpy 視覺化——曲線相交與牛頓法
```python
import numpy as np
import matplotlib.pyplot as plt

# 案例：f(z) = z^3 - 15z - 4（Bombelli 1572 年的方程！）
# 實部虛部曲線 u(x,y)=0 與 v(x,y)=0 的交點就是根
X, Y = np.meshgrid(np.linspace(-4, 4, 400), np.linspace(-4, 4, 400))
Z = X + 1j*Y
f = Z**3 - 15*Z - 4
u, v = f.real, f.imag

plt.figure(figsize=(7, 6))
plt.contour(X, Y, u, levels=[0], colors='b', linewidths=1.5)  # u=0
plt.contour(X, Y, v, levels=[0], colors='r', linewidths=1.5)  # v=0
plt.title("f(z)=z³-15z-4: u=0 (blue) ∩ v=0 (red) → roots")
plt.gca().set_aspect('equal'); plt.show()

# 驗證：三個根（含虛根成對出現）
roots = np.roots([1, 0, -15, -4])
print("三個根:", roots)  # 4, -2±√3 —— 共軛虛根成對！

# 牛頓法迭代：複數平面上追蹤收斂路徑
z = -1 + 2.5j
for k in range(20):
    z = z - (z**3 - 15*z - 4) / (3*z**2 - 15)
    print(f"迭代 {k+1}: z = {z:.8f}")
print("收斂至虛根 -2+√3i =", -2 + np.sqrt(3)*1j)
```

輸出顯示：藍色曲線 $u=0$ 與紅色曲線 $v=0$ 的交點恰好三個，即 $4$ 與 $-2\pm\sqrt{3}i$——正是 Gauss 幾何證明的「案發現場」；虛根成對共軛（Bombelli 的先聲被證實）；牛頓法在複數平面上收斂至虛根，虛數作為「平面上的點」完全可用於計算。

## 結案 -- 後果與影響
- 複數合法性確立：$\mathbb{C}$ 成為多項式方程的**自然棲息地**，「虛數是否存在」的兩百五十年爭議正式結案。
- 代數基本定理成為數學的基石：多項式環 $\mathbb{C}[x]$ 是唯一因式分解域、線性代數的特徵值理論、矩陣的 Jordan 標準形皆依賴此定理。
- Gauss 的幾何化思想（複數＝平面上的點）催生 1831 年他公開發表的複數平面詮釋，以及 Argand（1806）、Wessel（1797，當時無人注意）的獨立工作。
- 「證明必須嚴格」的標準被樹立：Gauss 對 d'Alembert 漏洞的批評是 19 世紀**分析嚴格化運動**（Cauchy、Weierstrass）的先聲。
- 為 1851 年 Riemann 複變函數論、Galois 理論（1832）、以及 20 世紀代數拓撲的「曲線相交」思想開路。
- 影響至今：每一次解方程、每一次計算特徵值、每一次 Fourier 變換，背後都是 1799 年那篇 21 歲青年的博士論文。

## 關鍵人物與文獻
| 人物 | 角色 |
|---|---|
| Carl Friedrich Gauss | 1799 年博士論文，第一個嚴肅證明；一生四個證明 |
| Jean le Rond d'Alembert | 1746 年第一個（有漏洞的）證明嘗試 |
| Albert Girard | 1629 年最早猜測 $n$ 次方程有 $n$ 根 |
| Leonhard Euler | 1749 年證明嘗試（隱含循環假設） |

- C. F. Gauss, *Dissertatio inauguralis de theoremate fundamentalis doctrinae de functionibus analyticis*, Helmstedt: Fleckeisen (1799)。
- C. F. Gauss, *Demonstratio nova altera theorematis...*, Göttingen (1816)：第二與第三個證明。
- C. F. Gauss, 第四個證明（1849），Jacobi Festschrift：博士論文五十週年紀念。
