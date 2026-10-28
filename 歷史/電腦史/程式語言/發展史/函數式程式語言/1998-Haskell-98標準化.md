# 1998：Haskell 98 標準化

## 事件
1998 年，以 Simon Peyton Jones 為主編的委員會發表 Haskell 98 語言標準。這是 Haskell 誕生（1990 年 Haskell 1.0，見 [1990-Haskell-1-0問世](1990-Haskell-1-0問世.md)）以來最重要的穩定化工程：委員會刻意將語言「凍結」成一個小而精的核心，作為教學、教科書與各編譯器實作的共同基礎。Haskell 98 之後，各編譯器（主要是 GHC）以「標準核心 + 方言擴展」的模式發展，這個模式沿用至今。

## 語法/特性加入的理論與實用原因

### 1. 語言凍結：穩定的小核心
- **理論原因**：Hindley–Milner 型別推論 + 惰性求值 + 單子式 IO，這個組合在理論上已足夠表達計算，不必再增加新機制；凍結可避免語意不定義清楚、各實作分歧。
- **實用原因**：教科書（如 2007 年的 Learn You a Haskell、Real World Haskell 的基礎章節）與課程需要一個不會每年改動的語言；移植性要求各編譯器（GHC、Hugs、nhc98）行為一致。
- **彌補缺陷**：Haskell 1.x 各版本（1.0 到 1.4）之間互不相容，委員會持續改版造成「版本漂移」，教材與程式碼迅速過時。

```haskell
-- Haskell 98 核心：型別類別、單子 IO、代數資料型別
data Tree a = Leaf | Node (Tree a) a (Tree a)

class Functor f where
  fmap :: (a -> b) -> f a -> f b

main :: IO ()
main = putStrLn "hello"
```

Haskell 98 的穩定核心語法總覽：函數定義（用模式匹配分分支）、type class 與 instance、do 記法的單子 IO，全部只用標準語言即可寫出完整程式：

```haskell
-- 函數定義：以模式匹配分支，與代數資料型別對應
data Shape = Circle Double | Rect Double Double

area :: Shape -> Double
area (Circle r) = pi * r * r
area (Rect w h) = w * h

-- type class instance：為自訂型別提供 == 的實作
instance Eq Shape where
  Circle a == Circle r = a == r
  Rect a b == Rect c d = a == c && b == d
  _        == _         = False

-- do 記法：單子 IO 的標準語法
main :: IO ()
main = do
  putStrLn "請輸入半徑："
  s <- getLine
  print (area (Circle (read s)))
```

這段程式完全不依賴編譯器擴展，在 Hugs、nhc98、GHC 皆可直接編譯執行——這正是「凍結核心」追求的可攜性：

```haskell
-- 一個 Haskell 98 可攜程式（不需任何 {-# LANGUAGE #-} 擴展）
-- Hugs:   hugs 98demo.hs
-- GHC:    runghc 98demo.hs
import Data.List (sort)

median :: Ord a => [a] -> Maybe a
median xs = case sort xs of
  [] -> Nothing
  ys -> Just (ys !! (length ys `div` 2))

main :: IO ()
main = print (median [3, 1, 4, 1, 5])
```

標準函式庫的高階函數是日常主力，`map`/`filter`/`foldr` 的串接構成函數式風格的基本樣貌：

```haskell
-- stdlib：map / filter / foldr 的組合
evens  = filter even [1..10]            -- [2,4,6,8,10]
squares = map (^2) evens                -- [4,16,36,64,100]
total  = foldr (+) 0 squares            -- 204

-- foldr 具良好代數性質，也是 GHC 融合轉換的理論基礎
myMap f = foldr (\x acc -> f x : acc) []
```

### 2. 型別類別與單子 IO 的標準化
- **理論原因**：Wadler 與 Blott 的型別類別（1989）解決了重載（overloading）在 HM 推論下的理論問題；單子（Moggi 1991、Wadler 1992）為命令式副作用提供了純函數式語意，兩者構成 Haskell 的理論基石，標準化使教科書有了固定主題。
- **實用原因**：IO 單子讓「純核心 + 邊界效應」的分離可以實際寫出有用的程式；型別類別讓 `==`、`+` 等運算子可以重載。
- **彌補缺陷**：1990 年代初各版本對重載與 IO 的處理不一（context 語法、流式 IO vs 單子 IO），標準化終止了這些分歧。

型別類別解決的重載問題，實際寫起來像這樣——`==` 與 `show` 對不同型別有不同實作，但由型別推論自動分派：

```haskell
-- 型別類別：Eq 與 Show 的重載由編譯器依型別自動選擇實作
class (Eq a, Show a) => Comparable a where
  compareDesc :: a -> String

-- 單子 IO 標準化後，所有實作的 IO 行為一致，
-- 教科書可以固定教 do 記法而不必討論各版差異
main :: IO ()
main = do
  print (1 == 1)        -- Eq Int
  print ("a" == "a")    -- Eq [Char]
  print (Just 3)        -- Show (Maybe Int)
```

### 3. 穩定核心 + 方言擴展的雙軌模式
- **理論原因**：將「教學核心」與「研究前沿」分離：核心保持簡單可教，擴展（GHC 的 GADTs、type families 等）承接新理論，兩者不互相拖累。
- **實用原因**：工程師可以選擇只用 Haskell 98 撰寫可攜程式，或開啟擴展使用進階功能。
- **彌補缺陷**：委員會設計的版本（每數年一次大改）使生態難以累積；雙軌模式讓核心穩定而前沿持續演進。

雙軌模式的實際寫法：同一份程式碼，僅在需要前沿功能時才開啟 GHC 擴展（如 2006 年的 GADTs），核心邏輯仍維持 Haskell 98：

```haskell
{-# LANGUAGE GADTs #-}   -- 僅此一行是 GHC 擴展，其餘皆為 Haskell 98 核心

data Term a where
  TInt :: Int -> Term Int

double :: Term a -> Term a   -- 前沿功能與 98 核心共存於同一模組
double (TInt n) = TInt (n * 2)
```

## 彌補了什麼缺陷
Haskell 98 彌補了 1.x 時代各版本不相容、版本漂移的混亂，建立了穩定的教學與可攜基礎，催生了 2000 年代 Haskell 教科書浪潮（Learn You a Haskell 2007、Real World Haskell 2008）。代價是核心缺少 IO 之外的現代型別系統功能（GADTs、type families、多參數型別類別等），這些之後由 GHC 擴展補足——2010 年的 Haskell 2010 修訂版因此只做了小幅整理。

## 相關條目
- [1990-Haskell-1-0問世](1990-Haskell-1-0問世.md)
- [1996-GHC編譯器問世](1996-GHC編譯器問世.md)
- [2010-Haskell2010標準](2010-Haskell2010標準.md)
