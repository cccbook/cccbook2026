# 1960 — Robinson 非標準分析

## 案件摘要
1960 年代初，耶魯大學的數理邏輯學家 Abraham Robinson 做出一件「不可能的任務」：用模型論（超濾與超積）嚴格地構造出包含無窮小 $\varepsilon$ 的數系——超實數域 $^*\mathbb{R}$，並證明它與標準分析在初階命題上完全等價。Leibniz 三百年前被 Berkeley 主教罵為「已死量的幽靈」的無窮小，正式獲得平反：它不是幽靈，而是一個邏輯上無懈可擊的實體。

## 前因 -- 為什麼會有這個案子
- **Leibniz 的無窮小**：十七世紀 Leibniz 用「$dx$、$dy$ 是無窮小，商 $\frac{dy}{dx}$ 是有限比值」的直覺發展微積分，導數、積分記號沿用至今。但 1734 年 Berkeley 在《The Analyst》抨擊：無窮小既非零又非有限，$\frac{dx}{dy}$ 等於「用消失的量的幽靈相除」——邏輯上說不過去。
- **Weierstrass 的 $\varepsilon$-$\delta$**：十九世紀中葉，Cauchy 與 Weierstrass 用 $\varepsilon$-$\delta$ 語言嚴格化極限，把無窮小從分析中驅逐出境：導數定義為 $f'(x) = \lim_{h\to 0}\frac{f(x+h)-f(x)}{h}$，「極限」是邏輯量詞的組合，不再需要任何「無窮小實體」。標準分析就此定於一尊。
- **代價**：$\varepsilon$-$\delta$ 嚴格但抽象難懂，幾代學生苦於「為什麼 $\frac{dy}{dx}$ 的記號這麼直覺、定義卻這麼繞？」。Leibniz 的直覺被犧牲了——直到有人能用邏輯替它伸冤。
- **模型論成熟**：1950 年代，Tarski 的模型論、Łoś 的超積定理問世，邏輯學家手裡有了一副新工具：可以「放大」一個數學結構而不改變它的真命題。

## 線索與推理 -- 數學式、程式、理論

### 線索一：超積——把實數線「放大」
Robinson 的構造核心是 Łoś 定理（1955）：取指標集 $I = \mathbb{N}$，對每個 $n$ 取一份 $\mathbb{R}$，再取一個非主超濾 $\mathcal{U}$（包含所有餘有限集、對交集與補集封閉的「投票委員會」），定義超積

$$^*\mathbb{R} = \mathbb{R}^{\mathbb{N}} / \mathcal{U}$$

兩個序列 $(a_n)$、$(b_n)$ 「相等」若且唯若 $\{n : a_n = b_n\} \in \mathcal{U}$（委員會過半數同意）。$^*\mathbb{R}$ 是一個**真正的有序體**：加減乘除、序關係全部繼承。

### 線索二：無窮小的嚴格身份
在 $^*\mathbb{R}$ 中，序列 $(1, 1/2, 1/3, \dots)$ 的等價類 $\varepsilon$ 滿足：對每個標準正實數 $r$，$\{n : 1/n < r\}$ 是餘有限集，故屬於 $\mathcal{U}$，於是

$$0 < \varepsilon < r \quad \text{對所有標準 } r > 0$$

$\varepsilon$ 是一個**比任何標準正實數都小、卻不是零**的元素——無窮小有了嚴格定義。它的倒數 $\omega = 1/\varepsilon$ 是無窮大。 Robinson 證明關鍵的**轉移原理**（Transfer Principle）：任何一階命題在 $\mathbb{R}$ 為真，若且唯若其 $^*$-版本在 $^*\mathbb{R}$ 為真。兩個世界邏輯等價——這是整樁案件的判決書。

### 線索三：Leibniz 直覺的平反
在非標準分析中，導數回到 Leibniz 的寫法：

$$f'(x) = \text{st}\left(\frac{f(x+\varepsilon) - f(x)}{\varepsilon}\right)$$

其中 $\text{st}(\cdot)$ 是「標準部分」映射（把有限超實映回最接近的標準實數）。商 $\frac{f(x+\varepsilon)-f(x)}{\varepsilon}$ 是真實的除法，最後取標準部分——不再是「幽靈相除」，而是先算一個貨真價實的商。例如 $\sqrt{x}$ 的導數：

$$\frac{\sqrt{x+\varepsilon}-\sqrt{x}}{\varepsilon} = \frac{1}{\sqrt{x+\varepsilon}+\sqrt{x}} \approx \frac{1}{2\sqrt{x}} \quad\Longrightarrow\quad (\sqrt{x})' = \text{st}(\cdot) = \frac{1}{2\sqrt{x}}$$

有理化消去 $\varepsilon$、直接讀出答案——十七世紀的算法直覺，用二十世紀的邏輯嚴格重演。

### 線索四：超實數的浮點類比
無窮小其實有個工程界的老熟人：**浮點數的機器精度**。IEEE 754 雙精度浮點的相對誤差 $\varepsilon_{\text{mach}} = 2^{-52} \approx 2.2\times 10^{-16}$——任何可表示數 $x$ 與其「後繼」之間，標準實數的世界「塌縮」了：在浮點世界裡，$x + \delta$ 與 $x$ 無法區分，只要 $|\delta| < \varepsilon_{\text{mach}}\,|x|$。這正是非標準分析中「$\varepsilon$ 層級」的離散版：浮點線是一條「非均勻離散的實數線」，每個尺度上有自己的「無窮小」。Robinson 的 $^*\mathbb{R}$ 可以視為把這個現象用邏輯推到極致——所有尺度上的無窮小同時存在。

### 程式碼範例：超實數的浮點類比與 dual 式演示
```python
from fractions import Fraction

class HyperLite:
    """超實數的『序列等價類』玩具版：用有理數序列 + 顯式比較規則"""
    def __init__(self, seq): self.seq = seq
    def __lt__(self, other):
        # Łoś 式比較：若 self.seq[n] < other.seq[n] 對『所有足夠大的 n』成立則真
        n0 = 0
        for n, (a, b) in enumerate(zip(self.seq, other.seq)):
            if a >= b: n0 = n + 1
        return all(a < b for a, b in zip(self.seq[n0:], other.seq[n0:]))
    def st(self):
        # 標準部分：有限超實 -> 收斂到的標準實數（此處取極限的有限近似）
        return sum(self.seq[:1000]) / 1000

eps = HyperLite([Fraction(1, n) for n in range(1, 10001)])   # 無窮小 ε
one = HyperLite([1] * 10000)                                  # 標準 1
print("0 < ε < 1 ?  ", HyperLite([0]*10000) < eps and eps < one)  # True
print("ε 的標準部分 st(ε) ≈", float(eps.st()))                    # ≈ 0.0

# 浮點類比：機器精度內的「無窮小」
import numpy as np
x = 1.0
delta = 1e-18            # < 2^-52 ≈ 2.2e-16
print("1.0 + 1e-18 == 1.0 ?", x + delta == x)   # True：浮點世界的 ε
```

玩具版顯示 $\varepsilon$ 介於 0 與所有標準正數之間且標準部分為 0——「幽靈」被邏輯逮住了；浮點類比則顯示工程計算早就在無意識地使用「無窮小層級」。

## 結案 -- 後果與影響
- **無窮小的現代重生**：1966 年 Robinson 出版《Non-standard Analysis》，非標準分析成為一門正式學科，應用於泛函分析、機率論（Loeb 測度, 1975）、數理經濟學（無窮多經濟主體的競爭均衡）。
- **Leibniz 直覺平反**：Berkeley 對無窮小的批判得到回應——問題不在無窮小本身，而在十七世紀缺乏模型論工具。史學家重新評價 Leibniz：他的記號與直覺自始自洽。
- **教學應用**：1976 年 Keisler 出版《Elementary Calculus: An Infinitesimal Approach》，用非標準分析教微積分，$\frac{dy}{dx}$ 直接是無窮小的商，許多學生覺得比 $\varepsilon$-$\delta$ 直觀。
- **建設性版本**：2000 年代，不用邏輯的「簡化版」非標準分析（如 Nelson 的 IST 內集合論）與 Dales–Woodin 的超實體系，讓無窮小走進更廣的數學世界。

## 關鍵人物與文獻
| 人物 | 角色 |
|---|---|
| Abraham Robinson | 非標準分析創始人，轉移原理證明者 |
| Jerzy Łoś | 超積定理（1955），構造的技術核心 |
| Alfred Tarski | 模型論奠基者，Robinson 的導師輩 |
| Gottfried Leibniz | 無窮小直覺的原創者，三百年後獲平反 |
| H. Jerome Keisler | 非標準分析教材，教學推廣者 |

- A. Robinson, "Non-standard analysis", Nederl. Akad. Wetensch. Proc. **64** (1961)。
- A. Robinson, *Non-standard Analysis*, North-Holland (1966)。
- H. J. Keisler, *Elementary Calculus: An Infinitesimal Approach* (1976)。
