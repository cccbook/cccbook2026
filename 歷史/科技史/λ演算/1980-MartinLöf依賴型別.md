# 1980 — Martin-Löf 依賴型別理論

## 案件摘要
瑞典邏輯學家 Per Martin-Löf 於 1979–1980 年間發表「構造型別理論」（Constructive Type Theory），將 Russell 的型別論、Curry–Howard 對應與 Brouwer 的直覺主義數學熔於一爐。型別不再只是防錯標籤，而成為「命題」本身；證明即程式。這是「命題作為型別」思想的極限形式。

## 前因 -- 為什麼會有這個案子
- **Russell 的惡夢**：1901 年 Russell 悖論 $\{x \mid x \notin x\} \in x \iff x \notin x$ 摧毀了樸素集合論，型別論是解藥之一，但 Russell 的 Ramified Type Theory 過於笨重。
- **Brouwer 的直覺主義**：數學證明必須是「建構」——要證明「存在 $x$ 使 $P(x)$」，你必須真的給出 $x$。排中律 $P \lor \neg P$ 不能自由使用。
- **Curry–Howard 對應（1958/1969）**：Curry 發現簡單型別 λ 演算中型別與直覺命題邏輯同構：

  $$\text{型別} \leftrightarrow \text{命題}, \quad \text{項（程式）} \leftrightarrow \text{證明}, \quad \text{化簡} \leftrightarrow \text{證明正規化}$$

  例如蘊含消去對應函數應用：若 $f : A \to B$ 且 $a : A$，則 $f\,a : B$。
- **懸案**：Curry–Howard 只處理簡單型別 $A \to B$。像「對所有自然數 $n$，存在質數 $p > n$」這種**依賴於值的命題**，簡單型別無法表達。

## 線索與推理 -- 數學式、程式、理論
Martin-Löf 的關鍵推理：**讓型別本身依賴於項**。於是出現兩種新的型別構造子：

### 依賴積型（Dependent Product，Π 型）
$$\prod_{x : A} B(x)$$

一個函數 $f : \Pi x:A.\, B(x)$，其回傳型別 $B(x)$ 隨輸入 $x$ 而變。當 $B$ 不依賴 $x$ 時退化為普通函數型 $A \to B$。這對應邏輯的**全稱量詞** $\forall x:A.\, B(x)$。

範例：`Vector A n → Vector A (n+1)` 型的「加入一個元素」函數——回傳型別隨輸入長度改變，靠型別系統保證不會弄錯長度。

### 依賴和型（Dependent Sum，Σ 型）
$$\sum_{x : A} B(x)$$

一個元素 $(x, b) : \Sigma x:A.\, B(x)$ 是一對：第一分量 $x : A$，第二分量 $b : B(x)$。這對應邏輯的**存在量詞** $\exists x:A.\, B(x)$——給出 $x$，並附上 $P(x)$ 的證明 $b$。這正是 Brouwer 建構主義的存在證明！

### 判斷 vs 命題
Martin-Löf 區分兩個層次，這是理論的核心創新：

| 判斷（Judgement） | 意義 | 命題（Proposition） |
|---|---|---|
| $A \ \mathsf{type}$ | $A$ 是一個型別 | — |
| $a : A$ | $a$ 具有型別 $A$ | $A$ 為真（Curry–Howard） |
| $a = b : A$ | $a$ 與 $b$ 定義相等 | — |

**判斷是後設層次的宣稱，命題是理論內部的對象**。「$a : A$」這個判斷成立 ⟺ 命題 $A$ 有證明（即項 $a$）。判斷不能被當成項操作，這與同倫型別論中 HoTT 將「等於」變成命題的做法形成對照。

### 恆等型與構造
$$\mathsf{Id}_A(x, y)$$

$x = y$ 的證明是建構出來的：唯一建構子 $\mathsf{refl} : \mathsf{Id}_A(x, x)$。配合歸納定義（W-type：$\mathsf{W}_{x:A} B(x)$ 是良基樹的型別，推廣了自然數與各種歸納資料結構），整個數學可以從零開始建構：

```text
-- Agda 風格：自然數與加法的依賴型別定義
data Nat : Set where
  zero : Nat
  suc  : Nat → Nat

_+_ : Nat → Nat → Nat
zero  + n = n
suc m + n = suc (m + n)

-- 依賴型別函數：回傳型別依賴於值 n
Vec : Set → Nat → Set
Vec A zero    = Unit
Vec A (suc n) = A × Vec A n
```

### 理論定義（判斷規則）
Π 型的引入與消去規則（λ 演算的直接推廣）：

$$\frac{\Gamma, x:A \vdash b : B(x)}{\Gamma \vdash \lambda x:A.\, b : \Pi x:A.\, B(x)} \;(\Pi\text{-I}) \qquad \frac{\Gamma \vdash f : \Pi x:A.\, B(x) \quad \Gamma \vdash a : A}{\Gamma \vdash f\,a : B(a)} \;(\Pi\text{-E})$$

β 化簡 $\ (\lambda x:A.\,b)\,a \;\longrightarrow\; b[a/x]\$ 在此成為**證明化簡**：一個證明被化簡成更直接的證明。

## 結案 -- 後果與影響
- **型別論成為數學基礎**：Martin-Löf 型別論（MLTT）證明整個建構主義數學可以在其中形式化，是繼 ZFC 之後最重要的數學基礎候選。
- **證明助手大爆發**：NuPRL（1980s）、Coq（1989）、Agda（1999/2007）、Idris（2012）、Lean（2015）全部以依賴型別為核心。Coq 基於 Calculus of Constructions，Agda 幾乎直接實作 MLTT。
- **程式即證明的工程實現**：依賴型別讓「正確性由型別保證」變成現實——CompCert 用 Coq 驗證 C 編譯器，四色定理用 Coq 機械驗證。
- **HoTT 與 Cube**：2000 年代同倫型別論（Homotopy Type Theory）以 MLTT 為基礎；Barendregt 的 Lambda Cube 中，「加依賴型別」正是通往 λΠ 的一軸。
- **重大懸念**：MLTT 的同一性型別 $\mathsf{Id}$ 引出了不可判定的 UIP 問題，最終催生了 HoTT 的 univalence 公理——案件仍在延燒。

## 關鍵人物與文獻
- **Per Martin-Löf**：瑞典邏輯學家，機率論（Martin-Löf randomness）與型別論雙棲大師。
- 文獻：
  - Martin-Löf, P. (1980). *Constructive Mathematics and Computer Programming* (Philosophical Transactions of the Royal Society).
  - Martin-Löf, P. (1984). *Intuitionistic Type Theory* (Bibliopolis, Naples) — 佛羅倫斯講義，MLTT 聖經。
  - Nordström, Petersson, Smith (1990). *Programming in Martin-Löf's Type Theory*.
- 相關：Brouwer（直覺主義）、Heyting（直覺邏輯形式化）、Curry–Howard（Howard 1969〈The Formulae-as-Types Notion of Construction〉）。
