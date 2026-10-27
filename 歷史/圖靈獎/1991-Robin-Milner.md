# 1991 Robin Milner —— 讓型別成為證明、讓通訊成為數學

> 「一位邏輯學家出身的英國人，一手打造了 ML 語言、型別推論
> 與行程代數 CCS。他的共同主題：**讓機器自己完成推理**。」

## 案件檔案

| 項目 | 內容 |
|---|---|
| 得主 | A. J. Robin Milner (1934–2010) |
| 得獎理由 | LCF、ML、CCS 三項工作：定理證明、型別系統、併發理論 |
| 關鍵詞 | ML、Hindley–Milner 型別推論、CCS、LCF |

## 前因

1970 年代的兩個缺口：

1. 定理證明器的證明**不可信**（系統 bug 即假定理）
2. 併發程式的正確性**無數學工具**（Hoare 的 CSP 1978 已開路）

## 線索與推理

### 線索一：LCF（Logic of Computable Functions, 1972–75）

Scott（1976 案）的不動點語義需要機器驗證。Milner 的設計
天才：**核心 tactic 引擎極小化 + 用 ML 語言寫證明策略**。

```
thm 是抽象型別：唯一建構途徑是通過核心推論規則
⟹ 只要有型別 thm 的值，必為合法定理（「證明即型別」的實踐）
```

後裔：Isabelle、Coq（λ演算史 1989-Coq 案）——**現代形式化
數學的全部基礎設施**。

### 線索二：ML 與 Hindley–Milner 型別推論

ML 原是 LCF 的策略語言，後自立為語言。關鍵發明：

```
型別推論 Algorithm W：
  輸入無標註的程式，自動解出最一般型別（principal type）
  例：let map f [] = [] | map f (x::xs) = f x :: map f xs
  推得 map : (a → b) → a list → b list   （全自動！）

基礎：統一（unification）+ 標記性（parametricity）
Hindley 1969 年已在 λ 演算中提出同構演算法
```

**寫程式不寫型別、卻有靜態型別保證**——此後 Haskell（1990）、
F#、Swift、Rust 皆承其血統。

### 線索三：CCS（Calculus of Communicating Systems, 1980）

把 Hoare 的 CSP 精緻化為完整代數：

```
P ::= 0 | a.P | P + Q | P | Q | ...
通訊 = 同步動作 (a 與 ā 對接)
語義：雙模擬（bisimulation）——兩個行程若互相模仿彼此
      可觀察行為，即視為等價
```

**雙模擬是併發系統的「同構」概念**：正確性不再靠列舉執行
路徑，而靠行為等價的證明。此後 π-calculus、行程驗證工具
（CWB、mCRL2）皆由此而出。

## 理論評析

Milner 三案的共同定理化套路：

| 案 | 被形式化的對象 | 核心工具 |
|---|---|---|
| LCF | 證明 | 型別系統當「證明的防火牆」 |
| ML | 程式 | 統一推論型別 |
| CCS | 通訊 | 雙模擬等價 |

**凡是能定義等價關係的領域，就能自動化推理**——這是本案
的方法論總綱。

## 後果

- 函數式語言的復興與型別系統成為程式語言研究主流。
- 併發理論進入驗證工業（model checking 2007 案的姊妹學科）。

## 關聯案件

→ [1980-C.A.R.-Hoare](1980-C.A.R.-Hoare.md)、[1976-Rabin-Scott](1976-Rabin-Scott.md)、[1996-Amir-Pnueli](1996-Amir-Pnueli.md)
