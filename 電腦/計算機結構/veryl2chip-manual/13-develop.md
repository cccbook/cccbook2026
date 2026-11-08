# 13. 驗證與開發

這一章給想確認工具可信度、或想修改 veryl2chip 本身的人。

## 怎麼知道工具是對的

| 檢查 | 證明什麼 | 在哪裡 |
|---|---|---|
| RTL 模擬 vs 官方 | `v2c sim` 的語意與官方 `veryl test` / iverilog 一致 | 範例的 testbench |
| 閘級模擬 | 同一個 testbench 在通用閘、iCE40、vlib、SKY130 網表上都通過 | `cargo test`、`v2c gatesim` |
| **形式等價** | 合成後的網表與官方 `veryl build` 產生的 SystemVerilog **數學上等價**（組合電路完整證明；循序電路 k-induction 或有界檢查） | `veryl-eda/test.sh`（yosys + slang） |
| SKY130 網表 | yosys 用 PDK 的 Liberty 函式讀元件，與 RTL 等價 | `veryl-eda/test.sh` |
| 位元流 | 自己的佈局繞線產生的 `.asc`，用 IceStorm 的 `icebox_vlog` 轉回電路，與網表隨機輸入逐週期比對；`.bin` 與 icepack 逐位元組相同 | `fpga/pnr_test.sh`、`fpga/cosim.py` |
| FPGA 流程 | RISC-V SoC 從對應後的網表、從繞好的位元流各模擬一次 | `fpga/flow.sh` |
| 版圖 | DRC 0 違規；KLayout 讀回 GDS，檢查元件數、不重疊、寬度與間距 | `asic` 流程、`tools/gds_check.py` |
| C 編譯器 | `src/rv/tests/*.c` 的輸出與主機的 `cc` 相同；RISC-V 程式的結果與 spike 相同 | `cargo test` |
| 虛擬板 | 板子引擎與 netsim 一致；位元流解碼與 nextpnr 的結果一致 | `cargo test board`、`cargo test bitstream` |
| 網頁 | 每個範例都用和網頁相同的 wasm + TypeScript API 跑過一遍 | `npm test` |

## 跑測試

```sh
./test.sh            # CI 跑的：veryl-sim、veryl-eda 的 cargo test、tutorial/check.sh、npm test
./test.sh --full     # 再加上 veryl-eda/test.sh（需要 OSS CAD Suite，數十分鐘）
```

每一步失敗也會繼續跑，最後印出摘要。個別執行：

```sh
cd veryl-eda && cargo test --release          # 合成所有範例、在網表上跑 testbench、C 編譯器、v2c 指令
cd veryl-eda && cargo test --release --test v2c  # 只測 v2c 的各個子指令
cd veryl-eda && ./test.sh                     # 形式等價 + FPGA 流程 + SKY130（含 GDS 檢查）
cd veryl-eda && ./fpga/pnr_test.sh            # 自己的佈局繞線：每個設計的位元流 vs 網表 + icetime
cd web && npm test                            # 網頁（要先 npm run build）
```

`veryl-eda/test.sh` 用到的環境變數：

| 變數 | 用途 |
|---|---|
| `YOSYS_SLANG` | 有 slang 前端的 yosys（OSS CAD Suite 的）。Homebrew 的 yosys 讀不了 `veryl build` 輸出的 enum 轉型與 function |
| `GDS_PY` | 有 KLayout 模組的 Python（`pip install klayout`），用來檢查 SKY130 的 GDS；沒設定時若 `python3` 有就用它 |
| `OUT` | 輸出目錄（預設暫存目錄） |
| `VERYL_EDA_CHIPDB` | IceStorm 晶片資料庫；`./test.sh` 找不到時從 `web/dist/chipdb.js` 取出 |

等價檢查使用 `-set-init-zero`，因為最佳化器假設正反器上電為 0（iCE40 是這樣）。

## 新增測試設計

- 合成用的測試設計放在 `veryl-eda/examples/`，並加進 `veryl-eda/test.sh` 的 `DESIGNS`（格式 `檔名:模組:模式`，
  模式 `comb` / `ind` / `bmcN`）。這些檔案會被複製進官方 Veryl 專案產生標準答案，所以 module 名稱不能和 `examples/src` 重複。
- 用 `veryl check`（在 `examples/` 裡執行）確認語法；`v2c` 的「not supported」不是語法錯誤，只是本專案沒支援。

## 原始碼地圖

| 目錄 | 內容 |
|---|---|
| `veryl-sim/` | 模擬器（crate `veryl2chip-sim`）：`elab.rs` 展開、`sim.rs` 事件驅動模擬、`value.rs` 4 值位元向量、`cli.rs` |
| `veryl-eda/src/` | 合成器（crate `veryl2chip-eda`）：`elab.rs` 符號執行成閘、`netlist.rs` 最佳化、`ice40.rs`、`bram.rs`、`output.rs`、`netsim.rs`、`cli.rs`、`bin/v2c.rs` |
| `veryl-eda/src/pnr/` | iCE40 自己的佈局繞線與位元流 |
| `veryl-eda/src/asic/` | 標準元件流程：`map` `place` `route` `detail` `sta` `layout` `drc` `gds` |
| `veryl-eda/src/pdk/` | 技術抽象、Liberty / LEF / DEF 讀取、SKY130 綁定；`veryl-eda/pdk/sky130hd/` 內附的子集 |
| `veryl-eda/src/board/` | 虛擬板：引擎、iCEBreaker、位元流解碼、周邊 |
| `veryl-eda/src/rv/` | C 編譯器、組譯器、指令集模擬器 |
| `veryl-wasm/` | 給網頁的 WebAssembly（C ABI，JSON 進出） |
| `web/` | IDE 與展示頁（TypeScript）；`web/dist/` 是建好的、直接可用的網頁（有進 git） |
| `examples/` | Veryl 範例（官方 Veryl 專案）、`examples/c/` C 範例、`examples/sw/` RISC-V 組合語言測試 |
| `tutorial/` | 教學與虛擬實驗課 |
| `tools/` | SKY130 下載與子集、GDS 檢查、字型、簡體轉換 |

更細的說明在 `AGENTS.md`、`web/PLAN.md` 與兩個 crate 的 README。

## 建置與發行

```sh
./build.sh                 # Rust 工具 + web/dist；改了 Rust 或 TypeScript 都要重建 web/dist
./publish.sh               # 發行到 crates.io 的預演（不上傳）
./publish.sh --yes         # 真的發行 veryl2chip-sim、veryl2chip-eda，並打 tag vX.Y
```

發行新版前，兩個 `Cargo.toml` 的版本（以及 eda 對 sim 的相依版本）都要升。

文件有三種語言：`README.md`（英文）、`README.tw.md`（繁體）、`README.cn.md`（簡體，由 `tools/tocn.py` 從繁體轉換）。
網頁介面的文字寫成 `tr('繁體', 'English')`，簡體由對照表自動產生。

CI（`.github/workflows/static.yml`）跑 `./test.sh` 的內容，推到 main 時把新建的 `web/dist` 部署到 GitHub Pages。
