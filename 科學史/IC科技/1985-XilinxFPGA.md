# 1985 - Xilinx FPGA：可重組態硬體的誕生

## 案件摘要
1985 年 Xilinx 共同創辦人 Ross Freeman 提出「可由使用者自行配置的 IC」—— FPGA（Field-Programmable Gate Array），並推出世界第一顆商用 FPGA XC2064。硬體從此可以像軟體一樣「改版重燒」，改寫了 ASIC 的遊戲規則。

## 前因 -- 為什麼會有這個案子
- **mask 費用問題**：客製 ASIC 需要全套光罩（mask set），1980 年代一套要數萬美元、製作週期數週；若設計有錯，全部重來（NRE = Non-Recurring Engineering cost 極高）。
- 小量多樣的應用（工業控制、通訊卡、原型驗證）根本攤不起 ASIC 的 NRE。
- 既有的可程式邏輯元件（PAL/GAL、EPROM）邏輯容量太小，且結構固定。
- Ross Freeman 在 Zilog 任職時的洞察：**若把電晶體「浪費」在可重組態的連接上，摩爾定律會讓這種浪費越來越便宜** —— 等到IC 更大更便宜，FPGA 就會贏。

## 線索與推理 -- 數學式、程式、理論

### 1. FPGA 基本架構：LUT + CLB + 路由通道
現代 FPGA 是一個二維的可重組態陣列：

$$
\text{FPGA} = \underbrace{\{\text{CLB}\}}_{\text{邏輯方塊陣列}} + \underbrace{\{\text{Switch Box / Channel}\}}_{\text{可程式路由}} + \underbrace{\{\text{IOB}\}}_{\text{可程式 I/O}}
$$

- **LUT（Look-Up Table，查找表）**：用一個小 SRAM 實作任意布林函數。
- **CLB（Configurable Logic Block）**：由數個 LUT + 正反器（FF）+ 進位鏈組成。
- **路由通道**：開關矩陣（switch box）決定訊號如何在 CLB 之間傳遞；組態存在 SRAM 中，斷電即失（SRAM-based FPGA 開機時從外部 Flash 載入 bitstream）。

### 2. LUT 的數學：實作 $f: \{0,1\}^n \to \{0,1\}$
一個 $n$ 輸入 LUT 就是儲存真值表的 $2^n$ 位元 SRAM：

$$
f(x_1,\dots,x_n) = \text{SRAM}\!\left[\sum_{i=1}^{n} x_i \cdot 2^{i-1}\right]
$$

理論上 LUT 可以實作**任何** $n$ 輸入布林函數（因為 $2^n$ 個真值表項目就是函數的完整描述）。對照之下，若用兩層 AND-OR 邏輯實作，最壞情況需要 $2^{n-1}$ 個 AND 閘（見 1986-邏輯合成.md 的 Quine–McCluskey）；LUT 以「查表」換取「無需最佳化」的通用性。

例如 4 輸入函數 $f = \Sigma m(0, 3, 5, 6)$（多數 4 取 2 以上的對稱函數）只需把 16 位元的常數 `0000 1001 0110 1000` 燒進 LUT。

### 3. 可重組態硬體的威力
$$
\text{FPGA 晶片成本} = C_{\text{晶片}} \cdot (1+\alpha), \qquad \text{ASIC 總成本} = C_{\text{晶片}} \cdot N + \text{NRE}
$$

當量產數量 $N$ 小時 FPGA 佔優勢；當 $N$ 超過損益兩平點（breakeven point，通常數萬至數十萬顆）ASIC 才划算。更關鍵的是：FPGA 可以**現場升級**（remote firmware update），瑕疵可修，產品生命週期內可疊代。

### 4. Xilinx vs Altera
- **Xilinx**（1984，Ross Freeman、Bernard Vonderschmitt、James Barnett）：首創 SRAM-based FPGA，XC2064 有 64 個 CLB、約 850 個等效閘。
- **Altera**（1983，Robert Hartmann）：以 EPROM-based CPLD（如 MAX 系列）起家，1988 年推出 SRAM-based FLEX 系列，主打高容量。
- 兩強競爭 35 年，直到 2020 年 AMD 宣布收購 Xilinx（2022 完成）、Intel 於 2015 年收購 Altera —— FPGA 成為兩大 CPU 巨頭的戰略資產。

### 5. FPGA vs ASIC 對照表

| 面向 | FPGA | ASIC |
|------|------|------|
| NRE | 極低（bitstream 可重燒） | 極高（mask set） |
| 單顆成本 | 高 | 低（量產時） |
| 上市時間 | 天～週 | 月～年 |
| 效能/功耗 | 較差（路由延遲、組態電晶體開銷） | 最佳 |
| 修改設計 | 現場重燒，即時 | 需重下 mask |
| 適用 | 原型、小量、演算法迭代、5G/推論加速 | 大量消費性/手機晶片 |

### 6. Verilog FPGA 範例

```verilog
// 可合成的 4-bit 計數器 + 七段顯示解碼（典型 FPGA 入門設計）
module counter7seg
  (input  wire       clk, rst_n,
   output wire [6:0] seg);   // {a,b,c,d,e,f,g}
  reg [3:0] cnt;
  always @(posedge clk or negedge rst_n) begin
    if (!rst_n) cnt <= 4'd0;
    else        cnt <= cnt + 1'b1;    // cnt(t+1) = (cnt(t)+1) mod 16
  end
  // 組合邏輯：合成後成為一顆 4-LUT 鏈（FPGA 上自然映射到 LUT）
  assign seg = (cnt == 4'd0) ? 7'b1111110 :
               (cnt == 4'd1) ? 7'b0110000 :
               (cnt == 4'd2) ? 7'b1101101 :
               (cnt == 4'd3) ? 7'b1111001 :
               (cnt == 4'd4) ? 7'b0110011 :
               (cnt == 4'd5) ? 7'b1011011 :
               (cnt == 4'd6) ? 7'b1011111 :
               (cnt == 4'd7) ? 7'b1110000 :
               (cnt == 4'd8) ? 7'b1111111 : 7'b1111011;
endmodule
```

## 結案 -- 後果與影響
- FPGA 讓「硬體試誤」的成本趨近於零，成為數位系統原型驗證、ASIC 前的 emulation 標準工具。
- 摩爾定律持續兌現 Freeman 的賭注：FPGA 從 850 閘成長到今日上千萬等效閘、內建硬體乘法器、ARM 硬核、SerDes 收發器的「萬能晶片」。
- 開啟「可重組態運算」（reconfigurable computing）研究領域，影響 2010 年代的 DNN 硬體加速（微軟 Catapult 用 FPGA 加速 Bing 搜尋）。
- EDA 流程也因 FPGA 而分家：FPGA 工具鏈（Xilinx Vivado、Intel Quartus）強調快速收斂（place & route），與 ASIC 合成工具互相滋養。

## 關鍵人物與文獻
- **Ross Freeman**（1947–1989）：FPGA 概念發明人，2009 年入選美國發明家名人堂（National Inventors Hall of Fame）。
- **Bernard Vonderschmitt、James Barnett**：Xilinx 共同創辦人，負責商業化。
- **Xilinx XC2064**（1985）：世界第一顆商用 FPGA。
- W. Carter et al., "A User Programmable Reconfigurable Gate Array"（Xilinx 專利 US 4,642,487，1987）。
- Jonathan Rose et al., "The VPR Place-and-Route Benchmark Suite"（FPGA 學術研究基礎）。
