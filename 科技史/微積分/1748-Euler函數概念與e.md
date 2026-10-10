# 1748 — Euler 函數概念與 e

## 案件摘要
1748 年，Euler 在柏林出版兩卷本巨著《Introductio in analysin infinitorum》（無窮分析引論）。這本書做了一件看似平淡卻徹底改變數學的事：把「函數」確立為分析學的基本對象，並以冪級數為函數的標準表示。書中系統闡述了 $e$ 與 $e^x$、$e$ 的定義級數、$\sin x$ 與 $\cos x$ 的展開式，以及那條被譽為最美數學式的 Euler 恆等式：

$$e^{i\pi} + 1 = 0$$

微積分從此有了統一的語言。這是分析學「標準化」的結案證書。

## 前因 -- 為什麼會有這個案子
- **對數與指數的混亂**：17 世紀的對數是純計算工具（Napier, 1614），指數記號 $a^x$ 對無理數指數的意義模糊不清。Bernoulli 兄弟與 Leibniz 曾為「$\log(-x)$ 是否有意義」爭論不休，$\log x$ 與 $e^x$ 的互逆關係直到 1690 年代才被釐清。
- **函數概念的模糊**：Leibniz 1694 年首次使用「function」一詞，但意思只是「幾何量的依賴關係」。18 世紀初，「函數」與「曲線」、「解析式」的關係糾纏不清，John Bernoulli 與 Euler 之間還有「任意曲線是不是函數」的辯論（延伸到 1747 年 d'Alembert 的弦振動爭論）。
- **級數計算的積累**：Mercator（1668）已算出 $\ln(1+x)$ 的級數；Newton 有 $\arctan$、二項級數；Leibniz 有 $\frac{\pi}{4} = 1 - \frac13 + \frac15 - \cdots$。但這些都是零散案例，缺乏統一的組織。
- **Euler 的雄心**：Euler 意識到，分析學需要一本「字典」——先定義函數、級數、指數、對數、三角函數，再談微積分。《Introductio》正是為他自己的《Institutiones calculi differentialis》（1755）與《Institutiones calculi integralis》（1768–70）鋪路的前置卷。

## 線索與推理 -- 數學式、程式、理論

### 線索一：現代「函數」概念的確立
《Introductio》開卷第一句就定義：**函數是由變數與常數以任意方式組成的解析表示式**。Euler 把函數分類為代數函數與超越函數（transcendental，即 $\sin$、$\cos$、$e^x$、$\log$ 等不能用有限次代數運算表示的函數），並主張：**超越函數應該用冪級數定義**。

這個觀點的革命性在於：函數不再依附幾何曲線，而是成為代數對象。$y = f(x)$ 從此是分析學的標準記號（記號 $f(x)$ 也是 Euler 在 1734 年引入的）。現代教科書中「函數、定義域、表示式」的框架，直接源於此書。

### 線索二：e 與 $e^x$ 的登場
Euler 用兩條路徑定義 $e$：

**路徑一（極限）**：複利的連續極限
$$e = \lim_{n \to \infty}\left(1 + \frac{1}{n}\right)^n \approx 2.71828\,18284\,59045$$
記號 $e$ 也是 Euler 引入的（1727 年手稿首次使用，1748 年出版）。

**路徑二（級數）**：
$$e = 1 + \frac{1}{1!} + \frac{1}{2!} + \frac{1}{3!} + \cdots$$

由此推廣到指數函數：
$$e^x = \lim_{n\to\infty}\left(1 + \frac{x}{n}\right)^n = 1 + x + \frac{x^2}{2!} + \frac{x^3}{3!} + \cdots$$

關鍵性質：$\dfrac{d}{dx}e^x = e^x$（唯一不變的函數）、$e^x e^y = e^{x+y}$、$e^x$ 是 $\ln x$ 的反函數。Euler 證明 $\ln x = \displaystyle\int_1^x \frac{dt}{t}$，從此對數有了積分表示，指數有了級數表示，兩者統一於 $e$。

### 線索三：三角函數的級數與 Euler 公式
Euler 在書中系統推出：

$$\sin x = x - \frac{x^3}{3!} + \frac{x^5}{5!} - \cdots, \qquad \cos x = 1 - \frac{x^2}{2!} + \frac{x^4}{4!} - \cdots$$

更深刻的是**Euler 公式**（1740 年代逐步形成，1748 年書中正式陳述）：比較 $e^{ix}$ 的級數與 $\cos x + i\sin x$ 的級數，逐項相同，故

$$e^{ix} = \cos x + i\sin x$$

取 $x = \pi$：

$$e^{i\pi} + 1 = 0$$

五個最重要的常數 $e, i, \pi, 1, 0$ 出現在同一條式子中。這條恆等式同時解決了 $\log(-1) = i\pi$ 的百年爭論——複對數的謎團結案。Euler 還據此推出著名的乘積公式：

$$\frac{\sin x}{x} = \prod_{n=1}^{\infty}\left(1 - \frac{x^2}{n^2\pi^2}\right)$$

由此輕鬆算出 Basel 問題（他 1735 年的成名作）：$\displaystyle\sum_{n=1}^\infty \frac{1}{n^2} = \frac{\pi^2}{6}$。

### 線索四：級數操作的黃金時代與隱患
Euler 對冪級數的操作大膽到近乎魯莽：逐項微分、逐項積分、無窮乘積、甚至發散級數的「求和」（他 1749 年處理 $1 - 1 + 1 - 1 + \cdots = \frac12$，是 Cesàro 求和的先聲）。這些操作大多正確，但缺乏收斂性論證——「形式操作」的信仰為 19 世紀的嚴格化運動埋下伏筆。Abel 1826 年的名言：「Euler 的發散級數操作產生了許多偉大的結果，但……」正是對這個時代的總結。

### 程式碼範例：$e$ 的級數收斂與 Euler 公式數值驗證
```python
import numpy as np
import matplotlib.pyplot as plt
from math import factorial

# 1) e 的級數部分和收斂
print("e 的級數部分和：")
partial = 0.0
errs = []
for n in range(0, 15):
    partial += 1 / factorial(n)
    err = abs(np.e - partial)
    errs.append(err)
    if n in (0, 2, 4, 6, 8, 10):
        print(f"  n={n:2d}, 部分和 = {partial:.12f}, 誤差 = {err:.2e}")

# 2) e^{i pi} + 1 = 0 的數值驗證（用級數計算 e^{iπ}，不借助 cmath.exp）
def exp_series(z, N=40):
    s = np.zeros_like(z, dtype=complex)
    term = np.ones_like(z, dtype=complex)
    for k in range(1, N + 1):
        term = term * z / k
        s += term
    return s

pi = np.pi
z = np.array([1j * pi])
val = exp_series(z)
print("\ne^{iπ} 的級數值 =", val[0])
print("e^{iπ} + 1 =", val[0] + 1, "（理論為 0）")

# 3) e^{ix} = cos x + i sin x 的逐點檢查
x = np.linspace(-2 * pi, 2 * pi, 200)
lhs = exp_series(1j * x)
rhs = np.cos(x) + 1j * np.sin(x)
print("max |e^{ix} - (cos x + i sin x)| =", np.max(np.abs(lhs - rhs)))

fig, ax = plt.subplots(1, 2, figsize=(11, 4))
ax[0].semilogy(range(15), errs, "o-")
ax[0].set_title("部分和誤差：e = Σ 1/n!")
ax[1].plot(x, lhs.real, label="Re e^{ix}")
ax[1].plot(x, np.cos(x), "k--", lw=0.8, label="cos x")
ax[1].legend(); ax[1].set_title("Euler 公式：e^{ix} = cos x + i sin x")
plt.show()
```

數值輸出顯示：$e$ 的級數誤差約以 $\dfrac{1}{(n+1)!}$ 的速度崩落；$e^{i\pi}+1$ 的級數值在小數點後十餘位為零；$e^{ix}$ 與 $\cos x + i\sin x$ 的最大偏差僅為浮點誤差等級——Euler 公式的三重驗證全部通過。

## 結案 -- 後果與影響
- **分析學的語言標準化**：函數、$f(x)$、$e$、$e^x$、$\ln$、$\sin x$ 級數、$\pi$ 的記號與用法，從此成為全歐洲（乃至全世界）教科書的標準。
- **複數的合法化**：Euler 公式讓 $i$ 從「形式符號」變成有幾何意義的對象（1806 年 Argand、Wessel 的複數平面是後續），為 Cauchy 的複分析鋪路。
- **超越函數的系統化**：$\Gamma$ 函數、Beta 函數、橢圓積分在 Euler 手中逐一誕生，特殊函數論的時代開啟。
- ** Basel 問題與 ζ 函數**：$\sum 1/n^2 = \pi^2/6$ 是 Riemann ζ 函數的先聲（1859），通往質數分佈與解析數論。
- **隱患的兌現**：Euler 式的形式操作在 19 世紀初製造了級數濫用的悖論，直接催生 Cauchy 的《Cours d'Analyse》（1821）與嚴格化運動。
- 影響至今：所有科學與工程教科書的數學語言，都是 1748 年這本書的直接後代。

## 關鍵人物與文獻
| 人物 | 角色 |
|---|---|
| Leonhard Euler | 1748 年《Introductio》，函數概念、$e$、Euler 公式 |
| John Bernoulli | Euler 的老師，指數與對數關係的釐清者 |
| Nicholas Mercator | 1668 年 $\ln(1+x)$ 級數 |
| Isaac Newton | 二項級數與超越函數的先驅 |
| Roger Cotes | 早期接近 $e^{ix}$ 形式的先驅（1714） |

- L. Euler, *Introductio in analysin infinitorum*, Lausanne (1748)。英譯：J. D. Blanton, *Introduction to Analysis of the Infinite*, Springer (1988, 1990)。
- E. Hairer & G. Wanner, *Analysis by Its History*, Springer (1996)。
