# 1928 - Church 發明 λ 演算

## 案件摘要
1928 年前後，普林斯頓大學的 Alonzo Church 為了研究數學基礎與「可計算性」的本質，
發明了一套以函數為唯一原子的形式系統 —— λ 演算（Lambda Calculus）。
一個看似排版意外的符號「λ」，最終成為貫穿邏輯學、電腦科學與程式語言的千年符號。

## 前因 -- 為什麼會有這個案子
- 20 世紀初，數學基礎危機未解：Russell 悖論動搖了集合論，Hilbert 綱領要求為數學尋找一致且完備的基礎。
- Russell 與 Whitehead 的《Principia Mathematica》（1910–1913）以邏輯主義方式重建數學，但其中「函數」的記法笨重：以帽號記法 $\hat{x}.M$ 表示「以 $x$ 為引數的函數 $M$」。
- Church 想追問一個更根本的問題：「什麼是函數？什麼是『可有效地計算』？」他決定把函數當作第一公民，把一切（數、邏輯命題、甚至邏輯本身）都還原為函數。
- 傳說（Church 本人在 1960 年代受訪時的說法之一）：$\hat{x}$ 送排版時，帽子 ^ 被排印工人換成了大寫希臘字母 Λ，再演變為小寫 λ。一個印刷廠的「筆誤」，就此寫入歷史。

## 線索與推理 -- 數學式、程式、理論

### 1. λ 項（λ-term）的文法
λ 演算的全部世界，僅由三條文法規則構成：

$$
M, N ::= x \quad\mid\quad \lambda x.\, M \quad\mid\quad M\ N
$$

| 構造 | 名稱 | 直覺意義 |
|------|------|----------|
| $x$ | 變數（variable） | 一個未知的值或參數 |
| $\lambda x.\, M$ | 抽象（abstraction） | 函數定義：「把 $x$ 代入 $M$」 |
| $M\ N$ | 應用（application） | 函數呼叫：把 $N$ 餵給 $M$ |

約定：應用左結合，即 $a\ b\ c = ((a\ b)\ c)$；抽象盡量向右延伸，即 $\lambda x.\ a\ b = \lambda x.\ (a\ b)$。

以 Python 的 closure 觀念對照，抽象就是回傳函數、應用就是呼叫函數：

```python
# λx. x  在 Python 中：
identity = lambda x: x
# (λx. x) y 應用：
identity(42)   # => 42
```

### 2. β-歸約（β-reduction）：計算的核心引擎
計算只有一條規則 —— 把引數代入函數體：

$$
(\lambda x.\, M)\ N \;\longrightarrow_\beta\; M\,[N/x]
$$

其中 $M\,[N/x]$ 表示「把 $M$ 中所有自由出現的 $x$ 替換為 $N$」。

例：
$$
(\lambda x.\, x\ x)\ (\lambda y.\, y) \;\to_\beta\; (\lambda y.\, y)(\lambda y.\, y) \;\to_\beta\; \lambda y.\, y
$$

注意：有些項會永遠歸約不停，例如

$$
\Omega = (\lambda x.\, x\ x)(\lambda x.\, x\ x) \;\to_\beta\; \Omega \;\to_\beta\; \Omega \;\to_\beta\; \cdots
$$

λ 演算因此天生就具有「可能不停機」的特性 —— 這正是後來可計算性理論與停機問題的伏筆。

### 3. α-等價（α-equivalence）：名字不重要，結構才重要
$$
\lambda x.\, x \;\equiv_\alpha\; \lambda y.\, y \;\equiv_\alpha\; \lambda z.\, z
$$

只要把束縛變數系統性地改名，兩項就是同一個函數。這就像偵探辦案：兇手換了名字，罪行結構不變。α-等價是 β-歸約安全進行的前提 —— 代入前常需先 α-改名以避免變數捕捉（variable capture）。

### 4. η-歸約（η-reduction）：外延性
$$
\lambda x.\, f\ x \;\longrightarrow_\eta\; f \qquad (x \notin FV(f))
$$

意思是：若 $f$ 本身就是「把引數交給 $f$」的函數，那層包裝是多餘的。η-歸約體現了函數的**外延性**（extensionality）：決定函數的是輸入輸出的對應關係，而非寫法。

### 5. 自由變數與束縛變數
- $FV(x) = \{x\}$
- $FV(\lambda x.\, M) = FV(M) \setminus \{x\}$（$x$ 被 λ **束縛**了）
- $FV(M\ N) = FV(M) \cup FV(N)$

一個項若沒有自由變數（$FV(M) = \emptyset$），稱為**封閉項**（closed term）或**組合子**（combinator）。λ 演算最有趣的居民，幾乎都是組合子。

### 6. 以偽碼實作 β-歸約
```text
function substitute(M, x, N):
    if M == x:            return N
    if M is variable:     return M
    if M == (λy. P):
        if y == x:        return M            # x 已被束縛，停止
        if y ∈ FV(N):     y' = fresh();  P = substitute(P, y, Var(y'))
                                                # 先 α-改名避免捕捉
        return λy'. substitute(P, x, N)
    if M == (P Q):        return (substitute(P, x, N) substitute(Q, x, N))
```

## 結案 -- 後果與影響
- 1928–1936 年，Church 以 λ 演算為工具發表了一系列邏輯與可計算性論文，開啟了整個研究綱領。
- 1936 年 Church 用它證明判定問題（Entscheidungsproblem）不可判定；同年 Turing 用圖靈機獨立證明同一結果，兩者後來被證明等價（Church–Turing 命題）。
- λ 演算成為函數式程式語言的理論基石：Lisp（1958）、ML、Haskell、Scala、乃至 JavaScript 的 `=>` 箭頭函數與 Python 的 `lambda`，都是 $\lambda x.\, M$ 的後裔。
- 「計算只需函數與一條歸約規則」—— 這是電腦科學史上最優雅的結案陳詞。

## 關鍵人物與文獻
- **Alonzo Church**（1903–1995）：普林斯頓邏輯學家，λ 演算之父，後續亦指導 Turing 與 Kleene。
- A. Church, *A set of postulates for the foundation of logic*, Annals of Mathematics, 33 & 34 (1932, 1933)。
- A. Church, *The Calculi of Lambda-Conversion*, Princeton University Press (1941)。
- H. B. Curry & R. Feys, *Combinatory Logic* (1958)：λ 演算與組合邏輯的系統性整理。
- H. P. Barendregt, *The Lambda Calculus: Its Syntax and Semantics* (1984)：至今的標準參考書。
