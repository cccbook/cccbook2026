# 1965-Edmonds與多項式時間

## 案件摘要

1965 年，Jack Edmonds 在《Canadian Journal of Mathematics》發表《Paths, Trees, and Flowers》，給出一般圖最大匹配的多項式時間演算法（blossom 演算法）。但這篇論文真正的爆炸性主張藏在開頭：他主張把「好演算法」正式定義為「多項式有界時間」的演算法。在此之前，「效率」是人人心中各異的模糊詞；Edmonds 為它立下法治。這個定義成為後來 P、NP、NP-完備性整座複雜性理論大廈的地基。

## 前因 -- 為什麼會有這個案子

- 圖論演算法的「效率」無人定義，「好演算法」（good algorithm）只是口頭上的模糊詞。
- 匹配問題（maximum matching）：二部圖早在 1931 年就有匈牙利演算法，但一般圖（含奇數長度環）長期無有效解法。
- 1957 年 Berge 已證明增廣路徑定理，為匹配演算法鋪路，卻缺少處理奇環的技巧。
- Cobham 1964 年《The intrinsic computational difficulty of functions》已提出以多項式時間刻畫「可行計算」的先聲。
- Edmonds 在研究「計算效率能否成為數學上嚴格的對象」這一哲學問題。

## 線索與推理 -- 數學式、程式、理論

### 線索一：「好演算法」的正式定義

Edmonds 自述：「我主張把『好』（good）定義為多項式有界（polynomially bounded）。」也就是說，存在多項式 $p$ 使演算法在輸入長度 $n$ 上至多花 $p(n)$ 步：

$$\text{good} \iff \exists p \in \mathbb{R}[x],\ \text{時間} \le p(n)$$

這是本案的核心理念：多項式（如 $n^3$）與指數（如 $2^n$）之間，是一條文明的分界線。

### 線索二：增廣路徑理論（Berge 1957）

設 $M$ 是圖 $G$ 的匹配。一條「增廣路徑」是起訖皆為未匹配點、且沿路匹配邊與非匹配邊交錯的路徑。Berge 定理：

$$M \text{ 是最大匹配} \iff G \text{ 中不存在 } M\text{-增廣路徑}$$

沿增廣路徑翻轉（匹配邊變非匹配、反之亦然）可使匹配大小 $+1$。問題只剩：如何在一般圖上找到增廣路徑？

### 線索三：blossom 收縮 —— 破案時刻

在二部圖中，增廣路徑的交錯搜尋不會出錯；但在一般圖中，搜尋可能繞進奇數長度的環（blossom，奇環），在其中迷路。Edmonds 的破案技巧：把奇環收縮（contract）成單一超節點再繼續搜尋，找到增廣路徑後再展開還原。每個 blossom 收縮一次，總複雜度為 $O(n^3)$：

$$|M| \le \frac{n}{2} \ \Rightarrow\ \text{至多 } O(n) \text{ 次增廣，每次 } O(n^2)$$

一般圖匹配第一次被馴服——這是本案的破案時刻。

### 線索四：Edmonds-Karp 最大流

同一思想的延伸：Edmonds 與 Karp 在 1969/1972 年證明，在 Ford-Fulkerson 的增廣路徑法中改用 BFS（最短增廣路徑優先），複雜度即被多項式化為 $O(VE^2)$， regardless of 邊權。

### 程式碼示範

```python
def hungarian_match(adj, left):
    match = {}

    def try_kuhn(u, visited):
        for v in adj[u]:
            if v not in visited:
                visited.add(v)
                if v not in match or try_kuhn(match[v], visited):
                    match[v] = u
                    return True
        return False

    for s in left:
        try_kuhn(s, set())
    return match

adj = {"A": ["1", "2"], "B": ["1"], "C": ["2", "3"], "D": ["3"]}
m = hungarian_match(adj, ["A", "B", "C", "D"])
print(m)
assert len(m) == 3
```

此示範以增廣路徑法求二部圖最大匹配——正是 blossom 演算法的前置理論；一般圖中的奇環收縮是它缺少的最後一塊拼圖。

## 結案 -- 後果與影響

- 「P = 多項式時間可解」成為複雜性理論的標準定義，為 1971 年 Cook 的 NP-完備性理論與 P vs NP 問題搭好舞台。
- blossom 演算法進入主流工具：Python 的 `networkx.max_weight_matching` 即為其實現。
- Edmonds-Karp 使最大流問題正式納入多項式時間可解的版圖。
- 「好演算法」的哲學影響半世紀：多項式 vs 指數的界線，成為判斷問題「本質困難度」的文明分界線。
- Edmonds 的「非多項式 = 實際不可解」假說，直接啟發了 Cobham-Edmonds 論題。

## 關鍵人物與文獻

- J. Edmonds (1965). Paths, Trees, and Flowers. *Canadian Journal of Mathematics*, 17, 449-467.
- A. Cobham (1964). The intrinsic computational difficulty of functions. *Proceedings of the 1964 Congress for Logic, Methodology and Philosophy of Science*, 24-30. North-Holland.
- C. Berge (1957). Two theorems in graph theory. *Proceedings of the National Academy of Sciences*, 43(9), 842-844.
- J. Edmonds, R.M. Karp (1972). Theoretical improvements in algorithmic efficiency for network flow problems. *Journal of the ACM*, 19(2), 248-264.
- S.A. Cook (1971). The complexity of theorem-proving procedures. *Proceedings of the 3rd ACM Symposium on Theory of Computing*, 151-158.
- J. Edmonds (1965). Minimum partition of a matroid into independent subsets. *Journal of Research of the NBS*, 69B, 67-72.
