# 1666 — Newton 流數術

## 案件摘要
1665–1666 年大瘟疫期間，Newton 離開 Cambridge 回到故鄉 Woolsthorpe，在「奇蹟年」中把廣義二項式級數與 Wallis 的插值方法整合，發明「流數術」（method of fluxions）：把變量視為隨時間「流動」的量，其變化率稱為「流數」。他區分**正流數問題**（由流動量求流數，即微分）與**反流數問題**（由流數求流動量，即積分），並證明兩者互逆——微積分基本定理的雛形。1666 年的〈論流數〉（Tract on Fluxions）手稿是這場案件的完整筆錄。

## 前因 -- 為什麼會有這個案子
- 1665 年 Newton 已在 Wallis 的插值懸案上建立廣義二項式定理，並發現「級數逐項積分」是萬能求積引擎。
- 1655 年 Wallis 的 $\int_0^1 x^n dx = \frac{1}{n+1}$、1637 年 Fermat 的 adequality 切線法，兩件兇器分別對應積分與微分，但**沒有人把它們連成互逆關係**。
- Newton 的老師 Barrow 已在《幾何講義》(1670 出版) 中用幾何方式處理切線與面積的關係（Newton 親筆協助整理，講義中的 Lemma 暗藏基本定理的幾何原型）。
- 1665–1666 年 Cambridge 因瘟疫關校，Newton 在 Woolsthorpe 的兩年間還發現了廣義二項式、光譜分解與萬有引力的早期想法——流數術是這場「奇蹟年」的數學主案。
- 案件的動機：物理量（位置、速度）隨時間連續變化——需要一套語言同時描述「量」與「變化率」，並讓兩者可以互相推算。

## 線索與推理 -- 數學式、程式、理論

### 線索一：流數的語言
Newton 記號：$x = o$（流動量，用字母 $o$ 或 $p, q$），其流數記為 $\dot{o}$（字母上加點）。若 $x$、$y$ 都是時間 $t$ 的函數，則

$$\dot{x} = \frac{dx}{dt}, \qquad \dot{y} = \frac{dy}{dt}, \qquad \frac{\dot{y}}{\dot{x}} = \frac{dy}{dx}$$

對曲線 $y = f(x)$，切線斜率就是 $\frac{\dot{y}}{\dot{x}}$——Fermat 的 adequality 之謎在此被重新破譯：Newton 用「無窮小時間 $o$ 中的增量」取代 Fermat 的含糊 $E$，即

$$\frac{f(x + \dot{x}\,o) - f(x)}{\dot{x}\,o} \to f'(x)$$

### 線索二：正流數問題（微分）
求 $y = x^n$ 的流數：在無窮小時間 $o$ 內，$x \to x + \dot{x}o$，$y \to y + \dot{y}o$。代入 $y = x^n$ 展開（用廣義二項式級數，對任意指數都有效）：

$$y + \dot{y}o = (x + \dot{x}o)^n = x^n + n x^{n-1}\dot{x}o + \frac{n(n-1)}{2}x^{n-2}(\dot{x}o)^2 + \cdots$$

消去 $y = x^n$、除以 $o$、捨去含 $o$ 的高次項（Newton 稱之為「略去無窮小」）：

$$\dot{y} = n x^{n-1}\dot{x} \quad \Rightarrow \quad \frac{dy}{dx} = n x^{n-1}$$

冪法則誕生——而且因為有廣義二項式級數，這對**分數、負指數**同樣有效。

### 線索三：反流數問題（積分）與基本定理
反過來：已知流數 $\dot{y} = x^n\dot{x}$，求流動量 $y$。Newton 的答案是「面積的瞬時增長率」：

$$\frac{d}{dx}\int_0^x f(t)\,dt = f(x), \qquad \int_a^b f'(x)\,dx = f(b) - f(a)$$

這就是**微積分基本定理**：正流數與反流數互逆。Newton 在 1666 年手稿中明確寫出這一互逆關係（以幾何語言：面積的流數等於邊界縱坐標）。有了它，求積不再是 Cavalieri 式的個別巧技，而是「找反導數」的系統程序：$\int x^n dx = \frac{x^{n+1}}{n+1}$（Wallis 的公式成為定理的直接推論）。

### 線索四：從手稿到《原理》
1666 年的〈論流數〉手稿未出版；1669 年〈分析學〉、1671 年《流數術與無窮級數》（Method of Fluxions，1736 年才英譯出版）逐步展開。1687 年，在 Halley 的催促與資助下，Newton 出版《自然哲學的數學原理》（Principia Mathematica），用流數術證明橢圓軌道、萬有引力平方反比——全書雖以幾何語言包裝，核心卻是流數術。

### 程式碼範例：流數術數值微分與基本定理驗證
```python
import numpy as np

# (1) 正流數問題：冪法則 (dy/dx = n x^{n-1})，含分數/負指數
def fluxion_numeric(f, x0, o=1e-7):
    return (f(x0 + o) - f(x0 - o)) / (2 * o)

for n, x0 in [(2, 1.5), (3, 2.0), (0.5, 0.25), (-1, 4.0)]:
    f = lambda x, n=n: x**n
    num = fluxion_numeric(f, x0)
    exact = n * x0**(n-1)
    print(f"n={n}, x={x0}: 數值流數 {num:.8f}, 理論 {exact:.8f}")

# (2) 反流數問題：∫_0^b x^n dx = b^{n+1}/(n+1)（Wallis 公式 = 定理推論）
b = 2.0
x = np.linspace(0, b, 1000000)
for n in [1, 2, 3, 0.5]:
    V = np.trapz(x**n, x)
    print(f"n={n}: 數值積分 {V:.8f}, b^(n+1)/(n+1) = {b**(n+1)/(n+1):.8f}")

# (3) 微積分基本定理：d/dx ∫_0^x t^2 dt = x^2
F = lambda x: np.trapz(np.linspace(0, x, 1000)**2, np.linspace(0, x, 1000))
x0 = 3.0
num = fluxion_numeric(F, x0)
print(f"基本定理: d/dx ∫_0^{x0} t²dt ≈ {num:.6f}（理論 x² = {x0**2}）")
```

程式輸出：數值流數與 $nx^{n-1}$ 逐項吻合（含 $n = 0.5$、$n = -1$）；數值積分與 $\frac{b^{n+1}}{n+1}$ 一致（Wallis 公式重現）；面積函數的流數等於原函數 $x^2$——正/反流數互逆，基本定理在數值上成立。

## 結案 -- 後果與影響
- 微積分基本定理確立：微分與積分**互逆**，求積從個別巧技變成系統程序——這是 17 世紀數學最大的結案。
- 1687 年《原理》用流數術統一了天上與地上的力學：橢圓軌道、潮汐、擺的運動全部可算。
- 優先權之爭：1684 年 Leibniz 率先**出版**微積分（用 $dx$、$\int$ 記號），Newton 主張 1666 年手稿在先。Royal Society 1712 年的裁決偏袒 Newton，今日史家判定兩人獨立發明——Newton 在先，Leibniz 的記號（今日教科書所用）更優。
- 1736 年《流數術》英譯出版，19 世紀 Cauchy/Weierstrass 用極限語言補上 Newton「略去無窮小」的邏輯漏洞。
- Newton 自己的回顧（1714 年致 Des Maizeaux 的信）寫道：1665–1666 年間他「在兩年內比之前與之後的任何時間都更專注於數學與哲學」，並把廣義二項式、流數術、光譜與引力列為這段時期的發現——四案同時告破。

## 關鍵人物與文獻
| 人物 | 角色 |
|---|---|
| Isaac Newton | 流數術、微積分基本定理、《原理》 |
| Isaac Barrow | 《幾何講義》暗藏基本定理的幾何原型 |
| Gottfried W. Leibniz | 1684 率先出版微積分，記號勝出 |
| Edmond Halley | 催促與資助《原理》出版 |
| John Wallis | 插值方法的先驅 |

- I. Newton, *Tract on Fluxions*〈論流數〉(1666 手稿，未出版)。
- I. Newton, *De Analysi per Aequationes Numero Terminorum Infinitas* (1669)。
- I. Newton, *Philosophiæ Naturalis Principia Mathematica* (1687)。
- I. Newton, *Method of Fluxions* (寫於 1671，1736 出版)。
