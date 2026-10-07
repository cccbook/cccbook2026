# 1815-Cauchy 置換群

## 案件摘要
1815 年，Cauchy 在《École Polytechnique 雜誌》發表關於置換（substitutions）的系列論文，
首次把「根的置換」當成獨立的數學物件系統性研究，並證明了著名的 **Cauchy 定理**：
若質數 $p$ 整除群 $G$ 的階，則 $G$ 必有 $p$ 階元素（從而存在 $p$ 階子群）。
置換群因此成為群論史上第一個被認真研究的具體實例。

## 前因 -- 為什麼會有這個案子
- **Lagrange 的先聲（1770）**：Lagrange 在《Réflexions sur la résolution algébrique des équations》中
  研究三次、四次方程時發現：方程的根在置換下形成的函數
  $$\phi(x_1, x_2, \dots, x_n) \mapsto \phi(x_{\sigma(1)}, \dots, x_{\sigma(n)})$$
  其「可分辨的取值數」必整除 $n!$（後世稱 **Lagrange 定理的雛形**）。
  例如三次方程中 $x_1^2 x_2 + x_2^2 x_3 + x_3^2 x_1 - x_1 x_2^2 - x_2 x_3^2 - x_3 x_1^2$
  在 $3! = 6$ 個置換下只取 2 個值。
- Lagrange 自己認為這只是解方程的技巧，**沒有把置換本身當作研究主體**。
- 1799–1813 年 Ruffini 嘗試證明五次方程無根式解，被迫發展置換的性質（如 $S_5$ 沒有 60 階... 不對，
  他研究了置換的封閉性與階數），但因工具粗糙而未完成。
- 案件問題：**如果置換是解方程的核心，那麼置換系統本身有什麼結構定律？**

## 線索與推理 -- 數學式、程式、理論

### 線索一：循環記法
Cauchy 引入了沿用至今的**循環記法（cycle notation）**：
$$\sigma = \begin{pmatrix} 1 & 2 & 3 \\ 2 & 3 & 1 \end{pmatrix} = (1\,2\,3)$$
意即 $1 \mapsto 2,\ 2 \mapsto 3,\ 3 \mapsto 1$。任一置換都可分解成**互不相交循環的乘積**：
$$\sigma = (1\,3)(2\,4)(5)$$
循環分解的唯一性（不計順序）是置換群的第一條「結構定理」，而
$$\text{order}(\sigma) = \operatorname{lcm}(\text{各循環長度})$$
這直接給出 Cauchy 定理在 $S_n$ 中的具體樣貌。

### 線索二：Cauchy 定理（1815）
> **Cauchy 定理**：設 $G$ 為有限群，質數 $p \mid |G|$，則 $G$ 中存在階為 $p$ 的元素。

證明骨架（現代版本，考慮集合 $X = \{(a_1,\dots,a_p) \in G^p : a_1 a_2 \cdots a_p = e\}$）：
- $|X| = |G|^{p-1}$，因為前 $p-1$ 個元素可任選，最後一個被乘積方程鎖定。
- 令循環群 $C_p = \langle \rho \rangle$ 作用在 $X$ 上（循環輪換各分量）。
- 不動點個數由軌道公式給出：
  $$|X| = |\text{Fix}| + \sum_{\text{非平凡軌道}} p$$
  故 $p \mid |\text{Fix}|$。而 $|\text{Fix}| \ge 1$（$(e,\dots,e)$ 是不動點），
  且 $|\text{Fix}| \ne 1$（否則 $p \nmid 1$ 矛盾），所以存在 $a \ne e$ 使 $(a,\dots,a) \in X$，
  即 $a^p = e$。$\blacksquare$
- 推論：$\langle a \rangle$ 是 $G$ 的 $p$ 階子群。

### 線索三：置換群 = 群論的第一個實例
Cauchy 證明了：$n$ 個文字的置換共有 $n!$ 個，在合成運算下封閉、有單位元、有反元素：
$$(\sigma \circ \tau)(x) = \sigma(\tau(x)), \quad \sigma^{-1}\sigma = \mathrm{id}$$
這正是 1854 年 Cayley 給出抽象群定義前的「具體模型」。
Cauchy 在 1815–1845 年間寫下大量置換群論文，證明了如「兩個 3-循環的乘積類型」等大量結果，
為 Galois 理論備好了語言。

### Python 實作：置換群（循環分解與群運算）

```python
from functools import reduce
from math import gcd

def perm_from_cycles(n, *cycles):
    """由循環記法建立置換（tuple p, p[i] = i 的像）"""
    p = list(range(n))
    for c in cycles:
        for k, x in enumerate(c):
            p[x] = c[(k + 1) % len(c)]
    return tuple(p)

def to_cycles(p):
    """分解回互不相交循環（略去固定點可加回）"""
    seen, cycles = set(), []
    for i in range(len(p)):
        if i in seen or p[i] == i:
            seen.add(i); continue
        c, j = [], i
        while j not in seen:
            seen.add(j); c.append(j); j = p[j]
        cycles.append(tuple(c))
    return cycles

def compose(t, s):
    """(t∘s)(x) = t[s[x]]"""
    return tuple(t[s[x]] for x in range(len(s)))

def inverse(p):
    r = [0] * len(p)
    for i, x in enumerate(p): r[x] = i
    return tuple(r)

def order(p):
    """置換的階 = lcm(循環長度)"""
    L = [len(c) for c in to_cycles(p)]
    return reduce(lambda a, b: a * b // gcd(a, b), L, 1)

# --- 實驗：S3 全體 ---
S3 = sorted({perm_from_cycles(3, c)
             for c in [(), (0,1), (0,2), (1,2), (0,1,2), (0,2,1)]})
print(len(S3), "個元素")                      # 6
sigma = perm_from_cycles(3, (0,1,2))
print(to_cycles(sigma), "order =", order(sigma))  # [(0,1,2)] order = 3
print(compose(perm_from_cycles(3,(0,1)), perm_from_cycles(3,(1,2))))
# (0 1)(1 2) = (0 2 1)

# 驗證 Cauchy 定理：3 | 6，S3 中有 3 階元素
assert any(order(p) == 3 for p in S3)
```

### 理論定義
> **定義（置換群）**：$\mathrm{Sym}(X)$ 為集合 $X$ 上所有雙射在合成運算下的群；
> 其子群稱為**置換群**。當 $X = \{1,\dots,n\}$ 時記 $S_n$，$|S_n| = n!$。

## 結案 -- 後果與影響
- 循環記法成為通用語言，至今每本群論教科書都在使用。
- Cauchy 定理是有限群論的基石，其逆定理（Sylow 定理的特例）開啟了 1872 年 Sylow 的子群理論。
- 置換群提供了第一個具體群實例，直接導致：
  - **Galois（1832）**用置換群判定方程可解性；
  - **Cayley（1854）**提出抽象群定義；
  - **Jordan（1870）《Traité des substitutions》**將置換群論系統化。
- 解方程的問題從此轉化為**研究對稱性的問題**——這是代數學的第一次典範轉移。

## 關鍵人物與文獻
| 人物 | 年份 | 貢獻 |
|------|------|------|
| Lagrange | 1770 | 根的置換、Lagrange 定理雛形 |
| Ruffini | 1799 | 置換的封閉性研究（五次方程嘗試）|
| Cauchy | 1815 | 循環記法、Cauchy 定理、置換群系統研究 |
| Cayley | 1854 | 抽象群定義 |
| Jordan | 1870 | 《Traité des substitutions et des équations algébriques》|
