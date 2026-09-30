# 1821 — Cauchy 極限與連續

## 案件摘要
1821 年，Cauchy 在巴黎出版《Cours d'Analyse de l'École Royale Polytechnique》（分析教程），為微積分的基礎發動最徹底的一次「重審」：他首次以**極限**為唯一起點，定義連續性、級數收斂與積分，並提出數列收斂的**Cauchy 判準**（收斂數列的項最終會任意接近）。無窮小的幽靈、級數的濫用、Lagrange 冪級數路線的不足，全部在這本書中被逐一釐清。這是分析學嚴格化運動的開端證書。

## 前因 -- 為什麼會有這個案子
- **百年基礎危機**：Newton 的極限與 Leibniz 的無窮小都缺乏嚴格定義。Berkeley 1734 年《The Analyst》的攻擊懸而未決；18 世紀數學家靠「形式操作的正確直覺」工作，但直覺屢屢失靈。
- **級數濫用的悖論**：Euler 式的大膽操作產生一堆悖論：$\sum \frac{1}{n^2} = \frac{\pi^2}{6}$ 是對的，但同樣手法也產生錯誤結果。發散級數 $\sum (-1)^n$ 的和到底是多少？逐項積分何時合法？沒有人說得清。
- **Lagrange 冪級數路線的不足**：Lagrange（1797）企圖以冪級數重建微積分，但「任意函數可展開」是未證明的假設，收斂半徑的謎團無法在實代數框架內解釋。Cauchy 曾是這條路線的學習者（他最初崇敬 Lagrange），但意識到必須換一條路。
- **Fourier 級數的引爆**：Fourier 1807/1822 年《Théorie analytique de la chaleur》斷言「任意函數」都可展開為三角級數——連不連續函數都可以！這與 Lagrange 的信念直接衝突，迫使數學界必須回答：什麼是函數？什麼是收斂？什麼是積分？Cauchy 的《Cours d'Analyse》正是對這場危機的回應。

## 線索與推理 -- 數學式、程式、理論

### 線索一：極限的敘述——無窮小的除名
《Cours d'Analyse》開篇，Cauchy 首次給出極限的語言化定義：**若一個變數逐次取值趨近某個固定值，使得最終與固定值的差可以任意小，則稱固定值為這些值的極限**。

以此為基礎：
- **無窮小被重新定義**：無窮小不再是「幽靈量」，而是「極限為 0 的變數」——它降級為一個普通概念的特例。
- **導數**：$f'(x) = \displaystyle\lim_{i\to 0}\frac{f(x+i)-f(x)}{i}$——極限是定義，增量 $i$ 是普通變數，Berkeley 的攻擊正式失效。
- **連續性**：Cauchy 的定義——若 $f(x+i) - f(x)$ 隨 $i$ 趨於 0 而趨於 0，即

$$\lim_{\Delta x \to 0} f(x + \Delta x) = f(x)$$

則 $f$ 在 $x$ 連續。**連續性第一次成為精確概念**，而不再是「筆不離紙」的幾何直覺。

### 線索二：級數收斂與 Cauchy 判準
Cauchy 定義級數收斂：部分和 $S_n = \sum_{k=0}^{n} u_k$ 趨於極限 $S$。更關鍵的是**Cauchy 判準**：

$$\text{數列 } (S_n) \text{ 收斂} \iff \forall \varepsilon > 0, \exists N, \; m, n > N \Rightarrow |S_m - S_n| < \varepsilon$$

**收斂性的判定不需要預先知道極限**——只需檢查項之間是否任意接近。這解決了「如何證明收斂」的百年難題。Cauchy 用它判定：等比級數收斂、調和級數 $\sum 1/n$ 發散（部分和的差可以任意大）、以及正項級數的各種判準（今日教科書的 Cauchy 根值判準、比值判準前身）。

他也首次明確提出：**收斂級數才能求和，發散級數的和沒有意義**——Euler 時代的形式求和被正式除名（Abel 1826 年響應：「發散級數是魔鬼的發明」）。

### 線索三：逐項操作的條件與連續函數的性質
Cauchy 證明了 18 世紀直覺操作的成立條件：
- **連續函數的中值定理**：若 $f$ 在 $[a,b]$ 連續且 $f(a)f(b)<0$，則存在 $c$ 使 $f(c)=0$（他 1821 年的證明依賴「連續函數的介值性」——這在當時的直觀實數觀下是顯然的，要到 Dedekind 1872 年的實數構造才完全嚴格）。
- **一致收斂的萌芽**：Cauchy 1821 年曾「證明」連續函數的收斂級數之和連續——這個證明有漏洞（漏了「一致收斂」條件），由 Seidel（1847）與 Stokes（1848）指出，Weierstrass 完成補救。**逐項積分、逐項微分、級數和的連續性，全部需要一致收斂**——這是 Cauchy 判準之後分析學最重要的技術概念。
- **定積分的嚴格化**：Cauchy 1823 年以有限和的極限定義積分 $\int_a^b f(x)\,dx$（Cauchy 積分，Riemann 積分的前身），並證明連續函數可積。

### 線索四：從 Cauchy 到 ε-δ——Weierstrass 的完成
Cauchy 的極限定義仍用自然語言（「可以任意小」），且他的「實數」仍是直觀的。Weierstrass 在 1870 年代柏林的講座中，把極限翻譯成純粹的邏輯語言：

$$\lim_{x \to a} f(x) = L \iff \forall \varepsilon > 0, \exists \delta > 0, \; 0 < |x - a| < \delta \Rightarrow |f(x) - L| < \varepsilon$$

這就是 **ε-δ 定義**。配合 Dedekind（1872）的實數構造與 Cantor（1872）的實數完備性，Cauchy 判準終於有了嚴格基礎（**完備性**：Cauchy 數列必收斂——這是實數的定義性質，有理數不具備）。現代分析學的「ε-嚴格化」傳統在此定型。

### 程式碼範例：Cauchy 判準與收斂發散的數值偵查
```python
import numpy as np
import matplotlib.pyplot as plt

# 1) Cauchy 判準的數值檢查：等比級數（收斂）vs 調和級數（發散）
def partial_sums(seq, n_max):
    s, out = 0.0, []
    for k in range(1, n_max + 1):
        s += seq(k)
        out.append(s)
    return np.array(out)

N = 200
S_geo = partial_sums(lambda k: 0.5**k, N)      # 收斂到 1
S_har = partial_sums(lambda k: 1.0 / k, N)     # 發散（~ln n）

def cauchy_check(S, eps, tail):
    """檢查尾部任意兩項之差是否 < eps"""
    return np.max(np.abs(S[tail:] - S[-1])) < eps

print("Cauchy 判準檢查（檢查最後 50 項的最大波動）：")
print(f"  等比級數: max|S_m - S_n| = {np.max(np.abs(S_geo[-50:] - S_geo[-1])):.2e}"
      f"  < 0.001 ? {cauchy_check(S_geo, 1e-3, 50)}")
print(f"  調和級數: S_{N} - S_{N-50} = {S_har[-1] - S_har[-51]:.2e}"
      f"  < 0.001 ? {cauchy_check(S_har, 1e-3, 50)}")

# 2) Cauchy 反例回顧：光滑但不可展開
x = np.linspace(-2, 3, 500)
f_cauchy = np.exp(-1 / np.where(x == 0, 1, x**2))

# 3) 連續函數的介值性：求根（Cauchy 中值定理的應用）
from scipy.optimize import brentq
root = brentq(lambda t: t**3 - 2*t - 5, 1, 3)
print(f"\n介值性求根: x^3 - 2x - 5 = 0 的根 ≈ {root:.10f}")

fig, ax = plt.subplots(1, 2, figsize=(11, 4))
ax[0].plot(np.arange(1, N+1), S_geo, label="Σ 0.5^k → 1（收斂）")
ax[0].plot(np.arange(1, N+1), S_har, label="Σ 1/n → ∞（發散）")
ax[0].axhline(1, ls="--", c="gray", lw=0.5)
ax[0].legend(); ax[0].set_title("Cauchy 判準：收斂 vs 發散")
ax[1].plot(x, f_cauchy, lw=2, label="e^{-1/x²}（連續，導數全 0）")
ax[1].plot(x, np.zeros_like(x), "r--", lw=1, label="Maclaurin 級數 = 0")
ax[1].set_ylim(-0.1, 1.2); ax[1].legend()
ax[1].set_title("光滑 ≠ 可展開（Cauchy 反例）")
plt.show()
```

數值輸出顯示：等比級數尾部波動小於 0.001（通過 Cauchy 判準，收斂），調和級數尾部兩項之差遠大於 0.001（不通過，發散）——判準在數值上區分了兩種命運。而 Cauchy 反例再次展示「連續」與「可展開」的分界。

## 結案 -- 後果與影響
- **分析學嚴格化的開端**：極限成為微積分的唯一起點，無窮小的幽靈被除名（直到 1960 年代 Robinson 的非標準分析才以嚴格形式復活）。
- **級數理論的重建**：收斂定義、Cauchy 判準、一致收斂的萌芽，終結了 Euler 時代的形式操作，Abel、Dirichlet、Weierstrass 循此路線完成級數理論。
- **實數的嚴格化**：Cauchy 判準暴露「什麼是實數」的問題，Dedekind（1872）與 Cantor（1872）的實數構造補完基礎，**完備性**成為實數的定義性質。
- **Weierstrass 的 ε-δ**：Cauchy 的語言化定義被翻譯成純邏輯，現代教科書的極限定義直接沿用至今。
- **通往 20 世紀**：Lebesgue 積分（1902）、泛函分析、度量空間的完備性理論（Banach 空間），全部以 Cauchy 判準為基石。
- 影響至今：任何一本分析教科書的第一章，都是 1821 年這場重審的直接後代。

## 關鍵人物與文獻
| 人物 | 角色 |
|---|---|
| Augustin-Louis Cauchy | 1821 年《Cours d'Analyse》，極限、連續、Cauchy 判準 |
| Joseph Fourier | 三角級數引爆基礎危機 |
| Joseph-Louis Lagrange | 冪級數路線的倡議者（Cauchy 的先驅） |
| Karl Weierstrass | ε-δ 定義，一致收斂的完成 |
| Richard Dedekind | 1872 年實數構造，完備性的基礎 |
| Niels Abel | 批判發散級數，響應嚴格化 |

- A.-L. Cauchy, *Cours d'Analyse de l'École Royale Polytechnique*, Paris (1821)。英譯：R. Bradley & C. E. Sandifer, *Cauchy's Cours d'analyse*, Springer (2009)。
- J. Fourier, *Théorie analytique de la chaleur*, Paris (1822)。
- V. J. Katz, *A History of Mathematics*, 3rd ed., Pearson (2009)。
