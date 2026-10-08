# 1987：Haskell 構想會議（FPCA '87）

## 事件
1987 年 9 月，在奧勒岡州波特蘭舉行的 **FPCA '87**（Functional Programming Languages and Computer Architecture）會議上，與會者在漫長的討論後達成共識：成立一個委員會，設計一門**開放標準**的惰性純函數式語言——這就是 **Haskell** 的誕生起點。委員會由 **Paul Hudak**（耶魯）主持，**Philip Wadler**（格拉斯哥）、**John Hughes**（Chalmers）等人共同領導，成員來自 Yale、Glasgow、Chalmers、Oxford 等學界機構。

## 成立的理論與實用原因
### 1. Miranda 的商業授權限制
- **理論原因**：當時惰性純函數式語言的學術基礎（組合子圖歸約、call-by-need、代數資料型別）已相當成熟，理論上不存在技術障礙，缺的只是一個開放、可自由演進的載體。
- **實用原因**：Miranda 由 Research Software Ltd 商業發行，大學**不能自由**將它用於教學與研究（無法修改、無法自由散布實作），數十所大學的課程被卡在授權問題上。
- **彌補缺陷**：學術社群需要一個像 C 一樣可自由取得與實作的標準語言。

授權差異可以這樣對照——同一個 primes 程式，Miranda 卡在授權，Haskell 則任何人皆可自由實作：

```text
-- Miranda（1985）：Research Software Ltd 商業發行
--   ✓ 教學示範   ✗ 自由散布實作   ✗ 修改語言   ✗ 大學全面採用
-- Haskell（目標）：委員會報告即標準
--   ✓ 教學示範   ✓ 自由散布實作   ✓ 開放演進   ✓ 任何人可實作
```

### 2. 惰性函數式語言方言過多（dozen+）
- **理論原因**：Miranda 之外，還有 SASL、KRC、Hope、LML、Clean（當時稱 Concurrent Clean 的前身）等**十幾種**惰性語言方言，語法與語意互不相容，研究成果難以累積與互相比較。
- **實用原因**：委員會目標正是「**統一**現有惰性函數式語言」——設計一門可作為研究、教學與語意實驗共同基準的語言。
- **彌補缺陷**：重蹈 LISP 方言大戰的覆轍（見 [1984-CommonLisp標準化](1984-CommonLisp標準化.md) 的教訓）。

方言互不相容可從語法差異看出——同一個「無窮質數」在 Miranda 與 Haskell（1990 版之前各實驗方言）寫法各異，委員會的目標就是讓一份程式碼通行所有實作：

```miranda
-- Miranda：where 子句、分號分隔的列表推導
primes = sieve [2..]
         where sieve (p:x) = p : sieve [n | n <- x; n mod p > 0]
```

```haskell
-- Haskell：where 子句、逗號分隔的列表推導（1990 年定稿語法）
primes = sieve [2..]
  where sieve (p:x) = p : sieve [n | n <- x, n `mod` p > 0]
```

### 3. 「avoid success at all costs」名言的背景
- **理論原因**：委員會深知標準化語言一旦廣泛採用，向後相容的包袱將阻礙語言繼續作為**研究實驗平台**。
- **實用原因**：主持委員 Paul Hudak 因此留下名言——Haskell 的目標是「**不惜一切代價避免成功（avoid success at all costs）**」，意在讓語言保持自由演進、不必背負商業相容性包袱。諷刺的是，Haskell 後來成為影響最深遠的函數式語言之一。
- **彌補缺陷**：避免 Miranda 式的商業綁架，也避免 Common Lisp 式的龐大相容包袱。

### 4. 委員會的設計決策
- **理論原因**：委員會決定語言應是**純函數式**（完全無副作用）、**惰性求值**、具備**型別類**（解決 ad-hoc 多型）與**打點排版**規則，並採用 Miranda 風格語法。
- **實用原因**：語言需免費、開放、任何人皆可實作，並以委員會報告（而非商業公司）作為標準文件。
- **彌補缺陷**：Miranda 的授權封閉與各惰性方言的不一致。

委員會的設計決策可化為一份「標準化目標清單」，日後的 Haskell 1.0 逐一兌現：

```text
-- Haskell 設計目標（FPCA '87 決議）：
--   1. 純函數式：完全無副作用
--   2. 惰性求值：call-by-need
--   3. 型別類：解決 ad-hoc 多型（Miranda 未解的難題）
--   4. 打點排版：offside rule
--   5. Miranda 風格語法，利於方言使用者遷移
--   6. 開放標準：報告即規格，任何人都可實作
```

## 彌補了什麼缺陷
1987 年的構想會議彌補了兩大缺陷：**Miranda 商業授權**使教學研究受限，以及**惰性函數式語言方言過多**導致研究無法累積。三年後的成果即為 [1990-Haskell-1-0問世](1990-Haskell-1-0問世.md)，並在 1998 年定著於 [1998-Haskell-98標準化](1998-Haskell-98標準化.md)。

## 相關條目
- [1985-Miranda誕生](1985-Miranda誕生.md)
- [1990-Haskell-1-0問世](1990-Haskell-1-0問世.md)
- [1998-Haskell-98標準化](1998-Haskell-98標準化.md)
- [1984-CommonLisp標準化](1984-CommonLisp標準化.md)
