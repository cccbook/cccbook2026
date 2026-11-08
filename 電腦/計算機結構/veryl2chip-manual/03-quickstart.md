# 3. 五分鐘上手

用一個 4 位元計數器把整條流程走一遍。建一個目錄，放兩個檔案。

`counter.veryl`：設計與它的 testbench

```veryl
module Counter (
    i_clk  : input  clock   ,
    i_rst  : input  reset   ,
    i_en   : input  logic   ,
    o_count: output logic<4>,
) {
    var count: logic<4>;

    always_ff {
        if_reset {
            count = 0;
        } else if i_en {
            count += 1;
        }
    }

    assign o_count = count;
}

#[test(test_counter)]
module TestCounter {
    inst clk: $tb::clock_gen;
    inst rst: $tb::reset_gen(clk);

    var en   : logic   ;
    var count: logic<4>;

    inst dut: Counter (
        i_clk  : clk  ,
        i_rst  : rst  ,
        i_en   : en   ,
        o_count: count,
    );

    initial {
        en = 1;
        rst.assert();
        clk.next(5);
        $assert(count == 4'd5);
        en = 0;
        clk.next(3);
        $assert(count == 4'd5);
        $finish();
    }
}
```

`counter.pcf`：腳位（iCEBreaker：12 MHz 時脈、板上按鈕當 reset、擴充板的 BTN1 當 enable、LED1–4 顯示計數）

```
set_io i_clk 35
set_io i_rst 10
set_io i_en 20
set_io o_count[0] 26
set_io o_count[1] 27
set_io o_count[2] 25
set_io o_count[3] 23
```

## 1. 模擬

```sh
$ v2c sim counter.veryl
=== simulating TestCounter ===
$finish called at time 95
TestCounter: PASS
```

`v2c sim --vcd wave.vcd counter.veryl` 另外寫出波形，可用 GTKWave 開。

## 2. 合成

```sh
$ v2c synth -o counter.json --verilog counter.v counter.veryl
=== Counter ===
  port input    1 i_clk
  port input    1 i_rst
  port input    1 i_en
  port output   4 o_count
  cells: 14
    $_AND_         2
    $_DFF_PN0_     4
    $_MUX_         4
    $_NOT_         1
    $_XOR_         3
```

合成器自動挑了最後一個不是 testbench 的 module（`Counter`）。

## 3. FPGA 位元流

```sh
$ v2c fpga --pnr veryl --pcf counter.pcf --bin counter.bin counter.veryl
  cells: 10
    SB_DFFR        4
    SB_LUT4        6
  veryl pnr: 6 LCs, 52 routing pips, 0.2s
  timing: critical path 8.19 ns, Fmax 122.10 MHz
wrote counter.bin
$ iceprog counter.bin          # 插上 iCEBreaker 才需要
```

Fmax 122 MHz 遠高於板子的 12 MHz，可以放心燒。沒有板子的話，用網頁 IDE 的虛擬開發板（第 12 章）。

## 4. 合成後再模擬一次

```sh
$ v2c gatesim ice40 counter.veryl
TestCounter: PASS
gate-level simulation: Counter as 10 cells (ice40)
```

同一個 testbench 跑在合成後的 iCE40 網表上，結果一樣，表示合成沒有改變行為。

## 5. ASIC

```sh
$ v2c asic counter.veryl                         # 教學用的 vlib 元件庫
$ v2c asic --pdk sky130 --def counter.def --gds counter.gds counter.veryl
...
asic: DRC 1999 shapes: 0 shorts, 0 spacing, 0 min-area, 0 opens; 11 taps (0 sites too far)
timing: critical path 1.339 ns, Fmax 747.0 MHz
wrote counter.gds (83834 bytes: 62 cell instances, 555 shapes, 7 labels)
wrote counter.def
```

第二行用的是真實的開源製程 SkyWater SKY130：`counter.gds` 是通過設計規則檢查的晶片版圖，可以用 KLayout 打開來看（第 9 章）。

## 在網頁上做同樣的事

打開 IDE，在歡迎頁按「＋ 新專案」（或檔案區的 ＋ 新增檔案），貼上 `counter.veryl`：

- ▶ **測試**：跑 testbench，下方面板顯示結果與波形。
- 標題列的後端選單選 **FPGA** 或 **ASIC · vlib / ASIC · SKY130**，階段選單選要看的階段（③ 最佳化、⑤ 佈局、⑥ 繞線…）。
- ⚡ **虛擬板**：燒進畫出來的 iCEBreaker，按住 BTN1 看 LED 數上去。
