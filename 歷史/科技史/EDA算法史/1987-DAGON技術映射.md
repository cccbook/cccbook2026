# 1987-DAGON技術映射

## 案件摘要
SIS 能把邏輯優化成多級網路，但最後一哩懸而未決：**怎樣把抽象的邏輯網路映射到工藝庫的實際閘**（NAND2、AOI21、MUX……）——選哪些閘、接成什麼形狀，直接決定面積、延遲、功耗。1987 年 DAC，IBM 的 Kurt Keutzer 發表 **DAGON**：把技術映射化為 **DAG 模式比對 + 樹覆蓋的動態規劃**——把邏輯 DAG 切成樹，對每棵樹用庫的模式樹做最優覆蓋（借鑑編譯器代碼生成的樹覆蓋理論，Aho-Johnson 1976）。DAGON 是技術映射的開山之作，FlowMap（FPGA 映射, 1992）、CutMap 等整族演算法皆其直系後裔，今日所有 FPGA/ASIC 合成器的映射引擎都站在它的肩膀上。

## 前因 -- 為什麼會有這個案子
- **SIS 的缺口**：多級優化後的網路是「抽象閘」（AND/OR），不是工藝庫的實際單元——「技術綁定（technology binding）」缺系統化演算法。
- **選閘是組合爆炸**：一個邏輯節點可用多種庫單元實現（NAND2 vs NOR2 vs AOI21），局部最優 ≠ 全局最優——需要全域視野的覆蓋演算法。
- **編譯器的先例**：Aho-Johnson（1976）的樹覆蓋代碼生成——表達式樹 → 機器指令，動態規劃最優覆蓋——數學模板已就緒。
- **IBM 的現場**：Keutzer 在 IBM 研究合成，需要把 SIS 式優化接到 IBM 工藝庫上——實戰缺口。

## 線索與推理 -- 數學式、程式、理論

### 核心：覆蓋（covering）的數學化
給定邏輯 DAG $N$ 與工藝庫 $L$（每個單元 = 一棵模式樹 $p$，帶面積/延遲成本）。技術映射 = 用 $L$ 的模式**覆蓋** $N$：

$$\min \sum_{p \in \text{cover}} \text{cost}(p)$$

- **NP-困難**（DAG 覆蓋）；DAGON 的戰術：**切成樹**——在多 fanout 節點處切斷，DAG 變成森林；
- **樹覆蓋 = 動態規劃最優**：對每棵樹自底向上，每個節點取「所有可行模式」的最優組合：

$$\text{cost}(v) = \min_{p \in \text{patterns matching at } v} \big(\text{cost}(p) + \sum_{\text{leaves of } p} \text{cost}(\text{leaf})\big)$$

這是 Aho-Johnson 樹覆蓋的直系移植——**跨界借力的教科書案例**：編譯器的代碼生成理論餵給了硬體合成。

### 範例：三種覆蓋的取捨
邏輯 $f = \overline{(a \cdot b) + c}$ 可映射為：
- NAND2 + NOR2 + OR2：3 閘；
- AOI21（and-or-invert）：1 閘——面積省 2/3、延遲更短；
- NAND2 + NOR2（堆疊）：2 閘但深度更深。
動態規劃在每個節點計算所有模式的最優子組合，全局選出最小成本——局部與全局的矛盾由 DP 的最優子結構化解。

### 延遲驅動的擴充
面積最優 ≠ 延遲最優。後繼者把 DP 的成本換成「抵達時間」：
- **FlowMap（1992）**：FPGA LUT 映射，以 cut 的深度為成本，DP 保證深度最優；
- **CutMap、Cut 枚舉法**（1990s）：列舉每節點的候選 cut，配延遲/面積雙目標——成為現代映射引擎的標準架構。

## 結案 -- 後果與影響
- **技術映射的母體**：DAGON 樹覆蓋 + FlowMap 深度最優 + cut 枚舉，構成今日所有映射引擎（Synopsys DC、ABC 的 SC/LUT mapping）的架構基礎。
- **跨學科借力的典範**：編譯器代碼生成（Aho-Johnson）→ EDA 技術映射——與圖著色暫存器分配（編譯器）平行的另一樁「軟體理論餵硬體」案件。
- **FPGA 映射的誕生**：FlowMap 等後繼讓 FPGA 合成可行，支撐 Xilinx/Altera 的崛起——映射演算法直接塑造了一個產業。
- **Keutzer 的續航**：Keutzer 後為 Google 研究深度學習硬體與神經架構搜索——映射的組合思維延續到 AI 晶片時代。

## 關鍵人物與文獻
- **Kurt Keutzer**：IBM→Synopsys→Berkeley，技術映射之父，後為 AI 硬體研究先驅。
- 文獻：
  - K. Keutzer, "DAGON: Technology Binding and Local Optimization by DAG Matching," *DAC* 1987, 341–347.
  - A. V. Aho, S. C. Johnson, "Optimal Code Generation for Expression Trees," *J. ACM* 23, 488 (1976)（樹覆蓋理論）。
  - J. Cong, Y. Ding, "FlowMap: An Optimal Technology Mapping Algorithm for Delay Optimization in Lookup-Table Based FPGA Designs," *ICCAD* 1992.
