# 1990s - 硬體模擬與 Emulation：在 tapeout 之前開機的偵探術

## 案件摘要
1990 年代，晶片規模衝上千萬閘，軟體模擬器每秒只能跑幾千個 cycle——boot 一個作業系統要跑上好幾天，
等模擬完才發現 bug，tapeout 已經晚了一年。硬體加速器（Zycad）與 FPGA-based emulation（QuickTurn 1989）
把被測電路「搬進」真實硬體，以 MHz 級速度重現晶片行為；Cadence Palladium（1997）與 Mentor Veloce
接棒，使「在 tapeout 之前就 boot OS、跑真實軟體」成為先進晶片的標準偵探程序。

## 前因 -- 為什麼會有這個案子
- **軟體模擬太慢**：event-driven simulator 在工作站上每秒模擬數百到數千個 cycles；一顆 1000 萬閘 SoC 的 reset 序列＋boot OS 需 $10^9$ 個 cycle，單純軟體模擬要數天到數週。
- **mask 失敗代價驚人**：1990 年代一次 tapeout 失敗動輒數十萬美元、延誤一季產品窗口；許多 bug（軟硬體互動、DMA 競爭、interrupt 時序）只有跑真實軟體才抓得到。
- **凶器已有兩個來源**：Zycad（1980s）用**客製處理器**映射閘級電路做 simulation acceleration；QuickTurn（1989, Haque 等人）改用**現成 FPGA**，把 DUT 分割到多顆 FPGA 上做 emulation——速度MHz級，成本更低、更快上市。
- **關鍵推理**：三種速度階層各司其職，構成一個驗證金字塔：

$$
\underbrace{\text{軟體模擬}}_{\text{kHz，全可見}} \;\ll\; \underbrace{\text{Emulation / 加速器}}_{\text{MHz 級，可 replay}} \;\ll\; \underbrace{\text{FPGA prototype}}_{\text{10s MHz，跑真實環境}}
$$

快的抓數量（跑得遠），慢的抓品質（看得深）——驗證策略就是在速度與能見度之間做取捨。

## 線索與推理 -- 數學式、程式、理論

### 1. 案件現場：模擬速度的三個階層

| 階層 | 速度（每秒 cycles） | 能見度 | 典型用途 |
|------|--------------------|--------|----------|
| 軟體 event-driven simulator | $10^3$–$10^4$ | 100%（每個訊號每刻） | 單元/RTL 驗證、debug |
| Simulation acceleration | $10^4$–$10^5$ | 100%（可切換 trace） | testbench 加速、迴歸 |
| Hardware emulation | $10^6$（MHz 級） | 選擇性 trace | boot OS、軟硬體協同 |
| FPGA prototyping | $10^7$–$10^8$ | 有限（需加邏輯分析儀） | 驅動程式開發、系統展示 |

模擬時間估算：一顆 $10^7$ 閘的 SoC 要 boot Linux 約 $10^9$ cycle，event-driven simulator 以 $10^3$ cycles/s 計需 $10^6$ 秒 ≈ **12 天**；emulation 以 $10^6$ cycles/s 計只需 **17 分鐘**。

### 2. Emulation 的架構：把閘映射到處理器或 FPGA

兩條技術路線，目標相同：

- **Custom processor（Zycad → Palladium）**：每顆晶片內含數萬個簡化的「模擬處理器」，每個處理器可編程為一個或數個邏輯閘（ truth table + 4 個輸入），以 pipeline 方式每 clock 評估一層邏輯。Palladium（1997）用這種架構達到數百萬 cycles/s。
- **FPGA-based（QuickTurn → Veloce 的早期路線）**：把 DUT 的閘級網表**分割**到多顆 FPGA，每顆 FPGA 以硬描述方式綜合出真實電路，速度受 FPGA 內部延遲與跨 FPGA 接線限制，通常 0.5–5 MHz。

**In-circuit emulation（ICE）**：emulator 透過速度橋接器（rate adapter）接到**真實**的介面（PCI、Ethernet、DRAM），讓 DUT 與真實世界互動——bug 現場不再是合成的 testbench，而是真實驅動程式與真實資料。

### 3. Partitioning 演算法：FPGA 資源約束下的圖分割

把閘級網表 $G = (V, E)$ 分割到 $k$ 顆 FPGA，每顆有資源上限（look-up table 數、I/O pin 數）：

$$
\min \sum_{e \in E} \mathbb{1}[\text{cut}(e)] \quad \text{s.t.} \quad |V_i| \le C_{\text{LUT}},\; |\text{I/O}_i| \le C_{\text{pin}}
$$

跨 FPGA 的每一條 cut 邊都會吃掉兩個 I/O pin 並增加延遲，因此目標是**最小割（min-cut）**。**Kernighan–Lin 演算法（1970）**是兩路分割的經典啟發式：
1. 對每個節點計算 $D_v = E_{\text{ext}}(v) - E_{\text{int}}(v)$（外部連接 − 內部連接）。
2. 嘗試所有 $(a, b)$ 對調，計算增益 $g = D_a + D_b - 2\,c(a,b)$。
3. 選最大增益的對調，鎖定該兩節點，重複直到全部鎖定。
4. 取過程中最大的累積增益 $\max_k \sum_{i \le k} g_i$ 作為最終分割，重複整輪直到不再改進。

複雜度每輪 $O(n^3)$（Fiduccia–Mattheyses 1982 改進為 $O(|E|)$）。I/O pin 約束是 emulation 特有的難點：就算 LUT 夠，pin 不夠就放不下，因此實務工具必須同時最佳化兩種資源。

### 4. 跨 FPGA 接線 overhead：分區的代價

分割後總延遲為：

$$
T_{\text{emul}} = \sum_{i} T_{\text{FPGA},i} + \sum_{e \in \text{cut}} T_{\text{wire}}(e) \gg T_{\text{silicon}}
$$

每條 cut 邊經過 FPGA I/O、PCB 走線、對方 FPGA I/O，延遲約 5–20 ns——比矽晶片內部慢 10–50 倍，這就是 emulation 只有 MHz 級速度的根本原因。實務解法：
- **Min-cut partitioning + 管線化**：把跨 FPGA 路徑切成多級 pipeline，用「多拍」換「單拍快」。
- **時序模型預測**：在分割階段就用延遲模型估 $T_{\text{emul}}$，把熱點（高 cut 密度）重新分配。
- **多條 scan chain 互通**：emulator 也借用 DFT 的 scan 技術做 debug，重現某個 cycle 的完整狀態。

### 5. Co-simulation：快慢混合的偵探團隊

真實驗證很少「純 emulation」：testbench 中的 CPU 模型、memory model 跑在軟體模擬器（慢但好寫），
DUT 的 RTL/閘級網表跑在 emulator（快但難改），兩者以 **co-simulation 環境**同步：

$$
\text{Testbench（軟體）} \xleftrightarrow{\;\text{co-sim bus}\;} \text{Emulator（硬體）} \xleftrightarrow{\;\text{ICE}\;} \text{真實世界}
$$

同步的關鍵是 **cycle-accurate handshake**：軟體端與硬體端每個模擬 clock 交換一次事件，軟體慢就讓硬體等待。QuickTurn 的 SpeedBridge、Cadence 的 Palladium co-modeling interface 都是這種架構。

### 6. Python 實作：簡化的 Kernighan–Lin 兩路分割

```python
from itertools import combinations

def kernighan_lin(edges, n_nodes):
    """兩路 min-cut 分割（KL 演算法），回傳兩分區與割邊數"""
    adj = {v: {} for v in range(n_nodes)}
    for u, v in edges:
        adj[u][v] = adj[v][u] = adj[u].get(v, 0) + 1
    A = set(range(n_nodes // 2))                       # 初始對半
    B = set(range(n_nodes)) - A
    for _ in range(n_nodes):                           # 最多 n 輪
        side = lambda v: A if v in A else B
        D = {v: sum(w for o, w in adj[v].items() if o not in side(v))
                - sum(w for o, w in adj[v].items() if o in     side(v))
             for v in range(n_nodes)}
        a_free, b_free, swaps = set(A), set(B), []
        while a_free and b_free:                       # 每步鎖定最大增益的對調
            g, a, b = max((D[a] + D[b] - 2 * adj[a].get(b, 0), a, b)
                          for a in a_free for b in b_free)
            swaps.append((a, b, g))
            a_free -= {a}; b_free -= {b}
            for x in a_free: D[x] += 2 * adj[x].get(b, 0)   # 對調後更新 D
            for x in b_free: D[x] += 2 * adj[x].get(a, 0)
            D[a] = D[b] = -9999
        cum, k_best = 0, -1                            # 取最佳累積增益前綴
        for i, (_, _, g) in enumerate(swaps):
            cum += g
            if cum > 0 and (k_best < 0 or cum > sum(s[2] for s in swaps[:k_best + 1])):
                k_best = i
        if k_best < 0:
            break
        for a, b, _ in swaps[:k_best + 1]:             # 執行前 k_best 步對調
            A, B = (A - {a}) | {b}, (B - {b}) | {a}
    cut = sum(1 for u, v in edges if (u in A) != (v in A))
    return A, B, cut

edges = [(0,1),(1,2),(2,3),(3,0),(0,2),(4,5),(5,6),(6,7),(7,4),(2,6),(3,7)]
A, B, cut = kernighan_lin(edges, 8)
print(f"A = {sorted(A)}, B = {sorted(B)}, cut = {cut}")
# 預期輸出：A = [0, 1, 2, 3], B = [4, 5, 6, 7], cut = 2
# （兩個 4-clique 各自完整保留，僅 (2,6) 與 (3,7) 跨界——min-cut = 2）
```

兩個緊密連接的 4-clique 被分到兩顆 FPGA，只有 2 條邊跨 FPGA——
這正是 QuickTurn 分割演算法想要達成的效果：少割線、少 pin、少延遲。

## 結案 -- 後果與影響
- **Pre-silicon software validation 成為標準**：boot OS、跑驅動程式、真實資料流驗證在 tapeout 之前完成，1990 年代末大型 SoC 幾乎必配 emulation。
- **Tapeout 前抓 bug**：軟硬體互動 bug、時序競爭、整合問題在硬體上重現並 replay，mask 失敗率大降。
- **現代三強成形**：Cadence Palladium（1997，客製處理器路線）、Siemens EDA（原 Mentor）Veloce（2004 起，混合架構）、Synopsys ZeBu（FPGA/處理器混合），至今仍是 emulation 市場三強。
- **Replay & debug 是核心價值**：emulation 能在任何 cycle 停下、dump 全狀態、回放歷史——這是 prototype（速度快但難 debug）做不到的。
- **驗證金字塔延續至今**：軟體模擬（kHz）→ emulation（MHz）→ FPGA prototype（10s MHz）→ silicon（GHz）的四層速度階層，仍是今日晶片驗證的標準分工。

## 關鍵人物與文獻
- **Zycad**（1980s）：事件驅動模擬加速器的先驅，客製處理器映射閘級電路。
- **Naveed Haque、Murthy Chetry** 等：QuickTurn（1989）創辦團隊，FPGA-based emulation 與 SpeedBridge 的發明者。
- **Cadence**：Palladium（1997，收購 Ambit/QuickTurn 技術路線後整合）；Palladium XP 至今仍是 emulation 主力。
- **Mentor Graphics（現 Siemens EDA）**：Veloce（2004 起），FPGA-based emulation 與 Veloce virtuafeb。
- **Brian Kernighan、Shen Lin**：「An Efficient Heuristic Procedure for Partitioning Graphs」（*Bell System Technical Journal*, 1970）：KL min-cut 演算法。
- **C. M. Fiduccia、R. M. Mattheyses**：「A Linear-Time Heuristic for Improving Network Partitions」（DAC 1982）：FM 改進版。
- **Janick Bergeron**：*Writing Testbenches: Functional Verification of HDL Models*（Kluwer, 2000）：驗證方法學的奠基教科書。
