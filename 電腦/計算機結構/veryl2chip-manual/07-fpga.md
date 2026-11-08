# 7. FPGA：`v2c fpga`

```
v2c fpga [--top MODULE] [--pcf PINS.pcf] [--asc OUT.asc] [--bin OUT.bin]
         [--pnr veryl|nextpnr] [--seed N] [--no-timing-driven] [--program PROG.bin]
         [-o OUT.json] [--verilog OUT.v] [-v] FILE.veryl...
```

目標晶片是 Lattice **iCE40UP5K-SG48**（iCEBreaker 開發板上的那顆：5280 個邏輯單元、30 塊 4 Kbit block RAM、12 MHz 時脈）。

## 步驟

1. **對應**（一定做）：全加器的進位變成 `SB_CARRY` 進位鏈，其他邏輯以 4 輸入查表 `SB_LUT4` 覆蓋，
   正反器變成 `SB_DFF*`，同步讀取的記憶體變成 `SB_RAM40_4K`。印出元件統計；`-o` / `--verilog` 寫出對應後的網表。
2. **佈局繞線**（給了 `--asc` 或 `--bin` 才做）：把元件放到晶片上的位置並連線。
3. **位元流**：`--bin` 寫出可以燒的檔案。

## 兩種佈局繞線工具

| | `--pnr nextpnr`（預設） | `--pnr veryl` |
|---|---|---|
| 是誰 | 外部的 nextpnr-ice40 + icepack | 本專案自己的佈局繞線與位元流 |
| 需要 | OSS CAD Suite | IceStorm 的 `chipdb-5k.txt`（`VERYL_EDA_CHIPDB`） |
| 時序不夠 12 MHz | 失敗（nextpnr 的行為） | 照樣產生，印出 Fmax，由你判斷 |
| 其他 | | 時序導向（`--no-timing-driven` 關閉）、`--seed`、`-v` 印出關鍵路徑、粗估功耗 |

自己的佈局繞線產生的 `.bin` 與 icepack 逐位元組相同，並且用 IceStorm 的 `icebox_vlog` 把繞好的位元流轉回電路、
和網表逐週期比對過（第 13 章）。

```sh
$ v2c fpga --pnr veryl --pcf counter.pcf --bin counter.bin counter.veryl
  veryl pnr: 6 LCs, 52 routing pips, 0.2s
  power: 0.199 mW at 122.1 MHz = ...
  timing: critical path 8.19 ns, Fmax 122.10 MHz (wirelength-only pass 122.10 MHz)
wrote counter.bin
```

`--asc OUT.asc` 寫出 IceStorm 的文字格式（自己的佈局繞線會在旁邊一起寫 `.pcf`）；只給 `--bin` 時 `.asc` 放在暫存目錄。

## 腳位檔（`.pcf`）

每一行 `set_io 埠名 腳號`，向量埠寫 `o_led[0]`。`-nowarn` 表示設計沒用到這支腳也沒關係。
iCEBreaker 常用的腳（`tutorial/icebreaker.pcf` 有完整清單）：

| 腳 | 用途 |
|---|---|
| 35 | 12 MHz 時脈 |
| 10 | 板上按鈕 BTN_N（按下 = 0，拿來當 reset 剛好） |
| 11、37 | 板上紅 / 綠 LED（低電位亮） |
| 26、27、25、23、21 | 擴充板 LED1–LED5（高電位亮） |
| 20、19、18 | 擴充板 BTN1–BTN3（按下 = 1） |
| 6、9 | 序列埠 RX（進 FPGA）、TX（出 FPGA） |
| PMOD1A：4 2 47 45 3 48 46 44；PMOD1B：43 38 34 31 42 36 32 28 | 外接模組 |

沒有給 `--pcf` 時腳位由工具自己決定，位元流仍然可以做，但燒進板子不會接到你要的地方。

## 時序

`Fmax` 是電路能跑的最高頻率，要**高於 12 MHz** 才能在 iCEBreaker 上正常工作。不夠時：

- 把長的組合邏輯切成兩拍（加暫存器）；
- 試試不同的 `--seed`，或另一個佈局繞線工具；
- `-v` 看關鍵路徑經過哪些元件與連線。

## 燒錄

```sh
iceprog counter.bin
```

沒有板子：網頁 IDE 的 ⚡ 虛擬板跑的就是這個位元流解碼回來的電路（第 12 章），也可以把任何 iCE40UP5K 的 `.bin` 拖到虛擬板上。

## 把程式放進 block RAM（`--program`）

對於程式存在 block RAM 的 CPU（例如本專案的 `RvBoard`，第 10 章），`--program PROG.bin` 從位址 0 把二進位檔填進記憶體：

```sh
v2c cc -o hello.bin examples/c/hello.c
v2c fpga --top RvBoard --pnr veryl --pcf examples/rvsoc.pcf --program hello.bin --bin soc.bin \
    examples/src/rv32i.veryl examples/src/sync_ram.veryl examples/src/uart.veryl examples/src/rvsoc.veryl
iceprog soc.bin
```

整顆 SoC（約 4200 個邏輯單元、20 塊 block RAM）的佈局繞線約需一分鐘，Fmax 約 13–14 MHz。

只換程式的話不需要重新合成與佈局繞線（網頁 IDE 換 C 程式時就是直接改寫位元流裡的記憶體內容）。

## Lattice ECP5（`--arch ecp5`）

```
v2c fpga --arch ecp5 [--device 12k|25k|45k|85k] [--package CABGA381] [--lpf PINS.lpf]
         [--config OUT.config] [--bit OUT.bit] [--seed N] [-o OUT.json] [-v] FILE.veryl...
```

ECP5 是比 iCE40 大得多的 FPGA（25F 約 2.4 萬、85F 約 8.4 萬個 LUT，還有 SDRAM 介面的開發板，例如開源的 **ULX3S**）。
對應由 `v2c` 做（`LUT4`、進位鏈 `CCU2C`、正反器 `TRELLIS_FF`），佈局繞線與位元流交給 OSS CAD Suite 的 **nextpnr-ecp5** 與 **ecppack**：

```sh
$ v2c fpga --arch ecp5 --bit counter.bit counter.veryl
=== Counter ===
  ...
  cells: 9
    LUT4           5
    TRELLIS_FF     4
  TRELLIS_IO:       7/    365     1%
  TRELLIS_FF:       4/  83640     0%
  TRELLIS_COMB:       6/  83640     0%
  Max frequency for clock 'i_clk$TRELLIS_IO_IN': 371.89 MHz (PASS at 12.00 MHz)
wrote counter.bit
```

`TRELLIS_COMB` 是 LUT 加上進位鏈的用量；`PASS at 12.00 MHz` 是 nextpnr 預設的時脈目標，要指定別的頻率，在 `.lpf` 裡寫
`FREQUENCY PORT "i_clk" 25 MHZ;`。

- 預設 `--device 85k --package CABGA381`（ULX3S 85F）；其他型號用 `--device 12k|25k|45k`。
- 腳位檔是 Lattice 的 `.lpf`：`LOCATE COMP "o_led[0]" SITE "B2";`、`IOBUF PORT "o_led[0]" IO_TYPE=LVCMOS33;`。
  沒給 `--lpf` 時 nextpnr 自己放 IO。
- `--config` 是繞好的文字設定（Project Trellis 格式），`--bit` 是位元流，用 `openFPGALoader -b ulx3s counter.bit` 燒錄。
- `v2c gatesim ecp5` 用原本的 testbench 跑 ECP5 網表（第 8 章）。
- 和 iCE40 不同：reset 值是 1 的正反器，上電時就是 1（iCE40 全部上電為 0）。
- 目前還沒有：block RAM（記憶體會變成正反器，所以 RvBoard 的 8 KB 記憶體還放不進去）、乘法器、自己的 ECP5 佈局繞線、虛擬板。

## 限制

iCE40 只支援 UP5K；沒有 SPRAM（`SB_SPRAM256KA`）、PLL、`inout`；非同步讀取的記憶體不會變成 block RAM；
自己的佈局繞線不做 LUT 輸入腳交換。
