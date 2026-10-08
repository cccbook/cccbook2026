# 函數式程式語言發展史年表

> 函數式程式設計是程式語言史上最古老的傳統之一：從 1936 年 Church 的 λ 演算出發，
> 經過 LISP（1958）、Scheme（1975）、ML（1970s）、Miranda/Haskell（1980s-90s）、
> OCaml/Scala/F#/Clojure（1990s-2000s），一路到 Idris 與 Lean（2010s-2020s）的依值型別時代。
> 它的核心理念——函數是值、不可變資料、型別即證明——如今已滲透進幾乎所有主流語言。

## 前史：理論根源

| 年份 | 事件 | 意義 |
|------|------|------|
| 1920s | Curry 的組合邏輯 | 不需變數的函數組合理論，Combinatory Logic |
| 1936 | Church 的 λ 演算 | 與圖靈機等價的計算模型，一級函數的數學基礎 |
| 1956 | Dartmouth 會議 | AI 誕生，符號運算需要新的程式語言 |
| 1957 | APL 問世 | 函數層級程式設計的先驅 |

## 正式年表

| 年份 | 標題 | 關鍵語法/特性 |
|------|------|---------------|
| 1936 | [λ 演算：邱奇的奇點](1936-lambda演算邱奇奇點.md) | 變數綁定、β-歸約、α/η 轉換、Church–Turing 假說 |
| 1958 | [LISP 誕生](1958-LISP誕生.md) | S-表達式、列表與 CAR/CDR、COND、REPL、遞迴 |
| 1962 | [LISP 1.5 與 GC、巨集](1962-LISP-1-5與GC巨集.md) | 垃圾回收（標記-清除）、巨集系統、mapcar、FUNARG 問題 |
| 1970 | [ML 誕生於 LCF 定理證明器](1970-ML誕生於LCF定理證明器.md) | Hindley–Milner 型別推斷、參數多型、模式匹配 |
| 1975 | [Scheme 誕生](1975-Scheme誕生.md) | 詞法作用域、尾端呼叫優化、一級閉包、continuation |
| 1977 | [Backus 函數式風格宣言](1977-Backus函數式風格宣言.md) | FP 系統、組合子、批評 von Neumann bottleneck |
| 1983 | [Standard ML 誕生](1983-StandardML誕生.md) | 模組系統（functor/signature）、datatype、例外處理 |
| 1984 | [Common Lisp 標準化](1984-CommonLisp標準化.md) | 統一數十種方言、CLOS 多重分派、condition system |
| 1985 | [Miranda 誕生](1985-Miranda誕生.md) | 惰性求值、純函數式、列表推導、offside rule |
| 1987 | [Haskell 構想會議](1987-Haskell構想會議.md) | FPCA '87 決定設計開放標準的惰性純函數式語言 |
| 1990 | [Haskell 1.0 問世](1990-Haskell-1-0問世.md) | 型別類別（type classes）、單子（monad）與 IO |
| 1990 | [CAML 誕生](1990-CAML誕生.md) | INRIA 的 ML 工業級實作、Categorical Abstract Machine |
| 1996 | [OCaml 誕生](1996-OCaml誕生.md) | 物件系統、結構化子型別、原生碼編譯器、functors |
| 1996 | [GHC 編譯器問世](1996-GHC編譯器問世.md) | STG 機、嚴格性分析、fusion、擴展文化 |
| 1998 | [Haskell 98 標準化](1998-Haskell-98標準化.md) | 語言凍結小核心、穩定核心+方言擴展模式 |
| 1998 | [Erlang 開源](1998-Erlang開源.md) | actor 行程、監督樹、let it crash、OTP、熱替換 |
| 2004 | [Scala 誕生](2004-Scala誕生.md) | JVM 統合、case class、trait、implicit、higher-kinded types |
| 2005 | [F# 誕生](2005-Fsharp誕生.md) | OCaml 移植 .NET、async workflows、型別提供者、單位 of measure |
| 2007 | [Clojure 誕生](2007-Clojure誕生.md) | 不可變資料結構（HAMT）、STM、 Lisp on JVM |
| 2010 | [Haskell 2010 標準](2010-Haskell2010標準.md) | FFI 併入、GHC 擴展文化（GADTs、type families）、Hackage 生態 |
| 2013 | [Idris 依值型別](2013-Idris依值型別.md) | 型別依賴值（Vect n）、totality checking、Type-Driven Development |
| 2013 | [Lean 誕生](2013-Lean誕生.md) | 定理證明器+程式語言合一、依值型別論、mathlib |
| 2021 | [Lean 4 問世](2021-Lean4問世.md) | self-hosted 編譯器、metaprogramming、mathlib 遷移 |
| 2025 | [函數式程式語言的未來展望](2025-函數式程式語言的未來展望.md) | 函數式概念滲透主流、AI 定理證明、effect systems、WebAssembly |

## 發展主軸

1. **1936–1958：理論誕生** —— λ 演算從純數學變成 LISP，函數第一次成為「值」。
2. **1970–1985：型別與純度** —— ML 帶來型別推斷，Scheme 帶來詞法作用域，Miranda 帶來惰性與純度。
3. **1990–1998：標準化** —— Haskell、OCaml、Erlang 各自確立標準或開源，函數式從學術走向工業。
4. **2004–2013：多範式融合** —— Scala、F#、Clojure 把函數式概念帶進 JVM/.NET 生態。
5. **2013–至今：型別即證明** —— Idris 與 Lean 讓依值型別落地，AI 與形式化驗證（如 AlphaProof）以 Lean 為驗證器。
6. **全面滲透** —— Rust 的 ownership、Java 的 records、C++ 的 ranges/expected：函數式已是所有語言的基本配備。

## 相關書冊
- [C 程式語言發展史](../C/)
- [C++ 程式語言發展史](../C%2B%2B/)
- [JavaScript 程式語言發展史](../JavaScript/)
- [Rust 程式語言發展史](../Rust/)
