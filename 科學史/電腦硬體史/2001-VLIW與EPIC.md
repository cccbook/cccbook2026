# 2001 - VLIW 與 EPIC：Itanic 的沉船與 VLIW 的倖存

## 案件摘要
2001 年，Intel 與 HP 合資的 Itanium（IA-64）上市——VLIW/EPIC 的極端實驗：
把排程從硬體完全移到編譯器，128-bit bundle 裝 3 條指令、以 predication 消除分支。
理論很優雅，現實很殘酷：編譯器難寫、x86 相容性不足，Itanium 被 AMD 的 x86-64（2003）擊沉。
但 VLIW 沒有死——它在 DSP、印表機與 AI 加速器找到了自己的戰場。

## 前因 -- 為什麼會有這個案子
- **超標量的罩門**：硬體排程（scoreboard/Tomasulo/分支預測）越來越複雜、功耗越來越大——晶片面積與電力都花在「找並行」上。
- **VLIW 的先驅**：Josh Fisher 的 Multiflow Trace（1980s）證明：編譯器看得到整個程式，比硬體更會排程。
- **關鍵推理**：把「找並行」的責任完全交給編譯器，硬體只負責執行：

$$
\underbrace{\text{超標量}}_{\text{硬體排程}} \quad\Longleftrightarrow\quad \underbrace{\text{VLIW}}_{\text{編譯器排程}}: \text{bundle} = 3 \text{ 指令} \times 128\text{-bit}
$$

- **Intel 的賭注**：以 IA-64 取代 x86，同時甩掉相容包袱——卻低估了相容性的力量。

## 線索與推理 -- 數學式、程式、理論

### 1. 案件現場：VLIW bundle 與 EPIC 三件套

- **VLIW（Very Long Instruction Word）**：固定長度的超長指令，打包多條可並行的操作：

$$
\text{bundle}(128\text{-bit}) = \underbrace{op_1}_{41\text{b}} + \underbrace{op_2}_{41\text{b}} + \underbrace{op_3}_{41\text{b}} + \underbrace{template}_{5\text{b}}
$$

- **template**：宣告 bundle 中各指令槽的功能單元類型與 bundle 邊界——硬體不必解碼相依性。
- **EPIC 三件套**：predication（條件執行）、speculation（推測載入）、bundle template——把超標量的硬體智慧「顯式化」給編譯器。

### 2. Predication：消除分支的數學

把 `if` 改成條件執行——兩條路徑都執行、由謂詞暫存器選擇結果：

$$
\text{if}\ (p)\ x = a;\ \text{else}\ x = b \quad\Longrightarrow\quad
(p)\ x \leftarrow a;\quad (\bar{p})\ x \leftarrow b
$$

- 分支消失了，控制相依變資料相依——流水線不再沖刷（flush）。
- 代價：兩條路徑都花時間，分支體越大越浪費——predication 只適合小分支（if-conversion 有成本模型）。

### 3. 編譯器排程 vs 硬體排程：ILP 的兩條路

| | 超標量（硬體排程） | VLIW（編譯器排程） |
|---|------|------|
| 排程者 | 硬體（scoreboard/RS） | 編譯器（靜態打包） |
| 相依檢測 | 硬體每 cycle 檢查 | 編譯期一次算好 |
| 動態事件 | 可應對（cache miss、預測錯） | 束手無策（stall 整個 bundle） |
| 硬體成本 | 高（排程邏輯） | 低（簡單執行單元） |
| 編譯器 | 簡單 | **極難**（trace scheduling） |

- **關鍵弱點**：程式行為不可預測（cache miss、資料相依迴圈）時，VLIW 的 bundle 只能整排等待——ILP 是靜態的謊言。
- trace scheduling（Fisher）：跨基本塊追蹤最熱路徑打包——編譯器複雜度隨 ILP 指數上升。

### 4. Itanic 的沉船：相容性 > 理論

- **x86 相容性不足**：Itanium 跑 x86 軟體要模擬，慢到不能用——企業不想重寫軟體。
- **編譯器難產**：EPIC 的性能上限取決於編譯器，但沒有人能寫出夠好的排程器。
- **AMD 的反擊（2003）**：x86-64（AMD64）——64-bit 擴充 + 保留 x86 相容性，業界一面倒。
- 2019 年 Itanium 宣告終結，綽號「**Itanic**」——教科書級的沉船。

### 5. Python 實作：VLIW bundle 排程

```python
prog = [                                   # (op, 依賴, 單元)
    ('load',  [],     'mem'),
    ('add',   [0],    'alu'),
    ('mul',   [1],    'mul'),
    ('load',  [],     'mem'),
    ('add',   [3],    'alu'),
    ('mul',   [2, 4], 'mul'),
]
latency = {'mem': 3, 'alu': 1, 'mul': 4}
ready_at, bundles = [0], []                # 各單元下次可用時間
done = {}
for op, deps, unit in prog:
    start = max([ready_at[0]] + [done.get(d, 0) for d in deps])
    finish = start + latency[unit]
    done[op] = finish                      # 簡化：以 op 編號當結果名
    ready_at[0] = finish
    bundles.append((op, start, finish))
width = 3                                  # 每 bundle 3 槽
cycles = max(f for _, _, f in bundles)
print(f"逐條排程總 cycles = {cycles}")
print(f"若打包成 {width}-wide VLIW：約 {cycles // width + (cycles % width > 0)} 個 bundle")
for op, s, f in bundles:
    print(f"  {op:4s}: cycle {s}–{f}")
# 逐條排程總 cycles = 15
# 若打包成 3-wide VLIW：約 5 個 bundle   ← 編譯器看到相依圖，可並行打包
# （但 cache miss 會讓 mem 指令 stall 整個 bundle——VLIW 的靜態軟肋）
```

## 結案 -- 後果與影響
- **Itanium 的教訓**：理論再優雅，**相容性與生態**比架構更強——與 CISC/RISC 之戰同一結論。
- **AMD x86-64 反擊成功**：2003 年 AMD64 成為 64-bit x86 標準，Intel 被迫跟進。
- **VLIW 倖存戰場**：DSP（TI C6x）、印表機、媒體處理（Hexagon DSP）、AI 加速器（VLIW 風格的 NPU 指令集）——行為可預測的領域 VLIW 依然強勢。
- **理論延續**：predication 進入 ARM 與 RISC-V（條件指令）、trace scheduling 的編譯技術延續到 LLVM。

## 關鍵人物與文獻
- **Josh Fisher**：VLIW 概念與 trace scheduling, 1983；Multiflow Computer 創辦人。
- **Joseph Huckaba / Intel–HP 團隊**：Itanium（IA-64）設計。
- **Jim Keller**（AMD）：x86-64 架構的工程領導者。
- J. Fisher, P. Faraboschi, C. Young, *Embedded Computing: A VLIW Approach to Architecture, Compilers and Tools*, 2005。
- 相關案件：`1981-CISC與RISC之戰.md`、`1967-Tomasulo演算法.md`、`1978-Intel8086.md`。
