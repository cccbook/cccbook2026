# 2016：VS Code 擴充與 Lean 3 預覽——編輯器即證明介面

## 事件
2016 年，Lean 社群推出首個 **VS Code extension**（`vscode-lean`，
由 Gabriel Ebner 等人開發），並開始預告 **Lean 3**。這是 Lean 工具鏈
「editor 即證明互動介面」的起點，也首次以 **Language Server Protocol（LSP）**
作為編輯器與 Lean 之間的橋樑。

## 為何重要
- **VS Code extension（vscode-lean）**：語意高亮、即時錯誤提示、
  **Goal 面板**——把游標放在證明腳本某一行，就能看到「目前目標」與
  「可用假設」，證明從盲寫變成互動。
- **LSP 協定導入**：編輯器支援不再硬綁特定 IDE——補足 Coq
  （Proof General 只支援 Emacs）與 Isabelle（jEdit 綁定）的缺陷。
- **`#check`/`#eval`/`#print` 除錯指令**：把 REPL 式的探索帶進編輯器。
- **2016 年也是 Lean 3 前端重寫的開始**：C++ 前端讓回應速度大幅提升，
  為互動式證明提供必要的效能。

## 理論與實用原因
- **理論原因**：互動式定理證明的本質是「證明狀態的探索」——
  LCF 傳統的 tactic 就是狀態轉移函式，編輯器必須把這個狀態視覺化。
- **實用原因**：Coq/Isabelle 的 IDE 體驗是初學者的最大門檻；
  2016 年 VS Code 成長迅速，Lean 選擇站上成長最快的平台。

## 程式範例

**Goal 面板所看到的東西**——逐行探索證明狀態：

```lean
theorem swap_add (a b : Nat) : a + b = b + a := by
  -- 游標在這一行時，Goal 面板顯示：
  --   ⊢ a + b = b + a
  induction a with
  | zero =>
    --   ⊢ 0 + b = b + 0
    simp
  | succ n ih =>
    --   ⊢ (n + 1) + b = b + (n + 1)    （ih : n + b = b + n 也在假設區）
    simp [Nat.succ_add, ih]
```

**`#check`/`#eval`/`#print`**——REPL 式除錯，結果直接顯示在編輯器：

```lean
#check @Nat.add_comm        -- Nat.add_comm : ∀ (n m : ℕ), n + m = m + n
#eval 2 + 2                 -- 4
#print Nat.add_comm         -- 顯示定理的完整證明項（proof term）
```

**泛用符號輸入**——vscode-lean 的「輸入數學符號」：

```lean
-- 輸入 \forall → ∀、\to → →、\and → ∧：數學符號直接打字
example : ∀ (P Q : Prop), P ∧ Q → Q ∧ P := by
  intro P Q ⟨hp, hq⟩
  exact ⟨hq, hp⟩
```

**對照：Coq 的 IDE 缺陷**——Proof General 綁 Emacs、CoqIDE 陽春：

```coq
(* Coq：Proof General 只在 Emacs，初學者門檻極高；
   錯誤訊息與目標面板分散在不同視窗 *)
Lemma swap : forall a b, a + b = b + a.
```

## 彌補了什麼缺陷
彌補了 Coq/Isabelle「IDE 綁定特定平台、證明狀態探索不直觀」的缺陷——
Lean 用 VS Code extension + LSP，讓任何支援 LSP 的編輯器都能變成
證明互動介面。

## 相關條目
- [2017-Lean-3與mathlib誕生](2017-Lean-3與mathlib誕生.md)
- [2021-Lean4-VS-Code擴充與Lake](2021-Lean4-VS-Code擴充與Lake.md)
