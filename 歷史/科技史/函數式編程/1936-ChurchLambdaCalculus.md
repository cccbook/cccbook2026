# 1936-Church Lambda Calculus

## 案件摘要

1932 年，Princeton 的邏輯學家 Alonzo Church 發表 "A set of postulates for the foundation of logic"，企圖以「函數」而非集合為基礎重建整個邏輯。這個雄心勃勃的系統在 1935 年被他的學生 Kleene 與 Rosser 證明是矛盾的——偵探辦案中途發現證據自相矛盾。Church 於是壯士斷腕，退守到系統中純粹的函數部分，這部分不但無矛盾，還在 1936 年催生了 λ-Calculus 與不可判定性的證明。這個「失敗系統的殘骸」，後來成為所有現代程式語言型別系統與函數式編程的理論核心。

## 前因 -- 為什麼會有這個案子

- Hilbert 計畫正處於全盛期：目標是為全部數學找到一個一致且完備的形式系統，並以有限方法證明其一致性。
- Princeton 在 1930 年代聚集了 Church、Kleene、Rosser、Gödel（1933 年訪問）、Turing（1936 年抵達），成為與 Göttingen 分庭抗禮的邏輯重鎮。
- Church 的哲學立場：邏輯的基礎不該是集合論（Russell 悖論已重創它），而應該是「函數作為原始概念」——一個建構主義式的、以計算為導向的系統。
- 1932 年的原始系統包含 λ 定義、正整數理論與一組邏輯公設；Church 相信它能同時扮演邏輯基礎與計算系統。
- 案件的轉折：Kleene 與 Rosser 在 1935 年證明 Church 的原始系統（以及 Curry 的類似系統）蘊含矛盾——Richard 悖論的翻版在其中可被建構出來。

## 線索與推理 -- 數學式、程式、理論

### 線索一：λ-Calculus 的語法

純 λ-Calculus 只有三種語法構件：

$$
M ::= x \mid \lambda x.\,M \mid M\,N
$$

- $x$：變數；$\lambda x. M$：抽象（建立函數）；$M\,N$：應用（把 $N$ 餵給 $M$）。
- 應用左結合：$M\,N\,P = (M\,N)\,P$；λ 的管轄範圍向右延伸到盡頭。

### 線索二：三條改寫規則

α 變換（改名，不改變意義）：

$$\lambda x.\,M \equiv \lambda y.\,M[x := y] \quad (y \notin FV(M))$$

β 歸約（計算的核心）：

$$(\lambda x.\,M)\,N \;\to\; M[x := N]$$

η 變換（外延性）：

$$\lambda x.\,f\,x \;\equiv\; f \quad (x \notin FV(f))$$

自由變數 $FV(M)$ 與束縛變數的區分是整個系統的技術核心：β 歸約代入時必須避免變數捕獲，這正是 Schönfinkel 想用組合子繞過的麻煩。

### 線索三：Church-Rosser 定理——合流性

Church 與 Rosser 於 1936 年證明：若項 $M$ 可以歸約到 $N_1$ 也可以歸約到 $N_2$，則必存在 $N_3$ 使 $N_1 \to N_3$ 且 $N_2 \to N_3$：

$$
M \twoheadrightarrow N_1,\; M \twoheadrightarrow N_2 \;\Longrightarrow\; \exists N_3.\; N_1 \twoheadrightarrow N_3 \wedge N_2 \twoheadrightarrow N_3
$$

這個合流性（confluence）保證計算結果不依賴歸約順序——λ-Calculus 的「確定答案」性質，是它成為可靠計算模型的關鍵。

### 線索四：用純 λ 項編碼一切資料

Church 數字（自然數的 λ 編碼）：

$$
\begin{aligned}
0 &\equiv \lambda f.\lambda x.\,x \\
1 &\equiv \lambda f.\lambda x.\,f\,x \\
\mathrm{SUCC} &\equiv \lambda n.\lambda f.\lambda x.\,f\,(n\,f\,x) \\
\mathrm{ADD} &\equiv \lambda m.\lambda n.\lambda f.\lambda x.\,m\,f\,(n\,f\,x) \\
\mathrm{MUL} &\equiv \lambda m.\lambda n.\lambda f.\,m\,(n\,f)
\end{aligned}
$$

布林與配對：

$$\mathrm{TRUE} \equiv \lambda a.\lambda b.\,a \qquad \mathrm{FALSE} \equiv \lambda a.\lambda b.\,b \qquad \mathrm{PAIR} \equiv \lambda a.\lambda b.\lambda z.\,z\,a\,b$$

Y 組合子（遞迴的钥匙，代替被禁止的 self-reference）：

$$Y \equiv \lambda f.\,(\lambda x.\,f\,(x\,x))\,(\lambda x.\,f\,(x\,x)), \qquad Y\,f = f\,(Y\,f)$$

### 線索五：Python 驗證 Church 編碼

Python 的 closure 恰好就是 λ 抽象，可用來模擬整個系統：

```python
TRUE  = lambda a: lambda b: a
FALSE = lambda a: lambda b: b

ZERO  = lambda f: lambda x: x
SUCC  = lambda n: lambda f: lambda x: f(n(f)(x))
ADD   = lambda m: lambda n: lambda f: lambda x: m(f)(n(f)(x))
MUL   = lambda m: lambda n: lambda f: m(n(f))
POW   = lambda m: lambda n: n(m)          # m 的 n 次方

def to_int(n):  return n(lambda i: i + 1)(0)
def to_bool(b): return b(True)(False)

assert to_int(ZERO) == 0
assert to_int(SUCC(ZERO)) == 1
assert to_int(ADD(SUCC(ZERO))(SUCC(SUCC(ZERO)))) == 3

three = ADD(SUCC(ZERO))(ADD(SUCC(ZERO))(SUCC(ZERO)))
four  = SUCC(three)
assert to_int(MUL(three)(four)) == 12      # 3 x 4 = 12
assert to_int(POW(three)(SUCC(ZERO))) == 3

PAIR = lambda a: lambda b: lambda z: z(a)(b)
FST  = lambda p: p(TRUE)
SND  = lambda p: p(FALSE)
p = PAIR(three)(four)
assert to_int(FST(p)) == 3 and to_int(SND(p)) == 4
print("Church 數字/布林/配對驗證通過")
```

### 線索六：符號 β 歸約直譯器

```python
# 極簡 λ-Calculus 直譯器（不處理捕獲避免，示範用）
# Var("x") / Lam("x", M) / App(M, N)
def app(f, a): return (f, a)
def subst(t, x, v):
    if t == x:            return v
    if isinstance(t, str): return t
    if t[0] == "lam":
        name, body = t[1], t[2]
        return ("lam", name, subst(body, x, v)) if name != x else t
    f, a = t
    return (subst(f, x, v), subst(a, x, v))
def beta(t):
    if isinstance(t, tuple) and len(t) == 2:
        f, a = t
        if isinstance(f, tuple) and f[0] == "lam":
            return subst(f[2], f[1], a)     # (λx.M) N -> M[x:=N]
        return (beta(f), beta(a))
    return t
def eval_(t, n=50):
    for _ in range(n):
        s = beta(t)
        if s == t: return t
        t = s
    return t

# (λx. x) y -> y
print(eval_(app(("lam", "x", "x"), "y")))    # 輸出: y
# (λx. λy. x) a -> λy. a
print(eval_(app(("lam", "x", ("lam", "y", "x")), "a")))  # 輸出: ('lam', 'y', 'a')
```

## 結案 -- 後果與影響

- 案件偵破：Church 的原始邏輯系統雖然矛盾，但其中的純函數部分（λ-Calculus）是一致、可靠且表達力驚人的計算系統。
- 1936 年 Church 以 λ-可定義性證明判定問題（Entscheidungsproblem）不可解，同年 Turing 以圖靈機獨立證明同一結果（見另案）。
- 單純型 λ-Calculus（simply typed lambda calculus，Church 1940）成為所有現代型別系統的祖先：ML、Haskell、TypeScript、Rust 的型別理論都可追溯到它。
- 無型 λ-Calculus 成為 LISP（1958，McCarthy）與 Scheme 的理論核心；LISP 的 function 與 first-class function 概念直接來自 Church。
- Church-Rosser 合流性成為程式語言語義學與改寫系統（rewriting systems）的基礎定理。
- Y 組合子成為「遞迴不必依賴名字」的經典示範，在函數式編程文化中具有近乎傳奇的地位。

## 關鍵人物與文獻

- Alonzo Church（1903-1995）：λ-Calculus 之父，Princeton 邏輯學派核心。
  - A. Church, "A set of postulates for the foundation of logic", Annals of Mathematics, 33(2):346-366, 1932; 34(2):839-864, 1933.
  - A. Church, "An unsolvable problem of elementary number theory", American Journal of Mathematics, 58:345-363, 1936.
  - A. Church, "A formulation of the simple theory of types", Journal of Symbolic Logic, 5(2):56-68, 1940.
- Stephen Kleene（1909-1994）與 J. Barkley Rosser（1907-1989）：證明原始系統矛盾與 Church-Rosser 定理。
  - S. C. Kleene & J. B. Rosser, "The inconsistency of certain formal logics", Annals of Mathematics, 36(3):630-636, 1935.
  - A. Church & J. B. Rosser, "Some properties of conversion", Transactions of the American Mathematical Society, 39(3):472-482, 1936.
- Haskell Curry：同時期平行發展的組合邏輯系統也遭 Rosser 證明矛盾，但同樣倖存於函數部分。
- 參考：H. P. Barendregt, "The Lambda Calculus: Its Syntax and Semantics", North-Holland, 1984（權威專著）。
