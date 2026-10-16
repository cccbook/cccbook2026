# 1987-Haskell誕生會議

## 案件摘要

1987 年 9 月，在奧勒岡州波特蘭舉行的 FPCA（Functional Programming Languages and Computer Architecture）會議上，Paul Hudak、Philip Wadler、John Hughes、Simon Peyton Jones 等二十餘位研究者做成一項重大決議：成立一個開放的語言設計委員會，統一當時惰性函數式語言的碎片化亂象。會中列舉的「嫌疑犯」包括 Miranda、SASL、KRC、Hope、Id、Orwell 等。委員會決定以邏輯學家 Haskell Curry 為新語言命名，並於 1988 年召開首次委員會會議。本案的核心謎題是：為什麼學界需要一個「委員會設計」的開放標準語言，而不是任由最好的私有實作勝出？

## 前因 -- 為什麼會有這個案子

- 1980 年代末，惰性函數式語言嚴重碎片化：教學用 Miranda/KRC、平行研究用 Id、英國學派用 Orwell/Hope，各自為政。
- 碎片化的直接代價：教材、程式庫、研究成果無法移植；一門課的程式在另一所大學的語言上完全跑不起來。
- Miranda 雖然最流行，卻是 Turner 的 Research Software Ltd 的商業軟體，授權費與封閉原始碼使其難以成為公共標準；Turner 明確表示不願開放。
- 學界需要一個「開放標準」的非嚴格、純函數式語言：任何人可自由實作，語義以報告（report）定義。
- FPCA 會議上的共識：與其再添一個新方言，不如設計一個能整合現有優點的語言。

## 線索與推理 -- 數學式、程式、理論

### 線索一：設計原則的辯論

委員會面對的第一組證詞是「純度」之爭：

- **純函數（purity）vs 副作用**：純函數式陣營（Hudak、Wadler）主張表達式無副作用，才能保證引用透明（referential transparency）與等式推理：
  $$e \Downarrow v \implies e \equiv v$$
  任何地方都可以把表達式替換為其值，程式正確性可用代數變換證明。
- **非嚴格（non-strict）vs 嚴格**：另一組證詞關乎求值順序。委員會投票決定跟隨 Miranda 的非嚴格傳統（call-by-need），因為它允許無窮結構與模組化解耦；反對者（如 Peyton Jones 早期）擔心非嚴格使效能難以掌控——這場辯論在後續十年持續發酵。

### 線索二：type class 的誕生

第二個謎題：Hindley-Milner 型別系統優雅但無法表達 overloading（ad-hoc polymorphism）。例如 `(==)` 在 Int、Bool、字串上的實作不同，HM 只能給它一個單一型別，導致要嘛禁止重載、要嘛型別錯誤。

Wadler 與 Stephen Blott 的破案提案（1989）：在型別上附加「約束」（constraint），即 type class：

$$\texttt{(==)} :: \forall a.\, \texttt{Eq}\, a \Rightarrow a \to a \to \texttt{Bool}$$

讀作：對任意型別 $a$，只要 $a$ 屬於 $\texttt{Eq}$ 類別，`(==)` 的型別就是 $a \to a \to \texttt{Bool}$。約束 $\texttt{Eq}\,a$ 是型別層級的邏輯前提，解決了 overloading 與 HM 的矛盾，同時保持型別推論的自動化。

### 線索三：為什麼 HM 單獨不夠——程式示範

```haskell
class Eq a where
  (==) :: a -> a -> Bool

instance Eq Bool where
  True  == True  = True
  False == False = True
  _     == _     = False

instance Eq [a] => Eq [a] where  -- 概念示意：遞迴結構的重載
  instance 實作逐一比較元素
```

若沒有 type class，嘗試用 HM 寫泛型相等會失敗：

```haskell
-- 純 HM：只能假設 a 上有一個全域 ==，但 HM 根本沒有這個假設
-- elem :: a -> [a] -> Bool   -- 錯誤：沒有 Eq a 約束，無從呼叫 (==)
elem :: Eq a => a -> [a] -> Bool   -- 正確：帶約束的版本
elem _ [] = False
elem x (y:ys) = x == y || elem x ys
```

沒有約束時，`elem` 的型別參數 $a$ 上沒有任何操作可用——這正是委員會要解決的核心難題。

### 線索四：語言設計作為「委員會數學」

委員會的方法論本身就是一條線索：語言不用實作（implementation）定義，而用報告（report）定義——語義以數學規則書寫，任何人都可以做出符合報告的編譯器。這是數學公理化的作法：先有公理（report），後有定理（實作）。命名致敬 Haskell Curry，因為 Curry 的組合子邏輯正是函數式編程的理論根基：

$$\texttt{S}fgx = fx(gx), \qquad \texttt{K}xy = x$$

### 破案時刻

1988 年首次委員會會議（耶魯大學）確認設計原則：非嚴格、純函數式、完整的 HM 加 type class。1990 年 Haskell 1.0 報告問世，碎片化亂象開始收束。

## 結案 -- 後果與影響

- 1990 年發表 Haskell 1.0；1997 年 Haskell 98 成為穩定標準，此後長期是教學與可移植程式的基準。
- GHC（1992 年起）成為世界上最強的最佳化編譯器之一，證明非嚴格語言可以有高效能。
- Haskell 成為函數式研究的孵化器：monad、STM、arrow、GADT、type family 等重大概念都在此孵化後擴散到主流語言。
- type class 的構想進入 Scala（implicits/typeclass 模式）、Rust（trait）、Swift（protocol），成為表達 ad-hoc polymorphism 的通用設計。
- 「以報告定義語言」的模式被後續多個語言標準化程序（如 Standard ML、Scheme RnRS）沿用。

## 關鍵人物與文獻

- Paul Hudak（耶魯）— 委員會主席之一，Haskell 1.0 報告主編。
- Philip Wadler（格拉斯哥）— type class 提案人，設計哲學主導者。
- John Hughes（Chalmers）— 〈Why Functional Programming Matters〉作者，設計辯論核心。
- Simon Peyton Jones（UCL/Glasgow）— GHC 實作主導者。
- David Turner — Miranda 的開放性爭議當事人，其語法成為 Haskell 藍本。
- 文獻：
  - Hudak, P., Peyton Jones, S., Wadler, P., et al. (1990). "Report on the Programming Language Haskell, Version 1.0." Yale University / Glasgow University technical report.
  - Wadler, P., & Blott, S. (1989). "How to Make Ad-Hoc Polymorphism Less Ad Hoc." *Proceedings of the 16th ACM Symposium on Principles of Programming Languages (POPL)*, 60–76.
  - Hudak, P., & Fasel, J. (1992). "A Gentle Introduction to Haskell." *ACM SIGPLAN Notices*, 27(5).
  - Turner, D. A. (1985). "Miranda: A Non-Strict Functional Language with Polymorphic Types." *FPCA*, LNCS 201, Springer, 1–16.
  - Peyton Jones, S. (1987). *The Implementation of Functional Programming Languages.* Prentice Hall.
