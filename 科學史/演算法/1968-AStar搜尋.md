# 1968-AStar搜尋

## 案件摘要

1968 年，SRI International 的 Peter Hart、Nils Nilsson 與 Bertram Raphael 發表〈A Formal Basis for the Heuristic Determination of Minimum Cost Paths〉，為啟發式搜尋建立了嚴格的數學基礎——這就是後來通稱的 A* 演算法。 案子的起點是 SRI 的機器人 Shakey：它需要在陌生環境中規劃從 A 到 B 的最短路徑，但 Dijkstra 演算法的盲目擴張太慢。 三位偵探提出的解方是一條看似簡單的公式 $f(n) = g(n) + h(n)$，並證明：只要啟發式函數「永不高估」，A* 找到的路徑必然最優。

## 前因 -- 為什麼會有這個案子

- Shakey 機器人（SRI，1966–1972）是第一台能自主感知與行動的行動機器人，路徑規劃是它的核心需求；格狀地圖上的最短路徑計算每秒都在進行。
- Dijkstra 演算法（1959）雖然保證最優，卻是「盲目」的：它像水波一樣向所有方向等速擴張，浪費大量算力在背離目標的節點上。
- 啟發式搜尋的概念在 20 世紀中葉已經模糊存在（賽局樹搜尋、人類解謎的經驗法則），但沒有人證明過「帶估計的搜尋」何時仍然最優；如何把「往目標方向的直覺」形式化，且不破壞 Dijkstra 的最優性保證，是當時的挑戰。

## 線索與推理 -- 數學式、程式、理論

### 線索一：A* 的核心公式

A* 為每個節點 $n$ 評估一個分數：

$$
f(n) = g(n) + h(n)
$$

其中 $g(n)$ 是從起點到 $n$ 的實際已知成本，$h(n)$ 是從 $n$ 到目標的啟發式估計，故 $f(n)$ 即「若經由 $n$ 前往目標，估計的總成本」。A* 每次從優先佇列取出 $f$ 值最小的節點擴張。

### 線索二：可採納性與最優性

Hart、Nilsson、Raphael 的關鍵定理：若 $h(n) \leq h^*(n)$（$h^*$ 是真實最優成本），則 A* 必找到最優路徑。

$$
\text{admissible:} \quad 0 \leq h(n) \leq h^*(n) \quad \forall n
$$

證明骨架：設目標 $t$ 被取出時的成本為 $g(t)$。反設存在更優路徑，其上必有一個仍在佇列中的節點 $n$，滿足

$$
f(n) = g(n) + h(n) \leq g(n) + h^*(n) = C^* < g(t)
$$

但 A* 取出了 $f$ 值更大的 $t$，矛盾，故 $g(t) = C^*$。

### 線索三：一致性（consistency）與啟發式距離

更強的條件是三角不等式：

$$
h(n) \leq c(n, n') + h(n') \quad \forall (n, n') \in E
$$

一致性蘊含可採納性，且保證 $f$ 沿任何路徑單調不減、每個節點最多被擴張一次。曼哈頓距離 $h_{\text{M}}(n) = |x_n - x_t| + |y_n - y_t|$ 與歐氏距離 $h_{\text{E}}(n) = \sqrt{(x_n - x_t)^2 + (y_n - y_t)^2}$ 在格子世界中都是一致的啟發式。

### 線索四：與其他演算法的對照

$h \equiv 0$ 時 A* 退化為 Dijkstra（$f = g$，均勻擴張、最優但盲目）；只有 $h$ 的貪婪最佳優先直奔目標、快但不保證最優；A* 的 $f = g + h$ 兼得最優與方向感，且 $h$ 越接近 $h^*$，擴張越少。

### 線索五：Python 實作與實測

以下程式在網格世界上實作 A*（heapq + 曼哈頓啟發式），並與 Dijkstra 對照擴張節點數：

```python
import heapq
GRID = ["..........", ".####.....", ".####..##.", ".......##.",
        "..##......", "..##..####", "......####", ".........."]
H, W = len(GRID), len(GRID[0])
START, GOAL = (0, 0), (7, 9)

def neighbors(p):
    r, c = p
    for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        nr, nc = r + dr, c + dc
        if 0 <= nr < H and 0 <= nc < W and GRID[nr][nc] == ".":
            yield (nr, nc), 1

def search(hfn, label):                       # 通用：h=0 即 Dijkstra
    openq, gbest, expanded = [(hfn(START), 0, START)], {START: 0}, 0
    while openq:
        f, g, node = heapq.heappop(openq)
        if g > gbest.get(node, float("inf")):
            continue
        expanded += 1
        if node == GOAL:
            print(f"{label:>9}: cost={g}, expanded={expanded}")
            return g, expanded
        for nxt, w in neighbors(node):
            ng = g + w
            if ng < gbest.get(nxt, float("inf")):
                gbest[nxt] = ng
                heapq.heappush(openq, (ng + hfn(nxt), ng, nxt))
    return None, expanded

manh = lambda p: abs(p[0]-GOAL[0]) + abs(p[1]-GOAL[1])   # 曼哈頓啟發式
c_astar, e_astar = search(manh, "A*")
c_dijk, e_dijk = search(lambda p: 0, "Dijkstra")          # h=0
print(f"cost equal: {c_astar == c_dijk}; "
      f"A* expands {e_dijk / e_astar:.2f}x fewer nodes than Dijkstra")
```

理論預測：兩者找到的路徑成本相同（可採納性 ⇒ 最優性），但 A* 擴張的節點數明顯較少——$h$ 的方向感把搜尋從「水波」變成「箭頭」。

## 結案 -- 後果與影響

- A* 成為 AI 搜尋的標準：遊戲尋路（RTS、迷宮）、機器人運動規劃、路網導航皆以它為基礎。
- 啟發式變體家族誕生：IDA*（1985，迭代加深、記憶體極省）、SMA*、Weighted A*（放棄最優性換速度）；「admissible heuristic」成為啟發式設計的準則。
- 啟發式品質的研究：$h$ 與 $h^*$ 的差距決定擴張量，催生了 pattern database（2000 年代）等強啟發式技術。
- Shakey 的視覺＋規劃架構是 AI agent 的先驅：感知—規劃—行動的閉環，影響了後世所有行動機器人與 STRIPS 規劃系統。

## 關鍵人物與文獻

- Peter E. Hart / Nils J. Nilsson / Bertram Raphael：SRI 人工智慧中心研究員，A* 的提出與證明者；Nilsson 後為史丹佛教授，Shakey 規劃系統負責人。
- Edsger W. Dijkstra：最短路徑演算法（1959）的發明者，A* 的退化基準；Richard E. Korf 則是 IDA*（1985）的發明者。

主要文獻：

- Hart, P. E., Nilsson, N. J., & Raphael, B. (1968). "A Formal Basis for the Heuristic Determination of Minimum Cost Paths". *IEEE Transactions on Systems Science and Cybernetics*, 4(2), 100–107.
- Hart, P. E., Nilsson, N. J., & Raphael, B. (1972). "Correction to 'A Formal Basis for the Heuristic Determination of Minimum Cost Paths'". *ACM SIGART Bulletin*, 37, 28–29.
- Dijkstra, E. W. (1959). "A Note on Two Problems in Connexion with Graphs". *Numerische Mathematik*, 1(1), 269–271.
- Korf, R. E. (1985). "Depth-First Iterative-Deepening: An Optimal Admissible Tree Search". *Artificial Intelligence*, 27(1), 97–109.
- Nilsson, N. J. (1984). "Shakey The Robot". SRI International Technical Note 323.
