# 2022：mathlib 移植開始——數學函式庫的大遷徙

## 事件
2022 年 10 月，**mathlib4** 誕生：社群開始把 Lean 3 的 mathlib
（當時已數十萬行、數萬個定理）移植到 Lean 4。這是史上最大規模的
函式庫遷徙之一，於 2023 年 7 月完成，mathlib 正式以 Lean 4 為主幹。

## 為何重要
- **移植的困難**：Lean 4 語法與 Lean 3 相似但不同（tactic 框架重寫、
  `do` 記法改變、命名規範調整）——社群用**機器輔助移植工具**
  （如 `port_mathlib` 腳本）+ 數百人手工接力，逐檔認領、逐檔審查。
- **`@[simp]` 與 attribute 體系移植**：mathlib 的自動化能力高度依賴
  `@[simp]` 引理庫——移植後 Lean 4 的 `simp` 立即獲得整個引理庫。
- **命名規範改革**：移植時統一命名（`norm_num`、`linarith` 等戰術、
  類型別命名），補足 Lean 3 時代命名不一致的缺陷。
- **2022 年也是 Lean 4 穩定化的關鍵年**：里程碑版本 m5/m6、
  增量編譯成熟、`lake` 成為官方建構工具。

## 理論與實用原因
- **理論原因**：mathlib 的價值在於「可重用的數學抽象層次」——
  範疇論 → 代數 → 分析的結構化繼承；移植不只是翻譯語法，
  更是重新設計抽象層次（Lean 4 的 structure eta 讓類型類層次更乾淨）。
- **實用原因**：沒有 mathlib，Lean 4 就只是一個語言；
  數學社群（Fermat 最後定理、LTE 後續）都等著 Lean 4 版的 mathlib。

## 程式範例

**移植前後的語法對照**——同一個定理，Lean 3 vs Lean 4：

```lean
-- Lean 3（mathlib 舊版）：
-- example (n : Nat) : n + 0 = n := by simp
-- def sum : ℕ → ℕ | 0 => 0 | (n+1) => n + 1 + sum n

-- Lean 4（mathlib 移植後）：
example (n : Nat) : n + 0 = n := by simp

def sum : Nat → Nat
  | 0 => 0
  | n + 1 => n + 1 + sum n   -- 模式比對語法改變：(n+1) → n + 1
```

**`@[simp]` 引理庫**——mathlib 的自動化基礎：

```lean
-- mathlib 提供數千條 @[simp] 引理，simp 自動呼叫
@[simp] theorem double_zero : 0 + 0 = 0 := rfl

example (n : Nat) : 0 + 0 + n = n := by simp   -- 用到 double_zero
-- 移植完成後，Lean 4 的 simp 立即獲得整個引理庫
```

**類型類層次**——mathlib 的抽象繼承：

```lean
-- mathlib 的代數層次：Semigroup → Monoid → Group → Ring → Field
class SMul (M : Type u) (α : Type v) where   -- 標量乘法（移植時統一）
  smul : M → α → α

instance : SMul Nat Nat where
  smul := Nat.mul

#eval SMul.smul 3 4   -- 12
```

**逐檔認領的移植流程**：

```bash
# 社群移植工作流（2022 年模式）
git clone https://github.com/leanprover-community/mathlib4
# 認領一個檔案 → 移植 → CI 驗證（零 sorry）→ 審查 → 合併
lake build
```

## 彌補了什麼缺陷
彌補了「Lean 4 有語言無函式庫」的缺陷——mathlib 移植讓 Lean 4
真正可作為數學形式化的主幹；移植過程同時完成命名統一與
抽象層次重設計。

## 相關條目
- [2021-Lean4-VS-Code擴充與Lake](2021-Lean4-VS-Code擴充與Lake.md)
- [2023-Lean-FRO與Lean-4-0-0](2023-Lean-FRO與Lean-4-0-0.md)
