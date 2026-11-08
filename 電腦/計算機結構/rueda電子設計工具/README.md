# rueda 電子設計工具

用 Rust 寫的一整套 IC 設計 EDA：硬體語言（Veryl、Fluxa）→ 模擬 → 合成 → FPGA 位元流或 ASIC 佈局，
再加上 RISC-V 軟體工具，以及在瀏覽器裡就能跑這一切的網頁 IDE。

本書以 `/Users/Shared/ccc/project/rueda/` 為對象，逐章拆解這條流程的每一個環節：
它們為什麼長成那樣，而不是只說它們長成那樣。

## 目錄

* 第1章 電子設計工具：歷史、地圖與rueda架構
    * [1.1-從繼電器到EDA：電子設計自動化四十年](01.1-從繼電器到EDA-電子設計自動化四十年.md)
    * [1.2-硬體描述語言的演進](01.2-硬體描述語言的演進.md)
    * [1.3-rueda的架構：一個指令串起所有工具](01.3-rueda的架構-一個指令串起所有工具.md)
* 第2章 Veryl：一門從零設計的硬體描述語言
    * [2.1-Veryl的型別系統與宣告語法](02.1-Veryl的型別系統與宣告語法.md)
    * [2.2-介面、時脈與重置領域](02.2-介面時脈與重置領域.md)
    * [2.3-從RTL到閘級：符號執行與結構雜湊](02.3-從RTL到閘級-符號執行與結構雜湊.md)
* 第3章 模擬：從事件驅動到程序網路
    * [3.1-四態值與delta cycle](03.1-四態值與delta-cycle.md)
    * [3.2-測試平台與initial區塊的編譯](03.2-測試平台與initial區塊的編譯.md)
    * [3.3-Kahn程序網路：Fluxa的時間模型](03.3-Kahn程序網路-Fluxa的時間模型.md)
* 第4章 合成：把語意變成閘
    * [4.1-網表IR與位元層級Builder](04.1-網表IR與位元層級Builder.md)
    * [4.2-最佳化：常數證明與固定點](04.2-最佳化-常數證明與固定點.md)
    * [4.3-高階合成：從task到FSM與資料路徑](04.3-高階合成-從task到FSM與資料路徑.md)
* 第5章 FPGA：從網表到位元流
    * [5.1-LUT覆蓋與進位鏈](05.1-LUT覆蓋與進位鏈.md)
    * [5.2-佈局與繞線：退火與PathFinder](05.2-佈局與繞線-退火與PathFinder.md)
    * [5.3-位元流格式與CRC](05.3-位元流格式與CRC.md)
* 第6章 ASIC：從網表到GDS
    * [6.1-PDK：Liberty與LEF](06.1-PDK-Liberty與LEF.md)
    * [6.2-擺置、CTS、PDN與繞線](06.2-擺置CTS-PDN與繞線.md)
    * [6.3-時序分析、DRC/LVS與GDSII](06.3-時序分析DRC-LVS與GDSII.md)
* 第7章 RISC-V軟體與SoC
    * [7.1-RISC-V指令集與SoC結構](07.1-RISC-V指令集與SoC結構.md)
    * [7.2-C編譯器、組譯器與指令集模擬器](07.2-C編譯器組譯器與指令集模擬器.md)
    * [7.3-Linux開機：從OpenSBI到busybox](07.3-Linux開機-從OpenSBI到busybox.md)
* 第8章 快速模擬與WebAssembly
    * [8.1-veryl-emu：週期式編譯模擬](08.1-veryl-emu-週期式編譯模擬.md)
    * [8.2-fluxa-emu：狀態機到程式碼](08.2-fluxa-emu-狀態機到程式碼.md)
    * [8.3-瀏覽器裡的JIT](08.3-瀏覽器裡的JIT.md)
* 第9章 網頁IDE與回饋迴圈
    * [9.1-wasm核心與JSON ABI](09.1-wasm核心與JSON-ABI.md)
    * [9.2-虛擬開發板與麵包板](09.2-虛擬開發板與麵包板.md)
    * [9.3-從模擬到晶片：完整流程](09.3-從模擬到晶片-完整流程.md)

## 快速上手

```sh
# 取得並建置
cd /Users/Shared/ccc/project/rueda
./build.sh                # target/release/reda 與 web/dist（--no-web：只建 reda）

# 一個指令跑完整條流程
reda sim counter.veryl                 # 跑測試平台（語言由副檔名決定）
reda sim fir.fx                        # Fluxa 程式的 test
reda synth -o adder.json adder.veryl   # 合成成閘級網表（yosys JSON / Verilog）
reda fpga --pnr veryl --pcf pins.pcf --bin top.bin top.veryl
reda asic --pdk sky130 --gds alu.gds alu.veryl
reda gatesim ice40 fifo.veryl          # 在合成後的網表上跑 testbench
reda emu --top Rv64Soc -o soc.wasm *.veryl
reda emu fir.fx                        # Fluxa 的 test，task 換成編譯後的版本
reda cc --run hello.c                  # 給 RISC-V SoC 的 C 程式，在指令集模擬器上執行
reda rvemu fw_payload.bin              # RV64 開發板模擬機（OpenSBI + Linux）
reda help [子指令]
```

## 三條閱讀路線

| 路線 | 章節 | 適合 |
|---|---|---|
| 語言到硬體 | 1 → 2 → 4 → 5 → 6 | 想理解「RTL 如何變成晶片」 |
| 軟體到系統 | 1 → 3 → 7 → 8 → 9 | 想理解「一個程式如何在瀏覽器裡開 Linux」 |
| EDA 演算法 | 1.1 → 4 → 5 → 6 | 想讀懂佈局繞線、LUT 覆蓋、時序分析 |

三條路線在第 4 章（網表 IR）會合流，因為**網表是唯一的匯流點**。

## 對應原始碼

```
rueda/
├── reda/            reda 指令（每個工具一個子指令）
├── eda/             與語言無關的後端
│   ├── src/           網表、block RAM、輸出格式、閘級模擬、時序約束、功耗
│   ├── src/fpga/      iCE40 / ECP5 對應、自己的佈局繞線與位元流、虛擬 iCEBreaker
│   ├── src/asic/      標準單元流程：擺置、時脈樹、繞線、時序、DRC / LVS、GDS
│   ├── src/pdk/       Liberty / LEF / DEF、SKY130 綁定
│   ├── bits/          與前端共用的位元向量
│   └── tools/         SKY130 下載、KLayout 的 GDS / LVS / 天線檢查
├── veryl/           Veryl 語言（sim / synth / emu / examples / tutorial）
├── fluxa/           Fluxa 語言（sim / synth / emu / rv32i / rv64 / docs）
├── riscv/           RISC-V 軟體（rvtools：C 編譯器、組譯器、RV32 ISS）
│                      rvemu：RV64 開發板模擬機，含 WebAssembly JIT）
└── web/             網頁 IDE（TypeScript）；wasm/：它的 WebAssembly 核心
```

## 本書的方法論

貫穿全書的五條原則：

1. **中介表示的選擇決定一切**——網表 IR 選成位元層級 + yosys 內部命名，換來跨語言共用後端。
2. **架構規則必須能被工具強制檢查**——`eda/` 不得依賴語言前端，由 Cargo 依賴圖保證。
3. **同一語意、多種實作、交叉驗證**——直譯 vs 編譯、RTL vs 閘級、內部 DRC vs KLayout。
4. **兩套驗證策略要分層搭配**——SAT / k-induction / BMC / 功能測試，按設計大小分配。
5. **範圍控制與誠實**——刻意不實作的東西要寫下來，沒檢查的規則要明說。
