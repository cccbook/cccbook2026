# 1879 年：Frege《概念文字》 — 謂詞邏輯誕生

> 偵探：Gottlob Frege。案發地：耶拿大學。卷宗：Begriffsschrift（概念文字）。

## 案發現場

[1847-Boole布林代數.md](1847-Boole布林代數.md) 只能玩「且或非」，[-0350-Aristotle三段論.md](-0350-Aristotle三段論.md) 只能玩一元包含。遇到「每個人都愛某人」「給定任意 $ε$ 存在 $δ$ 」這類嵌套量詞與關係命題，兩者同時啞火。

數學分析的嚴格化運動（Cauchy、Weierstrass）急需精確語言，否則極限、連續的證明全是糊塗帳。Frege 接到的報案是：**為數學打造無歧義的人工語言，並從邏輯推出算術**（邏輯主義）。

他給出的兇器是一本薄薄的小冊子 Begriffsschrift，卻是兩千年來邏輯的最大躍進。

## 偵查過程（含數學式/表格/理論）

### 第一條線索：量詞 $∀$ 與 $∃$ 的發明

Frege 把命題拆成「函數＋自變元」： $P(x)$ 是函數，代入個體得真假值。於是：

$$
∀x P(x)
$$

表示「對一切 $x$ ， $P(x)$ 成立」；而：

$$
∃x P(x)
$$

可定義為 $¬∀x ¬P(x)$ 。嵌套量詞終於可寫，例如「每個人被某人愛」：

$$
∀x ∃y Loves(y, x)
$$

與「有個人愛所有人」：

$$
∃y ∀x Loves(y, x)
$$

語序不同意義不同——亞里斯多德對此完全無能為力。

### 第二條線索：以蘊涵與否定為基元

Frege 只取 $→$ 與 $¬$ 為原始連結詞，其餘皆定義：

| 定義 | 公式 |
|------|------|
| $A ∧ B$ | $¬(A → ¬B)$ |
| $A ∨ B$ | $¬A → B$ |
| $A ↔ B$ | 由 $→$ 雙向合取定義 |

命題演算公理系統（Begriffsschrift 版，後世簡化整理）：

| 公理 | 形式 |
|------|------|
| A1 | $A → (B → A)$ |
| A2 | $(A → (B → C)) → ((A → B) → (A → C))$ |
| A3 | $(¬A → ¬B) → (B → A)$ |
| 規則 | Modus Ponens：由 $A$ 、 $A → B$ 得 $B$ |

僅此三公理加一規則，即可推出一切重言式。這是歷史上第一個**希爾伯特式公理系統**，[1900-Hilbert23問題.md](1900-Hilbert23問題.md) 與 [1910-PrincipiaMathematica.md](1910-PrincipiaMathematica.md) 都是它的直系子孫。

### 第三條線索：Frege vs 亞里斯多德對照表

| 維度 | 亞里斯多德 | Frege |
|------|------------|-------|
| 單位 | 詞項 $S$ 、 $P$ | 函數 $P(x)$ ＋個體 |
| 量詞 | 四型 A/E/I/O，不可嵌套 | $∀$ 、 $∃$ 可任意嵌套 |
| 關係 | 無（僅一元包含） | 多元關係 $R(x, y)$ |
| 連結詞 | 殘缺（靠自然語言） | $→$ 、 $¬$ 為基元，函數完備 |
| 證明 | 化歸為完美式 | 公理＋MP 的形式推導鏈 |
| 語意 | 對當方陣 | 函數外延＋真值，意義/指稱區分 |

Frege 還區分 Sinn（意義）與 Bedeutung（指稱），「晨星＝暮星」之謎首次得解——同指稱、不同意義。

## 結案報告

Frege 結案：**一階謂詞邏輯誕生**，量詞＋變元＋蘊涵否定基元足以表達全部數學推理骨架。

遺產：

1. Russell 讀到 Frege，寫出 [1910-PrincipiaMathematica.md](1910-PrincipiaMathematica.md)。
2. Hilbert 讀到 Frege，提出 [1900-Hilbert23問題.md](1900-Hilbert23問題.md) 的形式主義綱領。
3. Herbrand（[1929-Herbrand定理.md](1929-Herbrand定理.md)）、Gödel（[1931-Godel不完備定理.md](1931-Godel不完備定理.md)）、Gentzen（[1934-Gentzen自然演繹.md](1934-Gentzen自然演繹.md)）全在 Frege 的語言裡辦案。

諷刺的是：Frege 的邏輯主義剛完工，Russell 就用悖論炸了它（見 [1910-PrincipiaMathematica.md](1910-PrincipiaMathematica.md)）。但語言留下了，大廈雖塌，地基永存。

## 證據與工具

核心公式：

$$
∀x (Human(x) → Mortal(x)), Human(s) ⊢ Mortal(s)
$$

$$
∃x ∀y (ε > 0 → ∃δ ∀z (|z - a| < δ → |f(z) - f(a)| < ε))
$$

後者是 Weierstrass 連續性定義的邏輯骨架——沒有量詞寫不出來。

公理 A1 的直觀： $A → (B → A)$ 說「真理不怕多一個無關前提」，這正是弱化（weakening）的祖先，Gentzen 在 [1934-Gentzen自然演繹.md](1934-Gentzen自然演繹.md) 會把它變成結構規則。

延伸閱讀：量詞如何被機械化消去？請看 [1929-Herbrand定理.md](1929-Herbrand定理.md) 的 Skolem 化；量詞系統的極限？請看 [1931-Godel不完備定理.md](1931-Godel不完備定理.md)。
