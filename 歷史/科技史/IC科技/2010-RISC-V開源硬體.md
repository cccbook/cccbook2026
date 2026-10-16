# 2010 - RISC-V 開源硬體：免費的指令集，無限的晶片

## 案件摘要
2010 年，UC Berkeley 的 Krste Asanović、David Patterson、Yunsup Lee、Andrew Waterman 啟動 RISC-V 專案。
他們把指令集架構（ISA）規格完全開源——任何人都能免費實作、修改、量產，無需授權費。
與 ARM 的封閉授權模式相比，RISC-V 選擇了另一條路：ISA 規格免費、實作可開源可閉源。
這是開源硬體運動的里程碑，也是 2020 年代半導體民主化的起點。

## 前因 -- 為什麼會有這個案子
- **ARM 授權模式的罩門**：1990 年成立的 ARM 靠「授權架構 + 每顆晶片抽權利金」統治行動運算，但罩門有三——授權費與權利金對新創與學術界是沉重負擔、**locked in**（一旦採用 ARM 就被鎖死在 ARM 的路線圖上）、以及**無法客製化**（客戶不能自由增加指令集）。
- **RISC 源頭的回歸**：1980 年 Patterson（Berkeley RISC-I）與 Hennessy（Stanford MIPS）奠定的 RISC 哲學——硬體簡單化、load/store 架構、固定指令編碼——在 ARM 上大獲成功，兩人 2017 年獲圖靈獎。RISC-V 是 RISC 的第五代回歸，這次選擇開源。
- **Berkeley 的教訓**：Berkeley 早年開源 RISC-I/II、SPARC、SOAR，卻因 ISA 規格分裂與商業化不足而邊緣化。Krste Asanović 的關鍵推理——**ISA 規格必須凍結且開源，實作可以自由競爭**，才能避免重蹈覆轍：

$$
\text{RISC-V 價值} = \underbrace{\text{ISA 規格免費}}_{\text{開源}} \times \underbrace{\text{模組化擴充}}_{\text{可客製}} \times \underbrace{\text{實作自由}}_{\text{開源或閉源皆可}}
$$

- **專案的偶然起點**：最初只是為了替 Asanović 實驗室的平行計算專案找一個能自由使用的 ISA——與其申請 ARM 授權，不如自己設計一個乾淨的 32-bit ISA，只花三個月。

## 線索與推理 -- 數學式、程式、理論

### 1. 案件現場：模組化 ISA 的組合數

RISC-V 以 RV32I/RV64I 為基礎指令集，再以單字母擴充指令集堆疊：

$$
\text{RISC-V} = \underbrace{\text{RV32I / RV64I}}_{\text{基礎（整數）}} + \underbrace{M}_{\text{乘除}} + \underbrace{A}_{\text{原子操作}} + \underbrace{F}_{\text{單精度}} + \underbrace{D}_{\text{雙精度}} + \underbrace{C}_{\text{壓縮指令}}
$$

- 擴充指令集可自由組合（例如 RV32IMC、RV64G = RV64IMAFDZicsr_Zifencei），$n$ 個選配擴充有 $2^n$ 種組合——這是模組化的數學本質：

$$
N_{\text{組合}} = 2^{|\text{選配擴充}|} \quad\Longrightarrow\quad 6 \text{ 個選配} \Rightarrow 64 \text{ 種晶片變體}
$$

- **對比 x86/ARM**：x86 與 ARM 的 ISA 是**單體式**的——每次世代更新都把新指令集硬塞進同一份規格，客戶只能整包接受（對比 1990-ARM 案的 Thumb：ARM 也曾用 16-bit 壓縮指令解決程式碼密度，但那是單體內的補丁，RISC-V 的 C 擴充是模組化的選配）。
- **通用性**：RV32I 本身已是 **Turing complete**——40 條基礎指令已足以實作任何可計算函數，其餘擴充只是效能與功能加值：

$$
\forall f \in \text{可計算函數}，\ \exists P_{\text{RV32I}}：f(x) = \text{RV32I-CPU}(P, x)
$$

### 2. RISC 精簡指令的 CPI 模型

RISC-V 沿襲 RISC 哲學，以固定 32-bit 編碼、load/store 架構、簡化解碼器換取低 CPI 與高時脈：

$$
T_{\text{CPU}} = \text{IC} \times \text{CPI} \times T_{clk}, \qquad \text{CPI}_{\text{RISC-V}} \approx 1\text{–}1.2 \ (\text{單發射流水線})
$$

- **解碼器極簡**：指令編碼位置固定（opcode 在 bits [6:0]，rd 在 [11:7]，rs1/rs2 在 [19:15]/[24:20]），解碼器像組合邏輯而非 CISC 的微碼 ROM。
- **壓縮指令 C 擴充**：16-bit 壓縮指令可省 25–30% 程式碼密度，縮小 IC，對嵌入式與 AIoT 場景至關重要。
- **客製化指令的效能增益**：為 AI 加速器加一條向量指令，能取代數十條基礎指令——Amdahl 定律給出換取點：

$$
S_{\text{speedup}} = \frac{1}{(1-s) + \dfrac{s}{E}}
$$

當客製指令覆蓋的熱點程式佔比 $s$ 接近 1、加速比 $E$ 放大，整體加速比就逼近 $E$——這是 RISC-V 客製化晶片（AIoT、NPU）的理論根據。

### 3. 指令編碼的位元佈局

```asm
        addi  x1, x0, 5      ; 0x00500093   imm[11:0]=5, rs1=x0, funct3=000, rd=x1, opcode=0010011(I-type)
        addi  x2, x0, 0      ; 0x00000113   rd=x2 累加器歸零
loop:   add   x2, x2, x1     ; 0x00110133   R-type: rs2=x1, rs1=x2, funct3=000, rd=x2, opcode=0110011
        addi  x1, x1, -1     ; 0xFFF08293   imm=-1
        bne   x1, x0, loop   ; 0xFE002EE3   B-type: rs1=x1, rs2=x0, funct3=001, imm=-8（回跳 2 道指令）
        ; x2 = 5+4+3+2+1 = 15
```

RISC-V 指令的固定欄位（R-type）：

$$
\underbrace{\text{funct7}}_{31:25}\ \underbrace{\text{rs2}}_{24:20}\ \underbrace{\text{rs1}}_{19:15}\ \underbrace{\text{funct3}}_{14:12}\ \underbrace{\text{rd}}_{11:7}\ \underbrace{\text{opcode}}_{6:0}
$$

六種指令格式（R/I/S/B/U/J）共用 opcode 位置，解碼器只需讀 bits [6:0] 就能分流——這是「簡單到能開源」的設計哲學。

### 4. Python 實作：RV32I 簡易模擬器

```python
# RV32I 簡易模擬器：fetch / decode / execute（add/lw/sw/beq + addi/bne）
CODE = [
    ('addi', 1, 0, 5),      # x1 = 5
    ('addi', 2, 0, 0),      # x2 = 0
    ('add',  2, 2, 1),      # x2 += x1
    ('addi', 1, 1, -1),     # x1 -= 1
    ('bne',  1, 0, 2),      # 若 x1 != 0 跳到第 2 道（add）
    ('sw',   2, 0, 0),      # mem[0] = x2
    ('lw',   3, 0, 0),      # x3 = mem[0]
    ('beq',  3, 2, 8),      # 若 x3 == x2 跳到第 8 道（hlt）
    ('hlt',),
]
pc, reg, mem = 0, [0] * 32, {}
while True:
    op = CODE[pc]                                   # fetch
    if op[0] == 'addi':                             # decode + execute
        reg[op[1]] = (reg[op[2]] + op[3]) & 0xFFFFFFFF
        pc += 1
    elif op[0] == 'add':
        reg[op[1]] = (reg[op[2]] + reg[op[3]]) & 0xFFFFFFFF
        pc += 1
    elif op[0] == 'bne':
        pc = op[3] if reg[op[1]] != reg[op[2]] else pc + 1
    elif op[0] == 'beq':
        pc = op[3] if reg[op[1]] == reg[op[2]] else pc + 1
    elif op[0] == 'sw':
        mem[op[3]] = reg[op[1]]
        pc += 1
    elif op[0] == 'lw':
        reg[op[1]] = mem.get(op[3], 0)
        pc += 1
    else:
        break                                       # hlt
print(f"x1={reg[1]} x2={reg[2]} x3={reg[3]} mem[0]={mem.get(0, 0)}")
# 預期輸出：x1=0 x2=15 x3=15 mem[0]=15
# 5+4+3+2+1 = 15——這段程式在 RISC-V 真實硬體上只需 40 條基礎指令的子集
```

### 5. 開源 EDA 與教育晶片：從 ISA 到流片

- **SiFive（2015）**：Yunsup Lee、Andrew Waterman 與 Krste Asanović 創立，把 RISC-V 商業化——提供商用核心 IP 與客製化服務，證明「開源 ISA + 商業實作」可以並存。
- **RISC-V International（2015→）**：RISC-V 基金會 2020 年總部遷至瑞士，改名 RISC-V International——中立化的司法管轄讓中國、歐洲、印度各國放心採用。
- **開源 EDA 工具鏈**：OpenROAD（2020s，全自動 RTL-to-GDS）、OpenLane、SpinalHDL/Chisel——配合 1986 年邏輯合成的理論源頭，開源工具鏈讓學生與新創能免費流片。
- **Google 教育晶片 shuttle**：Google 贊助 efabless 的 MPW shuttle，把 RISC-V 晶片的流片成本壓到數百美元——教育與研究晶片首次可以量產。

## 結案 -- 後果與影響
- **開源硬體運動成形**：ISA 規格開源 + 實作自由競爭，對比 ARM 的封閉授權——ARM 也在 2019 年開放 ARMv8-A 架構給學術界，正是為了對抗這個浪潮。
- **客製化晶片（AIoT）**：各家廠商自由擴充指令集（向量、AI 加速、安全），SiFive、阿里平頭哥（玄鐵 C910）、Siordial 等推出客製化 RISC-V 晶片。
- **教育與研究晶片量產**：Berkeley、MIT、清華等校的 RISC-V 課程可以直接流片，學生設計的晶片能真的跑起來——這是半導體教育史的民主化時刻。
- **開源 EDA 工具鏈**：OpenROAD、OpenLane 與 efabless shuttle 讓「一個人、一台電腦、一顆晶片」從口號變成現實。
- **2020s 半導體民主化**：中國、印度、歐洲各國以 RISC-V 追求架構自主權——指令集從 ARM/x86 的雙寡頭，走向開源的多極世界。

## 關鍵人物與文獻
- **Krste Asanović**：Berkeley 教授，RISC-V 專案發起人，SiFive 共同創辦人。
- **David Patterson**：Berkeley RISC（1980）奠基人，2017 年圖靈獎，RISC-V 的精神導師。
- **Yunsup Lee 與 Andrew Waterman**：Berkeley 博士生，RISC-V 第一版 ISA 與模擬器的實作者，SiFive 共同創辦人。
- **John Hennessy**：Stanford MIPS（1981）奠基人，2017 年圖靈獎，RISC 哲學的另一半源頭。
- Waterman & Asanović (Eds.), *The RISC-V Instruction Set Manual, Volume I: User-Level ISA*。
- D. Patterson & J. Hennessy, *Computer Organization and Design: RISC-V Edition*, 2017。
- A. Waterman, Y. Lee, D. Patterson, K. Asanović, "The RISC-V Instruction Set Architecture", UC Berkeley Tech Report, 2011。
