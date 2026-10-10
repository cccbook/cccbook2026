# 1992-AlteraFLEX-SRAM架構

## 案件摘要
1992 年，Altera 推出 FLEX 8000，首度在這家以 EPROM/EEPROM CPLD 起家的廠牌中採用 SRAM 查找表（LUT）架構，Lucent Technologies 的 ORCA（1993）等隨後跟進。本檔追查：為何「CPLD 之父」要自我否定、改投 LUT 陣營，以及 SRAM FPGA 的組態載入流程如何在時序上重新定義系統設計。

## 前因 -- 為什麼會會有這個案子

回顧 1980 年代的結案：Altera 以 CPLD（MAX 5000/7000）佔據了「確定延遲、非易失、千閘尺度」的市場，Xilinx 以 SRAM FPGA 佔據了「高容量、可重寫」的市場。但 1990 年代初期，情勢起了變化：半導體製程從 $1.0\,\mu\text{m}$ 快速推進到 $0.8$、$0.65\,\mu\text{m}$，晶片可容納的電晶體數呈指數成長。市場開始要求數萬閘以上的可程式邏輯——而 CPLD 的兩級 SOP 架構在這個尺度上失效了：乘積項陣列的面積隨輸入數二次方成長，PIA 的 fan-in 也逼近物理極限。

更關鍵的是學理上的證據已經累積：Xilinx 的 William Carter 與 Ross Freeman 在 1980 年代提出的 LUT 概念，加上 Berkeley 的 ACT 研究計畫（1988-1992）對 LUT-based FPGA 的系統性驗證，證明 LUT 架構在容量成長上有更好的面積與延遲性質。Altera 面臨經典的「創新者兩難」：自己最賺錢的 CPLD 架構，恰好在成長市場中是錯的答案。

1992 年的 FLEX 8000 是 Altera 的自我否定之作：它採用 SRAM 組態、四輸入 LUT 邏輯單元（Altera 稱為 Logic Element, LE），同時保留了 CPLD 的血統——每 8 個 LE 組成一個 Logic Array Block（LAB），LAB 內有局部的類 SOP 互連，形成「LUT 為骨、CPLD 為筋」的混合架構。1993 年 Lucent（前 AT&T 貝爾實驗室系統）推出 ORCA 系列，同樣採用 SRAM LUT，證明這條路線已是產業共識。

## 線索與推理 -- 數學式、程式、理論（本體，最詳細）

### 線索一：乘積項爆炸 vs LUT 固定深度

n 變數任意布林函數的最壞情況 SOP 形式需要多少乘積項？考慮所有 $2^n$ 個最小項（minterm），每個最小項都是一個乘積項。一個「隨機」函數的期望最簡 SOP 大小約為：

$$\mathbb{E}[|\text{SOP}|] \approx \frac{2^n}{n \ln 2} \cdot \text{（常數因子）}$$

即乘積項數隨 $n$ **指數爆炸**。CPLD 硬體若要支援 $n = 16$ 的單級函數，需要：

$$2^{16} = 65{,}536 \text{ 個乘積項}$$

——物理上不可行。這就是 SOP 架構的數學死刑：它只能處理「淺而窄」的函數（$n \le 10 \sim 12$ 的少數項函數），超過就必須拆成多級，拆級意味着延遲成倍增加。

LUT 架構的解法是**用記憶體換陣列**：一個 $k$-LUT 是 $2^k \times 1$ 位元的 SRAM，任何 $k$ 變數函數（共 $2^{2^k}$ 個）都能以「一表一函數」實現：

$$\text{$k$-LUT 面積} = 2^k \text{ bits SRAM + } 2^k{:}1 \text{ MUX} \propto 2^k$$

面積雖然也隨 $k$ 指數成長，但 $k$ 是固定的架構參數（$k = 4$），於是任何函數（無論多複雜，只要 $\le k$ 變數）的實現深度都是**常數 1**：

$$t_{pd} = t_{\text{LUT}} = \text{const}, \quad \text{與函數複雜度無關}$$

複雜函數則拆成多個 LUT 串接，延遲與拆分後的層數成正比：

$$t_{pd} = L \cdot t_{\text{LUT}}, \quad L = \text{LUT 層數}$$

對照表如下：

| | 乘積項（CPLD） | LUT（FPGA） |
|---|---|---|
| 面積隨 $n$ | 陣列 $\propto n \times 2^n$（實作上 $n$ 受限） | $\propto 2^k$，$k$ 固定 |
| 單級可實現函數 | $\le m$ 個乘積項的 SOP | 任意 $k$ 變數函數 |
| 延遲 | 淺層寬邏輯：極小 | 與 LUT 層數 $L$ 成正比 |
| 複雜函數 | 需借項/拆級，不確定 | 均勻拆分，確定 |
| 大規模資料路徑 | 失效（項爆炸） | 適配良好 |

FLEX 8000 選 $k = 4$ 不是偶然：Berkeley 的研究（Rose et al., 1990）證明 $k=4$ 在面積與速度的乘積上接近最優。

### 線索二：FLEX 的 LE 與 FastTrack 互連

FLEX 8000 的邏輯單元（Logic Element, LE）結構：

- **LUT**：4 輸入查找表，實現組合函數；
- **可程式暫存器**：可設為 D-FF/T/JK/鎖存器，時脈可旁路；
- **進位鏈與級聯鏈**：LUT 之間的專用快速路徑（詳見線索四）；
- **LAB**：8 個 LE 為一組，共享 local interconnect（CPLD 血統的殘留）。

互連採用「FastTrack」連續式布線（continuous routing）：整片晶片鋪設橫縱貫穿的行（row）與列（column）匯流排，LE 經局部互連接入 FastTrack。與 Xilinx XC4000 的分段式（segmented）布線相比，FastTrack 的每段長度固定，延遲更可預測：

$$t_{\text{net}}^{\text{FastTrack}} \approx t_{\text{local}} + t_{\text{row/col bus}} = \text{分段常數}$$

這是 Altera 的推理：把 CPLD 的「確定性」哲學帶進 FPGA 布線層——布線資源是連續均勻的，任何兩點間延遲是可查表的常數，時序收斂（timing closure）因此更容易。

### 線索三：SRAM FPGA 的組態載入流程與時序

SRAM 組態意味着 FLEX 8000 每次上電都必須載入 bitstream。標準流程（串列被動組態模式，配 Altera EPC 串列配置 PROM）：

1. **上電復位**：$\text{nCONFIG}$ 拉低 → 內部復位，所有 I/O 三態；
2. **釋放**：$\text{nCONFIG}$ 拉高 → FPGA 釋放 $\text{nSTATUS}$，輸出 $\text{DCLK}$ 時脈；
3. **串列載入**：EPC PROM 在 DCLK 每個上升沿送出 1 位元資料（$\text{DATA}_0$）；
4. **完成**：全部位元載入後 FPGA 拉高 $\text{CONF\_DONE}$，進入初始化；
5. **生效**：初始化完成，I/O 依組態啟用，邏輯開始工作。

時序模型：

$$t_{\text{config}} = \frac{N_{\text{bits}}}{f_{\text{DCLK}}} + t_{\text{init}}$$

以 FLEX 81188（約 24,800 邏輯單元等級）為例，bitstream 約數 Mb 級，DCLK 典型 $4 \sim 10\,\text{MHz}$：

$$t_{\text{config}} \approx \frac{4 \times 10^6 \text{ bits}}{8\,\text{MHz}} + t_{\text{init}} \approx 500\,\text{ms} \sim \text{百 ms 級}$$

這數百 ms 的「空白期」對系統設計的影響是深遠的：板子上必須有其他元件（CPLD、微控制器或復位晶片）在這段期間接管復位與匯流排控制。這正是本案續集——CPLD 與 FPGA 分工——的系統學基礎。$\text{CONF\_DONE}$ 之後、I/O 生效之前，還要滿足復位釋放時序：

$$t_{\text{su}}(\text{reset release}) > t_{\text{init}} + t_{\text{skew}}$$

### 線索四：深寬電路在兩種架構下的延遲對比

以 32-bit 加法器為檢驗案例。波動進位加法器（RCA）的延遲：

$$t_{\text{RCA}}(n) = n \cdot t_{\text{carry}} + t_{\text{sum}}$$

- **CPLD（MAX）**：32-bit 加法需要多級 SOP 拆分。每級只能處理少數位元的進位方程（因為乘積項陣列的 fan-in 受限），拆分層數 $L \approx 4 \sim 8$，且每級都需穿越 PIA：

$$t_{\text{CPLD}} \approx L \cdot (t_{\text{macro}} + 2 t_{\text{PIA}}) \approx \text{數百 ns}$$

- **FPGA（FLEX）**：專用進位鏈（carry chain）把相鄰 LE 的 LUT 串接成快速進位路徑，進位延遲遠小於經 FastTrack 的延遲：

$$t_{\text{FLEX}} \approx 32 \cdot t_{\text{carry-chain}} \approx \text{數十 ns}$$

| 電路 | CPLD（MAX 7000 級） | FPGA（FLEX 8000 級） | 關鍵差異 |
|---|---|---|---|
| 8-bit 加法器 | ~50 ns（1-2 級 PIA） | ~15 ns（進位鏈） | 兩者皆可 |
| 32-bit 加法器 | ~300 ns（多級拆分） | ~40 ns（進位鏈） | CPLD 項爆炸，FPGA 勝 |
| 16-bit 計數器 | 項借用緊張 | 進位鏈直通 | FPGA 勝 |
| 32:1 解碼器（寬） | 1 級即成，~20 ns | 需 2-3 層 LUT | CPLD 勝（淺寬邏輯） |
| 狀態機（少量狀態） | 快，確定 | 稍慢但可 | 視規模 |

結論是清晰的分工律：**延遲與「寬度×深度」的乘積有關**。CPLD 在深度 1 的寬邏輯上無敵；深度 $> 2$ 或位寬 $> 16$ 的資料路徑，LUT + 進位鏈架構壓倒性勝出。FLEX 8000 正是為後者而生。

## 結案 -- 後果與影響

FLEX 8000 之後，Altera 全面轉向 SRAM LUT 路線（FLEX 10K 於 1995 年加入嵌入式 EAB 記憶體，1998 年的 Apex、2002 年的 Stratix 都沿此血統），CPLD 退居二線（MAX 系列持續供貨但不再是主角）。這是半導體史上少見的「自我否定成功案例」：Altera 沒有為了保護 CPLD 現金流而錯過 LUT 時代。

- 確立「LUT $k=4$ + 專用進位鏈 + 連續式布線」為 1990 年代 FPGA 架構的主流配方；
- 組態載入流程（nCONFIG/nSTATUS/CONF_DONE + 串列 EPC PROM）成為產業標準，Altera 的配置協定延用至今日的 Cyclone 系列；
- Lucent ORCA、其後 Atmel AT40K 等跟進，證明 SRAM LUT 已是共識而非 Xilinx 專利；
- CPLD 與 FPGA 的分工律（淺寬 vs 深寬）成為架構選擇的教科書結論。

## 關鍵人物與文獻

- Ross Freeman、William Carter —— Xilinx LUT 概念的提出者（1984-85），本案的學理源頭
- Jonathan Rose 等 —— Berkeley ACT 計畫，"Architecture of Field-Programmable Gate Arrays"（Proc. IEEE, 1990），$k=4$ LUT 的學理最優性
- Altera, "FLEX 8000 Datasheet"（1992）—— LE/FastTrack/組態流程的第一手文獻
- Lucent Technologies, "ORCA Series FPGAs"（1993）—— 跟進者
- S. Brown, J. Rose, "Architecture of FPGAs and CPLDs: A Tutorial"（IEEE Design & Test, 1996）
- Altera, "Configuring FLEX 8000 with EPC Devices" Application Note —— 組態時序細節
