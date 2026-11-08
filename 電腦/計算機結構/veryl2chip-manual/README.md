# veryl2chip 使用手冊

veryl2chip 是給 [Veryl](https://veryl-lang.org/) 硬體描述語言用的一整套 EDA 工具：
從寫好的 Veryl 程式開始，可以**模擬**、**合成**、做成 **FPGA 位元流**燒進 iCEBreaker 開發板，
也可以走 **ASIC 流程**一路做到通過設計規則檢查的 **GDSII 晶片版圖**（SkyWater SKY130 開源製程）。
全部用 Rust 寫成，可以在命令列用，也可以直接在瀏覽器裡用（不用安裝）。

這本手冊講「怎麼用」。命令列一律使用 `v2c` 指令。

## 目錄

| 章 | 內容 |
|---|---|
| [1. 認識 veryl2chip](01-intro.md) | 能做什麼、兩種用法、整條流程一覽 |
| [2. 安裝](02-install.md) | 線上版、`cargo install`、從原始碼建置、外部工具、環境變數 |
| [3. 五分鐘上手](03-quickstart.md) | 一個計數器：模擬 → 合成 → FPGA → ASIC |
| [4. 寫給 veryl2chip 的 Veryl](04-veryl.md) | testbench 的寫法、支援的語法、常見陷阱 |
| [5. 模擬：`v2c sim`](05-sim.md) | 頂層選擇、斷言、波形、結束碼 |
| [6. 合成：`v2c synth`](06-synth.md) | 閘級網表、統計、yosys JSON / Verilog、最佳化與 block RAM |
| [7. FPGA：`v2c fpga`](07-fpga.md) | iCE40 對應、腳位檔、佈局繞線、時序、位元流、燒錄 |
| [8. 合成後模擬：`v2c gatesim`](08-gatesim.md) | 用同一個 testbench 檢查合成結果 |
| [9. ASIC：`v2c asic`](09-asic.md) | vlib 與 SkyWater SKY130、DEF、DRC、GDSII、用 KLayout 看版圖 |
| [10. RISC-V 與 C：`v2c cc`](10-riscv-c.md) | 自己的 RISC-V SoC、C 編譯器、執行期函式庫、中斷與多執行緒 |
| [11. 網頁 IDE](11-ide.md) | 專案、編輯器、測試、合成各階段、網址參數 |
| [12. 虛擬開發板](12-board.md) | 三種模式、周邊、麵包板、分享實驗 |
| [13. 驗證與開發](13-develop.md) | 專案的測試、形式驗證、給想改程式的人 |
| [14. 參考](14-reference.md) | `v2c` 指令總表、環境變數、記憶體映射、疑難排解 |

## 其他文件

- 從零開始的教學（給第一次寫硬體的人）：[`tutorial/README.tw.md`](../tutorial/README.tw.md)
- 虛擬實驗課講義（不用買板子）：[`tutorial/labs.tw.md`](../tutorial/labs.tw.md)
- 各版本的歷史：[`history.md`](../history.md)
- 實作細節：[`veryl-sim/README.tw.md`](../veryl-sim/README.tw.md)、[`veryl-eda/README.tw.md`](../veryl-eda/README.tw.md)

本手冊對應 veryl2chip 2.1 起（有 `v2c` 指令的版本）。
