# 2017：Lean 3 與 mathlib 誕生——C++ 前端、元程式設計與社群函式庫

## 事件
2017 年 1 月，**Lean 3** 正式發佈：整個前端（elaborator、parser、
tactic 框架）從 Haskell 重寫成 **C++**，速度提升近十倍。
同年，社群函式庫 **mathlib** 誕生（初名 helper files，後整合為 mathlib），
以及版本管理器 **Elan**（仿 rustup）問世。

## 為何重要
- **C++ 前端重寫**：Lean 2 的 Haskell 前端回應慢，大型證明檔案
  常讓編輯器卡死——重寫後 elaborator 快了十倍，互動式證明變得可用。
- **elaborator 改革**：更好的錯誤訊息、更強的 higher-order unification、
  `structure eta`（結構 η 規則：`S.mk a b = s` 對結構值成立）。
- **`meta def` 元程式設計**：用戶可以直接用 Lean 寫 tactic——
  補足 Lean 2「tactic 只能以 C++ 寫」的缺陷。
- **mathlib**：社群接手數學函式庫，取代官方分散的 `library/` 與
  helper files——統一管理、統一審查，成為史上最大的形式化數學庫的起點。
- **Elan**：每個專案綁定特定 Lean 版本（`lean-toolchain` 檔案的先驅），
  消除版本升級地獄。

## 理論與實用原因
- **理論原因**：`structure eta` 讓「等價推理」更細粒度：兩個結構值相等
  當且僅當每個欄位相等——這是 extensional type theory 的關鍵特性，
  讀取類型別的合理語義。
- **實用原因**：Haskell 前端的效能瓶頸是 Lean 2 最大的痛；
  數學函式庫分散在官方與個人 repo，重複與版本不一致——mathlib 統一解決。

## 程式範例

**`meta def` 元程式設計**——Lean 3 讓你用 Lean 本身寫 tactic：

```lean
-- Lean 3：meta def 可以繞過型別檢查，直接操作證明狀態
meta def my_tactic : tactic unit :=
do tgt ← target,
   tactic.trace tgt,          -- 把目標印出來
   applyc `and.intro          -- 套用 and.intro

-- Lean 4 的同樣概念（對照）：
-- syntax "my_tac" : tactic
-- macro_rules | `(my_tac) => `(tactic (trace_state))
```

**structure eta**——結構值相等由欄位決定：

```lean
structure Point where
  x : Nat
  y : Nat

theorem point_eta (p : Point) : Point.mk p.x p.y = p := rfl
-- eta 規則讓「重建結構 = 原值」恆成立，這在 Lean 2 不成立
```

**type class 解析與 instance 問題**：

```lean
class Monoid (α : Type) where
  mul : α → α → α
  one : α

instance NatMulMonoid : Monoid Nat where
  mul := Nat.mul
  one := 1

#check Monoid.mul 20 10   -- 解析到 NatMulMonoid——type class 推理
```

**mathlib 風格的定理**——2017 年 mathlib 奠定的命名與組織風格：

```lean
-- mathlib 命名規範：thm 名稱用 snake_case，按數學主題分目錄
-- data/nat/basic.lean、algebra/group/basic.lean ...
theorem add_comm' (a b : Nat) : a + b = b + a := Nat.add_comm a b
```

**Elan 與 leanpkg**——專案綁定版本：

```toml
# leanpkg.toml（Lean 3 時代，Lake 的前身）
[package]
name = "myproj"
version = "0.1.0"
[dependencies]
mathlib = { git = "https://github.com/leanprover-community/mathlib" }
```

```bash
# Elan：安裝與切換 Lean 版本（仿 rustup）
elan toolchain install leanprover-community/lean-3.42.1
```

## 彌補了什麼缺陷
彌補了 Lean 2「Haskell 前端效能瓶頸、tactic 無法由用戶以 Lean 撰寫、
數學函式庫分散重複」的缺陷——Lean 3 用 C++ 重寫、`meta def`、
mathlib 三箭齊發，讓數學社群真正開始聚集。

## 相關條目
- [2016-VS-Code擴充與Lean3預覽](2016-VS-Code擴充與Lean3預覽.md)
- [2019-Lean-4構想與自舉宣言](2019-Lean-4構想與自舉宣言.md)
