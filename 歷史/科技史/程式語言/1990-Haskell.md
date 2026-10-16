# 1990 Haskell 1.0 誕生：純函數式的集大成與 Monad 之謎

## 案發現場

1980 年代末，函數式程式設計百花齊放卻四分五裂：Lazy ML、Miranda、Hope、Orwell——每個學術團隊都有自己的惰性函數式語言。教學與研究產生了嚴重的碎片化問題：論文裡的語言學生學不到，學生的語言論文裡不存在。

1987 年在波特蘭的 FPCA 會議上，與會者決定成立委員會，設計一個**開放標準的純函數式語言**，把各家之長融於一體。委員會由 Paul Hudak、Philip Wadler、Simon Peyton Jones、John Hughes 等人組成，1990 年發表 Haskell 1.0。

未解之謎有兩個：

1. **純度之謎**：如果語言完全禁止副作用（無賦值、無 IO、無可變狀態），連「印出一行字」都做不到，這語言怎麼可能實用？
2. **ad-hoc 多型之謎**：ML（[1973-ML型別推導.md](1973-ML型別推導.md)）的參數多型無法處理「`+` 對 int 是加法、對 string 是串接」這種重載；但引入重載又會破壞型別推導。能否兼得？

這個問題為何重要？純函數式是 Backus（[1977-Backus函數式倡議.md](1977-Backus函數式倡議.md)）倡議的終極實現，但「無副作用」的承諾若無法與現實的 IO 調和，整個範式就是空中樓閣。

## 偵查過程

**第一步：惰性求值與純度。** Haskell 採用惰性求值（lazy evaluation）：運算式延遲到需要結果時才計算，且只算一次。這使無限資料結構成為可能：

```haskell
ones = 1 : ones                 -- 無限串列
nats = 0 : map (+1) nats        -- 無限自然數
take 5 nats                     -- [0,1,2,3,4]
```

關鍵推導：惰性求值 + 純度是**相互需要的**。若允許副作用，惰性求值的「何時算」變成不可預測的副作用時序，程式語義就崩潰了。純度使「定義即等式」成立——換序不改變語義，程式可以像數學一樣推理。這是對 Backus「賦值產生隱藏時序」批判的終極回應。

**第二步：型別類（typeclass）——ad-hoc 多型的理論化。** Wadler 與 Stephen Blott 在 1989 年提出型別類，解決重載與推導的兩難：

```haskell
class Eq a where
    (==) :: a -> a -> Bool

instance Eq Int where
    x == y = primEqInt x y

instance (Eq a) => Eq [a] where       -- 條件實例：遞迴推導
    [] == [] = True
    (x:xs) == (y:ys) = x == y && xs == ys
```

型別類的推導規則：函數宣告 $(==) :: a \to a \to Bool$ 中，$a$ 被約束為 `Eq a` 的成員，寫作：

$$\frac{Eq\ a \in \Gamma \quad \Gamma \vdash e : a \to a \to Bool}{\Gamma \vdash (==) : a \to a \to Bool}$$

這樣重載有了理論基礎（ad-hoc 多型），而型別推導依然可判定。型別類直接影響了 Rust 的 trait、Scala 的 implicit、Swift 的 protocol。

**第三步：Monad——副作用之謎的解答。** 1990 年代初，Eugenio Moggi 提出：可以用範疇論的 monad 來建模計算的「效果」。Wadler 將其引入 Haskell（1992），Peyton Jones 將其應用於 IO。核心推導：把「帶效果的計算」表示為型別 $M\ a$（如 $IO\ a$ 表示「會做 IO、最終產生 $a$」），並提供兩個運算子：

$$
return : a \to M\ a \qquad
(\gg=) : M\ a \to (a \to M\ b) \to M\ b
$$

 Monad 需滿足三條定律：

$$return\ a \gg= f = f\ a \qquad m \gg= return = m \qquad (m \gg= f) \gg= g = m \gg= (\lambda x. f\ x \gg= g)$$

關鍵洞察：**效果被關在型別 $M$ 的「盒子」裡**，純函數無法拆開盒子，只有 `>>=` 能串接帶效果的計算。於是「無副作用」與「能印字」同時成立：$IO\ String$ 是純的值（一個描述），執行它的是執行期系統。這是程式語言史上最精妙的一次理論調和。

## 結案報告

Haskell 的遺產：

- **語言系譜**：直接繼承 ML（[1973-ML型別推導.md](1973-ML型別推導.md)）與 Backus（[1977-Backus函數式倡議.md](1977-Backus函數式倡議.md)）的血統；GHC 成為最強的函數式編譯器。C# 的 LINQ、Java 8 的 `Optional`、Rust 的 `Option`/`Result`、Swift 的 `map`/`flatMap`，都是 Monad 思想的工業化。
- **型別類理論化**：Rust 的 trait 系統、Scala 的 typeclass 模式、Swift protocol，都源自 Haskell。
- **惰性與純度**：影響了 Python 的生成器、Clojure 的惰性序列；「純函數核心、效果邊緣」（Functional core, imperative shell）成為現代軟體架構的口號。
- **學術影響**：函數式反應式程式設計（FRP）、依值型別（Idris、Agda）、特效系統（Koka、Eff），皆以 Haskell 為實驗場。

Haskell 證明：**最激進的理論純度，也能長出最實用的工程實踐——只要找到正確的數學結構（Monad）。**

## 證據與工具

Haskell 示範——惰性、型別類與 Monad：

```haskell
-- 惰性求值
nats :: [Integer]
nats = 0 : map (+1) nats

-- 型別類
class Eq a where
  (==) :: a -> a -> Bool

-- Monad：把副作用關進 IO 盒子
main :: IO ()
main = do
  print (take 5 nats)             -- [0,1,2,3,4]
  name <- getLine                 -- >>= 串接帶效果的計算
  putStrLn ("Hello, " ++ name ++ "!")

-- State Monad 自己寫一個
newtype State s a = State { runState :: s -> (a, s) }
instance Functor (State s) where
  fmap f (State g) = State (\s -> let (a, s') = g s in (f a, s'))
```

用 Python 模擬惰性求值與 State Monad：

```python
from itertools import count, islice

# 惰性：無限自然數
nats = count(0)
print(list(islice(nats, 5)))   # [0, 1, 2, 3, 4]

# State Monad：效果（狀態）關在盒子裡
class State:
    def __init__(self, run): self.run = run

def return_(a): return State(lambda s: (a, s))

def bind(m, f):                 # >>= ：串接帶效果的計算
    def run(s):
        a, s2 = m.run(s)
        return f(a).run(s2)
    return State(run)

def get(): return State(lambda s: (s, s))
def put(s2): return State(lambda _: (None, s2))

# 計數器：效果被型別約束，純函數無法逃逸
prog = bind(get(), lambda n:
       bind(put(n + 1), lambda _:
       return_(n + 1)))
print(prog.run(10))   # (11, 11)——純函數式地處理了「可變狀態」
```
