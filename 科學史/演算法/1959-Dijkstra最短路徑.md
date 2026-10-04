# 1959-Dijkstra最短路徑

## 案件摘要

1959 年，艾茲赫爾·戴克斯特拉（Edsger Dijkstra）在《Numerische Mathematik》發表僅兩頁半的短文〈A Note on Two Problems in Connexion with Graphs〉，一口氣解決了圖上的兩大難題：單源最短路徑與最小生成樹。據他晚年的自述，這個演算法是 1956 年他在阿姆斯特丹一家咖啡館陪未婚妻喝咖啡時，花了 20 分鐘構想出來的。案件的核心謎題是：為什麼「每次貪婪地挑最近的未確定節點」就能保證得到全域最短路徑？答案藏在「非負邊權」這個看似不起眼的假設裡。

## 前因 -- 為什麼會有這個案子

- Dijkstra 當時在阿姆斯特丹的 Stichting Mathematisch Centrum 工作，參與 ARMAC 電腦的開發；為了向公眾示範新電腦的能力，需要一個人人都懂的應用——「從阿姆斯特丹到格羅寧根的最短路線」應運而生。
- Bell Labs 的長途電話網路問題（與 Prim 1957 年的案件同源）也需要在帶權圖上尋找最省的連線與路徑。
- 理論背景：圖論的最短路徑問題在無權圖上可由廣度優先搜尋（BFS）解決，但帶權圖需要更精細的方法；含負權邊的圖則要等到 Bellman-Ford 演算法（1958，O(VE)）。
- 這類問題牽涉實際的運輸與通訊網路，1950 年代的電腦速度有限，需要一個不用窮舉所有路徑的高效解法。

## 線索與推理 -- 數學式、程式、理論

### 線索一：鬆弛操作與貪婪選擇

演算法維護每個節點的估計距離 $d[v]$，核心操作是鬆弛（relaxation）：沿著邊 $(u,v)$ 嘗試縮短到 $v$ 的路徑：

$$
d[v] = \min\left(d[v],\; d[u] + w(u, v)\right)
$$

貪婪選擇策略：每次從未確定的節點中取出 $d$ 值最小者 $u$，將其標記為確定。

### 線索二：無負邊假設的證明（貪婪不變量）

為什麼取出的 $u$ 其距離已是最優？這是不變量論證：若存在更短的路徑 $s \leadsto u$，該路徑必先離開已確定集合 $S$，設其第一條跨越邊為 $(x, y)$（$x \in S$，$y \notin S$），則：

$$
d[u] \le d[y] \le d[x] + w(x, y) + \underbrace{w(y \leadsto u)}_{\ge\, 0} \;\le\; d[u]
$$

第一步 $d[y] \le d[u]$ 來自「$u$ 是未確定節點中 $d$ 最小者」；中間的不等式需要所有邊權非負。因此非負權重是貪婪法正確性的必要條件——這正是本案最關鍵的線索。

### 線索三：負權反例的分析

若允許負邊，貪婪法會失敗。例如節點 s→A 權 1、s→B 權 4、B→A 權 -2：Dijkstra 先確定 A（d=1），但真正的最短路徑 s→B→A 長度只有 2——錯了嗎？不，此例最短路徑是 2 > 1，改用權 -4 的邊 B→A 則為 0 < 1，Dijkstra 將給出錯誤答案。含負權時必須改用 Bellman-Ford：

$$
O(V \cdot E)
$$

它對所有邊做 $|V|-1$ 輪鬆弛，且能偵測負環。

### 線索四：複雜度的兩種命運

- 樸素實現（陣列掃描找最小）：每輪 $O(V)$，共 $V$ 輪，總計 $O(V^2)$——Dijkstra 原始論文的版本，在稠密圖上仍是最優選擇。
- 優先佇列（二元堆）實現：每條邊至多觸發一次 decrease-key（或 lazy push），總計：

$$
O\big((V + E) \log V\big)
$$

稀疏圖上遠優於 $O(V^2)$。

### 破案時刻：可執行驗證

```python
import heapq

graph = {
    "Amsterdam": {"Utrecht": 46, "Den Haag": 59},
    "Utrecht": {"Amsterdam": 46, "Groningen": 159, "Den Haag": 61},
    "Den Haag": {"Amsterdam": 59, "Utrecht": 61},
    "Groningen": {"Utrecht": 159},
}

def dijkstra(graph, start):
    dist = {v: float("inf") for v in graph}
    prev = {v: None for v in graph}
    dist[start] = 0
    heap = [(0, start)]
    done = set()
    while heap:
        d, u = heapq.heappop(heap)
        if u in done:
            continue
        done.add(u)
        for v, w in graph[u].items():
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                prev[v] = u
                heapq.heappush(heap, (nd, v))
    return dist, prev

dist, prev = dijkstra(graph, "Amsterdam")

def path(prev, target):
    p = []
    while target:
        p.append(target)
        target = prev[target]
    return " -> ".join(reversed(p))

for v in ["Groningen", "Utrecht", "Den Haag"]:
    print(f"{v}: 距離 = {dist[v]} 公里, 路徑 = {path(prev, v)}")
assert dist["Groningen"] == 205
```

執行結果：阿姆斯特丹到格羅寧根的最短距離為 205 公里（經烏特勒支），實證了演算法的正確性——正是 1956 年 ARMAC 示範的翻版。

## 結案 -- 後果與影響

- 最短路徑演算法成為 GPS 導航的核心；A*（Hart, Nilsson, Raphael, 1968）是其啟發式版本，用估值函數 $f(n) = g(n) + h(n)$ 加速搜尋。
- 網路路由協定 OSPF（Open Shortest Path First）直接以 Dijkstra 演算法計算路由表，網際網路至今每天運行著它。
- Dijkstra 因包括本演算法在內的貢獻獲得 1972 年圖靈獎；他的〈Go To Statement Considered Harmful〉（1968）同樣影響深遠。
- 「20 分鐘構想」成為演算法設計的傳奇軼事——Dijkstra 晚年自述當時沒有紙筆，也刻意沒有使用鉛筆，以鍛鍊不寫下來也能思考的能力。
- 演算法的兩頁半短文也成為「簡潔論文」的典範；它與 Prim 演算法的相似結構，啟發了後世對貪婪法統一框架（如 matroid 理論）的研究。

## 關鍵人物與文獻

- E. W. Dijkstra, "A Note on Two Problems in Connexion with Graphs", *Numerische Mathematik*, 1, 1959, pp. 269–271.
- E. W. Dijkstra, "Go To Statement Considered Harmful", *Communications of the ACM*, 11(3), 1968, pp. 147–148.
- Peter E. Hart, Nils J. Nilsson, Bertram Raphael, "A Formal Basis for the Heuristic Determination of Minimum Cost Paths", *IEEE Transactions on Systems Science and Cybernetics*, 4(2), 1968, pp. 100–107.
- R. Bellman, "On a Routing Problem", *Quarterly of Applied Mathematics*, 16(1), 1958, pp. 87–90.
- Edsger W. Dijkstra, *A Discipline of Programming*, Prentice-Hall, 1976.
- Thomas H. Cormen, Charles E. Leiserson, Ronald L. Rivest, Clifford Stein, *Introduction to Algorithms*, 3rd ed., MIT Press, 2009（第 24 章：Single-Source Shortest Paths）。
