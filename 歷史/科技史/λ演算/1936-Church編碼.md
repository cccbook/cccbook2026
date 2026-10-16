# 1936 - Church 編碼：用函數寫出整個世界

## 案件摘要
在純粹的 λ 演算裡，沒有數字、沒有布林值、沒有資料結構、甚至沒有遞迴。
Church 編碼（Church Encoding）展示了驚人的偵探式推理：
只要用「函數」這一種原料，就能編碼出自然數、布林、配對與遞迴 ——
資料即函數，控制流即函數，一切都是函數。

## 前因 -- 為什麼會有這個案子
- 無類型 λ 演算的文法只有三條：$x \mid \lambda x.\, M \mid M\ N$，計算只有 β-歸約 $(\lambda x.\, M)\,N \to M\,[N/x]$。
- 問題：這麼貧瘠的系統，能表達「資料」嗎？能算術嗎？能遞迴嗎？（λ 演算中不能直接遞迴 —— $\lambda x.\, M$ 裡無法引用 $M$ 自己的名字。）
- Church、Kleene、Curry 等人在 1930 年代系統性構造出這些編碼，證明 λ 演算的表達力足以覆蓋全部原始遞迴函數（見〈1934 - Kleene λ 可定義函數〉一案）。
- 動機既有理論面（證明 Church 命題），也有實用面：Lisp（1958）的「一切皆串列」與函數式語言的「一切皆函數」都源於此。

## 線索與推理 -- 數學式、程式、理論

### 1. 自然數：Church 數字
自然數 $n$ 編碼為「把 $f$ 應用 $n$ 次到 $x$」：

$$
\bar{0} = \lambda f.\, \lambda x.\, x, \qquad
\bar{1} = \lambda f.\, \lambda x.\, f\ x, \qquad
\bar{2} = \lambda f.\, \lambda x.\, f\ (f\ x), \qquad
\bar{n} = \lambda f.\, \lambda x.\, f^n\ x
$$

**解碼**：$toInt(\bar{n}) = \bar{n}\ (\lambda y.\, y+1)\ 0 = n$。
**關鍵直覺**：數字本身就是迭代器 —— $\bar{n}$ 的語義就是「迭代 $n$ 次」。

### 2. 後繼與算術
$$
SUCC = \lambda n.\, \lambda f.\, \lambda x.\, f\ (n\ f\ x)
$$
$$
ADD = \lambda m.\, \lambda n.\, m\ SUCC\ n
\qquad\text{或}\qquad
ADD = \lambda m.\, \lambda n.\, \lambda f.\, \lambda x.\, m\ f\ (n\ f\ x)
$$
$$
MULT = \lambda m.\, \lambda n.\, \lambda f.\, m\ (n\ f)
$$

**推理**：
- $SUCC\ \bar{n}$：對 $x$ 迭代 $n$ 次後再套一層 $f$ → 迭代 $n+1$ 次。
- $ADD\ \bar{m}\ \bar{n}$：對 $\bar{n}$ 迭代 $m$ 次 $SUCC$。
- $MULT\ \bar{m}\ \bar{n}$：把「$n$ 次迭代」這件事本身再迭代 $m$ 次。

驗證：$MULT\ \bar{2}\ \bar{3} = \lambda f.\, \bar{2}\,(\bar{3}\,f) = \lambda f.\, (\bar{3}f) \circ (\bar{3}f)$，即 $f$ 複合 6 次 $= \bar{6}$ $\checkmark$

### 3. 布林值與條件
布林值編碼為「二選一的選擇器」：

$$
TRUE = \lambda a.\, \lambda b.\, a, \qquad FALSE = \lambda a.\, \lambda b.\, b
$$

條件（if）根本不用另外定義 —— 布林值本身就是 if：
$$
b\ X\ Y = \begin{cases} X & \text{若 } b = TRUE \\ Y & \text{若 } b = FALSE \end{cases}
$$

邏輯運算：
$$
AND = \lambda p.\, \lambda q.\, p\ q\ FALSE, \qquad
OR = \lambda p.\, \lambda q.\, p\ TRUE\ q, \qquad
NOT = \lambda p.\, p\ FALSE\ TRUE
$$

**測試**：$ISZERO$（判斷是否為零）巧妙地結合數字與布林：
$$
ISZERO = \lambda n.\, n\ (\lambda x.\, FALSE)\ TRUE
$$
若 $n = \bar{0}$，迭代 0 次，結果是 $TRUE$；否則每次迭代都把結果變成 $FALSE$。$\checkmark$

### 4. 配對（Pair）與選擇
配對 = 一個「帶著兩個值、等待被問要哪個」的函數：

$$
PAIR = \lambda a.\, \lambda b.\, \lambda s.\, s\ a\ b
$$
$$
FST = \lambda p.\, p\ TRUE, \qquad SND = \lambda p.\, p\ FALSE
$$

**測試**：
$$
FST\ (PAIR\ \bar{1}\ \bar{2}) = (PAIR\ \bar{1}\ \bar{2})\ TRUE = TRUE\ \bar{1}\ \bar{2} = \bar{1} \quad\checkmark
$$

有了配對，就能用「 $\bar{n} = (n, n-1)$ 配對串列」模擬鏈結串列（Lisp 的 cons/car/cdr 正是此法）。

### 5. Y 組合子：遞迴的解答
λ 演算中不能直接遞迴（函數體內無法引用自己）。Curry 提出的解法 —— **Y 組合子**：

$$
Y = \lambda g.\, (\lambda x.\, g\ (x\ x))\,(\lambda x.\, g\ (x\ x))
$$

**推理**：對任意 $g$，
$$
\begin{aligned}
Y\ g &\to_\beta (\lambda x.\, g\ (x\ x))\,(\lambda x.\, g\ (x\ x)) \\
&\to_\beta g\ ((\lambda x.\, g\ (x\ x))\,(\lambda x.\, g\ (x\ x))) \\
&= g\ (Y\ g)
\end{aligned}
$$

即 $Y\ g = g\ (Y\ g)$ —— **不動點方程式**：$Y$ 能為任何函數 $g$ 找到不動點 $Y\,g$。遞迴函數 $f$ 滿足 $f = F\ f$（$F$ 是「f 的一步」），所以 $f = Y\,F$。

以階乘為例：定義「一步」
$$
F = \lambda self.\, \lambda n.\, ISZERO\ n\ \bar{1}\ (MULT\ n\ (self\ (PRED\ n)))
$$
則
$$
FACTORIAL = Y\ F
$$
$$
FACTORIAL\ \bar{3} = Y\ F\ \bar{3} \to F\ (Y\ F)\ \bar{3} \to MULT\ \bar{3}\ (FACTORIAL\ \bar{2}) \to \cdots \to \bar{6} \quad\checkmark
$$

### 6. Python 驗證程式碼（closure 實作 Church numeral 並測試）
```python
# ---------- Church 數字 ----------
def N(n):                              # n ↦ λf.λx. f^n x
    return lambda f: lambda x: (
        x if n == 0 else
        (lambda acc: (lambda _f: _f) (None) and None or acc)(None) if False else
        f(N(n - 1)(f)(x))
    )
# 上面寫法易讀性差，改用更清晰的 closure 遞迴版：

def N(n):
    def _num(f):
        def _app(x, _n=n):
            result = x
            for _ in range(_n):
                result = f(result)
            return result
        return _app
    return _num
# 這是「迭代 n 次」的語義版，等價於 λf.λx. f^n x

SUCC = lambda n: lambda f: lambda x: f(n(f)(x))
ADD  = lambda m: lambda n: lambda f: lambda x: m(f)(n(f)(x))
MULT = lambda m: lambda n: lambda f: m(n(f))

def to_int(c):
    return c(lambda y: y + 1)(0)

# ---------- 布林 ----------
TRUE  = lambda a: lambda b: a
FALSE = lambda a: lambda b: b
NOT   = lambda p: p(FALSE)(TRUE)
AND   = lambda p: lambda q: p(q)(FALSE)
OR    = lambda p: lambda q: p(TRUE)(q)
ISZERO = lambda n: n(lambda x: FALSE)(TRUE)

# ---------- 配對 ----------
PAIR = lambda a: lambda b: lambda s: s(a)(b)
FST  = lambda p: p(TRUE)
SND  = lambda p: p(FALSE)

# ---------- Y 組合子與遞迴 ----------
def Y(g):                              # Y = λg.(λx.g(x x))(λx.g(x x))
    return (lambda x: g(lambda v: x(x)(v)))(
           (lambda x: g(lambda v: x(x)(v))))
# （用 η-展開 lambda v: x(x)(v) 避免Python立即求值造成的無限迴圈）

PRED = lambda n: lambda f: lambda x: (
    FST(n(lambda p: PAIR(SND(p))(SUCC(SND(p))))(PAIR(x)(x)))
)

FACT = Y(lambda self: lambda n:
         ISZERO(n)(N(1))(MULT(n)(self(PRED(n)))))

# ---------- 測試 ----------
assert to_int(N(0)) == 0 and to_int(N(5)) == 5
assert to_int(SUCC(N(4))) == 5
assert to_int(ADD(N(2))(N(3))) == 5
assert to_int(MULT(N(2))(N(3))) == 6
assert ISZERO(N(0)) is TRUE and ISZERO(N(1)) is FALSE
assert AND(TRUE)(FALSE) is FALSE and OR(TRUE)(FALSE) is TRUE
assert to_int(FST(PAIR(N(1))(N(2)))) == 1
assert to_int(SND(PAIR(N(1))(N(2)))) == 2
assert to_int(FACT(N(5))) == 120

print("Church 編碼全部測試通過：N/SUCC/ADD/MULT/BOOL/PAIR/Y/FACT ✓")
```

## 結案 -- 後果與影響
- Church 編碼證明了 λ 演算的表達力：**資料、控制流、遞迴，全可用純函數構造** —— 為 1936 年可計算性理論提供完整證據鏈。
- Church 數字與 Y 組合子成為電腦科學的經典教材：Y 組合子被稱為「電腦科學最美的發現之一」，是 Lisp、Scheme 中 `letrec`/`define` 遞迴的理論基礎。
- 「資料即函數」的思想影響深遠：Haskell 的代數資料型別與 continuation、JavaScript 的一級函數與 callback、乃至物件導向中「物件 = 帶狀態的分派函數」的實作，都是 Church 編碼的精神後裔。
- 實務註記：真實程式語言通常不用 Church 編碼（效率低），但它證明了一個深刻的結案陳詞：**函數是唯一的原子，卻足以建構整個計算世界。**

## 關鍵人物與文獻
- **Alonzo Church**：Church 數字的提出者。
- **Stephen C. Kleene**：算術的 λ 定義（SUCC/ADD/MULT）。
- **Haskell B. Curry**：Y 組合子的提出者（故又稱 Curry 的 paradoxical combinator）。
- A. Church, *The Calculi of Lambda-Conversion*, Princeton University Press (1941)。
- A. Church, *An unsolvable problem of elementary number theory*, American Journal of Mathematics 58 (1936)。
- H. B. Curry & R. Feys, *Combinatory Logic*, Vol. I (1958)。
- H. P. Barendregt, *The Lambda Calculus: Its Syntax and Semantics* (1984)：Church 編碼的標準參考。
