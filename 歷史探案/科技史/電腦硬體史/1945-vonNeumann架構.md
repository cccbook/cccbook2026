# 1945 - von Neumann 架構（儲存程式計算機的誕生）

## 案件摘要
1945 年 6 月，John von Neumann 寫下《First Draft of a Report on the EDVAC》：
把整台電腦濃縮成五個單元——
$$\text{運算器（ALU）} + \text{控制器（CU）} + \text{記憶體} + \text{輸入} + \text{輸出} \quad\Longrightarrow\quad \text{所有現代電腦的原型}.$$
案件的兇器只有一個觀念：**指令與資料都放記憶體——指令就是資料**（stored-program）。
這是 1936 年 Turing 通用機（見「1936-Turing機.md」）的工程實現，
也是 1946 年 ENIAC（見「1946-ENIAC電子計算機.md」）的「解案報告」。

## 前因 -- 為什麼會有這個案子
- **ENIAC 的罩門（1945）**：ENIAC 用**插線板（plugboard）與開關**「程式化」——
  要改一個程式，得**重新接線數天**（設置一個彈道問題要 1–2 天）：
  $$\text{程式設定時間} \sim \text{數天} \quad\gg\quad \text{計算時間} \sim \text{數秒}.$$
  **電腦算得再快，程式却慢如龜——瓶頸不在計算，在「載入程式」。**
- **關鍵推理：指令就是資料**：
  ENIAC 的程式在機器「外面」（接線），von Neumann 問：
  > 「為什麼不把程式像資料一樣，放進記憶體？」
  這正是 Turing 通用機 $U(\langle M, w \rangle) = M(w)$ 的工程翻譯：
  **機器的描述（程式）本身就是一串可儲存的符號（資料）**（Gödel 編碼的遺產）。
- **設計衝突的暗線**：ENIAC 的工程師 Mauchly 與 Eckert 早已有多個累加器與儲存想法；
  「First Draft」卻只署名 von Neumann——**團隊決裂的種子**（Eckert–Mauchly 後來自立門戶）。
- **Harvard Mark I 的對照（1944）**：指令與資料**分開儲存**（Harvard 架構）——
  程式在紙帶上，仍是「外接程式」。von Neumann 團隊選了第三條路：**共用記憶體**。

## 線索與推理 -- 數學式、程式、理論

### 第一條線索：五大單元與 fetch-decode-execute 週期
EDVAC 報告把電腦分為五個單元：
| 單元 | 功能 | 現代名稱 |
|------|------|----------|
| 中央算術器（CA） | 加減乘除、邏輯運算 | **ALU** |
| 中央控制器（CC） | 讀指令、發號施令 | **CU（控制單元）** |
| 記憶體（M） | 存**指令與資料** | **RAM** |
| 輸入（I） | 資料進入 | 鍵盤/磁碟 |
| 輸出（O） | 結果送出 | 螢幕/磁碟 |

執行週期（CPU 的心跳）：
$$\text{fetch（取指）} \to \text{decode（解碼）} \to \text{execute（執行）} \to \text{fetch} \to \cdots$$
控制器從記憶體取出指令（**取指**）、解出要做什麼（**解碼**）、執行（**執行**）、再取下一條——
**這個無限循環至今仍在你的手機裡每秒運行數十億次。**

### 第二條線索：指令就是資料（Gödel 編碼與 universal machine）
Gödel（1931）證明：任何公式都可編碼成自然數（**Gödel 編號**）；
Turing（1936）證明：任何機器都可編碼成帶上的字串。
von Neumann 的關鍵一步：**既然指令可編碼為數字，數字就能存進記憶體**——
$$\text{指令} \xrightarrow{\text{Gödel 編碼}} \text{數字} \xrightarrow{\text{記憶體}} \text{資料}.$$
後果（三個革命性的推論）：
- **程式可以被載入**：換程式 = 換記憶體內容（數秒，不是數天）。
- **程式可以寫程式**：一個存放在記憶體的程式，可以產生或修改另一段記憶體中的指令——
  **編譯器、組譯器、載入器**全都建基於此。
- **自我修改程式**：機器可以修改自己的指令（早期用法，今多視為危險，但證明了可能性）。
$$\text{stored-program} \quad\Longrightarrow\quad \text{軟體（software）這個概念誕生}.$$

### 第三條線索：von Neumann bottleneck（共用匯流排的代價）
指令與資料**共用同一條記憶體通道**——CPU 每個週期只能取一樣東西：
$$\text{每週期傳輸量} \le O(\text{bus width}) \quad\Longrightarrow\quad \text{CPU 常在等記憶體}.$$
- CPU 速度增長遠快於記憶體（**memory wall**，1980s 起）——瓶頸越來越窄。
- **解法：快取（cache）**——把常用的指令與資料放在 CPU 旁邊的小而快的記憶體（1950s Atlas 已有雛形，1960s IBM 360/85 發揚）。
- **另一路：Harvard 架構**（指令與資料分開匯流排）在**快取層面復活**——
  現代 CPU 的 **L1 快取分為 I-cache 與 D-cache**（modified Harvard）。
**von Neumann 的「缺陷」成為此後六十年微架構創新的主要動力。**

### Python：迷你 von Neumann 機模擬器

```python
# 迷你 von Neumann 機：記憶體同時放指令與資料
# 指令格式：("ADD", dst, src1, src2) / ("LOAD", dst, addr) / ("STORE", addr, src) / ("HALT",)
# 指令就放在記憶體裡——fetch-decode-execute

mem = [
    ("LOAD", 0, 10),   # 位址 0：R0 ← 記憶體[10]
    ("LOAD", 1, 11),   # 位址 1：R1 ← 記憶體[11]
    ("ADD",  2, 0, 1), # 位址 2：R2 ← R0 + R1
    ("STORE", 12, 2),  # 位址 3：記憶體[12] ← R2
    ("HALT",),         # 位址 4
    None, None, None, None, None,
    7,                 # 位址 10：資料
    35,                # 位址 11：資料
    None,              # 位址 12：結果放這
]
REG = [0, 0, 0, 0]
pc = 0  # program counter

for step in range(20):
    if pc >= len(mem) or mem[pc] is None: print("BUS ERROR"); break
    instr = mem[pc]                      # fetch：指令與資料來自同一個記憶體
    op = instr[0]                        # decode
    print(f"step {step} pc={pc} fetch={instr}")
    if op == "HALT": print("HALT"); break
    elif op == "LOAD":   REG[instr[1]] = mem[instr[2]]
    elif op == "STORE":  mem[instr[1]] = REG[instr[2]]
    elif op == "ADD":    REG[instr[1]] = REG[instr[2]] + REG[instr[3]]
    pc += 1                              # execute 完成，取下一條

print(f"寄存器 R0..R2 = {REG[:3]}")
print(f"記憶體[12]（7+35 的結果）= {mem[12]}")
```
輸出（摘要）：
```
step 0 pc=0 fetch=('LOAD', 0, 10)
step 1 pc=1 fetch=('LOAD', 1, 11)
step 2 pc=2 fetch=('ADD', 2, 0, 1)
step 3 pc=3 fetch=('STORE', 12, 2)
step 4 pc=4 fetch=('HALT',)
HALT
寄存器 R0..R2 = [7, 35, 42]
記憶體[12]（7+35 的結果）= 42
```
（注意：**指令與資料在同一個 `mem` 列表中**——fetch 與 LOAD 存取的是同一個記憶體。
這就是 stored-program：若把位址 0 的 LOAD 改成 ADD，機器會照做——**程式就是資料**。）

## 結案 -- 後果與影響
- **EDVAC（1951）與 IAS machine（1951）**：報告構想的實現；IAS machine（普林斯頓）成為
  全球複製的原型——英國 ACE、蘇聯、IBM 701 均源自此設計。
- **軟體成為可能**：程式儲存在記憶體 → 編譯器（1952 AUTOCODE、1957 FORTRAN）、
  作業系統、程式庫——**「軟體產業」從這份報告開始**。
- **程式可以寫程式**：組譯器、編譯器、直譯器、乃至今天的 AI 生成程式碼——
  都是「stored-program 原則」的延伸。
- **馮紐曼瓶頸**：指令與資料共用通道 → 快取階層（L1/L2/L3）、預取、管線——
  **現代 CPU 微架構的半部歷史都在對抗這個瓶頸**。
- **Harvard 架構的復活**：MCU（微控制器）與數位訊號處理器（DSP）用真 Harvard；
  現代 CPU 用 modified Harvard（L1 分 I-cache/D-cache）。
- **歷史定位**：1936 Turing 給「計算」下定義，1945 von Neumann 給「電腦」下定義——
  **此後所有電腦（手機、PC、超級電腦、伺服器）都是 von Neumann 架構的後代**。
- **署名風波的遺憾**：Eckert 與 Mauchly 對「First Draft」只署 von Neumann 一人不滿——
  專利之爭與「誰發明電腦」的訴訟（1973 Honeywell v. Sperry 判 ENIAC 專利無效）延燒三十年。

## 關鍵人物與文獻
- **J. von Neumann**：〈First Draft of a Report on the EDVAC〉（1945，Moore School）——儲存程式架構。
- **J. Mauchly、J. Presper Eckert**：ENIAC（1945）設計者；EDVAC 概念的共同貢獻者。
- **A. Turing**：通用機（1936）——「指令就是資料」的數學源頭（見「1936-Turing機.md」）。
- **K. Gödel**：Gödel 編號（1931）——公式即數字。
- **A. Burks、H. Goldstine、J. von Neumann**：〈Preliminary Discussion of the Logical Design of an Electronic Computing Instrument〉（1946）。
- 相關案件：`1936-Turing機.md`、`1946-ENIAC電子計算機.md`、`1962-虛擬記憶體.md`、`1964-IBMSystem360.md`。
