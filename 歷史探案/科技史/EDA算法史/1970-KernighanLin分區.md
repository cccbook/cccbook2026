# 1970-KernighanLin分區

## 案件摘要
晶片上的電路要切成一塊塊板子、一層層模組，切法決定跨板連線數——連線越少，成本與延遲越低。「把圖切成兩半、讓跨邊最少」是最小割問題的平衡版：普通 min-cut 演算法（最大流，1962 Ford-Fulkerson）不保證兩側大小均衡。1970 年，貝爾實驗室的 Brian Kernighan 與沈學緯（Shen Lin）發表 KL 演算法：反覆「成對交換」兩側節點，用增益函數記帳、每輪結束取最佳前綴回溯——首次讓**平衡分區**有大規模實用的啟發式。它與其線性時間後繼 FM（1982）共同構成半世紀來所有分區與 min-cut 佈局的祖譜。

## 前因 -- 為什麼會有這個案子
- **模組化是必需**：主機由數十塊板組成，跨板連線（backplane wiring）是成本與可靠性的大敵。
- **min-cut 不平衡**：最大流方法會切出「一側只有一個節點」的退化割，毫無工程價值——需要帶平衡約束的最小割：

$$\min_{(A,B)}\ |\{(u,v) \in E : u \in A, v \in B\}| \quad \text{s.t.}\ |A| = |B| \ (\pm \epsilon)$$

- **此問題 NP-困難**（圖二分平衡割是 NP-hard；Karp 1971 時代理論已就緒）——只能啟發式。
- **貝爾的現場**：Kernighan（後以 Unix 聞名）與 Lin 都在研究印刷電路板設計，Lin 1965 已有簡單交換法。

## 線索與推理 -- 數學式、程式、理論

### 核心：增益記帳 + 最佳前綴回溯
定義節點的外部代價 $E(a)$（連到對側的邊權和）與內部代價 $I(a)$（連到同側的邊權和），差值增益：

$$D(a) = E(a) - I(a)$$

交換一對 $(a, b)$ 的淨增益：

$$g(a,b) = D(a) + D(b) - 2\,c(a,b)$$

（$c(a,b)$ 是 $a,b$ 間的邊權，被算了兩次要扣回。）KL 的一輪（pass）：

1. 計算所有 $D$ 值；
2. 貪心選出當前增益最大的未鎖定對 $(a_i, b_i)$，交換、鎖定、更新 $D$；重複 $n/2$ 次；
3. **關鍵**：即使中途增益變負也不停手（先變差後變好是常態），記錄每步的累計增益 $G_i = g_1 + \dots + g_i$；
4. 一輪結束，取 $G_i$ 最大的**最佳前綴** $i^*$ 回溯——只保留前 $i^*$ 次交換，其餘撤銷。

$$i^* = \arg\max_i\ G_i, \quad \text{取 } \max_i G_i > 0 \text{ 才繼續下一輪}$$

這個「允許暫時變差 + 最佳前綴回溯」是後世一切局部搜尋（tabu search、模擬退火的深度優先前驅）的共同祖先之一。

### 複雜度與工程
- 一輪 $O(n^2 \log n)$（用堆選對）或 $O(n^2)$（直接法）；數輪到局部最優。
- 1973 Kernighan-Lin 把 KL 推廣到 $k$ 路分區與點權重。
- 工程技巧：隨機重啟、多起點取最好——確定性時代少見的統計思維。

### 範例
四節點圖：A 側 {1,2}、B 側 {3,4}，邊：1-3(3), 1-4(2), 2-3(4), 2-4(1), 1-2(3), 3-4(1)。$D(1) = 3+2-3 = 2$，$D(3) = 3+4-1 = 6$，交換 (1,3) 增益 $g = 2+6-2(0) = 8$（1、3 無直接邊）——一輪交換即把割從 10 降到 2。KL 的記帳讓每一步的收益可算、可回溯。

## 結案 -- 後果與影響
- **分區成為 EDA 標配**：KL 被 PCB 分板、邏輯劃分、min-cut 佈局（Dunlop-Kernighan 1985 的實踐）廣泛採用。
- **FM 的直系祖先**：Fiduccia-Mattheyses（1982）保留其增益記帳與回溯思想，把「成對交換」換成「單點搬移」、把記帳結構換成桶串，複雜度降到 $O(|E|)$。
- **Kernighan 的雙遺產**：同一位作者留下 Unix（K&R C）與 KL 演算法——系統與演算法兩個世界都欠他一份卷宗。
- **多層時代的伏筆**：KL/FM 的局部性限制，最終由 1997 年多層分區（hMetis）以「粗化-反粗化」突破；但每一層的最粗段，跑的仍是 KL/FM。

## 關鍵人物與文獻
- **Brian Kernighan**（1942–）：貝爾實驗室，Unix、C 語言與 KL 分區。
- **Shen Lin（沈學緯）**（1931–2018）：貝爾實驗室，分區與 TSP 啟發式（Lin-Kernighan, 1973）。
- 文獻：
  - B. W. Kernighan, S. Lin, "An Efficient Heuristic Procedure for Partitioning Graphs," *Bell Syst. Tech. J.* 49, 291 (1970).
  - S. Lin, B. W. Kernighan, "An Effective Heuristic Algorithm for the Traveling-Salesman Problem," *Operations Research* 21, 498 (1973).
  - C. M. Fiduccia, R. M. Mattheyses, "A Linear-Time Heuristic for Improving Network Partitions," *DAC* 1982.
