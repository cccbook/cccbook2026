# 2023：Lean FRO 與 Lean 4.0.0——穩定版、mathlib 移植完成與 omega

## 事件
2023 年是 Lean 的轉折年：
- 1 月，**Lean FRO（Formal Reasoning Organization）** 成立——
  由 **Amazon Web Services（AWS）** 贊助，Leonardo de Moura 擔任負責人，
  承諾長期投入 Lean 4 的語言與工具鏈開發。
- 9 月，**Lean 4.0.0** 穩定版正式發佈（結束 2021–2023 的 milestone 時代），
  之後改以 4.x 小步快跑（每月一版）。
- 7 月，**mathlib 完成 Lean 4 移植**——mathlib 正式以 Lean 4 為主幹，
  Lean 3 進入維護模式。
- **`omega` 戰術**（Lean 4.7，2023）問世：線性算術自動化，取代
  `linarith` 處理 `Nat`/`Int` 的線性不等式。

## 為何重要
- **Lean FRO**：補足「學術專案靠個人熱情、經費不穩」的缺陷——
  AWS 的贊助讓 Lean 有專職工程師，語言演進變成工業級承諾
  （類比 Rust 基金會 2020、OCaml Labs）。
- **Lean 4.0.0 穩定承諾**：milestone 時代每個版本都可能破壞相容；
  4.0.0 之後「向後相容」成為規範，大型專案（mathlib、企業採用）才敢投入。
- **`omega`**：`linarith` 基於實數線性代數，處理 `Nat`/`Int` 的
  整數溢出與自然數減法時常失敗；`omega` 基於 Presburger 算術的
  Omega 測試（Cooper 1972），原生理解 `Nat` 的截斷減法——
  補足整數線性算術自動化的缺口。

## 理論與實用原因
- **理論原因**：`omega` 的理論基礎是 Presburger 算術的可判定性
  （1929 年 Presburger 證明）與 Cooper 演算法（1972）——
  線性整數算術是可判定的，可以完全自動化。
- **實用原因**：`linarith` 在 `Nat` 減法（截斷）上屢屢失敗；
  數學形式化中最常見的目標就是線性不等式——自動化覆蓋率
  直接決定形式化生產力。

## 程式範例

**`omega` 戰術**——線性整數算術完全自動化：

```lean
-- omega 原生理解 Nat 截斷減法與不等式
example (a b : Nat) (h : a ≤ b) : a - b = 0 := by omega
example (a b : Int) (h1 : a < b) (h2 : b < c) : a < c := by omega
example (n : Nat) : n - n = 0 := by omega

-- 對照：linarith 在 Nat 截斷減法上失敗
-- example (a b : Nat) (h : a ≤ b) : a - b = 0 := by linarith  -- 失敗！
```

**Lean 4.0.0 的穩定語法**——之後向後相容：

```lean
-- Lean 4.0.0（2023-09）定型的核心語法
structure P where
  x : Nat
  y : Nat

theorem eta (p : P) : P.mk p.x p.y = p := rfl

def main : IO Unit do
  IO.println s!"Lean {Lean.versionString}"
```

**Lean FRO 的意義**——語言演進的工業級承諾：

```bash
# 2023 之後：每月一版的 4.x 小步快跑（對照 milestone 時代）
elan toolchain install leanprover/lean4:v4.7.0   # 2023-12: omega 問世
```

**mathlib 移植完成的生態效果**——Lean 4 正式成為數學主幹：

```lean
import Mathlib            -- mathlib 已完全在 Lean 4 上

example (a b : Nat) : a * b = b * a := Nat.mul_comm a b
-- 數十萬定理、數百萬行證明，全部在 Lean 4
```

## 彌補了什麼缺陷
彌補了「學術專案經費不穩、無長期承諾」的缺陷（Lean FRO）、
「milestone 時代相容性破壞」的缺陷（4.0.0）、以及
「Nat/Int 線性算術自動化失敗」的缺陷（`omega`）——
2023 年三箭齊發，Lean 從學術專案變成工業級基礎設施。

## 相關條目
- [2022-mathlib移植開始](2022-mathlib移植開始.md)
- [2024-Reservoir與生態擴張](2024-Reservoir與生態擴張.md)
