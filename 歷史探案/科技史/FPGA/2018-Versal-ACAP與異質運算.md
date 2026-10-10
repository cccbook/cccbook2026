# 2018-Versal-ACAP與異質運算

## 案件摘要

2018 年 10 月，Xilinx 發表 Versal ACAP（Adaptive Compute Acceleration Platform），採台積電 7nm 製程，2019 年出貨。它首次把 AI Engine（VLIW/SIMD 陣列）、NoC 網路單晶片、ARM 硬核與可程式邏輯融合在同一顆晶片上，宣稱 FPGA 的演化終點不是「更大的 FPGA」，而是「自適應運算平台」。這是可程式邏輯史上最大的一次架構轉型。

## 前因 -- 為什麼會會有這個案子

2010 年代後期，FPGA 面臨三面夾擊。第一是 **GPU 的威脅**：深度學習爆發後，NVIDIA 的 GPU 憑藉數萬個核心與成熟的 CUDA 生態，在資料中心 AI 訓練與推論上大放異彩；FPGA 雖然可重組態，但傳統 LUT/BRAM 架構對密集矩陣運算的能效不如 GPU 的專用 MAC 陣列。第二是 **ASIC 的威脅**：Google TPU、各種 NPU 證明「領域專用晶片」在單一工作負載上能效極高，只是缺乏彈性。第三是 **市場的呼喚**：5G、自駕車、資料中心加速需要「夠快但夠彈性」的晶片——比 ASIC 彈性、比 GPU 能效高、比 CPU 快。

Xilinx 內部的答案是：FPGA 的 LUT 織布（fabric）架構在 1985 年問世後，本質上是為「任意布林邏輯」設計的，而不是為「密集的數據流計算」設計的。若要應付 AI 時代，就必須在 FPGA 之外加一塊「為資料流而生」的硬體。這就是 AI Engine（AIE）的由來。

與此同時，另一個困境是 **架構瓶頸**：Zynq 的經驗顯示，當晶片上有處理器（PS）與可程式邏輯（PL）兩個域，它們之間的 AXI 互連會成為瓶頸——資料要從 DDR → PS → PL，每一步都有延遲與頻寬損耗。若再加 AI Engine 成為第三個域，傳統匯流排式互連根本無法承載。這是 NoC（Network-on-Chip）被引入的動機。

## 線索與推理 -- 數學式、程式、理論（本體，最詳細）

### 線索一：AI Engine 架構——VLIW + SIMD MAC 陣列

Versal 的 AI Engine 是一個二維陣列，每個 tile 包含：

- 一個 **VLIW SIMD 向量處理器**：Very Long Instruction Word（超長指令字），每條指令 512-bit，可同時發射多個操作。
- 一個 **SIMD MAC 陣列**：8 個 128-bit lanes，可做 8×INT16、16×INT8 或 4×FP32 的乘加。
- 32 KB 的本地記憶體（data memory），4 KB 的程式記憶體。
- 一個 DMA 引擎與 AXI-Stream 介面，連接相鄰 tile。

每個 tile 的計算能力約為每週期 128 MAC（INT8 模式），749 個 tile 的 VC1902 總計算力約為：

$$749 \text{ tiles} \times 128 \text{ MAC/cycle} \times 2 \text{ ops/MAC} \times 1.6\text{ GHz} \approx 307\text{ TOPS (INT8)}$$

這個能效的關鍵在於「資料流架構」：資料從一個 tile 的 DMA 流入，計算後直接流入下一個 tile，不經過中央記憶體。這與 GPU 的「共用記憶體 + 大量執行緒」架構完全不同，也與 FPGA 的「LUT 織布」架構不同。

### 線索二：矩陣乘法的 systolic array 實作

AI 加速的核心運算是矩陣乘法：

$$C_{ij} = \sum_{k=1}^{N} A_{ik} B_{kj}$$

傳統 CPU/GPU 的做法是「抓資料 → 算 → 存回」，每次乘加都要碰記憶體，記憶體頻寬是瓶頸。**Systolic array（脈動陣列）** 的做法則是讓資料像血液一樣在 PE（Processing Element）陣列中流動，每個 PE 只做一次乘加，資料一進一出，記憶體只在邊界被讀寫一次。

一個 $4 \times 4$ systolic array 計算 $C = A \times B$（$N=4$）：

```
        B[0][*]   B[1][*]   B[2][*]   B[3][*]     ← B 橫向流入
         ↓         ↓         ↓         ↓
A[*][0]→ PE(0,0)  PE(0,1)  PE(0,2)  PE(0,3)  → C[0][*] 沿邊界流出
A[*][1]→ PE(1,0)  PE(1,1)  PE(1,2)  PE(1,3)  → C[1][*]
A[*][2]→ PE(2,0)  PE(2,1)  PE(2,2)  PE(2,3)  → C[2][*]
A[*][3]→ PE(3,0)  PE(3,1)  PE(3,2)  PE(3,3)  → C[3][*]
```

每個 PE 的行為是：

$$C_{ij}^{(k)} = C_{ij}^{(k-1)} + a_{ik} \cdot b_{kj}, \quad C_{ij}^{(0)} = 0$$

總週期數分析：對 $N \times N$ systolic array 計算 $N \times N$ 矩陣乘法，需要 $3N - 2$ 個週期（$N$ 個週期填入 + $N-1$ 個週期排空 + $N-1$ 個週期流水線啟動）。吞吐量為每週期 $N^2$ 個 MAC，且記憶體頻寬需求只有 $O(N)$（邊界），而非 $O(N^2)$（每個 MAC 讀寫）。這就是 systolic array 的能效優勢：

$$\text{Arithmetic Intensity} = \frac{N^2 \text{ MACs/cycle}}{O(N) \text{ words/cycle}} = O(N) \text{ MACs/word}$$

AI Engine 的每個 tile 本質上是一個小型 systolic array，tile 之間用 AXI-Stream 串接，形成更大的「虛擬 systolic array」。Xilinx 的 Vitis AI 工具鏈會自動把神經網路層映射到 tile 陣列上，實現資料流。

### 線索三：NoC——封包交換 vs 總線的對比

Versal 的第二個革命是引入 **NoC（Network-on-Chip）**：在晶片上用「封包交換網路」取代傳統的 AXI 匯流排樹。傳統 AXI 互連是樹狀拓撲，多個 master 競爭同一條匯流排時，頻寬被瓜分，延遲不可預測。NoC 則像乙太網路：每個 master 有專用入口，資料被打成封包（packet），經過交換節點（switch）路由到目的地。

| 面向 | AXI 匯流排（樹狀） | NoC（網狀） |
|------|------|------|
| 拓撲 | 樹 | 2D mesh / 網狀 |
| 頻寬 | 共享，競爭瓜分 | 每路徑專用，可預測 |
| 延遲 | 負載相依，不可預測 | 可預留（QoS），近似確定性 |
| 擴展性 | master 多時瓶頸嚴重 | 可線性擴展 |
| QoS | 無 | 有（頻寬/延遲預留） |
| 適用 | 少量 master | 異質多域（PS + PL + AIE + DDR） |

NoC 的數學模型：若晶片上有 $M$ 個 master、$S$ 個 slave，匯流排的總頻寬 $B$ 被均分為 $B/M$；NoC 中每條路徑可預留頻寬 $b_i$，只要 $\sum_i b_i \leq B_{\text{NOC}}$（實際上由 mesh 的 bisection bandwidth 限制）即可同時滿足。Bisection bandwidth 是關鍵指標：把 mesh 對半切開，切面上的總頻寬決定「左半與右半之間」的最大資料交換速率。

Versal 的 NoC 更進一步提供「虛擬通道」與「QoS 預留」：設計者可以用工具聲明「這條路徑需要 X GB/s」，工具會在 NoC 上為它保留頻寬，使延遲近似確定性。這對 5G beamforming、即時視訊等應用至關重要。

### 線索四：ACAP vs FPGA vs GPU vs ASIC 的四者對比

| 面向 | ACAP（Versal） | 傳統 FPGA | GPU | ASIC |
|------|------|------|------|------|
| 計算範式 | VLIW/SIMD 資料流 + 可重組態邏輯 | LUT/FF 可重組態 | SIMT 大量執行緒 | 固定電路 |
| 峰值算力（INT8） | 高（~300+ TOPS） | 中 | 極高（數百 TOPS） | 極高 |
| 能效 | 高（資料流架構） | 中 | 中高 | 最高 |
| 彈性 | 高（三種域可重組態） | 最高 | 中（需重寫 kernel） | 無 |
| 開發模型 | C/C++ (AIE) + RTL | HDL/HLS | CUDA/OpenCL | 全客製流程 |
| 開發週期 | 短-中 | 中 | 短 | 極長（1–2 年） |
| 單位成本 | 高 | 高 | 中 | 大量時最低 |
| 適用 | AI 推論、5G、資料中心加速 | 原型、低量、特殊介面 | AI 訓練/推論、HPC | 大量、單一功能 |
| NRE 成本 | 無（可重組態） | 無 | 無 | 數千萬美元 |

推理的關鍵：ACAP 不是「更好的 FPGA」，而是「新的計算類別」。它的定位是「在 GPU 與 ASIC 之間的彈性高能效區間」——用 AIE 吃下資料流運算、用 PL 吃下任意介面與膠合邏輯、用 NoC 保證即時性、用 ARM 跑控制與作業系統。這是「異質單晶片」的終極形態。

### 線索五：異質運算的調度理論

異質系統的調度問題：給定一個工作負載 DAG（有向無環圖）$G = (V, E)$，每個節點 $v \in V$ 是一個任務，每種處理器類型 $p \in P$（CPU、AIE、PL、GPU）有各自的執行時間 $t(v, p)$，目標是最小化 makespan（總完成時間）。這是 NP-hard 的排程問題（HEFT、list scheduling 等啟發式是常用解法）。

HEFT（Heterogeneous Earliest Finish Time）的貪心策略：

$$\text{rank}_u(v) = \overline{w}(v) + \max_{s \in \text{succ}(v)} \left( c(v, s) + \text{rank}_u(s) \right)$$

其中 $\overline{w}(v)$ 是任務 $v$ 在各處理器上的平均執行時間，$c(v,s)$ 是通訊成本。任務按 rank 降序排列，依次分配到「最早完成時間（EFT）」最小的處理器上。

Versal 的 Vitis 工具鏈把這個調度問題交給工程師聲明 + 工具解決：工程師用 C++ 標記 kernel，工具分析資料依賴，自動把資料流 kernel 放到 AIE、控制流放到 ARM、介面邏輯放到 PL，並用 NoC 連接。這是「硬體異質性 + 軟體聲明式開發」的新範式。

## 結案 -- 後果與影響

Versal ACAP 於 2019 年底出貨（VC1902），標誌 FPGA 產業正式跨入「自適應運算」時代。2021 年推出的 Versal AI Core、Versal Premium 系列持續擴充，AIE 的規模與 NoC 的頻寬都不斷提升。競爭對手 Intel/Altera 也在 Agilex 中引入類似的異質架構（雖然沒有 AIE 等價物，直到後續才補上）。

更深遠的影響是「開發模型」的轉變：傳統 FPGA 工程師寫 HDL，而 Versal 的目標用戶是「用 C++ 寫 AI 應用的軟體工程師」。Vitis AI、Vitis AIE 工具鏈把硬體細節抽象掉，這是 Xilinx 從「賣晶片給硬體工程師」轉向「賣平台給軟體工程師」的策略宣示，也為日後 AMD 收購後的 AI 戰略鋪路。

影響條列：

- **AI Engine 成為新類別**：VLIW/SIMD 資料流陣列成為 Xilinx/AMD 後續所有高階產品的標配。
- **NoC 成為大型 FPGA 標配**：解決多域互連瓶頸，被 Versal Premium、Agilex 等繼承。
- **7nm 先進製程進入 FPGA**：打破 FPGA 停留在 16nm/14nm 的格局。
- **開發模型轉向 C++**：Vitis 統一軟體/硬體開發，降低入門門檻。
- **「自適應運算」行銷類別誕生**：Xilinx 用此定位區隔 FPGA 與 GPU/ASIC。

## 關鍵人物與文獻

- **Victor Peng**：時任 Xilinx CEO，Versal ACAP 的主導者與「自適應運算」概念的推手（後成為 AMD 執行副總裁）。
- **Ivo Bolsens**：Xilinx CTO，ACAP 架構與 Vitis 開發模型的關鍵人物。
- **Xilinx, "Versal ACAP: Architecture Manual"**（AM011）：Versal 架構官方文件。
- **Kung, H.T. & Leiserson, C.E., "Systolic Arrays (for VLSI)"**（1978）：systolic array 的原始論文。
- **Topcuoglu, H., Hariri, S., Wu, M.-Y., "Performance-Effective and Low-Complexity Task Scheduling for Heterogeneous Computing"**（IEEE TPDS 2002）：HEFT 排程演算法。
- **Dally, W.J. & Towles, B., "Route Packets, Not Wires: On-Chip Interconnection Networks"**（DAC 2001）：NoC 的奠基論文。
