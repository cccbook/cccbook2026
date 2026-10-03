# 1985-Miranda與惰性求值

## 案件摘要

1985 年，Kent 大學的 David Turner 透過 Research Software Ltd 發表 Miranda，這是史上第一個商業化的純函數式惰性求值語言。在此之前，Turner 已用 SASL（1976）與 KRC（1981）逐步驗證惰性求值的可行性。Miranda 的最大嫌疑動機是：Turner 想證明「惰性語言可以被高效地編譯與執行」，打破「函數式編程注定太慢」的偏見。本案的破案時刻，在於 Miranda 展示了無窮資料結構可以在有限記憶體中優雅運作，而且編譯技術（G-machine、supercombinators）確實夠快。

## 前因 -- 為什麼會有這個案子

- 1970 年代主流語言（Pascal、C、Lisp）都是 eager（嚴格）求值：函數參數在呼叫前就全部算好。這使得無窮資料結構（如所有質數的串列）根本「算不到」，因為求值永不終止。
- Peter Henderson 與 John Darlington 在 SASL 中實驗「lazy evaluation」，證明用串列延遲求值可以表達無窮結構。
- Stephen Brookes、Wadler 與 John Hughes 等人後續論證惰性求值能带来模組化優點：生產者與消費者可以完全解耦。
- Turner 自己的 G-machine（1979）研究顯示：λ 項可編譯成組合子，在圖規約機上高效執行——這是「惰性可以快」的理論武器。
- 學界教學上需要一個純粹、簡潔、可以真正跑起來的函數式語言；當時的教學語言不是太雜（Lisp 方言林立）就是太慢。

## 線索與推理 -- 數學式、程式、理論

### 線索一：call-by-need 的數學本質

惰性求值的核心是 call-by-need：參數不先求值，而是包成一個 thunk（未求值表達式加上環境的閉包），等到真正需要時才展開求值，並且 memoization——求值結果快取起來，第二次需要時直接讀取。

在指稱語義上，非嚴格求值允許底數（bottom，表示未定義或發散）傳遞而不引爆：

$$\llbracket \lambda x. e \rrbracket \, \rho = \lambda v. \llbracket e \rrbracket \, \rho[x \mapsto v]$$

嚴格求值要求 $v \neq \bot$ 才能進入函數體；非嚴格求值允許 $v = \bot$，只要 $x$ 不被用到。

### 線索二：無窮資料結構

Miranda 與 Haskell 的招牌：Fibonacci 數列定義為自身與自身尾部的遞迴 zip：

```haskell
fibs = 0 : 1 : zipWith (+) fibs (tail fibs)
```

這在數學上是「遞迴方程式的最小不動點」：

$$\text{fibs} = \bigsqcup_{n \geq 0} F^n(\bot)$$

其中 $F$ 是右邊表達式對應的連續泛函。因為每次只「需要」有限個元素，`take 10 fibs` 只求值前 10 個 thunk，其餘永遠停留在未展開狀態。

### 線索三：thunk 的 Python 實作

用 Python 模擬 call-by-need：每個 cons cell 帶一個 thunk，且求值一次後快取。

```python
class LazyList:
    def __init__(self, head, thunk):
        self.head = head
        self._thunk = thunk
        self._tail = None

    @property
    def tail(self):
        if self._tail is None:
            self._tail = self._thunk()
        return self._tail

def take(n, xs):
    out = []
    for _ in range(n):
        out.append(xs.head)
        xs = xs.tail
    return out

fibs = LazyList(0, lambda: LazyList(1, lambda: _fib_stream(fibs, fibs.tail)))

def _fib_stream(a, b):
    return LazyList(a.head + b.head, lambda: _fib_stream(a.tail, b.tail))

print(take(10, fibs))   # [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
```

注意 `_tail` 的快取：第二次存取 `fibs.tail` 時不再重算——這正是 memoization，也是 Haskell 中的 thunk 更新（update）。

### 線索四：G-machine 與 supercombinators

Turner（1979）的關鍵推理：與其在直譯器中反覆展開 λ 項，不如在編譯期把程式翻譯成組合子（combinator），讓執行期只需圖規約。

- **組合子編碼**：把 λ 項消去抽象（lambda lifting），例如以 SK 優化：
  $$\llbracket \lambda x. x \rrbracket = I, \quad \llbracket \lambda x. f \rrbracket = K\,f, \quad \llbracket \lambda x. f\,x \rrbracket = f$$
- **Hughes 的 supercombinators（1982）**：不只用固定的 S、K、I，而是為每個函數找出「最大的自由組合子」作為編譯單位，減少中間規約步數。
- **G-machine 執行**：程式被編譯成操作抽象機（圖堆疊機）的指令序列，規約即「在圖上找最外層 redex、替換為其結果」。
- **嚴格性分析（strictness analysis）**：若能證明某參數「一定會被用到」，就前瞻地先求值它，把 thunk 開銷省掉。形式上，若 $f\,\bot = \bot$，則 $f$ 對第一參數是嚴格的，可安全地 eager 求值。

### 破案時刻

Miranda 在 1980 年代中期被數十所大學採用為教學語言，編譯器效率足以在一般工作站上跑遞迴與無窮結構。Turner 的論證成立：惰性不等於慢。

## 結案 -- 後果與影響

- Miranda 成為 Haskell 誕生前最流行的教學與研究用純函數式語言。
- Miranda 的語法——`where` 子句、縮排式 offside rule、pattern matching 與 guard——直接成為 Haskell 的設計藍本。
- Turner 的組合子編譯思想經 supercombinators 精煉後，進入 GHC 的 STG（Spineless Tagless G-machine）中間表示。
- 惰性求值與無窮資料結構成為函數式編程的招牌能力，影響後世 Scala（lazy val）、Python 產生器等設計。
- 「純函數式可以商用」此案結案後，後續的語言統一運動（Haskell 會議）才有立足點。

## 關鍵人物與文獻

- David Turner — Miranda 的設計者，SASL、KRC 先驅，G-machine 發明人。
- Peter Henderson、John Darlington — SASL 惰性思想源頭。
- John Hughes — supercombinators 編譯技術；後著〈Why Functional Programming Matters〉。
- 文獻：
  - Turner, D. A. (1979). "A New Implementation Technique for Applicative Languages." *Software: Practice and Experience*, 9(1), 31–49.
  - Turner, D. A. (1985). "Miranda: A Non-Strict Functional Language with Polymorphic Types." *Proceedings of the 2nd International Conference on Functional Programming Languages and Computer Architecture (FPCA)*, LNCS 201, Springer, 1–16.
  - Hughes, R. J. M. (1982). "Super-combinators: A New Implementation Method for Applicative Languages." *Proceedings of the 1982 ACM Symposium on LISP and Functional Programming*, 1–10.
  - Henderson, P., & Darlington, J. (1980). "Applicative Programming and Specification." *IEEE Transactions on Software Engineering*, SE-6(2), 105–114.
  - Hughes, J. (1989). "Why Functional Programming Matters." *The Computer Journal*, 32(2), 98–107.
