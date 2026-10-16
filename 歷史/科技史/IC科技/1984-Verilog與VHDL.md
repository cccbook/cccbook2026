# 1984-Verilog與VHDL

## 案件摘要（3 行內的梗概）
在積體電路設計界，一場關鍵的語言革命正在醞釀。1984年，Gateway Design Automation 提出 Verilog，試圖取代手工繪製佈局的舊有模式。1987年，美國國防部主導的 VHDL 也正式成為 IEEE 標準，為硬體描述語言（HDL）的戰國時代拉開序幕。

## 前因 -- 為什麼會有這個案子
在 1980 年代初期，IC 設計仍停留在「手畫版圖」（manual layout）的黑暗時代。設計師必須在方格紙上或直接在佈局編輯器中繪製電晶體、金屬層與連線，這種做法隨著電路規模呈指數成長而變得難以為繼。更致命的是，晶片製造需要昂貴的光罩（mask），任何設計錯誤都意味著數十萬美元的打水漂。

這個案件的動機很明確：設計師亟需一種能在「暫存器轉移層級」（Register Transfer Level, RTL）描述硬體行為的方式，讓設計能在實際下線前先經過驗證。時代呼喚一種抽象層級的革命——從幾何佈局（geometry）轉向功能描述（behavior）。

## 線索與推理 -- 數學式、程式、理論（本體，最詳細）
本案的核心線索，是「抽象層級的上移」（abstraction elevation）。硬體設計的抽象可用層級來理解：

- **佈局層（Layout）**：描述電晶體、擴散區、金屬走線的幾何位置。
- **邏輯閘層（Gate Level）**：由 AND、OR、NOT 等基本邏輯閘構成的網路。
- **暫存器轉移層級（RTL）**：描述資料在暫存器間如何轉移與運算，時間以時脈（clock）為單位組織。

RTL 的數學本質，可以視為一個同步有限狀態機（Synchronous FSM）。對於一個時序電路，其狀態轉移可形式化地表示為：

$$
Q_{t+1} = f(Q_t, X_t), \quad Y_t = g(Q_t, X_t)
$$

其中 $Q_t$ 為當前狀態（暫存器值），$X_t$ 為輸入，$Y_t$ 為輸出，$f, g$ 為組合邏輯函數。這正是 RTL 想要捕捉的模型。

### Verilog 的崛起（1984）
Gateway Design Automation 於 1984 年提出 Verilog。其設計哲學是「類 C 的語法」（C-like syntax），讓工程師能快速上手。Verilog 最具代表性的時序建構是 `always @(posedge clk)`，用於描述在時脈正緣觸發的同步邏輯：

```verilog
module counter (
  input clk,
  input reset,
  output reg [7:0] count
);
  always @(posedge clk) begin
    if (reset)
      count <= 8'b0;
    else
      count <= count + 1'b1;
  end
endmodule
```

這段程式碼所描述的，正是上述的狀態轉移：每個時脈上緣，`count` 狀態根據 `reset` 與當前值更新。注意此處使用非阻塞賦值（`<=`）而非阻塞賦值（`=`），這是 Verilog 時序模型正確模擬的關鍵線索。

### VHDL 的制度化（1987）
與 Verilog 不同，VHDL（VHSIC Hardware Description Language）源自美國國防部 VHSIC 計畫，目的在於建立一套可供嚴格驗證與文件化的硬體描述語言。1987 年，VHDL 正式成為 IEEE 1076 標準。其對應的同步邏輯描述是 `process` 結構：

```vhdl
process (clk)
begin
  if rising_edge(clk) then
    if reset = '1' then
      count <= (others => '0');
    else
      count <= count + 1;
    end if;
  end if;
end process;
```

VHDL 強調強型別（strong typing）、結構化與自我文件化，與 Verilog 的簡潔風格形成鮮明對比。

### 模擬 vs 合成的語意差異（最關鍵的推理）
本案最微妙的線索在於：**HDL 是描述語言，不是程式語言**。Verilog/VHDL 同時服務兩個用途——模擬（simulation）與邏輯合成（synthesis）。

- **模擬語意（Simulation Semantics）**：定義語言在事件驅動模擬器中的精確執行行為（時間、delta cycle、敏感度列表）。
- **合成語意（Synthesis Semantics）**：定義哪些語言建構子可以被邏輯合成工具翻譯成實際的閘級電路（netlist）。

這個差異是設計陷阱的溫床：某些寫法在模擬器中行為正確，卻無法被合成，或反之。正因如此，RTL 設計師必須時時銘記「合成可行」（synthesizable）的寫法。

### 演進：Verilog-2001 與 SystemVerilog
時間線上還有後續線索。Verilog-1995（IEEE 1364-1995）後，IEEE 1364-2001（Verilog-2001）大幅改善了模組介面（ANSI port list）、generate、signed 等功能。更進一步，Accellera 推出的 SystemVerilog（後納入 IEEE 1800）則在驗證（assertion、coverage）與物件導向等面向大幅擴充，將 HDL 從單純的「描述」推向「設計＋驗證」（design & verification）整合的領域。

## 結案 -- 後果與影響
本案以「HDL 正式成為業界共通語言」宣告結案。Verilog 與 VHDL 的出現，完成了從「手畫版圖」到「RTL 設計」的革命性跨越。它們讓設計抽象化、可重複使用、可模擬驗證，直接促成了數位 IC 設計流程的現代化。

最深遠的影響是：設計複雜度不再受限於人手繪製的能力，而是受限於我們能否正確地「描述」與「驗證」系統。這場革命為日後 SOC（System-on-Chip）的蓬勃發展，鋪設了最關鍵的語言基石。

## 關鍵人物與文獻
- **Prabhu Goel** 等人（Gateway Design Automation）：推出 Verilog（1984），開啟商業化 HDL 時代。
- **美國國防部 VHSIC 計畫**：推動 VHDL 的開發與標準化。
- **IEEE 1076 委員會**：將 VHDL 標準化（IEEE Std 1076-1987）。
- **IEEE 1364 / IEEE 1800**：Verilog/SystemVerilog 標準演進。
- **Thomas & Moorby**，《The Verilog Hardware Description Language》：Verilog 經典教科書。
- **Ashenden**，《The Designer's Guide to VHDL》：VHDL 理論與實務權威。