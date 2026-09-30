# 1829 — Dirichlet 函數概念

## 案件摘要
1829 年，Peter Gustav Lejeune Dirichlet 發表〈Sur la convergence des séries trigonométriques...〉，給出 Fourier 級數收斂的第一個嚴格定理；同年在這篇論文中，他丟出了一顆震撼彈——一個**處處不連續的函數** $D(x) = 1_{x\in\mathbb{Q}}$。這個「怪物」用最簡單的定義撕毀了 18 世紀對「函數」的想像，迫使數學界徹底解放函數概念，也為日後的測度論埋下伏筆。

## 前因 -- 為什麼會有這個案子
- 1807 年 Fourier 宣稱「任意函數」都能展開成三角級數 $\frac{a_0}{2} + \sum (a_n\cos nx + b_n\sin nx)$，1822 年出版《Théorie analytique de la chaleur》。他解決了熱傳導問題，卻完全沒說清楚「任意函數」是什麼、級數何時收斂。
- 18 世紀的主流觀點（Euler 早期、Lagrange）認為函數必須由解析式給出，至少是「光滑的曲線」。Fourier 的級數居然能表示帶角點、甚至分段定義的函數，令數學界困惑：函數的邊界到底在哪裡？
- Cauchy（1821–1823）建立了極限與連續的定義，並證明連續函數的積分極限存在——但他的理論默認函數「大致連續」。
- 案件成形：Fourier 的主張需要一個判決。Dirichlet 曾在巴黎與 Fourier 親近，深知這個問題的分量。1829 年，他交出了判決書——外加一個沒人預料到的「證物」。

## 線索與推理 -- 數學式、程式、理論

### 線索一：Dirichlet 收斂定理
Dirichlet 證明：若 $f$ 在 $[-\pi, \pi]$ 上**分段連續且有界**、只有有限個極值點（Dirichlet 條件），則 Fourier 級數在每個點收斂，且收斂到

$$\frac{f(x^+) + f(x^-)}{2}$$

即左右極限的平均。在連續點處級數收斂到 $f(x)$ 本身；在跳躍點處收斂到「中間值」。這是 Fourier 主張的第一個嚴格版本：**大部分**函數確實可以展開，但必須附上條件。判決出爐，Fourier 半勝。

### 線索二：證明的關鍵武器——Dirichlet 核
Dirichlet 把部分和化為積分形式（今日稱 Dirichlet 積分表示法）：

$$S_N(x) = \frac{1}{\pi}\int_{-\pi}^{\pi} f(x+t)\, \frac{\sin\left((N+\frac{1}{2})t\right)}{2\sin(t/2)}\,dt$$

其中 $D_N(t) = \frac{\sin((N+1/2)t)}{2\sin(t/2)}$ 就是 **Dirichlet 核**。他證明：當 $N \to \infty$，這個積分在 Dirichlet 條件下收斂到 $\frac{f(x^+)+f(x^-)}{2}$。證明中他系統性地使用了「一致收斂」與「逐步極限」的論證，比 Cauchy 更精細。

順帶一提，Dirichlet 在同一篇論文中還計算了著名積分

$$\int_0^x \frac{\sin t}{t}\,dt$$

的收斂性（當 $x \to \infty$ 收斂到 $\frac{\pi}{2}$），這個積分日後被稱為 **Dirichlet 積分**，成為傅立葉分析與機率論（特徵函數）中的標準工具。

### 線索三：處處不連續函數——函數概念的解放
為了回答「哪些函數**不能**展開」，Dirichlet 在論文中給出一個反例：

$$D(x) = \begin{cases} 1, & x \in \mathbb{Q} \\ 0, & x \notin \mathbb{Q} \end{cases}$$

這個函數**處處不連續**：任何點的任何鄰域內，$D$ 的值都在 0 與 1 之間震盪。它的 Fourier 級數不存在（甚至連「圖像」都畫不出來）。但更重要的是它的哲學衝擊：

- $D$ 是一個**完全合法的函數**——每個輸入都有唯一輸出，這才是函數的本質。
- 函數不必有解析式、不必連續、甚至不必能畫圖。「函數 = 任意對應規則」的概念革命由此定調。
- 這一定調直接催生了 Riemann（1854）對可積性的研究：既然函數可以這麼病態，那 Cauchy 的積分理論還能撐多久？

### 線索四：測度論的伏筆
$D(x)$ 還埋著更深的一問：這個函數「在什麼意義下幾乎是 0」？有理數雖然無窮多，卻「稀疏」；無理數「稠密」且「更多」。要回答這個問題，需要「集合的大小」的理論——這條線索要到 Cantor 的集合論（1874 起）與 Lebesgue 的測度論（1902）才被解開。屆時答案是：$D(x)$ 在 Lebesgue 積分下等於 0，因為有理數集的測度為零。1829 年的怪物，在 73 年後被馴服。

### 程式碼範例：Dirichlet 函數與其「部分和」的視覺化
$D(x)$ 畫不出來，但我們可以畫出它的有限近似：只取分母小於 $N$ 的有理數：

```python
import numpy as np
import matplotlib.pyplot as plt
from fractions import Fraction

# D(x) 的有限近似：x 等於「分母 <= N 的有理數」時取 1
x = np.linspace(0, 1, 4000)

fig, axes = plt.subplots(1, 3, figsize=(14, 4), sharey=True)
for ax, N in zip(axes, [5, 12, 40]):
    rationals = [Fraction(p, q) for q in range(2, N + 1) for p in range(1, q)
                 if np.gcd(p, q) == 1]
    y = np.zeros_like(x)
    for r in rationals:
        y[np.abs(x - float(r)) < 0.0005] = 1
    ax.scatter(x, y, s=0.3, c="navy")
    ax.set_title(f"D_N(x): 分母 ≤ {N} 的有理數")
    ax.set_xlabel("x")
plt.suptitle("Dirichlet 函數的有限近似：有理點越來越密 → 處處不連續")
plt.show()

# 驗證：D(x) 的黎曼上和 = 1，下和 = 0（任何分割都一樣）
# → 黎曼不可積；但「有理點測度 = 0」暗示 Lebesgue 積分為 0
print("任何區間內既有有理數也有無理數 → 上和-下和 = 1 ≠ 0 → 黎曼不可積")
```

圖像顯示：隨著允許的分母變大，「等於 1 的點」越來越密，在任何小區間內都會出現——這正是「處處不連續」的視覺證據。而黎曼上和恆為 1、下和恆為 0，宣告 $D$ 不可積。

## 結案 -- 後果與影響
- Fourier 級數收斂問題獲得第一個嚴格判決：Dirichlet 條件下的收斂定理成為傅立葉分析的基石。
- **函數概念革命**：函數被定義為「任意對應規則」，解析式、連續性、可畫圖性全部退位。這是現代函數論的起點。
- 處處不連續函數暴露 Cauchy 積分理論的極限，直接刺激 Riemann（1854）研究「哪些函數可積」。
- 「有理數集有多小？」的追問為 Cantor 集合論（1874）與 Lebesgue 測度論（1902）埋下伏筆——最終 $D(x)$ 成為測度論的招牌例子：Lebesgue 可積且積分為 0。
- Dirichlet 本人後來接替 Gauss 在哥廷根的教席，並深刻影響了 Riemann——案件的下一棒早已安排好。
- 另一條支線：Dirichlet 1837 年在〈Über die Darstellung ganzlich unbekannter Functionen...〉中進一步把函數定義為「若對區間內每個 $x$ 都有唯一的 $y$ 與之對應，則 $y$ 是 $x$ 的函數」——這個定義今天仍在教科書中，是「對應規則」概念的正式定調。他也是解析數論的創立者（Dirichlet L-函數、算術級數中的素數定理），數學風格「以最少的假設得到最精確的結論」影響了整個德國學派。

## 關鍵人物與文獻
| 人物 | 角色 |
|---|---|
| Peter Gustav Lejeune Dirichlet | 收斂定理、Dirichlet 函數、函數概念解放 |
| Joseph Fourier | 熱傳導與三角級數，提出問題 |
| Augustin-Louis Cauchy | 極限理論，被反例挑戰 |
| Bernhard Riemann | 接手研究可積性 |
| Henri Lebesgue | 用測度論馴服 Dirichlet 函數 |

- P. G. L. Dirichlet, 〈Sur la convergence des séries trigonométriques qui servent à représenter une fonction arbitraire entre des limites données〉, J. reine angew. Math. **4**, 157–169 (1829)。
- J. Fourier, *Théorie analytique de la chaleur*, Paris (1822)。
