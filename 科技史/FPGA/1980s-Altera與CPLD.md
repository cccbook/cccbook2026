# 1980s-Altera與CPLD

## 案件摘要
1983 年成立的 Altera，於 1984 年推出 EP300（EPROM-based PLD），並於 1988 年推出 MAX 5000 系列，確立了 CPLD（Complex PLD）這一產品類別。本檔追查：在 Xilinx 於 1985 年推出首顆 FPGA 之後，為何 Altera 選擇了截然不同的「複雜可程式邏輯」路線，而這條路線又在哪些戰場上反敗為勝。

## 前因 -- 為什麼會會有這個案子

1970 年代末期，數位邏輯設計的主流是 74 系列中小型積體電路（SSI/MSI）搭配 PROM。1978 年 Monolithic Memories（MMI）推出 PAL（Programmable Array Logic），以「可程式 AND 陣列 + 固定 OR 陣列」的架構讓設計師能用一顆晶片取代數顆 TTL，掀起第一次「可程式邏輯」革命。但 PAL 有兩個致命限制：容量太小（一顆只有 8~10 個宏單元等級的邏輯量）且一次可程式、燒錯即報廢。

1981 年 Lattice 推出 GAL，以 EEPROM 單元實現電子抹除重寫，解決了「不可逆」的問題，但容量瓶頸依舊。同時，1985 年 Xilinx 推出以 SRAM 為組態儲存的 XC2064 FPGA，以「邏輯塊海洋 + 可程式互連」開創了高容量路線，但 FPGA 也有自己的弱點：組態易失（斷電即失，需外部組態晶片上電載入）、互連延遲不確定（布線路徑不同延遲不同）、單價高。

Altera 於 1983 年在加州創立（創辦人為 Robert Hartmann、Michael Magran 等人），面對的正是這個「PAL 太小、FPGA 太不確定」的夾縫。Altera 的推理是：市場上絕大多數的實際設計，需要的不是十萬閘的靈活性，而是「幾百到幾千閘、確定延遲、上電即用」的中型可程式邏輯。1984 年的 EP300（EPROM-based PLD，24 腳）是第一發子彈；1988 年的 MAX 5000 系列則以「多個宏單元 + 中央可程式互連矩陣」的架構，正式定義了 CPLD。

## 線索與推理 -- 數學式、程式、理論（本體，最詳細）

### 線索一：PAL 的代數模型與它的天花板

PAL 的本質是一個兩級積之和（Sum-of-Products, SOP）電路：

$$f(x_1,\dots,x_n) = \sum_{i=1}^{m} P_i(x_1,\dots,x_n) = \sum_{i=1}^{m} \prod_{j \in S_i} \ell_j$$

其中每個乘積項 $P_i$ 是輸入文字（literal）的 AND，$m$ 是硬體提供的乘積項數量（典型為 8）。關鍵約束是：

- 每個宏單元**固定**分到 $m$ 個乘積項，項與項之間不能共用；
- 固定 OR 陣列意味着 $m$ 一出廠就定死，函數若需要超過 $m$ 個乘積項就無法實現。

這就是 PAL 的數學天花板：一個 $n$ 變數函數的最簡 SOP 形式可能需要多達 $\binom{n}{\lfloor n/2 \rfloor}$ 個質蘊含項（例如對稱函數），遠超硬體上限。設計師只能手工拆分邏輯、跨越多顆 PAL，於是「PAL 之間的接線」又變回了一團麵包板亂線——問題只是被縮小，沒有被消滅。

### 線索二：CPLD 的架構解法——PIA 與宏單元

MAX 5000 的架構推理可以拆成三層：

| 層級 | MAX 5000 對應 | 功能 |
|---|---|---|
| 宏單元（macrocell） | 內含共用可擴充乘積項的邏輯單元 | 局部 SOP 邏輯 + 輸出暫存器 |
| 邏輯陣列塊（LAB） | 16 個宏單元為一組 | 局部互連，降低 PIA 負載 |
| 可程式互連矩陣（PIA） | 全域匯流排矩陣 | LAB 之間、I/O 之間的全域布線 |

與 PAL 的根本差異有二：

1. **乘積項可共用與擴展**：宏單元的乘積項可以借給同一 LAB 內的其他宏單元（product-term expansion），打破「每人固定 8 項」的限制，等效於讓 $m$ 變成軟性資源。
2. **單一確定性互連**：所有信號都經過 PIA，且 PIA 是「乘積項驅動的全域 AND 陣列」而非逐段開關。這帶來一個決定性的數學性質——

### 線索三：確定性 timing 的數學證明

設信號從宏單元 $A$ 到宏單元 $B$。在 CPLD 中，任何路徑都必須是：

$$A \rightarrow \text{PIA} \rightarrow B$$

路徑數只有一種拓撲，因此延遲是一個常數：

$$t_{pd}^{\text{CPLD}} = t_{\text{macro}} + t_{\text{PIA}} + t_{\text{macro}} = \text{const}$$

反觀 Xilinx XC2000/3000 這類「海洋式（sea-of-blocks）」架構，信號要穿過 $k$ 個可程式開關（switch matrix / pass transistor）：

$$t_{pd}^{\text{FPGA}} = t_{\text{logic}} + \sum_{i=1}^{k} \left( t_{\text{sw}_i} + t_{\text{wire}_i} \right), \quad k \text{ 隨布線結果浮動}$$

其中經過 $k$ 個串接 RC 級的傳播延遲近似為：

$$t_{pd} \approx 0.69 \, R_{\text{sw}} C_{\text{wire}} \cdot \frac{k(k+1)}{2}$$

——注意是 $O(k^2)$ 而非 $O(k)$，因為每級開關的電容都累加到下一級。這個平方爆炸正是早期 FPGA 長布線延遲不可預測的物理根源。CPLD 用「一次經過、延遲恆定」交換掉了「高容量」，這是一筆清楚的可算交易：對於 fan-in 高、層數淺的邏輯（狀態機、解碼器、位址譯碼），CPLD 的 $t_{pd}$ 恆定且小，是嚴格優勢。

### 線索四：非易失性的系統級推理

EP300 用 EPROM 單元（浮閘電晶體，紫外線抹除）、MAX 5000 用 EPROM 式製程，組態儲存在晶片內部且斷電不消失。上電時序為：

$$t_{\text{ready}} \approx t_{\text{power-up}} \approx \text{數百 ns} \sim \mu s$$

對比 SRAM FPGA 的上電流程：需要外部 PROM、上電後先載入 bitstream（典型 XC2064 需數十 ms 等級），期間所有 I/O 處於三態。這意味着：

- 若系統中有 SRAM FPGA，它**無法**充當自己的上電控制邏輯；
- 而 CPLD 上電即活，**可以**充當整塊板子的電源排序、復位生成、甚至 FPGA 的組態載入控制器（config controller）。

這構成一個優雅的分工：CPLD 管「生」（上電與組態），FPGA 管「算」（大量邏輯）。這個分工模式一直延續到今日的 SoC FPGA 設計。

### 線索五：CPLD vs FPGA vs PAL 規格對照表

| 特性 | PAL（1978） | CPLD（MAX 5000, 1988） | FPGA（XC2000, 1985） |
|---|---|---|---|
| 邏輯模型 | 兩級 SOP，固定 OR | 多宏單元 SOP + 乘積項共用 | LUT / 查找表（Xilinx） |
| 等效容量 | ~數百閘 | 數百～數千閘 | 數千～數萬閘 |
| 組態技術 | 熔絲（一次性） | EPROM（非易失） | SRAM（易失） |
| 上電行為 | 即用 | 上電即用 | 需外部 bitstream 載入 |
| 互連延遲 | 固定 | 固定（單一 PIA） | 路徑相關，$O(k^2)$ RC 累積 |
| 適合邏輯 | 小型組合邏輯 | 淺層寬邏輯、狀態機、glue logic | 深層寬電路、資料路徑、大型系統 |
| 重複燒寫 | 無 | 有（紫外線/後續 EEPROM） | 無限次 |

從表中的第三、五、六列可以讀出 Altera 的整套推理：**CPLD 不是「較差的 FPGA」，而是把 PAL 的確定性與非易失性放大到千閘尺度的另一個物種**。

## 結案 -- 後果與影響

MAX 5000 之後，Altera 沿著 CPLD 路線持續推進（MAX 7000 於 1992 年改用 EEPROM，成為史上最長壽的可程式邏輯產品線之一），並在此基礎上發展出 1992 年採用 SRAM LUT 的 FLEX 8000——即本案的續集。CPLD 與 FPGA 從此成為可程式邏輯的兩大並存物種，而非先後取代關係。

- 確立「CPLD = 確定延遲 + 非易失 + 上電即用」的產品定位，glue logic 市場被 CPLD 完全收割；
- CPLD 擔任 FPGA 組態載入控制器的分工模式成為板級設計的標準套路；
- Altera 以此建立起僅次於 Xilinx 的市場地位，兩強格局（duopoly）延續三十年；
- MAX 7000 系列活到 2020 年代仍在大批量出貨，證明「淺層寬邏輯」的需求從未消失。

## 關鍵人物與文獻

- Robert Hartmann 等 —— Altera 共同創辦人（1983），確立「複雜可程式邏輯」路線
- John Birkner、H.T. Chua —— PAL 發明人（MMI, 1978），CPLD 架構的源頭
- Freeman Waugh —— GAL/EEPROM 可程式邏輯先驅（Lattice, 1981）
- Altera, "EP300 Datasheet"（1984）—— 首顆 EPROM-based PLD
- Altera, "MAX 5000 Family Datasheet"（1988）—— CPLD 架構定義文件
- W. Carter et al., Xilinx XC2064（1985）—— 對照組：首顆 SRAM FPGA
- S. Brown, J. Rose, "Architecture of FPGAs and CPLDs: A Tutorial"（IEEE Design & Test, 1996）—— 兩種架構比較的經典文獻
