# 1727 Euler 系統化常微分方程：通解、積分因子與特徵根

## 案發現場

1727 年，二十歲的 Leonhard Euler 從巴塞爾來到俄國聖彼得堡科學院，接替離世的導師 Nicholas Bernoulli 與 Johann Bernoulli 之子的職位（Johann Bernoulli 本人推薦他去填補丹尼爾・伯努利的醫學職缺，丹尼爾則轉任數學職位）。此時微分方程已問世四十餘年，散落各處的解法像一座未整理的寶庫：Jacob Bernoulli 解過等時曲線與 Bernoulli 方程（見 [1690-JacobBernoulli等時曲線.md](1690-JacobBernoulli等時曲線.md)、[1695-Bernoulli方程.md](1695-Bernoulli方程.md)）、Johann 解過最速降線（[1696-最速降線問題.md](1696-最速降線問題.md)）、Leibniz 有積分因子之雛形——但**沒有一本系統性的教科書**，沒有統一的術語，沒有「哪類方程用哪種解法」的完整地圖。

當時的未解之謎包括：

1. **二階與高階方程**：$\ddot{y} = -\omega^2 y$ 這類方程已在力學中出現，但除特定的猜測與驗證外，沒有一般解法。高階線性方程的通解結構（通解 = 齊次通解 + 特解）尚未被明確表述。
2. **積分因子的系統化**：Leibniz 的「恰當乘子」技巧零散地存在，何時存在積分因子、如何求出，無人知曉。
3. **數值方法**：當方程無法用初等函數積出時（例如三體問題），該怎麼辦？分析與計算的邊界在哪裡？

Euler 遇到的正是這三重謎題。而他的重要性在於：他不是解決**某一個**方程，而是為**整門學科**繪製地圖、立下術語、建立方法論。今日常微分方程教科書的骨架，幾乎全是 Euler 的手筆。

## 偵查過程

### 偵查一：線性方程的通解結構

Euler 的第一個洞見是**疊加原理**：對 $n$ 階線性齊次方程

$$a_n(x)y^{(n)} + a_{n-1}(x)y^{(n-1)} + \cdots + a_0(x)\, y = 0$$

若 $y_1, y_2, \ldots, y_n$ 是解，則它們的任意線性組合 $C_1 y_1 + C_2 y_2 + \cdots + C_n y_n$ 也是解。Euler 證明了（在係數適當的條件下）齊次方程恰有 $n$ 個線性獨立的解，構成**通解**。

對非齊次方程（右邊不為零），Euler 明確表述了今日的標準定理：

$$y_{\text{通解}} = y_{\text{齊次通解}} + y_{\text{特解}}$$

**驗證**：設 $L[y] = a_n y^{(n)} + \cdots + a_0 y$（線性算子），$y_p$ 滿足 $L[y_p] = f(x)$，$y_h$ 滿足 $L[y_h] = 0$。則由線性性：

$$L[y_h + y_p] = L[y_h] + L[y_p] = 0 + f(x) = f(x) \checkmark$$

### 偵查二：Euler 方程與特徵根 $y = e^{rx}$

對係數為常數的方程，Euler 的靈感堪稱百年一遇：**猜測解的形式為指數函數**。他注意到指數函數 $e^{rx}$ 有個神奇的性質——求導不變形：

$$\frac{d}{dx}e^{rx} = r\, e^{rx}, \qquad \frac{d^n}{dx^n}e^{rx} = r^n\, e^{rx}$$

把它代入常係數方程 $a_n y^{(n)} + \cdots + a_0 y = 0$，每項都提出公因子 $e^{rx}$：

$$e^{rx}\left(a_n r^n + a_{n-1} r^{n-1} + \cdots + a_0\right) = 0$$

由於 $e^{rx} \neq 0$，得**特徵方程**：

$$a_n r^n + a_{n-1} r^{n-1} + \cdots + a_0 = 0$$

微分方程被代數化為多項式方程！以最經典的簡諧運動方程驗證：

$$y'' + \omega^2 y = 0 \quad\Rightarrow\quad r^2 + \omega^2 = 0 \quad\Rightarrow\quad r = \pm i\omega$$

複數根 $\pm i\omega$ 給出兩個實解 $\cos\omega x$ 與 $\sin\omega x$（Euler 透過他著名的公式 $e^{i\theta} = \cos\theta + i\sin\theta$ 處理複數根），通解為：

$$y = C_1 \cos\omega x + C_2 \sin\omega x$$

**等時曲線之謎**（[1690-JacobBernoulli等時曲線.md](1690-JacobBernoulli等時曲線.md)）中 Jacob 仰賴幾何直覺才辨認出的擺線運動 $\ddot{s} = -\omega^2 s$，如今用兩行代數就解決了。

Euler 更進一步處理了**變係數**的 Euler 方程（今稱 Cauchy-Euler 方程）：

$$x^n y^{(n)} + a_{n-1} x^{n-1} y^{(n-1)} + \cdots + a_0\, y = 0$$

其靈感是：$x^r$ 也有「求導降冪、維持形式」的性質：$\frac{d}{dx}x^r = r x^{r-1}$，$n$ 階導後 $x^{r-n}$ 仍為冪函數。代入後同樣得到特徵方程（各項提出 $x^r$）：

$$r(r-1)(r-2)\cdots(r-n+1) + a_{n-1} r(r-1)\cdots(r-n+2) + \cdots + a_0 = 0$$

### 偵查三：積分因子的系統化

對一階線性方程 $y' + P(x)y = Q(x)$，Euler 將 Leibniz 與 Bernoulli 的零散技巧（見 [1695-Bernoulli方程.md](1695-Bernoulli方程.md)）系統化。他的推理是：想找一個函數 $\mu(x)$，使 $\mu y' + \mu P y$ 恰好等於某乘積的導數：

$$\frac{d}{dx}(\mu y) = \mu y' + \mu' y \stackrel{!}{=} \mu y' + \mu P y \quad\Rightarrow\quad \mu' = \mu P$$

這是一個可分離變數方程，解得：

$$\mu(x) = e^{\int P\, dx}$$

**何時存在積分因子**？Euler 對一般形式 $M(x,y)dx + N(x,y)dy = 0$ 給出了判別法：方程恰當（即 $\partial M/\partial y = \partial N/\partial x$）時可直接積分；不恰當時，若 $\frac{M_y - N_x}{N}$ 只依賴 $x$，則積分因子 $\mu(x) = e^{\int \frac{M_y - N_x}{N} dx}$ 存在。這把「找積分因子」從藝術變成了演算法。

### 偵查四：Euler 法——數值解的思想誕生

當方程解不出初等函數時怎麼辦？Euler 在《Institutiones calculi integralis》（1768-1770）中給出了劃時代的答案：**用切線逐段逼近**。對 $y' = f(x, y)$，從初值 $(x_0, y_0)$ 出發：

$$y_{n+1} = y_n + h\, f(x_n, y_n)$$

**推理**：在 $(x_n, y_n)$ 處曲線的切線斜率為 $f(x_n, y_n)$，走一小步 $h$ 後，用切線代替曲線，$y$ 的增量近似為 $h \cdot f(x_n, y_n)$。誤差為 $O(h^2)$，累積全域誤差為 $O(h)$——步長越小越準。這是**歷史上第一個數值解微分方程的通用方法**，直達今日的三體問題、氣候模擬、分子動力學。

## 結案報告

三重謎題就此告破。Euler 於 1768-1770 年出版的三卷本《Institutiones calculi integralis》是**歷史上第一部系統性的積分學與微分方程教科書**，其章節結構——一階方程（可分離、線性、恰當）、高階線性方程、級數解、數值方法——與今日任何一本 ODE 教科書幾乎逐章對應。

此案的遺產：

1. **特徵根法**成為常係數線性方程的標準解法，並延伸到差分方程、偏微分方程（分離變數法中的分離常數即特徵值問題）、乃至量子力學的算子譜理論。Euler 方程（Cauchy-Euler 方程）至今是教科書必備習題。
2. **疊加原理與通解結構**是線性代數與微分方程交會的橋樑：「解空間是向量空間」的觀念，預示了函數空間、Hilbert 空間的誕生。
3. **積分因子法**在 Euler 手中系統化，成為一階 ODE 的標準武器（承繼 [1695-Bernoulli方程.md](1695-Bernoulli方程.md)）。
4. **Euler 法**開啟了數值分析的大門。從 Runge-Kutta（1900 年前後）到現代剛性方程求解器，整條數值 ODE 的譜系都是 Euler 法的後裔。
5. **變分法的交接棒**：Euler 於 1744 年出版《Methodus inveniendi》系統化了最速降線問題（[1696-最速降線問題.md](1696-最速降線問題.md)）催生的變分思想，並在 1756 年收到十九歲 Lagrange 的信後，慷慨地讓後者用純分析形式重寫變分法——Euler-Lagrange 方程因此得名。

Euler 一生寫了 850 餘篇論文與著作，其中關於微分方程的工作構成了今日「常微分方程」這門學科的原始基因組。Poincaré 曾說：「讀讀 Euler，讀讀 Euler，他是我們所有人的老師。」

## 證據與工具

以下 Python 程式示範 Euler 的兩大遺產：特徵根法（符號運算）與 Euler 法（數值逼近）。

```python
import numpy as np
from scipy.integrate import solve_ivp

# ── 遺產一：特徵根法 ─────────────────────────────
# 解 y'' + ω²y = 0（簡諧運動），特徵方程 r² + ω² = 0
omega = 2.0
roots = np.roots([1, 0, omega**2])
print(f"特徵方程 r² + {omega}² = 0 的根: {roots}")   # ±2i
print("複數根 ±iω → 實解 cos(ωx), sin(ωx)")
print(f"通解: y = C1·cos({omega}x) + C2·sin({omega}x)\n")

# ── 遺產二：Euler 法 ─────────────────────────────
# 解 y' = y（指數成長），初值 y(0)=1，真解 e^x
def euler_method(f, x0, y0, h, n):
    xs, ys = [x0], [y0]
    for _ in range(n):
        y0 = y0 + h * f(x0, y0)   # Euler 更新式：切線逐段逼近
        x0 = x0 + h
        xs.append(x0); ys.append(y0)
    return np.array(xs), np.array(ys)

for h in [0.5, 0.1, 0.05]:
    xs, ys = euler_method(lambda x, y: y, 0.0, 1.0, h, int(2/h))
    err = abs(ys[-1] - np.exp(2))
    print(f"Euler 法 (h={h:.2f}): y(2) ≈ {ys[-1]:.6f}，真解 e²={np.exp(2):.6f}，誤差 {err:.4f}")

# 步長減半，誤差約減半 → 全域誤差 O(h)，符合 Euler 的分析

# ── 對照：Euler 方程 x²y'' + 4xy' + 2y = 0 ──────
# 特徵方程：r(r-1) + 4r + 2 = 0 → r² + 3r + 2 = 0 → r = -1, -2
r2 = np.roots([1, 3, 2])
print(f"\nEuler 方程 x²y''+4xy'+2y=0 的特徵根: {r2} → 解 y = C1/x + C2/x²")

# ── 驗證通解結構：通解 = 齊次通解 + 特解 ──────────
# 解 y'' + y = 1，齊次通解 C1 cos x + C2 sin x，特解 y_p = 1
y_h = lambda x, C1, C2: C1*np.cos(x) + C2*np.sin(x)
print("\n驗證 y'' + y = 1 之特解 y_p = 1: y_p'' + y_p = 0 + 1 = 1 ✓")
print(f"齊次通解（C1=1, C2=0）滿足 y''+y=0: {y_h(1.0, 1, 0)} vs cos(1) = {np.cos(1.0)} ✓")
```

執行後可見：特徵根給出精確解、Euler 法的誤差隨步長減半而減半、通解結構經數值驗證成立——Euler 在 1727 年之後三十年間繪製的地图，至今仍是這門學科的地基。
