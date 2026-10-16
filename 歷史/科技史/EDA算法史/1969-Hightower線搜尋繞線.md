# 1969-Hightower線搜尋繞線

## 案件摘要
Lee 迷宮演算法（1961）保證最短，但要淹沒整張板——磁心記憶體時代這是奢侈。1968-69 年，Mikami-Tabuchi（日立）與 David Hightower（Bell Labs，德州儀器時期）先後找到破案新招：**別一格一格地走，改用一條條線段探索**。從起點沿水平垂直線延伸直到撞到障礙，在每個可行位置轉 90° 再延伸——候選「路徑骨架」從 $O(n)$ 個格子爆降到幾十條線段。線搜尋（line-search）繞線因此把記憶體需求砍掉幾個數量級，成為 1970-80 年代商用繞線器的主力，其思想直通今日 A* 繞線器的 escape segments。

## 前因 -- 為什麼會有這個案子
- **Lee 的記憶體飢渴**：一次繞線要標記整板格子；1960 年代記憶體昂貴，大板或密板直接跑不動。
- **速度也不夠**：淹板式搜尋浪費大量無關方向的探索；工程上需要「直奔目標」的啟發式。
- **連續平面的直覺**：人類佈線員靠「沿牆走、找缺口」的線段直覺，而非逐格數步——演算法應效法。
- **IBM 設計自動化的經驗**（1957-64）已證明走線可以機器化，缺的是更省的搜尋方式。

## 線索與推理 -- 數學式、程式、理論

### 核心：線段取代格子
從源點 $s$ 與目標 $t$ 各發出互交的延伸線（extend lines），規則：
1. 從起點向四方向延伸，直到撞上障礙（obstacle）；
2. 在每個「未探索的可行位置」轉 90°，發出垂直於原線的新延伸線；
3. 反覆直到兩族的線相交——交點即候選路徑。

狀態空間從「格子」變成「線段」，複雜度從 $O(n)$（$n$=格數）降到與障礙輪廓數成正比，通常僅幾十至幾百條線段。

```python
def line_search(obstacles, start, goal):
    """簡化示意：返回水平/垂直延伸線段數量級的探索示意。"""
    segs, frontier = [], [start]
    visited = set()
    while frontier and goal not in visited:
        nxt = []
        for p in frontier:
            for axis in ('h', 'v'):            # 水平與垂直延伸
                segs.extend(extend_to_obstacles(p, axis, obstacles))
        for s in segs:
            if intersects(s, goal): return reconstruct(segs)
            nxt += escape_points(s, visited)   # 線段端點轉 90°
        frontier = nxt
    return None
```

### 代價：不再保證最短
線搜尋找到的路徑**轉折不一定最少**，也不保證最短——這是用完整性換效率的交易。補救之道：
- **Mikami-Tabuchi（1968）**：每次從**所有**已生成線段延伸，較完整但較慢；
- **Hightower（1969）**：只從最新線段延伸（深度優先味），極快但可能漏解，需回溯；
- **Soukup（1978）**：朝目標方向加速推進（近 A* 的貪心），撞牆才回頭；
- **Hadlock（1977）**：堅持最短路，但以「繞送數（detours）」為搜尋指標——A* 家族的正統（見 1977 卷宗）。

### 逃逸點的細節
Hightower 的關鍵技巧是「逃逸點（escape point）」：轉彎處不取端點本身，而取越過障礙邊界一小段的位置，避免在死角打轉。這種幾何細節處理，成為線搜尋演算法工程品質的分水嶺。

## 結案 -- 後果與影響
- **商用繞線器的主力**：1970-80 年代 Calma、Applicon 等 CAD 系統的互動繞線與 PCB 佈線大量採用線搜尋，速度比 Lee 快一到兩個數量級。
- **通往 A* 的橋樑**：Soukup 的方向性推進 + Hadlock 的可採納啟發，合流成現代 A* 繞線——今日 detailed routing 引擎的每一次「局部修正」，內核都是線搜尋 + A*。
- **與格子法的分工**：工程上形成「全域用迷宮/Steiner，局部用線搜尋」的分工，成為 global routing / detailed routing 兩階段範式的先聲。
- **互動式設計的誕生**：線搜尋快到可以「邊畫邊算」，催生了互動式版圖編輯（後繼者：Magic, 1983）。

## 關鍵人物與文獻
- **David W. Hightower**：德州儀器→Bell Labs，線搜尋繞線的命名者與集大成者。
- 文獻：
  - K. Mikami, K. Tabuchi, "A Computer Program for Optimal Routing of Printed Circuit Connectors," *IFIPS* 1968.
  - D. W. Hightower, "A Solution to Line-Routing Problems on the Continuous Plane," *6th Design Automation Workshop*, 1969.
  - J. Soukup, "Fast Maze Router," *DAC* 1978.
