# 1990 — Haskell 誕生

## 案件摘要
1990 年，一個國際委員會發表了 Haskell 1.0——第一個標準化的純函數式程式語言，以邏輯學家 Haskell Curry 命名。λ 演算從此不只在教科書裡，而成為可以寫出作業系統、編譯器、Web 服務的實戰語言。惰性求值、typeclass、monad——三個來自 λ 演算與範疇論的武器，全部被收編。

## 前因 -- 為什麼會有這個案子
- **語言戰國時代**：1980 年代純函數式語言群雄並起——David Turner 的 **Miranda**（1985，惰性求值）、Milner 的 **ML**（1978，多型型別推論）、SASL、Hope……每個都有不同的語法與語義，教學與研究無所適從。
- **Miranda 的商業封鎖**：Miranda 是 Turner 公司的專利軟體，大學無法自由使用——委員會需要一個**開放、免費**的標準語言。
- **命名懸案**：Curry 的組合子邏輯（Curry–Howard 對應的來源）直接影響了函數式語言的理論基礎，委員會以 Curry 命名以致敬；Miranda 的英國血統則被一個「國際」委員會取代。
- **Fergus Henderson 等委員會**：1990 年版由 Paul Hudak、Philip Wadler、John Hughes、Simon Peyton Jones 等人共同設計——**委員會設計**是 Haskell 的獨特血統，之後每個版本（1998、2010）都經由委員會協商。

## 線索與推理 -- 數學式、程式、理論

### 惰性求值（call-by-need）
λ 演算有兩種求值策略：
- **急切求值（call-by-value）**：先求值參數再應用 $(\lambda x.\,M)\,N \to (\lambda x.\,M)\,V \to M[V/x]$
- **惰性求值（call-by-need）**：不先求值參數，直到真的需要時才求值一次（以 thunk 快取）：

  $$(\lambda x.\,M)\,N \to M[N/x] \text{（N 以未求值的形式傳遞）}$$

Church–Rosser 定理保證：**兩種策略最終結果相同**（若都停機）。但惰性求值可以處理無限資料結構：

```haskell
-- 無限串列：只有惰性求值才能定義！
ones     = 1 : ones                    -- 無限個 1
nats     = 0 : map (+1) nats           -- 無限自然數
fibs     = 0 : 1 : zipWith (+) fibs (tail fibs)  -- 無限費氏數列
take 10 fibs  -- [0,1,1,2,3,5,8,13,21,34]
```

### typeclass（型別類）
Haskell 的 typeclass 是 **System F 多型的推廣**——對型別做「條件約束」：

$$\frac{\text{型別 } a \text{ 必須屬於類 } Eq}{\text{函數 } (==) :: a \to a \to Bool \text{ 可以用於 } a}$$

```haskell
class Eq a where
  (==) :: a -> a -> Bool

-- 定義：對所有屬於 Ord 的型別 a，可以排序
sort :: Ord a => [a] -> [a]
```

這在 λ 演算的型別系統中對應 **受限量詞（bounded quantification）** $\forall a <: Eq.\, [a] \to \ldots$——System F 的推廣（Cardelli-Wegner 1985）。

### Monad（Wadler 1992 引入）
Haskell 是**純函數式**語言——沒有副作用。但列印、狀態、例外、I/O 都需要副作用！Philip Wadler 於 1992 年將範疇論的 **monad** 引入 Haskell，以「型別化副作用」解決這個懸案：

Monad 的三個操作（Kleisli triple，對應範疇論的 monad）：

```haskell
return :: a -> m a              -- 單位（unit）
(>>=)  :: m a -> (a -> m b) -> m b  -- 綁定（bind / Kleisli extension）
```

Monad 三定律（對應範疇論的結合律與單位律）：

```haskell
return a >>= f   ==  f a           -- left identity
m >>= return     ==  m             -- right identity
(m >>= f) >>= g  ==  m >>= (\x -> f x >>= g)  -- associativity
```

**關鍵推理**：副作用被「封裝」在 monad 型別中——`IO a` 表示「會產生型別為 `a` 的結果的動作」，型別系統強制所有副作用被明確標記。這在 λ 演算中對應 **Moggi 的 monadic metalanguage（1989）** $\lambda_{ml}$：計算型 $T A$ 與值型 $A$ 的分離。

### 一個 Haskell 範例（含 lambda 與 monad）
```haskell
-- λ 演算：匿名函數（Haskell 的 \ 就來自 λ！）
double = \x -> x * 2          -- λx. 2x
add    = \x y -> x + y        -- λx.λy. x+y（Curry 化）

-- 高階函數：map/filter/reduce（foldr）
-- map     : (a -> b) -> [a] -> [b]
-- filter  : (a -> Bool) -> [a] -> [a]
-- foldr   : (a -> b -> b) -> b -> [a] -> b
sumOfSquares = foldr (\x acc -> x*x + acc) 0 . filter even

-- Monad：I/O 與 lambda 的結合
main :: IO ()
main = do
  let xs = map double [1..5]           -- [2,4,6,8,10]
  mapM_ (\x -> putStrLn ("x = " ++ show x)) xs  -- monad 中用 lambda
```

`foldr` 直接對應 λ 演算的自然數歸納原理（Church numeral 的推廣）：

$$\mathsf{foldr}\,f\,z\,[x_1,\ldots,x_n] = f\,x_1\,(f\,x_2\,(\cdots(f\,x_n\,z)))$$

### Haskell 2010 / 2020 標準
- **Haskell 98**（1999）：第一個穩定標準，教科書的基礎。
- **Haskell 2010**（2010）：加入 Foreign Function Interface、修正 semicolon 規則——最後一個官方標準。
- **Haskell 2020**：社群倡議（未正式發布），納入 GHC 擴充（如 `LambdaCase`、`NumericUnderscores`）。
- 實務上，**GHC（Glasgow Haskell Compiler）** 的擴充（type families、GADTs、rank-N types）已成為事實標準。

## 結案 -- 後果與影響
- **純函數式成為主流選項**：Haskell 是第一個大規模使用的惰性純函數式語言，影響了 Scala、F#、Swift、Kotlin 的函數式特性。
- **monad 成為通用模式**：Wadler 的 monad 影響了整個函數式程式設計——甚至 JavaScript 的 Promise、Java 的 Optional 都是 monad 的變體。**「monad 是自函子（endofunctor）範疇上的幺半群」**——來自 Mac Lane 的範疇論，成為程式設計師的必修知識。
- **typeclass 影響了 Rust trait、Scala implicit**。
- **惰性求值的雙面性**：Haskell 證明了惰性求值的可行性，但也暴露了空間洩漏問題——嚴格求值（如 OCaml）在效能上反而更受歡迎。
- **工業應用**：Meta 的 Sigma 反詐欺系統、金融高頻交易、編譯器（Idris、Agda 都以 Haskell 寫成）。
- **後續**：Haskell 是 λ 演算與範疇論結合的最大實驗場——「Category Theory for Programmers」（Bartosz Milewski）等教材以此為基礎。

## 關鍵人物與文獻
- **Haskell Curry**：組合子邏輯之父，Curry–Howard 對應的來源。
- **Paul Hudak、Philip Wadler、John Hughes、Simon Peyton Jones**：Haskell 委員會核心成員。
- 文獻：
  - Hudak, P., et al. (1990). *Report on the Programming Language Haskell* (Yale Report).
  - Wadler, P. (1992). *Monads for Functional Programming* (Bast van Eck lecture).
  - Wadler, P., Blott, S. (1989). *How to make ad-hoc polymorphism less ad hoc* (typeclass 的起源).
  - Peyton Jones, S. (2003). *Haskell 98 Language and Libraries: The Revised Report*.
  - Marlow, S. (2010). *Haskell 2010 Language Report*.
