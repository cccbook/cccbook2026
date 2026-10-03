# 1986-StandardML報告

## 案件摘要

1980 年代中期，函數式程式設計的世界出現了一樁「方言叢生」的懸案：1973 年誕生於 Edinburgh LCF 專案的 ML 語言，在各機構衍生出 Edinburgh ML、Poly/ML 等互不相容的版本，程式無法移植。偵探 Robin Milner 於 1984 年提出標準化倡議，並在 1986 年與 Tofte、Harper 聯手完成《The Definition of Standard ML》報告（1990 年正式出版），將 ML 重建為有精確數學定義的主流語言。本案不只是「整理方言」，更開創了兩項偵探技術：以型別推論規則定義靜態語義、以抽象機器定義動態語義——第一個完整做到的主流語言。

## 前因 -- 為什麼會有這個案子

- 1973 年的 ML 原本是 LCF 定理證明器的內部元語言（meta-language），設計時從未考慮成為通用程式語言。
- ML 隨 LCF 散布到各研究機構後，方言快速分化：Edinburgh ML、Poly/ML 各自修改語法與語義，同一份程式在不同實作上無法執行。
- 學界與業界需要一個可移植、有正式規格的標準，否則函數式程式設計永遠只是「實驗室玩具」。
- 同時期的 Hope 語言帶來了代數資料型別（algebraic data type, ADT）與例外（exception）機制，這些好線索需要被整合進標準。
- Milner 的型別推論（Hindley-Milner, 1978）已在 ML 中實現，但「多型 + 可變參照」的組合被發現會導致型別系統不健全，需要一個正式的修補方案。

## 線索與推理 -- 數學式、程式、理論

### 線索一：模組層次的「函數應用」-- signature 與 functor

Standard ML 最原創的偵探技術，是把「函數抽象」提升到模組層次。signature 是模組的介面（型別規格），functor 則是「吃進一個結構、吐出另一個結構」的參數化模組——本質上是模組層次的函數應用：

$$
\text{signature } S = \text{sig } \text{spec} \text{ end} \qquad
\text{functor } F(X : S) : S' = \text{struct} \ldots \text{end}
$$

型別規則上，functor 應用類似項層次的 lambda 應用：

$$
\frac{\Gamma \vdash F : (S, S')\text{-functor} \quad \Gamma \vdash \text{struct} \ldots \text{end} \rhd X : S}
     {\Gamma \vdash F(\text{struct} \ldots \text{end}) : S'}
$$

### 線索二：靜態語義用推論規則、動態語義用抽象機器

《The Definition of Standard ML》是第一個用「兩套數學機器」完整定義語言的正式報告。靜態語義以自然演繹風格的型別規則書寫，例如函數應用：

$$
\frac{\Gamma \vdash e_1 : \tau \to \sigma \quad \Gamma \vdash e_2 : \tau}
     {\Gamma \vdash e_1 \; e_2 : \sigma}
$$

動態語義則定義一個抽象機器，以「狀態轉移」描述求值：

$$
(\text{state}) \mapsto (\text{state}')
$$

表達式 $e$ 求值為值 $v$ 寫作 $s, e \Rightarrow s', v$。這套寫法成為之後所有語言規格的教科書典範。

### 線索三：value restriction -- 可變參照下的多型危機

若允許含副作用的表達式自由獲得多型，會出現型別不健全：

$$
\text{let } r = \text{ref } [] \text{ in } r := [1]; \; \text{length}(r) \; \text{(* 期望 [] 卻是 [1] *)}
$$

Milner 的破案關鍵：只有「語法上確定為值」的表達式（value restriction）才能一般化（generalize）為多型 schema：

$$
\frac{\Gamma \vdash e : \tau \quad e \text{ 是 value}}{\Gamma \vdash \text{let } x = e \text{ in } \ldots : \forall \alpha.\, \tau}
$$

### 可執行程式碼：SML 的 signature、functor 與 pattern matching

```sml
(* signature：介面 *)
signature ORDERED = sig
  type t
  val compare : t * t -> order
end

(* functor：參數化模組，模組層次的函數應用 *)
functor MakeSet (O : ORDERED) = struct
  datatype set = Empty | Node of set * O.t * set

  fun insert (Empty, x) = Node (Empty, x, Empty)
    | insert (Node (l, y, r), x) =
        case O.compare (x, y) of
          LESS    => Node (insert (l, x), y, r)
        | GREATER => Node (l, y, insert (r, x))
        | EQUAL   => Node (l, y, r)

  fun member (Empty, _) = false
    | member (Node (l, y, r), x) =
        case O.compare (x, y) of
          LESS    => member (l, x)
        | GREATER => member (r, x)
        | EQUAL   => true
end

(* 套用 functor 到具體結構 *)
structure IntSet = MakeSet (struct
  type t = int
  val compare = Int.compare
end)

val s = IntSet.insert (IntSet.insert (IntSet.Empty, 3), 5)
val _ = print (Bool.toString (IntSet.member (s, 5)) ^ "\n")  (* true *)
```

### Python 模擬：functor 的參數化概念

```python
from typing import Protocol, TypeVar, Generic

class Ordered(Protocol):
    def compare(self, other) -> int: ...

T = TypeVar("T")

class MakeSet(Generic[T]):
    """模擬 functor：吃進一個帶 compare 的結構，吐出集合模組"""
    def __init__(self, cmp):
        self.cmp = cmp
        self.items = []

    def insert(self, x):
        if not self.member(x):
            self.items.append(x)
            self.items.sort(key=self.cmp)

    def member(self, x):
        import bisect
        i = bisect.bisect_left(self.items, x, key=self.cmp)
        return i < len(self.items) and self.items[i] == x

IntSet = MakeSet(cmp=lambda v: v)   # functor 應用
IntSet.insert(3); IntSet.insert(5)
print(IntSet.member(5))             # True
```

## 結案 -- 後果與影響

- SML/NJ（Standard ML of New Jersey，Appel 團隊，1990 年代）成為編譯器與 GC 研究的標準平台。
- OCaml（1996）的模組系統（signature、functor）直接源自 Standard ML 的設計。
- 以推論規則定義靜態語義、以抽象機器定義動態語義的寫法，成為語言規格的教科書典範：Haskell 98 Report、Scala 規格皆效法此模式。
- value restriction 成為所有 HM 型別系統語言（SML、OCaml、F#）處理可變狀態的標準答案。
- datatype + pattern matching 的正式語義，確立了 ADT 成為函數式語言的必備配備。
- 本案證明：一門語言可以像數學定理一樣被完整定義，語言設計從此有了「可驗證的規格文化」。

## 關鍵人物與文獻

- Robin Milner：型別推論（Hindley-Milner）作者、LCF 與 ML 的催生者，1991 年圖靈獎得主。
- Mads Tofte、Robert Harper：Standard ML 語義定義的共同作者，後續皆成為型別理論與語義學的重要學者。
- Robin Milner, Mads Tofte, Robert Harper, "The Definition of Standard ML", MIT Press, 1990.
- Robin Milner, "A Theory of Type Polymorphism in Programming", Journal of Computer and System Systems, 17(3), 1978.
- Robin Milner, "The Standard ML Core Language", Polymorphism, 2(2), 1985（1984 年提出的標準化草案）.
- Luca Cardelli, "A semantics of multiple inheritance", 1984（Hope/ADT 語義的相關基礎）.
- Andrew W. Appel, David B. MacQueen, "Standard ML of New Jersey", Third International Symposium on Programming Language Implementation and Logic Programming, 1991.
