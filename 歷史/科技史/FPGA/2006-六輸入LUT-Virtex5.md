# 2006-六輸入LUT-Virtex5

## 案件摘要
2006 年，Xilinx 在 65nm 製程的 Virtex-5 上首度將 LUT 從 4 輸入改為 6 輸入，打破延續十餘年的 4LUT 傳統。本案偵破 LUT 尺寸背後的面積-延遲辯論：學術界早有推論，業界為何等到 2006 年才動手？

## 前因 -- 為什麼會會有這個案子
從 1990 年代初的 XC4000 系列開始，Xilinx 的 FPGA 一直採用 4 輸入查找表（4-LUT）作為邏輯基本單元。Altera 陣營雖然嘗試過較粗粒度的架構（如 FLEX 的 4LUT + 產品項結構），但 4LUT 幾乎成為 FPGA 的「標準元件」。這個傳統的背後，是 1990 年代學術界一系列研究的結論：4 輸入是在「面積」與「延遲」之間的最佳平衡點。

但到了 2000 年代中期，情勢改變了。製程從 150nm 推進到 90nm、65nm，繞線延遲（而非電晶體開關延遲）成為主導因素；同時，設計的複雜度上升，使得 FPGA 內部互連的延遲佔比越來越高。4LUT 的優勢正在消失：一個需要 3 個 4LUT 串接的函數，若改用 6LUT 可能只要 1 個，電路深度從 3 降到 1，繞線次數也從 2 次降到 0 次。

Xilinx 面臨的困境是：改變 LUT 尺寸意味著架構的重大變革——工具鏈、IP、用戶的設計習慣都要調整。這不是一個可以輕易決定的案子。Xilinx 需要嚴謹的證據來證明 6LUT 在 65nm 製程下確實優於 4LUT，同時還要解決 6LUT 面積過大的問題。Virtex-5 就是這場「LUT 尺寸辯論」的最終結案陳詞。

## 線索與推理 -- 數學式、程式、理論（本體，最詳細）

### LUT 的本質：$2^n$ bits 的指數代價

一個 $n$ 輸入的 LUT 本質上是一個 $2^n \times 1$ 的 SRAM，可以實作任何 $n$ 輸入的布林函數。其面積代價是：

$$
A_{\text{LUT}}(n) = k \cdot 2^n
$$

其中 $k$ 為每個儲存位的等效面積（含 SRAM cell、位址解碼器、多工器等）。$2^n$ 的指數成長意味著：從 4LUT 到 5LUT，面積翻倍；從 4LUT 到 6LUT，面積變 4 倍。

但延遲的改善卻是線性的。一個 $n$ 輸入函數用 $k$-LUT 實作時，所需的 LUT 數量級為：

$$
N_{\text{LUT}}(n, k) \approx \frac{n}{k} \cdot C_{\text{logic}}
$$

而電路深度（延遲的關鍵）為：

$$
D(n, k) = \left\lceil \log_k n \right\rceil \cdot (t_{\text{LUT}} + t_{\text{wire}})
$$

偵破重點：$D(n,k)$ 對 $k$ 是對數下降，而非線性。這意味著從 4LUT 到 6LUT，深度從 $\lceil \log_4 n \rceil$ 降到 $\lceil \log_6 n \rceil$，改善幅度有限；但面積卻是 4 倍。這是學術界當年選擇 4LUT 的根本理由。

### 面積-延遲乘積的分析表

以實作一個 8 輸入函數為例，比較 4LUT、5LUT、6LUT：

| LUT 尺寸 | 單一 LUT 面積（相對） | 實作 8 輸入函數所需 LUT 數 | 電路深度 | 繞線次數 | 總面積（相對） | 面積-延遲乘積 |
|---------|---------------------|------------------------|---------|---------|-------------|-------------|
| 4LUT | 1 | 4（兩層：2+2 → 2） | 2 | 1 | 4 | 8 |
| 5LUT | 2 | 2（一層：2 → 1） | 2 | 0 | 4 | 8 |
| 6LUT | 4 | 2（一層：2 → 1） | 2 | 0 | 8 | 8 |

此表顯示：對 8 輸入函數，6LUT 並無優勢。但真正的設計不是單一函數，而是「邏輯塊內部的函數組合」。實際的綜合結果（Betz & Rose 的 VPR 研究）顯示，對真實電路（MCNC benchmark），深度改善是顯著的：

| Benchmark 類型 | 4LUT 平均深度 | 6LUT 平均深度 | 深度改善 | 面積變化 |
|--------------|-------------|-------------|---------|---------|
| 算術邏輯（ALU 類） | ~8 | ~5 | ~35% | +15–25% |
| 隨機邏輯（控制類） | ~10 | ~6 | ~40% | +10–20% |
| DSP 資料路徑 | ~6 | ~4 | ~30% | +20–30% |

### Betz & Rose 的 VPR 研究：最優 LUT 大小的學術推導

 Vaughn Betz 與 Jonathan Rose 在 1997–1999 年間開發了 VPR（Versatile Place and Route）工具，用於系統性研究 FPGA 架構參數（LUT 大小 $k$、邏輯塊內 LUT 數量 $N$、繞線資源分佈）。這是本案最關鍵的學術證據。

VPR 的研究方法是：對一組真實電路，掃描不同的 $k$ 與 $N$，量測「最小可實作面積」與「最小延遲」。其核心結論（Betz & Rose, FPGA'97 / TCP'98 / IEEE TCAD 1999）：

1. **最小面積的 $k$ 值**：$k = 4$ 至 $k = 5$ 之間，$k=4$ 略優。原因：$2^n$ 的指數成長使 $k \geq 6$ 時面積急速膨脹。
2. **最小延遲的 $k$ 值**：$k = 5$ 至 $k = 7$。原因：較大的 $k$ 減少電路深度與繞線次數。
3. **折衷點**：若以面積-延遲乘積（ADP, Area-Delay Product）為指標，$k = 5$ 至 $k = 6$ 最優。

$$
\text{ADP}(k) = A(k) \cdot D(k)
$$

Betz 的論文中給出：在 1990 年代的製程與繞線模型下，ADP 最優點在 $k \approx 4\text{–}5$。但到了 65nm 製程，繞線延遲 $t_{\text{wire}}$ 相對 $t_{\text{LUT}}$ 的比例上升，使 ADP 最優點向 $k = 6$ 移動。偵破重點：**LUT 的最優尺寸不是常數，而是隨製程與繞線架構演進的函數**。

$$
k_{\text{opt}}(\rho) = f\left( \frac{t_{\text{wire}}}{t_{\text{LUT}}}, \frac{A_{\text{wire}}}{A_{\text{logic}}} \right), \quad \rho = \frac{t_{\text{wire}}}{t_{\text{LUT}}}
$$

當 $\rho$ 上升（繞線相對變慢），$k_{\text{opt}}$ 上升。這是 Xilinx 在 2006 年才改用 6LUT 的理論依據：不是 Betz & Rose 錯了，而是 2006 年的製程條件改變了最優點。

### 6LUT 可分裂成兩個 5LUT：面積問題的解法

6LUT 的面積問題（$2^6 = 64$ bits）由一個精巧的電路技巧解決：**6LUT 可分裂成兩個 5LUT 共用 5 個輸入**。

架構上，一個 Virtex-5 的 6LUT 由兩個 5LUT（各 32 bits）組成，共用 5 個輸入位址（A1–A5），第 6 個輸入（A6）作為 2:1 多工器的選擇訊號：

$$
F_6(A_1, \ldots, A_6) = \overline{A_6} \cdot F_{5a}(A_1, \ldots, A_5) + A_6 \cdot F_{5b}(A_1, \ldots, A_5)
$$

當 A6 接地或固定時，電路退回兩個獨立的 5LUT。這個「可分裂」架構帶來：

| 模式 | 可實作函數 | 等效面積利用率 |
|------|-----------|-------------|
| 6LUT 模式 | 一個 6 輸入函數 | 100%（64 bits 全用） |
| 5LUT × 2 模式 | 兩個 5 輸入函數（共用 5 個輸入） | 100%（64 bits 全用，兩個函數各 32 bits） |

偵破重點：這個設計解決了「6LUT 面積大，但很多電路只用得到 5LUT」的問題。Virtex-5 的每個邏輯片（Slice）含 4 個 6LUT，可配置為 4 個 6LUT 或 8 個 5LUT，使工具（ISE 的綜合器）能依電路特性動態選擇粒度。這是「架構提供彈性、工具自動選擇」的設計範式。

### FPGA 邏輯塊粒度研究的經典結論

Betz & Rose 的研究還回答了另一個問題：邏輯塊（Logic Block）內應該放幾個 LUT？其結論：

| 邏輯塊內 LUT 數 $N$ | 面積效率 | 延遲效率 | 結論 |
|-------------------|---------|---------|------|
| 1 | 最差 | 最差 | 太細，繞線開銷大 |
| 2–4 | 好 | 好 | 最優區間 |
| 6–8 | 略差 | 略好 | 面積開銷開始超過延遲收益 |
| > 10 | 差 | 差 | 粒度過粗，利用率下降 |

Virtex-5 採用 $N = 4$（每 Slice 4 個 6LUT），兩個 Slice 組成一個 CLB。這與 VPR 研究的結論高度一致。

Virtex-5 的關鍵規格：

| 型號 | LUT 數 | 觸發器數 | BlockRAM (Kb) | DSP48E | 最大 I/O | 製程 |
|------|-------|---------|-------------|--------|---------|------|
| XC5VLX30 | 19,200 | 19,200 | 864 | 32 | 400 | 65nm |
| XC5VLX50 | 28,800 | 28,800 | 1,296 | 48 | 560 | 65nm |
| XC5VLX110 | 69,120 | 69,120 | 3,168 | 64 | 800 | 65nm |
| XC5VLX220 | 138,240 | 138,240 | 6,336 | 128 | 960 | 65nm |
| XC5VLX330 | 207,360 | 207,360 | 9,504 | 192 | 1,200 | 65nm |

### 為什麼 Altera 沒有先動？

Altera 的策略不同：其 Stratix 系列採用「ALM（Adaptive Logic Module）」架構——一個 ALM 包含兩個可變的 LUT（可配置為一個 6LUT、兩個 5LUT、或 8 個 3LUT 組合），與 Virtex-5 的「可分裂 6LUT」異曲同工。偵破重點：兩大陣營在 2006 年前後不約而同走向「可分裂、可變粒度」的架構，這是 VPR 學術結論的產業化收斂——LUT 尺寸不再是單一常數，而是一組可配置的選項。

## 結案 -- 後果與影響
Virtex-5 的 6LUT 架構成為日後所有 Xilinx 高階 FPGA 的標準（Virtex-6、7 系列、UltraScale 系列皆沿用）。本案的結案陳詞是：LUT 尺寸的最優值不是靜態的，而是「製程 → 繞線延遲 → 架構」的函數；學術界的 VPR 研究提供了方法論，產業界則以可分裂架構解決了面積問題。從此 FPGA 架構研究進入「參數化、可量化」的時代。

- 架構標準化：6LUT（可分裂）成為 Xilinx 2006 年後所有高階 FPGA 的標準
- 效能提升：電路深度平均降低 30–40%，使 Virtex-5 的最高頻率達到 550MHz（上一代約 500MHz）
- 面積效率：可分裂架構使 5LUT 電路的面積開銷可控，解決了 6LUT 的理論面積劣勢
- 研究方法學：VPR 成為 FPGA 架構研究的標準工具，日後所有架構論文都以 VPR 為基準
- 競爭收斂：Altera 的 ALM 與 Xilinx 的可分裂 6LUT 趨同，顯示架構空間的最優解是唯一的
- UltraScale 的延續：16nm UltraScale+ 採用「可分裂 6LUT + CARRY8」架構，證明本案結論的長期有效性

## 關鍵人物與文獻
- **Vaughn Betz**：VPR 工具與 FPGA 架構研究的先驅，後成為 Altera（後 Intel）FPGA 架構總監
- **Jonathan Rose**：多倫多大學教授，VPR 研究的合作者，FPGA 架構學術界的權威
- **V. Betz and J. Rose, "Directional Bias and Non-Uniformity in FPGA Global Routing Architectures" (ICCAD, 1996)**
- **V. Betz, J. Rose, A. Marquardt, "Architecture and CAD for Deep-Submicron FPGAs" (Kluwer, 1999)**：VPR 研究的集大成著作
- **Xilinx, "Virtex-5 FPGA User Guide (UG190)"**：6LUT 可分裂架構的官方文獻
- **Xilinx, "Virtex-5 Data Sheet (DS202)"**：規格的原始依據
- **J. Luu, I. Kuon, et al., "VPR 5.0: FPGA CAD and Architecture Exploration Tools with Unified Packing, Placement and Routing" (ICCAD, 2009)**：VPR 的後續發展
- **I. Kuon and J. Rose, "Measuring the Gap Between FPGAs and ASICs" (IEEE TCAD, 2007)**：面積-延遲折衷的量化依據
