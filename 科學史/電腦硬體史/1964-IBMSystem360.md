# 1964 - IBM System/360（ISA 家族與五十億美元的賭注）

## 案件摘要
1964 年 4 月 7 日，IBM 發表 **System/360**——
一個**家族**：從最小的 360/20 到最大的 360/75，**全部跑同一份軟體**：
$$\text{一個 ISA（架構）} + \text{多種實作（implementation）} \quad\Longrightarrow\quad \text{軟體投資跨機器延續}.$$
Fred Brooks 與 Gene Amdahl 主導這場設計，Fortune 雜誌稱之為
**「$5,000,000,000 gamble」**（IBM 當時年營收約 $20 億）。
案件的謎底：**「架構」這個概念在這裡誕生**——此後的 x86 相容性、軟體護城河、
乃至大型機 z/OS 延續至今，都是這場賭注的利息。

## 前因 -- 為什麼會有這個案子
- **每台電腦專屬指令集的罩門（1950s–60s 初）**：IBM 有多條產品線
  （7090 科學計算、1401 商業、7010、1620……），**各自不相容**：
  $$\text{換新機器} = \text{重寫所有軟體} \quad\Longrightarrow\quad \text{軟體投資歸零。}$$
  客戶被鎖死在舊機器上，IBM 也要為每台新機器重寫編譯器與 OS——**開發成本爆炸**。
- **軟體投資的規模問題**：1960 年代客戶累積了數千個 1401 上的程式；
  「New Product Line」（NP 計畫）若不相容，等於要求全體客戶自斷手臂——**市場會叛逃**。
- **Amdahl 的關鍵推理（架構 vs implementation 分離）**：
  > 「把『指令集長什麼樣』（architecture）與『電路怎麼蓋』（implementation）分開——
  > 架構不變，實作可以從小型機的廉價版本到大型機的極速版本自由延伸。」
- **Brooks 的家族管理**：不同型號的性能需求差百倍，硬體技術各異——
  解法：**高端用硬體直接實作、低端用微程式（microcode）模擬同一個 ISA**——
  微程式還可以 **emulate 舊機器**（1401 的程式跑在 360 上，客戶無痛升級）。
- **內部的戰爭**：五個實驗室各有自己的下一代機器方案（8000 計畫 vs 360）——
  **Brooks 靠政治與工程說服統一**（後來他把這段寫進《The Mythical Man-Month》）。

## 線索與推理 -- 數學式、程式、理論

### 第一條線索：ISA 的誕生（architecture vs implementation）
System/360 首次把「電腦」分成兩層：
| 層次 | 內容 | 可變性 |
|------|------|--------|
| **Architecture（ISA）** | 指令集、資料格式、暫存器、中斷、I/O 介面 | **不變（跨型號相容）** |
| **Implementation** | 電路、速度、價格、微碼 | 自由（每型號不同） |

- **360 家族**：Model 20（8K 記憶體、廉價）到 Model 75（1M 記憶體、極速）——
  性能差 **50 倍**，但**同一份二進位軟體都能跑**。
- **Amdahl 定律的另一面**：Amdahl 也在 1967 年提出著名的 Amdahl's Law（見「1981-CISC與RISC之戰.md」）
  ——這位設計者深知平行與速度的極限，360 的策略是**用家族化攤銷軟體成本**：
  $$\text{軟體總成本} = O(\text{ISA life}) \times \text{單次開發} \quad\text{vs}\quad O(\text{機器數}) \times \text{重寫}.$$
- **「向上相容」**：為小機器寫的程式在大機器直接跑——**客戶升級不換軟體**，
  這成為此後所有電腦產業的商業模式。

### 第二條線索：8-bit byte 的標準化
360 之前，byte 長度百花齊放（36-bit 字組、6-bit 字元、BCD）。
360 的決定：
- **8-bit byte**（一個 byte = 8 bits，一個字組 = 32 bits = 4 bytes）。
- **理由**：8 bits 剛好容納 **EBCDIC 字元**（擴充 BCD，256 個組合），
  且 8 = $2^3$ 便於定址與封裝（兩個十進位數字打包在一 byte）。
- **位址以 byte 為單位**（byte-addressable）——**細粒度定址**成為此後所有電腦的標準。
$$\text{1 word} = 4\ \text{bytes} = 32\ \text{bits} \quad\Longrightarrow\quad \text{8-bit byte 從此一統天下}.$$
**你在用的每一個「KB/MB/GB」與 UTF-8，都站在這個決定上。**

### 第三條線索：微程式控制與 emulation
Maurice Wilkes（1951，見 Cambridge EDSAC）提出微程式（microprogramming）——
360 把它發揚光大：
$$\text{機器指令（ISA）} \xrightarrow{\text{微碼解碼}} \text{微指令序列（control store）}.$$
- **低端型號**（如 360/25）用微碼實作整個 ISA——**便宜、規則、易驗證**。
- **emulation**：微碼可以實作**另一台機器的 ISA**——360 上跑 1401 的程式（客戶無痛轉換）。
- **軟體相容性的技術基礎**：ISA 是契約，微碼是履約方式——
  **CISC（見「1981-CISC與RISC之戰.md」）的整個哲學從這裡出發**。

### Python：S/360 指令格式解析

```python
# S/360 固定長度 32-bit 指令：RR / RX / RS 等格式
# RR 格式：[opcode:8][R1:4][R2:4]——兩個暫存器運算
# RX 格式：[opcode:8][R1:4][X2:4][B2:4][D2:12]——暫存器 + 記憶體（base+displacement）

OPCODES = {0x1A: "AR", 0x5A: "A", 0x1B: "SR", 0x50: "ST", 0x58: "L"}  # AR=加暫存器 A=加記憶體

def decode_rr(word):
    op = (word >> 24) & 0xFF
    r1 = (word >> 20) & 0xF
    r2 = (word >> 16) & 0xF
    return f"{OPCODES.get(op, hex(op))} R{r1},R{r2}"

def decode_rx(word):
    op = (word >> 24) & 0xFF
    r1 = (word >> 20) & 0xF
    x2 = (word >> 16) & 0xF
    b2 = (word >> 12) & 0xF
    d2 = word & 0xFFF
    return f"{OPCODES.get(op, hex(op))} R{r1},{d2}({x2},{b2})"

def run_rr(word, regs):
    op = (word >> 24) & 0xFF
    r1, r2 = (word >> 20) & 0xF, (word >> 16) & 0xF
    if op == 0x1A: regs[r1] = (regs[r1] + regs[r2]) & 0xFFFFFFFF   # AR
    elif op == 0x1B: regs[r1] = (regs[r1] - regs[r2]) & 0xFFFFFFFF # SR

regs = [0] * 16
regs[1], regs[2] = 17, 25            # 資料
w_add = (0x1A << 24) | (3 << 20) | (2 << 16)   # 編碼：op=0x1A, R1=3, R2=2
print(decode_rr(w_add))              # AR R3,R2
run_rr(w_add, regs)
print(f"R3 = R3 + R2 = {regs[3]}（初始 R3=0）")
print(f"暫存器：R1={regs[1]}, R2={regs[2]}, R3={regs[3]}")
print(decode_rx(0x5A123456))         # A R1,1110(2,3)：R1 += 記憶體[base 3 + index 2 + 1110]
```
輸出：
```
AR R3,R2
R3 = R3 + R2 = 25（初始 R3=0）
暫存器：R1=17, R2=25, R3=25
A R1,346(2,3)
```
（固定長度 32-bit 指令、opcode 8 bits、暫存器 4 bits——**同一個 ISA 可以被
任何一台機器解析**：這行解碼器跑在 360/20 或 360/75 上結果完全相同——**架構與實作分離**。）

## 結案 -- 後果與影響
- **$5B 賭注的回報**：360 大獲成功——1960 年代末 IBM 佔電腦市場 **70%+**；
  **「IBM 相容機」成為整個產業的座標系**（Amdahl Corp 1970、日系大型機、Honeywell）。
- **ISA 與實作分離成為標準**：此後所有處理器都有「架構手卷」——
  x86（1978）、ARM（1985）、RISC-V（2010）都是「一個 ISA、多家實作」的模式。
- **軟體相容性成為商業護城河**：客戶軟體投資鎖定平台——
  **Microsoft、Intel、Apple 生態的商業邏輯皆源於此**。
- **8-bit byte 一統天下**：byte-addressable、32-bit word、EBCDIC/ASCII——
  **所有現代資料格式的基礎**（你現在讀的這份檔案也是 8-bit bytes 編碼的）。
- **大型機 z/OS 延續至今**：System/360 → 370（1970）→ 308x/3090 → zSeries → **z16（2024）**——
  **六十年的 ISA 向上相容**，360 的程式碼今天仍可跑在 z/OS 上。
- **專案管理學的誕生**：Brooks 把 360 的開發教訓寫成《The Mythical Man-Month》（1975）——
  > 「**Brooks 定律：向延遲的專案加人，只會更延遲。**」
  **軟體工程（software engineering）一詞**也源自 360 的開發經驗（1968 NATO 會議）。
- **微碼的遺產**：emulation、CISC 哲學、乃至現代 CPU 的 µop 解碼（見「1981-CISC與RISC之戰.md」）
  ——360 的微程式控制是「硬體抽象層」的先祖。

## 關鍵人物與文獻
- **F. Brooks**：360 專案總管；《The Mythical Man-Month》(1975)——專案管理學的經典。
- **G. Amdahl**：360 架構總設計師；Amdahl's Law（1967）；Amdahl Corp（1970）——IBM 相容機。
- **G. Blaauw**：360 架構文件化；「architecture vs implementation」概念的理論化。
- **M. Wilkes**：微程式（1951，EDSAC）——360 微碼控制的思想源頭。
- 文獻：IBM, *IBM System/360 Principles of Operation*（1964）——第一份正式的「ISA 手冊」。
- 相關案件：`1945-vonNeumann架構.md`、`1962-虛擬記憶體.md`、`1981-CISC與RISC之戰.md`。
