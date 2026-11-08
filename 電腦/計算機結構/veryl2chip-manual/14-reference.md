# 14. 參考

## `v2c` 指令總表

```
v2c <子指令> [選項] FILE.veryl...
```

`v2c help <子指令>` 或 `v2c <子指令> -h` 顯示說明。成功的結束碼是 0，失敗（斷言、語法、合成錯誤）是 1，選項錯誤是 2。

| 子指令 | 作用 | 章 |
|---|---|---|
| `sim`（別名 `test`） | 執行 testbench | 5 |
| `list` | 列出模組，標出 `#[test]` | 5 |
| `synth` | 合成成閘級網表 | 6 |
| `fpga` | iCE40UP5K（預設）或 ECP5（`--arch ecp5`）：對應、佈局繞線、位元流 | 7 |
| `gatesim` | 在合成後的網表上跑 testbench | 8 |
| `asic` | 標準元件流程（vlib / SKY130） | 9 |
| `cc` | 編譯 C（或組譯 `.s`）給 RISC-V SoC，可直接執行 | 10 |
| `pdk` | 檢查完整的 SKY130 檔案 | 9 |
| `version` | 版本 | |
| `help` | 說明 | |

### 共通

| 選項 | 子指令 | 內容 |
|---|---|---|
| `--top M`、`-s M` | sim、synth、fpga、gatesim、asic | 頂層模組。sim 預設全部 `#[test]`；其他預設最後一個不是 testbench 的 module |
| `FILE.veryl...` | 全部 | 可以給多個檔案，順序不重要 |

### `v2c sim`

| 選項 | 內容 |
|---|---|
| `--vcd F.vcd` | 波形（有多個 testbench 時每個一個檔：`F_<top>.vcd`） |
| `--max-time N` | 模擬時間上限（預設 1000000） |

結束碼：0 通過；1 有 `$assert` 失敗，或原始碼錯誤；2 選項錯誤。

### `v2c synth`

| 選項 | 內容 |
|---|---|
| `-o F.json`、`--json F.json` | yosys JSON |
| `--verilog F.v` | 結構化 Verilog |

### `v2c fpga`

| 選項 | 內容 |
|---|---|
| `--pcf F.pcf` | 腳位檔 |
| `--asc F.asc` | 繞好的設定（IceStorm 文字格式） |
| `--bin F.bin` | 位元流 |
| `--pnr veryl\|nextpnr` | 佈局繞線工具（預設 nextpnr） |
| `--seed N` | 佈局種子 |
| `--no-timing-driven` | 只看線長（自己的佈局繞線） |
| `--program P.bin` | 把程式放進 block RAM |
| `-o F.json`、`--verilog F.v` | 對應後的網表 |
| `-v` | 關鍵路徑細節 |
| `--device up5k --package sg48` | 預設值（iCE40 目前只支援這個） |
| `--arch ice40\|ecp5` | 目標 FPGA（預設 ice40） |
| `--lpf F.lpf`、`--config F.config`、`--bit F.bit` | ECP5 的腳位檔、繞好的設定、位元流（nextpnr-ecp5 + ecppack） |
| `--device 12k\|25k\|45k\|85k --package CABGA381` | ECP5 的型號（預設 85k、CABGA381） |

### `v2c gatesim opt|ice40|ecp5|asic|sky130`

只有 `--top`。

### `v2c asic`

| 選項 | 內容 |
|---|---|
| `--pdk vlib\|sky130\|sky130:DIR` | 元件庫（預設 vlib） |
| `--seed N` | 佈局種子 |
| `--verilog F.v` | 標準元件網表（含元件模型） |
| `--def F.def` | DEF |
| `--gds F.gds` | GDSII（SKY130） |
| `--map-only` | 只做元件對應 |
| `-v` | 關鍵路徑、DRC 違規例子 |

### `v2c cc PROG.c|PROG.s`

| 選項 | 內容 |
|---|---|
| `-o P.bin` | 二進位映像檔 |
| `-S P.s` | 組合語言 |
| `-L P.lst` | 列表 |
| `--run [N]` | 在指令集模擬器上執行（預設最多 1000 萬個指令） |
| `--mem BYTES` | RAM 大小（預設 8192） |

### `v2c pdk [check] [DIR]`

DIR 預設依序找 `$VERYL_EDA_SKY130`、`~/sky130hd`。

## 舊指令

`veryl-sim` 與 `veryl-eda` 兩個指令仍然存在，`v2c` 的子指令只是幫它們加上對應的旗標：

| `v2c` | 舊指令 |
|---|---|
| `v2c sim ...` | `veryl-sim ...` |
| `v2c synth ...` | `veryl-eda ...` |
| `v2c fpga ...` | `veryl-eda --ice40 ...` |
| `v2c fpga --arch ecp5 ...` | `veryl-eda --ecp5 ...` |
| `v2c asic ...` | `veryl-eda --asic ...` |
| `v2c gatesim K ...` | `veryl-eda --gatesim K ...` |
| `v2c cc P.c ...` | `veryl-eda --cc P.c ...` |
| `v2c pdk` | `veryl-eda --pdk-check` |

## 環境變數

| 變數 | 用途 |
|---|---|
| `VERYL_EDA_CHIPDB` | IceStorm `chipdb-5k.txt`（`--pnr veryl`）；沒設定時找 OSS CAD Suite 的 `share/icebox/` |
| `VERYL_EDA_SKY130` | 完整 SKY130 hd 檔案的目錄（`v2c pdk`） |
| `VERYL_EDA_PROFILE` | 印出 ASIC 各步驟耗時與細部繞線每輪的衝突數 |
| `YOSYS_SLANG`、`YOSYS`、`GDS_PY`、`OUT` | `veryl-eda/test.sh` 用（第 13 章） |

## 檔案格式

| 副檔名 | 是什麼 | 誰產生 / 誰讀 |
|---|---|---|
| `.veryl` | Veryl 原始碼 | 你 |
| `.pcf` | 腳位：`set_io [-nowarn] 埠 腳號` | 你；`fpga --pcf`、虛擬板 |
| `.vcd` | 波形 | `sim --vcd`；GTKWave、IDE |
| `.json` | yosys JSON 網表 | `synth -o`、`fpga -o`；yosys |
| `.v` | 結構化 Verilog | `--verilog`；iverilog、yosys |
| `.asc` | iCE40 設定（文字） | `fpga --asc`；IceStorm 工具 |
| `.bin` | iCE40 位元流 | `fpga --bin`；iceprog、虛擬板 |
| `.lpf` | ECP5 腳位 | 你；`fpga --arch ecp5 --lpf` |
| `.config`、`.bit` | ECP5 繞好的設定、位元流 | `fpga --arch ecp5`；ecppack、openFPGALoader |
| `.def` | 佈局繞線 | `asic --def`；OpenROAD、KLayout |
| `.gds` | 晶片版圖 | `asic --gds`；KLayout、Magic |
| `.c`、`.s` | RISC-V 程式 | 你；`cc` |
| `.bin`（程式） | 從位址 0 開始的記憶體映像 | `cc -o`；`fpga --program`、虛擬板 |
| `.lab.json` | 分享的實驗 | IDE |

## RvSoc 記憶體映射

| 位址 | 名稱 | 說明 |
|---|---|---|
| `0x0000_0000`–`0x0000_1FFF` | RAM | 8 KB |
| `0x1000_0000` | `LED` | 8 位元輸出 |
| `0x1000_0004` | `BUTTONS` / `SWITCHES` | bit 2..0 按鈕，bit 15..8 開關 |
| `0x1000_0008` | `UART_DATA` | 送出 / 收到的位元組 |
| `0x1000_000C` | `UART_STATUS` | bit 0 傳送中，bit 1 收到 |
| `0x1000_0010` | `TIMER` / `MTIME` | 時脈計數（12 MHz） |
| `0x1000_0018` | `MTIMECMP` | 計時器中斷比較值 |
| `0x1000_0020` | `MSIP` | 軟體中斷 |
| `0x1000_2000` / `4000` / `6000` | `VGA_TEXT` / `VGA_FONT` / `VGA_COLOR` | VGA 文字模式（`RvVgaBoard`） |

## 疑難排解

| 現象 | 原因與解法 |
|---|---|
| `not supported` | 本專案沒支援的語法（第 4 章），不一定是語法錯誤；用官方 `veryl check` 確認 |
| `expected …` 之類的解析錯誤出現在 function 裡的 `<` / `>` | Veryl 0.22 的已知問題：function 內用 `<=`、`>=`、`<:`、`>:` |
| 測試沒有跑 | module 前面沒有 `#[test(名稱)]`；`v2c list` 看哪些是 testbench |
| 模擬永遠不結束 | testbench 沒有結束點；用 `clk.next(n)` 控制，或 `--max-time` |
| `combinational loop` | `always_comb` 裡某個訊號沒有在每條路徑都賦值，或真的有迴路 |
| 合成後少了一大堆電路 | 最佳化器移除了不影響輸出的邏輯，或永遠是 0 的暫存器；確認輸出埠真的用到它們 |
| gatesim 與 sim 結果不同 | 設計依賴未初始化的值，或合成器的錯誤（請回報） |
| `no chipdb` / 找不到 `chipdb-5k.txt` | 設定 `VERYL_EDA_CHIPDB`，或裝 OSS CAD Suite；或改用 `--pnr nextpnr` |
| nextpnr 因時序失敗 | 設計太慢（第 7 章）；`--pnr veryl` 一樣會產生並印出 Fmax |
| ASIC 很慢 | 大記憶體在 SKY130 變成正反器；用 `--map-only` 只拿網表，或改用 vlib |
| `v2c` 找不到 | `cargo install veryl2chip-eda`，或把 `veryl-eda/target/release` 加進 `PATH` |
| 虛擬板的設計跑得比真板子好 | 虛擬板不模擬時序違規與按鈕彈跳（第 12 章） |
