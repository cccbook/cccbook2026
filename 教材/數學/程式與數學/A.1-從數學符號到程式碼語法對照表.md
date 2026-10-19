# 附錄 A：從數學符號到程式碼語法對照表

> 程式設計與數學的關鍵之一，在於兩者使用「不同的表層語法」表達「相同的深層結構」。本附錄提供一份對照字典，幫助讀者在閱讀論文與撰寫程式之間自由切換。

## A.1.1 邏輯符號

| 數學符號 | 讀法 | Haskell / Lean 語法 | 備註 |
|---|---|---|---|
| $\top$ | 真 | `True` / `True` | 空命題的證明只有一個 |
| $\bot$ | 假 | `False` / `False` | 在 Curry–Howard 下對應 `Void` 型別 |
| $P \land Q$ | 且 | `(P, Q)` | 積型別，證明是「一對證明」 |
| $P \lor Q$ | 或 | `Either P Q` | 和型別，證明是「二選一的證明」 |
| $P \Rightarrow Q$ | 蘊含 | `P -> Q` | 函數型別即蘊含 |
| $\neg P$ | 非 | `P -> Void` | 定義為蘊含矛盾 |
| $\forall x \in A$ | 全稱量化 | `forall x, P x` | 多型函數 |
| $\exists x \in A$ | 存在量化 | `Σ x, P x` | 依賴積型別 |
| $P \leftrightarrow Q$ | 若且唯若 | `(P -> Q, Q -> P)` | 兩方向的蘊含 |

## A.1.2 集合與型別建構

| 數學 | 說明 | Haskell | Lean |
|---|---|---|---|
| $\{0,1,\dots\}$ | 自然數 | `data Nat = Z \| S Nat` | `inductive Nat` |
| $A \times B$ | 卡氏積 | `(a, b)` | `Prod A B` |
| $A + B$ | 不相交聯集 | `Either a b` | `Sum A B` |
| $A^B$ | 函數空間 | `b -> a` | `B -> A` |
| $A \cong B$ | 同構 | `newtype` + 兩向轉換 | `Equiv` / `Iso` |

## A.1.3 常用恆等式與其程式對應

$$
(A \times B) \times C \cong A \times (B \times C)
$$

→ tuple 嵌套順序無關緊要（結合律）。

$$
A^{B \times C} \cong (A^B)^C
$$

→ 柯里化：`curry :: ((a, b) -> c) -> a -> b -> c`

$$
(A + B) \times C \cong A \times C + B \times C
$$

→ case 表達式（分配律）：對和型別分支處理。

## A.1.4 λ 演算與程式碼

| 數學 | Haskell | Python |
|---|---|---|
| $\lambda x. x$ | `\x -> x` | `lambda x: x` |
| $(\lambda x. t)\ u$ | `(\x -> t) u` | `(lambda x: t)(u)` |
| $\text{let}\ x = u\ \text{in}\ t$ | `let x = u in t` | `x = u`（再使用） |
| $\mu f. f$（遞迴） | `fix f = f (fix f)` | 需明確命名 |

## A.1.5 量詞與依賴型別

在依賴型別語言中，命題本身就是型別：

```lean
-- ∀ n : Nat, n + 0 = n
example (n : Nat) : n + 0 = n := by simp

-- ∃ n : Nat, n * n = 25
example : ∃ n : Nat, n * n = 25 := ⟨5, by rfl⟩
```

## 小結

掌握這張對照表，讀者即可在「讀數學論文」與「寫型別化程式」之間雙向翻譯——這正是本書強調的：**兩者是同一套數學結構的兩種表層語法**。
