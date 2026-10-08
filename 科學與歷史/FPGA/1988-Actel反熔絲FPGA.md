# 1988-Actel反熔絲FPGA

## 案件摘要
1988 年，創立於 1985 年的 Actel 推出 ACT-1，這是史上第一顆商用反熔絲（antifuse）FPGA。本檔追查：在 SRAM FPGA 已占先機的 1988 年，Actel 為何押注「一次可程式、不可逆」的反熔絲技術，而這條路線又如何在航太與軍事市場建立起 Xilinx 無法撼動的堡壘。

## 前因 -- 為什麼會會有這個案子

1985 年 Xilinx 的 XC2064 開創了 SRAM FPGA，但它的弱點清單很長：組態存於 SRAM，斷電即失；上電後需數十 ms 從外部 PROM 載入 bitstream，期間系統不可用且需防範載入過程被干擾；SRAM 單元（6T 結構）體積大，擠壓了邏輯密度；且 SRAM 對輻射引致的單粒子翻轉（SEU, Single Event Upset）極度敏感——一個高能粒子打翻一個位元，整個互連或邏輯就錯了。

另一方面，傳統閘陣列（gate array）雖然密度高、延遲確定，但需要數萬美元的 mask 費用與數週的製造週期，完全喪失「可程式」的意義。1980 年代的航太與軍工設計師陷入兩難：要彈性就得忍受 SRAM FPGA 的易失與輻射脆弱，要可靠就得忍受閘陣列的不可更改。

Actel 於 1985 年在加州 Sunnyvale 創立（創辦人包括 Sinnappa Chetty 等前 Intel 與 Zilog 工程師），其核心洞察是：存在一種第三選項——反熔絲。熔絲（fuse）出廠時導通、燒斷後開路；反熔絲則相反：**出廠時是開路，編程後擊穿形成永久導通**。它平時不需要任何電晶體來「記住」組態，體積可以做到極小；一旦擊穿即成永久物理通路，天然抗輻射、天然非易失、天然上電即用。1988 年的 ACT-1（等效約 2000 閘，採用 PLICE 反熔絲製程，與 TI 合作量產）將這個洞察變成了產品。

## 線索與推理 -- 數學式、程式、理論（本體，最詳細）

### 線索一：反熔絲的物理——PLICE 的擊穿機制

Actel 使用的 PLICE（Programmable Low-Impedance Circuit Element）反熔絲是一個夾在兩層摻雜多晶矽/擴散區之間的介電層（ONO：氧化物-氮化物-氧化物疊層），厚度僅約 $80 \sim 100\,\text{\AA}$：

$$\text{Poly}_1 \;|\; \text{ONO dielectric} \;|\; \text{Poly}_2$$

未編程時，介電層是絕緣體，等效電路為一個小電容：

$$R_{\text{off}} \approx 10^{10} \sim 10^{12}\,\Omega, \quad C_{\text{off}} \approx 1 \sim 2\,\text{fF}$$

編程時施加約 $11 \sim 12\,\text{V}$ 的電壓（遠高於 $5\,\text{V}$ 工作電壓），介電層發生軟擊穿（dielectric breakdown），電流豚衝在介電層中熔出一條永久性矽導電細絲（conductive filament）：

$$R_{\text{on}} \approx 50 \sim 100\,\Omega, \quad C_{\text{on}} \approx 1 \sim 2\,\text{fF}$$

關鍵數學對比是**面積效率**。一個 SRAM 組態單元是 6 個電晶體：

$$\text{SRAM cell} = 6T \approx 100 \sim 120\,\mu\text{m}^2 \text{（0.8μm 製程）}$$

而一個 PLICE 反熔絲不需要任何控制電晶體（電壓經由特殊供電路徑施加），佔用面積：

$$\text{PLICE} \approx 1 \sim 2\,\mu\text{m}^2 \text{，即 SRAM 單元的約 } \tfrac{1}{100}$$

這個兩個數量級的面積比，是 Actel 敢於在架構中大量鋪設反熔絲（ACT-1 約 11 萬顆）而不犧牲密度的根本原因。代價則是一次性：$R_{\text{on}} \approx 50\,\Omega$ 不可回復，燒錯即報廢（或只能靠多餘備份路徑繞過）。

### 線索二：三種組態技術對照表

| 特性 | 反熔絲（PLICE） | SRAM | EEPROM/Flash |
|---|---|---|---|
| 出廠狀態 | 開路（$10^{10}\,\Omega$） | 隨機（需載入） | 開路/導通（可改） |
| 編程可逆性 | **不可逆** | 無限次重寫 | 約 $10^4 \sim 10^5$ 次抹寫 |
| 組態易失性 | 非易失 | **易失**（斷電即失） | 非易失 |
| 上電即用 | 是（ns 級） | 否（需載入 bitstream，ms 級） | 是（較慢的讀取） |
| 組態單元面積 | 極小（~1% of SRAM） | 大（6T） | 中（~2T + 電荷泵） |
| 抗輻射（SEU） | **極佳**（組態為物理結構，無位元可翻） | 差（需 TMR 或刷寫） | 中 |
| 導通電阻 | $50 \sim 100\,\Omega$（偏大） | 由傳輸閘決定（~數百 Ω） | 由傳輸閘決定 |
| 編程設備 | 需專用編程器 + 向量測試 | 板上直接由 PROM 載入 | 板上或編程器 |

從表中「抗輻射、上電即用、組態單元極小」三列的同時命中，可以直接推出 Actel 的目標市場畫像：**航太與軍事**。

### 線索三：通道式架構——閘陣列的影子

ACT-1 的物理版圖（floorplan）刻意模仿閘陣列：

```
 [邏輯模組列]   [邏輯模組列]   [邏輯模組列]
 ----routing channel------
 [邏輯模組列]   [邏輯模組列]   [邏輯模組列]
 ----routing channel------
```

- 邏輯模組（Logic Module, LM）排成列與列之間留出水平布線通道（routing channel），通道內鋪設多條線段，線段與線段之間以反熔絲交叉連接；
- 這與閘陣列的「單元列 + 布線通道」版圖同構，因此 Actel 可以直接借用閘陣列產業成熟的版圖與自動布線工具鏈；
- 布線以「兩點一熔絲」方式完成：連線 $A \to B$ 就是把路徑上的反熔絲逐一擊穿。路徑經過 $k$ 個反熔絲的延遲為：

$$t_{pd} = t_{\text{LM}} + \sum_{i=1}^{k}\left( t_{\text{wire}_i} + t_{R_{\text{on}}} \right)$$

$R_{\text{on}} \approx 50 \sim 100\,\Omega$ 遠大於金屬互連，因此每穿一顆反熔絲都付出可觀的 RC 延遲——Actel 的布線演算法必須嚴格控制 $k \le 2 \sim 3$。這是反熔絲 FPGA 的設計紀律：**延遲可預測（擊穿後路徑固定、不變），但每次跳接都昂貴**。

ACT-1 的邏輯模組本身也耐人尋味：不是 Xilinx 的 LUT，而是一個 8 輸入的多工器樹（三個 2:1 MUX + 組合），恰好能實現任意 3 變數函數加上部分 4 變數函數：

$$f(a,b,c) \text{ 任意 3-var 全覆蓋；} d\text{-dependent 子集覆蓋}$$

這個「MUX-based module」在當時被證明比 LUT 更省面積（MUX 樹的電晶體數少於 $2^4 = 16$ 位的 LUT SRAM + 選擇器），是 Actel 在密度上與 Xilinx 競爭的本錢。

### 線索四：航太與軍事偏好的推理鏈

把物理事實轉成系統優勢，推理鏈如下：

1. **抗 SEU**：SRAM 組態是「儲存的位元」，宇宙射線可翻轉；反熔絲組態是「物理短路」，沒有位元可以翻。在輻射環境中，反熔絲 FPGA 的組態錯誤率近似為零：

$$\text{SEU rate}_{\text{SRAM}} \sim 10^{-5} \text{ errors/bit-day（LEO）} \quad \Rightarrow \quad \text{SEU rate}_{\text{antifuse}} \approx 0$$

2. **上電即用**：衛星在軌道日出日落循環中頻繁斷電重啟，SRAM FPGA 每次都要重新載入（且有載入瞬間受單粒子擾動的風險）；反熔絲 FPGA 上電 ns 級即工作。
3. **無需外部組態晶片**：省掉 PROM = 少一個可被輻射擊中、可被偽造、可被篡改的零件——對軍規供應鏈安全是實質利益。
4. **不可逆 = 防篡改**：組態燒死在矽內，無法以讀出 SRAM 的方式複製 bitstream，天然防逆向。

這四條加總，解釋了為何 Actel（及其後繼者 Microsemi/Microchip）至今仍是航太級 FPGA 的事實標準，即使它的重編程能力為零。

## 結案 -- 後果與影響

ACT-1 之後，Actel 陸續推出 ACT-2、ACT-3、SX、ProASIC（Flash 組態）等系列，2022 年被 Microchip 收購。反熔絲路線證明了一個重要命題：**FPGA 不是一種技術，而是一種抽象**——組態儲存介質可以是 SRAM、EPROM、Flash 或反熔絲，只要能實現「可程式邏輯陣列」就算 FPGA。

- 建立「組態技術光譜」：SRAM（彈性/易失）— Flash（折衷）— 反熔絲（可靠/一次性），各自佔據不同市場；
- 航太、軍工、醫療（需上電即用）市場被反熔絲/Flash FPGA 長期占據，Xilinx 至今未完全突破；
- 反熔絲的「不可逆」特性意外成為安全賣點，預示了日後 bitstream 加密與防篡改議題；
- MUX-based 邏輯模組證明 LUT 不是唯一解，啟發後續多種架構實驗。

## 關鍵人物與文獻

- Sinnappa Chetty 等 —— Actel 共同創辦人（1985）
- Bill Waugh（TI）與 Actel 團隊 —— PLICE 反熔絲製程的共同開發者
- Actel, "ACT-1 Family Field Programmable Gate Array Datasheet"（1988）
- A. El Gamal et al., "An Architecture for Electrically Configurable Gate Arrays"（IEEE JSSC, 1989）—— Actel 架構的經典論文
- J. Greene, E. Hamdy, S. Beal, "Antifuse Field Programmable Gate Arrays"（Proceedings of the IEEE, 1993）—— PLICE 物理與可靠性
- W. Carter et al., Xilinx XC2064（1985）—— 對照組：SRAM FPGA 起源
