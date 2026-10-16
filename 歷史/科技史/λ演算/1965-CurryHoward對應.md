# 15. 1965 — William Howard 系統化 Curry–Howard 對應

## 案件摘要

1965 年，William Howard 在論文 *The Formulae-as-Types Notion of Construction*（1969 年正式出版）中首次系統化地提出「命題即型別、證明即程式」的對應。這個發現把邏輯與計算合而為一：一個證明就是一個 λ 項，一個型別就是一個命題，型別檢查就是證明檢查。這是理論計算機科學史上最深刻的橋樑。

## 前因 -- 為什麼會有這個案子

線索可以追溯到幾個源頭：

1. **1934 年，Haskell Curry** 觀察到 Hilbert 系統的組合子公理與直覺邏輯公理的形狀相同：
   - 組合子 $I = \lambda x.\, x$ 對應公理 $A \to A$；
   - 組合子 $K = \lambda x.\, \lambda y.\, x$ 對應公理 $A \to (B \to A)$；
   - 組合子 $S = \lambda x.\, \lambda y.\, \lambda z.\, x\ z\ (y\ z)$ 對應公理 $(A \to (B \to C)) \to ((A \to B) \to (A \to C))$。
2. **1958 年，Curry 在 *Combinatory Logic*** 中進一步指出這是「公式即型別」的現象。
3. **Gentzen 的自然演算（Natural Deduction, 1935）**：證明引入規則（introduction）與消去規則（elimination）成對出現，形狀酷似 λ 演算的建構與使用。

Howard 的推理是：**這不只是「形狀相似」，而是「同一件事」**。自然演算的證明樹與簡單型別 λ 演算的推導在結構上同構（isomorphic）。

## 線索與推理 -- 數學式、程式、理論

### 1. 對應表

| 邏輯（直覺命題邏輯） | 計算（簡單型別 λ 演算） |
|---|---|
| 命題 $A$ | 型別 $\tau$ |
| 證明（proof） | λ 項（term / program） |
| 蘊含 $A \to B$ | 函數型別 $\tau_1 \to \tau_2$ |
| 合取 $A \wedge B$ | 乘積型 $\tau_1 \times \tau_2$ |
| 析取 $A \vee B$ | 和型（sum type） $\tau_1 + \tau_2$ |
| 恆真 $\top$ | 單位型 $1$（unit） |
| 恆假 $\bot$ | 空型 $0$（void） |
| 引入規則（$\to$I） | $\lambda$ 抽象（建構函數） |
| 消去規則（$\to$E） | 函數應用 |
| 假設（assumption） | 變數（variable） |
| 證明的正規化 | 程式的求值終止 |
| 歸納/遞迴 | 原始遞迴 |

### 2. 蘊含 ↔ 函數

自然演算的蘊含引入規則：

$$
\frac{[A]\ \vdots\ B}{A \to B}\ (\to I)
\qquad
\frac{\Gamma \vdash A \to B \qquad \Gamma \vdash A}{\Gamma \vdash B}\ (\to E)
$$

對應 λ 演算的型別推導：

$$
\frac{\Gamma, x:\tau_1 \vdash e : \tau_2}{\Gamma \vdash \lambda x.\, e : \tau_1 \to \tau_2}
\qquad
\frac{\Gamma \vdash f : \tau_1 \to \tau_2 \qquad \Gamma \vdash a : \tau_1}{\Gamma \vdash f\ a : \tau_2}
$$

柯里化（Currying）在此對應下自然湧現：$A \to (B \to C) \cong (A \wedge B) \to C$。

### 3. Nat 的消去 ↔ 歸納

自然數型別 $\mathbb{Nat}$ 的引入與消去：

$$
\frac{}{\Gamma \vdash \texttt{zero} : \mathbb{Nat}}\ (\mathbb{Nat}\text{-}I_1)
\qquad
\frac{\Gamma \vdash n : \mathbb{Nat}}{\Gamma \vdash \texttt{succ}\ n : \mathbb{Nat}}\ (\mathbb{Nat}\text{-}I_2)
$$

消去規則（原始遞迴子）：

$$
\frac{
  \Gamma \vdash z : C \qquad
  \Gamma \vdash s : \mathbb{Nat} \to C \to C \qquad
  \Gamma \vdash n : \mathbb{Nat}
}{
  \Gamma \vdash \text{rec}_{\mathbb{Nat}}(z, s, n) : C
}
$$

這正是程式中的遞迴——**歸納證明就是遞迴程式**：

```haskell
-- 證明 2+2=4 的「計算版本」：遞迴加法
add :: Nat -> Nat -> Nat
add zero     m = m                      -- 零情況 = 基礎步驟
add (succ n) m = succ (add n m)         -- 歸納步驟 = 遞迴調用
```

### 4. 一個 Coq/Agda 式範例

```agda
-- Agda 風格：證明 A → A 恆有證明（即恆等函數）
id : ∀ {A : Set} → A → A
id x = x                          -- 這就是 λx.x 的證明版

-- 證明 (A ∧ B) → (B ∧ A)：交換律
swap : ∀ {A B : Set} → (A ∧ B) → (B ∧ A)
swap (a , b) = (b , a)            -- 模式匹配 = 消去規則

-- 證明 (A → B) → A → B：函數應用本身就是證明
apply : ∀ {A B : Set} → (A → B) → A → B
apply f x = f x
```

每一個「型別正確的定義」就是一個「構造性證明」。反過來，若命題 $A$ 的型別沒有任何項可以 inhabiting（如 $((A \to B) \to A) \to A$ 這樣的 Peirce 律），在直覺邏輯中就不可證明——這與簡單型別 λ 演算中「找不到對應的 λ 項」完全一致。

## 結案 -- 後果與影響

1. **證明助理（Proof Assistants）**：Coq、Agda、Lean 都建立在 Curry–Howard 對應上——寫程式就是寫證明；
2. **依賴型別程式設計**：Idris、Agda 使型別可以依賴值，把邏輯的豐富結構帶入程式；
3. **構造性數學**：計算的視角重新詮釋了 Brouwer 的直覺主義——「存在證明」必須「構造」出見證者（witness），對應程式中「必須算出」回傳值；
4. **型別理論的統一**：把 Martin-Löf 型別論（1972 之後）推向主流，成為函數式程式設計與數學基礎的共同語言；
5. **程式驗證**：型別系統就是輕量級的邏輯證明器，Haskell/ML 的強型別可直接視為某種「命題的證明」。

## 關鍵人物與文獻

- **William A. Howard**：美國邏輯學家，任職於普渡大學。
- **Haskell Curry**（1900–1982）：組合子邏輯的奠基者。
- W. A. Howard, *"The Formulae-as-Types Notion of Construction"*（1965 手稿，收錄於 Curry 1969 年的 Festschrift，正式出版 1980）。
- H. Curry & R. Feys, *Combinatory Logic, Vol. 1* (1958)。
- P. Martin-Löf, *"An Intuitionistic Theory of Types"* (1972)。
