# 1985：Miranda 誕生

## 事件
1985 年，英國 Kent 大學的 **David Turner** 透過其公司 **Research Software Ltd** 商業發行了 **Miranda**——第一門廣泛被採用的**純函數式、惰性求值**語言。Miranda 影響了整個 1980 年代末的教學與研究界，並成為 **Haskell 的直接前身**：正因 Miranda 的商業授權限制，學界才在 1987 年另起爐灶設計開放標準的 Haskell。

## 語法/特性加入的理論與實用原因
### 1. 惰性求值（lazy evaluation）
- **理論原因**：Lambda 演算的 **Church–Rosser 性質**（合流性）保證：若表示式有正規形式，則無論採用何種求值順序都會得到同一結果——因此「只在需要時才求值」的 **call-by-need** 策略是安全的。Turner 早年（1979、1982）以組合子圖歸約（SKI combinator、G-machine）實現了可行的惰性求值編譯器。
- **實用原因**：惰性求值允許定義**無窮資料結構**並用模組化方式組合程式（先定義生成器、再定義過濾器、最後取值），大幅提升程式的模組性（John Hughes 1989 年〈Why Functional Programming Matters〉的核心論證）。
- **彌補缺陷**：ML/Scheme 的急切求值無法自然表達無窮串流，且會對用不到的運算浪費計算。

```miranda
ones = 1 : ones                    -- 無窮串流
naturals = 0 : map inc naturals    -- 延遲定義自身
primes = sieve [2..]               -- 無窮質數
  where sieve (p:x) = p : sieve [n | n <- x; n mod p > 0]
```

只有惰性求值下，這些「自我參照的無窮定義」才可行；急切求值會立刻無限遞迴。生成器與過濾器可分開定義、最後才組合取值——Hughes 1989 年「模組性」論證的具體寫法：

```miranda
take 5 primes            -- [2, 3, 5, 7, 11]，只計算需要的部分
zip [1..] ["蘋果","香蕉"] -- [(1,"蘋果"),(2,"香蕉")]，無窮列表配有限列表
```

### 2. 純函數式（無副作用）
- **理論原因**：Miranda 沒有可變狀態與賦值，函數是數學意義上的**純函數**，具有引用透明性（referential transparency），因此等式推理、程式變換（program transformation）與自動平行化都變得可行。
- **實用原因**：程式行為與數學定義一一對應，證明正確性與教學都更簡單。
- **彌補缺陷**：SML 仍有可變參照（ref），Scheme 有 `set!`，副作用破壞了等式推理。

純函數可用等式推理逐步化簡，對照 Scheme 的 `set!` 使同一表示式兩次求值可能不同：

```miranda
square n = n * n

-- square (2 + 3)  ==  square 2 + square 3      -- 等式推理：
--            25    ==      4  +  9             -- 這裡不成立！
-- 但 square (2+3) = square (2+3) 永遠成立（引用透明性）
-- 因此編譯器可安全做共用子表示式消除與程式變換
```

### 3. 列表推導（list comprehension）
- **理論原因**：源自 SETL 語言的集合建構式，以數學集合敘述 `{x² | x ∈ N, x 奇}` 的語法直接對應。
- **實用原因**：讓列表轉換不必寫顯式遞迴，成為日後 Python、C# 等語言 list comprehension 的源頭。
- **彌補缺陷**：LISP/Scheme 的 `map`、`filter` 組合不如數學記法直觀。

列表推導的典型用法，語法直接對應數學集合敘述 `{x² | x ∈ [1..10], x 偶}`：

```miranda
squares = [ n*n | n <- [1..10]; n mod 2 = 0 ]
-- [4, 16, 36, 64, 100]
```

搭配多個產生器（對應笛卡兒積）更見威力：

```miranda
pairs = [ (x,y) | x <- [1..3]; y <- [x..3] ]
-- [(1,1),(1,2),(1,3),(2,2),(2,3),(3,3)]
```

### 4. 打點排版（offside rule）
- **理論原因**：以縮排取代括號——「排版即語法」，減少語法雜訊。
- **實用原因**：教學上程式外觀即結構；此規則直接被 [1990-Haskell-1-0問世](1990-Haskell-1-0問世.md) 與日後 Python 繼承。
- **彌補缺陷**：LISP 的括號海與 ALGOL 系的 `begin/end` 冗贅。

offside rule：定義體以縮排（比定義行更靠右）標示，縮排「掉出」邊界即定義結束，完全不需括號：

```miranda
factorial n = prod (down n)                 -- 定義體縮排即是結構
              where
              down 0 = [0]                  -- where 子句同樣靠縮排分層
              down n = n : down (n - 1)
              prod [0] = 1
              prod (x:xs) = x * prod xs
```

### 5. 型別類的先聲
- **理論原因**：Miranda 已面對「`+` 在 int 與 float 上意義不同，如何在 Hindley–Milner 靜態型別下表達 ad-hoc 多型」的問題，以內建重載的方式處理——這個問題在 Miranda 中未完全解決，直接催生了 Haskell 的型別類（type classes）。
- **實用原因**：數值運算需要對多種型別使用同一運算子。
- **彌補缺陷**：標準 ML 需靠模組 functor 才能泛化數值程式。

Miranda 以內建重載讓 `+` 同時服務 int 與 float，但使用者無法為**自己的型別**定義重載——這個未解問題正是 Haskell 型別類的動機：

```miranda
average xs = sum xs / #xs    -- sum 與 # 是內建重載，int/float 皆可用

-- 但若自訂 Complex 型別，無法讓 + 作用其上：
-- complex = mkcomplex 1 2
-- complex + complex         -- 型別錯誤：Miranda 不允許自訂重載
```

## 彌補了什麼缺陷
Miranda 彌補了 **ML/Scheme 仍允許副作用**與**急切求值無法定義無窮資料結構**兩大缺陷，第一次讓「純函數式 + 惰性求值」成為可日常使用的語言。但它本身是**商業授權**軟體，大學不能自由取得——這個缺陷正是 [1987-Haskell構想會議](1987-Haskell構想會議.md) 成立的直接原因。

## 相關條目
- [1983-StandardML誕生](1983-StandardML誕生.md)
- [1987-Haskell構想會議](1987-Haskell構想會議.md)
- [1990-Haskell-1-0問世](1990-Haskell-1-0問世.md)
- [1975-Scheme誕生](1975-Scheme誕生.md)
