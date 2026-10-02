# 1854-Cayley 抽象群

## 案件摘要
1854 年，Cayley 在《On the theory of groups, as depending on the symbolic equation $\theta^n = 1$》中首次給出**抽象群**的定義——不再問「群是什麼東西的變形」，而只問「它滿足什麼公理」。這是一樁超前的懸案：定義提出後近 20 年乏人問津，直到 1870 年代才被數學界正式接受，最終成為現代代數的基石。

## 前因 -- 為什麼會有這個案子
- 19 世紀上半葉，「群」以三種偽裝分頭出現：Galois 的置換群（permutation groups）、Gauss 以來的數論同餘類（如 $(\mathbb{Z}/p)^\times$）、以及幾何變換（如 Möbius 的變換群）。
- 這三個「嫌犯」行為相似（都有結合的合成運算、有單位、可逆），但當時的「群」一詞總是綁定在「置換」上。
- Cayley 沿著 Lagrange 的路線研究符號方程 $\theta^n = 1$（$\theta$ 為一個變換），意識到：真正重要的不是置換的外衣，而是**運算的公理性質**。
- 偵查目標：把群的「本質特徵」從具體實例中剝離出來，寫成一套公理。

## 線索與推理 -- 數學式、程式、理論

### 線索一：Cayley 的抽象群公理
Cayley 1854 年的定義（以現代語言重述）：一個群是符號的集合 $\{1, \alpha, \beta, \ldots\}$，滿足：

1. **封閉性**：任兩個符號的乘積仍在集合中；
2. **結合律**：$(\alpha\beta)\gamma = \alpha(\beta\gamma)$；
3. **單位元素**：存在 $1$ 使 $\alpha \cdot 1 = 1 \cdot \alpha = \alpha$；
4. **逆元素**：每個 $\alpha$ 有逆 $\alpha^{-1}$ 使 $\alpha\alpha^{-1} = 1$。

注意：Cayley 早於 Weber（1893）近 40 年給出抽象定義，且他的版本（有限群）甚至隱含消去律可推出逆元素。他並證明了第一個抽象定理：

> **Cayley 定理（1854/1878）**：每個 $n$ 階群同構於對稱群 $S_n$ 的一個子群。

### 線索二：Cayley 表（群乘法表）
Cayley 用「乘法表」呈現有限群的完整結構——今日稱為 Cayley 表。表中的每一列（每一行）都是群元素的**置換**（Latin square 性質），這正是 Lagrange 置換思想的延續。

以四階群為例，恰有兩個互不同構的群：循環群 $\mathbb{Z}_4$ 與 Klein 四元群 $\mathbb{Z}_2 \times \mathbb{Z}_2$（後者 1884 年由 Klein 命名）。

### 線索三：群同構的現代觀念
Cayley 的定義使我們能問：**兩個看起來不同的對象，是否「本質上是同一個群」？**
$$\varphi: G \to H,\quad \varphi(ab) = \varphi(a)\varphi(b),\quad \varphi \text{ 為雙射}$$

例如 $(\mathbb{Z}/4, +) \cong \langle i \rangle \subset \{1, i, -1, -i\}$（複數的四次單位根群），而 $\mathbb{Z}_2 \times \mathbb{Z}_2 \cong \{(\pm1, \pm1)\} \subset (\mathbb{R}^\times)^2$。「同構」成了偵探的比對工具：剝掉外衣，看骨架。

### 程式碼：Python 生成並檢驗 Cayley 表

```python
import numpy as np

def cayley_table(elems, op):
    n = len(elems)
    idx = {e: i for i, e in enumerate(elems)}
    T = np.zeros((n, n), dtype=int)
    for i, a in enumerate(elems):
        for j, b in enumerate(elems):
            T[i, j] = idx[op(a, b)]
    return T

def check_group_axioms(T):
    n = len(T)
    # 封閉性：表內元素均在 [0, n)
    closed = T.min() >= 0 and T.max() < n
    # 單位元素：存在 e 使該行該列皆為 0..n-1 依序
    identity = any(all(T[e, j] == j and T[j, e] == j for j in range(n)) for e in range(n))
    # 可逆性：每列皆為置換（Latin square）
    invertible = all(sorted(T[i]) == list(range(n)) for i in range(n))
    # 結合律：窮舉檢驗
    assoc = all(T[T[a,b], c] == T[a, T[b,c]]
                for a in range(n) for b in range(n) for c in range(n))
    return closed, identity, invertible, assoc

# Z_4：整數模 4 加法
Z4 = cayley_table(range(4), lambda a, b: (a + b) % 4)
print("Z_4 的 Cayley 表：\n", Z4)
print("公理檢驗 (封閉,單位,可逆,結合):", check_group_axioms(Z4))

# Z_2 x Z_2：Klein 四元群
V4 = cayley_table([(0,0),(0,1),(1,0),(1,1)],
                  lambda a, b: ((a[0]+b[0])%2, (a[1]+b[1])%2))
print("Z_2 x Z_2 的 Cayley 表：\n", V4)
print("公理檢驗 (封閉,單位,可逆,結合):", check_group_axioms(V4))

# 同構比對：Z_4 與複數四次單位根群 {1, i, -1, -i}
roots = [1, 1j, -1, -1j]
R4 = cayley_table(roots, lambda a, b: a * b)
print("單位根群 Cayley 表：\n", R4)   # 與 Z4 同構（調換 1j 與 -1 的標號即可比對）
```

## 結案 -- 後果與影響
- **結案**：群被從「置換的外衣」中解放，成為獨立的代數結構；Cayley 表與同構概念提供了比對群結構的標準工具。
- **遲來的承認**：1854 年的論文幾乎無人引用——當時置換群仍是主流框架，抽象觀念太超前。直到 1870 年代，數學家（如 Jordan《Traité》1870、Klein、Sylow）的工作累積，加上 1878 年 Cayley 重新發表 abstract groups 的論文並由 Burnside、Hölder 等人推廣，抽象群觀念才在 1890 年代（Weber 的公理化）徹底確立。
- 深遠影響：群論成為 20 世紀代數的範式——環、域、模、李群、表示論皆沿用「公理 + 同構 + 同態」的偵探方法論；物理學中對稱性 = 群，更是現代物理的語言。

## 關鍵人物與文獻
- **Arthur Cayley（1821–1895）**：劍橋數學家，多產的代數學與幾何學家，矩陣論、不變量論的開創者。
- **Heinrich Weber（1842–1913）**：1893 年給出廣為接受的抽象群公理。
- **Camille Jordan（1838–1922）**：《Traité des substitutions et des équations algébriques》(1870)，置換群理論的集大成。
- 文獻：A. Cayley, "On the theory of groups, as depending on the symbolic equation $\theta^n = 1$", *Philosophical Magazine*, 1854；以及其 1878 年的續作 "The theory of groups"。
