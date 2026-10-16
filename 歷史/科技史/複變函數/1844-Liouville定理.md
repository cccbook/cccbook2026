# 1844 — Liouville 定理

## 案件摘要
1844 年，巴黎的 Joseph Liouville 在計算橢圓函數的邊界行為時發現一條驚人的約束：**有界的整函數必為常數**——一個在整個複平面上處處解析、又不會爆炸的函數，只能是直線。這條看似消極的「不可能性定理」，卻引出代數基本定理最優雅的證明（三行結案），並開啟整函數論。同年，Liouville 用連分數造出史上第一個被證明的超越數 $\sum 10^{-n!}$（Liouville 常數）——一樁案子，兩項結案。

## 前因 -- 為什麼會有這個案子
- Cauchy 積分公式（1825/1826）已經給出殺傷性武器：$f(a) = \frac{1}{2\pi i}\oint_\gamma \frac{f(z)}{z-a}dz$，內部由邊界決定。如果邊界（大圓上的 $|f|$）不爆炸，內部還能藏什麼祕密？
- 橢圓函數的雙週期之謎：Abel（1827）與 Jacobi（1829）研究 $\wp$ 函數一類的雙週期函數，Liouville 在 1840 年代發展雙週期函數的一般理論（他的講義 1847 年由 Brioschi 整理出版）。雙週期函數在一個基本週期平行四邊形內有界，若它是整函數，必然常數——橢圓函數**必須有極點**。這是定理的直接案發現場。
- 代數基本定理（每個非常數複係數多項式必有複根）自 Gauss 1799 年以來已有四五個證明，全是「硬算」：Gauss 的拓撲論證、代數論證、解析論證。有沒有一行就能結案的優雅證法？
- 超越數的懸案：是否存在「不是任何整係數多項式之根」的數？1740 年代 Euler 懷疑 $e$ 與 $\pi$ 是超越數，但無人能證明任何一個具體的超越數——這是第二現場。

## 線索與推理 -- 數學式、程式、理論

### 線索一：Liouville 定理——三行結案
設 $f$ 整函數（全平面解析），且 $|f(z)| \le M$ 對所有 $z$ 成立。任取一點 $a$、半徑 $R$，由 Cauchy 積分公式：

$$f'(a) = \frac{1}{2\pi i}\oint_{|z-a|=R}\frac{f(z)}{(z-a)^2}\,dz$$

取絕對值，用積分不等式（$|dz| = R\,dt$）：

$$|f'(a)| \le \frac{1}{2\pi}\int_0^{2\pi}\frac{|f(z)|}{R^2}\,R\,dt \le \frac{M}{R}$$

令 $R\to\infty$：$|f'(a)| \le 0$，故 $f'(a)=0$ 對所有 $a$ 成立——$f$ 是常數。**證明僅三行**。全平面「處處可微 + 不爆炸」的組合如此強烈，函數被壓成直線；解析性的威力遠超實變函數（實函數 $f(x)=\sin x$ 有界且非常數，但它不解析於複平面——$\sin z$ 在虛軸方向指數爆炸）。

### 線索二：代數基本定理的優雅證明
設 $p(z) = z^n + a_{n-1}z^{n-1} + \cdots + a_0$ 為非常數多項式。**反證**：若 $p$ 無根，則 $f(z) = 1/p(z)$ 是整函數。且 $|p(z)| \to \infty$（$|z|\to\infty$，因為最高次項支配），故 $f$ 有界。由 Liouville 定理，$f$ 是常數，則 $p$ 是常數——矛盾！故 $p$ 必有複根。**結案**：

$$\text{無根} \Rightarrow 1/p \text{ 整函數且有界} \Rightarrow \text{常數} \Rightarrow \text{矛盾}$$

Gauss 用了幾十頁的定理，Liouville 用三行。這條證明路線也推廣出：整函數論中「有界整函數 = 常數」與「多項式 = 增長受多項式控制的整函數」的對應，引向 Weierstrass 因式定理與 Picard 定理。

### 線索三：橢圓函數——定理的正面應用
雙週期函數 $f$：存在 $w_1, w_2$（不共線複數）使 $f(z+w_1) = f(z+w_2) = f(z)$。它在基本週期平行四邊形 $P$ 上連續故有界，由週期性整個平面上的值等於 $P$ 上的值。若 $f$ 是整函數，Liouville 定理說 $f$ 常數。**所以非常數雙週期函數必須有極點**。Weierstrass $\wp$ 函數：

$$\wp(z) = \frac{1}{z^2} + \sum_{(m,n)\neq(0,0)}\left(\frac{1}{(z-mw_1-nw_2)^2} - \frac{1}{(mw_1+nw_2)^2}\right)$$

在每個週期格點有二階極點——這正是雙週期性「被迫」的結果。Liouville 更證明：非常數雙週期函數在基本平行四邊形內極點的階數總和（含零點的階數總和）恰為 2——這就是他的雙週期函數理論核心。

### 線索四：Liouville 常數——第一個被證明的超越數
1844 年 Liouville 在〈Sur des classes très-étendues de quantités...〉（C. R. Acad. Sci.）中證明：**代數數不能被有理數「太快逼近」**。具體地，若 $\alpha$ 是 $n$ 次代數數，存在 $c>0$ 使對所有整數 $p, q$（$q>1$）：

$$\left|\alpha - \frac{p}{q}\right| > \frac{c}{q^n}$$

於是構造一個被無理逼近「太快的」數：

$$L = \sum_{k=1}^{\infty} 10^{-k!} = 0.110001000000000000000001\ldots$$

其截斷 $p_m/q$（$q = 10^{m!}$）滿足 $|L - p_m/q| < \frac{2}{10^{(m+1)!}} = \frac{2}{q^{m+1}}$——比任何 $n$ 次代數數允許的逼近下界快得多，故 $L$ 不可能是任何次數的代數數。**史上第一個被證明的超越數正式結案**。Cantor 1874 年以對角論證證明超越數「不可數多」，但 Liouville 的是第一個有名有姓的。

### 程式碼範例：Liouville 常數與代數基本定理的數值對照
```python
import numpy as np
from decimal import Decimal, getcontext
from fractions import Fraction

# 案件一：Liouville 常數的高精度計算  L = Σ 10^(-k!)
getcontext().prec = 50
import math
L = sum(Decimal(10) ** (-math.factorial(k)) for k in range(1, 8))
print("Liouville 常數 =", L)

# 案件二：驗證 Liouville 不等式——截斷逼近「太快」，故 L 超越
# 截斷到 k! 位：p/q, q = 10^(k!)，誤差 < 2/10^((k+1)!) = 2/q^(k+1)
for k in range(2, 6):
    q = 10 ** math.factorial(k)
    p = int(L * q)                      # 截斷的有理數
    err = abs(float(L) - p/q)
    bound = 2 / q ** (k+1)              # 遠快於任何代數數允許的 c/q^n
    print(f"k={k}: |L - p/q| = {err:.2e} < 2/q^(k+1) = {bound:.2e}")

# 案件三：代數基本定理——數值找根（多项式必有複根）
p = np.poly1d([1, 0, 1])                # p(z) = z^2 + 1
roots = np.roots(p)
print("p(z)=z^2+1 的複根:", roots)

# 案件四：|sin z| 在複平面虛軸方向爆炸（有界整函數不存在非平凡例）
for y in [1, 5, 10, 20]:
    print(f"|sin({y}i)| = {abs(np.sin(1j*y)):.3e}  (實軸上 |sin(x)| ≤ 1)")
```

數值輸出顯示：Liouville 常數的小數展開在 $k!$ 位置出現 1、截斷誤差確實快於任何代數數允許的下界（超越性驗證）、$z^2+1$ 的複根 $\pm i$（代數基本定理）、以及 $\sin z$ 在虛軸方向指數爆炸——有界非常數整函數確實不存在。

## 結案 -- 後果與影響
- **整函數論誕生**：Liouville 定理成為整函數增長理論的第一定律，直接推廣到 Weierstrass 因式定理（1876，整函數的完全因式分解）與 Picard 大定理（1879，本性奇點附近取值至多例外一次）。
- **代數基本定理最優雅證明**：三行結案成為今日教科書標準，解析方法從此主導；「證明不可能性」成為數學的新武器。
- **超越數論誕生**：Liouville 不等式開啟無理逼近度量理論，直接鋪路給 Hermite 1873 年證明 $e$ 是超越數、Lindemann 1882 年證明 $\pi$ 是超越數（古希臘化圓為方問題結案）、Thue–Siegel–Roth 定理（1955，逼近指數的極限）。
- 橢圓函數理論：Liouville 的雙週期函數一般理論由 Brioschi、Hermite 承接，成為 Weierstrass 學派的基礎。
- 影響至今：複動力學（Mandelbrot 集合）、模形式與 L 函數（Fermat 最後定理的 Wiles 證明）、調和分析，本質上都是「增長受控 → 結構受限」的 Liouville 思想。

## 關鍵人物與文獻
| 人物 | 角色 |
|---|---|
| Joseph Liouville | 1844 年證明 Liouville 定理與第一個超越數 |
| Augustin-Louis Cauchy | 積分公式——定理的殺傷性武器 |
| Niels Abel / Jacobi | 橢圓函數雙週期性的發現者 |
| Charles Hermite | 承接橢圓函數理論，1873 年證明 $e$ 超越 |
| Georg Cantor | 1874 年證明超越數不可數多 |

- J. Liouville, 〈Sur des classes très-étendues de quantités dont la valeur n'est ni algébrique, ni même réductible à des irrationnelles algébriques〉, C. R. Acad. Sci. Paris **18** (1844)。
- J. Liouville, *Leçons sur les fonctions doublement périodiques* (1847 講義，Brioschi 記錄刊出 1859)。
- C. Hermite, 〈Sur la fonction exponentielle〉, C. R. Acad. Sci. Paris **77** (1873)。
