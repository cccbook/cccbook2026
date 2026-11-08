# A.3 ASIC 與 FPGA 物理設計演算法對照矩陣

把 ASIC 後端與 FPGA CAD 並排來看，會發現一件有趣的事：兩者共享幾乎同一套演算法祖源——maze routing（Lee 演算法，1961）、模擬退火（Kirkpatrick et al., 1983）、多層次圖分割（Fiduccia–Mattheyses 1982、Karypis 的 hMETIS 1997）、二次式與力向量佈局（Kleinhans 的 GORDIAN 1991、Eisenmann 的 force-directed 1991）——卻在資源結構的約束下分岔成兩棵不同的樹。ASIC 的晶片是連續的：任何一格金屬、任何一點矽面積都可用，演算法必須在連續空間上最佳化面積、線長與時序，最後靠 legalization 把結果「整數化」到製程網格。FPGA 的晶片則是離散的：邏輯資源是固定的 LUT/FF/BRAM 陣列，開關盒（switch box）的連接性是出廠就定死的，演算法必須把電路「塞進」這個有限且不均勻的資源網格，optimization 目標從「畫最好的圖」變成「在不違規的前提下找到可行解」。本章以一張對照矩陣整理兩大領域在各設計階段的演算法差異，並簡述分岔的歷史脈絡。

## 對照矩陣

| 階段 | ASIC 核心演算法 | FPGA 核心演算法 | 優化目標差異 | 代表工具 / 論文 |
|---|---|---|---|---|
| Logic optimization | AIG-based resub、SAT sweeping、rewrite/refactor（ABC） | LUT-level resynthesis、cut-based restructure（ `abc -d lutpack`、UTPack） | 最小化 gate/級數 vs. 最小化 LUT 數與 LUT 深度 | Mishchenko ABC；Cong & Hwang UCB |
| Technology mapping | 標準單元覆蓋（cut-covering、SIS、`amap`、`&nf`） | cut enumeration + 覆蓋（CutMap、FlowMap、T-VPack packing） | area/delay 對 cell library vs. $`k`$ -LUT 覆蓋 | Cong & Ding FlowMap 1994；Berkeley SIS |
| Partitioning | 多層次 hypergraph partition（hMETIS、KaHyPar、F-M/K-L） | 同源，但以 LUT/CLB 為單位，接 packing（T-VPack、AAPack） | 切割數、edge cut vs. LUT/CLB 資源 + inter-CLB wire 數 | Fiduccia–Mattheyses 1982；Karypis hMETIS 1997 |
| Floorplanning | 連續區域規劃（B*-tree、sequence pair、SA、analytic mixed-size） | 幾乎不存在；硬巨集（BRAM/DSP）由 arch 固定位置，僅做 macro assignment | macro 位置與 blocked 區 vs. 固定資源網格 | Chang, Cong B*-tree 2000；Murata sequence pair 1995 |
| Global placement | 連續全域：analytic（ePlace/RePlAce、RePlAce 電場模型）、quadratic（FastPlace、mPL6）+ SA 混合 | 離散模擬退火（VPR T-Place）、analytic 輔助（Analytical placer for FPGA、UTPlace-F） | HPWL + congestion + timing vs. CLB/LUT 佔用 + 可繞性 | Chang ePlace ICCAD'15；Betz & Rose VPR 1997 |
| Legalization | 四角/Abacus/針對 cell row 的緊密擺放 | 直接落到固定 site：packing 進 LUT/FF、cluster 分配 | 吸附到 row 網格 vs. 吸附到 CLB/SB 資源 | Viswanathan Abacus 2007；Betz & Rose |
| Global routing | 碎形/二維格上迷宮+擁塞（Labyrinth、BoxRouter、NTUgr） | negotiated congestion routing（PathFinder，VPR/nextpnr 核心） | 線長 + overflow vs. 在固定 switch box 內找可繞路徑 | Kastner Labyrinth 2002；Betz & Rose PathFinder 1999 |
| Detail routing | grid-based pattern/maze router（TritonRoute、BonnRoute、Dr. CU） | 在 SB/CB 拓撲內做 exact routing（nextpnr router、VPR detail） | DRC 精確性 vs. 硬體 bitstream 一致性 | UCSD TritonRoute；Claire Wolf nextpnr |
| Timing analysis | STA（OpenSTA、Synopsys PrimeTime）：delay 模型精細（NLDM/CCS）、PATH-based | STA 在 LUT 延遲近似 + P&R 迭代中融入（VPR delay model） | 精確 delay signoff vs. 快速估計以引導 P&R | OpenROAD OpenSTA；VPR timing analyzer |
| Signoff | DRC/LVS（Magic、KLayout、Calibre）、formal、gate sim | bitstream 生成 + 可靠性驗證（nextpnr `--freq`、FASM） | 製程規則完備 vs. 架構規則完備 + 時脈可達 | OpenLane、Magic；icepack/FASM |

## 同源而分岔的歷史脈絡

1980 年代，兩個領域還在同一个實驗室裡育種。Berkeley 的 MAGIC 團隊與 Caltech 的資源，既催生了 ASIC 版圖工具，也餵養了早期的 FPGA CAD——Xilinx 的自動化工具很多早期技術來自學術界與 Berkeley 系。當時「-placement」演算法論文幾乎同時宣稱對 ASIC cell row 與 FPGA CLB 皆可適用：模擬退火（Timberwolf 1985，Sechen 與 Sangiovanni-Vincentelli）同時是 ASIC 與 FPGA placer 的祖師；Lee maze routing 1961 年的格子搜尋，則同時支撐了 ASIC 的 detail router 與 FPGA 的 switch-box router。

分岔始於 1990 年代中期 FPGA 架構與 CAD 的系統化。Betz 與 Rose 在 1997 年提出 VPR，把 FPGA 的 P&R 拆解成 packing（把 LUT/FF 塞進 CLB）、SA placement 與 negotiated-congestion routing（PathFinder）三段，確立了以「資源合法佔用」為中心的演算法體系；同期的 ASIC 界則沿著 GORDIAN、mPL、Capo 等路線，走向大規模連續優化 + legalization 的範式。此後二十年，兩邊各有自己的競賽與 benchmark（見 A.2），演算法逐漸殊途：ASIC 走向 analytic placement（ePlace、RePlAce）、精細 delay 模型與 grid-based routing；FPGA 走向 pack-aware placement（UTPlace-F、混合 analytic+SA）、PathFinder 式的違約擁塞談判，以及對固定 bitstream 拓撲的完美一致性要求。

近年則出現「合流」的跡象。一方面，OpenROAD 與 OpenLane 讓 ASIC 流程開源化，學術演算法能直接進入產業流程；另一方面，FPGA 界引入 analytic placement 與 hMETIS 分割（如 AAPack、UTPlace-F 系列），使兩邊的演算法庫重新互通。從教學角度，最好的切入點仍是那三個共祖：maze routing、模擬退火、多層次分割——掌握了它們，再去讀 ASIC 與 FPGA 各自的特化版本，就能看懂整張對照矩陣。
