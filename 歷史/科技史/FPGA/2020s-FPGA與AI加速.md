# 2020s-FPGA與AI加速

## 案件摘要

2020 年代，FPGA 在 AI 推論、邊緣運算、5G/Open RAN 無線電與金融加速中找到自己的戰場：不是與 GPU 拼訓練，而是以「低延遲、高能效、可重組態資料流」吃下 GPU 不擅長的區間。INT8/INT4 量化、稀疏化與高階合成（HLS）三項技術，讓 FPGA 成為邊緣 AI 與即時推論的重要平台。

## 前因 -- 為什麼會會有這個案子

2012 年 AlexNet 引爆深度學習後，AI 運算的需求曲線近乎垂直上升。NVIDIA 的 GPU 憑藉數萬核心與 CUDA 生態佔據了訓練市場，FPGA 陣營一度陷入「FPGA 對 AI 還有什麼用」的質疑。但推理（inference）市場與訓練市場的需求截然不同：推論要求**低且確定的延遲**（自駕車的感知週期、5G 的 slot 時限、高頻交易的微秒級）、**高能效**（邊緣設備的散熱與功耗限制）、以及**模型快速迭代**（演算法每季更新）。

FPGA 的傳統架構（LUT + BRAM + DSP）在這三個需求上有天然優勢：資料流架構不需要指令週期，延遲可精確預測；每個運算的能耗遠低於 GPU 的指令提取-解碼-執行流水線；且可以為每個模型重新織出專用電路。但困境同樣明顯：HDL 開發門檻極高，軟體背景的 AI 工程師根本不會寫 Verilog；且 FP32 運算在 FPGA 上的代價高昂。

案件的解題線索有三：一是**量化**（把 FP32 模型壓成 INT8/INT4，正好落在 FPGA DSP 單元的甜蜜點）；二是**資料流架構**（weight-stationary 的空間計算）；三是**高階合成**（HLS 讓 C++ 工程師也能寫 FPGA）。三者合流，讓 FPGA 在 2020 年代重新確立了 AI 推論的定位。

## 線索與推理 -- 數學式、程式、理論（本體，最詳細）

### 線索一：神經網路推理的卷積數學

卷積神經網路（CNN）的核心運算是卷積：

$$y[o][i][j] = \sum_{c}\sum_{m}\sum_{n} W[o][c][m][n] \cdot x[c][i+m][j+n]$$

其中 $x$ 是輸入特徵圖、$W$ 是卷積核、$y$ 是輸出。FPGA 上有兩種主要實作策略：

**策略 A：im2col + GEMM（矩陣乘法化）**。把卷積「攤平」成矩陣乘法：把每個感受野（receptive field）展開成一行，得到矩陣 $X'$，則卷積變成 $Y = W' \times X'$ 的矩陣乘法，可以復用高效 GEMM 引擎。GPU/TPU 都採用此法。缺點是 im2col 會把資料膨脹 $K \times K$ 倍（$K$ 為核大小，如 $3\times3$ 膨脹 9 倍），記憶體頻寬與快取壓力大。

**策略 B：空間架構（spatial architecture，直接資料流）**。不攤平，直接在 FPGA 上織出一個二維 PE 陣列，每個 PE 負責一個輸出通道的部分和，資料在 PE 間流動。採用 **weight-stationary（權重固定）** 資料流：權重 $W[o][c][m][n]$ 預先載入 PE 的暫存器並「固定不動」，輸入特徵圖流過 PE，部分和在 PE 內累加。每次載入權重可重用於整個特徵圖，權重的記憶體存取次數從 $O(H \times W \times C)$ 降到 $O(C \times K \times K)$。

兩者對比：

| 面向 | im2col + GEMM | 空間架構（weight-stationary） |
|------|------|------|
| 資料膨脹 | $K^2$ 倍 | 無 |
| 權重重用 | 快取依賴 | PE 內固定，最優 |
| 硬體複雜度 | 低（一個 GEMM 引擎） | 高（客製 PE 陣列） |
| 彈性（多種核大小） | 高 | 需重新織布 |
| FPGA 適配 | 中 | 高（FPGA 的空間性是優勢） |

FPGA 的本質優勢在此顯現：GPU 是「時間架構」（一組執行單元分時執行所有層），FPGA 可以織出「空間架構」（每層一塊專用電路，層間用 FIFO 直連，層與層並行執行）。這種 **layer pipelining** 使總延遲為：

$$T_{\text{total}} = \sum_{l} T_l \quad \text{(GPU，序列)} \qquad T_{\text{total}} \approx \max_l T_l + T_{\text{ramp}} \quad \text{(FPGA，流水線)}$$

對即時推論（如 YOLO 類偵測網路），FPGA 的流水線延遲可比 GPU 的批次處理延遲低一個數量級。

### 線索二：INT8 量化的定點數理論

量化的數學：把 FP32 張量 $x \in [x_{\min}, x_{\max}]$ 映射到 $n$-bit 整數。**對稱量化**（symmetric，常用於權重）：

$$Q(x) = \mathrm{round}\left(\frac{x}{s}\right), \quad s = \frac{\max|x|}{2^{n-1}-1}$$

**非對稱量化**（asymmetric，常用於激活值，因激活值分布常偏斜）：

$$Q(x) = \mathrm{round}\left(\frac{x}{s}\right) + z, \quad s = \frac{x_{\max} - x_{\min}}{2^n - 1}, \quad z = -\mathrm{round}\left(\frac{x_{\min}}{s}\right)$$

其中 $s$ 是 scale（步長）、$z$ 是 zero-point（零點）。反量化為 $\hat{x} = s \cdot (Q(x) - z)$。

量化誤差分析：round 操作引入的誤差在 $[-s/2, s/2]$ 內近似均勻分布，故量化雜訊的方差為：

$$\sigma_q^2 = \frac{s^2}{12}$$

訊號雜訊比（SQNR，以 dB 計）：

$$\mathrm{SQNR} \approx 6.02 \cdot n + 1.76 \text{ dB}$$

INT8（$n=8$）約 49.9 dB，INT4（$n=4$）約 25.8 dB。關鍵推理：神經網路對量化雜訊有容忍性，因為推論任務（分類、偵測）的決策邊界有一定餘裕；經驗上 INT8 量化的精度損失通常在 1% 以內（配合 calibration 校正），INT4 則需要量化感知訓練（QAT）。

量化為何對 FPGA 特別有利？因為 FPGA 的 DSP48 單元原生支援 INT8/INT16 乘法：一個 DSP48E2（UltraScale+）可做一個 $27\times18$-bit 乘法，或打包成 **2 個 INT8 乘法**（用位元操作技巧把兩個 INT8 打包進一個乘法器）。這使 INT8 模式的算力直接翻倍；某些架構甚至可做 INT4 的 4 倍打包。而 GPU 的 FP16/FP32 單元在 INT8 上的打包效率不如 FPGA 的彈性位寬。

### 線索三：FPGA vs GPU 推理延遲與能效對比

| 面向 | FPGA（空間資料流） | GPU（SIMT 批次） |
|------|------|------|
| 延遲（單張推論） | 低且確定（流水線，微秒級抖動） | 中（批次湊滿才高效，延遲抖動大） |
| 吞吐量（大批次） | 中 | 極高 |
| 能效（推論，TOPS/W） | 高（無指令開銷） | 中高 |
| 模型迭代 | 需重新合成（分鐘-小時級） | 改 kernel 即可（秒-分鐘級） |
| 開發門檻 | HLS/RTL（高，HLS 已降低） | CUDA（低，生態成熟） |
| 彈性位寬 | 完全彈性（INT4/8/16/FP16/自訂） | 固定（INT8/FP16/FP8） |
| 網路/介面整合 | 極強（可直連 5G 射頻、感測器） | 需經主機 PCIe |
| 適用 | 邊緣、即時、確定性延遲 | 資料中心大批次推論 |

推理的關鍵：FPGA 的能效優勢來自「資料流無指令開銷」。GPU 每個 MAC 運算伴隨指令提取、解碼、排程的能耗（約占總能耗的一半以上）；FPGA 的 PE 陣列中，資料在 PE 間直接流動，沒有指令。理論上，同製程下資料流架構的 MAC 能效可比指令驅動架構高 2–5 倍。

而「確定性延遲」是 GPU 難以取代的：高頻交易要求微秒級且可預測的回應（任何 tail latency 都可能造成損失）、自駕車的感知-決策週期有硬時限、5G 的 slot 是 0.125 ms 的固定週期。這些應用中「最壞情況延遲」比「平均吞吐量」更重要，而這正是空間資料流架構的天然屬性。

### 線索四：高階合成（HLS）讓軟體工程師可編程 FPGA

HLS（High-Level Synthesis）的理論：把 C/C++ 程式合成為 RTL 電路。編譯器分析程式中的資料依賴與循環結構，自動做「循環展開（unroll）」、「迴圈管線化（pipeline）」、「陣列分區（partition）」。一個簡短的 C++ HLS 推論層範例：

```cpp
#include <ap_int.h>
#include <hls_stream.h>

typedef ap_int<8>  q8_t;      // INT8 量化值
typedef ap_int<32> acc_t;     // 32-bit 累加器

// 單層 INT8 全連接：y = W·x + b，權重固定於 BRAM
void fc_layer(const q8_t x[N], const q8_t W[M][N],
              const acc_t bias[M], q8_t y[M]) {
#pragma HLS ARRAY_PARTITION variable=W cyclic factor=8 dim=2
FC_OUT:
    for (int m = 0; m < M; m++) {
#pragma HLS PIPELINE II=1        // 目標：每週期產出一個輸出
        acc_t acc = bias[m];
FC_SUM:
        for (int n = 0; n < N; n++) {
#pragma HLS UNROLL factor=8      // 8 路並行乘加 → 8 個 DSP48
            acc += (acc_t)W[m][n] * x[n];
        }
        // ReLU 後再量化回 INT8
        acc = (acc < 0) ? 0 : acc;
        y[m] = (q8_t)(acc >> SHIFT);
    }
}
```

`#pragma HLS PIPELINE II=1` 要求「每週期啟動一次迭代」（Initiation Interval = 1），HLS 編譯器會為此排程硬體；`UNROLL factor=8` 把內層循環展開 8 路，對應 8 個 DSP 的並行乘加。軟體工程師只需理解「循環 = 並行電路的機會」，不必手寫 Verilog。Vitis HLS 進一步把整個網路合成為資料流資料流電路（`#pragma HLS DATAFLOW`），層間自動插入 FIFO，實現層級流水線。

## 結案 -- 後果與影響

2020 年代，FPGA 在 AI 推論的定位確立：**邊緣即時推論 + 確定性延遲 + 網路整合**。AMD 收購 Xilinx 後，Zynq/Versal 成為邊緣 AI 的主力（Vitis AI 工具鏈支援 INT8 模型直接部署到 DPU），Alveo 系列在金融加速（交易所撮合、風控、高頻交易）站穩腳跟；5G Open RAN 中，FPGA（尤其 RFSoC）是 L1 層即時處理的事實標準。Intel/Altera 的 Agilex 也在邊緣與通訊 AI 中持續競爭。

更深遠的影響是「開發人口」的擴大：HLS 與 Vitis AI 讓軟體工程師（而非只有 RTL 工程師）能夠部署 FPGA 推論應用，FPGA 的可用工程師人口擴大了一個數量級。同時，「量化 + 資料流」的設計範式也反向影響了 ASIC 世界——NPU 的 INT8/INT4 設計與 FPGA 的實踐互相印證。

影響條列：

- **邊緣 AI 確立**：Zynq/Versal + DPU 成為工業視覺、車用、醫療邊緣推論的平台。
- **金融加速成熟**：低延遲交易系統中 FPGA 成為標配（納斯達克、CME 等交易所採用）。
- **5G/Open RAN 依賴**：L1 層的即時性使 FPGA/RFSoC 成為 5G 基站的關鍵元件。
- **量化範式普及**：INT8/INT4 推論從 FPGA 實踐擴散為全產業標準。
- **開發門檻下降**：HLS/Vitis AI 讓軟體工程師進入 FPGA 生態，擴大人口紅利。
- **與 GPU 分工明確**：訓練歸 GPU、大批次推論歸 GPU、即時/邊緣/確定性延遲歸 FPGA。

## 關鍵人物與文獻

- **Lisa Su / Victor Peng**：AMD 收購 Xilinx 後推動 Vitis AI 與邊緣 AI 戰略的關鍵人物。
- **Jacob, B., et al., "Quantization and Training of Neural Networks for Efficient Integer-Arithmetic-Only Inference"**（CVPR 2018）：INT8 量化的奠基論文（TensorFlow Lite 量化方案）。
- **Han, S., Mao, H., Dally, W.J., "Deep Compression: Compressing Deep Neural Networks with Pruning, Trained Quantization and Huffman Coding"**（ICLR 2016）：稀疏化與量化的經典。
- **Chen, Y.-H., Krishna, T., Emer, J., Sze, V., "Eyeriss: An Architecture for Energy-Efficient Dataflow for CNNs"**（2016）：weight-stationary 等資料流分類的經典分析。
- **Cong, J. et al., "High-Level Synthesis for FPGAs: From Prototyping to Deployment"**（IEEE TCAD）：HLS 理論與實踐的综述。
- **Xilinx Vitis AI 文檔**：DPU 架構與 INT8 部署流程的官方文件。
