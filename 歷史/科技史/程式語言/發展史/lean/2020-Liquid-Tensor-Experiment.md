# 2020：Liquid Tensor Experiment——形式化數學的里程碑

## 事件
2020 年 12 月，菲爾茲獎得主 **Peter Scholze** 在 mathlib 社群發起
**Liquid Tensor Experiment（LTE）**：請社群以 Lean/mathlib 形式化
他與 Clausen 的「凝聚數學（condensed mathematics）」中一個他最不確定的
關鍵定理（Liquid vector spaces 的消失定理）。核心部分於 2021 年 6 月完成，
完整形式化在 2022 年 7 月收工。

## 為何重要
- **數學家親自背書**：Scholze 說「這是我在數學上最緊張的證明之一」——
  形式化完成意味著連頂尖數學家都需要機器檢查的證明，Lean/mathlib
  的表達力與自動化已能應付前沿研究數學。
- **證明助手的工業級考驗**：LTE 牽涉範疇論、同調代數、拓樸——
  需要數萬行依賴、龐大的 `import` 圖與 `@[simp]` 庫——
  這直接暴露了 Lean 3 的**效能瓶頸**（檔案太大、elaborator 太慢），
  成為 Lean 4 移植的最大動力之一。
- **社群協作模式**：LTE 由數十人接力（Scholze 寫 blueprint、
  Johan Commelin 領軍、社群分工作業）——「blueprint + 逐格認領」
  成為之後大型形式化專案（如 Fermat 最後定理專案）的標準作業模式。

## 理論與實用原因
- **理論原因**：凝聚數學把拓樸與代數統一（analytic/condensed 的
  範疇等價），證明依賴深層的範疇論機器——正是依賴型別理論的
  強項：範疇、極限、同調都是普通的依賴結構。
- **實用原因**：Scholze 想知道「這個證明到底對不對」——
  人類審查已經不夠；形式化是唯一完全可信的檢查。

## 程式範例

**LTE 的形式化風格**——範疇論與同調代數是普通依賴結構：

```lean
-- mathlib 風格：範疇、函子、自然變換都是型別
universe v u

class Category (Obj : Type u) where
  Hom : Obj → Obj → Type v
  id (X : Obj) : Hom X X
  comp : Hom X Y → Hom Y Z → Hom X Z

-- 極限與短正合列——LTE 的基本積木
-- class Abelian (C : Category) where ...
-- theorem Liquid_tensor_theorem : ...（LTE 的主定理，數千行）

-- 「逐格認領」的 blueprint 風格：每個 lemma 對應藍圖的一格
theorem aux_lemma (M : Type) [AddCommGroup M] (h : ...) :
    CondensedOfModule.of M = ... := by
  -- 需要之前的十幾個輔助引理——社群接力完成
  sorry  -- LTE 過程中用 sorry 標記未完成格，最後全部消滅
```

**`sorry` 的文化**——未完成格明確標記，整庫必須零 sorry：

```lean
-- sorry 是「這裡有洞」的顯式標記，kernel 不會接受含 sorry 的
-- 定理作為最終證明；mathlib 的 CI 會追蹤並消滅所有 sorry
theorem unfinished (n : Nat) : n + 0 = n := by sorry  -- 必須補完
```

**效能壓力**——LTE 的依賴圖直接推動 Lean 4：

```lean
-- Lean 3 時代：import 數百個 mathlib 檔案，elaborator 要跑數分鐘
-- import Mathlib.Analysis...

-- 這正是 2021 年 Lean 4 移植的最大動力：
-- 自舉編譯器 + 增量編譯（incremental recompilation）
```

## 彌補了什麼缺陷
彌補了「人類審查無法完全確認前沿研究數學證明」的缺陷，也暴露並
推動解決了 Lean 3「大型依賴圖下 elaborator 效能不足」的缺陷——
LTE 之後，Lean 4 的移植與增量編譯成為最高優先。

## 相關條目
- [2017-Lean-3與mathlib誕生](2017-Lean-3與mathlib誕生.md)
- [2021-Lean-4問世](2021-Lean-4問世.md)
