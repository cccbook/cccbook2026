# A1 Lean 符號與 tactic 速查

## 本章導讀

這是全書的口袋卡，忘記符號或 tactic 時回來翻一頁就好。
內容只有三張大表加一段小抄：型別符號表、邏輯符號表、常用 tactic 表。
搭配最後的使用提示，保證你在證明卡關時三十秒內找到逃生門。

## 淺顯說明

背 Lean 符號不用死背，只要記三大家族。
型別家族管程式的身分證，邏輯家族管命題的連接詞，tactic 家族管證明的動作。
看到 $Nat$ 就想到數，看到 $p \to q$ 就想到 $intro$ ，看到卡住就想到 $simp$ 。

小訣竅是把符號和 tactic 綁在一起記： $forall$ 配 $intro$ ， $exists$ 配 $use$ ，
等號配 $rw$ 與 $rfl$ ，歸納配 $induction$ ，算術配 $omega$ 與 $ring$ 。
這樣三張表就串成一張網，查一處就能牽出另一處。

## 正規理論

核心判斷仍是同一條，只是換個角度速記：

$$
\Gamma \vdash e : \alpha
$$

讀作在上下文 $Gamma$ 中，項 $e$ 的型別是 $alpha$ 。
命題即型別的口訣則是：

$$
Proof(p) \simeq p
$$

型別符號速查表如下：

| 符號 | 讀法 | 意義 | 例子 |
|------|------|------|------|
| $Type$ | 型別宇宙 | 所有型別的家 | $Nat : Type$ |
| $Prop$ | 命題宇宙 | 證明無關的命題 | $True : Prop$ |
| $Nat$ | 自然數 | 非負整數 | $0$ 、 $1$ 、 $42$ |
| $Int$ | 整數 | 可負整數 | $-3$ 、 $7$ |
| $List$ | 串列 | 同型別序列 | $[1, 2]$ |
| $Option$ | 可空值 | 有或無 | $none$ 、 $some \; 3$ |
| $\to$ | 函數箭頭 | 函數與蘊涵 | $Nat \to Nat$ |
| $\times$ | 積型別 | 二元組 | $Nat \times Bool$ |

邏輯符號速查表如下：

| 符號 | 讀法 | 對應 tactic | 備註 |
|------|------|-------------|------|
| $\to$ | 蘊涵 | $intro$ 、 $apply$ | $p \to q$ 即函數 |
| $\forall$ | 全稱 | $intro$ 引入， $apply$ 使用 | $\forall x, P(x)$ |
| $\exists$ | 存在 | $use$ 給見證， $cases$ 消去 | $\exists x, P(x)$ |
| $\land$ | 合取 | $constructor$ 、 $cases$ | $p \land q$ 即 pair |
| $\lor$ | 析取 | $left$ 、 $right$ 、 $cases$ | $p \lor q$ 即 sum |
| $\lnot$ | 否定 | 展開為 $p \to False$ | $\lnot p$ 即 $p \to False$ |
| $=$ | 相等 | $rfl$ 、 $rw$ 、 $simp$ | 同構代換的起點 |
| $False$ | 假 | $False.elim$ | 由假可得一切 |

常用 tactic 速查表如下：

| tactic | 用途 | 典型時機 | 小抄 |
|--------|------|----------|------|
| $intro$ | 引入假設 | 目標是 $p \to q$ 或 $forall$ | $intro \; h$ 取名 |
| $apply$ | 後向推理 | 目標恰為某引理結論 | $apply \; h$ 倒推 |
| $exact$ | 精準命中 | 恰有同型別假設 | $exact \; h$ 結束 |
| $rw$ | 重寫 | 有等式可用 | $rw \; [h]$ 代換 |
| $simp$ | 化簡 | 雜項清理 | $simp$ 或 $simp \; only$ |
| $cases$ | 分類拆解 | 析取、存在、歸納型別 | $cases \; h$ 分岔 |
| $induction$ | 歸納 | 自然數與遞迴結構 | $induction \; n$ 兩步 |
| $use$ | 給見證 | 目標是 $exists$ | $use \; 3$ 舉例 |
| $rfl$ | 自反 | 兩邊定義相等 | $rfl$ 一鍵 |
| $omega$ | 線性算術 | 整數不等式 | $omega$ 自動 |
| $ring$ | 環等式 | 含加乘冪 | $ring$ 展開比對 |

## 簡易範例

把三張表串起來的小綜合，用一行註解標出每步查的是哪張表。

```lean
-- 邏輯符號 + intro / exact
example (p q : Prop) (h : p) : p ∧ q → p := by
  intro _hq
  exact h

-- 相等 + rw / rfl
example (a : Nat) : a + 0 = a := by
  rw [Nat.add_zero]
  rfl

-- 存在 + use，算術 + omega / ring
example : ∃ n : Nat, n + 2 = 5 := by
  use 3
  omega

example (a b : Int) : (a + b) ^ 2 = a ^ 2 + 2 * a * b + b ^ 2 := by
  ring

-- 歸納 + simp 收尾
example (n : Nat) : n + 0 = n := by
  induction n with
  | zero => rfl
  | succ k ih => simp [ih]
```

遇到新目標時，先看目標主連接詞，再到 tactic 表找對應行，這就是查表的正確姿勢。

## 歷史典故

速查表的背後是兩段濃縮的歷史。
先看 [Lean 誕生](../2013-Lean誕生.md) ，它決定把數學符號直接做成 Unicode 輸入， $forall$ 、 $exists$ 、 $to$ 才能在編輯器裡漂亮呈現。

再看 [Lean3 與 mathlib](../2017-Lean3與mathlib.md) 。
mathlib 把上表的 tactic 打磨成統一風格， $simp$ 集、 $omega$ 、 $ring$ 都是在那個時期定型的。

若想展望未來，可加讀 [AlphaProof 與 AI 證明](../2024-AlphaProof與AI證明.md) 。
當 AI 也開始查同一張表，你會發現人類速查與機器搜尋用的是同一套詞彙。

## 使用提示

1. 證明卡住先看目標形狀：箭頭用 $intro$ ，等號用 $rw$ ，存在用 $use$ ，歸納用 $induction$ 。
2. 自動化有順序：先 $simp$ 清理，再 $ring$ 或 $omega$ 收尾，不要一開始就亂槍打鳥。
3. $simp$ 失控時退回 $simp \; only$ ，一次只加一條引理，用 $trace_state$ 觀察變化。
4. 符號打不出來時，在 VS Code 輸入反斜線加英文，如 `\forall` 補全為 $forall$ ， `\to` 補全為 $to$ 。
5. 把本頁加入書籤，每次寫證明前花十秒掃一次 tactic 表，久了就會內化成直覺。
