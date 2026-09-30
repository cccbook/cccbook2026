# 1841 Liouville 可積性之謎

## 案發現場

十九世紀上半葉，數學家已經掌握了求解各類微分方程的龐大工具箱：分離變數、積分因子、常數變易法、級數解。樂觀的情緒瀰漫：只要夠聰明、夠努力，任何微分方程都能「解出來」吧？

但有一個幽靈始終徘徊：**Riccati 方程**。這個形如

$$
y' = a(x)\,y^2 + b(x)\,y + c(x)
$$

的一階方程（特例 $y' = y^2 + 1$ 甚至出現在求 $\tan$ 的問題中）困擾了數學家近一百年。Bernoulli 家族解開了某些特例，Euler 研究過它的一般理論，但沒有人能用「初等函數」寫出一般解。問題是：**這到底是「還沒找到」，還是「根本不存在」？**

這是兩種完全不同的診斷。前者需要更聰明的人，後者需要新的數學。接案的，是法國數學家 Joseph Liouville（1809–1882）。1841 年，Liouville 發表論文，首次**證明**：Riccati 方程在一般的情況下，解**不能用初等函數表示**。

這是數學史上第一次有人嚴格證明「解不出來」——從此數學家知道了：大多數微分方程的解，是「造不出來」的新函數，而不是「藏起來」的初等函數。

## 偵查過程

### 第一步：什麼是「初等函數」？

要證明「解不是初等函數」，必須先精確定義「初等函數」。Liouville 採用的定義：初等函數是從 $x$、常數出發，經過**有限次**的四則運算、代數運算（開方等）、指數、對數、三角函數組合而成的函數。

例如 $\sqrt{x^2+1}\,e^{\arctan x}$、$\dfrac{\ln(\sin x)}{x}$ 都是初等函數。關鍵限制是「有限次組合」——無窮級數不算。

### 第二步：偵查武器——Liouville 定理（積分形式）

Liouville 的核心武器是他自己發現的定理（今稱 Liouville 定理）：**若一個初等函數的積分仍是初等函數，則該積分必定具有特定形式**。具體而言，對形如

$$
\int f(x)\,e^{g(x)}\,dx
$$

的積分，若它是初等函數，則必存在有理函數 $R(x)$ 使得

$$
\int f(x)\,e^{g(x)}\,dx = R(x)\,e^{g(x)} + \text{常數}.
$$

「積分若存在（初等），就必須長成這個樣子」——這是「證明不存在」的經典策略：列出所有可能形狀，再逐一證明每個形狀都行不通。

這個定理是**微分代數**（differential algebra）的先聲：把函數放進一個「代數結構」中研究其微分性質，而不在乎具體的解析形式。日後 Picard-Vessiot 理論將把這套思想完全代數化。

### 第三步：把 Riccati 方程化為二階線性方程

Liouville 的關鍵觀察：Riccati 方程可以透過變數替換**線性化**。設

$$
y = -\frac{u'}{a(x)\,u},
$$

其中 $u$ 是新的未知函數。計算 $y'$：先對 $y = -\dfrac{u'}{au}$ 求導：

$$
y' = -\frac{u''}{a u} + \frac{(u')^2}{a u^2} + \frac{a' u'}{a^2 u}.
$$

把它代入 Riccati 方程 $y' = a y^2 + b y + c$：

- $a y^2 = a\cdot\dfrac{(u')^2}{a^2u^2} = \dfrac{(u')^2}{a u^2}$；
- $b y = -\dfrac{b u'}{a u}$。

代入後 $(u')^2$ 項兩邊相消，整理得到：

$$
u'' - \left(\frac{a'}{a} + b\right)u' + a\,c\,u = 0.
$$

**Riccati 方程等價於一個二階線性 ODE**。特別地，最簡單的例子 $y' = y^2 + 1$（$a = c = 1, b = 0$）對應

$$
u'' + u = 0,
$$

解 $u = A\cos x + B\sin x$，於是 $y = -u'/u = \dfrac{A\sin x - B\cos x}{A\cos x + B\sin x} = \tan(x + \varphi)$。✓ 這正是 $\tan$ 的微分方程。

### 第四步：偵查高潮——證明初等解不存在

現在考慮標準形式

$$
y' = y^2 + x \quad (\text{即 } a=1,\ b=0,\ c=x),
$$

它對應二階線性方程

$$
u'' + x\,u = 0.
$$

Liouville 論證的要點：假設 $y$ 是初等函數，則 $u$（由 $u'/u = -ay$ 透過積分得到）也涉及初等函數的積分。利用他的積分定理，任何初等的 $u$ 必須具有特定形式；但對 $u'' + xu = 0$（即 Airy 方程的親戚），逐步檢查所有可能形式——有理函數、有理函數乘指數、對數項——每一種都導出矛盾。

例如：假設 $u = R(x)e^{g(x)}$，$R, g$ 為有理函數。代入 $u'' + xu = 0$：

$$
u'' = e^{g}\big[R'' + 2R'g' + R(g'') + R(g')^2\big],
$$

方程變成

$$
R'' + 2R'g' + R\,g'' + R(g')^2 + xR = 0.
$$

考察 $x \to \infty$ 的漸近行為：解的漸近展開涉及分數冪 $x^{3/2}$ 的項（$u \sim x^{-1/4}\sin\frac{2}{3}x^{3/2}$），而有限次的有理函數與指數組合**無法**產生 $x^{3/2}$ 這種分數冪相位的振盪——矛盾。因此 $y$ 不能是初等函數。

（用現代語言：這個方程的解是 Airy 函數 $\mathrm{Ai}(-x)$ 的近親，Airy 函數不在初等函數的微分域擴張之中。）

### 第五步：覺悟——「大多數方程解不出來」

Liouville 的結果波及整個數學界。結論遠不止 Riccati 一例：他證明了 $\displaystyle\int e^{-x^2}dx$（誤差函數的積分）不是初等函數；他的理論框架可以判定一大批方程的初等可積性。數學家終於覺悟：

- **大多數微分方程沒有初等函數解**——「解不出來」是常態，「解得出來」是例外；
- 解不存在的方程，其解本身就是**新的特殊函數**（Bessel、Airy、Legendre……參見 [1812-Gauss與超幾何函數.md](1812-Gauss與超幾何函數.md)）；
- 對不可積的方程，出路是：級數解、漸近解，或**數值方法**。

## 結案報告

Liouville 解開了 Riccati 之謎：一般的 Riccati 方程沒有初等函數解，這不是「還沒找到」，而是「不存在」。

遺產：

1. **微分代數**：Liouville 的思想在十九世紀末由 Picard-Vessiot 理論完全代數化，成為判定「方程可否用有限次運算解出」的系統工具。
2. **特殊函數論的正當性**：Airy、Bessel、誤差函數從此有了「存在的理由」——它們是微分方程的解，本來就不可能是初等函數（參見 [1812-Gauss與超幾何函數.md](1812-Gauss與超幾何函數.md)、[1858-SturmLiouville理論.md](1858-SturmLiouville理論.md)）。
3. **數值方法的覺醒**：既然解析解是例外，數值方法（Euler 法、Runge-Kutta 法）成為解微分方程的正規軍——這是二十世紀計算數學興起的理論前提。
4. **可積系統的判據**：Liouville 的可積性概念（需要多少個運動積分）直接影響 Hamilton-Jacobi 理論（參見 [1838-Jacobi與Hamilton-Jacobi方程.md](1838-Jacobi與Hamilton-Jacobi方程.md)）與 Poincaré 對三體問題「不可解」的證明（參見 [1886-Poincare三體問題.md](1886-Poincare三體問題.md)）。
5. **不可證明性的先聲**：證明「某事不可能用某類工具完成」，這種思維模式與日後 Galois 理論（五次方程無根式解）、Gödel 不完備定理一脈相承。

## 證據與工具

```python
# Liouville 可積性之謎：數值探索 Riccati 方程與 Airy 函數
import numpy as np
from scipy.integrate import solve_ivp
from scipy.special import airy

# 1) Riccati 方程 y' = y^2 + 1 的初等解：y = tan(x + phi)
sol = solve_ivp(lambda t, y: y**2 + 1, [0, 1], [0.0], max_step=0.01)
print("y' = y^2+1 數值解 y(1) =", sol.y[0][-1], " tan(1) =", np.tan(1))

# 2) Riccati 方程 y' = y^2 + x：解不是初等函數（Airy 函數的親戚）
# 線性化：y = -u'/u => u'' + x u = 0
sol_u = solve_ivp(lambda t, z: [z[1], -t*z[0]], [0, 3], [1.0, 0.0], max_step=0.01)
q, qp = sol_u.y
y_riccati = -qp/q          # 由線性化解反推 Riccati 的解
# 漸近行為：涉及 x^{3/2} 相位——初等函數組合無法產生
print("線性化反推的 Riccati 解 y(1) =", y_riccati[np.argmin(np.abs(sol_u.t - 1))])
print("（此解即 Airy 型函數，不能用初等函數表示）")

# 3) Airy 函數的漸近行為：相位 ~ (2/3) x^{3/2}
x_a = np.linspace(5, 15, 200)
ai, aip, bi, bip = airy(x_a)
phase_asymptotic = 2/3 * x_a**1.5
# 檢驗漸近公式 Ai(x) ~ exp(-2x^{3/2}/3)/(2 sqrt(pi) x^{1/4})
ai_asym = np.exp(-phase_asymptotic)/(2*np.sqrt(np.pi)*x_a**0.25)
err = np.max(np.abs(ai - ai_asym)/np.abs(ai))
print(f"Airy 漸近公式最大相對誤差 = {err:.4f}（x 越大越準）")
print("注意相位是 x^(3/2)——分數冪，這正是初等函數組合無法企及的結構")

# 4) 對照組：初等可積的方程 y' = y（解 e^x 是初等函數）
sol_e = solve_ivp(lambda t, y: y, [0, 2], [1.0], max_step=0.01)
print("y' = y 數值解 y(2) =", sol_e.y[0][-1], " e^2 =", np.exp(2))

# 5) 視覺化：Airy 函數（微分方程的新解）vs tan x（初等解）
import matplotlib.pyplot as plt
plt.figure(figsize=(8,4))
plt.subplot(1,2,1)
plt.plot(x_a, ai, label="Ai(x)（Airy：非初等）")
plt.plot(x_a, ai_asym, '--', label="漸近公式")
plt.legend(); plt.title("非初等解：Airy 函數")
plt.subplot(1,2,2)
t2 = np.linspace(0, 1.4, 100)
plt.plot(t2, np.tan(t2), label="tan(x)（初等解）")
plt.legend(); plt.title("初等解：Riccati 特例 y'=y^2+1")
plt.savefig("liouville.png", dpi=100)
print("已存圖 liouville.png")
```
