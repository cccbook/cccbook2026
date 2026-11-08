# 1. 認識 veryl2chip

## 它能做什麼

把一個用 Veryl 寫的數位電路設計，一路帶到「可以燒的 FPGA」或「可以送去做的晶片版圖」：

```
Veryl 原始碼
   │  v2c sim        模擬：跑 #[test] testbench，看波形
   ▼
閘級網表          v2c synth      合成：展開、最佳化成 AND / OR / XOR / MUX / 正反器
   │
   ├─► FPGA   v2c fpga       iCE40UP5K：LUT 對應 → 佈局 → 繞線 → 時序 → 位元流（iceprog 燒進 iCEBreaker）
   │
   └─► ASIC   v2c asic       標準元件對應 → 列式佈局 → 時脈樹 → 繞線 → 時序 → 功耗
                              （vlib 教學元件庫，或 SkyWater SKY130：再加 DRC 與 GDSII 版圖）

合成後的網表 → v2c gatesim   用同一個 testbench 再模擬一次，確認合成沒有改變行為
C 程式       → v2c cc        編譯給專案裡的 RISC-V SoC（也是用 Veryl 寫的）執行
```

全部工具都是這個專案自己寫的（模擬器、合成器、FPGA 佈局繞線與位元流、ASIC 後端、C 編譯器），
需要外部工具的地方只有：燒錄實體板子（`iceprog`）、選用的 nextpnr 佈局繞線，以及給開發者用的驗證工具。

## 兩種用法

| | 網頁 IDE | 命令列 `v2c` |
|---|---|---|
| 安裝 | 不用，打開網頁即可（[線上版](https://ccc-eda.github.io/veryl2chip/web/dist/index.html)） | `cargo install veryl2chip-eda` |
| 適合 | 上課、實驗、看每個階段的圖、虛擬開發板 | 自動化、大設計、整合到其他流程 |
| 能力 | 模擬、波形、合成各階段的圖、FPGA / ASIC（含 SKY130）、虛擬開發板、C 程式 | 同樣的流程，輸出檔案（JSON、Verilog、`.asc`、`.bin`、DEF、GDS、VCD） |

兩者用的是**同一份程式**（網頁裡跑的是編成 WebAssembly 的同一套 Rust 程式碼），結果相同。

## 名詞

| 名詞 | 意思 |
|---|---|
| 頂層（top） | 要模擬或合成的那個 module |
| testbench | 帶 `#[test(...)]` 屬性、用來測試設計的 module；模擬時預設跑全部 testbench，合成時預設不碰它們 |
| 網表（netlist） | 合成後由邏輯閘與正反器組成的電路 |
| LUT / LC | iCE40 FPGA 的 4 輸入查表 / 邏輯單元（LUT + 進位 + 正反器） |
| 位元流（bitstream） | 燒進 FPGA 的設定檔（`.bin`） |
| 標準元件（standard cell） | ASIC 用的現成邏輯閘版圖（NAND2、DFF…） |
| PDK | 製程設計套件：元件庫、各層金屬規則、版圖（本專案支援 SkyWater SKY130） |
| Fmax | 電路能跑的最高時脈頻率；iCEBreaker 的時脈是 12 MHz |
| DRC | 設計規則檢查：金屬寬度、間距、短路、斷路 |
| GDSII | 晶片版圖的標準檔案格式（`.gds`） |

## 這個專案裡有什麼

| 目錄 | 內容 |
|---|---|
| `veryl-sim/` | 模擬器（crate `veryl2chip-sim`） |
| `veryl-eda/` | 合成、FPGA、ASIC、C 編譯器、虛擬板引擎，以及 `v2c` 指令（crate `veryl2chip-eda`） |
| `veryl-wasm/` | 上面兩者編成 WebAssembly |
| `web/` | 網頁 IDE（`web/dist/index.html`） |
| `examples/` | 範例設計（加法器、狀態機、UART、VGA、RISC-V…）與 C 程式（`examples/c/`） |
| `tutorial/` | 從零開始的教學與虛擬實驗課 |
| `tools/` | 下載 SKY130、檢查 GDS 等小工具 |
| `manual/` | 本手冊 |
