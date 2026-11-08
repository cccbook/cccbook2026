# 附錄 A.1 中英術語對照表

本書（與本專案的介面翻譯）使用的術語。繁體中文為準；
簡體的「大陸慣用術語」見 `web/src/i18n_hans.ts` 的對應
（例：模擬→仿真、繞線→布线、列→行）。

## 通用

| 繁體 | English | 備註 |
|---|---|---|
| 精細化（展開） | elaboration | 把階層/參數/generate 展平 |
| 網表 | netlist | cell 與連接（位元）圖 |
| 符號執行 | symbolic execution | elab 把 RTL 直接變成閘的手法 |
| 位元流 | bitstream | FPGA 組態二進位 |
| 組態 | configuration | 位元流的語義內容 |
| 晶片資料庫 | chip database (chipdb) | IceStorm 的裝置描述 |
| 邏輯單元 | logic cell (LC) | iCE40：LUT+carry+FF |
| 查找表 | LUT (look-up table) | 4 輸入真值表 |
| 進位鏈 | carry chain | SB_CARRY 的串接 |
| 觸發器 | flip-flop (FF) | 時序元件 |
| 區塊記憶體 | block RAM | SB_RAM40_4K |
| 多工器 | multiplexer (mux) | if/case 的綜合結果 |
| 資料冒險 | data hazard | 單週期核心天然沒有 |
| 毛波（毛刺） | glitch | 引擎按層求值即消除 |
| 非阻塞性指定 | non-blocking assignment (NBA) | `always_ff` 的語義 |
| 差值（δ）週期 | delta cycle | 模擬器的組合收斂單位 |

## 綜合與驗證

| 繁體 | English | 備註 |
|---|---|---|
| 常數折疊 | constant folding | optimize 的一步 |
| 死碼清除 | dead logic sweep | optimize 的一步 |
| 覆蓋 | covering | 用 LUT 樹覆蓋閘圖 |
| 切點 | cut | 樹覆蓋的切斷點 |
| 等價性檢查 | equivalence checking | yosys 對 veryl build 的金模型 |
| 形式驗證 | formal verification | SAT/BMC 意義上的證明 |
| 隨機模擬 | random simulation | optimize 的常數節點證明 |
| 支撐集 | support | 函數真正依賴的輸入 |
| 原點（參照模型） | oracle | 每層的獨立真相 |
| 金模型（黃金參考） | golden model | 例：ISS 對 RTL |
| 指令集模擬器 | ISS (instruction-set simulator) | `rv/iss.rs` |
| 週期精確 | cycle-exact | ISS 與 RTL 的週期一致 |
| 測試台 | testbench | `#[test]` 模組 |

## FPGA 實作

| 繁體 | English | 備註 |
|---|---|---|
| 打包 | packing | LUT+FF 併成一個 LC |
| 佈局 | placement | 把 cell 放進 tile |
| 退火 | annealing | 佈局的模擬退火 |
| 成本函數 | cost function | 線長 + 時序 |
| 時序驅動 | timing-driven | 佈局時考慮 Slack |
| 繞線 | routing | 全域 + 細部 |
| 全域繞線 | global routing | 軌道級分配 |
| 細部繞線 | detailed routing | pip 級指定 |
| 路徑尋優 | PathFinder | 迭代協商式繞線 |
| 溢流 | overflow | 軌道超載 |
| 導通點 | pip | 兩線之間的可組態開關 |
| 時鐘樹合成 | CTS (clock tree synthesis) | ASIC 流程的一步 |
| 時鐘偏斜 | clock skew | CTS 的目標 |
| 插入延遲 | insertion delay | 時鐘到達葉端的延遲 |
| 全域緩衝器 | global buffer | iCE40 的 glb_netwk 驅動 |
| 保留集 | reservation set | LR/SC |
| 靜態時序分析 | STA | 計算所有端點的 Slack |
| 建立時間 | setup time | 時序約束之一 |
| 維持時間 | hold time | hold slack |
| 鬆弛 | slack | 允許時間 − 需要時間 |
| 臨界路徑 | critical path | 最小 slack 的路徑 |
| 腳位檔 | pcf | `set_io 名 腳` |
| 反解 | decode (bitstream → design) | 位元流 → Design |

## ASIC 與 PDK

| 繁體 | English | 備註 |
|---|---|---|
| 標準單元 | standard cell | vlib / SKY130 |
| 時序庫 | Liberty (.lib) | NLDM 延遲模型 |
| 實體庫 | LEF | 單元的版圖摘要 |
| 實體設計格式 | DEF | 佈局繞線結果 |
| 製程設計套件 | PDK | 例：SKY130HD |
| 圖形資料流系統 | GDSII | 版圖交換格式 |
| 設計規則檢查 | DRC | 間距/寬度/短路 |
| 電源網 | PDN (power delivery network) | 電軌與條帶 |
| 井接觸 | tap cell | 防閂鎖 |
| 填充單元 | filler cell | 列填滿 |
| 行 | row | 標準單元擺放列 |
| 晶格點 | site | row 的最小寬度單位 |
| 布局利用率 | utilization | cell 面積 / 可用面積 |
| 軌道 | track | 繞線格線 |
| 層 | layer | 金屬/多晶矽層 |
| 通孔 | via | 層間連接 |
| 隔離環（禁布區） | halo | 電晶體周圍的繞線禁區 |
| 內部缺陷（凹缺） | notch | 同一 net 的自干涉 |
| 電壓降 | IR drop | 電源網壓降 |
| 動態功耗 | dynamic power | 翻轉功耗 |
| 漏電功耗 | leakage power | 靜態功耗 |
| NLDM | non-linear delay model | Liberty 的查表延遲 |
| 輸入轉換 | input transition | NLDM 的第二維 |
| 負載 | load (capacitance) | 扇出電容 |
| 單元寬度 | cell width | site 的倍數 |

## RISC-V

| 繁體 | English | 備註 |
|---|---|---|
| 多週期 | multi-cycle | RvCore |
| 單週期 | single-cycle | RiscvCore |
| 狀態機 | FSM (state machine) | FETCH/DECODE/… |
| 投機取指 | speculative fetch | EXEC 送出下一讀取 |
| 陷阱 | trap | 例外或中斷 |
| 例外 | exception | 同步的 trap |
| 中斷 | interrupt | 非同步的 trap |
| 陷入向量 | trap vector | mtvec |
| 機器模式 | machine mode | 本核心唯一模式 |
| 控制狀態暫存器 | CSR | Zicsr |
| 讀改寫 | read-modify-write | AMO |
| 原子指令 | atomic instruction | LR/SC/AMO |
| 保留 | reservation | LR 記下的位址 |
| 未對齊 | misaligned | 位址非 4/2 的倍數 |
| 可變參數 | variadic | C 的 `...` |
| 幀指標 | frame pointer | s0 |
| 序言／結語 | prologue / epilogue | 函式的開頭/收尾 |
| 裸函式 | naked function | 只有 asm 的函式 |
| 死碼移除 | dead code elimination | 函式級 reachable-set |
| 波特率 | baud rate | UART，cpb = f/baud |
| 責任週期 | duty cycle | 高電位時間比例 |
| 行程編碼 | RLE (run-length encoding) | VGA 幀壓縮 |
| 麵包板 | breadboard | 虛擬接線實驗 |

## 模擬器與時序

| 繁體 | English | 備註 |
|---|---|---|
| 活動驅動 | activity-driven | 只評估變化訊號的下游 |
| 層級（深度） | level | 組合 cell 的拓撲深度 |
| 風扇出 | fanout | net 餵的 cell 清單（CSR） |
| 排程 | scheduling | 事件佇列與層序求值 |
| 收斂 | settle | 組合邏輯停止變化 |
| 上電 | power-up | FF 初值（iCE40 = 0） |
| 電源重開 | power cycle | 保留設計、重置狀態 |
| 窗口 | window | duty 統計的時間區間 |
| 邊緣計數 | edge count | 頻率的量度（蜂鳴器） |
| 驅動者 | driver | net 的唯一來源 |
| 雙驅動 | multiple drivers | 短路（警告） |
| 浮接 | floating | 無驅動、無電阻路徑 |
| 上拉／下拉 | pull-up / pull-down | 電阻的弱傳遞 |
| 亞穩態 | metastability | 兩級同步器的理由 |
| 中點取樣 | mid-bit sampling | UART 的抗偏移取樣 |
| 誤框 | framing error | 停止位元為 0 |

## 介面與工具

| 繁體 | English | 備註 |
|---|---|---|
| 整合開發環境 | IDE | web 的 index.html |
| 覆蓋層 | overlay | 綜合視覺化（SynthOverlay） |
| 語法上色 | syntax highlighting | tokenizer 產生 |
| 工作器 | worker | 瀏覽器的執行緒 |
| 會話 | session | thread-local 的狀態組 |
| 序列埠 | serial port | 8N1、TX/RX |
| 波特率除數 | clocks per bit (cpb) | f_clk / baud |
| 字型 | font | 5×7 點陣（font5x7） |
| 文字模式 | text mode | VgaText 的 VRAM/字型/顏色 |
| 幀 | frame | 一次完整的 VGA 掃描 |
| 可見區 | visible area | 640×480（在 800×525 內） |
| 同步脈衝 | sync pulse | HSYNC / VSYNC（低致能） |
| 消隱 | blanking | 同步與前後廊的不可見拍 |
| 擴充板 | PMOD | Pmod 規格的接腳排 |
| 腳位檔 | pin file | pcf 的另一稱呼 |

## 使用注意

1. **同義詞的選擇**：「繞線」（routing）在本專案的
   繁體介面與本書一致；簡體介面用「布线」（大陸慣用）。
   「模擬」（simulation）簡體為「仿真」——這兩個是
   `i18n_hans.ts` 詞彙表的第一批條目。
2. **容易混淆的對**：
   - 佈局（placement，把 cell 放進 tile）vs
     佈局繞線（place and route，整個後端流程）；
   - 細部繞線（detailed routing，pip 級）vs
     詳細路由（不要用——routing 不譯「路由」，
     那是網路術語）；
   - 行（row，標準單元擺放列）vs 列
     （簡體的「行」= 繁體的「列」——
     `i18n_hans.ts` 的「列→行」條目就是處理這個）。
3. **縮寫的展開**：第一次出現時展開
   （靜態時序分析（STA）），之後可用縮寫。
   LUT、FF、CSR、ISS 這類高頻縮寫正文直接用。
4. **專案特有詞**：虛擬開發板（virtual board）、
   位元流反解（bitstream decode）、活動驅動
   （activity-driven）、強/弱 net（strong/weak net）
   ——這些是本專案的造詞，英文照原始碼註解用詞。
5. **與介面的一致性**：IDE 裡的按鈕文字就是本書的
   術語（例：流程目標的「asic」「sky130」直接用英）；
   `npm test` 檢查每個 `tr()` 對，本書新增術語時
   應同步檢查 `src/i18n.ts` 是否已有同義異譯。

## 數學與公式慣例（補充）

本書的公式（

$$
...
$$

）用到的量，對應的術語：

| 符號 | 繁體 | English | 出現處 |
|---|---|---|---|
| $`F_{\max}`$ | 最高頻率 | maximum frequency | STA： $`F_{\max} = 1 / T_{\text{critical}}`$ |
| $`T_{\text{clk}}`$ | 時脈週期 | clock period | 12 MHz → 83.3 ns |
| $`t_{\text{setup}}`$ | 建立時間 | setup time | Liberty 約束 |
| $`t_{\text{hold}}`$ | 維持時間 | hold time | hold slack |
| $`c`$ | 負載 | load capacitance | NLDM 的第二維 |
| $`s`$ | 輸入轉換 | input transition | NLDM 的第一維 |
| $`T`$ | 週期數 | cycle count | ISS 的 cycles |
| $`\text{cpb}`$ | 每位元時脈數 | clocks per bit | $`12\,\text{MHz} / 115200 \approx 104`$ |
| $`\text{duty}`$ | 責任週期 | duty cycle | 高拍數 / 窗口 |
| $`\bar{c}`$ | 每拍平均求值數 | average evals per cycle | board_speed 的 evals/cycle |
| $`L`$ | LUT 總數 | LUT count | 與 $`\bar{c}`$ 對比 |
| $`W`$ | 線長 | wirelength | 佈局成本的主要項 |
| $`u`$ | 利用率 | utilization | cell 面積 / 可用面積 |
| $`\text{slack}`$ | 鬆弛 | slack | 需求 − 到達 |
| $`N_{\text{ovl}}`$ | 溢流 | overflow | PathFinder 的收斂條件 |

## 總索引（英→繁）

供英文文獻對照（與上表同一批詞，反向排列）：

activity-driven 活動驅動、annealing 退火、baud rate 波特率、
bitstream 位元流、block RAM 區塊記憶體、breadboard 麵包板、
carry chain 進位鏈、chip database 晶片資料庫、
constant folding 常數折疊、covering 覆蓋、critical path 臨界路徑、
cut 切點、cycle-exact 週期精確、CSR 控制狀態暫存器、
dead code elimination 死碼移除、decode 反解、DRC 設計規則檢查、
duty cycle 責任週期、elaboration 精細化、fanout 風扇出、
flip-flop 觸發器、framing error 誤框、GDSII 圖形資料流系統、
glitch 毛波、golden model 金模型、halo 隔離環、
hold time 維持時間、IDE 整合開發環境、
instruction-set simulator 指令集模擬器、interrupt 中斷、
IR drop 電壓降、layer 層、LEF 實體庫、level 層級、
Liberty 時序庫、logic cell 邏輯單元、metastability 亞穩態、
misaligned 未對齊、multiplexer 多工器、netlist 網表、
NLDM 非線性延遲模型、overflow 溢流、PDK 製程設計套件、
pip 導通點、placement 佈局、power cycle 電源重開、
prologue／epilogue 序言／結語、pull-up／pull-down 上拉／下拉、
RLE 行程編碼、routing 繞線、row 行、setup time 建立時間、
site 晶格點、skew 時鐘偏斜、slack 鬆弛、speculative fetch 投機取指、
standard cell 標準單元、symbolic execution 符號執行、
testbench 測試台、track 軌道、trap 陷阱、
utilization 利用率、via 通孔、wirelength 線長。

本表與 `web/src/i18n_hans.ts` 的轉換表、`tools/tocn.py`
的 OpenCC 詞表共用精神：**繁體是事實來源（source of truth）**，
英文只是對照，簡體一律由工具生成。新增術語時的三步：
加入上表、檢查 `i18n.ts` 是否已有同義異譯、
（若是新概念）在 `i18n_hans.ts` 補簡體詞彙條目。
