# 1983：Standard ML 誕生

## 事件
1983 年起，愛丁堡大學的 **Robin Milner** 與 **Mads Tofte** 開始將 LCF 定理證明器所用的詮釋語言 **Edinburgh ML** 系統化為一門正式定義的語言——**Standard ML（SML）**。參與者還包括 Robert Harper、David MacQueen 等人，最終於 1990 年出版《The Definition of Standard ML》（1997 年修訂版），成為少數擁有「形式化語意定義」的程式語言。Standard ML 是第一門將 **Hindley–Milner 型別系統**完整化、並配備**模組系統**的靜態型別函數式語言。

## 語法/特性加入的理論與實用原因
### 1. Hindley–Milner 型別推斷的完整化
- **理論原因**：Milner 在 1978 年發表的論文證明了 HM 型別系統的型別推斷演算法（Algorithm W）具有**完整型別推斷**能力——程式設計師幾乎不用寫型別宣告，編譯器就能自動推導出所有型別，且型別錯誤在編譯期即被捕捉。1983 年的 Standard ML 將 Damas–Milner 演算法正式納入語言定義，並處理了多態參照（polymorphic references）等邊界問題（value restriction）。
- **實用原因**：LISP 的動態型別使得大型系統的錯誤往往延遲到執行期才爆發；SML 讓大型系統在編譯期就獲得型別安全保證，同時保留「不用寫型別」的簡潔性。
- **彌補缺陷**：Edinburgh ML 雖有型別推斷但語言本身非正式、實作間行為不一致。

```sml
fun map f [] = []
  | map f (x::xs) = f x :: map f xs
(* 型別：('a -> 'b) -> 'a list -> 'b，完全自動推斷 *)
```

呼叫端完全不必標註型別，編譯期即檢查錯誤——對照 LISP 同樣的程式要到執行期才發現型別不符：

```sml
val squares = map (fn x => x * x) [1, 2, 3]   (* 推斷為 int list：[1, 4, 9] *)
(* map (fn x => x + 0.5) [1, 2, 3]            (* 編譯錯誤：int 與 real 不相符 *)
```

### 2. 模組系統：structure、signature、functor
- **理論原因**：Milner 將「函數式抽象」的思想提升到**模組層級**——functor 就是「以模組為參數、以模組為返回值」的函數，signature 則相當於模組的型別。這是參數化多型在模組系統的推廣，成為後世 ML 系模組語言（OCaml、Agda 模組系統）的藍本。
- **實用原因**：LCF 的策略（tactics）函式庫需要良好的封裝與複用機制；大型定理證明與編譯器專案需要明確的介面分離。
- **彌補缺陷**：LISP 沒有真正的模組系統，Edinburgh ML 只靠命名慣例分隔。

```sml
signature ORDERED = sig
  type t
  val compare : t * t -> order
end

functor MakeSet (O : ORDERED) = struct
  datatype set = Empty | Node of set * O.t * set
  fun insert (Empty, x) = Node (Empty, x, Empty)
    | insert (Node (l, y, r), x) =
        case O.compare (x, y) of
          LESS    => Node (insert (l, x), y, r)
        | EQUAL   => Node (l, y, r)
        | GREATER => Node (l, y, insert (r, x))
end

(* 同一個 functor 可套用到任何有序型別 *)
structure IntSet   = MakeSet (struct type t = int fun compare (a,b) = Int.compare (a,b) end)
structure StringSet = MakeSet (struct type t = string fun compare (a,b) = String.compare (a,b) end)
```

這正是「SML 需靠 functor 才能泛化數值程式」的具體寫法——抽象與實作在模組層級分離，對照 LISP 只能靠命名慣例（如 `mylib-insert`）模擬封裝。

### 3. datatype 宣告與模式匹配
- **理論原因**：源自 1970 年代對代數資料型別（algebraic data types）的研究，`datatype` 允許定義**和型別（sum type）**，搭配模式匹配做結構化解構，對應 HOPE 語言的實驗成果。
- **實用原因**：定理證明器需要表示語法樹與證明項，和型別是天然的工具。
- **彌補缺陷**：LISP 需用 cons cell 與符號手動編碼資料結構，缺乏編譯期檢查。

```sml
datatype expr = Const of int
              | Var   of string
              | Plus  of expr * expr
              | Times of expr * expr

(* 模式匹配做結構化解構：求值語法樹 *)
fun eval env (Const n)   = n
  | eval env (Var name)  = env name
  | eval env (Plus (a, b))  = eval env a + eval env b
  | eval env (Times (a, b)) = eval env a * eval env b

val tree = Plus (Const 3, Times (Const 2, Var "x"))
val result = eval (fn "x" => 5 | _ => 0) tree   (* [13] *)
```

若新增建構子（如 `Minus`）而漏掉某個匹配分支，編譯器會發出「non-exhaustive match」警告——LISP 的 cons cell 編碼完全得不到這種檢查。

### 4. 例外處理（exception）
- **理論原因**：在靜態型別語言中引入非局部跳脫需要與型別系統整合；SML 的 exception 是一等值的「和型別的動態成員」，由 raise 與 handler 配對。
- **實用原因**：LCF 中戰術失敗需要即時中止回溯，例外處理是控制搜尋流程的自然機制。
- **彌補缺陷**：Edinburgh ML 只有簡陋的錯誤中止；LISP 的錯誤機制依賴動態作用域難以分析。

exception 與 raise/handle 配對的典型用法——戰術失敗時回退到另一個策略：

```sml
exception Failure of string

fun tactic1 goal = raise Failure "tactic1 失敗"
fun tactic2 goal = "證明完成"

(* handle 捕捉例外並提供備案，控制搜尋流程 *)
fun tryTactics goal =
      (tactic1 goal; tactic2 goal)
      handle Failure msg => (print ("回退：" ^ msg); tactic2 goal)
```

## 彌補了什麼缺陷
Standard ML 彌補了兩大缺陷：其一是 **LISP 系語言的動態型別無法支撐大型系統**——SML 用完整化的 Hindley–Milner 型別推斷達成「動態語言的便利 + 靜態語言的安全」；其二是 **Edinburgh ML 缺乏正式標準**——《The Definition of Standard ML》使其成為語意形式化的典範。它的模組系統與 datatype 更直接影響了 [1990-CAML誕生](1990-CAML誕生.md) 與 [1996-OCaml誕生](1996-OCaml誕生.md)。

## 相關條目
- [1970-ML誕生於LCF定理證明器](1970-ML誕生於LCF定理證明器.md)
- [1990-CAML誕生](1990-CAML誕生.md)
- [1996-OCaml誕生](1996-OCaml誕生.md)
- [1985-Miranda誕生](1985-Miranda誕生.md)
