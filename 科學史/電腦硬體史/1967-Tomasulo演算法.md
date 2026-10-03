# 1967 - Tomasulo 演算法（亂序執行與 register renaming 的誕生）

## 案件摘要
1967 年，IBM 的 Robert Tomasulo 在 **IBM System/360 Model 91** 的浮點單元中
發明了一個改變電腦史的演算法：
$$\text{register renaming} + \text{reservation station} + \text{CDB 廣播} \quad\Longrightarrow\quad \text{亂序執行，hazard 消失}.$$
**破案關鍵**：Tomasulo 發現 stall 的元凶不只是**真相依（RAW）**，
還有**假相依（WAR/WAW）**——而假相依可以用「暫存器重命名」直接消除。
這套機制在 1960 年代默默運行了二十多年，
直到 **1995 年 Pentium Pro（P6 微架構）** 復活它，成為**現代所有 CPU 的標準配備**。

## 前因 -- 為什麼會有這個案子
- **in-order 執行的罩門**：流水線機器（見 CDC 6600 scoreboard）按順序發射指令，
  一旦遇到 **RAW 相依**，整條流水線必須 stall 等待：
  $$\text{stall 週期} = \text{功能單元延遲} - \text{可用填充週期}.$$
  浮點除法延遲約 20 週期——一個除法可以讓**整條流水線停擺 20 週期**，浪費極大。
- **假相依的冤案**：WAR 與 WAW 只是**暫存器不夠用**造成的名字衝突，
  與資料的真實流向無關：
  $$\text{WAR/WAW} = \text{暫存器名稱衝突} \neq \text{真實資料相依}.$$
  編譯器理論上可以重命名，但 1960 年代的記憶體太小，編譯器做不到——
  **Tomasulo 的推理：讓硬體自己改名**。
- **CDC 6600 scoreboard 的啟示（1964）**：scoreboard 證明硬體可以排程、可以亂序完成
  （見「1964-CDC6600超級電腦.md」），但它不做 renaming，WAR/WAW 仍會 stall——
  **Tomasulo 要補上這個洞，並走得更遠：連執行都亂序**。
- **IBM 360/91 的任務**：IBM 需要一台浮點性能壓過 CDC 6600 的大型機——
  Tomasulo 的浮點單元正是為此而生（雖然 360/91 只賣了約 20 台，演算法卻不朽）。

## 線索與推理 -- 數學式、程式、理論

### 第一條線索：register renaming 的數學（WAR/WAW hazard 消除）
架構暫存器（程序員看到的）只有少數幾個（如 4 個浮點暫存器），
但硬體裡有**更多的物理暫存器**（reservation station 的儲位）：
$$\text{架構暫存器 } R_i \xrightarrow{\text{renaming}} \text{物理暫存器 } P_j \quad (j \gg i).$$
**重命名的威力**：每次寫入都配一個**新的物理暫存器**，
同名指令互不干擾：
$$A: R1 \leftarrow R2 + R3 \ (\text{寫 } P_1) \quad,\quad C: R1 \leftarrow R6 + R7 \ (\text{寫 } P_2).$$
- WAW（A、C 都寫 R1）：**P₁ ≠ P₂，互不相干** → hazard 消除。
- WAR（後面指令要寫 R1）：讀取方已綁定 **P₁**，寫入方寫 **P₂** → hazard 消除。
$$\text{假相依數量} \propto \frac{1}{\text{物理暫存器數量}} \quad\Longrightarrow\quad \text{renaming 讓假相依趨近於零}.$$
**真相依（RAW）無法消除**——資料真的要等——但 renaming 之後，
流水線只需要等 RAW，其他指令可以**繞過去先執行**。

### 第二條線索：reservation station 的硬體排程
Tomasulo 的三段式流程（注意與 scoreboard 的差別）：
$$\text{Issue（in-order）} \to \text{Execute（out-of-order）} \to \text{Write-back（out-of-order，經 CDB）}.$$
1. **Issue**：指令從解碼器按順序取出 → 進入對應的 **reservation station（RS）**；
   若來源運算元還沒好，**記下「誰會產生它」**（RS 標籤）而不是 stall。
2. **Execute**：RS 持續監看——當**兩個來源都就緒**（標籤被 CDB 廣播結果命中）→ 執行。
   **多個 RS 可同時執行**，誰的運算元先齊誰先跑——**亂序執行**。
3. **Write-back**：結果經 **CDB（Common Data Bus）** 廣播給所有 RS 與暫存器。
   多個結果同時好 → CDB **一次只能廣播一個**（仲裁）。
$$\text{Tomasulo} = \text{RS（排程 + 儲存）} + \text{CDB（廣播 + 仲裁）} + \text{renaming（消除假相依）}.$$

### 第三條線索：IPC 的提升
設 RAW 相依比例為 $r$（無法消除），假相依（WAR/WAW）比例為 $f$（renaming 可消除）：
- **Scoreboard（6600）**：$r$ 與 $f$ 都造成 stall：
  $$S_{sb} = \frac{1}{1 - (r + f) + (r + f)\cdot s}, \quad s = \text{平均 stall 深度}.$$
- **Tomasulo**：只有 $r$ 造成 stall：
  $$S_{tm} = \frac{1}{1 - r + r\cdot s}.$$
- 取 $r = 0.3$、$f = 0.2$、$s = 5$：$S_{sb} \approx 1.67$，$S_{tm} \approx 2.22$——
  **renaming 帶來額外 33% 的加速**，且功能喟元越慢（$s$ 越大），差距越大。

### 第四條線索：1990s 復活與 ROB
Tomasulo 演算法在 1967 年後沉寂二十餘年，因為：
- 晶片面積太小（360/91 的浮點單元佔滿一個機櫃，做不出更多 RS）。
- 360/91 只賣 ~20 台，演算法被埋沒在冷門機型裡。
**1990s 的三個條件同時成熟**：
1. **電晶體暴增**（Moore's Law，見「1958-積體電路.md」）——RS 與 renaming 表變得便宜。
2. **Pentium Pro（1995，P6 微架構）**：Intel 首次把 **Tomasulo + ROB** 放進 x86：
   **ROB（Reorder Buffer）** 記錄指令的原始順序，使**提交（commit）按序**：
   $$\text{issue（in-order）} \to \text{execute（out-of-order）} \to \text{commit（in-order，經 ROB）}.$$
   ROB 讓**推測執行（speculation）**安全——預測錯的指令在 commit 階段被丟棄。
3. **現代 CPU（1995–2024）全部採用**：Intel/AMD/Apple M/ARM 大核的亂序核心，
   都是「**Tomasulo + ROB + 分支預測**」的三本柱——物理暫存器超過 300 個（x86 只有 16 個架構暫存器）。

### Python：Tomasulo 簡化模擬（issue / execute / write-back 與 renaming）

```python
# Tomasulo 簡化模擬：register renaming + reservation station + 亂序執行
# 指令格式：(目的地, 來源1, 來源2, 功能單元, 延遲)

def tomasulo_sim(instrs, n_rs=3):
    """每條寫入配新物理暫存器（renaming）；RS 運算元齊即執行（亂序）"""
    phys = 0          # 物理暫存器計數器
    rename = {}       # 架構暫存器 -> 產生它的標籤
    ready = {}        # 標籤 -> 值就緒的週期
    rs_busy = {}      # RS 儲位 -> 釋放週期
    cycle, issued, log = 0, set(), []

    while len(log) < len(instrs) or any(e[2] is None for e in log):
        cycle += 1
        # Issue（in-order）：有閒置 RS 才發射，否則 stall
        for i, (dst, s1, s2, fu, lat) in enumerate(instrs):
            if i in issued:
                continue
            free = [r for r in range(n_rs) if rs_busy.get(r, -1) < cycle]
            if not free:
                break  # RS 全滿 → stall（in-order issue）
            tag, phys = f"P{phys}", phys + 1
            dep = [rename[s] for s in (s1, s2) if s and s in rename]
            rename[dst] = tag          # renaming：寫入配新標籤
            rs_busy[free[0]] = 10**9
            issued.add(i)
            log.append([i, cycle, None, tag, dep])
            break  # 每週期最多發射一條
        # Execute（out-of-order）：運算元齊了就執行，寫回並釋放 RS
        for entry in log:
            if entry[2] is not None:
                continue
            i, issue_c, _, tag, dep = entry
            if all(ready.get(d, -1) < cycle for d in dep):
                ready[tag] = max(issue_c, cycle) + instrs[i][4]
                entry[2] = ready[tag]
                for r in [r for r, t in rs_busy.items() if t > cycle]:
                    del rs_busy[r]
                break  # 單一 CDB：每週期只廣播一個結果
    return log

instrs = [
    ("R1", "R2", "R3", "add", 4),   # RAW：R1
    ("R4", "R1", "R5", "mul", 7),   #   要等 R1（真相依，必須等）
    ("R1", "R6", "R7", "add", 4),   # WAW/WAR：renaming 後不 stall！
    ("R8", "R9", None,  "shift", 2),# 獨立 → 亂序先行
]
log = tomasulo_sim(instrs)
for i, issue, finish, tag, dep in log:
    d = instrs[i][0]
    print(f"指令{i}({d}): issue@{issue}, finish@{finish}, 寫到 {tag}")
```
輸出：
```
指令0(R1): issue@1, finish@5, 寫到 P0
指令1(R4): issue@2, finish@13, 寫到 P1
指令2(R1): issue@3, finish@7, 寫到 P2
指令3(R8): issue@4, finish@6, 寫到 P3
```
（與 scoreboard 版本（見「1964-CDC6600超級電腦.md」）對比：
**同樣的指令序列，scoreboard 在第 14 週期才完成重寫 R1 的指令，
Tomasulo 靠 renaming（重寫 R1 配新標籤 P₂，而非等舊的 P₁）讓它第 7 週期就完成**——
假相依消失，這就是 register renaming 的威力。）

## 結案 -- 後果與影響
- **亂序執行成為現代 CPU 標準**：
  - **1995 Pentium Pro（P6）**：Intel 把 Tomasulo + ROB 引入 x86——1990s 末的 P6 系列獨霸市場。
  - **2000s–2024**：Intel Core、AMD Zen、Apple M、ARM Cortex-X——
    **所有高性能 CPU 核心都是 Tomasulo 的後裔**，物理暫存器超過 300 個。
- **register renaming 成為必修課**：架構暫存器少（x86-64 只有 16 個通用暫存器），
  但 renaming 讓硬體層面有數百個物理暫存器——**ISA 的不足由微架構補救**。
- **ROB + 推測執行的安全網**：ROB 讓亂序執行的結果**按序提交**——
  分支預測錯誤時只需清空 ROB，架構狀態不受污染——
  這是**推測執行（speculative execution）**能安全存在的基礎。
- **三本柱架構**：現代 CPU 性能 = **superpipeline（深流水線）+ OoO（亂序）+ speculative（推測）**，
  三者都以 Tomasulo 演算法為地基。
- **Spectre 的陰影（2018）**：推測執行被證明有**安全漏洞**（Spectre/Meltdown）——
  Tomasulo 的遺產在 2018 年成為資安戰場，修補（retpoline、微碼更新）犧牲 5–30% 性能。
- **360/91 的弔詭**：機器本身只賣約 20 台，但演算法成為所有 CPU 的核心——
  **「硬體失敗、思想永生」的教科書案例**。

## 關鍵人物與文獻
- **Robert Tomasulo**（IBM Research）：〈An Efficient Algorithm for Exploiting Multiple Arithmetic Units〉(IBM Journal, 1967)。
- **IBM System/360 Model 91**（1967）：Tomasulo 演算法的搖籃，浮點性能當時全球第一。
- **Seymour Cray**：scoreboard 的發明者，Tomasulo 的先行者（見「1964-CDC6600超級電腦.md」）。
- **J. Hennessy & D. Patterson**：《Computer Architecture: A Quantitative Approach》(1990)——Tomasulo 教科書化的推手。
- 相關案件：`1964-CDC6600超級電腦.md`、`1969-快取記憶體.md`、`1981-CISC與RISC之戰.md`、`2007-多核心CPU.md`。
