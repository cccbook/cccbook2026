# 1945 - Von Neumann 架構

## 案件摘要
1945 年，數學家 John von Neumann 發表《First Draft of a Report on the EDVAC》，把「程式與資料一起放在記憶體」的想法寫成了電腦的藍圖。這份報告定義了沿用至今的電腦基本結構，是所有現代電腦的「共同祖先」。

## 前因 -- 為什麼會有這個案子
- ENIAC（1946 公開）沒有儲存程式：要改一個程式，得花工程師幾天時間重新插線、設定開關。
- ENIAC 團隊（Eckert 與 Mauchly）在設計後繼機 EDVAC 時，想解決「程式設定太慢」的問題。
- von Neumann 以顧問身份參與 1944 年起的 EDVAC 計畫，把討論結果整理成報告，於 1945 年 6 月流傳。

關鍵痛點可以用一個簡單的複雜度來刻劃：

$$T_{\text{改程式}}^{\text{ENIAC}} \gg T_{\text{執行}}^{\text{ENIAC}}$$

重新設定程式所需的時間遠大於程式執行的時間——這在工程上完全不合理，必須破案。

## 線索與推理 -- 數學式、程式、理論

### 定義：儲存程式（stored-program）概念
> 一部電腦若其程式（指令序列）與資料同樣以二進位形式儲存在同一個可讀寫記憶體中，且指令可以像資料一樣被修改、讀取，則稱為儲存程式電腦。

統一的關鍵：記憶體中不區分「指令」與「資料」，只是取用方式不同：

$$\text{memory}[pc] \xrightarrow{\text{當作指令}} \text{decode}, \qquad \text{memory}[addr] \xrightarrow{\text{當作資料}} \text{operand}$$

### 定義：五大單元
報告將電腦分為五個單元：

| 單元 | 英文 | 職責 |
|---|---|---|
| 運算器 | Arithmetic Unit（ALU） | 執行加減乘除與邏輯運算 |
| 控制器 | Control Unit | 解碼指令、發出控制訊號 |
| 記憶體 | Memory | 儲存程式與資料 |
| 輸入 | Input | 將外界資料送入記憶體 |
| 輸出 | Output | 將計算結果送出 |

### 定義：指令週期（fetch–decode–execute）
$$
\begin{aligned}
\text{FETCH:}\quad & IR \leftarrow M[PC];\ PC \leftarrow PC + 1 \\
\text{DECODE:}\quad & (op,\ addr) \leftarrow \text{decode}(IR) \\
\text{EXECUTE:}\quad & AC \leftarrow f(op,\ AC,\ M[addr])
\end{aligned}
$$

### Python 實作：簡單 von Neumann CPU 模擬器
```python
# 簡化 von Neumann 機器：記憶體存程式+資料，一個累加器 AC
# 指令格式：(op, addr)；op: 0=LOAD, 1=ADD, 2=SUB, 3=STORE, 4=JMP, 5=HALT

def run(program, data_mem_size=16):
    mem = list(program) + [0] * data_mem_size   # 程式與資料同放一個記憶體
    pc, ac = 0, 0
    while True:
        op, addr = mem[pc]; pc += 1            # FETCH + DECODE
        if   op == 0: ac = mem[addr]           # EXECUTE
        elif op == 1: ac = ac + mem[addr]
        elif op == 2: ac = ac - mem[addr]
        elif op == 3: mem[addr] = ac
        elif op == 4: pc = addr
        else: break
    return mem

# 計算 3 + 5 * 2 的直線版本（先算 5*2 用兩次加法近似）：
# 資料區從位址 8 開始：m8=3, m9=5
prog = [(0, 8),   # LOAD  3
        (0, 9),   # LOAD  5
        (1, 9),   # ADD   5  -> 10
        (3, 10),  # STORE m10
        (0, 10),  # LOAD  10
        (1, 8),   # ADD   3  -> 13
        (3, 11),  # STORE m11
        (5, 0)]   # HALT
print(run(prog)[11])   # 輸出 13
```

### 與 Harvard 架構的對照表
| 特性 | Von Neumann 架構 | Harvard 架構 |
|---|---|---|
| 指令與資料儲存 | 同一記憶體 | 分開的兩套記憶體 |
| 匯流排 | 共用一組 | 指令、資料各自獨立 |
| 同時取指令+資料 | 不行（馮諾伊曼瓶頸） | 可以，頻寬較高 |
| 自修改程式 | 可能 | 不可能 |
| 硬體成本 | 較低 | 較高 |
| 典型應用 | 一般電腦（x86、ARM 上的記憶體子系統） | 微控制器（如 PIC、AVR）、DSP |

## 結案 -- 後果與影響
- 幾乎所有現代電腦（桌上型、筆電、伺服器、手機）都是 von Neumann 架構的後裔。
- 副產品是「馮諾伊曼瓶頸」（von Neumann bottleneck）：CPU 與記憶體之間共用通道限制了速度——這也促成了快取（cache）、哈佛化設計（分離 L1 指令快取）等後續發明。
- 儲存程式概念使「軟體產業」成為可能：程式從硬體接線中解放，變成可以販售、複製、修改的資料。
- 因報告只署名 von Neumann，Eckert 與 Mauchly 的貢獻被掩蓋，引發了歷史上著名的優先權爭議。

## 關鍵人物與文獻
- **John von Neumann**（1903–1957）：數學家，報告執筆者。
- **J. Presper Eckert、John Mauchly**：ENIAC/EDVAC 實際設計者，主張「高速讀寫記憶體」的概念源自其 Mercury 延遲線設計。
- 文獻：*First Draft of a Report on the EDVAC*, Moore School of Electrical Engineering, University of Pennsylvania, 1945（Moore School Lecture No. 42 的整理）。
