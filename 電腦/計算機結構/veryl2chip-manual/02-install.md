# 2. 安裝

## 不安裝：線上版

打開 <https://ccc-eda.github.io/veryl2chip/web/dist/index.html> 就是完整的 IDE（第 11 章）。
它不需要伺服器，下載 `web/dist/` 整個目錄後，直接用瀏覽器開 `index.html` 也能離線使用。

## 安裝 `v2c`

需要 Rust（<https://rustup.rs>）：

```sh
cargo install veryl2chip-eda
v2c version
```

這會裝上 `v2c`，以及舊的 `veryl-eda` 指令。若也想要單獨的模擬器指令 `veryl-sim`，再裝 `veryl2chip-sim`
（`v2c sim` 已經包含模擬器，通常不需要）。

## 從原始碼建置

```sh
git clone https://github.com/ccc-eda/veryl2chip
cd veryl2chip
./build.sh            # Rust 工具（release）與 web/dist；--no-web 只建 Rust 工具
```

建好的指令在 `veryl-eda/target/release/v2c`。可以把這個目錄加進 `PATH`，或在 `veryl-eda/` 裡用
`cargo run --release --bin v2c -- ...`。建網頁需要 wasm32 target 與 Node.js（`build.sh` 會自動補裝 target 與 npm 套件）。

## 外部工具（依需要）

| 工具 | 用途 | 從哪裡來 |
|---|---|---|
| `iceprog` | 把 `.bin` 燒進實體 iCEBreaker | [OSS CAD Suite](https://github.com/YosysHQ/oss-cad-suite-build/releases) |
| `nextpnr-ice40`、`icepack` | `v2c fpga` 預設的佈局繞線工具（用 `--pnr veryl` 就不需要） | OSS CAD Suite |
| `nextpnr-ecp5`、`ecppack`、`openFPGALoader` | ECP5（`v2c fpga --arch ecp5`）的佈局繞線、位元流、燒錄 | OSS CAD Suite |
| IceStorm 的 `chipdb-5k.txt` | `--pnr veryl`（自己的佈局繞線）需要的晶片資料庫 | OSS CAD Suite 的 `share/icebox/`；或用 `VERYL_EDA_CHIPDB` 指定 |
| `gtkwave` | 看 `v2c sim --vcd` 產生的波形 | OSS CAD Suite 或系統套件 |
| 官方 `veryl` | `veryl check` / `veryl test` / `veryl build`（語法的標準答案） | `cargo install veryl` |
| KLayout | 看 `.gds` 晶片版圖；`tools/gds_check.py` 用它的 Python 模組 | <https://www.klayout.de>，Python 模組：`pip install klayout` |
| 完整 SKY130 檔案 | 只有 `v2c pdk`、`--pdk sky130:目錄` 需要（`--pdk sky130` 用內附的子集） | `tools/sky130.sh` 下載 |

沒有 OSS CAD Suite 也能做大部分的事：模擬、合成、`v2c fpga --pnr veryl`（只要有晶片資料庫）、ASIC 流程、C 程式。

## 環境變數

| 變數 | 用途 |
|---|---|
| `VERYL_EDA_CHIPDB` | IceStorm `chipdb-5k.txt` 的路徑（自己的佈局繞線用） |
| `VERYL_EDA_SKY130` | 完整 SKY130 hd 檔案的目錄（`v2c pdk`） |
| `VERYL_EDA_PROFILE` | 設定後印出 ASIC 流程各步驟的耗時與細部繞線每一輪的衝突數 |
| `YOSYS_SLANG`、`GDS_PY` | 開發者的驗證腳本用（第 13 章） |
