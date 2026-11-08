# C.1 開源 EDA 術語對照表

開源數位晶片設計流程（Yosys → OpenROAD → signoff）涉及大量英文術語，本章整理常用詞彙的中英對照與意涵，作為全書的一致用語參考。

## 工具與專案

| 英文 | 中文 | 意涵 |
|---|---|---|
| OpenROAD | OpenROAD | 開源 RTL-to-GDSII 自動化實體設計工具，本書主角，涵蓋 floorplan 到 routing 與 ECO。 |
| OpenSTA | OpenSTA | 開源 static timing analysis 引擎，內建於 OpenROAD，負責時序簽核分析。 |
| OpenDB | OpenDB | OpenROAD 的資料庫層，以 C++ 表示 netlist 與實體資訊，Tcl 命令透過它操作設計。 |
| ORFS | OpenROAD Flow Scripts | OpenROAD 官方流程腳本，以 GNU Make 從 RTL 一路跑到 GDS 與 DRC/LVS。 |
| Yosys | Yosys | 開源 synthesis 工具，將 RTL 轉為 gate-level netlist。 |
| OpenLane | OpenLane | 以 OpenROAD + Yosys 為核心的封裝流程，提供預設配置的 ASIC 實作。 |
| iverilog | Icarus Verilog | 開源 Verilog 事件驅動模擬器，常用於功能驗證。 |
| Verilator | Verilator | 開源 Verilog 編譯式模擬器，速度快，廣泛用於迴歸驗證。 |
| KLayout | KLayout | 開源 GDS 檢視與編輯工具，常用於版圖檢查與 DRC script。 |
| Magic | Magic | 經典開源版圖編輯器，支援 DRC 與 GDS 產生。 |

## 檔案格式

| 英文 | 中文 | 意涵 |
|---|---|---|
| LEF | 實體庫交換格式（Library Exchange Format） | 描述 cell 的實體外形、pin 位置與繞線層規則。 |
| DEF | 設計交換格式（Design Exchange Format） | 描述設計的 placement、routing 與 floorplan 結果。 |
| Liberty (.lib) | 時序庫格式 | 描述 standard cell 的時序、功耗與 DC 特性模型。 |
| SPEF | 標準寄生交換格式 | 描述萃取後的 RC 寄生參數，供精確 STA 使用。 |
| GDSII | GDSII 版圖格式 | 晶圓製造的最終版圖交付格式。 |
| SDC | 設計約束格式（Synopsys Design Constraints） | 描述 clock、I/O delay 等時序限制，STA 的輸入之一。 |
| NLDM | 非線性延遲模型 | Liberty 內以二維查表表示延遲與 transition 的模型。 |
| CDL | 電路描述語言 | 簡化 netlist 格式，供 LVS 工具比對電路。 |
| VCD | 值變化轉儲 | 記錄訊號隨時間變化的波形檔，供模擬結果除錯。 |
| PDK | 製程設計套件（Process Design Kit） | 包含 tech LEF、Liberty、DRC/LVS 規則的製程檔案集合。 |

## 設計表示

| 英文 | 中文 | 意涵 |
|---|---|---|
| RTL | 暫存器傳輸層 | 用 Verilog/VHDL 描述暫存器間資料流動的抽象層級。 |
| netlist | 電路網表 | 由 cell 與 net 構成的連接描述，合成後的 gate-level 結果。 |
| standard cell | 標準元件 | PDK 提供的預鑄邏輯閘/正反器，版圖等高、可並排擺放。 |
| macro | 巨集電路 | 較大的預設計區塊，如 memory、IP block，placement 時需預留位置。 |
| instance | 實例 | netlist 中某個 cell 的一次具體使用。 |
| pad | 焊墊 | 晶片邊緣的 I/O 單元，連接訊號到封裝。 |
| pin | 接腳 | cell 或 block 的輸入輸出端點。 |
| tie cell | 綁定元件 | 提供常數 0/1 連接的小 cell，避免直接接電源軌。 |
| tapcell | 井接觸元件 | 提供 well/substrate 接觸，滿足 latch-up 規則。 |

## 實體設計階段

| 英文 | 中文 | 意涵 |
|---|---|---|
| floorplan | 布局規劃 | 劃分 die/core 區域、擺放 macro 與 power grid 的第一步。 |
| placement | 擺置 | 將 cell 放到 core 區域內，分 global placement 與 detailed placement。 |
| CTS | 時脈樹合成 | 插入 clock buffer 樹，使時脈抵達各正反器的 skew 最小化。 |
| routing | 佈線 | 將 net 依規則實際連接，分 global routing 與 detailed routing。 |
| power grid / PDN | 電源網絡 | 供 VDD/VSS 的金屬網格結構，由 pdngen 產生。 |
| pin placement | 接腳擺放 | 決定 block I/O pin 的位置，影響後續繞線品質。 |
| utilization | 使用率 | cell 面積占 core 面積的比例，太高會導致擁塞與收斂困難。 |
| legalization | 合法化 | detailed placement 將 cell 對齊 site 並消除重疊的步驟。 |
| ECO | 工程變更命令 | 在後段流程中做的小幅修正，如插 buffer、換 cell。 |
| tapeout | 下線 | 設計定案送交晶圓廠製造的最終階段。 |

## 簽核與分析

| 英文 | 中文 | 意涵 |
|---|---|---|
| signoff | 簽核 | 交付前的最終驗證（時序、DRC、LVS 全部通過）。 |
| STA | 靜態時序分析 | 不靠模擬向量、遍歷所有路徑的時序分析方式。 |
| setup time | 建立時間 | 時脈有效緣前資料需穩定的最短時間，違反造成 setup violation。 |
| hold time | 保持時間 | 時脈有效緣後資料需維持的最短時間，違反造成 hold violation。 |
| slack | 時序餘量 | 要求時間減去到達時間；負值即違規。 |
| WNS | 最差負 Slack | 所有路徑中最差的 slack 值。 |
| TNS | 總負 Slack | 所有違規路徑 slack 的總和。 |
| skew | 時脈偏斜 | 時脈抵達不同正反器的時間差。 |
| DRC | 設計規則檢查 | 檢查版圖是否符合製程幾何規則（spacing、min-area 等）。 |
| LVS | 版圖與電路比對 | 驗證 GDS 版圖抽取出的電路與 netlist 一致。 |
| antenna effect | 天線效應 | 長金屬走線累積電荷損傷閘極，需 diode 或跳層修復。 |
| MPW | 多專案晶圓 | 多個設計共享同一晶圓以分攤光罩費用的低成本投片方式。 |
| IR drop | 電壓降 | 電流通過電源網絡造成的壓降，過大影響時序與功能。 |
| congestion | 繞線擁塞 | 某區域需求走線資源超過供給，導致 short 與 DRC。 |
| clock propagation | 時脈傳播模式 | STA 計入實際 clock tree 延遲，post-CTS 分析必須的模式。 |
