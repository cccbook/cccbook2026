# B.1 PDK 檔案格式速查：Techfile、LEF/DEF、Liberty 與 SPEF

一份 PDK 由多種檔案格式組成，各司其職：有的描述製程規則、有的描述元件外觀、有的描述電氣模型。本附錄以表格搭配範例，快速比對各格式的用途、產生者與消費者。

## 總覽

| 格式 | 副檔名 | 用途 | 由誰產生 | 被誰消費 |
|---|---|---|---|---|
| Techfile | `.tf`、`.drf` | 製程層次與 DRD 規則 | 晶圓廠 | 版圖編輯器（Virtuoso）、DRD 檢查 |
| Technology LEF | `.lef` | 製程層、金屬與 via 資訊 | 晶圓廠 | P&R、萃取、時序工具 |
| Cell LEF | `.lef` | 單元的外觀、pin、遮蔽區 | 晶圓廠／單元庫廠商 | P&R、萃取工具 |
| DEF | `.def` | 設計的版圖資訊（placement/routing） | P&R 工具 | 萃取、signoff、GDS 產生 |
| Liberty | `.lib` | 單元時序／功耗／面積模型 | 單元庫廠商（特徵化） | 合成、P&R、STA |
| SPICE model card | `.spi`、`.scs` | 電晶體 SPICE 模型參數 | 晶圓廠（foundry model team） | SPICE 模擬器、特徵化 |
| SPEF | `.spef` | 寄生電阻電容網路 | 寄生萃取工具 | STA、gatesim |
| GDSII / OASIS | `.gds`、`.oas` | 最終版圖幾何資料 | 版圖工具／P&R | 光罩製作、DRC/LVS |
| Rule deck | `.svrf`、`.icv` 等 | DRC/LVS 規則集 | 晶圓廠 + EDA 廠商 | Calibre、IC Validator |
| SDC | `.sdc` | 時序約束 | 設計者／前端工具 | 合成、P&R、STA |

## Techfile（DRD 規則）

Techfile 描述製程的所有層次（layer）與其間距、線寬、包覆等設計規則（DRD, Design Rule Deck），是版圖環境的基礎。通常由晶圓廠提供，供版圖編輯器建立技術檔，並可匯出給 DRC 工具使用。

```
layer M1
  width      = 0.14
  spacing    = 0.14
  min_area   = 0.1
end
via V1
  enclosure  = 0.02
end
```

## LEF：Technology LEF 與 Cell LEF

LEF（Library Exchange Format）分兩部分。Technology LEF 描述製程金屬層、via 定義與繞線方向；Cell LEF 描述每個標準單元或硬 IP 的抽象外觀（abstract view）：邊界、pin 位置與金屬形狀。兩者皆由晶圓廠或庫廠產生，由 P&R（如本書的 veryl-eda ASIC 流程）、寄生萃取與 DEF 產生工具消費。

```
MACRO INVX1
  CLASS CORE ;
  SIZE 1.0 BY 2.7 ;
  PIN A
    DIRECTION INPUT ;
    LAYER M1 ; RECT 0.1 0.8 0.5 1.2 ;
  END
END INVX1
```

## DEF

DEF（Design Exchange Format）記錄「這顆晶片實際被擺成什麼樣」：die area、row、單元擺放（placement）、繞線（routing）與電源網路。由 P&R 工具輸出，交給寄生萃取、實體驗證與 GDS 流工具。

```
VERSION 5.8 ;
DIEAREA ( 0 0 ) ( 1000 1000 ) ;
COMPONENTS 2 ;
  - INVX1 _u1 + PLACED ( 200 270 ) N ;
END COMPONENTS
END DESIGN
```

## Liberty（.lib）

Liberty 是單元的電氣抽象模型：每個 corner 一份檔案，內含 cell 面積、pin 方向與電容、以 lookup table 表示的 delay／transition／功耗，以及時序arc。由庫廠以 SPICE 特徵化（characterization）產生，被合成、P&R 與 STA 消費。

```
library (sky130_fd_sc_hd__tt) {
  cell (INVX1) {
    area : 4.0 ;
    pin (A) { direction : input ; capacitance : 0.006 ; }
    pin (Y) {
      timing () {
        cell_rise ("delay_template") { index_1("0.1"); index_2("0.5"); values("0.12"); }
      }
    }
  }
}
```

## SPICE model card

晶圓廠量測實際元件後擬合出的電晶體模型參數（如 BSIM4 參數集），以文字形式提供 TT/SS/FF 等 corner。由 foundry 的模型團隊產生，被 SPICE 模擬器（ngspice、Spectre）與 Liberty 特徵化工具消費。本書 `v2c` ASIC 流程做 gatesim 前，支援的 PDK 即需要這類模型。

```
.MODEL nch nmos level=54 version=4.5
+ tox=4.15e-9 vth0=0.45 u0=0.025
```

## SPEF

SPEF（Standard Parasitic Exchange Format）記錄寄生萃取後的每條 net 之 R/C 值與節點連接，以電阻電容網路形式描述真實互連。由寄生萃取工具（讀取 LEF/DEF 或 GDS）產生，被 STA（含 crosstalk 分析）與 gate-level 模擬消費。

```
*D_NET net_17 0.0032
*CONN
*I _u1:Y O
*I _u2:A I
*CAP
1 _u1:Y 0.0021
*RES
1 _u1:Y _u2:A 45.0
*END
```

## GDSII / OASIS

GDSII 是流交換的業界標準版圖格式，OASIS 是其較新的壓縮繼承者。由版圖編輯器或 P&R→GDS 流工具產生，是最終交給光罩製作（mask shop）與 DRC/LVS 物理驗證的資料。

## DRC / LVS rule deck

DRC/LVS 規則集（rule deck）是晶圓廠規則與 EDA 語法的結合：以 Mentor Calibre 的 SVRF（Standard Verification Rule Format）或 Synopsys IC Validator 的 ICV 格式撰寫，內含層次運算（AND/OR/NOT/SIZE）與檢查語句。由晶圓廠與 EDA 廠商共同維護，僅被對應的驗證工具消費。概念上長這樣：

```
LAYER m1 = M1 ;
WIDTH m1 < 0.14 ERROR "M1.W.1" ;
```

## SDC

SDC（Synopsys Design Constraints）以 Tcl 語法描述時序意圖：clock 定義、輸入輸出延遲、false path 等。由設計者（或前端工具從 RTL 註解產生）撰寫，被合成、P&R 與 STA 沿用，確保各階段對「時間」的認知一致。

```
create_clock -name clk -period 10.0 [get_ports clk]
set_input_delay 2.0 -clock clk [all_inputs]
set_output_delay 2.0 -clock clk [all_outputs]
```

## 小結

理解這些格式的分工，就能看懂一條 ASIC 流程：RTL 經合成讀 Liberty 變成 netlist；P&R 讀 LEF/SDC 產出 DEF；萃取工具由 DEF 產出 SPEF；STA 讀 SPEF 做 signoff；最後 DEF + LEF 轉成 GDS 交給 DRC/LVS rule deck 驗證並送 tapeout。
