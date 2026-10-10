# 1977 Backus 函數式倡議：把程式設計從馮紐曼風格中解放

## 案發現場

1977 年 8 月，John Backus 站上 ACM 圖靈獎頒獎典禮的講台。這位 FORTRAN 的發明人、BNF 范式的創立者，做了一件出乎所有人意料的事：**他批判了自己畢生的作品。**

他的演講題目是「Can Programming Be Liberated from the von Neumann Style? A Functional Style and Its Algebra of Programs」。

當時的未解之謎：**為什麼軟體危機愈演愈烈？為什麼程式這麼難寫、難讀、難證明正確？** Backus 的答案是：因為指令式語言的根基——馮紐曼架構本身——就是問題。

馮紐曼電腦的本質是「記憶體 + CPU，逐字修改狀態」，而 FORTRAN、ALGOL、PL/I 這些語言只是給這個瓶頸（Backus 稱之為 **von Neumann bottleneck**）套上一層薄皮。每次資料都要在記憶體與 CPU 之間一個字一個字地搬運；高階語言的變數賦值不過是這種搬運的語法糖。結果是：

- 程式被「一個字一個字」的思維綁架，無法用大的概念單位思考。
- 賦值語句產生**隱藏的時序依賴**，程式的語義被狀態的變化順序污染。
- 程式無法做**代數推理**——你不能像化簡 $a(b+c) = ab+ac$ 那樣化簡程式。

這個批判為何重要？1977 年正值軟體危機高峰，結構化程式設計剛剛勝利，人們以為問題已解。Backus 卻指出：結構化只是讓「字級思考」有條理，並沒有改變思維的單位。真正需要的是**函數式風格**——用「整體到整體」的函數組合取代「字級」的賦值。

## 偵查過程

Backus 提出的解方是 **FP 系統**——一個沒有變數、沒有賦值、只有函數與組合子（combinators）的語言。他的設計推理如下：

**第一步：程式即運算式。** FP 程式是運算式 $e$，作用於單一參數 $x$（可以是任意物件），寫作 $e : x$。沒有命名、沒有狀態，程式就是資料到資料的映射。

**第二步：組合子的代數。** FP 提供一組固定的組合子，它們是「吃函數、吐函數」的高階函數：

- 組合 $f \circ g$：$(f \circ g) : x = f : (g : x)$
- 構造 $[f, g]$：$[f, g] : x = \langle f : x,\ g : x \rangle$
- 條件 $\bar{p} \rightarrow f ; g$：若 $p : x$ 為真則 $f : x$ 否則 $g : x$

關鍵在於**組合子滿足代數律**。例如：

$$(f \circ g) \circ h = f \circ (g \circ h)$$

$$[f, g] \circ [h, k] = [f \circ h,\ g \circ k]$$

這些律使程式可以像中學代數一樣被化簡、變換、證明等價。這正是 Backus 夢寐以求的「程式代數」。

**第三步：一個實例。** 計算內積（dot product）——Backus 演講的招牌例子：

$$innerproduct : \langle x, y \rangle = /+\ \circ\ \alpha \times \circ\ transpose : \langle x, y \rangle$$

拆解：$transpose$ 轉置矩陣，$\alpha \times$ 對每對元素做乘法（map），$/+$ 做歸約（reduce）。整個定義是「三個組合子的一行串接」，沒有迴圈、沒有索引、沒有暫存變數。對比 FORTRAN 的十行 DO 迴圈，Backus 問：**哪一個更容易證明正確？**

**第四步：更進一步的 FFP 與 λ 演算。** Backus 還提出 FFP（Formal FP），允許使用者自訂函數並帶有名字；並承認現代的 λ 演算（如 ISWIM）也可以是函數式語言的基礎——只要去掉賦值。這為後來的 Scheme、ML、Haskell 鋪了路。

## 結案報告

Backus 倡議的遺產：

- **宣告式思維之源**：map/reduce 這兩個詞從此成為程式設計的基本詞彙。Google 的 MapReduce 分散式運算框架（2004）直接以此命名。
- **語言系譜**：Scheme（1975）、Standard ML、Haskell（[1990-Haskell.md](1990-Haskell.md)）、Erlang、Clojure 都是這場倡議的受益者。連指令式語言也被收編——Java 8（2014）、C++（[1983-Cplusplus.md](1983-Cplusplus.md)）20、Python（[1991-Python.md](1991-Python.md)）全都加入了 `map`、`filter`、lambda 運算式。
- **純度理論**：Backus 對「賦值產生隱藏時序」的批判，直接催生了「純函數」與「副作用」的概念體系，最終由 Haskell 的 Monad（見 [1990-Haskell.md](1990-Haskell.md)）理論化。
- **程式代數**：組合子邏輯影響了 Point-free 風格、Kay 的訊息組合（[1980-Smalltalk.md](1980-Smalltalk.md)）、以及現代的函數組合函式庫。

Backus 用圖靈獎演講完成了程式語言史上最著名的一次「自我否定」，並為下一個四十年指出了方向。

## 證據與工具

Haskell 示範——Backus 的內積，point-free 風格：

```haskell
-- 組合子風格：無變數、無賦值
innerproduct :: Num a => ([a], [a]) -> a
innerproduct = sum . uncurry (zipWith (*))

main = print (innerproduct ([1,2,3], [4,5,6]))  -- 32
```

用 Python 模擬 FP 系統的組合子與代數律：

```python
compose = lambda f, g: lambda x: f(g(x))
construct = lambda *fs: lambda x: tuple(f(x) for f in fs)
# FP 內積：/+ ∘ (α ×) ∘ transpose
transpose = lambda p: list(zip(*p))
alpha_mult = lambda m: [p[0] * p[1] for p in m]
reduce_add = lambda xs: sum(xs)

ip = compose(reduce_add, compose(alpha_mult, transpose))
print(ip(([1,2,3], [4,5,6])))   # 32

# 驗證結合律: (f ∘ g) ∘ h == f ∘ (g ∘ h)
f = lambda x: x + 1
g = lambda x: x * 2
h = lambda x: x - 3
assert compose(compose(f, g), h)(10) == compose(f, compose(g, h))(10)
print("代數律成立")
```
