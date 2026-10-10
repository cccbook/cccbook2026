# Lean 程式語言發展史年表

> Lean 是 2013 年由 Leonardo de Moura 在微軟研究院（Microsoft Research）開始的
> 定理證明器與程式語言，名稱取自「精簡（lean）」——目標是打造一個
> 核心小而可信、同時又是通用程式語言的證明助手。
> 它以依賴型別理論（dependent type theory）為基礎，讓「數學證明」與「程式碼」
> 共用同一套語言：程式即證明、型別即命題（Curry–Howard 對應）。
> 2023 年成立 Lean FRO（Formal Reasoning，由 AWS 贊助），Lean 4 已成為
> 數學形式化（mathlib 數百萬行證明）與可驗證程式設計的主流工具。

## 前史：理論根源

| 年份 | 事件 | 意義 |
|------|------|------|
| 1967 | de Bruijn 的 Automath | 「程式即證明」的先驅：證明可以像程式一樣被機器檢查 |
| 1972 | Milner 的 LCF | 定理證明器與 tactic（策略）概念的起源；證明核心小型化 |
| 1973 | Curry–Howard 對應確立 | 命題即型別、證明即程式——Lean 的理論基石 |
| 1983 | Martin-Löf 類型論 | 依賴型別（dependent types）的理論基礎 |
| 1989 | Coq 問世 | 依賴型別互動式定理證明器，Galina 區分 Prop/Set——Lean 的直接前身 |
| 2006 | Z3 SMT 解答器成熟 | de Moura 的前作：自動化推理引擎，後來成為 Lean tactic 的後端 |
| 2012 | Isabelle/HOL 的 Sledgehammer | 自動化 tactic 呼叫外部證明器——Lean 的 automation 設計參考 |

## 正式年表

| 年份 | 標題 | 關鍵語法/特性 |
|------|------|---------------|
| 2013 | [Lean 誕生於微軟研究院](2013-Lean誕生於微軟研究院.md) | Lean 1：依賴型別理論核心、universe polymorphism、unification hints |
| 2015 | [Lean 2：核心分離與 HoTT](2015-Lean-2核心分離與HoTT.md) | 雙核心模式（standard/HoTT）、巢狀與相互歸納類型、kernel 簡化重寫 |
| 2016 | [VS Code 擴充與工具初現](2016-VS-Code擴充與Lean3預覽.md) | 首個 VS Code extension（vscode-lean）、LSP 協定導入、editor 即證明介面 |
| 2017 | [Lean 3 與 mathlib 誕生](2017-Lean-3與mathlib誕生.md) | C++ 前端重寫、elaborator 改革、`meta def` 元程式設計、mathlib 社群函式庫、Elan |
| 2019 | [Lean 4 構想與自舉宣言](2019-Lean-4構想與自舉宣言.md) | Lean 4 論文發表：編譯器以 Lean 本身撰寫、宏與元程式設計合一 |
| 2020 | [Liquid Tensor Experiment](2020-Liquid-Tensor-Experiment.md) | Scholze 挑戰：以 mathlib 形式化凝聚數學核心定理——形式化數學的里程碑 |
| 2021 | [Lean 4 問世](2021-Lean-4問世.md) | 自舉編譯器、`macro`/`syntax`/`do` 記法、structure eta、C runtime |
| 2021 | [Lean 4 VS Code 擴充與 Lake](2021-Lean4-VS-Code擴充與Lake.md) | vscode-lean4 擴充、Lake 建構工具取代 leanpkg、InfoView 重寫 |
| 2022 | [mathlib 移植開始](2022-mathlib移植開始.md) | mathlib4 誕生、數學函式庫向 Lean 4 大遷徙、Elan 統一工具鏈 |
| 2023 | [Lean FRO 與 Lean 4.0.0](2023-Lean-FRO與Lean-4-0-0.md) | Lean FRO 成立（AWS 贊助）、Lean 4.0.0 穩定版、mathlib 完成移植、`omega` |
| 2024 | [Reservoir 與生態擴張](2024-Reservoir與生態擴張.md) | Reservoir 套件庫上線、`partial def` 成熟、VFML 與機器學習形式化 |
| 2025 | [grind 戰術與 Lean 4.16](2025-grind戰術與Lean-4-16.md) | `grind` 自動化戰術（E-graph + SMT）、`bv_decide` 位元向量決策 |
| 2026 | [未來展望](2026-未來展望.md) | 數學形式化與可驗證軟體的合流、Lean 作為通用語言的可能性 |

## 工具鏈發展主軸

1. **2016 vscode-lean → 2021 vscode-lean4** —— 編輯器從「外部外掛」走向
   「證明互動介面」：語意高亮、Goal 面板、逐行證明除錯，補足了 Coq/Isabelle
   IDE 體驗的缺陷。
2. **2017 Elan** —— 仿 rustup 的版本管理器：每個專案綁定特定 Lean 版本，
   消除「Lean 3 與 Lean 4 不相容」的版本地獄。
3. **2017 leanpkg/make → 2022 Lake** —— 建構工具從 Makefile 腳本走向
   宣告式依賴管理（`lakefile.lean`），與語言本身同一套語法。
4. **mathlib** —— 2017 年誕生的社群數學函式庫，2023 年完成 Lean 4 移植，
   已超過數百萬行、數十萬定理，是史上最大的形式化數學庫。
5. **Reservoir（2024）** —— Lean FRO 官方套件庫，補足 Lean 4 生態
   缺乏中央套件註冊處的缺陷。

## 發展主軸

1. **2013–2015：微軟研究院實驗** —— de Moura 以 Z3 作者之姿打造「精簡的證明器」，
   核心小到一個人可以驗證。
2. **2015–2017：Lean 2/3 的迭代** —— 雙核心實驗（HoTT）、C++ 重寫、
   mathlib 誕生，數學社群開始聚集。
3. **2017–2021：Lean 4 的豪賭** —— 為了解決 Lean 3「elaborator 難改、
   元程式設計受限、效能不足」的缺陷，de Moura 決定讓編譯器自舉：
   Lean 4 的編譯器、宏、戰術全部以 Lean 撰寫。
4. **2021–至今：自舉時代與數學大躍進** —— Liquid Tensor Experiment、
   mathlib 移植、FRO 成立、`grind` 自動化——Lean 從學術玩具
   變成形式化數學與可驗證軟體的工業級基礎設施。
