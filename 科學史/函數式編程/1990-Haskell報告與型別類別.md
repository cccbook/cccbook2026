# 1990-Haskell報告與型別類別

## 案件摘要

1990 年，《Haskell 1.0 報告》由 Paul Hudak、Simon Peyton Jones、Philip Wadler 等人編纂完成，正式以數學報告定義了這門語言。報告的兩大支柱：type class（源自 Wadler 與 Stephen Blott 1989 年的論文 "How to make ad-hoc polymorphism less ad hoc"）與日後加入的 monadic I/O。後者的理論由 Eugenio Moggi（1991）以範疇論奠定，Wadler（1992、1995）將其推廣到函數式編程社群。1997 年 Haskell 98 整合一切成為穩定標準。本案的謎題是：一門「純潔」到連賦值都沒有的語言，要如何在違反純潔性的嫌疑下印出 Hello World？

## 前因 -- 為什麼會有這個案子

- 委員會成立後的整合工作：Miranda、SASL、Hope、Orwell 等語言的優點需要熔於一爐，報告是唯一的裁判。
- 純函數式語言的「副作用難題」：引用透明要求 $e \equiv v$，但 `print` 的本質就是改變外部世界——程式要嘛無法印出 Hello World，要嘛違反純潔性。
- Overloading 與 Hindley-Milner 的矛盾：`(==)`、`(+)` 在不同型別上語義不同，HM 的單態推論無法容納，需要 Wadler-Blott 的 type class 補強。
- I/O 的舊方案（stream-based I/O、continuation-passing）在真實程式上難以組合，需要更強的抽象。

## 線索與推理 -- 數學式、程式、理論

### 線索一：type class 與字典傳遞

Type class 在語言層面是 class/instance，在編譯層面是 dictionary-passing translation：每個約束 $\texttt{Eq}\,a$ 被編譯成一個「字典」參數——一個記錄該型別所有類別方法的值。

$$\texttt{(==)} :: \forall a.\, \texttt{Eq}\, a \Rightarrow a \to a \to \texttt{Bool}$$

編譯後變成：

$$\texttt{eqDict} : \forall a.\, \texttt{Eq}\, a \to \{ \texttt{eq} : a \to a \to \texttt{Bool} \}$$

```haskell
class Eq a where
  (==) :: a -> a -> Bool

instance Eq Bool where
  True  == True  = True
  False == False = True
  _     == _     = False
```

呼叫 `x == y` 時，編譯器靜態解析 $a$ 的型別，傳入對應的 `Eq Bool` 字典：

```haskell
-- 編譯器眼中的形式（示意）：
-- eq @Bool eqDictBool x y
elem :: Eq a => a -> [a] -> Bool
elem _ []       = False
elem x (y:ys)   = x == y || elem x ys
-- 遞迴呼叫把字典沿呼叫鏈傳遞：eq @a dict x y
```

字典傳遞保證：overloading 在編譯期完全解析，執行期零型別資訊開銷。

### 線索二：Moggi 的 monad 理論

Moggi（1991）的關鍵洞察：計算（computation）與值（value）是兩個範疇。一個 monad 是範疇論上的三元組 $(T, \eta, \mu)$，作用在範疇 $\mathcal{C}$ 上：

- 單位 $\eta : \text{Id} \Rightarrow T$——把值包裝成計算；
- 乘法 $\mu : T^2 \Rightarrow T$——把「計算的計算」壓平成計算；
- 滿足結合律與單位律：$\mu \circ T\eta = \mu \circ \eta T = \text{id}$，$\mu \circ T\mu = \mu \circ \mu T$。

Kleisli 延伸（即 bind）是程式設計師實際使用的操作：

$$\text{bind} : T\,a \to (a \to T\,b) \to T\,b$$

在 Haskell 中即 `(>>=) :: m a -> (a -> m b) -> m b`。

### 線索三：Wadler 的推廣與 IO 語義

Wadler 在 "Monads for functional programming"（1995）中指出：I/O、可變狀態、例外、非確定性都是 monad。Haskell 的 `IO a` 的語義是關鍵破案證詞：**一個 `IO a` 值是「動作的描述」而非「執行動作」**。純函數返回動作描述，動作的執行只在最頂層由執行期系統完成：

```haskell
main :: IO ()
main = do
  putStrLn "Hello, World!"
  name <- getLine
  putStrLn ("Hello, " ++ name ++ "!")
```

`do` 記法是 bind 的語法糖，脫糖後：

```haskell
main = putStrLn "Hello, World!" >>= \_ ->
       getLine >>= \name ->
       putStrLn ("Hello, " ++ name ++ "!")
```

純潔性無恙：`main` 本身是純的（一個不變的描述值），世界只在 `main` 被執行時才改變——副作用被隔離在 `IO` 容器內。

### 線索四：Maybe monad 與鏈式運算

另一條佐證：用 Maybe monad 處理可能失敗的計算鏈，替代繁瑣的巢狀判空：

```haskell
lookupUser :: Int -> Maybe String
lookupAge  :: String -> Maybe Int

profile :: Int -> Maybe Int
profile uid = do
  name <- lookupUser uid   -- 中途 Nothing 則整條鏈短路為 Nothing
  age  <- lookupAge name
  return age               -- 即 η：把值包回 Maybe
```

用 Python 模擬 Maybe monad 與 bind 鏈：

```python
class Maybe:
    def bind(self, f): raise NotImplementedError

class Nothing(Maybe):
    def bind(self, f): return self
    def __repr__(self): return "Nothing"

class Just(Maybe):
    def __init__(self, value): self.value = value
    def bind(self, f): return f(self.value)   # μ 與 η 的合成
    def __repr__(self): return f"Just {self.value!r}"

def just(x): return Just(x)

def lookup_user(uid): return just("Ada") if uid == 1 else Nothing()
def lookup_age(name): return just(36) if name == "Ada" else Nothing()

profile = lookup_user(1).bind(lambda name:
          lookup_age(name).bind(lambda age:
          just(age)))
print(profile)   # Just 36
print(lookup_user(2).bind(lookup_age))  # Nothing，鏈自動短路
```

### 破案時刻

1997 年 Haskell 98 報告發布：type class 與 monadic I/O 一併納入標準。「純函數式無法做 I/O」的指控不成立——副作用被 monad 容器馴服，而且 GHC 的 rewrite rules 與嚴格性分析證明惰性程式可以跟 C 一樣快。

## 結案 -- 後果與影響

- Monad 成為函數式編程的「副作用容器」標準，影響 F# computation expression、Scala、Rust 的 Result/Option、以及 async/await 的理論基礎。
- Haskell 98 成為大學教材標準，此後十年教學與可移植程式的共同基準。
- GHC 的 rewrite rules 與 strictness analysis 證明惰性語言可以達到 C 級效能，終結「函數式必慢」的偏見。
- Moggi 的計算範疇論成為 PL 理論的顯學，effect systems、algebraic effects 都是它的後裔。
- Type class 的 dictionary-passing 進入主流：Rust trait、Scala implicits、Swift protocol conformance 都是同一思想的變體。

## 關鍵人物與文獻

- Paul Hudak（耶魯）— Haskell 1.0 報告主編。
- Simon Peyton Jones（Glasgow）— GHC 與報告核心，STG 與最佳化技術推手。
- Philip Wadler — type class 與 monadic I/O 的推廣者。
- Stephen Blott — type class 論文共同作者。
- Eugenio Moggi（熱那亞）— monad 理論的範疇論奠基者。
- 文獻：
  - Hudak, P., Peyton Jones, S., Wadler, P., et al. (1990). "Report on the Programming Language Haskell, Version 1.0." Yale University / Glasgow University technical report.
  - Wadler, P., & Blott, S. (1989). "How to Make Ad-Hoc Polymorphism Less Ad Hoc." *POPL '89*, 60–76.
  - Moggi, E. (1991). "Notions of Computation and Monads." *Information and Computation*, 93(1), 55–92.
  - Wadler, P. (1992). "Comprehending Monads." *Mathematical Structures in Computer Science*, 2(4), 461–492.
  - Wadler, P. (1995). "Monads for Functional Programming." *Advanced Functional Programming*, LNCS 925, Springer, 24–52.
  - Peyton Jones, S. (1992). "Implementing Lazy Functional Languages on Stock Hardware: The Spineless Tagless G-machine." *Journal of Functional Programming*, 2(2), 127–202.
  - Haskell Committee (1997). *Haskell 98: A Non-strict, Purely Functional Language.* Report.
