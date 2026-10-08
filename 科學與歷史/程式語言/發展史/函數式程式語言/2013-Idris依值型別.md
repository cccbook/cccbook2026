# 2013：Idris 依值型別

## 事件
Edwin Brady 自 2007 年開始開發 Idris 原型，2013 年推出接近 1.0 的實用版本（1.0 正式版於 2017 年初，與其著作《Type-Driven Development with Idris》同年出版）。Idris 是第一個以「依值型別程式設計」（type-driven development）為核心設計目標、面向一般程式設計師的通用語言，而不只是研究或定理證明工具。2020 年發布的 Idris 2 改以 Quantitative Type Theory 為基礎重寫。

## 語法/特性加入的理論與實用原因
### 1. 依值型別（dependent types）：型別可依賴值
- **理論原因**：依值型別論（源自 Martin-Löf type theory）允許型別以值為參數，使「回傳長度為 n 的向量」這類性質可以直接寫進型別。
- **實用原因**：長度、排序、邊界等不變量在編譯期即可檢查，省下大量防禦性程式碼與執行期斷言。
- **彌補缺陷**：Haskell/OCaml 的型別系統無法表達「回傳長度為 n 的列表」——`[a]` 不攜帶長度資訊，這類錯誤只能靠測試捕捉。

```idris
data Vect : Nat -> Type -> Type where
  Nil  : Vect Z a
  (::) : a -> Vect n a -> Vect (S n) a

zip : Vect n a -> Vect n b -> Vect n (a, b)  ; 兩輸入長度必須相等，編譯器強制
head : Vect (S n) a -> a  ; 對空向量取 head 直接型別錯誤，不需 Maybe
```

對照組：Haskell 的 `[a]` 不攜帶長度，`head` 只能回傳 `Maybe a`，呼叫端被迫處理永遠不該發生的 `Nothing`：

```haskell
-- Haskell：長度資訊不在型別中，防禦性程式碼到處都是
safeHead :: [a] -> Maybe a
safeHead []     = Nothing        -- 呼叫端必須處理這個不該發生的情況
safeHead (x:_)  = Just x

zipSame :: [a] -> [b] -> Maybe [(a, b)]  -- 長度相等只能靠執行期檢查
zipSame xs ys = if length xs == length ys then Just (zip xs ys) else Nothing
```

Idris 中長度編碼在型別裡，`zip` 的長度相等是編譯期事實，取元素不需 `Maybe`。`append` 的結果長度 `n + m` 也直接由型別算出：

```idris
append : Vect n a -> Vect m a -> Vect (n + m) a
append Nil ys = ys
append (x :: xs) ys = x :: append xs ys
-- 回傳型別 Vect (n + m) a 由輸入長度決定，不需任何執行期斷言
```

### 2. Curry–Howard 對應：寫型別＝寫定理
- **理論原因**：命題即型別、證明即程式——依值型別使這個對應可日常使用，函數簽名就是待證命題，實作就是證明。
- **實用原因**：`total` 與 `partial` 關鍵字、利用類型洞（holes，`?rhs`）互動式開發，編譯器根據型別建議補全程式碼。
- **彌補缺陷**：單元測試只能驗證抽樣的例子，無法證明「所有輸入都正確」。

「先寫型別、用洞互動補全」是 Type-Driven Development 的核心流程：

```idris
-- 步驟一：只寫型別（簽名就是待證命題）
appendNilLeft : (xs : Vect n a) -> xs ++ [] = xs

-- 步驟二：用洞 ?rhs 互動開發，編譯器依型別建議補全
appendNilLeft Nil = ?rhs_nil      -- ?rhs_nil : Nil ++ [] = Nil，即_refl
appendNilLeft (x :: xs) = ?rhs_cons
-- 編譯器告訴你 ?rhs_cons 的型別，逐步以 refl 導出證明
```

對照組：單元測試只能抽樣驗證，型別簽名則是對所有輸入的證明：

```idris
-- 測試只能驗證抽樣的例子：
--   appendNilLeft [1,2] == [1,2]  ✓  但 [3,4,5] 呢？無窮多個輸入測不完
-- 型別（定理）則涵蓋所有 Vect n a：
appendNilLeft xs = refl  -- 一行證明所有情況（配合歸納後的簡化）
```

### 3. Totality checking（全函數檢查）
- **理論原因**：全函數（對所有輸入都終止且覆蓋所有情況）才對應完整的證明；檢查終止性（structural recursion）與覆蓋性。
- **實用原因**：標注 `total` 的函數保證不會當機、不會無窮迴圈，是合約式開發的基礎。
- **彌補缺陷**：Haskell/OCaml 不區分全函數與部分函數，非窮舉 pattern matching 只給警告。

```idris
%default total   -- 本模組預設全部函數必須證明會終止且窮舉

-- total：編譯器驗證 structural recursion，保證不當機、不無窮迴圈
total vlength : Vect n a -> Nat
vlength Nil = Z
vlength (_ :: xs) = S (vlength xs)

partial loopForever : Nat -> Nat   -- 明確標注 partial，不參與證明
loopForever n = loopForever n
-- 若把 total 函數寫成遞迴在所有情況下不終止，編譯直接錯誤
```

### 4. 急切求值與線性資源（Idris 2 的 QTT，2020）
- **理論原因**：Idris 1 選擇急切求值以求語義單純；Idris 2 採用 Quantitative Type Theory——每個變數在型別中標注使用次數（0/1/許多），把線性型別（linear types）與依值型別統一。
- **實用原因**：使用次數 0 表示編譯期可安全消除，次數 1 可做記憶體管理（Idris 2 因此得以 self-hosted，以自身實作）。
- **彌補缺陷**：Idris 1 的垃圾回收與 erased 引數（`%elim`）機制不夠系統化。

Idris 1/2 都支援依值反射——在程式中直接呼叫編譯器計算型別或證明：

```idris
-- 依值反射：用 = 型別在函數中表達並證明性質
sameLength : Vect n a -> Vect m b -> Bool
sameLength {n} {m} _ _ = n == m   -- 長度 n、m 是型別層的值，直接可比較

-- QTT（Idris 2）：使用次數寫在型別裡
--   (0 x : a) 表示 x 編譯期消除、(1 x : a) 表示恰好用一次（可用於記憶體管理）
dup : (1 x : a) -> (a, a)   -- Idris 2：線性使用，x 恰好用一次
```

## 彌補了什麼缺陷
Idris 把依值型別從定理證明器的象牙塔帶進實用語言，彌補了 Haskell/OCaml 無法在型別中表達值相關性質（長度、排序、協定狀態）的缺口，並證明「測試無法證明正確性」可以由「型別驅動開發 + 全函數檢查」部分取代。它也直接影響了 Lean 的程式語言面向、Idris 2 的 QTT、以及 Rust/Swift 中更細粒度的資源與不變量表達風潮。

## 相關條目
- [1996-GHC編譯器問世](1996-GHC編譯器問世.md)
- [2010-Haskell2010標準](2010-Haskell2010標準.md)
- [2013-Lean誕生](2013-Lean誕生.md)
- [2021-Lean4問世](2021-Lean4問世.md)
- [2025-函數式程式語言的未來展望](2025-函數式程式語言的未來展望.md)
