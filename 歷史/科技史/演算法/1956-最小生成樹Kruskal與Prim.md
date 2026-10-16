# 1956-最小生成樹Kruskal與Prim

## 案件摘要

1956 年，約瑟夫·克魯斯卡爾（Joseph Kruskal）在美國數學學會會議錄上發表〈On the Shortest Spanning Subtree of a Graph and the Traveling Salesman Problem〉；隔年 1957 年，貝爾實驗室的羅伯特·普林（Robert Prim）在《Bell System Technical Journal》發表〈Shortest Connection Networks and Some Generalizations〉。兩人從不同角度解決了同一個案件：如何用最短的電纜（或最便宜的邊）把所有城市連成一片網路。這個「最小生成樹」（MST）問題的破案關鍵，是證明一個看似天真的貪婪策略——每次都挑最省的邊——竟能保證全域最優。

## 前因 -- 為什麼會有這個案子

- 貝爾實驗室（Bell Labs）面臨實際工程問題：設計長途電話網路時，要用最省的電纜把所有城市連接起來，網路不能有環（多餘的邊只是浪費）。
- 早在 1926 年，捷克數學家 Otakar Borůvka 已為摩拉維亞電氣化問題發表第一個 MST 演算法，但長期被西歐與美國學界忽略，成為本案的「先聲」。
- 1950 年代中期，圖論與網路流理論興起：Ford 與 Fulkerson 1956 年發表最大流演算法，圖上的組合最佳化成為熱門戰場。
- Kruskal 當時在 Bell Labs，接觸到此問題後提出邊排序加判環的解法；Prim 則從數學家 V. Jarník（1930）的舊想法出發，獨立重新發現從點擴張的解法。

## 線索與推理 -- 數學式、程式、理論

### 線索一：MST 的定義與切割性質

給定無向加權連通圖 $G=(V,E)$，權重 $w: E \to \mathbb{R}$，最小生成樹是連通所有 $n=|V|$ 個點、恰有 $n-1$ 條邊、總權最小的樹。整個貪婪法有效性的理論核心是切割性質（cut property）：

> 將點集任意切成兩部分 $(S, V \setminus S)$，橫跨此切割的最小權邊 $e$，必定屬於某棵最小生成樹。

證明思路：若某 MST $T$ 不含 $e$，把 $e$ 加入 $T$ 會形成環，環上必有另一條橫跨切割的邊 $f$；以 $e$ 換掉 $f$ 得到總權不增的生成樹，故 $e$ 可在 MST 中。這個交換論證（exchange argument）保證「每一步都挑合法的最小邊」不會鑄成大錯。

### 線索二：Kruskal——邊排序與並查集

Kruskal 把所有邊按權重由小到大排序，逐一嘗試加入：若邊的兩端已在同一連通分量（會成環）就跳過，否則合併兩分量。判環用並查集（union-find）：

$$
\text{時間} = O(E \log E) \;(\text{排序}) + O(E \,\alpha(V)) \;(\text{並查集}) = O(E \log E)
$$

其中 $\alpha$ 是反 Ackermann 函數，實務上視為常數。

### 線索三：Prim——從點出發擴張

Prim 從任一起點開始，每次把「連到樹外、權最小」的邊所指向的點拉進樹中。用優先佇列（min-heap）實作時，每條邊至多進出堆一次：

$$
O(E \log V)
$$

### 線索四：Borůvka 的並行性與 Dijkstra 對照

- Borůvka 演算法：每個連通分量各自挑出其最小外接邊，全部同時合併，每輪分量數至少減半，共 $O(\log V)$ 輪——天然適合並行計算，日後成為高效並行 MST 演算法的基礎。
- 與 Dijkstra 演算法的對照：兩者結構相似（都是「由近到遠」擴張），但 Dijkstra 累加的是整條路徑長度 $\text{dist}[u] + w(u,v)$，Prim 只看單邊權重 $w(u,v)$——一字之差，解的是完全不同的問題。

### 破案時刻：可執行驗證

```python
import heapq

edges = [
    ("A", "B", 7), ("A", "C", 9), ("A", "F", 14), ("B", "C", 10),
    ("B", "D", 15), ("C", "D", 11), ("C", "F", 2), ("D", "E", 6),
    ("E", "F", 9),
]

def kruskal(V, E):
    parent = {v: v for v in V}
    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    total, mst = 0, []
    for u, v, w in sorted(E, key=lambda e: e[2]):
        ru, rv = find(u), find(v)
        if ru != rv:
            parent[ru] = rv
            total += w
            mst.append((u, v, w))
    return total, mst

def prim(V, E):
    adj = {v: [] for v in V}
    for u, v, w in E:
        adj[u].append((w, v)); adj[v].append((w, u))
    start = V[0]
    visited = {start}
    heap = list(adj[start]); heapq.heapify(heap)
    total, mst = 0, []
    while len(visited) < len(V):
        w, v = heapq.heappop(heap)
        if v in visited:
            continue
        visited.add(v)
        total += w
        mst.append((v, w))
        for e in adj[v]:
            heapq.heappush(heap, e)
    return total, mst

t1, m1 = kruskal(list("ABCDEF"), edges)
t2, _ = prim(list("ABCDEF"), edges)
print("Kruskal MST 總權 =", t1, m1)
print("Prim    MST 總權 =", t2)
assert t1 == t2
```

執行後兩種演算法都給出總權 33 的最小生成樹，實證了貪婪法的一致性。

## 結案 -- 後果與影響

- Kruskal 與 Prim 成為貪婪演算法（greedy algorithm）的兩座里程碑，「切割性質 + 交換論證」成為證明貪婪演算法正確性的標準套路。
- 並查集（union-find）因 Kruskal 演算法的需求而發展，Tarjan 於 1975 年給出帶有路徑壓縮與按秩合併的 $O(E\,\alpha(V))$ 攤還分析，成為資料結構理論的經典。
- MST 成為網路設計（電信、電力、管線）、資料聚類（單連結聚類）、近似演算法（TSP 的 2-approximation 以 MST 為跳板）的基礎工具。
- Borůvka 演算法在並行計算時代重獲重視，成為並行與外存（external memory）MST 演算法的骨架。
- 問題本身也催生了 Steiner 樹、度限制生成樹等變體研究。

## 關鍵人物與文獻

- Joseph B. Kruskal, "On the Shortest Spanning Subtree of a Graph and the Traveling Salesman Problem", *Proceedings of the American Mathematical Society*, 7(1), 1956, pp. 48–50.
- Robert C. Prim, "Shortest Connection Networks and Some Generalizations", *Bell System Technical Journal*, 36(6), 1957, pp. 1389–1401.
- Otakar Borůvka, "O jistém problému minimálním"（關於一個最小化問題）, *Práce mor. přírodověd. spol. v Brně*, 3, 1926.
- E. W. Dijkstra, "A Note on Two Problems in Connexion with Graphs", *Numerische Mathematik*, 1, 1959, pp. 269–271.
- Robert E. Tarjan, "Efficiency of a Good But Not Linear Set Union Algorithm", *Journal of the ACM*, 22(2), 1975, pp. 215–225.
- Thomas H. Cormen, Charles E. Leiserson, Ronald L. Rivest, Clifford Stein, *Introduction to Algorithms*, 3rd ed., MIT Press, 2009（第 23 章：Minimum Spanning Trees）。
