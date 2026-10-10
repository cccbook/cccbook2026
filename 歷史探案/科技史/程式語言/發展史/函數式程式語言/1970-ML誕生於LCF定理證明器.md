# 1970：ML 誕生於 LCF 定理證明器

## 事件
1970年，**Robin Milner** 在愛丁堡大學為 LCF（Logic for Computable Functions，可計算函數的邏輯）定理證明器設計了 **ML**（Meta Language，中介語言）。ML 原本不是獨立語言，而是讓使用者撰寫證明策略、操作定理的「指令語言」。Milner 隨後發展出 Hindley–Milner 型別系統與 W 演算法（1975 年正式發表），ML 逐漸成為獨立的通用函數式語言，並衍生出 Standard ML（1983 起）與 Caml（1985）/OCaml（1996）。

## 語法/特性加入的理論與實用原因

### 1. 型別推斷（Hindley–Milner 型別系統）
- **理論原因**：定理證明必須保證證明程式本身無型別錯誤——「型別正確的程式不會出某些類的錯」正是數學嚴謹性的要求。Milner 借鑑 Hindley（1969）的型別演算法，設計出可推斷型別的系統，並以 **W 演算法**（1975 年發表）實現。
- **實用原因**：要求使用者手寫型別宣告會拖慢互動式定理證明的節奏；型別推斷讓編譯器自動算出所有型別。
- **彌補缺陷**：LISP 的動態型別讓許多錯誤（把符號當數字加）要執行到才會發現；ML 在編譯期就攔下這類錯誤。

```
fun fact 0 = 1
  | fact n = n * fact (n - 1)
(* ML 自動推斷 fact : int -> int *)
```

完全不必寫型別宣告，編譯器（或 REPL）自動推得每個值的型別：

```sml
- fun double n = n * 2;
val double = fn : int -> int        ; 由 * 推得 n 是 int
- fun add a b = a + b;
val add = fn : int -> int -> int    ; 由 + 推得兩個引數都是 int
- val msg = "hello";
val msg = "hello" : string          ; 字面值直接定案
- fun f x = if x > 0 then x else 0;
val f = fn : int -> int             ; if 的兩支型別必須一致，推得 int
```

對照組：LISP 動態型別要到執行期才爆發錯誤：

```lisp
;; LISP：(+ 1 "a") 直譯器不會事先擋下，執行到才報錯
(+ 1 "a")
; 執行期錯誤："a" 不是數字
;; 若這行程式藏在幾萬行之外、罕用的分支裡，
;; 可能上線數月後才第一次被執行到
```

### 2. 靜態強型別但不用寫型別宣告
- **理論原因**：Hindley–Milner 型別系統是「參數多型」的單型化（let-polymorphism），兼顧嚴謹與簡潔。
- **實用原因**：達成「靜態型別的安全性 + 動態型別的書寫便利」兩者兼得。
- **彌補缺陷**：同時彌補 LISP（無靜態型別保障）與 ALGOL/FORTRAN（必須手寫型別）兩方的缺陷。

對照組：ALGOL 60 / FORTRAN 必須手寫型別宣告；ML 的推斷省去這層負擔，卻保留同樣的靜態保障：

```fortran
C     FORTRAN：每個變數都要宣告型別
      INTEGER N
      REAL X
      N = 3
      X = 1.5
```

```sml
(* ML：不寫任何型別宣告，錯誤照樣在編譯期被攔下 *)
val n = 3
val x = 1.5
(* n * x  → 編譯期型別錯誤：int 與 real 不能直接相乘 *)
(* 而在 LISP 中 (+ 3 1.5) 會安靜地算出 4.5，隱藏的精度問題到執行期才浮現 *)
```

### 3. 參數多型（Parametric Polymorphism）
- **理論原因**：`length : 'a list -> int` 這種「對任意型別都成立」的函數在數學上就是自然的泛函，型別系統應能表達之。
- **實用原因**：定理證明器處理各種資料結構，容器操作需要通用化，否則要為每種型別複製一份函數。
- **彌補缺陷**：當時主流靜態語言沒有泛型；不寫泛型的代價是大量重複程式碼。

`length` 的型別 `'a list -> int` 是推斷出來的參數多型——同一份程式碼對任何元素型別都成立：

```sml
- fun length nil = 0
=   | length (_ :: t) = 1 + length t;
val length = fn : 'a list -> int    ; 『a 是型別變數：任意型別

- length [1, 2, 3];
val it = 3 : int
- length ["a", "b"];
val it = 2 : int                    ; 同一份程式碼，字串列表也適用
- length [(1, "x"), (2, "y")];
val it = 2 : int                    ; 配對列表也適用
```

對照組：沒有泛型的靜態語言得為每種型別複製一份函數：

```text
;; 無泛型時的慘況（C 語言風格的複製貼上）：
int length_int(int a[], int n)   { /* ... */ }
int length_str(char *s[], int n) { /* 幾乎相同的程式碼 */ }
int length_pair(...)             { /* 又一份相同的程式碼 */ }
```

### 4. 模式匹配（Pattern Matching）
- **理論原因**：數學定義本來就是「按結構分情形定義」——0 的階乘是 1、n 的階乘是 n×(n−1)!。模式匹配把這種定義方式直接搬進語言。
- **實用原因**：定理證明需要解構代數資料型別（項、公式、證明樹），模式匹配是最自然的寫法，且編譯器能檢查所有情形是否涵蓋（exhaustiveness check）。
- **彌補缺陷**：LISP 的 cond 需手動呼叫謂詞逐一測試，容易漏掉情形；模式匹配把遺漏變成編譯錯誤。

模式匹配按資料結構分情形定義，編譯器還會檢查涵蓋性：

```sml
(* 按結構分情形：與數學定義逐字對應 *)
fun fact 0 = 1
  | fact n = n * fact (n - 1);

(* 模式匹配解構列表：空列表與「頭 :: 尾」兩種情形 *)
fun sum nil = 0
  | sum (h :: t) = h + sum t;

(* 模式匹配解構配對 *)
fun fst (x, _) = x;
fun snd (_, y) = y;
fst (3, "x");    (* => 3 *)
```

對照組：LISP 用 cond + 謂詞手動分支，漏掉一種情形編譯器不會警告：

```lisp
;; LISP cond：若忘了 (null l) 這一條，
;; (car nil) 會在執行期才爆炸，且編譯器無從警告
(defun sum (l)
  (cond ((atom l) l)                     ; 只測了 atom，忘了處理空列表的語義
        (t (+ (car l) (sum (cdr l))))))
```

```sml
(* ML：若只寫一條子句，編譯器立即發出警告 *)
- fun sum (h :: t) = h + sum t;
(* 警告：match nonexhaustive；nil 的情形沒有涵蓋 *)
```

## 彌補了什麼缺陷
ML 證明了「靜態強型別」與「函數式便利」可以並存：型別推斷免除了型別宣告的負擔，參數多型免除了程式碼重複，模式匹配免除了手動分支檢查。它彌補的最大缺陷是 LISP 動態型別「錯誤要到執行期才爆發」的問題——對必須絕對嚴謹的定理證明而言，這是生死攸關的差別。Hindley–Milner 型別系統此後成為 Haskell、F#、Rust 等語言的基石。

## 相關條目
- [1962-LISP-1-5與GC巨集](1962-LISP-1-5與GC巨集.md)
- [1975-Scheme誕生](1975-Scheme誕生.md)
- [1977-Backus函數式風格宣言](1977-Backus函數式風格宣言.md)
