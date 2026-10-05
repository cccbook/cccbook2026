# 1962-FloydWarshall 與網路流

## 案件摘要
1962 年，Robert Floyd 發表了一個三重迴圈就能解決全對最短路徑（all-pairs shortest paths）的演算法；同年 Stephen Warshall 在研究電腦控制系統時獨立提出圖論版本，兩人殊途同歸，後世合稱 Floyd-Warshall 演算法。而在更早的 1956 年，Ford 與 Fulkerson 的《Maximal Flow through a Network》為網路流理論奠基。本案要偵辦的謎題是：為什麼「全對最短路」與「網路最大流」這兩件看似無關的案子，會在同一個年代先後告破？答案藏在動態規劃與對偶性這兩把鑰匙之中。

## 前因 -- 為什麼會有這個案子
- Dijkstra（1959）的演算法只解「單源」最短路徑，要得到全對答案必須以每個頂點為源頭跑 n 次，稠密圖上成本高達 O(n³) 之外還有堆積的常數負擔。
- Bell Labs 的長途電話網路與美國鐵路網都面臨同一個問題：不問「最快的路」，而問「這張網最多能同時運送多少流量」——這是 1950 年代冷戰與通訊基建的實際需求。
- Stephen Warshall 當時在 RAND 公司從事電腦控制系統研究，需要快速判斷圖上任意兩點之間是否存在路徑，也就是「傳遞閉包」問題。
- 1950 年代末，數學家開始意識到：一個問題的「最小化」版本往往隱藏著一個「最大化」的對偶版本，這條線索最終導向 max-flow min-cut 定理。

## 線索與推理 -- 數學式、程式、理論

### 線索一：Floyd 的動態規劃——中繼點逐層擴張
Floyd 的破案關鍵是一個看似平凡的觀察：從 i 到 j 的最短路，要嘛不經過編號大於 k 的中繼點，要嘛恰好經過 k 一次。令 $d^{(k)}[i][j]$ 表示「只允許使用前 k 個頂點當中繼點」時的最短距離，則有遞迴式：

$$
d^{(k)}[i][j] = \min\bigl(d^{(k-1)}[i][j],\; d^{(k-1)}[i][k] + d^{(k-1)}[k][j]\bigr)
$$

初始條件 $d^{(0)}[i][j]$ 即邊權（無邊為無窮大）。逐層擴張 k 從 1 到 n，最終 $d^{(n)}$ 就是全對最短路。驚人的是：由於第 k 層只依賴第 k-1 層，且更新 $d[i][k]$ 與 $d[k][j]$ 在本輪不會再被改動到影響自身，整個 DP 可以「原地」用一個二維陣列完成——三重迴圈、O(n³) 時間、O(n²) 空間。Warshall 的版本則更早：他處理的是布林的傳遞閉包，把 min 換成 or、加法換成 and：

$$
R^{(k)}[i][j] = R^{(k-1)}[i][j] \lor \bigl(R^{(k-1)}[i][k] \land R^{(k-1)}[k][j]\bigr)
$$

Floyd-Warshall 還能處理負邊（只要沒有負環），偵測負環只需檢查對角線：若演算法結束時 $d[i][i] < 0$，表示存在經過 i 的負環。

### 線索二：與 n 次 Dijkstra 的對照
全對問題的另一條辦案路線是跑 n 次 Dijkstra。稠密圖上 Dijkstra 用鄰接矩陣是 O(n²)，n 次共 O(n³)，與 Floyd-Warshall 同階；但稀疏圖（m = O(n)）配二元堆是 O(n²m log n) 的漸近上界之外，還要注意 Dijkstra 不能處理負邊。因此：

- 稠密圖、可能有負邊：Floyd-Warshall 勝出。
- 稀疏圖、無負邊：n 次 Dijkstra 實務上更快，因為 Floyd 的 O(n³) 是「必然跑滿」的。

### 線索三：Ford-Fulkerson 的增廣路徑與最大流最小割
Ford 與 Fulkerson 的最大流理論核心是「增廣路徑」：只要殘餘網路（residual network）中從源點 s 到匯點 t 還有一條容量為正的路徑，就能沿它推入流量、增加總流。破案時刻是他們證明了這個過程收斂到的值恰好等於最小割：

$$
\max_{f} |f| = \min_{(S,\, \bar S)} \sum_{u \in S,\, v \in \bar S} c(u, v)
$$

這個 max-flow min-cut 定理是組合優化中「對偶性」的第一個具體典範——一個可行解的價值上限，等於另一個對偶問題的下界，兩者在此相遇。Ford-Fulkerson 本身只在整數容量下保證終止；Edmonds 與 Karp（1972）發現只要每次都用 BFS 找「最短的」增廣路徑，就能把複雜度綁定為 O(VE²)，消除了病態收斂的疑雲。

### 程式佐證：Python 可執行示範

```python
INF = float('inf')

def floyd_warshall(graph, n):
    d = [[INF] * n for _ in range(n)]
    for i in range(n):
        d[i][i] = 0
    for u, v, w in graph:
        d[u][v] = min(d[u][v], w)
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if d[i][k] + d[k][j] < d[i][j]:
                    d[i][j] = d[i][k] + d[k][j]
    has_negative_cycle = any(d[i][i] < 0 for i in range(n))
    return d, has_negative_cycle

def max_flow(capacity, s, t):
    residual = [row[:] for row in capacity]
    n = len(capacity)
    flow = 0
    while True:
        parent = [-1] * n
        parent[s] = s
        queue = [s]
        while queue:
            u = queue.pop(0)
            for v in range(n):
                if parent[v] == -1 and residual[u][v] > 0:
                    parent[v] = u
                    queue.append(v)
        if parent[t] == -1:
            return flow
        path, v = [], t
        while v != s:
            path.append(v)
            v = parent[v]
        bottleneck = min(residual[parent[v]][v] for v in path)
        for v in path:
            u = parent[v]
            residual[u][v] -= bottleneck
            residual[v][u] += bottleneck
        flow += bottleneck

graph = [(0, 1, 4), (0, 2, 1), (1, 3, 1), (2, 1, 2), (2, 3, 5), (1, 3, -2)]
d, neg = floyd_warshall(graph, 4)
print("0 到 3 最短距離:", d[0][3], "| 負環:", neg)

cap = [[0, 4, 1, 0], [0, 0, 2, 1], [0, 0, 0, 5], [0, 0, 0, 0]]
print("最大流:", max_flow(cap, 0, 3))
```

執行結果：`0 到 3 最短距離: 1 | 負環: False`、`最大流: 4`——注意負邊被正確利用，繞經中繼點 0→2→1→3 反而比直達的 0→1→3（成本 5）更短。

## 結案 -- 後果與影響
- Floyd-Warshall 成為全對最短路徑的教科書標準，廣用於網路路由、交通規劃、社交網路的「六度分隔」計算。
- max-flow min-cut 定理成為組合優化對偶性的典範，影像分割、二部圖匹配、工作排程等問題都能歸約到最大流。
- 「中繼點逐層擴張」的 DP 思想成為動態規劃的經典案例，啟發了後續大量閉包與矩陣式 DP。
- Warshall 的原論文是從「傳遞閉包」出發，說明同一數學骨架可以換皮成不同問題的解。
- Edmonds-Karp 之後，Dinic（1970）等更快的最大流演算法陸續出現，網路流成為獨立的研究領域。

## 關鍵人物與文獻
- Robert W. Floyd, "Algorithm 97: Shortest Path", Communications of the ACM, 5(6): 345, 1962.
- Stephen Warshall, "A Theorem on Boolean Matrices", Journal of the ACM, 9(1): 11-12, 1962.
- L. R. Ford, Jr. and D. R. Fulkerson, "Maximal Flow through a Network", Canadian Journal of Mathematics, 8: 399-404, 1956.
- Jack Edmonds and Richard M. Karp, "Theoretical Improvements in Algorithmic Efficiency for Network Flow Problems", Journal of the ACM, 19(2): 248-264, 1972.
- E. W. Dijkstra, "A Note on Two Problems in Connexion with Graphs", Numerische Mathematik, 1: 269-271, 1959.
- Thomas H. Cormen et al., Introduction to Algorithms, 4th ed., MIT Press, 2022（第 14、22 章）.
