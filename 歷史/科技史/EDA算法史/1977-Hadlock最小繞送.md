# 1977-Hadlock最小繞送

## 案件摘要
Lee 演算法（1961）保證最短但淹板，線搜尋（1969）省記憶體但不保證最短——魚與熊掌能否兼得？1977 年，數學家 Frank Hadlock 發表格子圖最短路的研究，揭示了破案鑰匙：**把「最短」重寫成「最少繞送（detour）」**。若路徑長 $L = M + 2d$（$M$ 是起終點的曼哈頓距離，$d$ 是背離目標的步數），則找最短路 ⟺ 找繞送數最小的路。以繞送數為搜尋指標，波前只沿「朝目標」方向優先擴展——這正是 A* 演算法（Hart-Nilsson-Raphael, 1968）在格子圖上的最優化實例。Hadlock 的工作成為 A* 繞線的理論基礎，今日所有 EDA detailed routing 引擎的「預估函數 $f = g + h$」，都以此為數學根據。

## 前因 -- 為什麼會有這個案子
- **Lee 的淹板矛盾**：BFS 四方向無差別擴展，大量探索與目標相反方向的格子——記憶體與時間都浪費。
- **線搜尋失了最優性**：Mikami/Hightower 為省記憶體犧牲最短保證，對時序關鍵 net 不可接受。
- **AI 領域的 A* 已誕生**（1968）：Hart-Nilsson-Raphael 證明：只要啟發函數 $h$ 不高估剩餘距離（admissible），A* 找到的必是最短路——理論工具就緒，缺格子圖上的應用與分析。
- **手工佈線的直覺**：人類佈線員「先直奔目標，被迫才繞」——繞送數正是這個直覺的數學化。

## 線索與推理 -- 數學式、程式、理論

### 核心：最短 ⟺ 最少繞送
設起點 $s$、終點 $t$，曼哈頓距離 $M = |x_s - x_t| + |y_s - y_t|$。任何路徑 $P$ 滿足：

$$|P| = M + 2 \cdot d(P)$$

其中 $d(P)$ 是**繞送數**——背離目標方向（使距離暫時 +1）的步數。每繞一步多走 2 步（繞去又繞回）。因此：

$$\min |P| \iff \min d(P)$$

於是搜尋指標從「步數」換成「繞送數」：以 $f(n) = g(n) + h(n)$ 為優先序（$g$ = 已走繞送，$h$ = 到目標的曼哈頓距離），用優先佇列擴展——**$h$ 恰是 admissible 啟發**（曼哈頓距離不會高估剩餘步數），A* 最優性定理直接適用：

$$h(n) \le h^*(n) \implies \text{A* 首次擴展 } t \text{ 時即最優}$$

### 複雜度的推理
BFS 探索半徑為 $M + 2d^*$ 的**整個**菱形區域；A* 以 $h$ 引導，理論上只探索繞送 $\le d^*$ 的區域。實測上記憶體與時間常省一個數量級——最優性與效率同時到手，魚與熊掌兼得。

```python
import heapq

def a_star_route(grid, start, goal):
    """f = g + h，h = 曼哈頓距離（admissible）→ 首達即最短。"""
    R, C = len(grid), len(grid[0])
    h = lambda p: abs(p[0]-goal[0]) + abs(p[1]-goal[1])
    heap = [(h(start), 0, start)]
    g = {start: 0}; parent = {}
    while heap:
        f, gv, cur = heapq.heappop(heap)
        if cur == goal:
            path = [cur]
            while cur in parent: cur = parent[cur]; path.append(cur)
            return path[::-1]
        if gv > g[cur]: continue
        for dr, dc in ((1,0),(-1,0),(0,1),(0,-1)):
            nr, nc = cur[0]+dr, cur[1]+dc
            if 0 <= nr < R and 0 <= nc < C and grid[nr][nc] == 0:
                ng = gv + 1
                if ng < g.get((nr,nc), 10**9):
                    g[(nr,nc)], parent[(nr,nc)] = ng, cur
                    heapq.heappush(heap, (ng + h((nr,nc)), ng, (nr,nc)))
    return None
```

### 工程化：懲罰與擁塞
Hadlock/A* 框架的真正威力在**格子代價可自訂**：把擁塞、過孔成本、層切換成本寫進 $g$，把預估擁塞寫進 $h$——現代 negotiated congestion routing（PathFinder, 1990s）就是在 A* 骨架上迭代調整代價。

## 結案 -- 後果與影響
- **A* 成為 detailed routing 內核**：從 1977 到今日，所有商用繞線器的格點搜尋都以 A* 為骨幹；Lee 演算法退居「全網互斥檢查」與教學角色。
- **最優性證明進入 EDA**：admissible 啟發 + A* 定理的引入，讓繞線器第一次有「既快又證明最短」的數學保證。
- **擁塞談判的骨架**：A* 的可自訂代價催生 PathFinder 式 negotiated routing（FPGA 繞線標準）與現代 global routing 的迷宮式談判。
- **理論傳播**：Hadlock 的論文（Networks 期刊）成為格子圖最短路的經典文獻，EDA 與組合最佳化在此案交會。

## 關鍵人物與文獻
- **Frank O. Hadlock**：數學家，格子圖最短路理論。
- **P. E. Hart, N. J. Nilsson, B. Raphael**：SRI，A* 演算法發明者（1968）。
- 文獻：
  - F. O. Hadlock, "A Shortest Path Algorithm for Grid Graphs," *Networks* 7, 323 (1977).
  - P. E. Hart, N. J. Nilsson, B. Raphael, "A Formal Basis for the Heuristic Determination of Minimum Cost Paths," *IEEE Trans. SSC* 4, 100 (1968).
  - L. McMurchie, C. Ebeling, "PathFinder: A Negotiation-Based Performance-Driven Router for FPGAs," *FPGA* 1995.
