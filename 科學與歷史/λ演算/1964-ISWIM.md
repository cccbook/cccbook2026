# 14. 1964 — Peter Landin 的 ISWIM 語言（"If you See What I Mean"）

## 案件摘要

1964 年，Peter Landin 在論文 *How to Use the Evaluation of Expressions by Machines* 與 1966 年的 *"The Next 700 Programming Languages"* 中提出 ISWIM（"If you See What I Mean"）語言。這是一門「紙上的語言」——從未完整實作，卻定義了此後函數式語言五十年的語法樣貌：`where` 子句、縮排（offside rule）、以及「語法只是 λ 演算的糖衣」的設計哲學。

## 前因 -- 為什麼會有這個案子

1960 年代初的程式語言世界群雄並起：ALGOL 60 剛確立「區塊結構與語法形式化」的傳統，LISP 則以 S-expression 混亂但強大地實現了 λ 演算。Landin 觀察到一個線索：

- ALGOL 60 的 `begin ... end`、宣告、敘述結構繁瑣；
- LISP 的大量的括號令人類難以閱讀；
- 但兩者底層都是同一個數學結構——λ 演算。

Landin 的推理是：**如果所有語言的語義核心都是 λ 演算，那麼語言設計的重點就應該放在「讓人類『看見意義』的語法」上**。他造出 ISWIM 這個名字："If you See What I Mean"（如果你懂我的意思）。他著名的宣稱是：ALGOL 只不過是 700 種程式語言中的一種，未來的語言都應該圍繞 λ 演算這個核心設計。

## 線索與推理 -- 數學式、程式、理論

### 1. 語法設計：`where` 子句

ISWIM 最大的創新是把 ALGOL 的「先宣告、後使用」顛倒成「先使用、後宣告」：

```iswim
-- ISWIM 風格
recip x = 1/x  where x ≠ 0

-- 平方根的 Newton 法（Landin 的經典例子）
sqrt a = approxs a/2  where approxs = ...
```

其結構對應 λ 演算：

$$
\texttt{let}\ x = e\ \texttt{in}\ b \quad \Longleftrightarrow \quad (\lambda x.\, b)\ e
$$

而 ISWIM 的 `where` 則是反序的糖：

$$
b\ \texttt{where}\ x = e \quad \Longleftrightarrow \quad \texttt{let}\ x = e\ \texttt{in}\ b \quad \Longleftrightarrow \quad (\lambda x.\, b)\ e
$$

### 2. Offside Rule：縮排即語法

ISWIM 以「offside rule（越位規則）」取代括號：**任何符號如果出現在它所在行的起始縮排左邊，就不屬於這個區塊**。形式化地說，一個 token $t$ 在位置 $(i, j)$（行 $i$、欄 $j$），它屬於某結構當且僅當 $j \geq j_0$（$j_0$ 為該結構的起始欄）。

這條規則被 SASL、Miranda、Haskell 直接繼承。Haskell 中：

```haskell
-- offside rule 的現代繼承者：Haskell
let x = 1
    y = 2
in x + y

-- 同理，where 子句：
gcd a b
  | a > b     = gcd (a - b) b
  | otherwise = a
```

### 3. Desugaring：語法只是糖

Landin 的核心方法論：把高階語法 **desugar（脫糖）** 成 λ 演算的甘藍菜核心（"a kernel of cabbage"，他戲稱 λ 演算核心）。例如：

```text
-- ISWIM 表達式                 -- desugar 成 λ 演算
let f = λx. x+1 in f 3    ⟹    (λf. f 3) (λx. x+1)
letrec 的遞迴宣告          ⟹    Y (λf. λx. ... f x ...)（後來的遞迴語義）
```

他還提出了著名的 **SECD 機器**（Stack, Environment, Control, Dump）作為 λ 演算的操作語義模型——這是第一個把 λ 演算「編譯成機器碼」的抽象機。

### 4. 语法到語義的完整管道

$$
\text{ISWIM 語法} \xrightarrow{\text{desugar}} \lambda\text{ 演算核心} \xrightarrow{\text{SECD}} \text{機器執行}
$$

## 結案 -- 後果與影響

ISWIM 本身沒有完整的實作，但它的「語法遺產」無所不在：

1. **ML（1973）** 繼承了 `let ... in` 與 case/match 的 λ 結構；
2. **SASL（1972）、Miranda（1985）、Haskell（1990）** 繼承了 offside rule 與 `where` 子句——Haskell 的縮排規則就是 ISWIM 的 offside rule；
3. Landin 的 desugaring 方法成為編譯器前端設計的標準手法（如 Haskell 的 Core IR）；
4. SECD 機器成為函數式語言操作語義與虛擬機（如 CAM、SECD 家族）的起點；
5. "The Next 700 Programming Languages" 的宣言在半世紀後被 "The Next 700 Semantic Frameworks" 等文獻致敬。

## 關鍵人物與文獻

- **Peter Landin**（1930–2019）：英國計算機科學家，曾與 Christopher Strachey 合作，後移居倫敦大學。
- P. Landin, *"The Mechanical Evaluation of Expressions"* (1964)——提出 SECD 機器。
- P. Landin, *"The Next 700 Programming Languages"* (1966)——提出 ISWIM。
- P. Landin, *"A Correspondence between ALGOL 60 and Church's Lambda-Notation"* (1965)——奠定 ALGOL 與 λ 演算的對應。
