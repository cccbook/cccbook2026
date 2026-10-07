# 1924-Schönfinkel 組合子邏輯

## 案件摘要

1924 年 12 月 7 日，蘇聯數學家 Moses Schönfinkel 在 Göttingen 數學學會發表演講，提出一個驚人的主張：整個數學邏輯可以只靠少數幾個「組合子」（combinators）建立起來，完全不需要變數。這場演講的論文 "Über die Bausteine der mathematischen Logik"（論數理邏輯的積木）因 Schönfinkel 返回蘇聯、健康與精神狀況惡化，遲至 1927 年才由 Heinrich Behmann 代為整理發表。這是史上第一次有人系統性地「消除變數」，為函數式編程埋下第一塊基石。

## 前因 -- 為什麼會有這個案子

- Frege（1879《概念文字》）與 Russell（1910-13《數學原理》）的邏輯系統雖然強大，但處處依賴「束縛變數」（bound variables）與量詞，符號操作極為繁瑣，證明往往冗長難以機械化。
- 變數帶來的技術麻煩：代入（substitution）時要處理變數捕獲、改名等各種邊界情況，形式系統的推演規則因此複雜。
- Hilbert 學派（Göttingen）正追求「元數學」計畫：希望邏輯系統的證明能像算術一樣被機械化檢驗，因此渴望更簡潔、更「可操作」的邏輯基礎。
- Schönfinkel 腦中的關鍵洞見：既然函數終究可以化約成單一參數的形式，那麼「變數」其實只是函數應用的配角，或許可以整個去掉。
- 他自問：「若我成功消除變數，整個 Fregian 系統的推演將大幅簡化。」這就是本案的偵探動機。

## 線索與推理 -- 數學式、程式、理論

### 線索一：函數的「化約」——多元函數變單元函數

Schönfinkel 觀察到，一個宣稱吃兩個參數的函數 $f(x, y)$，其實可以改寫為吃一個參數、回傳一個新函數：

$$f(x, y) \quad\Longrightarrow\quad (f(x))(y)$$

這個技巧後來被稱為 currying（雖然更公平的名字應該是 Schönfinkeling）。它使得「函數應用」永遠只有一種形式：把一個東西交給另一個東西。

### 線索二：兩個基本積木——S 與 K

Schönfinkel 定義了兩個原始組合子，並宣稱它們足以表達一切：

$$\mathbf{S}\,x\,y\,z = x\,z\,(y\,z)$$

$$\mathbf{K}\,x\,y = x$$

- $\mathbf{K}$ 的作用是「製造常數」：給它一個 $x$，它回傳一個永遠吐出 $x$ 的函數——它一手取代了變數代入中最基本的「保留」操作。
- $\mathbf{S}$ 的作用是「分配」：它把 $z$ 同時餵給 $x$ 與 $y$，再組合結果——它取代了「共享同一變數」的操作。
- 保留（K）+ 分享（S）正是代入規則所需的全部要素，因此任何含變數的運算式都能被翻譯成只用 S、K 的運算式。

### 線索三：消除束縛變數的證明

任何 $\lambda$ 項 $\lambda x. M$ 都可以遞迴地翻譯成組合子項（此演算法後來由 Curry 發展為 bracket abstraction）：

$$
\begin{aligned}
\llbracket \lambda x. x \rrbracket &= \mathbf{S}\,\mathbf{K}\,\mathbf{K} \\
\llbracket \lambda x. M \rrbracket &= \mathbf{K}\,\llbracket M \rrbracket \quad (x \notin FV(M)) \\
\llbracket \lambda x. M\,N \rrbracket &= \mathbf{S}\,\llbracket \lambda x. M \rrbracket\,\llbracket \lambda x. N \rrbracket
\end{aligned}
$$

這就是破案時刻：變數被證明是多餘的。整個邏輯只需要 $\mathbf{S}$、$\mathbf{K}$ 兩個「積木」。

### 線索四：布林值也能變成組合子

- 定義 $\mathbf{TRUE} = \mathbf{K}$（$\mathbf{K}\,x\,y = x$，總是選第一個參數）
- 定義 $\mathbf{FALSE} = \mathbf{K}\,\mathbf{I}$（$\mathbf{K}\,\mathbf{I}\,x\,y = \mathbf{I}\,y = y$，總是選第二個參數）；等價地也可用 $\mathbf{S}\,\mathbf{K}$ 的組合表達。Schönfinkel 在論文中展示了布林值如何以組合子編碼，使邏輯連接詞也能化約為積木運算。

Python 驗證如下：

```python
S = lambda x: lambda y: lambda z: x(z)(y(z))
K = lambda x: lambda y: x

TRUE = K
FALSE = K(I)          # Schönfinkel 的 FALSE（K I x y = y）

I = S(K)(K)           # 恆等函數: I x = x
assert I(42) == 42

def to_bool(c):       # 把組合子布林轉回 Python bool
    return c(True)(False)

assert to_bool(TRUE) is True
assert to_bool(FALSE) is False

# KI 也等於 FALSE: (K I) x y = I y = y
assert to_bool(K(I)) is False

# 邏輯運算
AND = lambda p: lambda q: p(q)(FALSE)
OR  = lambda p: lambda q: p(TRUE)(q)
NOT = lambda p: p(FALSE)(TRUE)

assert to_bool(AND(TRUE)(TRUE)) is True
assert to_bool(OR(FALSE)(TRUE)) is True
assert to_bool(NOT(TRUE)) is False
print("S/K 組合子布林邏輯驗證通過")
```

### 線索五：還原（reduction）的機械性

組合子邏輯的推演只有一種規則：把 $\mathbf{S}$、$\mathbf{K}$ 的定義當成改寫規則反覆套用。這使得證明檢驗變成純機械操作，正合 Hilbert 學派的胃口。

```python
# SKI 還原示範（符號項，非 Python closure）
# 項的表示: 字串 = 原子, (f, a) = 應用 f a
S, K = "S", "K"

def app(f, a): return (f, a)

def rebuild(head, args):
    "把 head 與參數串回應用鏈"
    t = head
    for a in args:
        t = (t, a)
    return t

def chain_of(t):
    "把應用鏈 (f a b ...) 攤平成 [f, a, b, ...]"
    chain = []
    while isinstance(t, tuple):
        chain.append(t[1]); t = t[0]
    chain.append(t); chain.reverse()
    return chain

def norm(t):
    "遞迴還原至常態形"
    if not isinstance(t, tuple):
        return t
    c = [norm(x) for x in chain_of(t)]
    head, args = c[0], c[1:]
    # K x y -> x
    if head == K and len(args) >= 2:
        return norm(rebuild(args[0], args[2:]))
    # S x y z -> x z (y z)
    if head == S and len(args) >= 3:
        x, y, z, rest = args[0], args[1], args[2], args[3:]
        return norm(rebuild((x, z), [(y, z)] + rest))
    return rebuild(head, args)

# 驗證 1：I = S K K，(S K K) a -> a
print(norm(app(app(app(S, K), K), "a")))        # 輸出: a

# 驗證 2：B = S (K S) K，B f g x -> f (g x)
B = app(app(S, app(K, S)), K)
t = app(app(app(B, "f"), "g"), "x")
print(norm(t))                                   # 輸出: (f, (g, x))
```

## 結案 -- 後果與影響

- 案件偵破：變數不是邏輯的必需品，$\mathbf{S}$ 與 $\mathbf{K}$ 兩個組合子即可建構整個邏輯系統。
- Haskell Curry 於 1927 年在 Princeton 獨立發現了同樣的想法（看到 Schönfinkel 論文後大為震撼，赴 Göttingen 追隨 Hilbert 與 Behmann 深入研究），1930 年代將組合邏輯發展成完整的形式系統。
- Curry 發現了 $\mathbf{B}$、$\mathbf{C}$、$\mathbf{W}$ 等更多組合子，並證明 $\mathbf{S}$、$\mathbf{K}$ 是完備基底。
- 組合子成為函數式語言編譯器的中間表示：1970-80 年代 Turner 的 G-machine、supercombinators 都直接繼承這條血脈。
- 悲劇結尾：Schönfinkel 本人在 1927 年論文發表時已因精神疾病住院，1929 年返回蘇聯後窮困潦倒，1942 年死於莫斯科街頭。先驅的名字差點被歷史遺忘。

## 關鍵人物與文獻

- Moses Schönfinkel（1889-1942）：組合子邏輯的創始者，一生只留下這一篇關鍵論文。
  - M. Schönfinkel, "Über die Bausteine der mathematischen Logik", Mathematische Annalen, 92:305-316, 1924（演講）；由 H. Behmann 代為發表於 1927 年版。英譯收錄於 "From Frege to Gödel: A Source Book in Mathematical Logic, 1879-1931"（Harvard University Press, 1967, ed. Jean van Heijenoort）。
- Heinrich Behmann（1891-1970）：Göttingen 數學家，代 Schönfinkel 整理並發表論文。
- Haskell Curry（1900-1982）：獨立發現組合子，將其發展為完整學科。
  - H. B. Curry, "Grundlagen der kombinatorischen Logik", American Journal of Mathematics, 52(2):509-536 與 52(3):789-834, 1930.
- David Hilbert（1862-1943）：Hilbert 計畫的提出者，Göttingen 學派的核心。
- 參考：J. Roger Hindley, "A History of Combinatory Logic: From Schönfinkel to the Present", College Publications, 2020（歷史整理）。
