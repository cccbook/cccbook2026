# 1970 - Matiyasevich 證明希爾伯特第十問題不可解

## 案件摘要
1900 年希爾伯特提出第十問題：是否存在演算法，判定任意丟番圖方程是否有整數解？七十年後，蘇聯 22 歲的青年 Matiyasevich 補上最後一塊拼圖，與 Davis、Putnam、Robinson 共同證明：**這樣的演算法不存在**。

## 前因 -- 為什麼會有這個案子

**丟番圖方程**（Diophantine equation）是只求整數解的多項式方程，源自古希臘數學家 Diophantus 的《算術》。例如：

$$x^2 + y^2 = z^2 \quad (\text{有無窮多解：勾股數})$$

$$x^n + y^n = z^n, \; n \geq 3 \quad (\text{費馬最後定理：無解})$$

1900 年，希爾伯特在巴黎演講中提出 23 個問題，第十問題最為樸素：

> 給定一個整係數多項式 $P(x_1, \ldots, x_n)$，設計一個「根據有限步運算即可判定」的程序，判定方程 $P(x_1, \ldots, x_n) = 0$ 是否有整數解。

當時沒有人想到「程序」這個概念需要嚴格定義。1936 年 Turing 定義了圖靈機與**停機問題**（halting problem）——證明存在不可判定的問題。這為第十問題的「不可解」結局埋下了伏筆：也許希爾伯特要的程序根本寫不出來。

## 線索與推理 -- 數學式、程式、理論

### 線索一：丟番圖集合與遞迴可列舉集合

**定義（丟番圖集合）**：集合 $S \subseteq \mathbb{Z}^n$ 稱為丟番圖的，若存在多項式 $P$ 使得

$$a \in S \iff \exists x_1, \ldots, x_m \in \mathbb{Z} : P(a, x_1, \ldots, x_m) = 0$$

**定義（遞迴可列舉集合）**：能被圖靈機「列出」所有元素的集合（即半可判定：屬於時可確認，不屬於時可能永遠跑不完）。

**MRDP 定理（1970，DPRM）**：

$$S \text{ 是丟番圖集合} \iff S \text{ 是遞迴可列舉集合}$$

這是一個驚人的字典：**計算機科學的可計算性 = 數論的多項式性**。

### 線索二：推理鏈——從停機問題到不可解

1. 停機問題不可判定：不存在演算法判定圖靈機是否停機。
2. 停機集合（會停機的機器的編碼）是遞迴可列舉但非遞迴的。
3. 由 MRDP 定理，存在丟番圖方程 $P_H(e, x_1, \ldots, x_m)$ 使得：

$$e \in \text{停機集合} \iff \exists x : P_H(e, x) = 0$$

4. 若存在判定丟番圖方程可解性的通用演算法，就能判定停機問題——矛盾。

**結案推論**：不存在通用演算法判定 $P(x_1, \ldots, x_n) = 0$ 是否有整數解。希爾伯特第十問題**不可解**。

### 線索三：Fibonacci 數列是丟番圖的（最後一塊拼圖）

Davis 與 Putnam 證明：只要「指數關係」$b = a^c$ 是丟番圖的，定理就成立。Julia Robinson 奮鬥二十年未竟。1970 年 Matiyasevich 用 **Pell 方程**補上了這一步：Fibonacci 數列 $F_n$ 的成長是丟番圖的。

關鍵在於 Pell 方程

$$x^2 - a y^2 = 1$$

的解 $x + y\sqrt{a} = (x_1 + y_1 \sqrt{a})^n$ **指數增長**，而 $F_n$ 恰可透過 $F_n \approx \varphi^n / \sqrt{5}$（$\varphi = \frac{1+\sqrt{5}}{2}$）嵌入這類關係。Matiyasevich 證明：

$$b = F_{2c} \; (c \geq 0) \text{ 是丟番圖關係}$$

從而 $b = a^c$ 可由丟番圖條件表達，MRDP 定理完成。

### Python 演示：Pell 方程 $x^2 - 2y^2 = 1$ 的指數級解增長

```python
def pell_solutions(D, count):
    """用連分數收斂子求 Pell 方程 x^2 - D*y^2 = 1 的前 count 個解"""
    a0 = int(D ** 0.5)
    m, d, a = 0, 1, a0
    x_prev, x = 1, a0      # x_n = a_n * x_{n-1} + x_{n-2}
    y_prev, y = 0, 1
    sols = []
    for _ in range(count):
        m = d * a - m
        d = (D - m * m) // d
        a = (a0 + m) // d
        x, x_prev = a * x + x_prev, x
        y, y_prev = a * y + y_prev, y
        if x * x - D * y * y == 1:
            sols.append((x, y))
    return sols

sols = pell_solutions(2, 30)
for x, y in sols[:6]:
    print(f"x={x}, y={y}, x 位數={len(str(x))}")

# 觀察：相鄰兩解的比值趨近 3+2*sqrt(2) ≈ 5.828（指數增長率）
if len(sols) >= 2:
    print("增長率:", sols[1][0] / sols[0][0], "≈ 3+2√2 =", 3 + 2 * 2 ** 0.5)
```

輸出顯示解以 $3 + 2\sqrt{2} \approx 5.828$ 的比率指數增長——正是這種「多項式方程中藏著指數行為」的現象，讓丟番圖方程能編碼任意計算。

## 結案 -- 後果與影響

- **希爾伯特第十問題宣告不可解**，成為 20 世紀繼哥德爾不完備定理、Turing 停機問題之後第三座「不可知」的里程碑。
- 開創了**丟番圖可計算性理論**：許多著名問題被證明等價於丟番圖方程可解性（如 Riemann 猜想的某些形式化版本）。
- 哲學意涵：整數的多項式世界，已經蘊含了計算機的一切能力與極限。
- Hilbert's tenth over $\mathbb{Q}$（有理數）至今仍是懸案；2016 年後 Koenigsmann 等證明 $\mathbb{Z}$ 在 $\mathbb{Q}$ 中是一階可定義的，使問題傾向不可解。

## 關鍵人物與文獻

| 人物 | 貢獻 |
|---|---|
| Martin Davis, Hilary Putnam | 1961 年證明「指數關係可表達時」定理成立 |
| Julia Robinson | 奠定丟番圖集合理論，奮鬥二十年 |
| Yuri Matiyasevich | 1970 年用 Pell/Fibonacci 補完最後一步（年僅 22 歲） |

**文獻**：
- Matiyasevich, Y. (1993). *Hilbert's Tenth Problem*. MIT Press.
- Davis, M., Matiyasevich, Y., Robinson, J. (1976). "Positive resolution of Hilbert's tenth problem" (MRDP 綜述).
