# 16. 1969 — Dana Scott 的 D∞ 模型

## 案件摘要

1969 年，Dana Scott 在牛津與 Strachey 合作期間，發現無型別 λ 演算的語義有一個致命的邏輯問題：若要讓 $D \cong D \to D$，則 $|D| = |D|^{|D|}$，對任何非平凡集合這是不可能的（Cantor 對角線）。Scott 用「domain theory」繞過了這個矛盾，建立了 D∞ 模型——史上第一個無型別 λ 演算的數學語義，也是遞迴程式語義的基石。

## 前因 -- 為什麼會有這個案子

線索來自兩個困擾：

1. **無型別 λ 演算的悖論**：λ 演算中有不動點組合子 $Y = \lambda f.\, (\lambda x.\, f\ (x\ x))\ (\lambda x.\, f\ (x\ x))$，滿足 $Y\ f = f\ (Y\ f)$。這在語法上沒問題，但在集合論語義中，若 $D$ 是一個集合且 $D \cong D \to D$，那麼：

   $$
   |D| = |D \to D| = |D|^{|D|}
   $$

   由 Cantor 定理，對任何集合 $|D| < |D|^{|D|}$（當 $|D| \geq 2$），矛盾！這意味著**無型別 λ 演算在集合論中沒有非平凡的模型**。

2. **遞迴程式的語義問題**：1960 年代，程式中的遞迴（如 `while` 迴圈、遞迴函數）在數學上如何解釋？若 $\text{fact} = \lambda n.\, \ldots \text{fact} (n-1) \ldots$，這是一個自我指涉的方程，需要「解方程」的數學工具。

Scott 的推理：**讓函數空間不再是所有函數的集合，而是「連續函數」的子集合**——這樣函數空間可以「不比原集合大」，自我指涉就有了容身之處。

## 線索與推理 -- 數學式、程式、理論

### 1. Domain Theory：完全偏序（cpo）

Scott 引入 **complete partial order（cpo，完全偏序）**：

**定義（cpo）**：一個偏序集 $(D, \sqsubseteq)$ 是 cpo，若：
1. 有最小元素 $\bot \in D$（讀作 bottom，代表「未定義」或「無窮迴圈」）；
2. 對每個 $\omega$-鏈 $d_0 \sqsubseteq d_1 \sqsubseteq d_2 \sqsubseteq \cdots$，存在上確界 $\bigsqcup_{n=0}^{\infty} d_n \in D$。

**定義（連續函數）**：$f : D \to E$ 是連續的，若：
1. 單調：$d \sqsubseteq d' \Rightarrow f(d) \sqsubseteq f(d')$；
2. 保上確界：$f(\bigsqcup_n d_n) = \bigsqcup_n f(d_n)$。

關鍵性質：**連續函數的函數空間 $[D \to E]$ 本身也是一個 cpo**（點序 $f \sqsubseteq g \iff \forall d.\, f(d) \sqsubseteq g(d)$）。

### 2. 最小不動點

**Kleene 不動點定理**：若 $f : D \to D$ 是連續函數，則 $f$ 有最小不動點：

$$
\text{fix}(f) \;=\; \bigsqcup_{n=0}^{\infty} f^n(\bot)
$$

證明思路：$\bot \sqsubseteq f(\bot)$（$\bot$ 最小），由單調性得 $f(\bot) \sqsubseteq f^2(\bot) \sqsubseteq \cdots$ 是 $\omega$-鏈，故有上確界 $d^* = \bigsqcup_n f^n(\bot)$。由連續性：

$$
f(d^*) = f\left(\bigsqcup_n f^n(\bot)\right) = \bigsqcup_n f^{n+1}(\bot) = d^*
$$

即 $d^*$ 是不動點；且因為鏈從 $\bot$ 開始，$d^*$ 是最小的那個。

### 3. 遞迴程式的語義

遞迴函數定義 $\text{fact} = F(\text{fact})$ 的語義就是 $F$ 的最小不動點：

```haskell
-- fact 的定義方程
fact = λn. if n == 0 then 1 else n * fact (n-1)

-- 語義：fact = fix F，其中
F = λf. λn. if n == 0 then 1 else n * f (n-1)

-- 展開 fix F：
-- f^0(⊥) = λn. ⊥           （全體無定義）
-- f^1(⊥) = λn. if n==0 then 1 else ⊥   （只能算 0）
-- f^2(⊥) = λn. if n==0 then 1 else if n-1==0 then 1 else ⊥  （只能算 0,1）
-- ...
-- ⨆ f^n(⊥) = 真正的階乘函數（對所有自然數定義）
```

這就是「遞迴 = 極限」的直覺：每一步近似多算一點，極限就是完整語義。

### 4. D∞：繞過 Cantor 對角線

Scott 的 D∞ 構造：找一個 cpo $D$ 滿足 $D \cong [D \to D]$（注意：同構而非相等，且 $[D\to D]$ 只是**連續**函數空間）。構造方法：

$$
D_0 = \{*\} \text{（平凡集）}, \qquad D_{n+1} = [D_n \to D_n]
$$

每個 $D_{n+1}$ 是 $D_n$ 的「函數空間」，透過嵌入-投影對 $(\phi_n, \psi_n)$ 一層層嵌入，取極限：

$$
D_\infty = \text{（序列 } d_0 \in D_0, d_1 \in D_1, \ldots \text{ 的極限域）}
$$

在此 $D_\infty \cong [D_\infty \to D_\infty]$——**因為連續函數空間可以「裝進」原域**，Cantor 的反論被繞開了。應用 $D_\infty$ 的元素即可解釋 λ 演算：

$$
\llbracket \lambda x.\, e \rrbracket \rho = d \mapsto \llbracket e \rrbracket \rho[x \mapsto d], \qquad \llbracket e_1\ e_2 \rrbracket \rho = \llbracket e_1 \rrbracket \rho \cdot \llbracket e_2 \rrbracket \rho
$$

### 5. 與操作語義的區別

| 操作語義（Operational） | 指稱語義（Denotational，Scott） |
|---|---|
| 描述「如何算」（reduction steps） | 描述「算出什麼」（數學物件） |
| 結構歸納式定義 $\to_\beta$ 步驟 | 環境語義函數 $\mathcal{E}\llbracket e \rrbracket \rho$ |
| 對應 SECD 機器 | 對應 domain theory |
| 無法直接解釋 $Y$ 的無窮行為 | $\text{fix}(f) = \bigsqcup_n f^n(\bot)$ 直接解釋 |

兩者的一致性（adequacy / full abstraction）成為後續數十年的核心研究問題。

## 結案 -- 後果與影響

1. **Domain Theory 成為一門獨立學科**：cpo、連續函數、不動點定理、代數域、雙域（domain 的分類學）成為理論計算機科學的標準工具；
2. **遞迴程式的語義**：所有惰性/嚴格函數式語言（Haskell、ML）的語義都建立在最小不動點上；
3. **Wadler 等人的惰性求值理論**、Henderson/Launchbury 的 lazy semantics，都是 D∞ 思想的延伸；
4. **完全抽象問題**（Full Abstraction，Plotkin 1977、Milner 1977 提出，由 Abramsky、Ong、Hyland 等人於 1990 年代解決）成為語義學的中央山峰；
5. **類型論語義**：依賴型別語言（Agda、Coq）的語義也大量使用 domain-theoretic 工具。

## 關鍵人物與文獻

- **Dana Scott**（1932–）：美國邏輯學家、計算機科學家，图靈獎呼聲極高的人物，曾與 Strachey 在牛津合作。
- D. Scott, *"Outline of a Mathematical Theory of Computation"* (1970, Oxford PRG 技術報告)。
- D. Scott, *"Data Types as Lattices"* (1976, SIAM J. Computing)。
- D. Scott, *"Domains for Denotational Semantics"* (1982)。
- C. Strachey & C. Wadsworth, *"Continuations: A Mathematical Semantics for Handling Full Jumps"* (1974)。
