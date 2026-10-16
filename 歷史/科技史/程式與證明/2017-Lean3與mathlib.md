# 2017 Lean 3 案：tactic 住進 Lean 本體，mathlib 大爆炸

> 報案人：Lean 2 使用者。案情：tactic 用 Lua 寫，elaborator 慢，函式庫長不大。
> 偵探：de Moura、Daniel Selsam、Gabriel Ebner、Jeremy Avigad。兇器：Lean 寫的元程式框架 ＋ 高速虛擬機 ＋ mathlib monorepo。

## 案發現場

2016 年，Lean 2 的三個病灶同時發作。第一，Lua tactic 與本體脫節：想寫一個自動化的人，要在兩個語言、兩套語義之間跳來跳去。第二，elaborator 帶回溯搜尋，檔案一大就慢到不可預測。第三，函式庫還是小作坊形態，各自為政，沒有統一的協作紀律。

2016 年夏，Selsam 來實習，與 de Moura 一起打造 blast——一個借用 Z3 技術的 tactic，想證明 SMT 式自動化可以在互動證明器裡落地。同年 8 月 7 日，Avigad 寫信給剛加入的 Ebner：「Lean 3 正在重寫，真的很酷。最大亮點是有一個很快的求值器，Lean 可以當程式語言用，比解譯的 OCaml 和 Python 還快。」Ebner 回問：這是 call-by-value 的堆疊機嗎？——Lean 3 的虛擬機就這樣在通信中定型。

2017 年 1 月 20 日，Lean 3.0  first release，並在 POPL 2017 開教學。這是第一個「中度穩定」的 Lean，也是 mathlib 故事的起點。

## 偵查過程

### 線索一：更簡單的 elaborator，不要回溯式聰明

Lean 3 把 elaborator 簡化了：拿掉大範圍回溯搜尋，改走可預測、可除錯的精製路徑。代價是使用者偶爾要多寫一點註解，收穫是大型檔案的檢查時間變得穩定。這是一次典型的工程取捨：偵探寧可要一把鈍一點但不會卡鞘的刀。

### 線索二：元程式框架——偵探用辦案語言改造警局

Lean 3 的真正兇器是 ICFP 2017 論文《A Metaprogramming Framework for Formal Verification》（Ebner、Ullrich、Roesch、Avigad、de Moura）：tactic、記號、頂層命令全部可以用 Lean 自己來定義。配合高速虛擬機，Lean 第一次變成「可自舉自動化」的系統。

```lean
meta def my_simp : tactic unit := do
  t ← target,
  simp_set ← join_user_simp_lemmas,
  rewrite_search simp_set
```

概念上，每個 tactic 都是 $tactic\, \alpha$ 單子裡的程式，直接讀寫證明狀態。社群隨即爆發： $ring$ 、 $linarith$ 、 $omega$ 的前身、數百個領域 tactic，以及一整包語義 linter（提醒你犯了常見形式化錯誤），全是使用者寫的，不是核心團隊施恩的。

| Lean 2 | Lean 3 |
|------|------|
| tactic 用 Lua 寫，與本體隔閡 | tactic 用 Lean 寫，直達語法樹與證明狀態 |
| 求值靠外部 | 內建高速 VM，Lean 即程式語言 |
| HoTT 可配置核心 | 拿掉 HoTT，專心 CIC＋古典公理相容 |

### 線索三：mathlib——大教堂在市集裡蓋起來

Avigad、Carneiro 等人把函式庫獨立成 mathlib 專案，採用單一 monorepo、嚴格審查、快速迭代的開源紀律。短短幾年從數萬行衝到 Lean 3 末期的逾百萬行，涵蓋代數、拓樸、分析、數論，還長出 Schemes、Perfectoid Spaces、Liquid Tensor 挑戰等硬骨頭專案。mathlib 證明了一件事：形式化數學可以像開源軟體一樣協作。

但 C++ 本體的天花板也浮現了：想改解析器、pretty printer、tactic 框架，幾乎都要動 C++ 原始碼，會 C++ 又懂型別論的人太少；VM 解譯開銷讓高效自動化跑不快。Ebner 英雄般地維持 Lean 3（社群版一路發到 3.51.1），de Moura 卻已決定：下一版，把 Lean 用 Lean 重寫。詳見 [2021-Lean4自舉.md](2021-Lean4自舉.md)。

## 結案報告

Lean 3 破了「社群擴展性」大案：

- **可程式化證明器**：元程式框架讓自動化從核心團隊的特權變成全民運動。
- **mathlib 範式**：集中協作＋嚴格審查＋快速迭代，改寫了 Coq／Isabelle 各自為政的局面，也為日後的 AI 訓練（見 [2024-AlphaProof與AI證明.md](2024-AlphaProof與AI證明.md)）準備了百萬行語料。
- **代價**：C++ 本體＋解譯 VM 的效能與可改性天花板，逼出 Lean 4 的重寫決定。3.4.2 之後官方停止，社群版續命到 3.51.1，功成身退。

探案結語：Lean 3 沒有換警局大樓，但它發給每個警員一套萬能工具組，從此破案速度取決於社群的想像力，而不是局長的批文。

## 證據與工具

**證據一：時間軸**

| 時間 | 事件 |
|------|------|
| 2016 夏 | Selsam 實習，blast tactic；Avigad–Ebner 通信定型 VM |
| 2017-01-20 | Lean 3.0 first release，POPL 2017 教學 |
| 2017 | ICFP 元程式框架論文， $ring$ ／ $linarith$ ／linter 爆發 |
| 2017–2020 | mathlib 從數萬行衝向百萬行；3.4.2 官方收尾，社群版至 3.51.1 |

**證據二：tactic 狀態變遷（概念表）**

| 步驟 | 證明狀態 |
|------|------|
| 初始目標 | $⊢ p ∧ q → q ∧ p$ |
| $intro\, h$ 後 | $h : p ∧ q ⊢ q ∧ p$ |
| $cases\, h$ 後 | $hp : p,\, hq : q ⊢ q ∧ p$ |
| $exact\, ⟨hq,\, hp⟩$ 後 | 無剩餘目標，結案 |

**證據三：偵探工具箱**

| 工具 | 作用 |
|------|------|
| Lean 版 tactic 框架 | ICFP 2017，可自訂語法與命令 |
| 高速 VM | 比解譯 OCaml／Python 快的求值器 |
| mathlib monorepo | 最大最活躍的形式化數學庫前身 |
| Mathport（後期） | 把 Lean 3 證據搬運到 Lean 4 的時光機 |

**延伸閱讀**：Ebner et al., "A Metaprogramming Framework for Formal Verification"（ICFP 2017）；mathlib 官方文件；de Moura《The Making of Lean》Lean 3 章節。
