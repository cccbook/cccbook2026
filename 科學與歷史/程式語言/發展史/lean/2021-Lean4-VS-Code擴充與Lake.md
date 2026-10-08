# 2021：Lean 4 VS Code 擴充與 Lake——新一代工具鏈

## 事件
2021 年，隨 Lean 4 問世，官方推出全新的 **Lean 4 VS Code extension**
（`vscode-lean4`，取代 Lean 3 時代的 `vscode-lean`），並發佈
**Lake**（Lean Make，宣告式建構工具）取代 `leanpkg` + Makefile。

## 為何重要
- **Lean 4 VS Code extension**：
  - 基於 Lean 4 內建的 **LSP server**（本身是 Lean 程式）——
    編輯器與編譯器同一套程式碼，補足 Lean 3「extension 與編譯器
    分別維護」的缺陷。
  - **InfoView 重寫**：目標面板、假設區、診斷訊息互動摺疊；
    游標移動即時顯示證明狀態。
  - **逐行證明除錯**：像除錯程式一樣逐步執行 tactic。
- **Lake**：`lakefile.lean` 用 Lean 語法本身寫建構腳本——
  補足 `leanpkg` + Make「兩套語法、跨平台問題多」的缺陷。
- **Elan 持續演化**：`lean-toolchain` 檔案成為專案標準，
  Lean 3/Lean 4 可並存切換。

## 理論與實用原因
- **理論原因**：LSP 的本質是「把編輯器能力與語言服務分離」——
  與 LCF 傳統「把證明檢查與 tactic 產生分離」同一哲學：介面與核心解耦。
- **實用原因**：Lean 3 的 extension 要處理 C++/Haskell 兩種後端、
  通訊協定自訂；Lean 4 把 LSP server 寫進語言本體，extension 變薄。
  建構系統用 Makefile 在 Windows 上是噩夢——Lake 用 Lean 語法跨平台。

## 程式範例

**Lake 的 lakefile.lean**——建構腳本就是 Lean 程式：

```lean
-- lakefile.lean：宣告式依賴與建構目標，語法就是 Lean
import Lake
open Lake DSL

package myproj

@[default_target]
lean_lib Myproj

@[default_target]
lean_exe runner where
  root := `Main

require mathlib from git
  "https://github.com/leanprover-community/mathlib" @ "master"
```

```bash
# Lake 常用指令（對照 Makefile/leanpkg 的複雜性）
lake build          # 建構整個專案與依賴
lake env lean Main.lean   # 在專案環境下檢查單檔
lake exe runner           # 執行編譯後的可執行檔
```

**VS Code extension 的 InfoView**——逐行證明除錯：

```lean
theorem mult_comm (a b : Nat) : a * b = b * a := by
  -- InfoView 顯示：⊢ a * b = b * a
  induction a with
  | zero =>
    -- InfoView：⊢ 0 * b = b * 0
    simp
  | succ n ih =>
    -- InfoView：⊢ (n+1) * b = b * (n+1)
    --            ih : n * b = b * n
    simp [Nat.succ_mul, ih]
```

**Elan 與 lean-toolchain**——版本並存：

```bash
# 專案根目錄的 lean-toolchain 檔案：一行指定版本
# leanprover/lean4:v4.15.0

elan toolchain install leanprover/lean4:v4.15.0
elan default leanprover/lean4:v4.15.0
```

**對照：Lean 3 工具鏈的缺陷**：

```bash
# Lean 3 時代：leanpkg + Makefile + 自訂通訊協定
leanpkg build       # 底層叫 make，Windows 支援差
# extension 要分別處理 C++ (lean) 與 Haskell 後端的訊息格式
```

## 彌補了什麼缺陷
彌補了 Lean 3 時代「extension 與編譯器分別維護、建構系統依賴
Makefile（跨平台差）、版本管理混亂」的缺陷——Lean 4 的
vscode-lean4 + Lake + Elan 形成與 Rust（rust-analyzer + Cargo +
rustup）對等的一體化工具鏈。

## 相關條目
- [2021-Lean-4問世](2021-Lean-4問世.md)
- [2022-mathlib移植開始](2022-mathlib移植開始.md)
