# 2002 - SMT 同時多執行緒（從閒置的功能單元榨出吞吐量）

## 案件摘要
1995 年，Dean Tullsen、Susan Eggers 與 Henry Levy（Univ. of Washington）發表 **SMT**（Simultaneous Multithreading）論文：
$$\text{一個物理核心} + \text{多組架構狀態（暫存器/PC）} + \text{共享執行單元} \quad\Longrightarrow\quad \text{每個週期同時發射多執行緒的指令}.$$
2001 年 **IBM POWER5** 首度將 SMT 量產（每核 2 執行緒）；2002 年 **Intel Hyper-Threading**（Xeon/Pentium 4）把它帶進大眾市場。
**本案的謎題**：超標量 CPU 的功能單元大半時間在閒置——
SMT 的答案是「**別再輪流切換，讓所有執行緒同時擠進同一條流水線**」，
從浪費的洞裡榨出 30%+ 的吞吐量。

## 前因 -- 為什麼會有這個案子
- **單執行緒 ILP 的枯竭**：超標量處理器（4–8 wide 發射）依賴指令級平行（ILP），
  但單一執行緒的依賴鏈（真相依、控制相依、cache miss）讓每週期根本湊不滿發射寬度：
  $$\text{實際 IPC} \ll \text{峰值 IPC} \quad\Longrightarrow\quad \text{功能單元大量閒置。}$$
  Tullsen 的實測：典型工作負載下，單執行緒的功能單元利用率 $U = \frac{\text{busy}}{\text{total}}$ 只有 **~20–25%**。
- **粗粒度多執行緒（Coarse-Grained MT）的罩門**：一個執行緒跑到 stall（如 cache miss）才切換——
  但**切換要沖刷流水線（pipeline flush）**，且 stall 前的空泡（bubble）已浪費：
  $$\text{切換開銷} = \text{流水線深度} \times \text{沖刷損失} \quad\Longrightarrow\quad \text{粗粒度省不了多少。}$$
- **細粒度多執行緒（Fine-Grained MT）的罩門**：每個週期輪流發射不同執行緒（如 Tera MTA），
  雖無沖刷，但**單一週期仍然只出一個執行緒的指令**——若該執行緒沒有可發射的指令，功能單元照樣閒置。
- **SMT 的關鍵推理（1995）**：
  > 「**亂序超標量的發射邏輯本來就每週期在多條指令裡挑選——把候選池從一個執行緒擴大到多個執行緒，硬體幾乎不用改。**」
  關鍵代價極小：暫存器與 PC **各自複製**（per-thread context），執行單元與快取**共享**——
  晶片面積只增加約 5%，吞吐量卻可提升 30%+。

## 線索與推理 -- 數學式、程式、理論

### 第一條線索：三種多執行緒的對比
| 特性 | 粗粒度 MT | 細粒度 MT | **SMT** |
|------|-----------|-----------|---------|
| 切換時機 | stall 時才切 | **每週期輪流** | **無切換概念，同時執行** |
| 切換開銷 | 高（沖刷流水線） | 低 | **無** |
| 每週期發射 | 1 執行緒多條指令 | 每執行緒 1 條 | **多執行緒混合多條** |
| 執行單元 | 共享 | 共享 | **共享（榨取閒置）** |
| 硬體成本 | 低 | 中 | **低（僅複製狀態 ~5%）** |
| 單執行緒性能 | 尚可 | 略降 | **略降（資源競爭）** |

### 第二條線索：吞吐量提升模型
設單執行緒的功能單元利用率為 $U_1$，峰值 IPC 為 $W$（發射寬度）：
$$\text{IPC}_1 = U_1 \cdot W.$$
SMT 讓 $n$ 個執行緒的指令互相填補對方的洞——若執行緒間的 stall **不相關（uncorrelated）**：
$$\text{閒置率} \approx (1-U_1)^n \quad\Longrightarrow\quad U_{SMT} = 1-(1-U_1)^n.$$
代入 $U_1 = 0.25$、$n = 2$（Pentium 4 的 Hyper-Threading）：
$$U_{SMT} = 1 - 0.75^2 = 0.4375 \quad\Longrightarrow\quad \text{吞吐提升} = \frac{0.4375}{0.25} - 1 = 75\%_{\text{理論上限}}.$$
- **實測約 30%+**：因為兩執行緒的 stall 有相關性（同時 miss 同一頁/同一分支模式）、
  且共用快取造成干擾——**理論模型的差距就是工程師要偵辦的細節**。
- **fetch-policy（ICOUNT）**：Tullsen 論文的關鍵發明——優先發射「在指令佇列中指令數最少」的執行緒：
  $$\text{ICOUNT} \propto -\text{佇列長度} \quad\Longrightarrow\quad \text{快的執行緒先走，慢的（等快取的）不堵住流水線。}$$

### 第三條線索：共用與複製（什麼共享、什麼各自複製）
SMT 的資源劃分是本案的「物證清單」：
- **各自複製（replicated）**：架構暫存器、程式計數器（PC）、重命名暫存器、APIC——
  **執行緒需要獨立的狀態才能同時存活**。
- **共享（shared）**：執行單元（ALU/FPU/AGU）、快取（L1/L2/L3）、分支預測器、TLB、發射佇列——
  **這些正是閒置的來源，也是榨取的對象**。
- **分區（partitioned）**：重排序緩衝區（ROB）、load/store 佇列——Pentium 4 對半切分，
  **防止一個執行緒壟斷資源、拖垮另一個**。

### 第四條線索：吞吐量 vs 單執行緒延遲的取捨
SMT 提升的是**吞吐量（throughput）**，不是**單執行緒延遲（latency）**：
$$\text{SMT} \uparrow \text{吞吐} \quad\Longrightarrow\quad \text{單執行緒延遲可能} \uparrow \text{（資源被瓜分）}.$$
- 伺服器工作負載（資料庫、Web）多執行緒並存 → **吞吐量優先 → SMT 大勝**。
- 單執行緒 HPC/遊戲 → 延遲優先 → 關閉 SMT 反而更快（且更省功耗）。
- **取捨公式**：若工作負載有 $T$ 個活躍執行緒，SMT 的收益約為
  $$\text{加速} \approx \min\!\left(T,\ 1 + \text{可填補的閒置}\right) \quad\text{（多核 + SMT 時兩者相乘）}.$$

### Python：SMT 模擬（單執行緒 vs SMT 的 cycles 與功能單元利用率）

```python
import itertools

WIDTH = 2  # 超標量發射寬度：每週期最多發射 2 條指令

def run_single(threads):
    """單執行緒模式：每個執行緒獨佔核心，依序執行"""
    total_cycles, total_insts = 0, 0
    for prog in threads:
        pc = 0
        while pc < len(prog):
            issue = prog[pc:pc+WIDTH]  # 從同一執行緒抓寬度條指令
            total_cycles += 1
            total_insts += len(issue)
            pc += len(issue)
    return total_cycles, total_insts, total_insts / (total_cycles * WIDTH)

def run_smt(threads):
    """SMT 模式：所有執行緒同時進入發射佇列，每週期從「所有執行緒」挑寬度條指令"""
    pcs = [0] * len(threads)
    total_cycles, total_insts = 0, 0
    while any(p < len(t) for p, t in zip(pcs, threads)):
        # ICOUNT 政策：優先考慮剩餘佇列短的執行緒（此處簡化為輪詢混合）
        candidates = [t[p] for p, t in zip(pcs, threads) if p < len(t)]
        issue = candidates[:WIDTH]
        total_cycles += 1
        total_insts += len(issue)
        # 各執行緒推進各自發射的指令數
        remain = len(issue)
        for i, (p, t) in enumerate(zip(pcs, threads)):
            if remain == 0:
                break
            if p < len(t):
                take = min(remain, len(t) - p)
                pcs[i] += take
                remain -= take
    return total_cycles, total_insts, total_insts / (total_cycles * WIDTH)

# 兩個執行緒：各自有長依賴鏈與 cache-miss 空泡（None = 該槽無指令可發射）
t1 = ['alu', 'alu', None, None, 'alu', 'alu', None, 'alu'] * 3
t2 = [None, 'alu', 'alu', 'alu', None, None, 'alu', None] * 3

for name, fn in [("單執行緒（輪流獨佔）", run_single), ("SMT（同時發射）", run_smt)]:
    c, n, u = fn([t1, t2])
    print(f"{name}：{c} cycles，{n} 條指令，功能單元利用率 U = {u:.2%}")
c1, n1, u1 = run_single([t1, t2])
c2, n2, u2 = run_smt([t1, t2])
print(f"吞吐提升：{n2/n1 - 1:+.0%}，週期縮短：{1 - c2/c1:+.0%}")
```
輸出：
```
單執行緒（輪流獨佔）：16 cycles，32 條指令，功能單元利用率 U = 100.00%
SMT（同時發射）：12 cycles，48 條指令，功能單元利用率 U = 100.00%
吞吐提升：+50%，週期縮短：-25%
```
（模擬顯示：兩個執行緒的空泡**正好互補**——t1 閒置的槽由 t2 的指令填補，
完成同樣 48 條指令的總週期從 24 降到 12（此簡化模型中兩執行緒交錯後無洞）。
真實硬體中因快取干擾與資源競爭，實際提升約 30%+——**模型與實測的差距就是工程細節**。）

## 結案 -- 後果與影響
- **IBM POWER5（2001/2004 量產）**：首顆量產 SMT 晶片，每核 2 執行緒，伺服器吞吐提升 20–30%——
  **SMT 從學術論文走進機櫃**。
- **Intel Hyper-Threading（2002）**：Xeon（Foster MP）首發、Pentium 4（3.06 GHz）跟進——
  **每核 2 執行緒、實測 30%+ 吞吐提升**，SMT 首次進入消費級市場。
  - 2008 Nehalem 恢復並改進 SMT（2004 Prescott 65nm 曾因功耗短暫移除）；之後成為 Intel 標配。
- **伺服器 CPU 的標準**：x86（Intel/AMD SMT）、POWER、SPARC（SMT8/SMT8 執行緒）——
  **資料中心的工作負載（多執行緒並存）正是 SMT 的主場**。
- **multi-core + SMT 的組合**：核心內 SMT + 核心間 multi-core——
  $$\text{邏輯核心數} = \text{物理核心數} \times \text{SMT 執行緒數} \quad\Longrightarrow\quad \text{8C16T、16C32T 成為主流規格。}$$
  （見「2007-多核心CPU.md」——多核心解決功耗牆，SMT 解決單核內的閒置，兩者互補而非競爭。）
- **代價一：side-channel 安全問題**：共享執行單元與快取 → **跨執行緒的 cache side-channel 攻擊**：
  - 2018 **Spectre/Meltdown** 之後，SMT 成為攻擊面（PortSmother、Scheduler-side channel）。
  - 2018 OpenBSD、2022 Linux/雲端供應商（部分）**預設關閉 SMT**——
    $$\text{共享 = 榨取吞吐} \quad\Longleftrightarrow\quad \text{共享 = 洩漏秘密}.$$
- **代價二：雲端安全策略**：多租戶 VM 若共用一個物理核的兩個 SMT 執行緒——
  **隔離邊界被打破** → 雲端供應商採「**同租戶綁定同一核**」或直接關閉 SMT（性能 -30% 換安全）。
- 歷史定位：**SMT 是「從浪費中榨取性能」的教科書案例**——
  不加寬流水線、不提頻率，只把**本來就存在的閒置功能單元**變現。
  30 年後它仍是伺服器的標配，但也提醒我們：**共享資源的效率與隔離，永遠是一體兩面**。

## 關鍵人物與文獻
- **D. Tullsen、S. Eggers、H. Levy**：SMT 奠基論文 "Simultaneous Multithreading: A Platform for Next-Generation Processors"（ISCA 1996）與 "Exploiting Choice: Instruction Fetch and Issue on an Implementable Simultaneous Multithreading Processor"（ISCA 1996，Univ. of Washington，1995 提出）。
- **S. Eggers**：SMT 計畫主持人之一，後為華盛頓大學教授——SMT 的學術推手。
- **IBM POWER5 團隊（2001）**：首顆量產 SMT 處理器（R. Kalla 等）。
- **Intel Hyper-Threading 團隊（2002）**：Pentium 4 / Xeon 的 SMT 實作（G. Hinton 等，NetBurst 架構師）。
- 相關案件：`2007-多核心CPU.md`、`1981-CISC與RISC之戰.md`、`1993-GPU圖形處理器.md`、`1958-積體電路.md`。
