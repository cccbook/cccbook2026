# 1931 年：Gödel 不完備定理 — Hilbert 夢碎之夜

> 偵探：Kurt Gödel（25 歲）。案發地：維也納。卷宗：Über formal unentscheidbare Sätze。

## 案發現場

[1900-Hilbert23問題.md](1900-Hilbert23問題.md) 立案：證明算術一致、完備、可判定。[1910-PrincipiaMathematica.md](1910-PrincipiaMathematica.md) 試圖以身試法，[1929-Herbrand定理.md](1929-Herbrand定理.md) 帶來機械化曙光。一切看似只差臨門一腳。

Gödel 接到的不是懸賞，而是凶案：**直覺告訴他，形式系統不可能同時完備又一致。** 他要在 Principia 這類系統內部埋一顆「我不可證」的炸彈，讓系統親口承認自己的局限。

動機有二：Hilbert 的完備性要求與說謊者悖論（「這句話是假的」）的啟發——把語意悖論改寫為「這句話不可證」，悖論變定理。

## 偵查過程（含數學式/表格/理論）

### 第一條線索：哥德爾配數 $\lceil \phi \rceil$

把每個符號編碼為自然數，公式與證明都變成數。記公式 $\phi$ 的配數為：

$$
\lceil \phi \rceil
$$

例如原始編碼： $¬$ → 1、 $∨$ → 2、 $∀$ → 3、變元 $x_i$ →質數冪次。於是「 $\phi$ 可證」變成數論謂詞：

$$
Prov_T(\lceil \phi \rceil) = ∃p (Proof_T(p, \lceil \phi \rceil))
$$

其中 $Proof_T$ 是原始遞迴可判定的證明檢查關係。**元數學被算術吞噬**：談論證明的語句＝談論數的語句。

### 第二條線索：對角線引理

對任意性質 $Ψ(x)$ ，存在句子 $G$ 使得：

$$
T ⊢ G ↔ Ψ(\lceil G \rceil)
$$

證明靠「代入函數」 $diag$ ：構造 $\phi(x) = Ψ(diag(x))$ ，令 $G = \phi(\lceil \phi \rceil)$ 即自指完成。這是說謊者悖論的消毒版——把「真」換成「可證」。

取 $Ψ(x) = ¬Prov_T(x)$ ，得 Gödel 句 $G$ ：

$$
T ⊢ G ↔ ¬Prov_T(\lceil G \rceil)
$$

$G$ 斷言「我在此系統中不可證」。

### 第三條線索：第一／第二定理

| 定理 | 陳述 | 證明骨架 |
|------|------|----------|
| 第一 | 若 $T$ 一致且含算術，則 $G$ 真而不可證， $T$ 不完備 | 若 $T ⊢ G$ 則 $T ⊢ Prov_T(\lceil G \rceil)$ ，與 $G ↔ ¬Prov_T$ 矛盾；若 $T ⊢ ¬G$ 則證出假的 $Prov_T$ ，違反一致性 |
| 第二 | $T$ 證不出 $Con(T)$ | $Con(T)$ 定義為 $¬Prov_T(\lceil ⊥ \rceil)$ ，可證 $Con(T) → G$ ，故若 $T ⊢ Con(T)$ 則 $T ⊢ G$ ，與第一定理矛盾 |

關鍵蘊涵：

$$
T ⊢ Con(T) → G
$$

Hilbert 要求的有窮一致性證明，若可形式化於 $T$ 內，則 $T$ 自證一致→自證 $G$ →矛盾。故**第二問題無解**。

## 結案報告

Gödel 結案：**任何夠強的一致形式系統必不完備，且不能自證一致。** Hilbert 夢碎，[1900-Hilbert23問題.md](1900-Hilbert23問題.md) 的第二問題被判死刑。

遺產：

1. 真（ $⊨$ ）與可證（ $⊢$ ）永久分家，完備性僅對一階邏輯整體成立，對固定算術系統不成立。
2. 配數＋對角線成為理論 CS 標配：停機問題、Tarski 不可定義性皆同構。
3. 出路：Gentzen 在 [1934-Gentzen自然演繹.md](1934-Gentzen自然演繹.md) 用超限歸納（超出有窮）證明一致性；Herbrand 路線（[1929-Herbrand定理.md](1929-Herbrand定理.md)）轉向半判定與實用自動證明。

## 證據與工具

核心公式：

$$
G ↔ ¬Prov_T(\lceil G \rceil)
$$

$$
Con(T) = ¬Prov_T(\lceil ⊥ \rceil)
$$

$$
T ⊢ Con(T) → G
$$

自指玩具模型（Python 概念演示，非嚴格配數）：

```python
# Quine 程序：輸出自己的原始碼，體會對角線引理
s = 's = {!r}; print(s.format(s))'
print(s.format(s))
# Gödel 句 = 邏輯版 Quine：不斷言自己的真假，而斷言自己的不可證性
```

延伸閱讀：被炸毀的大廈見 [1910-PrincipiaMathematica.md](1910-PrincipiaMathematica.md)；炸彈的語言見 [1879-Frege概念文字.md](1879-Frege概念文字.md)；廢墟上的重建見 [1934-Gentzen自然演繹.md](1934-Gentzen自然演繹.md)；機械化餘燼見 [1929-Herbrand定理.md](1929-Herbrand定理.md)。
