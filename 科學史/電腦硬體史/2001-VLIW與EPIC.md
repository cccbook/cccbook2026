# 2001 - VLIW 與 EPIC：Itanium 的極端實驗

## 案件摘要
2001 年，Intel 與 HP 合資的 **Itanium（IA-64）** 正式上市——
史上最大的賭注：把**指令排程完全從硬體移到編譯器**，
一條 **128-bit bundle** 打包 3 條指令，靠 **EPIC**（Explicitly Parallel Instruction Computing）
的 predication 與 speculation 消滅分支。
VLIW 的源頭是 Josh Fisher 在 1980 年代的 Multiflow Trace 超級電腦。
結果：**Itanium 沉船（「Itanic」）**，但 VLIW 在 **DSP、印表機、AI 加速器**找到第二人生。
**本案偵辦重點：一個理論上完美的架構，為什麼會輸給「不完美」的超標量？**

## 前因 -- 為什麼會有這個案子
- **超標量的罩門（1990s）**：亂序執行（OoO）需要在硬體裡做**動態排程**——
  重命名暫存器、保留站（reservation station）、ROB、依賴追蹤電路——
  這些電路的複雜度與功耗隨發射寬度**超線性**成長：
  $$\text{排程電路面積} \sim O(w^2) \quad\Longrightarrow\quad 4\text{-wide 超標量已逼近功耗天花板}.$$
  而且**硬體在執行當下才知道相依關係**——決策時間只有幾個週期，排程品質受限。
- **VLIW 的關鍵推理（Josh Fisher, 1983–1984）**：
  > 「**編譯器有無限的時間分析程式，硬體只有幾個週期——把排程交給編譯器。**」
  編譯器在編譯期找出指令級並行（ILP），把**互不衝突的指令打包成超長指令字**（Very Long Instruction Word），
  硬體只需「解碼 → 並行發射」——**零動態排程電路**。
- **Multiflow Trace（1987）與 Cydrome（1987）**：Fisher 的 VLIW 公司做出 7-wide 機器，
  ILP 表現驚人，但**公司倒閉**（市場太小、二進位相容性為零）——技術正確、商業錯誤的前車之鑑。
- **HP PA-RISC 的超長字實驗**：HP 在 1990 年代發現 PA-RISC 加寬到極限，
  於是找上 Intel 合資——**IA-64 = VLIW 理論 + Intel 的市場力量**。
- **1994 年宣布的震撼**：Intel 公開宣布 x86 的未來是 IA-64，
  所有 RISC 廠商（HP/SGI/DEC）紛紛表態跟進——**整個業界押注 VLIW**。

## 線索與推理 -- 數學式、程式、理論

### 第一條線索：bundle 寬度與 ILP 的數學
VLIW 的性能上限由**程式本身的 ILP** 決定——編譯器能找到多少互不依賴的指令：
$$\text{理想加速} = \min\left(\text{發射寬度 } w, \; \text{平均 ILP}\right) \times \text{頻率因子}.$$
- Itanium 2（2002）：**6 個發射埠**（每 bundle 3 指令，最多 2 bundles/週期），
  峰值每週期 6 條指令——但**真實程式的平均 ILP 只有 1.5–2.5**（分支、記憶體相依、資料相依）。
- **推論**：VLIW 的好壞完全取決於編譯器與程式碼的「可並行性」——
  科學計算（規律迴圈）ILP 高，通用程式碼（指標、分支）ILP 低：
  $$\text{實際 IPC} = \text{ILP}_{avg} \approx \begin{cases} 2\text{–}4 & \text{數學運算核心} \\ 1\text{–}2 & \text{通用程式碼} \end{cases}$$

### 第二條線索：EPIC 三件套 — predication、speculation、bundle template
Itanium 不只是 VLIW，而是加料版 **EPIC**：
- **Predication（述詞執行）**：把 if/else 轉成「**兩邊都算，靠條件碼取捨**」——
  $$\text{if } (p)\; a=b+c \text{ else } a=b-c \quad\xrightarrow{\text{predication}}\quad
  (p_{T})\; t_1=b+c;\;\; (p_{F})\; t_2=b-c;\;\; a = p_T? t_1 : t_2.$$
  **分支徹底消失**：沒有 branch，就沒有 mispredict penalty——這是消除分支的數學解法。
  代價：兩邊都要執行，若一方有副作用或代價大，反而更慢。
- **Speculation（編譯器式投機）**：編譯器把 load 提前到分支之前執行（`ld.s` 標記），
  若猜錯觸發例外就丟棄結果——**把硬體的推測執行搬到編譯器**。
- **Bundle template**：128-bit bundle 內含 template bits，宣告 3 條指令的**執行埠類型**
  （整數/浮點/記憶體/分支）——硬體解碼器不必再猜，**排程資訊顯式寫在指令裡**（EPIC 的「E」）。

### 第三條線索：編譯器排程 vs 硬體排程的取捨
| 面向 | 編譯器排程（VLIW/EPIC） | 硬體排程（超標量 OoO） |
|------|------------------------|----------------------|
| 分析時間 | **無限**（編譯期，可跑數小時） | 幾個週期（執行期） |
| 視野 | **整個基本區塊/迴圈**（trace） | 指令窗口（數十～百條） |
| 硬體成本 | **極低**（無排程電路） | 高（$O(w^2)$ 電路 + 功耗） |
| 二進位相容 | **零**（換 CPU = 重新編譯） | 完整（舊程式直接跑） |
| 猜錯代價 | 錯誤路徑白白執行（predication） | 回滾 ROB（推測執行） |
| 可預測性 | 高（排程靜態固定） | 低（依賴 cache/動態行為） |
- **核心矛盾**：VLIW 的優勢（編譯期完美排程）正是它的死穴——
  **編譯器看不到執行期的 cache miss 與分支結果**，
  而**二進位相容性為零**意味著每代新 CPU 都要重編譯所有軟體。
  「**相容性 > 理論**」——這是本案最重要的判決。

### 第四條線索：Itanic 沉船與 x86-64 反擊
- **編譯器難寫（1997–2001）**：IA-64 的 EPIC 排程器號稱最難寫的編譯器之一——
  Intel 花了數年才勉強達標，**首次上市時性能竟輸給同期的 Pentium III/4**。
- **Itanium 2（2002）**：性能終於達標（SPECfp 表現優異），但**售價數千美元、功耗破百瓦**，
  生態只有 HPC/伺服器小眾市場。
- **AMD 的反擊（2003）**：AMD 推出 **x86-64（AMD64，Opteron）**——
  **直接擴充 x86 為 64-bit，完整相容舊軟體**。Itanium 的教訓被 AMD 用來反殺：
  $$\text{AMD64} = \text{x86 相容} + 64\text{-bit} \quad\Longrightarrow\quad \text{市場全勝（2004 微軟支援 AMD64 而非 IA-64）。}$$
- **「Itanic」沉沒（2000s–2021）**：媒體以鐵達尼號戲稱 Itanium——
  2021 年 Intel 正式停產，總銷量不到預期的 1%。
  **業界史上最大的架構賭注以失敗告終。**

### Python：VLIW bundle 模擬（編譯器式排程）

```python
from collections import defaultdict

def schedule_vliw(instrs, width=3, latencies=None):
    """編譯器式 list scheduling：依相依圖拓撲排序，
    把無相依衝突的指令打包成 width-wide bundles，回傳 bundles 與 ILP"""
    latencies = latencies or {}
    deps = {}       # instr index -> 依賴的 instr indices（讀寫與寫寫衝突）
    last_writer = {}
    for i, (op, dst, *srcs) in enumerate(instrs):
        deps[i] = set()
        for s in srcs + [dst]:
            if s in last_writer:
                deps[i].add(last_writer[s])
        last_writer[dst] = i
    ready_time = [0] * len(instrs)   # 每條指令最早可發射時間
    done = set()
    bundles, cycle = [], 0
    while len(done) < len(instrs):
        bundle = []
        for i in sorted(deps, key=lambda x: ready_time[x]):
            if i in done or len(bundle) >= width: continue
            if all(d in done or ready_time[d] <= cycle for d in deps[i]) and \
               all(d in done for d in deps[i] if latencies.get(instrs[d][0],1) > 0):
                bundle.append(i)
        if not bundle:
            cycle += 1; continue
        for i in bundle:
            ready_time[i] = cycle + latencies.get(instrs[i][0], 1)
            done.add(i)
        bundles.append((cycle, bundle))
        cycle += 1
    return bundles

# 基本區塊：a = b+c; d = e+f; g = a+d; h = b*2; i = g+h
instrs = [("add","a","b","c"), ("add","d","e","f"), ("add","g","a","d"),
          ("mul","h","b","2"), ("add","i","g","h")]
lat = {"add":1, "mul":2}
bundles = schedule_vliw(instrs, width=3, latencies=lat)
total = len(instrs)
print(f"5 條指令 → {len(bundles)} 個 bundles:")
for cyc, b in bundles:
    print(f"  cycle {cyc}: {[instrs[i] for i in b]}")
print(f"ILP = {total/len(bundles):.2f} 條指令/bundle（發射寬度 3，硬體無需動態排程）")
```
輸出：
```
5 條指令 → 3 個 bundles:
  cycle 0: [('add', 'a', 'b', 'c'), ('add', 'd', 'e', 'f'), ('mul', 'h', 'b', '2')]
  cycle 1: [('add', 'g', 'a', 'd')]
  cycle 2: [('add', 'i', 'g', 'h')]
ILP = 1.67 條指令/bundle（發射寬度 3，硬體無需動態排程）
```
（偵辦結論：編譯器把 5 條指令排成 3 個 bundles——**前三條互不依賴，一個 bundle 並行發射**；
但依賴鏈 `a→g→i` 強迫分成 3 個週期，**ILP 只有 1.67**，發射寬度 3 有一半是浪費——
**Itanium 的死因：真實程式碼的 ILP 根本填不滿 bundle**。）

## 結案 -- 後果與影響
- **Itanium 的教訓（2001–2021）**：理論上完美的架構敗給三個現實——
  **編譯器太難寫、二進位相容性為零、真實程式 ILP 不夠**。
  Intel 投入數十億美元，最後在 2021 年正式停產——**「Itanic」是架構史最大沉船**。
- **AMD x86-64 反擊成功（2003）**：AMD64 證明「**相容性擴充**」勝過「**推倒重來**」——
  Intel 2004 年被迫採用 AMD 的 x86-64（改名 Intel 64），
  **這是 Intel 第一次在 ISA 戰爭中向 AMD 低頭**（見「1978-Intel8086.md」的相容性護城河）。
- **超標量 + 亂序仍是主流**：x86 與 ARM 的桌上型/伺服器 CPU 至今都是
  亂序執行 + 推測執行 + 分支預測（見「1991-分支預測.md」）——
  **硬體排程雖然昂貴，但「舊程式直接跑」的價值碾壓一切理論優勢**。
- **VLIW 的勝利戰場（嵌入式與 DSP）**：在**單一程式、無相容性包袱**的領域，VLIW 大放異彩：
  - **DSP**：TI C6x 系列（1997–）就是 VLIW——訊號處理迴圈的 ILP 極高。
  - **印表機/多媒體**： Philips TriMedia、Transmeta Crusoe（用 VLIW + 軟體模擬 x86）。
  - **AI 加速器**：**Qualcomm Hexagon**（手機 DSP/NN）、Google TPU 的標量單元、
    許多 NPU 都是 VLIW 風格——**固定的規律運算正是 VLIW 的主場**。
- **predication 存活至今**：ARM 的條件執行（conditional execution）、
  RISC-V/AVX-512 的 mask 暫存器、GPU 的 predicate——**消除分支的思想處處可見**。
- **AI 時代的新 VLIW 浪潮**：AI 加速器的「規律矩陣運算 + 編譯器排程 + 無相容性包袱」
  讓 VLIW 重獲新生——**Itanium 輸掉的戰場，正是 AI 晶片贏回的戰場**（見「2012-GPU深度學習算力.md」）。
- 歷史定位：VLIW vs 超標量是「**編譯期智慧 vs 執行期智慧**」的取捨——
  答案不是二選一：**通用 CPU 用硬體排程，專用加速器用編譯器排程**，各據一方。

## 關鍵人物與文獻
- **Josh Fisher**：VLIW 之父（ Yale 博士論文 1979、JHU 1983）；Multiflow Trace（1987）創辦人；
  《Embedded Computing: A VLIW Approach to Architecture, Compilers and Tools》(2005)。
- **Glenford Myers**：Multiflow 共同創辦人；VLIW 編譯器工程先驅。
- **Bob Rau**：Cydrome 創辦人、polynomial loop transformation（軟體流水線理論）。
- **V. Kathail, M. Schlansker, B. Rau**：EPIC 架構論文（HP Labs, 1990s）。
- **D. Patterson & J. Hennessy**：《Computer Architecture: A Quantitative Approach》
  對 VLIW 的批判與鐵達尼隱喻。
- **AMD（Dirk Meyer 團隊）**：x86-64/AMD64（2003，Opteron/Athlon 64）。
- 相關案件：`1981-CISC與RISC之戰.md`、`1978-Intel8086.md`、
  `1991-分支預測.md`、`2012-GPU深度學習算力.md`、`2007-多核心CPU.md`。
