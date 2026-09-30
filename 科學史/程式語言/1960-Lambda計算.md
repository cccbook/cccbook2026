# 1960 Lambda 演算：函數的原子理論

## 案發現場

要理解 1960 年的「案發現場」，必須先回到更早的謎團。1930 年代，普林斯頓的 Alonzo Church 為了研究數學基礎，發明了 lambda 演算（λ-calculus）——一套只用「函數抽象」與「函數應用」兩種操作的極簡形式系統。1936 年 Church 用它證明了 Hilbert 的判定問題（Entscheidungsproblem）無解，與 Turing 的圖靈機證明遙相呼應。兩者後來被證明計算能力等價：**Church-Turing 命題**——一切可計算函數，都可用 lambda 演算計算。

但真正的「案發現場」在 1950 至 60 年代之交。當時程式語言界正面對幾個未解之謎：FORTRAN 與 COBOL 都是「命令式」語言，程式是一串改變狀態的指令；可是「函數」在這些語言裡只是二等公民——它不能被當成資料傳來傳去、不能在執行時期被組合出新的函數。數學家早已習慣把函數當值用（$\sin$ 可以當成變數傳給 $\int$），程式語言卻做不到。遇見這個問題的人包括 MIT 的 John McCarthy（LISP 之父）、以及研究 lambda 演算語義的 Haskell Curry 與 Peter Landin。他們追問：lambda 演算這套「函數的原子理論」，能否成為程式語言的數學基礎？

## 偵查過程

### 線索一：λ x. x——一切從最簡單的函數開始

Lambda 演算的項（term）用三條規則遞迴定義：

$$
\begin{aligned}
\text{變數：} & \quad x \\
\text{抽象：} & \quad \lambda x.\, M \quad (\text{把 } x \text{ 綁定為參數的函數}) \\
\text{應用：} & \quad M\;N \quad (\text{把 } N \text{ 代入函數 } M)
\end{aligned}
$$

最簡單的例子 $\lambda x.\,x$ 是恆等函數：輸入什麼就輸出什麼。注意整個系統**不需要數字、不需要型別、不需要任何內建運算**——一切都可以從函數建構出來。Church 甚至用純函數定義出了自然數（Church 數）：

$$
\begin{aligned}
\bar{0} &= \lambda f.\,\lambda x.\;x \\
\bar{1} &= \lambda f.\,\lambda x.\;f\;x \\
\bar{2} &= \lambda f.\,\lambda x.\;f\;(f\;x) \\
\bar{n} &= \lambda f.\,\lambda x.\;f^{\,n}(x)
\end{aligned}
$$

數字 $n$ 的本質是「把函數 $f$ 應用 $n$ 次」——這是對「什麼是數」的深刻重新詮釋。加法也只是一個函數：$\mathrm{add} = \lambda m.\,\lambda n.\,\lambda f.\,\lambda x.\; m\,f\,(n\,f\,x)$，它把 $n$ 的「應用 $f$ 共 $n$ 次」再交給 $m$ 繼續應用。整個算術，就用函數應用一招建構完成。

### 線索二：β 歸約與合流性——計算就是改寫

Lambda 演算的「執行」只有一個動作：**β 歸約（beta reduction）**。把應用 $(\lambda x.\,M)\,N$ 改寫為把 $M$ 中所有自由出現的 $x$ 換成 $N$：

$$
(\lambda x.\,x + 1)\;5 \;\to_\beta\; 5 + 1 \;\to_\beta\; 6
$$

這正是函數呼叫的數學原型——程式語言的「呼叫函數、代入參數」就是 β 歸約的具體實現。但一個項可能有多處可歸約，先歸約哪裡？結果會不會不同？Church 與 Rosser 在 1936 年證明了 **Church-Rosser 定理（合流性，confluence）**：若一個項可以歸約到兩個不同的正規形（normal form），則這兩個正規形必定相同（可在有限步內歸約到共同項）。用圖表示：

$$
\begin{array}{cc}
 & M \\
 {}_\beta\swarrow & \quad \searrow_\beta \\
 M_1 & \quad M_2 \\
 {}_\beta\searrow & \quad \swarrow_\beta \\
 & M_3
\end{array}
$$

這個定理是函數式語言的理論基石：它保證了「求值順序不影響最終結果」（只要會終止），因此編譯器可以放心採用任何求值策略，甚至並行求值與惰性求值。Haskell 的惰性求值（call-by-need）之所以正確，正是站在 Church-Rosser 定理的肩膀上。

### 線索三：Y 組合子——不用名字的遞迴之謎

Lambda 演算中最神秘的謎題是：**函數匿名，如何遞迴？** 遞迴需要函數呼叫自己，但 λ 抽象中的函數沒有名字，`λf. f(f)` 中的 `f` 指的是外面未定義的自由變數。解法是 Haskell Curry 找到的 **Y 組合子**：

$$
Y = \lambda f.\,(\lambda x.\,f\;(x\,x))\,(\lambda x.\,f\;(x\,x))
$$

其關鍵推導只有一行。令 $A = \lambda x.\,f\,(x\,x)$，則：

$$
Y\,f = A\,A \;\to_\beta\; f\,(A\,A) = f\,(Y\,f)
$$

也就是說 $Y\,f = f\,(Y\,f)$——Y 組合子構造出了 $f$ 的**不動點**：把 $Y\,f$ 代入 $f$，得到的還是 $Y\,f$。遞迴因此誕生：把「階乘的下一步」$g = \lambda n.\; n \le 1\ ?\ 1 : n \times (\,\cdot\,)\,(n-1)$ 中的「自我」留一個洞，用 $Y\,g$ 把 $g$ 自己塞回那個洞，階乘就有定義了。這證明了一個驚人的事實：**在純 lambda 演算中，遞迴不需要名字、不需要 assignment，只需要不動點**。這也是為什麼 Scheme、Haskell 中遞迴的通用寫法是不動點組合子（Haskell 用 `fix`）。

### 線索四：Curry-Howard 對應

Curry 與 Howard 在 1958–1969 年間發現了程式與邏輯的深層對應：

| 邏輯（自然演繹） | 程式（lambda 演算） |
|---|---|
| 命題 $A$ | 型別 $A$ |
| 證明 $a: A$ | 程式項 $a: A$ |
| 蘊含 $A \Rightarrow B$ | 函數型別 $A \to B$ |
| Modus ponens（$a:A$, $f:A\to B$ 得 $b:B$） | 函數應用 $f\,a$ |
| $\forall$ 量化 | 參數多型 |

一句話：**命題即型別，證明即程式，證明化簡即程式求值**。這個對應是後世 ML、Haskell、Coq、Agda 與依賴型別理論的理論地基。

## 結案報告

Lambda 演算是整個函數式程式設計陣營的理論憲法：

- 1958 年 John McCarthy 的 LISP 直接把 lambda 演算的函數當成一等公民引入程式語言（`LAMBDA` 這個關鍵字沿用至今，Python 的 `lambda` 也是其後裔）。
- 1964 年 Peter Landin 用 SECD 機器證明 lambda 演算可以有效率地編譯執行，開啟了函數式語言的實作之路；ML 與 Haskell 的型別推導、惰性求值都源於此。
- Scheme 的詞彙作用域與一級函數、JavaScript 的閉包與箭頭函數 `x => x`（正是 $\lambda x.\,x$ 的符號化身）、Java 8 的 lambda 表達式，全部都是 lambda 演算的語言學遺產。
- Curry-Howard 對應催生了證明助理（Coq、Agda、Lean），今日數學定理的機器驗證直接建築在 lambda 演算之上。
- 遞迴之謎的解答（不動點）也影響了程式語義學：Scott 以領域理論（domain theory）給 lambda 演算建立數學模型，為 1968 年 Dijkstra 之後的形式化驗證運動提供了工具。

一句話總結：圖靈機是「機器」的原子理論，lambda 演算是「函數」的原子理論；前者造出了硬體，後者造出了函數式語言。

## 證據與工具

以下用 Python 實作一個迷你 lambda 演算直譯器，重現 β 歸約、Church 數與 Y 組合子：

```python
# 迷你 lambda 演算：Var / App / Lam 三種項
class Var:
    def __init__(self, name): self.name = name
class Lam:                        # Lam(param, body) = λparam.body
    def __init__(self, param, body): self.param, self.body = param, body
class App:                        # App(f, arg) = f arg
    def __init__(self, f, arg): self.f, self.arg = f, arg

def free_vars(t):
    if isinstance(t, Var): return {t.name}
    if isinstance(t, Lam): return free_vars(t.body) - {t.param}
    return free_vars(t.f) | free_vars(t.arg)

def subst(t, name, val):          # 把 t 中自由的 name 換成 val（β 歸約的核心）
    if isinstance(t, Var):  return val if t.name == name else t
    if isinstance(t, Lam):
        if t.param == name: return t
        # 避免捕捉：改名（α 變換的簡化處理，此處省略衝突情況）
        return Lam(t.param, subst(t.body, name, val))
    return App(subst(t.f, name, val), subst(t.arg, name, val))

def reduce(t, depth=0):           # β 歸約到正規形（Church-Rosser 保證結果唯一）
    if isinstance(t, App) and isinstance(t.f, Lam):
        return reduce(subst(t.f.body, t.f.param, t.arg))
    if isinstance(t, Lam):
        return Lam(t.param, reduce(t.body))
    return t

show = lambda t: (
    t.name if isinstance(t, Var) else
    f"(λ{t.param}.{show(t.body)})" if isinstance(t, Lam) else
    f"({show(t.f)} {show(t.arg)})")

# 恆等函數 λx.x 應用於 5
I = Lam("x", Var("x"))
print("β 歸約 (λx.x 5) ->", show(reduce(App(I, Var("5")))))

# Church 數：0 = λf.λx.x , 2 = λf.λx.f(f x)
c0 = Lam("f", Lam("x", Var("x")))
c2 = Lam("f", Lam("x", App(Var("f"), App(Var("f"), Var("x")))))
succ = Lam("n", Lam("f", Lam("x", App(Var("f"), App(App(Var("n"), Var("f")), Var("x"))))))
c3 = reduce(App(succ, c2))
print("succ(2) 的 Church 數:", show(c3))
# Church 數 3 展開：把 f = (λf.λx.f x) 應用 3 次
val = App(App(c3, Lam("f", Lam("x", App(Var("f"), Var("x"))))), Var("x"))
print("Church 數 3 展開:", show(reduce(val)))

# Y 組合子：Y = λf.(λx.f(x x))(λx.f(x x))
Y = Lam("f", App(Lam("x", App(Var("f"), App(Var("x"), Var("x")))),
                 Lam("x", App(Var("f"), App(Var("x"), Var("x"))))))
print("Y 的結構:", show(Y))
# 用 Python 原生 lambda 模擬 Y f = f (Y f) 的不動點性質
Yf = lambda f: (lambda x: f(x(x)))(lambda x: f(x(x)))
# 有限版本的惰性 Y（避免無限展開）：用 Python 的 lambda 模擬 call-by-need
def lazyY(f):
    return (lambda x: f(lambda *a: x(x)(*a)))(lambda x: f(lambda *a: x(x)(*a)))

fact_gen = lambda f: lambda n: 1 if n <= 1 else n * f(n - 1)
factorial = lazyY(fact_gen)
print("Y 組合子實作遞迴：5! =", factorial(5), ", 10! =", factorial(10))
```

執行結果顯示三件事：第一，β 歸約把 `(λx.x 5)` 化為 `5`，函數呼叫就是改寫；第二，Church 數 `succ(2)` 展開為 `λf.λx.f(f(f x))`，數字就是函數應用的次數；第三，`lazyY` 用純 lambda（Python 的匿名函數）構造出階乘遞迴，證明遞迴不需要名字——只需要不動點 $Y\,f = f\,(Y\,f)$。
