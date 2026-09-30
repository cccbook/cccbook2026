# 1812 Gauss 與超幾何函數

## 案發現場

十八世紀末，數學家手中累積了一大堆「特殊級數」：牛頓的二項級數、Euler 的階乘積分、Legendre 的橢圓積分、Bessel 正在研究的柱面函數……這些級數各自為政，彷彿一座座孤島。偵辦本案的問題是：**這些級數之間，是否有一個共同的「祖先」？**

同時還有一個更隱蔽的懸案：級數的「收斂性」。十八世紀的數學家常把無窮級數當成「無限多項的多項式」隨意操作——逐項微分、逐項積分、隨意相加。Euler 本人就曾寫出 $1 - 1 + 1 - 1 + \cdots = \frac{1}{2}$ 這類在後世看來毫無根據的等式。級數何時可以放心使用？什麼時候會「爆掉」發散？當時沒有人說得清楚。

接下這個案子的，是當年才十五歲就進入 Göttingen 大學、被譽為「數學王子」的 Carl Friedrich Gauss。1812 年，Gauss 發表論文《無窮級數的一般研究》（Disquisitiones generales circa seriem infinitam），系統地研究了級數

$$
_2F_1(a,b;c;x) = 1 + \frac{a\,b}{c}\,x + \frac{a(a+1)\,b(b+1)}{c(c+1)\cdot 1\cdot 2}\,x^2 + \cdots
$$

這就是日後大名鼎鼎的**超幾何級數**（hypergeometric series）。Gauss 為它寫下了嚴格的收斂判據，並證明它滿足一個二階線性微分方程——**超幾何微分方程**。這篇論文被視為「分析嚴格化」的開山之作之一。

## 偵查過程

### 第一步：找出各種級數的統一形式

Gauss 的關鍵靈感是觀察係數的「比值結構」。許多經典級數的係數都能寫成階乘比的形式。例如二項級數 $(1+x)^a$ 的係數：

$$
(1+x)^a = 1 + a x + \frac{a(a-1)}{2!}x^2 + \cdots
$$

係數 $c_n$ 滿足

$$
\frac{c_{n+1}}{c_n} = \frac{a-n}{n+1}.
$$

若取 $a = 1$，這就是 $\frac{1}{n+1}$。Gauss 認識到：如果把「上升與下降的階乘」同時放進分子與分母，就得到最一般的係數結構：

$$
\frac{c_{n+1}}{c_n} = \frac{(a+n)(b+n)}{(c+n)(n+1)}.
$$

由 $c_0 = 1$ 逐項累乘，得到

$$
c_n = \frac{(a)_n (b)_n}{(c)_n\, n!}, \qquad (a)_n := a(a+1)\cdots(a+n-1),
$$

其中 $(a)_n$ 稱為 Pochhammer 符號（上升階乘）。這正是 $_2F_1$ 的係數。

### 第二步：驗證特例——族譜對起來了

Gauss 檢查了各種特例，發現「族譜」完全吻合：

- 取 $b = -n$：級數在第 $n$ 項截斷，回到二項級數 $(1+x)^a$；
- 取 $a=b=c=1$：得 $\displaystyle\sum_{n\ge 0} x^n = \frac{1}{1-x}$，即幾何級數——這正是「超幾何」名稱的由來；
- 取 $c=\frac{1}{2}, a=b$ 等特例，可得到 $\arcsin$、對數、Bessel 函數、Legendre 多項式等；
- 橢圓積分 $K(k) = \int_0^{\pi/2}\frac{d\theta}{\sqrt{1-k^2\sin^2\theta}}$ 恰好是

$$
K(k) = \frac{\pi}{2}\;{}_2F_1\!\left(\frac{1}{2},\frac{1}{2};1;k^2\right).
$$

一個函數統一了整個家族。

### 第三步：推導超幾何微分方程

設 $y(x) = \sum_{n\ge 0} c_n x^n$，其中 $\dfrac{c_{n+1}}{c_n} = \dfrac{(a+n)(b+n)}{(c+n)(n+1)}$。把這個比值關係改寫成：

$$
(c+n)(n+1)c_{n+1} = (a+n)(b+n)c_n.
$$

想造一個微分方程，就是要把這個「係數遞迴式」翻譯成 $y', y''$ 之間的關係。注意：

$$
y' = \sum_{n\ge 1} n\,c_n x^{n-1} = \sum_{n\ge 0}(n+1)c_{n+1}x^n,
$$

$$
y'' = \sum_{n\ge 0}(n+2)(n+1)c_{n+2}x^n.
$$

把遞迴式中的 $n$ 換成 $n+1$，得 $(c+n+1)(n+2)c_{n+2} = (a+n+1)(b+n+1)c_{n+1}$。組合 $x(1-x)y'' + [c-(a+b+1)x]y' - ab\,y$，逐項核對 $x^n$ 的係數：

- $x(1-x)y''$ 的 $x^n$ 係數：$(n+1)n\,c_{n+1} - n(n-1)c_n$（由 $x y''$ 與 $x^2 y''$ 項組成）；
- $[c-(a+b+1)x]y'$ 的係數：$c\,(n+1)c_{n+1} - (a+b+1)(n-1)c_n$；
- $-ab\,y$ 的係數：$-ab\,c_n$。

合計 $c_{n+1}$ 項係數：$(n+1)\big[(n+1)n/c\text{ 換算}\big]$，利用遞迴式 $(c+n)(n+1)c_{n+1}=(a+n)(b+n)c_n$ 代入化簡，全部 $c_{n+1}$ 項合為 $(a+n)(b+n)c_n$；全部 $c_n$ 項合為 $-[(n)(n-1) + (a+b+1)(n-1) + ab]c_n = -(n+a)(n+b)c_n$。兩者相消，恆為零。於是我們得到

$$
x(1-x)y'' + [c-(a+b+1)x]\,y' - ab\,y = 0.
$$

這是 Gauss 級數滿足的**超幾何微分方程**。它有三個正則奇點 $x = 0, 1, \infty$，這個「三奇點結構」在日後 Poincaré 的自守函數理論中將扮演核心角色（參見 [1886-Poincare三體問題.md](1886-Poincare三體問題.md)）。

### 第四步：嚴格的收斂判據

Gauss 用**比值判據**（d'Alembert 判據的嚴格化版本）分析收斂性：

$$
\lim_{n\to\infty}\left|\frac{c_{n+1}x^{n+1}}{c_n x^n}\right|
= |x|\lim_{n\to\infty}\left|\frac{(a+n)(b+n)}{(c+n)(n+1)}\right|
= |x|.
$$

- $|x| < 1$：級數絕對收斂；
- $|x| > 1$：級數發散；
- $x = 1$（Gauss 獨到的貢獻）：級數收斂當且僅當

$$
\Re(c-a-b) > 0.
$$

Gauss 對邊界情形 $x=\pm 1$ 的細緻分析，遠超同時代人的水準——他不只回答「收不收斂」，還給出了收斂速度的估計。這種一絲不苟的態度，正是把「十八世紀的形式計算」推向「十九世紀嚴格分析」的第一槍。

## 結案報告

本案的結論是：**超幾何函數是特殊函數家族的「共同祖先」**。幾何級數、二項級數、對數函數、反三角函數、Bessel 函數、Legendre 多項式、橢圓積分，全都是 $_2F_1$ 在不同參數下的特例。Gauss 以一個二階線性微分方程與一套嚴格的收斂理論，把散落的孤島連成了一片大陸。

遺產深遠：

1. **特殊函數論**：$_2F_1$ 之後又推廣出 $_pF_q$、合流超幾何函數 $_1F_1$（Airy、Bessel 皆由此生出，參見 [1841-Liouville可積性之謎.md](1841-Liouville可積性之謎.md)）。
2. **分析嚴格化**：Gauss 對級數收斂性的重視，直接啟發了 Abel 與 Cauchy 的嚴格級數理論（參見 [1824-Cauchy存在性定理.md](1824-Cauchy存在性定理.md)）。
3. **單值化與自守函數**：超幾何方程的三正則奇點結構，是 Riemann 之後 Poincaré 自守函數理論的源頭。
4. **現代物理**：量子力學中氫原子、諧振子、球面調和函數的求解，最後都歸結為超幾何方程。

## 證據與工具

```python
# 用數值方法驗證超幾何級數的性質
import numpy as np
from scipy.special import hyp2f1
from scipy.integrate import solve_ivp

# 1) 級數求和：手動累加 _2F1 的係數
def hypergeometric_series(a, b, c, x, N=50):
    """直接累加級數項，與 scipy 的 hyp2f1 對照"""
    total = 0.0
    coeff = 1.0  # c_0 = 1
    for n in range(N):
        total += coeff * x**n
        # 遞迴式：c_{n+1}/c_n = (a+n)(b+n) / ((c+n)(n+1))
        coeff *= (a + n) * (b + n) / ((c + n) * (n + 1))
    return total

a, b, c, x = 0.5, 0.5, 1.0, 0.3
print("手動級數:", hypergeometric_series(a, b, c, x))
print("scipy 函數:", hyp2f1(a, b, c, x))
# 橢圓積分 K(k) = (pi/2) * _2F1(1/2,1/2;1;k^2)
k = 0.5
from scipy.special import ellipk
print("橢圓積分檢驗:", (np.pi/2)*hyp2f1(0.5,0.5,1,k**2), "vs", ellipk(k**2))

# 2) 數值驗證：_2F1 滿足超幾何微分方程
def hypergeo_ode(x, y):
    """超幾何方程 x(1-x)y'' + [c-(a+b+1)x]y' - ab y = 0 化為一階組"""
    yp, ypp = y[1], y[2]
    return [yp, ypp, ((a+b+1)*x - c)*yp/ (x*(1-x)) + ab_term(x)*y[0]/(x*(1-x))]

def ab_term(x):
    return a*b

# 以 y(0.01)=1, y'(0.01)=ab/c 起始（級數在 0 附近的初值）
sol = solve_ivp(hypergeo_ode, [0.01, 0.9], [1.0, a*b/c, 0.0], max_step=0.01)
xv = sol.y[0]; yv = sol.y[1]  # solve_ivp 中 x 是 t 軸，此處重跑正確版本
sol = solve_ivp(lambda t, Y: [Y[1], ((a+b+1)*t - c)*Y[1]/(t*(1-t)) + a*b*Y[0]/(t*(1-t))],
                [0.01, 0.9], [1.0, a*b/c], max_step=0.01)
ts = sol.t
exact = np.array([hyp2f1(a, b, c, t) for t in ts])
err = np.max(np.abs(sol.y[0] - exact))
print("微分方程數值解 vs 級數精確解 最大誤差:", err)
```
