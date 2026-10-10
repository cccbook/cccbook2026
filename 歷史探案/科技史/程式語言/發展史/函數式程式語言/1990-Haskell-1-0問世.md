# 1990：Haskell 1.0 問世

## 事件
1990 年，由耶魯、格拉斯哥等學界合力設計的 **Haskell 1.0** 正式問世——第一門開放標準的**純函數式、惰性求值、靜態型別**語言。名稱紀念邏輯學家 **Haskell Curry**（組合子邏輯的奠基者）。首版報告由 Paul Hudak、Philip Wadler、John Hughes 等人主導撰寫，兌現了 [1987-Haskell構想會議](1987-Haskell構想會議.md) 統一惰性方言的承諾。

## 語法/特性加入的理論與實用原因
### 1. 型別類（type classes）
- **理論原因**：**Philip Wadler 與 Stephen Blott** 在 1989 年的論文〈How to make ad-hoc polymorphism less ad hoc〉中提出型別類——以「介面的受約束多型」（constrained polymorphism）解決 ad-hoc 多型的理論問題：如何讓 `Eq`、`Ord`、`Num` 等運算在**無副作用的靜態型別語言**中重載，同時保持型別推斷的可決定性（decidability）。這是 **Haskell 對 ML 最大的語法創新**。
- **實用原因**：沒有型別類，`==` 只能對單一型別使用，或得像 SML 用 functor 包一層模組；型別類讓泛型程式直接以約束撰寫。
- **彌補缺陷**：Miranda 只能靠內建重載、SML 只能靠模組系統表達 ad-hoc 多型。

```haskell
class Eq a where
  (==) :: a -> a -> Bool

member :: Eq a => a -> [a] -> Bool   -- 受約束的多型
member _ [] = False
member x (y:ys) = x == y || member x ys
```

有了 type class，還能為自訂型別宣告 instance——這是 Miranda 做不到的：

```haskell
data Point = Point Int Int

instance Eq Point where
  Point x1 y1 == Point x2 y2 = (x1 == x2) && (y1 == y2)

member (Point 1 2) [Point 1 2, Point 3 4]   -- → True，member 完全不用改
```

對照沒有 type class 的世界：`==` 只能對單一型別，同一個「判斷成員」邏輯得為每種型別寫一份：

```haskell
-- 沒有 type class：ad-hoc 多型只能靠「多份同構函數」
elemInt    :: Int -> [Int] -> Bool
elemInt x (y:ys) = x == y || elemInt x ys

elemChar   :: Char -> [Char] -> Bool
elemChar x (y:ys) = x == y || elemChar x ys
-- 每新增一種型別就再複製一份——type class 把它們統一成單一 member
```

### 2. 惰性求值
- **理論原因**：繼承自 [1985-Miranda誕生](1985-Miranda誕生.md) 的 call-by-need 策略，奠基於 Church–Rosser 合流性——非嚴格求值保證結果唯一。
- **實用原因**：無窮資料結構與模組化組合（生成器、過濾器、取值分離）成為 Haskell 的慣用法。
- **彌補缺陷**：急切語言無法自然表達 `primes = sieve [2..]` 這類無窮定義。

惰性求值下的無窮列表與模組化組合：

```haskell
ones     = 1 : ones                          -- 自我參照的無窮列表
naturals = 0 : map succ naturals             -- 只在需要時展開
primes   = sieve [2..]
  where sieve (p:xs) = p : sieve [n | n <- xs, n `mod` p > 0]

take 5 primes      -- [2,3,5,7,11]，急切語言在此會無限遞迴
zip [1..] "abc"    -- [(1,'a'),(2,'b'),(3,'c')]，無窮配有限
```

### 3. 單子（monad）與 I/O
- **理論原因**：**1990–91 年，Eugenio Moggi** 提出以範疇論的單子（monad）為計算效果（effect）建模的理論，**Philip Wadler** 隨即將其引入程式語言設計。純函數式語言的難題是「如何在無副作用的世界裡做 I/O」——單子把 I/O 這類效果封裝在 `IO a` 型別中，使純函數與效果程式在型別層級**明確分離**。Haskell 自 **1.3** 版起正式以 IO monad 處理 I/O，取代早期的 stream-based I/O。
- **實用原因**：`do` 記法讓命令式風格的程式碼能在純函數式框架下撰寫。
- **彌補缺陷**：Haskell 1.0 的 stream I/O 難以組合互動式程式；Miranda 根本沒有正規的 I/O 模型。

```haskell
main :: IO ()
main = do
  name <- getLine
  putStrLn ("Hello, " ++ name)
-- 效果被型別系統隔離：main 是 IO ()，其餘世界仍是純的
```

`do` 記法只是 monad 運算的語法糖——串接多個 I/O 動作、並把結果「帶出」單子：

```haskell
main :: IO ()
main = do
  line1 <- getLine
  line2 <- getLine
  putStrLn ("你輸入了：" ++ line1 ++ " 和 " ++ line2)
-- 等價於：getLine >>= \line1 -> getLine >>= \line2 -> putStrLn (...)
```

### 4. 純函數與打點排版
- **理論原因**：完全無副作用的純函數保證引用透明性，等式推理與程式變換可行；打點排版（offside rule）繼承自 Miranda。
- **實用原因**：教學與證明的簡潔性；語法與 Miranda 接近以利方言使用者遷移。
- **彌補缺陷**：SML/Scheme 的副作用破壞推理；LISP 的括號雜訊。

純函數與打點排版的簡例——定義體靠縮排分層，無需括號或 begin/end：

```haskell
factorial :: Int -> Int
factorial n = prod (down n)
  where
    down 0     = [0]                    -- where 子句同樣靠縮排分層
    down n     = n : down (n - 1)
    prod [0]   = 1
    prod (x:xs) = x * prod xs
```

## 彌補了什麼缺陷
Haskell 1.0 彌補了 **Miranda 的商業授權問題**（開放標準、任何人都可實作）與**惰性方言分裂**（統一 Miranda、SASL、KRC、LML 等十餘種方言）。其型別類與單子兩大理論創新，更反向影響了 Scala、Rust、Swift 等後世語言。後續發展見 [1998-Haskell-98標準化](1998-Haskell-98標準化.md)。

## 相關條目
- [1985-Miranda誕生](1985-Miranda誕生.md)
- [1987-Haskell構想會議](1987-Haskell構想會議.md)
- [1998-Haskell-98標準化](1998-Haskell-98標準化.md)
- [1983-StandardML誕生](1983-StandardML誕生.md)
