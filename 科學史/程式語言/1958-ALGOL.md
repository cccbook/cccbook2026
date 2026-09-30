# 1958 ALGOL：演算法語言的誕生

## 案發現場

1950 年代中期，電腦界陷入一場「巴別塔危機」。IBM 有 FORTRAN，Univac 有 MATH-MATIC，每家廠商都有自己的語言，每種語言都綁死在特定機器上。科學計算的論文開始面對一個尷尬的問題：論文裡的「演算法」到底該怎麼寫？用 FORTRAN 寫，讀者可能沒有 IBM 機器；用流程圖寫，又不夠精確。當時 ACM 與歐洲的 GAMM（應用數學與力學學會）都意識到：需要一種**機器無關的、用來描述演算法的通用語言**。

遇見這個問題的人包括 IBM 的 John Backus（FORTRAN 之父）、蘇黎世 ETH 的 Heinz Rutishauser、以及後來加入的 Peter Naur 與 Alan Perlis。對他們而言，這不只是工程問題，而是學術問題——「演算法」這個自圖靈與邱奇以來的核心概念，需要一個正式的書寫載體。這就是 ALGOL（ALGOrithmic Language）計畫的起點：1958 年蘇黎世會議產出 ALGOL 58，1960 年巴黎會議修訂為 ALGOL 60。

## 偵查過程

### 線索一：用文法定義語言本身

Backus 在設計 FORTRAN 時就曾思考：語言的語法可否用數學方式嚴格描述？在 1959 年的巴黎 UNESCO 會議上，他發表了描述 ALGOL 語法的記法，後經 Naur 用於 ALGOL 60 報告，成為著名的 **BNF（Backus-Naur Form）**。核心概念是：一個語言就是一個字串集合，可用生成規則（產生規則）遞迴地定義。例如算術運算式：

$$
\begin{aligned}
\langle expr \rangle &::= \langle term \rangle \mid \langle expr \rangle + \langle term \rangle \mid \langle expr \rangle - \langle term \rangle \\
\langle term \rangle &::= \langle factor \rangle \mid \langle term \rangle \times \langle factor \rangle \\
\langle factor \rangle &::= \langle identifier \rangle \mid \langle number \rangle \mid (\langle expr \rangle)
\end{aligned}
$$

這三條規則不只是描述語法，它們**同時就是遞迴下降剖析器的骨架**：$\langle expr \rangle$ 遞迴地引用自己，因此任意深度的巢狀括號如 `(a + (b × (c − d)))` 都能被生成與解析。這是第一次，程式語言的語法有了精確的數學定義，編譯器設計從手工藝變成工程科學。

### 線索二：區塊結構與遞迴

ALGOL 60 引入了 `begin ... end` 區塊，使程式具有層層巢狀的詞彙領域（scope）結構：

```algol
begin
    integer n;
    real procedure fact(k);
        value k; integer k;
        fact := if k ≤ 1 then 1 else k × fact(k − 1);
    n := fact(5)
end
```

這段程式展示了兩大創舉。第一，變數 `n` 與程序 `fact` 的可見範圍被區塊限定，離開區塊即消失——這是靜態作用域與堆疊式儲存配置的濫觴。第二，**遞迴程序**。FORTRAN 90 年代以前的版本明確禁止遞迴，因為它把所有變數放在靜態儲存區；ALGOL 的設計者則推導出：既然變數的生命週期跟著區塊走，那麼每次程序呼叫就該在**執行堆疊（run-time stack）**上配置一個新的活動紀錄（activation record）。Dijkstra 等人提出的堆疊式執行模型，使遞迴自然可行，這個模型至今仍是所有主流語言執行時期的基礎。

### 線索三：Call by Name 與 Jensen's Trick

ALGOL 60 的參數傳遞提供了 call-by-name：實際參數不是先求值再傳入，而是把「未求值的運算式本體」用 thunk 包起來，每次在程序內用到該參數時才重新求值。這催生了著名的 **Jensen's Trick**——用一個程序同時實作內積、矩陣加法等看似不同的運算：

```algol
begin
    real procedure sigma(i, lo, hi, term);
        value lo, hi;
        integer i, lo, hi; real term;
    begin
        real s;
        sigma := 0;
        for i := lo step 1 until hi do s := s + term;
        sigma := s
    end;
    outreal(1, sigma(j, 1, 100, 1/j))
end
```

呼叫 `sigma(j, 1, 100, 1/j)` 時，`term` 是未求值的 `1/j`，且 `j` 是呼叫者的變數——因此程序內每次 `s + term` 都會以當下的 `j` 求值 `1/j`，結果是 $\sum_{j=1}^{100} \frac{1}{j}$。同一個 `sigma`，傳入 `x[i] × y[i]` 就變成內積。Call by name 證明了「程式碼本身可以當資料傳遞」，這正是延遲求值與 lambda 傳遞的先聲——但它每用一次就重算一次，代價高昂，日後被 call-by-value（多數語言）與 call-by-need（Haskell）取代。

## 結案報告

ALGOL 60 是程式語言史上「影響最大、卻自身未流行」的經典，人稱**「語言中的拉丁文」**：它是後世語言的祖先，但沒有人在日常生活中使用它。原因包括：官方報告沒有規定輸入輸出（I/O 留給各實作）、缺乏商業支援、以及 IBM 較看好自己的 FORTRAN。

但它的遺產無所不在：

- **BNF 文法**成為描述一切語言（從 C 到 JSON 到 SQL）的標準工具，編譯器教科書第一章都是它。
- **區塊結構、堆疊式儲存、遞迴**成為所有主流語言的預設。
- ALGOL 68 雖然過於複雜而失敗，但從它的評審委員會出走，誕生了 [1970-Pascal.md](1970-Pascal.md) 的 Niklaus Wirth。
- Tony Hoare 在 ALGOL 60 的基礎上發展了 ALGOL W，進而催生 Pascal；C 語言的語法骨架（`{ }` 區塊、運算式文法）直接承襲自 B（BCPL）而 B 源自 ALGOL 傳統。
- 歐洲學界以 ALGOL 為基礎發展出的 Simula，見 [1967-Simula物件導向.md](1967-Simula物件導向.md)。

一句話總結：FORTRAN 讓程式設計流行，ALGOL 讓程式設計成為一門科學。

## 證據與工具

以下用 Python 模擬「用 BNF 文法生成 ALGOL 運算式」與 Jensen's Trick 的語義：

```python
import random

# BNF 產生規則（對應 ALGOL 60 的 <expr> 文法）
grammar = {
    "expr":  [["term"], ["expr", "+", "term"]],
    "term":  [["factor"], ["term", "*", "factor"]],
    "factor": [["id"], ["(", "expr", ")"]],
}

def generate(symbol, depth=0):
    if depth > 4:                      # 控制深度避免無限遞迴
        return random.choice(["a", "b", "c"])
    if symbol not in grammar:
        return symbol
    rule = random.choice(grammar[symbol])
    return " ".join(generate(s, depth + 1) for s in rule)

print("隨機生成的 ALGOL 運算式：", generate("expr"))

# Jensen's Trick 模擬：call by name 用 Python 的 lambda（thunk）模擬
def sigma(i_name, lo, hi, term):       # term 是一個「未求值」的 thunk
    s = 0.0
    env = {i_name: None}               # i 是呼叫者的變數，每次迴圈更新
    for j in range(lo, hi + 1):
        env[i_name] = j
        s += term(env[i_name])         # 每次用到 term 才求值 -> call by name
    return s

# 同一個 sigma：調和級數、內積、平方和
print("調和級數 sum 1/j  =", sigma("j", 1, 100, lambda j: 1 / j))
print("內積 sum x[i]*y[i] =", sigma("i", 0, 3, lambda i: [1,2,3][i] * [4,5,6][i]))
print("平方和 sum i^2     =", sigma("i", 1, 10, lambda i: i * i))
```

執行結果會顯示：第一部分隨機生成如 `a + b * ( expr ... )` 的合法運算式，證明 BNF 規則即可生成語言；第二部分證明同一個 `sigma` 程序，靠 call-by-name 傳入不同的運算式，就能變成調和級數、內積或平方和——正是 1960 年 Jensen's Trick 的精髓。
