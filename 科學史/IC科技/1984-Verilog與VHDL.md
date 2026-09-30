# 1984 - Verilog 與 VHDL：硬體描述語言的革命

## 案件摘要
1984 年 Gateway Design Automation 的 Phil Moorby 提出 Verilog，讓工程師用程式語言描述硬體；1987 年美國國防部贊助的 VHDL 成為 IEEE 標準（IEEE 1076）。從此晶片設計從「手畫版圖」進入「RTL 描述 + 自動合成」的時代。

## 前因 -- 為什麼會有這個案子
- 1970–80 年代晶片規模從數千閘（SSI/MSI）暴增到數萬閘（LSI/VLSI），人工畫版圖（layout）已不可行。
- 設計驗證只能靠麵包板或人工推理，錯誤代價極高：一枚 mask 重製要數週與數萬美元。
- 業界需要一種「可執行的規格書」：寫一次，既能模擬驗證，又能導出實際電路。
- 美國國防部（DoD）為了武器系統 IC 的文件一致性，主導開發 VHDL（VHSIC Hardware Description Language，VHSIC = Very High Speed Integrated Circuit）。

## 線索與推理 -- 數學式、程式、理論

### 1. 從版圖到 RTL 的革命
設計抽象層級由低到高：

$$
\text{物理版圖} \prec \text{電晶體} \prec \text{閘級} \prec \text{RTL} \prec \text{行為級}
$$

RTL（Register Transfer Level，暫存器轉移層級）的理論定義：電路被描述為一組暫存器與其間的資料轉移運算，在每個時脈邊緣：

$$
R_{j}(t+1) = F_j\big(R_1(t), R_2(t), \dots, R_k(t), x(t)\big)
$$

亦即狀態方程 $S' = F(S, X)$ —— 這正是有限狀態機（FSM）的數學模型，Mealy/Moore 機在 RTL 中獲得直接的程式化表達。

### 2. Verilog `always @(posedge clk)` 與 VHDL process
兩種語言用不同語法表達同一個「時脈邊緣觸發」語意：

```verilog
// Verilog：D 型正反器
module dff (input wire d, clk, rst_n, output reg q);
  always @(posedge clk or negedge rst_n)
    if (!rst_n) q <= 1'b0;
    else        q <= d;
endmodule
```

```vhdl
-- VHDL：D 型正反器
library ieee;
use ieee.std_logic_1164.all;
entity dff is
  port (d, clk, rst_n : in  std_logic;
        q             : out std_logic);
end entity;
architecture rtl of dff is
begin
  process (clk, rst_n)
  begin
    if rst_n = '0' then
      q <= '0';
    elsif rising_edge(clk) then
      q <= d;
    end if;
  end process;
end architecture;
```

### 3. 模擬 vs 合成的語意差異（本案件的「陷阱」）
- **模擬語意**：Verilog 依事件排程（event-driven simulation）逐行執行，`#delay`、阻塞/非阻塞賦值都有精確的排程行為。
- **合成語意**：綜合器只認得「可實現為電路」的子集（synthesizable subset）。
- 經典規則：**時序邏輯用非阻塞 `<=`，組合邏輯用阻塞 `=`**。混用會造成模擬與實際電路不一致（simulation-synthesis mismatch）：

```verilog
// 錯誤示範：模擬正確但合成出的電路行為不同
always @(posedge clk) begin
  b = a;   // 阻塞：立刻更新
  c = b;   // 同一週期 c 拿到「新」的 b —— 與意圖不符
end
// 正確：全部用 <= 時，c(t+1) = b(t) = a(t)，形成兩級移位
```

敏感列表不完整（如漏寫 `or b`）在模擬中造成鎖存行為，合成器則會推論出 Latch —— 兩者再次分歧。

### 4. 演進：Verilog-2001 → SystemVerilog
- **Verilog-1995**：IEEE 1364-1995，第一個 Verilog 標準。
- **Verilog-2001**：IEEE 1364-2001，加入 `always @(posedge clk)` 以外的簡化語法：`signed` 型別、`generate`、逗號分隔敏感列表、`localparam`、多維陣列。
- **SystemVerilog**（IEEE 1800-2005 起，2009 併入 1364）：加入 `logic` 型別、`interface`、`always_ff`/`always_comb`、`typedef`、`enum`、以及驗證用的 class、constrained random、SVA 斷言（SystemVerilog Assertions）。

```verilog
// SystemVerilog：意圖明確，消除語意歧義
module counter #(parameter WIDTH = 8)
  (input  logic             clk, rst_n,
   output logic [WIDTH-1:0] cnt);
  always_ff @(posedge clk or negedge rst_n) begin
    if (!rst_n) cnt <= '0;
    else        cnt <= cnt + 1'b1;   // (t+1) = (t) + 1 mod 2^W
  end
endmodule
```

## 結案 -- 後果與影響
- 設計產能提升一個數量級以上，百萬閘設計成為可能，直接促成 1990 年代 SoC 與深次微米革命。
- Verilog 因工具普及與 Cadence 於 1990 年開放（Open Verilog International）而成為業界主流；VHDL 則在歐洲、航天與軍工領域根深蒂固。
- 兩者共同催生了「RTL → 邏輯合成 → 閘級網表」的設計流程（見 1986-邏輯合成.md）。
- 今日 SystemVerilog 是唯一同時涵蓋設計與驗證（UVM）的工業標準語言。

## 關鍵人物與文獻
- **Phil Moorby**：Verilog 之父，Gateway Design Automation（1984），後進入 Cadence。
- **Gateway Design Automation**：推出 Verilog-XL 模擬器。
- **IEEE 1364**（Verilog）、**IEEE 1076**（VHDL）、**IEEE 1800**（SystemVerilog）。
- DoD VHSIC 計畫（1980s）：VHDL 的催生者；IBM、Intermetrics、Texas Instruments 參與開發。
- Donald Thomas & Philip Moorby, *The Verilog Hardware Description Language*（經典教科書）。
