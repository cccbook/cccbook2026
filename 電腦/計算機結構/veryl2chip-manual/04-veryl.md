# 4. 寫給 veryl2chip 的 Veryl

veryl2chip 讀的就是一般的 Veryl（用 `veryl-parser` 0.22 解析），檔案不需要特別的格式。
官方 `veryl check` 是語法與語意的標準答案；veryl2chip 的模擬器刻意比較小，它說「不支援」的東西不一定是語法錯誤。

## 一個設計的檔案

- 一次可以給好幾個 `.veryl` 檔：`v2c sim a.veryl b.veryl`，模組可以互相引用，順序不拘。
- package、enum（成員寫成 `Pkg::EnumName::Member`）、struct（第一個欄位在最高位元，和 SystemVerilog 一樣）、
  const、function、interface 與 modport、generate for / if 都可以用。
- 有 `Veryl.toml` 的 Veryl 專案也能直接用：把 `src/*.veryl` 交給 `v2c` 即可。

## testbench

testbench 是一個帶 `#[test(名稱)]` 的 module。標準寫法：

```veryl
#[test(test_x)]
module TestX {
    inst clk: $tb::clock_gen;          // 這個 inst 本身就是時脈
    inst rst: $tb::reset_gen(clk);     // 記住它用的時脈

    // ... inst dut: X (i_clk: clk, i_rst: rst, ...);

    initial {
        rst.assert();                  // 拉 reset，經過一拍
        clk.next(10);                  // 前進 10 個時脈
        $assert(dut_output == 8'd42);  // 不成立就記一次失敗
        $finish();
    }
}
```

- 不要自己寫 `var clk: clock` 再手動翻轉；用 `$tb::clock_gen`。
- 每一個 `initial` 敘述之後，模擬器都會讓組合邏輯穩定下來，所以沒有時脈的純組合電路也可以這樣測：
  設輸入、下一行就 `$assert` 輸出。
- 可用的系統函式：`$display $write $info $warning $error $fatal $assert $finish $time $clog2 $signed $unsigned $bits $random`。
- 想讓 testbench 快一點，可以用參數把設計縮小（例如計數器的寬度），教學的 Blinky 就是這樣做的。

## 支援的語法

| 模擬（`v2c sim`） | 合成（`v2c synth / fpga / asic`） |
|---|---|
| module、參數、const、port、`var`、`let`、`assign`、`always_comb`、`always_ff`（`if_reset`、同步 / 非同步 reset、正緣 / 負緣）、`if`、`case`、`switch`、`for`、`inst`、`initial`、`final` | 同左（`initial` / `final` 與 `$display` 類會被忽略） |
| package、enum、struct、一維陣列、function（不可遞迴）、generate、`import Pkg::*`、interface / modport | 同左；陣列以變數索引讀寫會變成多工器 / 解碼器 |
| 4 態值（0 / 1 / x），最多 256 bit | 常數最多 256 bit |
| | 運算子：`+ - *`、位元 / 邏輯 / 化簡、比較、移位（常數或變數）、串接、`repeat`、三元；`/ %` 合成成除法器；`**` 只限常數 |

**還不支援**：泛型 interface 埠（請指名 modport）、遞迴、`inout`、超過 256 bit 的寬度、latch
（沒有完整賦值的 `always_comb` 在合成時會被當成組合迴路回報）。

## 給合成看的寫法

- **記憶體**：陣列如果只在**一個** `always_ff` 裡以整個元素寫入、也只以整個元素讀取，就會被認成記憶體。
  讀出的資料再進暫存器（**同步讀取**）的話，FPGA 上會變成 block RAM（`SB_RAM40_4K`），vlib ASIC 會變成 SRAM 巨集；
  非同步讀取的記憶體留在邏輯裡。範例：`examples/src/sync_ram.veryl`。
- **初值**：最佳化器假設正反器上電為 0（iCE40 就是如此），從來不被寫入的暫存器會被當成常數 0 移掉。
- **頂層**：合成預設取**最後一個非 testbench** 的 module；要合成別的就加 `--top`。

## Veryl 0.22 的陷阱（`veryl check` 驗證過）

- `function` 本體裡單獨的 `<` / `>` 會讓語法分析器以為是泛型：改用 `<=` / `>=` 或 `<:` / `>:`。
- enum 成員要寫完整：`Pkg::EnumName::Member`，不是 `Pkg::Member`。
- `bit` 是保留字，不能當名稱。
- 沒有 reset 的陣列寫入，`veryl check` 會警告 `missing_reset_statement`；在那個 `always_ff` 前加 `#[allow(missing_reset_statement)]`。
- Veryl 0.22 內建的模擬器（`veryl test`）在 interface 設計上會算錯；veryl2chip 與 iverilog 的結果一致。
