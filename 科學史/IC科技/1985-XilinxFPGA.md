# 1985-XilinxFPGA

## 案件摘要（3 行內的梗概）
1985 年，Ross Freeman 在 Xilinx 公司發明了現場可程式化閘陣列（Field-Programmable Gate Array, FPGA）。這項發明解決了客製硬體高昂的 mask 費用與交期問題。它開啟了「可重組態硬體」（reconfigurable hardware）的時代。

## 前因 -- 為什麼會有這個案子
在 80 年代中期，想要製作一顆客製化的數位 IC，幾乎只有 ASIC（Application-Specific Integrated Circuit）一途。然而，ASIC 的開發有著致命的門檻：光罩（mask set）費用極為昂貴，少則數十萬美元，多則上百萬美元；此外，從設計到晶圓回來往往需要數個月的製造週期。

對於原型驗證、小批量生產、或需要頻繁修改的設計而言，這個風險太過沉重。設計師面臨一個困境：要嘛選擇昂貴又不可更改的 ASIC，要嘛退回到離散邏輯（TTL/CMOS SSI/MSI）拼裝，犧牲整合度與效能。

這個案件的動機清晰：尋找一種「軟體可程式化、硬體可執行」的中間形態——一塊出廠後仍能依照使用者需求重新配置內部連線與邏輯的晶片。

## 線索與推理 -- 數學式、程式、理論（本體，最詳細）
破案的關鍵線索，在於將「布林函數的查表實作」與「可程式化的互連網路」結合起來。FPGA 的核心思想是：用記憶體取代固定的邏輯閘，藉由改寫記憶體內容來改變電路功能。

### LUT：布林函數的查找表
FPGA 最基本的建構單元是**查找表（Look-Up Table, LUT）**。一個 $n$ 輸入的 LUT 能夠實作任何 $n$ 變數的布林函數 $f: \{0,1\}^n \to \{0,1\}$。

從數學角度來看，$n$ 個布林變數總共 $2^n$ 種輸入組合。任何布林函數都可由其真值表（truth table）完全決定。LUT 的工作原理即是：將這個真值表儲存在一塊 $2^n \times 1$ 位元的 SRAM 中，輸入位址 $x \in \{0,1\}^n$ 用來索引 SRAM，輸出即為 $f(x)$。

形式化表示如下：

$$
f(x_1, x_2, ..., x_n) = \operatorname{LUT}[\, \operatorname{addr}(x_1,...,x_n)\,], \quad \operatorname{addr} = \sum_{i=1}^{n} x_i \cdot 2^{i-1}\, (\text{or any ordering})
$$

舉例而言，一個 3 輸入 LUT（$n=3, 2^3=8$ 個記憶體單元）可以實作任意 3-輸入邏輯（如 XOR3、MUX、半加器等），只需載入對應的 8-bit 真值表即可。這正是「可重組態」（reconfigurable）的本質：**改變 SRAM 內容 = 改變電路功能**。

### CLB 與路由通道
單純的 LUT 還不足以構成完整的數位系統。Xilinx 的架構將 LUT 與其他元件封裝成**可組態邏輯區塊（Configurable Logic Block, CLB）**。典型的 CLB 至少包含：
- 一或多個 LUT
- 可程式化的正反器（Flip-Flop），用於實作時序邏輯
- 多工器（MUX）與進位鏈（carry chain），用於優化加法器等算術電路

這些 CLB 再透過**可程式化路由通道（programmable routing channels）**與開關矩陣（switch matrix）連接起來。整個 FPGA 就像一片「海洋」的邏輯單元，由一張可重寫的互連網路將其編織成所需的電路拓樸。

### 可重組態硬體（Reconfigurable Hardware）
FPGA 的革命性在於其「可重組態性」。與 ASIC 一旦下線就無法修改不同，FPGA 的組態（configuration）是儲存在外部或內部的位流（bitstream）中，載入後即可決定：
1. 每個 LUT 的真值表內容
2. CLB 內部各元件的連接方式
3. 全晶片的路由資源連線

這意味著同一顆晶片，可以在不同時間執行完全不同的硬體功能（這種特性後來衍生出動態部分重組態（Partial Reconfiguration）等技術）。理論上，硬體的行為變得如同軟體般可載入與替換。

### Verilog FPGA 範例
為了將設計實際映射到 FPGA，我們同樣使用 HDL。以下以 Verilog 實作一個簡單的 4 位元上數計數器，並在 FPGA 上實現時序邏輯：

```verilog
module counter_4bit (
  input  clk,
  input  reset_n,        // 低態有效重置
  output reg [3:0] q
);

  always @(posedge clk or negedge reset_n) begin
    if (!reset_n)
      q <= 4'b0000;
    else
      q <= q + 1'b1;
  end

endmodule
```

這段 RTL 在合成階段，會被合成工具（如 Xilinx Vivado、AMD Vitis/Vivado HLS 環境，或 Intel Quartus）映射到 FPGA 的資源：
- 加法運算 `q + 1'b1` 會利用 CLB 內的算術資源（carry chain）優化
- 暫存器 `q` 會映射到 CLB 內的正反器
- 時脈樹（clock tree）則由 FPGA 的內建時脈路由網路處理

值得注意的是，FPGA 設計流程與 ASIC 類似，但合成目標（target）從標準單元庫（standard cell library）變成了 LUT/CLB/路由資源，這也是「模擬 vs 合成」語意在實務上的體現。

### FPGA vs ASIC 對照表
本案最清晰的推理證據，莫過於兩者的取捨（trade-off）：

| 比較項目 | FPGA（Field-Programmable Gate Array） | ASIC（Application-Specific Integrated Circuit） |
|---|---|---|
| **可重組態性** | 高（出廠後可重複燒錄、多次修改） | 低（一次製造，無法修改） |
| **開發成本（NRE）** | 極低（無光罩費） | 極高（光罩費、設計驗證成本昂貴） |
| **單位成本（量產）** | 高（每顆晶片） | 低（規模經濟，量愈大愈便宜） |
| **效能（速度、功耗）** | 中～較低 | 高（客製化最佳化，較省電、較快） |
| **面積效率** | 較差（因可程式化開關佔面積） | 較佳 |
| **開發週期** | 短（天～數週即可驗證） | 長（數月～一年以上） |
| **適用場景** | 原型驗證、快速開發、小批量、可重組態系統（如軟體無線電、加密硬體更新） | 大量量產、高效能需求、成本敏感的最終產品 |

### Xilinx vs Altera
FPGA 產業早期的雙雄競爭也是本案的重要脈絡。Xilinx（由 Ross Freeman、Bernard Vonderschmitt、Jim Barnett 於 1984 年創立）率先於 1985 年推出商業化 FPGA（XC2064 被視為早期代表產品）。Altera（後被 Intel 收購）則是另一大陣營，兩者在架構、工具鏈（Vivado/Quartus）與市場定位上長期競爭，深刻影響了整個可程式化邏輯產業的走向。

## 結案 -- 後果與影響
本案以「可重組態硬體的商業化」宣告結案。Ross Freeman 的 FPGA 發明，填補了軟體與 ASIC 之間長久存在的設計鴻溝（design gap）。

其深遠影響包括：
- **加速原型與驗證**：設計師可以在實體硬體上即時驗證 RTL，大幅降低了 IC 設計的風險。
- **賦予硬體彈性**：FPGA 讓「硬體升級」成為可能（例如通訊協定更新、演算法調整），這在航太、國防、通訊等領域尤其關鍵。
- **催生新應用**：FPGA 在機器學習加速、資料中心（FPGA offload）、即時訊號處理（DSP）、網路加速等領域持續扮演重要角色。
- **拓展設計民主化**：降低了進入硬體設計的門檻，讓更多研究者與創客能夠實作客製硬體。

最終的推理結論是：FPGA 並非要取代 ASIC，而是與 ASIC 形成互補的生態系——**原型、驗證與彈性用 FPGA；量產、極限效能與成本優化用 ASIC**。這個取捨邏輯，至今仍是 IC 設計決策的核心準則。

## 關鍵人物與文獻
- **Ross Freeman**（Xilinx）：FPGA 發明者，普遍被譽為「FPGA 之父」。
- **Bernard Vonderschmitt、Jim Barnett**：Xilinx 聯合創辦人，協助將 FPGA 商業化。
- **Xilinx, Inc.**：1985 年推出早期 FPGA 產品，奠定可程式化邏輯產業基礎。
- **Altera Corporation（Intel Programmable Solutions Group）**：FPGA 產業重要競爭者。
- **Brown & Rose**，《Architecture of FPGAs and CPLDs: A Tutorial》：深入解析 FPGA 架構的經典文獻。
- **Trimberger**（Xilinx）：多篇 FPGA 架構與應用論文，記錄了該領域的早期發展。