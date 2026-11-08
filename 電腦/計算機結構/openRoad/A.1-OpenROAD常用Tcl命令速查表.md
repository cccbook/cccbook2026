# A.1 OpenROAD 常用 Tcl 命令速查表

OpenROAD 以 Tcl script 驅動，無論是直接下指令（`openroad -no_init` 進入互動模式）或透過 OpenROAD Flow Scripts（ORFS）跑完整流程，底層都是同一組命令。本章按設計流程階段分類整理常用命令，供撰寫 script 與除錯時快速查閱。

## 輸入與設計讀取

| 命令 | 用途說明 |
|---|---|
| `read_lef` | 讀入 LEF 檔（technology LEF 與 cell LEF），建立 tech 與 library 資訊。 |
| `read_liberty` | 讀入 Liberty (.lib) 時序庫，STA 與 resizer 都需要。 |
| `read_verilog` | 讀入合成後的 gate-level netlist。 |
| `link_design` | 將 netlist 與 LEF/Liberty 連結，建立完整 instance/net 階層。 |
| `read_def` | 讀入 DEF 檔（floorplan 或上一階段輸出的擺置/繞線結果）。 |
| `read_sdc` | 讀入 SDC 時序限制檔。 |
| `read_db` | 讀入 OpenDB 二進位資料庫，可跳過前面的讀檔步驟直接恢復狀態。 |
| `read_spef` | 讀入 SPEF 寄生參數檔，用於精確的 post-route STA。 |

## Floorplan

| 命令 | 用途說明 |
|---|---|
| `initialize_floorplan` | 依目標 utilization 與 site 建立初始 die/core 區域。 |
| `make_tracks` | 產生各金屬層的 routing track。 |
| `place_pins` | 自動擺放 I/O pin（IO planner）。 |
| `insert_tiecells` | 插入 tie cell 連接常數 0/1 訊號。 |
| `tapcell` | 插入 tapcell / well-tap 以滿足 latch-up 規則。 |
| `pdngen` | 產生 power grid（電源網絡）。 |
| `add_ndr` | 定義非預設繞線規則（NDR），常用於時脈網路雙倍間距。 |

## Placement

| 命令 | 用途說明 |
|---|---|
| `global_placement` | 執行 global placement（RePlAce 演算法）。 |
| `estimate_parasitics` | 以 placement 估計方式（如 Steiner tree）計算寄生參數供 STA。 |
| `set_wire_rc` | 設定估寄生用的單位長度電阻電容，搭配 `estimate_parasitics` 使用。 |
| `repair_timing` | 修補 setup/hold 違規：可自動 insert buffer、resize、gate clone 等。 |
| `detail_placement` | 執行 detailed placement（legalization，將 cell 對齊 site 並去除重疊）。 |
| `check_placement` | 檢查 placement 合法性（重疊、pin access、site 對齊等）。 |

## Clock Tree Synthesis

| 命令 | 用途說明 |
|---|---|
| `clock_tree_synthesis` | 執行 CTS，插入 clock buffer/inverter 樹。 |
| `set_clock_tree_options` | 設定 CTS 選項，如 buffer cell、最大 fanout、skew target。 |
| `report_clock_skew` | 回報各 clock group 的 skew。 |
| `repair_clock_nets` | 修補時脈網路的最大長度/延遲違規（插 buffer）。 |
| `set_propagated_clock` | 將 clock 設為 propagated mode，用於 CTS 之後的 STA。 |

## Routing

| 命令 | 用途說明 |
|---|---|
| `global_route` | 執行 global routing，決定每條 net 走哪些層與 gcell 路徑。 |
| `set_routing_layers` | 限制 signal routing 可用的金屬層範圍。 |
| `set_macro_extension` | 設定 macro 週邊的 keepout/擴展繞線區。 |
| `detail_route` | 執行 detailed routing（TritonRoute），實際在 track 上繞線並處理 DRC。 |
| `repair_pdn_vias` | 修補 power grid 中不足的 via 疊層。 |
| `detailed_route_debug` | 開啟 detailed routing 除錯介面，觀察違規位置。 |

## 寄生萃取與 STA

| 命令 | 用途說明 |
|---|---|
| `define_process_corner` | 定義 process corner（如 `-ext_model_index`），供萃取使用。 |
| `extract_parasitics` | 於 post-route 階段執行寄生萃取，產生實際 RC。 |
| `write_spef` | 將萃取結果寫出為 SPEF 檔。 |
| `report_checks` | OpenSTA 核心報告：列出 violation path 細節（預設 setup）。 |
| `report_checks -path_delay min` | 回報 hold violation path。 |
| `report_checks -path_delay max_min` | 同時回報 setup 與 hold。 |
| `report_tns` | 回報總負 Slack（Total Negative Slack）。 |
| `report_wns` | 回報最差負 Slack（Worst Negative Slack）。 |
| `report_worst_slack` | 回報最差 slack 值（setup 或 hold）。 |
| `report_design_area` | 回報設計總面積與 utilization。 |
| `report_power` | 回報功耗估計。 |
| `report_drc` | 回報 detailed route 後的 DRC 違規數量與位置。 |
| `check_antennas` | 檢查 antenna 違規。 |

## Resizer 與最佳化

| 命令 | 用途說明 |
|---|---|
| `set_dont_use` | 指定 resizer/CTS 不得使用的 cell（如高功耗、特殊 cell）。 |
| `estimate_parasitics -placement` | 以 placement 資訊估寄生，是 resize/repair 前的標準前置。 |
| `repair_design` | 修復 max capacitance / max slew / max fanout 違規。 |
| `repair_timing -setup` | 專注修補 setup violation。 |
| `repair_timing -hold` | 專注修補 hold violation。 |
| `repair_tie_fanout` | 修補 tie cell 連接的 fanout。 |

## 輸出

| 命令 | 用途說明 |
|---|---|
| `write_def` | 輸出 DEF 檔（可帶版本參數如 `write_def -version 5.8`）。 |
| `write_verilog` | 輸出最佳化後的 netlist。 |
| `write_db` | 將目前狀態存成 OpenDB 二進位檔，利於快速重載。 |
| `write_guides` | 輸出 global routing guides。 |
| `write_cdl` | 輸出 CDL 網表，供 LVS 使用。 |

## ORFS 常用 make 目標

ORFS 透過 GNU Make 包裝 OpenROAD，常用目標如下：

| 目標 | 用途說明 |
|---|---|
| `make` | 執行從 synthesis 到 DRC/LVS 完成的全部流程。 |
| `make DESIGN_CONFIG=...` | 指定設計設定檔執行流程。 |
| `make floorplan` / `make place` / `make cts` / `make route` | 單獨執行某個 stage。 |
| `make gui_floorplan` 等 | 開啟 GUI 並載入該 stage 結果。 |
| `make clean_all` | 清除該設計所有產出。 |
| `make print-*` | 查詢變數內容，如 `make print-VAR`。 |

## 使用小提示

- 開頭先 `read_lef` + `read_liberty`，順序不可顛倒：沒有 tech LEF 無法 `link_design`。
- CTS 之後記得 `set_propagated_clock`，否則 STA 仍用 ideal clock 估延遲，結果會過於樂觀。
- `estimate_parasitics` 與 `extract_parasitics` 分屬 pre-route 估計與 post-route 精算，signoff 一律用後者。
- GUI 除錯可啟動 `openroad -gui`，載入 DEF/db 後可檢視 placement、routing 與 DRC 標記。
