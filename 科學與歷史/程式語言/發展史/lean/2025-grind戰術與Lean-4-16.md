# 2025：grind 戰術與 Lean 4.16——E-graph 自動化時代

## 事件
2025 年 3 月，Lean 4.16 發佈，引入新一代自動化戰術 **`grind`**——
基於 **E-graph（等價圖，E-matching）** 與 SMT 技術的統一自動化引擎，
目標是整合 `simp`、`omega`、`aesop`、`sat` 的能力，成為 Lean 的
「一鍵自動化」。同年，**`bv_decide`**（4.15，2025-01）穩定：
基於位元向量（bit-vector）SMT 的決策程序。

## 為何重要
- **`grind` 戰術**：
  - 以 E-graph 統一等價推理：`simp` 的改寫、`omega` 的線性算術、
    類型類解析的結果都放進同一張等價圖——補足 Lean 4 之前
    「自動化戰術各自為政、要手動組合」的缺陷。
  - 支援 `@[grind]` 標記：引理像 `@[simp]` 一樣供 `grind` 使用，
    自動化覆蓋率隨函式庫成長。
- **`bv_decide`**：位元向量算術（CPU 指令的語義）直接呼叫
  SAT/SMT 後端——補足「驗證低階程式（編譯器、加密）時
  位元運算自動化缺失」的缺陷。
- **2025 年的大型形式化**：Fermat 最後定理專案（FLT blueprint）、
  Perfect Numbers 專案相繼啟動——Lean 已能承載史上最大的數學
  形式化目標。

## 理論與實用原因
- **理論原因**：E-graph 的理論基礎是 congruence closure 演算法
  （Nelson–Oppen 1980）與 E-matching（de Moura 的 Z3 前作）——
  等價關係的閉包可以高效表示與查詢；`grind` 把 congruence closure
  從 Z3 帶回 Lean 本體。
- **實用原因**：自動化是形式化生產力的決定因素；
  `simp`/`omega`/`aesop` 各有盲區，組合使用靠人工——
  `grind` 用 E-graph 統一，一鍵解決更多目標。

## 程式範例

**`grind` 戰術**——E-graph 統一自動化：

```lean
-- grind：整合 simp/omega 的能力，一鍵自動化
example (a b : Nat) (h : a = b) : a + 0 = b := by grind

-- @[grind] 標記的引理供 grind 使用
@[grind] theorem double_zero (n : Nat) : 0 + n = n := Nat.zero_add n

example (a b c : Nat) (h1 : a = b) (h2 : b = c) : a + c = c + b := by
  grind   -- E-graph 自動推出 a = c，等價閉包一次完成

-- 對照：Lean 4.16 之前要手動組合多個戰術
-- example ... := by simp only [...]; omega; exact ...
```

**`bv_decide`**——位元向量決策：

```lean
-- 位元運算的自動化：CPU 指令語義的驗證
open Lean.Grind in
example : (5 : UInt8) &&& 3 = 1 := by
  decide   -- bv_decide/decide 呼叫位元向量求解

example (x : UInt8) : x ||| 0 = x := by
  bv_decide   -- 位元向量 SMT 後端
```

**E-graph 的精神**——等價閉包的高效表示：

```lean
-- E-graph 把「a = b」「b = c」的等價閉包存成一張圖，
-- 任何表達式查詢等價類只需常數時間——這是 congruence closure
-- 的核心思想（Nelson–Oppen 1980，de Moura 的 Z3 淵源）

example (f : Nat → Nat) (a b : Nat) (h : a = b) :
    f a = f b := by grind   -- 全等閉包（congruence）自動推出
```

**Fermat 最後定理專案**——2025 年的最大形式化：

```lean
-- FLT blueprint 風格：把大定理拆成數千個 lemma 逐格認領
-- theorem fermat_last (n : Nat) (hn : n > 2) :
--     ∀ (a b c : Nat), a ^ n + b ^ n ≠ c ^ n := by
--   -- 數千個輔助引理，社群接力中
--   sorry
```

## 彌補了什麼缺陷
彌補了 Lean 4「自動化戰術各自為政、位元運算自動化缺失」的缺陷——
`grind` 用 E-graph 統一自動化、`bv_decide` 補上低階驗證，
自動化覆蓋率成為 Lean 生態的核心競爭力。

## 相關條目
- [2024-Reservoir與生態擴張](2024-Reservoir與生態擴張.md)
- [2026-未來展望](2026-未來展望.md)
