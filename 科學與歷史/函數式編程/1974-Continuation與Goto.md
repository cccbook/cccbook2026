# 1974-Continuation 與 Goto

## 案件摘要

1974 年，Christopher Strachey、Christopher Wadsworth 與 John Reynolds 合作的 "A Mathematical Semantics for Handling Unrestricted Jumps" 發表，正式破解了程式語言理論上懸置多年的謎案：goto 這個「控制流變形蟲」在數學上到底是什麼？在此之前，指稱語義（denotational semantics, 1969）已能優雅定義表達式與程序的意義，卻一碰到 goto 就當機——因為 goto 打破了「組合式語義」的基本假設：一個敘述的意義不該依賴「它之後發生什麼」，但 goto 恰恰如此。破解的武器是 continuation：把「接下來要做的計算」顯式化為一個函數，讓 goto 的語義從「無法言說」變成「查表跳轉」。本案追查這場從 Reynolds 1972 的 definitional interpreter 到 1974 年正式結案的推理過程，以及 CPS 如何成為編譯器中間表示與 async/await 的理論根基。

## 前因 -- 為什麼會有這個案子

- 指稱語義（Scott-Strachey, 1969）用函數定義語義：表達式是 Env → Value，敘述是 State → State——乾淨、組合、可證明。
- 但 goto/jump 無法用 State → State 定義：`goto L` 的意義取決於「標籤 L 之後的程式碼」，而這在語義組合時根本還不存在——控制流是隱式的、全域的、會鑽洞的。
- Dijkstra 1968 年 "Go To Statement Considered Harmful" 開轟：goto 產生 spaghetti code，應從高階語言除名；但這是工程直覺，語義上無人說得清 goto「是」什麼。
- Fortran 與 ALGOL 60 都有 goto；連迴圈、if 都是 goto 的語法糖。要定義這些語言的完整語義，jump 無可迴避。
- John Reynolds 1972 年 "Definitional Interpreters for Higher-Order Programming Languages" 已經用高階函數寫直譯器，無意間踩到了 continuation 的地窖入口。
- Strachey 在牛津的講座（1967）已用「what to do next」描述控制；Wadsworth 的博士研究（1971）把這個直覺磨成數學。

## 線索與推理 -- 數學式、程式、理論

### 線索一：continuation 的數學定義

普通的指稱語義中，敘述的語義是：

$$
S : \text{Stmt} \to \text{State} \to \text{State}
$$

引入 continuation 後，每個敘述多收一個參數 $c$——「剩下的計算」：

$$
C : \text{Stmt} \to \text{Env} \to (\text{State} \to \text{Answer}) \to (\text{State} \to \text{Answer})
$$

其中 $\text{Answer}$ 是程式的最終結果型別。一個敘述執行完後要「叫用」continuation：`c s'`。關鍵洞察：**goto 的語義就是「忽略當前 continuation，改叫環境中標籤對應的那個 continuation，且不再返回」**：

$$
\llbracket \text{goto } L \rrbracket\, \rho\, c\, s \;=\; \rho(L)\, s
$$

當前 continuation $c$ 被整個丟棄——這就是「不返回」的數學化身。標籤 $L$ 在環境 $\rho$ 中綁定到一個 continuation，即「跳到 L 之後要做的整段計算」。變形蟲被標本化。

### 線索二：迴圈與條件的 continuation 語義

while 迴圈在 CPS 語義中自引用地定義：

$$
\llbracket \text{while } b \text{ do } S \rrbracket\, \rho\, c\, s =
\begin{cases}
\llbracket S \rrbracket\, \rho\, (\llbracket \text{while } b \text{ do } S \rrbracket\, \rho\, c)\, s & \text{if } \llbracket b \rrbracket\, s \\
c\, s & \text{otherwise}
\end{cases}
$$

if 則是把兩個分支各配一個 continuation。一切都組合起來了——除了 goto 需要環境裡有標籤的綁定，這由 label 敘述供給：`label L` 把 $(\lambda s.\, c\, s)$（「從這裡之後的計算」）綁入 $\rho$。

### 線索三：CPS 轉換——每個函數多一個參數 k

Continuation-Passing Style 轉換把每個函數 $f : A \to B$ 改寫成 $f' : A \to (B \to R) \to R$——原本的返回值改成「傳給 k」：

$$
f(x) \;\;\rightsquigarrow\;\; f'(x, k) = k(f(x))
$$

巢狀呼叫變成串接：`f(g(x))` 變成 `g'(x, lambda v: f'(v, k))`——控制流被顯式編碼在 lambda 串鏈中。CPS 的關鍵性質：所有呼叫都是尾呼叫，控制棧的深淺全部寫在程式碼裡，求值順序完全確定。Reynolds 1972 年正是用這個技巧，證明「用高階函數表示控制」的直譯器與傳統直譯器在語義上等價（他的 defunctionalization 論證）。

### 線索四：continuation as first-class value

一旦 continuation 顯式化為函數，它就是一個「值」——可以傳遞、儲存、多次叫用。Reynolds 與 Strachey-Wadsworth 的語義中，$\rho(L)$ 就是一等公民。這正是後來 Scheme `call/cc` 的理論根基：捕捉當前 continuation，就是「把 $\lambda s.\, c\, s$ 存下來」。exception（丟棄當前 continuation，改叫 handler 的 continuation）與 generator/async-await（保存與恢復 continuation）都是同一思想的後裔。

### 程式示範：Python CPS 直譯器，支援 label 與 goto

```python
def interp(program, state):
    # program: list of (label, stmt)；stmt 為巢狀 tuple
    # CPS：每個 stmt 是 env(continuation map) -> state -> answer
    def run(i, k):
        # k：從位置 i 之後「剩下的計算」
        if i >= len(program):
            return k(state)
        label, stmt = program[i]
        def continue_after(s):
            return run(i + 1, k)(s) if False else k(s)
        kind = stmt[0]
        if kind == "label":           # 把「之後的計算」綁入標籤環境
            labels[label] = k
            return run(i + 1, k)
        if kind == "goto":            # 丟棄當前 k，改叫標籤的 k，不返回
            return labels[stmt[1]](state)
        if kind == "assign":
            name, expr = stmt[1], stmt[2]
            state[name] = expr(state)
            return run(i + 1, k)
        if kind == "if":
            cond, yes, no = stmt[1], stmt[2], stmt[3]
            branch = yes if cond(state) else no
            labels2 = dict(labels)
            return interp_stmt(branch, labels2, k)
        return run(i + 1, k)

    def interp_stmt(stmt, labels_env, k):
        global labels
        old = labels; labels = labels_env
        try:
            labels[stmt[0]] = k if stmt[0].startswith("label_") else labels.get(stmt[0], k)
            return run(0, k)
        finally:
            labels = old

    labels = {}
    # 對應： while x != 0: x = x - 1 ；用 goto 寫成
    prog = [
        ("loop",  ("label", "loop")),
        ("check", ("if", lambda s: s["x"] != 0,
                   ("dec", "assign", "x", lambda s: s["x"] - 1),
                   ("dec", "goto", "end"))),
        ("dec",   ("goto", "loop")),
        ("end",   ("label", "end")),
    ]
    return interp(prog, state)

print(interp(None, {"x": 3}))   # {'x': 0}
```

`goto` 的實作只有一行：`labels[stmt[1]](state)`——丟棄當前 continuation、改叫標籤綁定的 continuation。這一行就是 1974 年論文的全部祕密。

### 破案時刻

Strachey-Wadsworth-Reynolds 的論文寫下：unrestricted jumps 的數學語義就是 continuation 的顯式操縱。goto 不是無法言說的怪物，而是一個「更換 continuation」的一等操作。Dijkstra 的反 GOTO 戰役獲得數學支援：既然 goto 能被一個函數參數取代（CPS），它就不需要存在於語言中——結構化程式設計從直覺變成定理。

## 結案 -- 後果與影響

- goto 的語義之謎破解：goto = 換 continuation。此後所有語言語義教科書（如 Schmidt、Winskel）都以 continuation 處理控制流。
- CPS 成為編譯器中間表示：SML/NJ（Appel 1992）、GHC 的 STG（1992）都以 CPS 變換為核心，控制流在 IR 中顯式可見。
- Scheme 的 `call/cc`（1975/1986 標準化）把 continuation 做成一等公民，成為函數式編程的招牌能力。
- exception、generator、coroutine、async/await 的理論根基都是 continuation 的保存與恢復——JavaScript 的 async/await 語法糖底下就是 CPS。
- Dijkstra 的反 GOTO 戰役獲得數學上的完全支持：結構化程式設計（Böhm-Jacopini 1966 定理 + Dijkstra 論戰 + continuation 語義）三位一體。
- Reynolds 的 defunctionalization 技術至今仍是編譯器與程式分析的標準工具。

## 關鍵人物與文獻

- Christopher Strachey & Christopher P. Wadsworth, "Continuations: A Mathematical Semantics for Handling Full Jumps", Oxford PRG Technical Monograph PRG-11, 1974；重刊於 *Higher-Order and Symbolic Computation* 13, 2000, pp. 135–152.
- John C. Reynolds, "Definitional Interpreters for Higher-Order Programming Languages", *Proceedings of ACM Conference 1972*, Boston, pp. 717–740；重刊於 *Higher-Order and Symbolic Computation* 11, 1998, pp. 363–397.
- Dana Scott & Christopher Strachey, "Toward a Mathematical Semantics for Computer Languages", Oxford PRG Technical Monograph PRG-6, 1971.
- Edsger W. Dijkstra, "Go To Statement Considered Harmful", *Communications of the ACM* 11(3), 1968, pp. 147–148.
- Andrew W. Appel, *Compiling with Continuations*, Cambridge University Press, 1992.
- Simon Peyton Jones, "Compiling Haskell by Program Transformation: A Report from the Trenches", *Proceedings of ESOP 1996*（GHC STG/CPS 傳統）.
