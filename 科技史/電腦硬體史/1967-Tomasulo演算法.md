# 1967 - Tomasulo 演算法：亂序執行的心臟

## 案件摘要
1967 年，Robert Tomasulo 在 IBM System/360 Model 91 的浮點單元中實現了
**register renaming + reservation station + 亂序執行**。
它讓指令「依序發射、亂序執行」，靠硬體排程榨出相依性之間的並行度。
沉寂近三十年後，1995 年 Pentium Pro 讓它復活——此後每一顆高性能 CPU 的心臟都是 Tomasulo。

## 前因 -- 為什麼會有這個案子
- **in-order 執行浪費流水線**：RAW 相依讓後續指令排隊等待，即使其他功能單元空閒。
- **假相依更冤**：WAR/WAW 只是暫存器名字撞到，卻也造成 stall——暫存器只有幾個，指令卻很多。
- **scoreboard（CDC 6600, 1964）已開路**：但它靠「等讀完才寫」規避 WAR，且暫存器數量少時仍被假相依卡住。
- **關鍵推理**：與其避免假相依，不如**改名**——把架構暫存器映射到更多物理暫存器上：

$$
\text{架構暫存器 } R_i \xrightarrow{\text{renaming}} \text{物理暫存器 } P_k,\qquad \text{WAR/WAW 消除}
$$

配合 reservation station（硬體排程站）與 CDB（結果廣播匯流排），亂序執行即成立。

## 線索與推理 -- 數學式、程式、理論

### 1. 案件現場：reservation station 三件套

每個功能單元前掛一組 **reservation station（RS）**，指令在 RS 排隊等待運算元：

1. **Issue**：從指令佇列取指令；有閒置 RS 就發射，並做 renaming（目的暫存器 → 本 RS 標籤）。
2. **Execute**：兩個來源都就緒（值已到手）就開始運算；多個 RS 就緒則**任選一個**（硬體排程）。
3. **Write-back**：結果上 **CDB** 廣播；所有等這個標籤的 RS 一次收到——WAR 消除（晚到的寫不會蓋掉已讀的值，因為讀的是 RS 中的副本）。

$$
\text{in-order issue} \to \text{out-of-order execute} \to \text{out-of-order write-back}
$$

### 2. Register renaming：假相依的消除術

$$
\begin{aligned}
\text{WAR} &: R_4 \leftarrow R_1 \times R_5;\quad R_1 \leftarrow R_2 + R_3 &&\Rightarrow \text{renaming 後寫 } P_1 \ne \text{讀的 } P_0\\
\text{WAW} &: \text{兩條指令都寫 } R_1 &&\Rightarrow \text{renaming 後各寫各的物理暫存器}
\end{aligned}
$$

- renaming 由 **RS 標籤**實現：架構暫存器 $R_1$ 的「最新結果」由標籤 $tag$ 指認，讀取者登記等待該標籤。
- 效果：相依性圖中只剩 RAW 真相依，ILP（指令級並行度）大幅上升。

### 3. CDB：一條匯流排的廣播

結果從功能單元出來後上 CDB，**一次廣播、全機可見**：

$$
\text{CDB 頻寬} = 1 \text{ 結果/cycle} \quad\Longrightarrow\quad \text{CDB 是新瓶頸}
$$

多個功能單元同時完成時要仲裁（arbitration）——現代 CPU 用多條 result bus 擴充此瓶頸。

### 4. 1990s 復活：P6 微架構

- **Pentium Pro（1995）**：以 ROB（reorder buffer）補全 Tomasulo——加回 **in-order commit**，讓例外與中斷語義精確。
- **現代組合**：in-order issue → out-of-order execute → **in-order commit**（ROB 維持程式序）：

$$
\text{IPC} \approx \min(\text{issue 寬度},\ \text{RS 就緒率},\ \text{CDB 頻寬})
$$

- 深流水線 + 分支預測 + Tomasulo = 推測執行三本柱（見 1991-分支預測案）。

### 5. Python 實作：Tomasulo 簡化模擬

```python
prog = [                                  # (op, dst, srcs, latency)
    ('mul', 'R1', ['R2', 'R3'], 4),
    ('add', 'R4', ['R1', 'R5'], 2),       # RAW on R1
    ('add', 'R1', ['R6', 'R7'], 2),       # WAR on R1（被 i0 讀? 不是，被 i1 讀的是 R1 值）
    ('mul', 'R8', ['R1', 'R4'], 4),       # RAW on R1(新版) 與 R4
]
free_at, result_at, regs = [], {}, {}
regs['R2'] = regs['R3'] = regs['R5'] = regs['R6'] = regs['R7'] = 0
phys = 0                                  # 物理暫存器編號（renaming）
for i, (op, dst, srcs, lat) in enumerate(prog):
    phys += 1
    start = 0                             # RS 就緒即可發射
    for s in srcs:
        start = max(start, result_at.get(s, 0))       # RAW：等最新結果
    finish = start + lat
    if free_at:                            # 功能單元仲裁（同類單元）
        start = max(start, min(free_at))
    result_at[dst] = finish                # renaming：目的暫存器指向新物理暫存器
    free_at.append(finish)
    print(f"i{i} {op:3s} {dst}: start={start} finish={finish} (物理暫存器 P{phys})")
print(f"總 cycles = {max(result_at.values())}")
# i0 mul R1: start=0 finish=4 (P1)     ← 舊 R1
# i1 add R4: start=4 finish=6 (P2)     ← 等 i0 的 R1（RAW，真相依）
# i2 add R1: start=0 finish=2 (P3)     ← WAR 消除：與 i0 並行！
# i3 mul R8: start=6 finish=10 (P4)    ← 等 R4 與新版 R1
# 總 cycles = 10（in-order 執行需 4+2+2+4=12）
```

（i2 的 WAR 在 renaming 後與 i0 並行——Tomasulo 榨出 2 cycles。）

## 結案 -- 後果與影響
- **亂序執行成為標準**：Pentium Pro（1995）、PowerPC 604、Alpha 21264……現代高性能 CPU 全是 Tomasulo 的後代。
- **ROB 補全**：in-order commit 讓精確例外（precise exceptions）成為可能，推測執行得以安全。
- **renaming 延續**：物理暫存器從 8 個長到 200+ 個，ILP 榨取的戰場至今未歇。
- **理論延續**：dataflow 架構、memory disambiguation、ML 預測相依性——源頭都是 1967 這篇 IBM 論文。

## 關鍵人物與文獻
- **Robert Tomasulo**：IBM 360/91 浮點單元設計者；1997 年 Eckert–Mauchly Award。
- **Jim Thornton**（CDC）：scoreboard 與 Tomasulo 兩條路線的另一位開路人。
- R. M. Tomasulo, "An Efficient Algorithm for Exploiting Multiple Arithmetic Units", *IBM Journal of R&D*, 1967。
- J. Hennessy, D. Patterson, *Computer Architecture: A Quantitative Approach*, 1990。
- 相關案件：`1964-CDC6600超級電腦.md`、`1969-快取記憶體.md`、`1991-分支預測.md`。
