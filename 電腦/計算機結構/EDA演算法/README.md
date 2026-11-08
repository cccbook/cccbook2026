# 《計算的晶片：EDA 演算法的歷史與內幕》目錄

一本寫給軟體工程師、EDA 研發工程師與計算機工程研究生的書——深入晶片設計自動化的引擎蓋之下，系統化拆解從邏輯表示、綜合、切割擺放到繞線簽核的核心數學模型與演算法，並對比 ASIC 的連續幾何約束與 FPGA 的離散資源約束。

每一節都從真實的歷史事件出發：誰在哪一年、因為什麼經濟與制度的壓力、發明了什麼演算法，然後才講清楚這個演算法今天怎麼寫。

---

## 目錄

* 第1章-紙上算出晶片：EDA 的起源與計算複雜度的詛咒
    * [1.1-從畫圖紙到畫電路：1950-1980 的自動化萌芽](01.1-從畫圖紙到畫電路：自動化的萌芽.md)
    * [1.2-NP-Hard 無所不在：為什麼晶片問題永遠解不完](01.2-NP-Hard無所不在：為什麼晶片問題永遠解不完.md)
    * [1.3-啟發式與近似演算法：在完美與可行之間妥協](01.3-啟發式與近似演算法：在完美與可行之間妥協.md)
    * [1.4-圖與超圖：把幾百萬個電晶體變成數學物件](01.4-圖與超圖：把幾百萬個電晶體變成數學物件.md)

* 第2章-布林的遺產：邏輯表示與 SAT 求解
    * [2.1-香農 1937 論文之後：布林代數如何進入工程世界](02.1-香農1937論文之後：布林代數如何進入工程世界.md)
    * [2.2-BDD 的革命：Bryant 1986 與 ROBDD 正準形式的運算](02.2-BDD的革命：Bryant1986與ROBDD正準形式的運算.md)
    * [2.3-AIG 與 ABC：Berkeley 的開源邏輯優化帝國](02.3-AIG與ABC：Berkeley的開源邏輯優化帝國.md)
    * [2.4-SAT 求解器二十年的躍進：從 Davis-Putnam 到 CDCL](02.4-SAT求解器二十年的躍進：從Davis-Putnam到CDCL.md)

* 第3章-綜合的鍊金術：從程式碼到閘電路
    * [3.1-高階綜合的起伏：1980 年代的夢、失落與回歸](03.1-高階綜合的起伏：1980年代的夢、失落與回歸.md)
    * [3.2-排程演算法：ASAP/ALAP、List Scheduling 與力導向排程](03.2-排程演算法：ASAP-ALAP、ListScheduling與力導向排程.md)
    * [3.3-資源分配與綁定：圖著色與最大加權二分匹配](03.3-資源分配與綁定：圖著色與最大加權二分匹配.md)
    * [3.4-兩級邏輯優化：Quine-McCluskey 與 Espresso 的啟發式展開](03.4-兩級邏輯優化：Quine-McCluskey與Espresso的啟發式展開.md)
    * [3.5-多級邏輯優化：MIS/SIS 的分解、抽取與代入](03.5-多級邏輯優化：MIS-SIS的分解、抽取與代入.md)
    * [3.6-技術映射的 ASIC 之路：Pattern Matching 與 cut-based 映射](03.6-技術映射的ASIC之路：PatternMatching與cut-based映射.md)
    * [3.7-技術映射的 FPGA 之路：K-LUT 與 FlowMap 演算法](03.7-技術映射的FPGA之路：K-LUT與FlowMap演算法.md)
    * [3.8-Retiming：Leiserson-Saxe 演算法與跨暫存器搬移的等價性](03.8-Retiming：Leiserson-Saxe演算法與跨暫存器搬移的等價性.md)

* 第4章-切割與樓板規劃：把百萬閘分而治之
    * [4.1-Kernighan-Lin 的 1970 年論文：成對交換與增益序列](04.1-Kernighan-Lin的1970年論文：成對交換與增益序列.md)
    * [4.2-FM 演算法：gain bucket 資料結構與 O(n) 單次掃描](04.2-FM演算法：gainbucket資料結構與O(n)單次掃描.md)
    * [4.3-多層級切割：hMetis 的 coarsening-unrefinement 框架](04.3-多層級切割：hMetis的coarsening-unrefinement框架.md)
    * [4.4-切割的戰場：Multi-FPGA 模擬與 ASIC 模組化設計](04.4-切割的戰場：Multi-FPGA模擬與ASIC模組化設計.md)
    * [4.5-Slicing Tree 與模擬退火：樓板規劃的組合優化](04.5-SlicingTree與模擬退火：樓板規劃的組合優化.md)
    * [4.6-B*-Tree 與非切片結構：Wong-Liu 框架的演進](04.6-B星Tree與非切片結構：Wong-Liu框架的演進.md)

* 第5章-擺放演算法：連續的 ASIC 與離散的 FPGA
    * [5.1-二次線長最小化：Quadratic Placement 的譜方法起源](05.1-二次線長最小化：QuadraticPlacement的譜方法起源.md)
    * [5.2-GORDIAN 與 Force-Directed：把電路當彈簧網](05.2-GORDIAN與Force-Directed：把電路當彈簧網.md)
    * [5.3-ePlace 與 RePlAce：靜電力類比的密度懲罰函數](05.3-ePlace與RePlAce：靜電力類比的密度懲罰函數.md)
    * [5.4-VPR 的模擬退火：FPGA 擺放三十年不敗的溫度排程](05.4-VPR的模擬退火：FPGA擺放三十年不敗的溫度排程.md)
    * [5.5-Legalization：從連續座標到站位與晶格的對齊](05.5-Legalization：從連續座標到站位與晶格的對齊.md)
    * [5.6-腳位指派與電源網：擺放之後的兩個小問題](05.6-腳位指派與電源網：擺放之後的兩個小問題.md)

* 第6章-時序分析：納秒的會計學
    * [6.1-Elmore 延遲與 RC 樹：一個 1948 年模型的長壽](06.1-Elmore延遲與RC樹：一個1948年模型的長壽.md)
    * [6.2-DAG 上的最長路徑：拓撲排序與 STA 的計算框架](06.2-DAG上的最長路徑：拓撲排序與STA的計算框架.md)
    * [6.3-時序收斂之戰：CPPR、OCV 與製程變異](06.3-時序收斂之戰：CPPR、OCV與製程變異.md)
    * [6.4-統計靜態時序分析 SSTA：把機率引進時序世界](06.4-統計靜態時序分析SSTA：把機率引進時序世界.md)

* 第7章-繞線演算法：迷宮、協商與 Rip-up
    * [7.1-Lee 演算法與迷宮搜尋：租用 AT&T 機器算一條線的年代](07.1-Lee演算法與迷宮搜尋：租用AT&T機器算一條線的年代.md)
    * [7.2-Soukup 與 A*：讓迷宮搜尋跑得夠快](07.2-Soukup與A星：讓迷宮搜尋跑得夠快.md)
    * [7.3-全域繞線：Steiner 樹與 Pattern/ Rip-up 的分工](07.3-全域繞線：Steiner樹與Pattern-Ripup的分工.md)
    * [7.4-PathFinder 協商繞線：FPGA 世代共享的擁塞哲學](07.4-PathFinder協商繞線：FPGA世代共享的擁塞哲學.md)
    * [7.5-ASIC 詳細繞線：Track Assignment 與 DRC 約束下的網格迷宮](07.5-ASIC詳細繞線：TrackAssignment與DRC約束下的網格迷宮.md)
    * [7.6-FPGA 的繞線資源圖：Switch Box、Connection Box 與 RRG 遍歷](07.6-FPGA的繞線資源圖：SwitchBox、ConnectionBox與RRG遍歷.md)

* 第8章-驗證與簽核：在 tape-out 之前
    * [8.1-DRC 與 LVS：掃描線演算法與幾何計算的較量](08.1-DRC與LVS：掃描線演算法與幾何計算的較量.md)
    * [8.2-寄生參數萃取：從邊界元素法到 Pattern-based 快速模型](08.2-寄生參數萃取：從邊界元素法到Pattern-based快速模型.md)
    * [8.3-等價性檢查 LEC：BDD、SAT 與 cut-point 的商業化](08.3-等價性檢查LEC：BDD、SAT與cut-point的商業化.md)
    * [8.4-OPC 與 ILT：當微影的光波長追不上線寬](08.4-OPC與ILT：當微影的光波長追不上線寬.md)

* 第9章-產業、制度與新戰場：EDA 的下一步
    * [9.1-EDA 產業的寡占史：三十年購併與三巨頭的形成](09.1-EDA產業的寡占史：三十年購併與三巨頭的形成.md)
    * [9.2-開源 EDA 的崛起：從 VTR、ABC 到 OpenROAD 與 RISC-V 生態](09.2-開源EDA的崛起：從VTR、ABC到OpenROAD與RISC-V生態.md)
    * [9.3-機器學習進入 EDA：Google 的 RL 擺放論戰與 GNN 預測](09.3-機器學習進入EDA：Google的RL擺放論戰與GNN預測.md)
    * [9.4-Chiplet 與 3D-IC：切割、熱傳導與堆疊擺放的新問題](09.4-Chiplet與3D-IC：切割、熱傳導與堆疊擺放的新問題.md)

* 附錄
    * [A.1-常用開源 EDA 框架與工具索引](A.1-常用開源EDA框架與工具索引.md)
    * [A.2-經典 Benchmark 集錦：ISCAS、MCNC、ISPD 的身世](A.2-經典Benchmark集錦：ISCAS、MCNC、ISPD的身世.md)
    * [A.3-ASIC 與 FPGA 物理設計演算法對照矩陣](A.3-ASIC與FPGA物理設計演算法對照矩陣.md)
