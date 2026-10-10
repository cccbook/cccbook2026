# 1996：OCaml 誕生

## 事件
1996 年，法國國家資訊與自動化研究院（INRIA）的 Xavier Leroy、Jérôme Vouillon 與 Damien Doligez 等人，將 Caml Light 重新設計並擴充，發表 Objective Caml（簡稱 OCaml）。它在經典的 ML 語言之上加入了物件系統與子型別（subtyping），並提供編譯到原生機器碼（native-code compiler）的編譯器，使函數式語言首次同時具備「ML 型別系統 + 物件導向 + 產業級執行速度」。OCaml 是多範式語言：函數式、命令式、物件導向三種風格並存，由強大的 Hindley–Milner 型別推論統合。

## 語法/特性加入的理論與實用原因

### 1. 物件系統與結構化子型別（structural subtyping）
- **理論原因**：1990 年代物件導向當道，ML 陣營若要證明函數式語言可以容納物件，需要一個不犧牲型別推論的物件理論。OCaml 採用「結構化子型別」——型別的相容性由結構決定，而非名稱宣告，這在理論上更接近紀錄型別的推廣。
- **實用原因**：讓函數式程式碼能與物件導向框架、GUI 工具箱互動，降低進入門檻。
- **彌補缺陷**：Caml Light 完全沒有物件與子型別，無法參與當時主流的 OOP 生態。

```ocaml
class point init_x =
  object
    val mutable x = init_x
    method get_x = x
    method move d = x <- x + d
  end

(* 結構化子型別：只要結構相容就能互通，不需事先宣告繼承 *)
let print (p : < get_x : int >) = Printf.printf "%d\n" p#get_x
let p = new point 3
let () = print p          (* point 的結構包含 get_x，故可傳入 *)
```

對照 Java：Java 的介面抽象靠「名稱」宣告（`class Point implements Printable`），OCaml 只看物件實際擁有的方法，更接近鴨子型別但保有靜態檢查。`#` 是方法呼叫運算子。

### 2. 原生碼編譯器與高效 GC
- **理論原因**：ML 語言具有靜態強型別與可預測的記憶體配置模式，理論上可以編譯到與 C 相近的機器碼，而不需直譯或只做位元組碼。
- **實用原因**：位元組碼編譯器（bytecode compiler）速度不足以應付實務；Damien Doligez 設計的增量式（incremental）垃圾回收器避免長時間暫停，適合互動與伺服場景。
- **彌補缺陷**：早期 ML 實作（包括 SML/NJ）編譯速度慢、記憶體佔用大，且授權不利於商業使用；OCaml 採寬鬆的 LGPL/Q 授權，產業可安心採用。

### 3. 模組系統與 functors
- **理論原因**：ML 的模組語言（源自 1980 年代 MacQueen 等人的工作）提供參數化模組——functor：以「模組」為參數、回傳「模組」的函數，是型別層次的抽象。
- **實用原因**：大型專案可以在不使用物件的情況下做到抽象與重用，編譯期即可解析，沒有虛擬呼叫的執行期成本。
- **彌補缺陷**：物件導向的介面抽象在函數式語言中缺乏對應物；functor 提供了更強的編譯期抽象。

```ocaml
module type ORDERED = sig type t val compare : t -> t -> int end

module MakeSet (O : ORDERED) = struct
  (* 以 O.compare 實作平衡樹集合 *)
  type t = Empty | Node of t * O.t * t

  let rec add x = function
    | Empty -> Node (Empty, x, Empty)
    | Node (l, v, r) ->
        (match O.compare x v with
         | 0 -> Node (l, v, r)
         | c when c < 0 -> Node (add x l, v, r)
         | _ -> Node (l, v, add x r))
end

module IntSet = MakeSet (struct type t = int let compare = compare end)
let s = IntSet.add 3 (IntSet.add 1 IntSet.Empty)
```

functor 在編譯期即解析：`MakeSet` 只寫一次，就能對 int、字串、任意可比較型別各生成一份平衡樹，沒有 Java 泛型擦除或虛擬呼叫的執行期成本。

### 4. 多範式統合
- **理論原因**：函數式核心（代數資料型別、模式匹配、高階函數）與命令式（可變參考 `ref`、迴圈）、物件三者可以共存於同一型別系統，證明「純」與「非純」不需要分裂成兩種語言。
- **實用原因**：工程師可依情境選擇風格：演算法用函數式，效能瓶頸用命令式，框架互作用物件。
- **彌補缺陷**：純函數式語言（如 Haskell）處理副作用需透過單子，學習曲線陡；OCaml 提供較平緩的折衷。

同一支程式裡，演算法用函數式、效能熱點用命令式，兩種風格自由混搭：

```ocaml
(* 函數式：以遞迴與模式匹配處理串列 *)
let rec sum = function
  | [] -> 0
  | x :: rest -> x + sum rest

(* 命令式：以 ref 與 for 迴圈處理效能敏感的累加 *)
let sum_fast arr =
  let acc = ref 0 in
  for i = 0 to Array.length arr - 1 do
    acc := !acc + arr.(i)
  done;
  !acc

(* 物件：封裝一個計數器 *)
class counter =
  object
    val mutable n = 0
    method tick = n <- n + 1
    method get = n
  end

let () = Printf.printf "%d %d %d\n" (sum [1;2;3]) (sum_fast [|1;2;3|])
             (let c = new counter in c#tick; c#tick; c#get)
```

模式匹配對 `option` 型別的處理，展現 ML 家族「以型別表達可能缺席」的慣用法：

```ocaml
(* 對照 Java：可能回傳 null，呼叫端忘了檢查就 NPE *)
let safe_div a b =
  if b = 0 then None else Some (a / b)

match safe_div 10 2 with
| Some q -> Printf.printf "%d\n" q
| None   -> print_endline "除以零！"   (* 編譯器強制處理 None 分支 *)
```

## 彌補了什麼缺陷
OCaml 彌補了 Caml Light 缺少物件與子型別的遺憾，也解決了 SML 各編譯器速度與授權的產業障礙。它證明 ML 家族語言可以是「產業利器」：2000 年代起，Jane Street 以 OCaml 作為核心交易系統語言，Facebook 以其開發 Hack 與 Flow，Xen hypervisor 的控制層以 OCaml 撰寫，定理證明器 Coq 的實作底層也是 OCaml。

## 相關條目
- [1990-CAML誕生](1990-CAML誕生.md)
- [1996-GHC編譯器問世](1996-GHC編譯器問世.md)
- [2004-Scala誕生](2004-Scala誕生.md)
- [2005-Fsharp誕生](2005-Fsharp誕生.md)
- [2013-Lean誕生](2013-Lean誕生.md)
