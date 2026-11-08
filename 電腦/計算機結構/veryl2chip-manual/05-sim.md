# 5. 模擬：`v2c sim`

```
v2c sim [--top MODULE] [--vcd FILE.vcd] [--max-time N] FILE.veryl...
v2c list FILE.veryl...
```

`v2c sim` 是事件驅動的模擬器（類似 Icarus Verilog）：4 態值（0 / 1 / x）、delta cycle、非阻塞賦值、時脈產生器、VCD。

## 跑哪個 module

| 情況 | 模擬的頂層 |
|---|---|
| 沒給 `--top` | **所有**帶 `#[test(...)]` 的 module，一個接一個 |
| 沒有任何 testbench | 最後宣告的 module |
| `--top M`（或 `-s M`） | 只有 `M` |

不確定檔案裡有哪些 module，用 `v2c list`：

```sh
$ v2c list counter.veryl
Counter
TestCounter  (#[test])
```

## 結果與結束碼

```sh
$ v2c sim counter.veryl
=== simulating TestCounter ===
$finish called at time 95
TestCounter: PASS
```

`$assert` 不成立時印出時間並計一次失敗：

```
ASSERTION FAILED at time 65
TestCounter: 1 failure(s)
```

| 結束碼 | 意思 |
|---|---|
| 0 | 全部通過 |
| 1 | 有斷言失敗，或檔案 / 語法 / 展開錯誤（例如 `err.veryl:2:1: parse error: ...`） |
| 2 | 命令列參數錯誤（提示 `v2c help sim`） |

所以可以直接放進腳本或 CI：`v2c sim *.veryl || exit 1`。

## 時間

`$tb::clock_gen` 的時脈週期是 10 個時間單位（`clk.next()` 前進一個週期）。
模擬在 `$finish`、或到 `--max-time`（預設 1000000）時停止；超時會印出 `simulation stopped: reached max time N`。
大設計（例如 RISC-V 跑完整個程式）若跑不完，把 `--max-time` 加大。

## 波形

```sh
v2c sim --vcd wave.vcd counter.veryl
gtkwave wave.vcd
```

有好幾個 testbench 時，每個寫一個檔：`wave_TestA.vcd`、`wave_TestB.vcd`…
波形裡有 testbench 與它底下每一層的訊號（名稱如 `dut.count`）。網頁 IDE 的波形分頁看的是同一份資料。

## 除錯技巧

- `$display("count=%d", count);` 在 `initial` 裡隨時印值。
- 先用 `--top` 單獨跑一個 testbench。
- 結果和預期不同時，先用官方 `veryl test` 跑一次對照：兩邊都錯通常是設計的問題，只有一邊錯就回報給我們。
