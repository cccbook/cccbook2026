# A.1 常用開源 EDA 框架與工具索引

開源 EDA 工具的發展史，幾乎就是一部「學術界先開源、產業界後跟進」的歷史。一九八〇到九〇年代，Caltech、Berkeley、UCLA 等校園裡誕生的原型系統（Magic、SIS、ABC 的前身），奠定了日後整個開源晶片設計流程的基石。二〇〇〇年代以後，隨著 Yosys、VPR、nextpnr 等專案日趨成熟，以及 DARPA/CHIPS 計畫在 2017 年之後對 OpenROAD 的大力資助，開源社群終於在 2020 年前後達成一個重要里程碑：第一次能以純開源工具完成從 RTL 到 GDSII 的完整 ASIC 流程（如 OpenLane 與 SkyWater SKY130 PDK 的組合）。本附錄以表格索引本書引用過的常用開源工具，並為每一個工具補上簡短的身世考據。

## 工具總表

| 工具 | 領域 | 主要功能 | 原始機構 / 作者 | 首版年份 | 取得方式 |
|---|---|---|---|---|---|
| Yosys | 邏輯合成 | RTL 讀取、elaboration、優化、技術映射 | Clifford Wolf（奧地利） | 2012 | github.com/YosysHQ/yosys |
| ABC | 邏輯合成 / 驗證 | AIG 優化、scorr、mapping、SAT 驗證 | UC Berkeley，Alan Mishchenko | 2005 | github.com/berkeley-abc/abc |
| VPR / VTR | FPGA | packing、placement、routing 與架構探索 | 多倫多大學 Jonathan Rose 等人 | 1997（VPR 1.0） | verilogtorouting.org |
| nextpnr | FPGA | P&R（iCE40、ECP5、Nexus、gowin 等） | David Shah、Claire Xen（Wolf） | 2018 | github.com/YosysHQ/nextpnr |
| OpenROAD | ASIC 後端 | floorplan、place、CTS、route、timing 全流程 | UCSD/DARPA CHIPS，Andrew Kahng、Igor Markov 等 | 2018 | theopenroadproject.org |
| OpenLane / OpenLane 2 | ASIC 全流程 | 將 Yosys+OpenROAD+Magic 等整合為自動流程 | efabless（Anton Blanchard、Mohamed Shalan、Donn Morrison） | 2020 | github.com/The-OpenROAD-Project/OpenLane |
| Magic | 版圖編輯 / DRC | 互動式 VLSI 版圖、corner-stitching DRC | UC Berkeley，John Ousterhout | 1980 | opencircuitdesign.com/magic |
| ngspice | 電路模擬 | SPICE3f5 衍生的電晶體級模擬器 | Berkeley SPICE 衍生，ngspice 團隊 | 1993 | ngspice.sourceforge.net |
| iverilog | 事件驅動模擬 | Verilog-2005 編譯與模擬 | Stephen Williams | 1998 | github.com/steveicarus/iverilog |
| Verilator | 編譯式模擬 | 把 Verilog/SystemVerilog 編成 C++ 加速模擬 | Wilson Snyder（Antmicro 等贊助） | 1998（開源化 2003） | verilator.org |
| KLayout | 版圖檢視 / 腳本 | GDS/OASIS 檢視、DRC 腳本、magic-layer 處理 | Matthias Koefferlein（德國） | 2009 | klayout.de |
| OpenFPGALoader | 燒錄 | 跨廠商 FPGA bitstream 下載（JTAG/FTDI） | Gwenhael Goavec-Merou | 2020 | github.com/trabucayre/openFPGALoader |
| TritonRoute（TritonRoute-WLE、TritonRoute2） | 繞線 | 佈局後 global/detailed routing（後併入 OpenROAD） | UCSD/TAMU，Igor Markov、Andrew Kahng 團隊 | 2008（ISPD 比賽版本） | 併入 github.com/The-OpenROAD-Project/OpenROAD |
| RePlAce | 全域佈局 | 電流密度模型（ePlace）全域佈局 | UCSD/UT Austin，Chin-Chih Chang、Jhih-Rong Gao、Igor Markov 等 | 2018 | github.com/The-OpenROAD-Project/RePlAce |
| hMETIS | 圖分割 | 多層次 hypergraph partitioning（學術授權） | 明尼蘇達大學 George Karypis、Vipin Kumar | 1997 | users.cs.umn.edu/~karypis/metis/hmetis |
| KaHyPar / CuGR | 圖分割 | 現代多層次分割（KaHyPar 為 N 級多層次；CuGR 為 GPU 加速分割） | 卡爾斯魯爾理工（KIT）Sebastian Schlag 等 / 學界近期 GPU 工作 | KaHyPar 2014 | github.com/kahypar/kahypar |

## 各工具的歷史背景

Yosys 是開源邏輯合成的中樞。Clifford Wolf 在完成 OHR（Open Hardware Repository）相關工作之際，於 2012 年推出這套以 C++ 撰寫、以 IR 為核心的合成器，並內建呼叫 ABC 的橋接（`abc` pass），使開源社群第一次擁有從 RTL 到 gate-level netlist 的完整路徑。YosysHQ 成立後，Yosys 成為 OpenLane、F4PGA（前身 SymbiFlow）等流程的共同起點。

ABC 雖小，卻是開源合成品質的靈魂。Berkeley 的 Alan Mishchenko 自 2005 年起以 And-Inverter Graph（AIG）為統一表示，重寫了布爾優化、resubstitution、SAT sweeping 與技術映射（`amap`、`&nf` 等），許多商業合成器的核心思想也源自這裡的論文。Yosys 幾乎所有邏輯優化的重活都交給 ABC。

VPR 是 FPGA 學術界的事實標準。多倫多大學 Jonathan Rose 教授團隊自 1990 年代末發展 VPR，搭配 VTR（Verilog-to-Routing）專案把 Yosys、ABC 與 VPR 串成完整流程，幾乎所有 FPGA 架構論文都以 VTR benchmark suite 與 VPR 為比較基準。其 packing（T-VPack）、SA placement 與 maze-based routing 演算法，也是本書 FPGA 章節的核心素材。

nextpnr 誕生於 iCE40 反向工程社群。Claire Xen（Clifford Wolf）與 David Shah 在 2018 年以Project IceStorm 的 bitstream 研究為基礎寫出通用 P&R 框架，可透過架構描述（ChipDB 或 Python arch）支援 iCE40、ECP5、MachXO2、Nexus 等家族。它取代了前一代 icestorm 的 arachne-pnr，成為開源 FPGA 流程的預設後端。

OpenROAD 是 DARPA「IDEA」與 CHIPS 計畫的旗艦成果。UCSD 的 Andrew Kahng、後來加入 UT Austin 的 Igor Markov 與 NVIDIA 出身的 Tom Spyrou（現為 Precision Innovations 領軍）等人，自 2018 年起把 TritonPlace、TritonRoute、OpenDP、OpenSTA 等學術元件整合成一套可做到 24 小時內完成 RTL-to-GDS 的自動流程（「No Human Intrusion」），是 OpenLane 的引擎。

OpenLane 由 efabless 在 2020 年為 SKY130 的 chipIgnite 服務而打造，把 Yosys、OpenROAD、Magic、KLayout 用 Tcl（後來 OpenLane 2 改用 Python）腳本串起來，加上 Step/State 的設計，讓一般工程師能用一條命令跑完 ASIC 流程。它是第一個被大規模用於 tapeout（如多次 MPW Shuttle）的開源流程。

Magic 是史上最長壽的開源 VLSI 工具之一。John Ousterhout 在 1980 年前後於 Berkeley 博士期間寫出這套以 corner-stitching 資料結構為核心的版圖編輯器，後來由 Caltech 的 Tim Edwards 維護至今。它的 DRC 引擎（尤其 GDS 讀寫與 SKY130 驗證組合）至今仍是 OpenLane signoff 的一環。

ngspice 血統可追溯到 1975 年 Berkeley 的 SPICE。Larry Nagel 與 Donald Pederson 的 SPICE 經 SPICE3f5 於 1993 年起由社群以開源方式接手維護，成為開源 PDK（如 SKY130）提供 SPICE 模型時的預設模擬器，也是本書討論 cell delay 抽取時的底層工具。

iverilog 與 Verilator 代表開源模擬的兩條路線。Stephen Williams 自 1998 年維護 Icarus Verilog，走事件驅動、解譯式路線，易用但速度有限；Wilson Snyder 的 Verilator 則把 RTL 編譯成多執行緒 C++，速度可快上一到兩個數量級，如今已是大型 SoC（如 Google 的一些研究專案、OpenTitan 驗證）的主力開源模擬器。

KLayout 由德國工程師 Matthias Koefferlein 於 2009 年開源，補上了商業版圖檢視器（如 Virtuoso、CalibreWorkbench）之外的一塊空白，提供高效能 GDS/OASIS 顯示、Ruby/Python 腳本與獨立的 DRC 引擎（DRC deck 常見於 SKY130 社群流程）。

OpenFPGALoader 由 Gwenhael Goavec-Merou 於 2020 年開始開發，統一了過去各家自行維護的燒錄工具（icepack/iceprog、ecppll/openocd 等），支援 Xilinx、Intel、Lattice、Gowin 等數十款元件，是開源 FPGA 流程從 bitstream 走到實體板卡的最後一哩。

TritonRoute 系列出自 UCSD 與 Texas A&M 的學術路線。Igor Markov 團隊在 ISPD 2008 佈局/繞線比賽前後發展 TritonRoute-WLE（wirelength extrusion）與後續的 detailed router，最終被整併進 OpenROAD 的 ODR（OpenROAD Detailed Router，即 FlexRouter 前身），是開源 ASIC detail routing 的演算法骨幹。

RePlAce 將 2012 年台大電機系與 UCLA 合作提出的 ePlace 電流密度佈局演算法（Chin-Chih Chang 等人於 ICCAD/ICCAD'15 發表）工程化，以電場/電流密度的力學類比求解全域佈局，在 2018 年被 OpenROAD 採納為預設 global placer，展現了「論文變工具」的經典路徑。

hMETIS 是圖分割領域的分水嶺。明尼蘇達大學的 George Karypis 與 Vipin Kumar 在 1997 年提出的多層次 hypergraph partitioning 演算法（搭配 METIS），影響了此後二十年所有分割器。由於授權關係（僅供學術使用），它無法進入主流開源發行版，於是社群轉而擁抱 KIT 的 KaHyPar（2014 起，Sebastian Schlag 等人，以 N-level 與穩定的品質著稱）與近年 GPU 加速的分割研究（如 CuGR 等以 CUDA 實作的新一代分割器），形成「經典—現代」兩代的對照。

這些工具彼此銜接，構成今天開源 EDA 的全景：Yosys 與 ABC 負責邏輯，VTR 與 nextpnr 覆蓋 FPGA，OpenROAD 與 OpenLane 覆蓋 ASIC，Magic、KLayout、ngspice、Verilator 則在驗證與 signoff 各據一方。理解每個工具「從哪個實驗室來、解決了哪一個瓶頸」，正是閱讀 EDA 演算法史最好的索引。
