# 2024：Reservoir 與生態擴張——套件庫、partial def 與可驗證軟體

## 事件
2024 年，Lean 生態全面擴張：
- **Reservoir** 上線——Lean FRO 官方的套件（package）註冊處，
  補足 Lean 4 生態「缺乏中央套件庫」的缺陷（類比 crates.io 之於 Rust）。
- **`partial def` 成熟**：允許無法證明終止的定義（如操作 IO、
  寫直譯器時的迴圈），編譯器以虛擬碼 + 檢查生成。
- **VFML（Verified Field ML）與機器學習形式化**：Lean 開始用於
  驗證機器學習系統（如 Amazon 的 Lean 驗證專案）。
- Lean 4.x 持續每月小步快跑（4.1–4.9+），`@[deprecated]`、
  `deriving` handler、`@[grind]` 前身等工具陸續加入。

## 為何重要
- **Reservoir**：Lean 4 之前套件散落 GitHub，缺乏版本鎖定與
  安全審查——Reservoir 提供中央註冊、語義化版本、依賴解析，
  補足「數學函式庫強大但通用軟體生態薄弱」的缺陷。
- **`partial def`**： Lean 4 要求遞迴必須證明終止（良基或結構遞迴），
  但有些定義終止性不可判定（如 `while` 迴圈、直譯器）——
  `partial def` 讓「程式語言 Lean」與「證明器 Lean」各取所需。
- **企業採用**：AWS 用 Lean 驗證內部系統、數學形式化專案
  （如 2024 年的 Prime Number Theorem、Fermat 最後定理預備工作）
  選擇 Lean——證明助手首次進入「可驗證軟體工程」。

## 理論與實用原因
- **理論原因**：`partial def` 的理論基礎是「部分函式」（partial
  functions）：以額外的 `Inhabited` 假設與惰性值實現，代價是
  該定義不能用在證明中的計算規約——明確區分「可計算的證明物件」
  與「可執行的程式」。
- **實用原因**：通用程式設計需要迴圈與遞迴；要求每個 def 都證明
  終止會嚇跑普通程式設計師——`partial def` 是「證明器」與
  「通用語言」的妥協。

## 程式範例

**`partial def`**——不需要證明終止的定義：

```lean
-- partial def：允許無法證明終止的遞迴（如直譯器的主迴圈）
partial def evalLoop (env : String → Nat) (e : Expr) : Nat :=
  match e with
  | .lit n => n
  | .var x => env x
  | .add a b => evalLoop env a + evalLoop env b
  | .loop a => evalLoop env (Expr.loop a)  -- 可能不終止

inductive Expr where
  | lit : Nat → Expr
  | var : String → Expr
  | add : Expr → Expr → Expr
  | loop : Expr → Expr
```

**Reservoir 風格的依賴管理**——中央套件庫：

```bash
# Reservoir（2024）：中央套件註冊處（類比 crates.io）
lake update   # 解析 lakefile.lean 的依賴，鎖定版本到 lake-manifest.json
```

```lean
-- lakefile.lean：依賴 Reservoir 上的套件
require verso from git "https://github.com/leanprover/verso"
```

**運算子重載與 deriving**——Lean 4 通用語言化的證明：

```lean
structure Vec2 where
  x : Nat
  y : Nat
deriving Repr, BEq, DecidableEq   -- 自動生成實作（Lean 4 的 deriving handler）

instance : Add Vec2 where
  add a b := ⟨a.x + b.x, a.y + b.y⟩

instance : ToString Vec2 where
  toString v := s!"({v.x}, {v.y})"

#eval ⟨1, 2⟩ + ⟨3, 4⟩   -- (4, 6)
```

**可驗證軟體**——規格與實作同一份程式碼：

```lean
-- Lean 4：函式帶著前置/後置條件（型別層面）
def safeHead (as : Array α) (h : as.size > 0) : α :=
  as[0]   -- 需要證明 0 < as.size——越界在編譯期被消滅
```

**對照：Python 的缺陷**——越界與型別錯誤執行期才爆：

```python
def head(xs):
    return xs[0]   # 空陣列時 IndexError，執行期才爆
```

## 彌補了什麼缺陷
彌補了「Lean 4 缺乏中央套件庫」（Reservoir）、「部分函式無法
表達」（`partial def`）、「證明器與通用語言身份衝突」的缺陷——
2024 年 Lean 正式成為「可驗證軟體工程」的通用語言。

## 相關條目
- [2023-Lean-FRO與Lean-4-0-0](2023-Lean-FRO與Lean-4-0-0.md)
- [2025-grind戰術與Lean-4-16](2025-grind戰術與Lean-4-16.md)
