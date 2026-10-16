# 1941 - Church 的書《The Calculi of Lambda-Conversion》

## 案件摘要

1941 年，Alonzo Church 出版《The Calculi of Lambda-Conversion》，
把散落各論文的 λ 演算整理成第一部系統性專著。這是偵探把十年案情
卷宗裝訂成冊的時刻——β-轉換、βη-轉換、Church–Rosser 定理自此
成為學界標準的「案發程序規範」。

## 前因 -- 為什麼會有這個案子

- 1932–36 年 Church 在數篇論文中提出 λ 演算，但形式分散、記號各異，
  甚至最初的系統含錯（Kleene 與 Rosser 於 1935 年指出其不一致性）。
- 1936 年 Church 用 λ 演算證明判定問題無解；1937 年 Turing 證明等價性。
- 學界需要一份**權威、自足、嚴格**的文獻，作為深入研究與教學的基礎。
- Church 在普林斯頓的 Annals of Mathematics Studies 叢書第 6 號
  出版此書——一份裝訂成冊的「結案報告」。

## 線索與推理 -- 數學式、程式、理論

### 兩套計算系統：λβ 與 λβη

書中系統性呈現兩個演算：

- **λβ 演算**：僅含 β-轉換
- **λβη 演算**：β-轉換 + η-轉換（extensionality，外延性）

無型別 λ 項的文法（BNF）：

```
M ::= x | λx. M | (M M)
```

### β-轉換

β-紅巢（redex）與其約簡：

$$
(\lambda x.\, M)\ N \;\to_\beta\; M[x := N]
$$

其中 $M[x := N]$ 表示把 $M$ 中自由出現的 $x$ 替換為 $N$（注意需先
α-改名避免捕獲衝突，variable capture）。

例：

$$
(\lambda x.\, x^2)\ 3 \to_\beta 3^2 = 9
$$

程式模擬（Python）：

```python
def beta_reduce(func, arg):
    # func: (param_name, body)
    param, body = func
    return substitute(body, param, arg)

def substitute(term, var, val):
    if isinstance(term, str):
        return val if term == var else term
    if term[0] == 'lam':
        if term[1] == var:
            return term          # x 被遮蔽，停止替換
        return ('lam', term[1], substitute(term[2], var, val))
    return (substitute(term[1], var, val),
            substitute(term[2], var, val))
```

### η-轉換（外延性）

$$
\lambda x.\, M\ x \;\to_\eta\; M \qquad (\text{條件：} x \notin \mathrm{FV}(M))
$$

η-轉換表達「外延相等」：兩函數若對所有參數給出相同結果，則視為相同。

$$
f = g \;\iff\; \forall x.\ f\ x = g\ x
$$

例：$\lambda x.\ (\lambda y.\ y)\ x \to_\eta \lambda y.\ y$

程式模擬：

```python
def eta_reduce(term):
    # lam x (app M x), 且 x 不在 M 的自由變數中
    if term[0] == 'lam' and term[2][0] == 'app' \
       and term[2][2] == term[1] and term[1] not in free_vars(term[2][1]):
        return term[2][1]
    return term
```

### Church–Rosser 定理（合流性 Confluence）

全書最重要的定理，1936 年由 Church 與 Barkley Rosser 證明：

> **定理（Church–Rosser / Confluence）**：若 $M \twoheadrightarrow P$ 且
> $M \twoheadrightarrow Q$，則存在 $N$ 使 $P \twoheadrightarrow N$ 且
> $Q \twoheadrightarrow N$。

$$
\begin{array}{ccc}
 & M & \\
\swarrow & & \searrow \\
P & & Q \\
\multimap & & \multimap \\
 & N &
\end{array}
$$

其中 $\twoheadrightarrow$ 是 $\to$ 的自反傳遞閉包（多重步約簡），
$\multimap$ 表示「存在路徑」。

**推論一（正規形式唯一性）**：若 $M$ 有正規形式，則其正規形式
在（α-等價意義下）唯一。

**推論二（一致性）**：不存在項 $P$ 使 $P =_\beta \lambda x.\, x$ 且
$P =_\beta \lambda x.\, y$——演算不會推出矛盾。

證明技術：平行約簡（parallel reduction, ⊸ 關係）+ Tait–Martin-Löf 的
「完成菱形圖」（strip lemma）：平行約簡一步保留菱形性質，
再對約簡長度歸納。此技術至今仍是證明合流性的標準方法。

程式驗證菱形性質的示意（隨機取項、隨機約簡、尋找匯合點）：

```python
import random

def random_reduce_chain(m, k):
    for _ in range(k):
        redexes = find_redexes(m)
        if not redexes:
            return m
        m = reduce_one(m, random.choice(redexes))
    return m

def confluence_check(m, trials=100):
    for _ in range(trials):
        p = random_reduce_chain(m, 5)
        q = random_reduce_chain(m, 5)
        if meet(p, q, max_steps=20):
            return True     # 找到匯合點 N
    return False
```

### 對無型別與型別化的總結

書中同時呈現：

- 無型別 λβ / λβη 演算：圖靈完備，可定義一切可計算函數
- 簡單型別版本（1940）：強正規化，可避免悖論
- Church 數字、配對、條件式、遞迴的 λ 編碼

## 結案 -- 後果與影響

- λ 演算自此有了標準教材，後續所有教科書（Barendregt 1984《The Lambda
  Calculus: Its Syntax and Semantics》是第二座里程碑）皆以它為起點。
- Church–Rosser 定理成為**所有rewriting 系統的典範定理**，term rewriting、
  graph rewriting、界面理論皆沿用平行約簡證法。
- η-轉換啟發了外延性（extensionality）研究，影響集合論基礎與範疇論
  （Cartesian closed category 中的外延相等）。
- 程式語言方面：Haskell 的語意（pure λ + lazy evaluation）、
  ML/Haskell 的「等式推理」（equational reasoning）皆立足於此書的框架。

## 關鍵人物與文獻

- **Alonzo Church**（1903–1995）：作者，λ 演算創始人。
- **Barkley Rosser**：Church–Rosser 定理的共同證明者。
- Church, A. (1941). *The Calculi of Lambda-Conversion*.
  Annals of Mathematics Studies, No. 6. Princeton University Press.
- Barendregt, H. (1984). *The Lambda Calculus: Its Syntax and Semantics*.
