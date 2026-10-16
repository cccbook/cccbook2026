# 1941-Curry 組合邏輯

## 案件摘要

Haskell Curry 在 1941 年出版《A Formalization of Logic》（Harvard University Press），為這樁始於 1924 年的懸案畫下正式句點：他將 Schönfinkel 的先驅洞見與自己在 1930 年代發展的一系列論文，鎔鑄成一門完整的形式學科——組合邏輯（combinatory logic）。Curry 不只重建了系統，還發現了 bracket abstraction 演算法、固定點組合子理論，並在 1934 年就觀察到類型與證明之間的神秘相似性——這個觀察在 1980 年由 Howard 完成後，成為當代證明助理（Coq/Agda/Lean）的理論核心。

## 前因 -- 為什麼會有這個案子

- 1927 年，Curry 在 Princeton 研究微分方程時獨立發現了「消除變數」的想法，隨後得知 Schönfinkel 的論文已先行一步——他形容這是「令人沮喪的巧合」，但決定繼續深入。
- Curry 赴 Göttingen（1928-1930）追隨 Hilbert 學派，在 Behmann 指導下完成博士論文，將組合子想法發展為完整的形式系統。
- Schönfinkel 的先驅工作幾乎被遺忘：他本人因病退隱，論文僅此一篇，Curry 成為這門學科實際上的奠基者與命名者（combinatory logic 一詞由 Curry 提出）。
- 1930 年代系列論文：Curry 在《American Journal of Mathematics》連載 "Grundlagen der kombinatorischen Logik"，建立基底組合子、還原理論與一致性證明。
- 1935 年的打擊：Rosser（與 Kleene）證明 Curry 1930 年系統中的邏輯部分也蘊含矛盾——Curry 與 Church 面對同樣的難題，選擇了相似的退守策略。
- 案件動機：Curry 的哲學立場是「形式主義與建構主義的結合」——他相信邏輯應建立在最簡單、最可操作的原始概念上，而組合子正是這樣的積木。

## 線索與推理 -- 數學式、程式、理論

### 線索一：組合邏輯的形式系統

Curry 的系統以 $\mathbf{B}$、$\mathbf{C}$、$\mathbf{K}$、$\mathbf{W}$ 為基底（S 可由它們合成）：

$$
\begin{aligned}
\mathbf{B}\,f\,g\,x &= f\,(g\,x) \quad &\text{（合成）} \\
\mathbf{C}\,f\,x\,y &= f\,y\,x \quad &\text{（交換）} \\
\mathbf{K}\,x\,y &= x \quad &\text{（消去）} \\
\mathbf{W}\,f\,x &= f\,x\,x \quad &\text{（重複）} \\
\mathbf{S}\,x\,y\,z &= x\,z\,(y\,z)
\end{aligned}
$$

- Curry 證明 $\mathbf{S}\,\mathbf{K}$ 是完備基底，但 $\mathbf{B}\,\mathbf{C}\,\mathbf{K}\,\mathbf{W}$ 系統在翻譯 λ 項時產生更小、更可讀的組合子項。
- 還原（reduction）是唯一的推演規則；Curry 發展了還原的詞序理論（standardization）與一致性證明。

### 線索二：Curry 化（currying）

多元函數 = 單元函數的鏈：

$$f(x, y) = f(x)(y), \qquad f : A \times B \to C \;\cong\; f : A \to (B \to C)$$

$$\text{curry}(f) = \lambda x.\lambda y.\,f(x, y), \qquad \text{uncurry}(g) = \lambda p.\,g(\pi_1 p)(\pi_2 p)$$

歷史註記：這個技巧在 Schönfinkel 1924 年的論文中已經出現，因此更準確的名字應該是 Schönfinkeling；但 Curry 在 1958 年與 Feys 的專著中將其系統化，「currying」之名遂不脛而走。

```python
# Schönfinkeling vs Curry 化
def add(x, y):            # 多元函數
    return x + y

add_curried = lambda x: lambda y: add(x, y)   # 單元函數的鏈

assert add(3, 4) == add_curried(3)(4) == 7
assert add_curried(3)(4) == 7

# 偏應用（partial application）是 currying 的自然副產品
add3 = add_curried(3)
assert add3(10) == 13 and add3(100) == 13 + 100
print("currying 驗證通過")
```

### 線索三：bracket abstraction——λ 消除演算法

Curry 的關鍵貢獻：一個把任意 λ 項翻譯成組合子項的機械演算法。定義翻譯 $[x]M$（把變數 $x$ 從 $M$ 中抽象出來）：

$$
\begin{aligned}
[x]\,x &= \mathbf{I} \\
[x]\,M &= \mathbf{K}\,M \quad (x \notin FV(M)) \\
[x]\,M\,N &= \mathbf{S}\,([x]\,M)\,([x]\,N)
\end{aligned}
$$

性質：$([x]M)\,x = M$（對任何 $x$）。任何 $\lambda x. M = [x]M$。用 $\mathbf{B}$、$\mathbf{C}$ 可優化：

$$[x]\,M\,N = \mathbf{B}\,([x]\,M)\,N \;\;(x \notin FV(N)), \qquad [x]\,M\,N = \mathbf{C}\,M\,([x]\,N) \;\;(x \notin FV(M))$$

Python 實作 bracket abstraction：

```python
# λ 項轉組合子項（bracket abstraction）
# Lam("x", M) / App(M, N) / Var("x") / 原子組合子為字串
S, K, I = "S", "K", "I"

def App(f, a): return (f, a)
def Var(x):    return x
def Lam(x, m): return ("lam", x, m)

def abstract(x, m):
    "[x]M：把 x 從 M 中抽象出來"
    if m == x:
        return I                                  # [x]x = I
    if not occurs(x, m):
        return (K, m)                             # [x]M = K M
    if isinstance(m, tuple):
        f, a = m
        if isinstance(f, tuple):                  # M N 形式（f 是應用）
            return (S, (abstract(x, f), abstract(x, a)))
        # f 是原子（組合子或變數）
        if f == x:
            return (S, (I, abstract(x, a)))       # [x](x N) = S I [x]N
        return (S, ((K, f), abstract(x, a)))      # [x](c N) = S (K c) [x]N
    raise ValueError("unreachable")

def occurs(x, m):
    if m == x: return True
    if isinstance(m, tuple): return occurs(x, m[0]) or occurs(x, m[1])
    return False

def to_combinator(t):
    "把 λ 項整個翻譯成組合子項"
    if isinstance(t, tuple) and t[0] == "lam":
        return abstract(t[1], to_combinator(t[2]))
    if isinstance(t, tuple):
        return (to_combinator(t[0]), to_combinator(t[1]))
    return t

def show(t):
    if isinstance(t, tuple): return f"({show(t[0])} {show(t[1])})"
    return str(t)

# λx. x -> I
print(show(to_combinator(Lam("x", Var("x")))))              # 輸出: I

# λx. K x -> S (K K) I（未優化；可用 B、C 優化為 K）
print(show(to_combinator(Lam("x", (K, Var("x"))))))         # 輸出: (S ((K K) I))

# λx. x a -> S (I (K a))（即 C I a 的展開）
print(show(to_combinator(Lam("x", (Var("x"), "a")))))       # 輸出: (S (I (K a)))
```

### 線索四：組合邏輯與 λ-Calculus 的等價性

Curry 證明：兩個系統在表達力上等價——每個 λ 項都有對應的組合子項，且還原行為一致：

$$\llbracket \lambda x. M \rrbracket\,a = \llbracket M[x := a] \rrbracket$$

這個等價性有實際意義：λ-Calculus 好寫（人類友善），組合子好算（機器友善）——編譯器可以讓人類用 λ 寫程式、機器用組合子執行。

### 線索五：固定點組合子理論

Curry 系統化了一切組合子的不動點理論：對任何組合子 $Y$，若 $Y\,f = f\,(Y\,f)$，則 $Y$ 是固定點組合子。Curry 的 $\mathbf{Y}$ 是 Church 的 $Y \equiv \lambda f.\,(\lambda x.\,f\,(x\,x))(\lambda x.\,f\,(x\,x))$ 的組合子版本：

$$\mathbf{Y} = \mathbf{S}\,(\mathbf{K}\,(\mathbf{S}\,\mathbf{I}\,\mathbf{I}))\,(\mathbf{S}\,(\mathbf{S}\,(\mathbf{K}\,\mathbf{S})\,\mathbf{K})\,(\mathbf{K}\,(\mathbf{S}\,\mathbf{I}\,\mathbf{I})))$$

### 線索六：Curry-Howard 對應的「Curry」部分

- 1934 年，Curry 在論文中已觀察到：組合子的基底與 Hilbert 系統的公理模式之間存在形式相似性。
- 這個相似性在 1958 年《Combinatory Logic I》中被系統化：

$$
\mathbf{S}\,x\,y\,z = x\,z\,(y\,z) \;\leftrightarrow\; (A \to (B \to C)) \to ((A \to B) \to (A \to C)) \text{（公理模式）}
$$

$$
\mathbf{K}\,x\,y = x \;\leftrightarrow\; A \to (B \to A)
$$

- 完整的對應（「命題即類型，證明即程式」）在 1980 年由 William Howard 完成：直覺主義邏輯的證明 = 單純型 λ-Calculus 的項；蘊含消除 = 函數應用。這個對應後來被稱為 Curry-Howard 對應，成為 Coq、Agda、Lean 等證明助理的理論核心。

## 結案 -- 後果與影響

- 案件偵破：組合邏輯成為一門完整的形式學科，與 λ-Calculus 分庭抗禮、互相等價。
- 1958、1972 年：Curry 與 Feys、Hindley、Seldin 出版《Combinatory Logic》I、II 卷，集大成。
- Haskell 語言（1990 年命名）直接致敬 Haskell Curry——函數式編程史上以人名命名的語言。
- 1970-80 年代：David Turner 以組合子為基礎發展 SASL、KRC 與 Miranda 的編譯技術（G-machine、supercombinators），惰性函數式語言的編譯全部建立在組合子上。
- Curry-Howard 對應成為 proof assistants（Coq/Agda/Lean/Isabelle）的理論核心——「寫程式即寫證明」。
- 型別理論的系統化：Curry 對單純型組合邏輯的分析（1960s）與 Howard 的對應共同奠定現代型別系統。
- 組合子邏輯至今活躍：Binary Lambda Calculus、PLDI 中的編譯技術、以及作為程式語言理論教學的核心工具。

## 關鍵人物與文獻

- Haskell Curry（1900-1982）：組合邏輯的奠基者與命名者。
  - H. B. Curry, "A Formalization of Logic", Harvard University Press, 1941.
  - H. B. Curry, "Functionality in combinatory logic", Proceedings of the National Academy of Sciences, 20:584-590, 1934.
  - H. B. Curry, "Grundlagen der kombinatorischen Logik", American Journal of Mathematics, 52(2):509-536 與 52(3):789-834, 1930.
  - H. B. Curry & R. Feys, "Combinatory Logic, Volume I", North-Holland, 1958.
  - H. B. Curry, J. R. Hindley & J. P. Seldin, "Combinatory Logic, Volume II", North-Holland, 1972.
- Moses Schönfinkel（1889-1942）：先驅，currying 技巧的原始發現者。
- William Howard（1926-）：完成 Curry-Howard 對應。
  - W. A. Howard, "The formulae-as-types notion of construction", in "To H. B. Curry: Essays on Combinatory Logic, Lambda Calculus and Formalism", Academic Press, 1980.（1969 年手稿）
- J. Barkley Rosser（1907-1989）：證明 Curry 1930 系統的邏輯部分矛盾。
  - J. B. Rosser, "A mathematical logic without variables", Annals of Mathematics, 36(1):127-150, 1935.
- David Turner（1946-）：組合子編譯技術（G-machine）的發明者。
  - D. A. Turner, "A new implementation technique for applicative languages", Software: Practice and Experience, 9(1):31-49, 1979.
- 參考：J. Roger Hindley, "A History of Combinatory Logic: From Schönfinkel to the Present", College Publications, 2020.
