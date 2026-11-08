# 8. 合成後模擬：`v2c gatesim`

```
v2c gatesim opt|ice40|ecp5|asic|sky130 [--top MODULE] FILE.veryl...
```

合成器會不會把電路做錯？最直接的檢查：**用同一個 testbench**，把被測的 module 換成它合成後的網表，再模擬一次。

```sh
$ v2c gatesim ice40 counter.veryl
=== simulating TestCounter ===
TestCounter: PASS
gate-level simulation: Counter as 10 cells (ice40)
```

| 網表 | 內容 |
|---|---|
| `opt` | 最佳化後的通用閘（`v2c synth` 的結果） |
| `ice40` | iCE40 對應後：`SB_LUT4`、`SB_CARRY`、`SB_DFF*`、`SB_RAM40_4K` |
| `ecp5` | ECP5 對應後：`LUT4`、`CCU2C`、`TRELLIS_FF` |
| `asic` | vlib 標準元件（含 SRAM 巨集） |
| `sky130` | SkyWater SKY130 標準元件 |

- 被換掉的是 `--top`（預設：最後一個不是 testbench 的 module）；檔案裡所有 testbench 照常執行。
- testbench 若用不同參數實例化設計，每組參數各合成一份網表。
- 閘級模型保留 x 的傳遞（LUT 用多工器樹表示），所以未初始化的值會像 RTL 一樣是 x。
- 結果和 `v2c sim` 不同，表示合成有問題（或設計依賴了合成器假設不成立的東西，例如未初始化的暫存器——最佳化器假設上電為 0）。

網頁 IDE 的「模擬對象」選單（RTL / 閘級：通用閘 / iCE40 / 標準元件）做的是同一件事；✔ 全面驗證一次跑完 RTL 與三種網表並比較。
