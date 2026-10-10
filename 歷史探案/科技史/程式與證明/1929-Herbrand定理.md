# 1929 年：Herbrand 定理 — 自動證明之母

> 偵探：Jacques Herbrand（21 歲博士論文）。案發地：巴黎。卷宗：Recherches sur la théorie de la démonstration。

## 案發現場

[1879-Frege概念文字.md](1879-Frege概念文字.md) 給了量詞，[1910-PrincipiaMathematica.md](1910-PrincipiaMathematica.md) 展示了證明的浩瀚，[1900-Hilbert23問題.md](1900-Hilbert23問題.md) 懸賞判定法。但一階邏輯的證明搜尋仍像大海撈針：量詞的實例有無窮多，該試哪個？

Herbrand 接到的報案是：**能否把一階不可滿足性歸約為有限個命題基例的不可滿足性？** 若能，則一階證明可交給真值表＋枚舉——機器證明成為可能。

他 21 歲交卷，兩年後登山遇難，年僅 23 歲。這篇論文被後世稱為自動證明之母。

## 偵查過程（含數學式/表格/理論）

### 第一條線索：Skolem 化 — 拔掉存在量詞

先把公式化為前束範式，再消去 $∃$ ：

$$
∀x ∃y P(x, y) \leadsto ∀x P(x, f(x))
$$

其中 $f$ 是新鮮 Skolem 函數，「對每個 $x$ 選一個見證 $y$ 」。外層 $∃x ∀y P(x, y)$ 則換成常數 $c$ ：

$$
∃x ∀y P(x, y) \leadsto ∀y P(c, y)
$$

Skolem 化保持**可滿足性等價**（非等價，但對 Herbrand 夠用）。剩下的只有 $∀$ ，可任意代入基項。

### 第二條線索：Herbrand 宇宙與定理本體

設簽名含常數 $a$ 、函數 $f$ ，Herbrand 宇宙 $H$ 是所有基項（ground terms）：

$$
H = \{a, f(a), f(f(a)), …\}
$$

Herbrand 定理（一版）：公式集 $S$ 不可滿足，當且僅當存在有限個 $H$ 上的基例集 $S'$ ，使 $S'$ 命題不可滿足。

換言之：

$$
S \text{ unsat} ↔ ∃有限 S' ⊆ ground(S) (S' \text{ 命題 unsat})
$$

無窮的量詞搜尋坍縮為有限的真值表檢查——[1847-Boole布林代數.md](1847-Boole布林代數.md) 的真值表在此借屍還魂。

### 第三條線索：小例子全程示範

欲證 $∃x P(x)$ 可由 $∀x P(x)$ 推出，等價證下式不可滿足：

$$
\{∀x P(x), ¬P(c)\}
$$

其中 $c$ 是把結論否定後 Skolem 化的常數。Herbrand 宇宙取 $\\{c\\}$ 即可，基例集：

| 基例 | 來源 |
|------|------|
| $P(c)$ | $∀x P(x)$ 代入 $x = c$ |
| $¬P(c)$ | 否定結論 |

$\{P(c), ¬P(c)\}$ 命題不可滿足，故原蘊涵成立。再看稍難的：

$$
∀x (P(x) → Q(f(x))), P(a) ⊢ ∃y Q(y)
$$

否定結論得 $∀y ¬Q(y)$ ，代入 $y = f(a)$ 與前提 $x = a$ 的基例 $\{¬P(a) ∨ Q(f(a)), P(a), ¬Q(f(a))\}$ 即命題矛盾。機器只需枚舉 $a$ 、 $f(a)$ 兩項即破案。

## 結案報告

Herbrand 結案：**一階證明＝系統枚舉基例＋命題判定**。半可判定性就此確立：不可滿足者終將被有限基例出賣，可滿足者可能永遠等下去。

遺產：

1. Gilmore 1960、Davis–Putnam、Robinson 歸結全是 Herbrand 程序的優化版。
2. Gödel 完備性定理的構造性證明幾乎就是 Herbrand 構造。
3. 局限：枚舉爆炸。Robinson 的合一演算法把「先枚舉再比對」變成「按需合一」，才真正實用。

Gödel（[1931-Godel不完備定理.md](1931-Godel不完備定理.md)）證明有些真理永不可證，Herbrand 則保證不可滿足者必有有限證人——兩面夾擊，刻畫了一階邏輯的邊界。

## 證據與工具

核心公式：

$$
∀x ∃y P(x, y) \equiv_{sat} ∀x P(x, f(x))
$$

$$
S \text{ unsat} ↔ ∃有限 S' (S' \text{ unsat})
$$

Python 迷你 Herbrand 枚舉（檢查上例）：

```python
from itertools import product
# 基例 {¬P(a)∨Q(f(a)), P(a), ¬Q(f(a))} 的命題檢查
for Pa, Qfa in product([False, True], repeat=2):
    c1 = ((not Pa) or Qfa)
    c2 = Pa
    c3 = (not Qfa)
    if c1 and c2 and c3:
        print("可滿足", Pa, Qfa)
        break
else:
    print("不可滿足：原蘊涵成立")
```

延伸閱讀：判定夢的終結在 [1931-Godel不完備定理.md](1931-Godel不完備定理.md)；證明結構的優雅重構在 [1934-Gentzen自然演繹.md](1934-Gentzen自然演繹.md)；公理系統的源頭在 [1879-Frege概念文字.md](1879-Frege概念文字.md) 與 [1910-PrincipiaMathematica.md](1910-PrincipiaMathematica.md)。
