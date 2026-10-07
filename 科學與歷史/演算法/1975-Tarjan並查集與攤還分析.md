# 1975-Tarjan並查集與攤還分析

## 案件摘要

並查集（union-find）資料結構自 Galler 與 Fischer 1964 年提出後，實務上快得出奇，卻沒有人能證明它到底有多快。Robert Tarjan 在 1975 年發表《Efficiency of a Good But Not Linear Set Union Algorithm》，證明路徑壓縮加按秩合併的並查集，m 次操作的總成本是 $O(m\,\alpha(n))$——反 Ackermann 函數，對一切實用的 n 小於 5，實質上是常數。更深的破案在於：單次操作可能很慢，但「攤還」（amortized）之後卻近乎完美。這是攤還分析正式登場的歷史時刻。

## 前因 -- 為什麼會有這個案子

- Galler 與 Fischer 1964 年提出並查集的樸素實現：直覺很快，但最壞情況下樹可退化成一條長鏈，find 是 $O(n)$。
- Kruskal 1956 年的最小生成樹演算法需要高效判環：反覆查詢「兩端點是否已連通」，正是並查集的用武之地，但樸素版會拖垮整體複雜度。
- 路徑壓縮與按秩合併兩個加速技巧先後被提出（Hopcroft-Ulman 1973 也分析了類似組合），但精確的上界始終是懸案。
- Tarjan 的問題意識：「大家都說這演算法好，但『好』到底是多好？是否存在更好的下界？」
- 當時的分析工具（最壞情況分析、平均情況分析）都無法描述「偶爾慢、整體快」的行為，需要新的分析框架。

## 線索與推理 -- 數學式、程式、理論

### 並查集的基本操作

並查集維護一個不相交集合的分割，用森林表示，每棵樹一個集合：

- `find(x)`：沿父指標找到 x 所在樹的根（集合代表元）。
- `union(x, y)`：先 find 兩者根，再把一棵樹掛到另一棵之下。

### 兩個加速技巧

**路徑壓縮（path compression）**：find 時把路徑上所有節點直接掛到根，壓平樹：

$$x \to p(x) \to \cdots \to r \quad \Longrightarrow \quad x \to r,\ p(x) \to r,\ \ldots$$

**按秩合併（union by rank）**：維護每棵樹的秩（高度上界），矮樹掛高樹，保證樹高為 $O(\log n)$：

$$\text{rank}(r_1) < \text{rank}(r_2) \ \Rightarrow\ r_1 \text{ 接到 } r_2 \text{ 之下}$$

### 攤還分析與反 Ackermann 函數

Tarjan 證明的核心定理：n 個元素、m 次操作（$m \geq n$），路徑壓縮 + 按秩合併的總成本為

$$T(m, n) = O\big(m\,\alpha(m, n)\big) \approx O(m\,\alpha(n))$$

其中 $\alpha$ 是反 Ackermann 函數——使 Ackermann 函數 $A(k,k) \geq n$ 的最小 k。Ackermann 的增長速度是災難級的：

$$A(1,n) = 2n, \quad A(2,n) = 2^n, \quad A(3,n) = 2^{2^{\cdot^{\cdot^{2}}}}\ (\text{塔狀指數}), \quad A(4,4) = 2^{2^{2^{65536}}}$$

$A(4,4)$ 遠超宇宙中原子數。因此對一切實用的 n，$\alpha(n) \leq 4$——這是「實質常數」的教科書案例。同時 Tarjan 證明對應下界：任何此類演算法都無法做到 $\omega(m\,\alpha(n))$，即上界緊緻（但不是線性，標題「Not Linear」由此而來）。

### 攤還分析的誕生

攤還分析的哲學：不看單次操作的最壞成本，而看一串操作的總成本除以次數。兩大技術隨之成型：

- **聚合法（aggregate method）**：直接計算 m 次操作的總成本 $T(m)$，攤還成本 $T(m)/m$。
- **勢能法（potential method）**：定義資料結構的勢能函數 $\Phi(D)$，令第 i 次操作的攤還成本為

$$\hat{c}_i = c_i + \Phi(D_i) - \Phi(D_{i-1})$$

$$\sum_{i=1}^{m} c_i = \sum_{i=1}^{m} \hat{c}_i + \Phi(D_0) - \Phi(D_m) \leq \sum_{i=1}^{m} \hat{c}_i \quad (\text{若 } \Phi(D_m) \geq \Phi(D_0))$$

昂貴的操作（如深的 find）消耗勢能、便宜的操作（如壓縮後的 find）儲存勢能，總帳算下來近乎線性。

### 程式碼示範：並查集實作與 find 步數驗證

以下 Python 程式實作路徑壓縮 + 按秩合併的並查集，並計數 find 的實際沿邊步數，驗證攤還後近乎常數。

```python
import random, math

class DSU:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n
        self.steps = 0                      # 統計 find 沿邊步數

    def find(self, x):
        root = x
        self.steps += 1
        while self.parent[root] != root:
            root = self.parent[root]
            self.steps += 1
        while self.parent[x] != root:       # 路徑壓縮
            self.parent[x], x = root, self.parent[x]
        return root

    def union(self, a, b):                  # 按秩合併
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False
        if self.rank[ra] < self.rank[rb]:
            ra, rb = rb, ra
        self.parent[rb] = ra
        if self.rank[ra] == self.rank[rb]:
            self.rank[ra] += 1
        return True

n, m = 100000, 200000
d = DSU(n)
pairs = [(random.randrange(n), random.randrange(n)) for _ in range(m)]
for a, b in pairs:
    d.union(a, b)
# 第二輪：全部已是壓縮後的狀態，find 應近乎 O(1)
d.steps = 0
for a, b in pairs:
    d.find(a); d.find(b)
print(f"n={n}, m={2*m} 次 find，總步數={d.steps}")
print(f"攤還步數/操作 = {d.steps / (2*m):.3f}，log2(n) = {math.log2(n):.1f}")
print(f"alpha(n) 實用上界 = 4")
```

輸出顯示第二輪 find 的攤還步數遠小於 $\log_2 n$——近乎常數，正是 $O(\alpha(n))$ 的實測證據。

## 結案 -- 後果與影響

- 攤還分析成為資料結構分析的標準方法：動態陣列擴容、Fibonacci heap（1984/1987）、splay tree（1985）的分析全部採用聚合/勢能法。
- Kruskal 與 Prim 最小生成樹演算法獲得高效實現：判環成本從 $O(\log n)$ 降到實質常數，MST 總複雜度由排序項主導。
- $O(\alpha(n))$ 成為「實質常數」的教科書案例，出現在每一本演算法教科書中。
- Tarjan 開啟了「下界與上界緊緻」的研究風氣，自調整資料結構與動態圖演算法由此發展。
- Tarjan 於 1986 年獲圖靈獎，表揚其在演算法與資料結構分析的貢獻。

## 關鍵人物與文獻

- Robert E. Tarjan, "Efficiency of a Good But Not Linear Set Union Algorithm", Journal of the ACM, 22(2), 1975, pp. 215-225.
- Bernard A. Galler & Michael J. Fischer, "An Improved Equivalence Algorithm", Communications of the ACM, 7(5), 1964, pp. 301-303.
- John E. Hopcroft & Jeffrey D. Ullman, "Set Merging Algorithms", SIAM Journal on Computing, 2(4), 1973, pp. 294-303.
- Joseph B. Kruskal, "On the Shortest Spanning Subtree of a Graph and the Traveling Salesman Problem", Proceedings of the American Mathematical Society, 7(1), 1956, pp. 48-50.
- Robert E. Tarjan, Data Structures and Network Algorithms, SIAM, 1983.
