# 演算法歷史年表

> 副標題：從 von Neumann 的合併排序到 Adam 優化器——一場「把問題變快、把快變成理論」的運動。
>
> 每一個條目對應本目錄中的一篇「推理探案」風格 wiki：`年份-標題.md`

## 第一幕：排序與圖論的奠基（1945–1965）

| 年份 | 事件 | wiki |
|---|---|---|
| 1945 | von Neumann 發明合併排序（merge sort）：分治法的誕生，EDVAC 報告時代的副產品 | [1945-合併排序](1945-合併排序.md) |
| 1956 | Kruskal 與 Prim 發明最小生成樹演算法：貪婪法的兩座里程碑 | [1956-最小生成樹Kruskal與Prim](1956-最小生成樹Kruskal與Prim.md) |
| 1957 | Richard Bellman 出版《Dynamic Programming》：動態規劃（DP）的正式誕生，「最佳化原理」與重疊子問題 | [1957-Bellman動態規劃](1957-Bellman動態規劃.md) |
| 1959 | Dijkstra 發明最短路徑演算法：20 分鐘構想的 O(n²) 貪婪法，GPS 導航的祖先 | [1959-Dijkstra最短路徑](1959-Dijkstra最短路徑.md) |
| 1960 | Tony Hoare 發明快速排序（quicksort）：分治＋分割的實務王者 | [1960-快速排序](1960-快速排序.md) |
| 1964 | Williams 發明堆積排序、Floyd 改良堆積建構：完全二元樹的 O(n log n) 排序 | [1964-堆積排序與Floyd](1964-堆積排序與Floyd.md) |
| 1965 | Jack Edmonds 發表《Paths, Trees, and Flowers》：提出「好演算法」（多項式時間）的正式定義， blossom 演算法證明匹配問題是 P | [1965-Edmonds與多項式時間](1965-Edmonds與多項式時間.md) |

## 第二幕：演算法的理論化與複雜性革命（1968–1979）

| 年份 | 事件 | wiki |
|---|---|---|
| 1968 | Knuth 出版《The Art of Computer Programming》第一卷：演算法分析（analysis of algorithms）成為學科，大 O 記法從數學進入電腦科學 | [1968-KnuthTAOCP與演算法分析](1968-KnuthTAOCP與演算法分析.md) |
| 1968 | Hart、Nilsson、Raphael 發明 A* 搜尋：啟發式函數＋最優性的證明，AI 搜尋與遊戲尋路的標準 | [1968-AStar搜尋](1968-AStar搜尋.md) |
| 1969 | Strassen 發明矩陣乘法 O(n^2.807)：第一次打破「矩陣乘法必須 O(n³)」的直覺，分治遞迴的威力 | [1969-Strassen矩陣乘法](1969-Strassen矩陣乘法.md) |
| 1971 | Cook 提出 NP 完備性理論（Cook-Levin 定理）：SAT 是 NP-complete，「P vs NP」的第一個錨點 | [1971-NP完備性與CookLevin](1971-NP完備性與CookLevin.md) |
| 1972 | Karp 發表《Reducibility Among Combinatorial Problems》：21 個經典問題皆 NP-complete，歸約（reduction）成為標準武器 | [1972-Karp21題](1972-Karp21題.md) |
| 1975 | Tarjan 分析並查集（union-find）：路徑壓縮＋按秩合併的攤還複雜度 O(α(n))——反 Ackermann 函數，攤還分析的誕生 | [1975-Tarjan並查集與攤還分析](1975-Tarjan並查集與攤還分析.md) |
| 1977 | Knuth、Morris、Pratt 發表 KMP 字串匹配演算法：O(n+m) 的線性時間匹配，失配表的智慧 | [1977-KMP字串匹配](1977-KMP字串匹配.md) |
| 1979 | Khachiyan 發明椭球法（ellipsoid method）：線性規劃首次被證明是多項式時間可解，Klee-Minty 立方體的反擊 | [1979-椭球法與線性規劃](1979-椭球法與線性規劃.md) |

## 第三幕：演算法進入工業與網路時代（1998–2010s）

| 年份 | 事件 | wiki |
|---|---|---|
| 1998 | Brin 與 Page 發表 PageRank：以「隨機漫遊的平穩分佈」重寫網頁排序，Google 的數學心臟 | [1998-PageRank與Google](1998-PageRank與Google.md) |
| 2014 | Kingma 與 Ba 發表 Adam 優化器：動量＋自適應學習率的隨機梯度優化，深度學習的引擎 | [2014-Adam與隨機梯度優化](2014-Adam與隨機梯度優化.md) |

## 主線索回顧（偵探筆記）

1. **分治法**：合併排序（1945）→ 快速排序（1960）→ Strassen（1969）——把問題切成一半，複雜度從 n² 降到 n log n，甚至 n^2.807。
2. **貪婪法**：Kruskal/Prim（1956）、Dijkstra（1959）——「每步取局部最優」何時有效？需要 greedy-choice property 的證明。
3. **動態規劃**：Bellman（1957）——重疊子問題＋最佳子結構，用空間換時間；DP 是「記憶化的暴力」。
4. **複雜性理論**：Edmonds 的「好演算法」（1965）→ Cook-Levin（1971）→ Karp 21 題（1972）——P vs NP 的世紀懸案。
5. **攤還分析**：Tarjan（1975）——單次操作可能慢，但總成本有界；資料結構的分析從最壞情況轉向攤還。
6. **啟發式與工業**：A*（1968）的 admissible heuristic、PageRank（1998）的平穩分佈、Adam（2014）的動量——理論與工程的最優結合。

## 關鍵人物

- **John von Neumann**：合併排序、EDVAC
- **Richard Bellman**：動態規劃
- **Joseph Kruskal / Robert Prim**：最小生成樹
- **Edsger Dijkstra**：最短路徑、堆疊、結構化編程
- **Tony Hoare**：快速排序
- **John Williams / Robert Floyd**：堆積排序
- **Jack Edmonds**：多項式時間、blossom
- **Donald Knuth**：TAOCP、演算法分析、KMP
- **Peter Hart / Nils Nilsson / Bertram Raphael**：A*
- **Volker Strassen**：矩陣乘法
- **Stephen Cook**：NP 完備性
- **Richard Karp**：21 題、歸約
- **Robert Tarjan**：並查集、攤還分析
- **Leonid Khachiyan**：椭球法
- **Larry Page / Sergey Brin**：PageRank
- **Diederik Kingma / Jimmy Ba**：Adam
