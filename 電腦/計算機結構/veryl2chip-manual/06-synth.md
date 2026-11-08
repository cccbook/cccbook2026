# 6. 合成：`v2c synth`

```
v2c synth [--top MODULE] [-o OUT.json] [--verilog OUT.v] FILE.veryl...
```

把 Veryl 設計展開成一張**扁平的閘級網表**：所有子模組攤平（訊號名稱如 `u_alu.sum`），if / case 變成多工器，
for 迴圈展開，function 內聯，`always_ff` 變成正反器。

## 輸出

```sh
$ v2c synth -o counter.json --verilog counter.v counter.veryl
=== Counter ===
  port input    1 i_clk
  ...
  cells: 14
    $_AND_         2
    $_DFF_PN0_     4
    $_MUX_         4
    ...
```

| 選項 | 內容 |
|---|---|
| （預設） | 埠與元件統計（類似 yosys 的 `stat`） |
| `-o OUT.json`（`--json`） | yosys JSON：`yosys -p "read_json OUT.json"` 可以讀 |
| `--verilog OUT.v` | 結構化 Verilog：iverilog 可以模擬 |
| `--top M`（`-s M`） | 合成 `M`；預設是最後一個不是 testbench 的 module |

網表用的是 yosys 的內部元件：`$_NOT_ $_AND_ $_OR_ $_XOR_ $_MUX_`（Y = S ? B : A），
正反器 `$_DFF_P_` / `$_DFF_N_`，非同步 reset `$_DFF_{P,N}{P,N}{0,1}_`，同步 reset `$_SDFF_…`。

## 最佳化做了什麼

- 常數摺疊、結構雜湊（相同的閘只留一個）、`x & !x` 之類的化簡、平衡的化簡樹。
- 證明常數節點：隨機模擬找候選，再對 16 個輸入以內的支撐集窮舉證明。
- 移除永遠是 0 的暫存器（上電為 0、從不被寫成 1）。程式 ROM 是常數時，CPU 用不到的硬體會整個消失。
- 偵測組合迴路（例如沒有完整賦值的 `always_comb`），以錯誤回報。

## 記憶體

合成時被認成記憶體的陣列（第 4 章的條件）在通用網表裡仍是正反器；到了 FPGA / ASIC 對應時，
同步讀取的會換成 block RAM / SRAM 巨集。例如 512×8 的 `SyncRam`：通用網表 12832 個元件，iCE40 上只要 1 個 `SB_RAM40_4K`。

## 確認合成是對的

- `v2c gatesim opt FILE...`：用原本的 testbench 跑合成後的網表（第 8 章）。
- 有 yosys（含 slang 前端）的話，可以對官方 `veryl build` 產生的 SystemVerilog 做形式等價證明（專案的 `veryl-eda/test.sh` 就是這樣做，第 13 章）。
