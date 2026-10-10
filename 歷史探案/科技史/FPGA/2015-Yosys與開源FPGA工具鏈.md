# 2015-Yosys與開源FPGA工具鏈

## 案件摘要
2013 年，奧地利的獨立開發者 Clifford Wolf 發布了開源邏輯合成器 Yosys；2015 年，他與 David Shah 等人啟動 Project IceStorm，逆向工程出 Lattice iCE40 FPGA 的 bitstream 格式。這兩塊拼圖合在一起，首次讓工程師能夠從 Verilog 原始碼一路走到可下載的位元流，全程不依賴任何閉源工具，開啟了全開源 FPGA 工具鏈的紀元（其後演進為 SymbiFlow／F4PGA、openXC7 等計畫）。

## 前因 -- 為什麼會會有這個案子
FPGA 自 1985 年誕生以來，長期存在一個「看不見的房間」：設計者寫完 Verilog 之後，晶片內部到底發生了什麼事，完全交給廠商的閉源工具鏈處理。Xilinx 的 ISE／Vivado、Altera 的 Quartus，動輒佔用數十 GB 磁碟空間、安裝繁瑣、對合成結果是徹底的黑箱。工程師若想知道「為什麼我的電路合成出來變這樣」，唯一手段是對照廠商的報告檔案反覆猜測；若想研究合成演算法本身，更是連原始碼都看不到。

更實際的困境是授權與成本。學術界與小型開發者往往買不起正式授權，只能使用「免費但有限制」的 WebPACK 版本，或被迫選用廠商指定的入門晶片。而且閉源工具鏈把使用者綁死在特定晶片上：一旦晶片停產或廠商調整授權政策，多年累積的設計流程（尤其是腳本、CI 自動化）就整條報廢。在開源軟體世界，GCC／LLVM 早已證明「編譯器可以開源」，但 FPGA 的「編譯器」（合成器＋佈局繞線器）卻遲遲沒有對應物。

最後一塊短板是 bitstream 格式本身。就算有了開源合成器，若不知道如何把合成結果轉成晶片認得的位元流，工具鏈依然缺了最關鍵的一環。各廠商從不公開 bitstream 規格，理論上這需要對晶片做逆向工程——這正是本案最像「偵探辦案」的部分。2013 年 Yosys 的出現提供了合成端；2015 年 Project IceStorm 攻下了 bitstream 端，案件就此偵破。

## 線索與推理 -- 數學式、程式、理論

### 線索一：邏輯合成的流程理論——從 RTL 到技術映射
FPGA 工具鏈本質上是把「高階描述」翻譯成「晶片物理資源」的編譯器，流程如下：

| 階段 | 輸入 | 輸出 | 對應 CPU 編譯器的概念 |
|---|---|---|---|
| 前端解析（elaborate） | Verilog/VHDL | 內部表示（IR），如 RTLIL | 詞法／語法分析，產生 AST 與 IR |
| 高階最佳化 | RTLIL | 簡化後的邏輯網路 | 常數折疊、死碼消除 |
| 程序處理（proc） | always 區塊 | FSM、多工器結構 | 控制流還原 |
| 技術映射（techmap） | 通用邏輯閘 | LUT／FF 原語 | 指令選擇（instruction selection） |
| 布局繞線（place & route） | LUT 網路 | 晶片上的物理位置 | 暫存器配置＋定址 |
| 位元流產生 | 佈局結果 | .bit 檔 | 目的碼（object file） |

其中「技術映射」的核心問題是：給定一個布林函數 $f$，如何用最少（或最快）的 $k$-輸入 LUT 表示它？形式上，這是把布林網路覆蓋（cover）成若干 $k$-feasible cuts 的最小成本問題：

$$C(v) = \min_{\text{cut}(v)} \left( 1 + \sum_{u \in \text{inputs}(\text{cut}(v))} C(u) \right)$$

其中 $C(v)$ 是映射到節點 $v$ 所需的 LUT 數。動態規劃可在 $O(n \cdot 2^k)$ 時間內求出近似解。

### 線索二：Yosys 的設計——合成器如同「邏輯的 LLVM」
Clifford Wolf 在設計 Yosys 時採取了一個關鍵決策：不重造整個輪子，而是把 Yosys 做成「前端＋技術映射」，並把佈局繞線交給專門工具。Yosys 的內部表示 RTLIL 是一種有向圖形式的邏輯網路，所有最佳化 pass 都作用在這個共同表示上，就像 LLVM 的 IR 一樣可以自由穿插、組合。

Yosys 的典型流程腳本：

```tcl
read_verilog counter.v
synth_ice40 -top counter
write_json counter.json
```

`synth_ice40` 其實是一串 pass 的巨集：`proc` → `opt`（多輪最佳化）→ `fsm`（FSM 提取與重新編碼）→ `memory`（記憶體推斷為 BRAM）→ `techmap` → `abc -lut 4`。這種「pass 組合」架構讓研究者可以用 `help` 查閱每個 pass，甚至自己用 Python/C++ 寫新 pass 插入流程中——這是閉源工具鏈永遠做不到的透明度。

### 線索三：ABC 演算法——AIG 上的邏輯最佳化
Yosys 的最佳化後端委託給 Alan Mishchenko 在 UC Berkeley 開發的 ABC。ABC 的核心資料結構是 AIG（And-Inverter Graph）：整個布林網路只用一種節點——二輸入 AND 閘，加上節點邊上的反相器標記。任何布林函數都可表示為：

$$f(x_1,\dots,x_n) = \text{AND}\big(\pm g_1, \pm g_2\big), \quad g_i \in \{\text{AIG 子節點, 常數, 輸入}\}$$

（$\pm$ 表示邊上是否掛反相器。）AIG 極度精簡，使得「結構等價檢驗」與「最佳化操作」變得高效。ABC 的三大招式：

| 操作 | 原理 | 效果 |
|---|---|---|
| Rewriting | 對 4 節點子圖窮舉所有替換候選，選最優者 | 區域性減少節點數 |
| Refactoring | 對較大錐（cone，約 10-15 節點）重新提取布林表示再合成 | 打破局部結構的惡性形態 |
| Resubstitution | 觀察節點 $v$ 的支援集內是否已有節點能算出 $v$ 的函數 | 刪除冗餘節點而不改變功能 |

以 Resubstitution 為例：若節點 $v = g_1 \oplus g_2$，而 $g_1, g_2$ 都在 $v$ 的可達支援集裡，則 $v$ 可以直接刪除、由下游引用 $g_1 \oplus g_2$ 的計算。每個操作都維持功能等價（可用 SAT 檢驗），整個最佳化是「不斷在等價類之間移動到更小表示」的搜尋過程。理論上邏輯最佳化是 NP-hard，ABC 用啟發式搜尋逼近。

### 線索四：偵探的放大鏡——bitstream 逆向工程
本案最精彩的部分：如何搞清楚 iCE40 晶片的 bitstream 格式？沒有任何文件，Clifford Wolf 與 David Shah 的方法是「控制變數實驗」，後來被稱為 fuzzer 方法：

1. **先搞懂架構**：iCE40 是典型的島狀架構——邏輯塊（PLB，每塊含 8 個 LUT/FF 對）、BRAM、DSP、IO、時脈網路，排列成網格。
2. **寫最小差異設計**：產生兩個只有一處不同的設計，例如「這個 PLB 的 LUT0 輸出連到 FF」vs「不連」。
3. **合成並比對 bitstream**：用廠商工具（iCEcube2）產生兩個 bitstream，逐位元組比對，找出改變的位元。
4. **推斷編碼規則**：若某位元翻轉總是伴隨「路由開關改變」，就推斷該位元是某個 pip 的配置位；重複數百次實驗建立完整映射表。
5. **驗證閉環**：用推斷出的格式自己生成 bitstream，燒錄到真晶片上驗證功能正確。

數學上，這是在對未知的配置函數 $\beta: \text{電路配置} \to \{0,1\}^N$ 做黑箱學習。每次 fuzzer 實驗提供一條約束 $\beta(c_i) = b_i$，當約束足以唯一確定 $\beta$ 在目標配置空間上的值，逆向工程即完成。iCE40 的 bitstream 是 0x7EAA997E 開頭、以 CRC16 結尾的指令流，配置資料以 16 位字為單位按行列寫入晶片的配置記憶體——這些規則全部靠上述實驗還原。

### 線索五：全開源工具鏈的閉環
Project IceStorm 完成後，完整的開源流程是：

```
Verilog → Yosys（合成＋技術映射）→ nextpnr（佈局繞線）→ icepack（bitstream 打包）→ iceprog（燒錄）
```

nextpnr 由 Clifford Wolf 與 David Shah 合作開發，是一個「架構無關」的佈局繞線器：晶片資源描述以 JSON 檔（後來改為 C++ 架構 API）輸入，同一套模擬退火佈局演算法即可服務不同晶片。模擬退火的核心是接受函數：

$$P(\text{接受劣化解}) = e^{-\Delta C / T}$$

其中 $T$ 是溫度參數，隨迭代遞減。佈局成本 $C$ 綜合考慮線長（HPWL，半周長線長）與時序約束。這種通用化設計讓 nextpnr 後來擴展出支援 ECP5（ecp5 目標）、Nexus（Nexus 目標）等系列，成為開源 FPGA 生態的基礎設施。

### 線索六：開源 vs 閉源工具鏈對照表

| 面向 | 閉源（Vivado/Quartus） | 開源（Yosys/nextpnr） |
|---|---|---|
| 磁碟佔用 | 30–100 GB | 幾百 MB |
| 授權 | 收費／晶片限定免費版 | 完全自由（ISC/MIT 授權） |
| 可否研究合成演算法 | 黑箱，只有報告檔 | 完整原始碼，pass 可自寫 |
| 位元流格式 | 未公開 | IceStorm 全部逆向公開 |
| 晶片支援 | 全系列、最先進製程 | iCE40、ECP5、Nexus 等中低端 |
| 時序收斂品質 | 頂尖（廠商內部 know-how） | 中等，約落後 10–30% Fmax |
| CI／自動化 | 繁瑣 | 命令列友善，極易整合 |
| 教育用途 | 限縮 | 完全開放，可讀到每一步 |

閉源工具在「壓榨最先進晶片效能」上仍然無可取代，但開源工具鏈在中低端晶片、教育、研究、長期維護上取得了決定性勝利。

## 結案 -- 後果與影響
2015 年 Project IceStorm 發布第一個全開源 bitstream 流程後，開源 FPGA 社群迅速壯大。iCE40 因為工具鏈完全開源，反而從「Lattice 的邊緣小晶片」變成開發者與學界的最愛；Lattice 也順勢擁抱開源，成為對開源工具最友善的 FPGA 廠商。nextpnr 擴展到 ECP5 之後，開源工具鏈可支援的晶片範圍擴大到具有 DSP 與 PCIe 的中型元件。

計畫的後繼者不斷湧現：Google 與社群合作的 SymbiFlow（後更名 F4PGA）把技術映射到 Xilinx 7-series 與 Lattice 晶片；openXC7 針對 Xilinx 7-series；RapidWright 等則提供對閉源工具產出物的程式化操作。開源合成器的思想甚至反哺了 ASIC 世界——Yosys 被廣泛用於開源 ASIC 流程（如 SkyWater PDK 的開源晶片計畫）。

案件的最終影響：

- **打破黑箱**：FPGA 的「編譯器內部」首次對所有人可見，合成演算法從秘傳學問變成可研究、可教學的公開知識。
- **降低門檻**：幾百 MB 的工具鏈讓任何擁有筆電的人都能學 FPGA，教育普及度大幅提升。
- **活躍開源晶片生態**：iCE40/ECP5 等開源友善晶片形成生態位，RISC-V 軟核、開源 SoC（如 LiteX）蓬勃發展。
- **倒逼廠商開放**：Lattice 明確支援開源工具，其他廠商也開始提供更多文件與介面。
- **工具鏈研究復興**：nextpnr 的通用架構成為學術界研究新型佈局繞線演算法的平台。

## 關鍵人物與文獻
- **Clifford Wolf**：Yosys 與 IceStorm 的主要作者，開源 FPGA 工具鏈的奠基者。
- **David Shah**：nextpnr 共同開發者，IceStorm bitstream 逆向工程的主要貢獻者。
- **Alan Mishchenko**：UC Berkeley，ABC 邏輯最佳化工具的作者。
- **Project IceStorm 文件**：<https://github.com/YosysHQ/icestorm>——iCE40 bitstream 格式的完整公開紀錄。
- **Yosys 手冊**：Claire Wolf, "Yosys Manual"，詳述 RTLIL 與 pass 架構。
- **A. Mishchenko et al.**, "Scalable Logic Synthesis Using a Simple Circuit Structure"（AIG 相關論文）。
- **SymbiFlow／F4PGA**：<https://f4pga.org>——開源工具鏈的後繼計畫。
- **Lattice iCE40 系列**：首款被全開源工具鏈完整支援的 FPGA 家族。
