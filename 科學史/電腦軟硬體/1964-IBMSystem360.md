# 1964 — IBM System/360

## 案件摘要
1964 年 4 月 7 日，IBM 以 50 億美元（當時年營收僅約 30 億）的豪賭，發表 System/360——史上第一個「相容電腦家族」。Gene Amdahl 的統一架構設計讓同一套指令集跨越性能等級，並順手把 8-bit byte 變成世界標準，奠定此後六十年的電腦硬體正典。

## 前因 -- 為什麼會有這個案子
1950–60 年代初的 IBM 有一個致命的結構性問題：**每台電腦都是獨立的孤島**。IBM 同時生產多條互不相容的產品線——科學計算用 7090 系列（二進位、字長 36 bit）、商業資料處理用 1401 系列（變動字長、字元碼）、小型機用 7040……每台機器有自己的指令集、自己的週邊、自己的作業系統、自己的組合語言。

後果是災難性的：

- 客戶升級機器 = 重寫所有軟體，於是客戶寧可留在舊機上
- IBM 自己要為每條產品線維護獨立的軟體團隊，研發成本失控
- 競爭對手（如 Honeywell、CDC）趁機蠶食市場

1961 年，IBM 內部啟動 **SPREAD 計畫**（Systems Programming, Research, Engineering, and Development）研究對策，結論大膽到近乎瘋狂：**廢棄所有現有產品線，造一個統一架構的全新家族**，用同一架構涵蓋從最小到最大的所有機型。這就是「360」名字的由來——360 度，全方位、涵蓋一切。

1962 年，**Gene Amdahl** 被任命為主架構師。他面對的核心難題是：如何讓一台幾萬美元的小機器與一台幾百萬美元的旗艦「看起来是同一台電腦」？

## 線索與推理 -- 數學式、程式、理論
### 1. 相容家族：同一 ISA 跨越性能等級
Amdahl 的解法是現代電腦工業最重要的概念發明——**架構（architecture）與實作（implementation）分離**。他明確區分：

- **架構（ISA）**：程式設計師看見的機器——指令集、暫存器、定址方式、中斷機制
- **實作**：架構的具體硬體——電路、速度、價格

只要所有機型實作**同一個 ISA**，軟體就能在家族內自由遷移。System/360 家族的性能跨越約 $50\times$，價格跨越約 $50\times$（從約 \$13 萬到 \$550 萬）：

$$\frac{\text{Model 75 性能}}{\text{Model 30 性能}} \approx 50, \qquad \frac{\text{Model 75 價格}}{\text{Model 30 價格}} \approx 50$$

用數學語言說，家族中每台機器都是同一抽象機器的不同「效能等化實例」：對任意機型 $m$ 與程式 $P$，其語義不變，只有執行時間伸縮：

$$\text{Semantics}_m(P) = \text{Semantics}(P), \quad \text{Time}_m(P) = c_m \cdot T(P)$$

軟體投資從此「跟著架構走」而非「跟著機器走」。這個思想直接催生了後世所有的相容機產業（PC clones）、x86 的長壽（40 年相容性）、以及今天的「指令集生態」概念（ARM、RISC-V）。

### 2. 8-bit byte 標準化
在 System/360 之前，byte/word 長度百家爭鳴：36 bit（7090）、12/24 bit（PDP 系列）、變動字元長（1401）。System/360 統一採用 **8-bit byte、32-bit word**，並搭配 EBCDIC 與（後來的）ASCII 字元碼。8-bit 的選擇有精密的工程推理：

- 8 bit 可表示 $2^8 = 256$ 個符號，足以容納字母、數字、標點與控制碼
- 8 是 2 的冪，方便二進位運算與定址
- 32-bit word = 4 bytes，可同時容納一個單精度浮點數與一個位址

這個決定讓「byte = 8 bits」成為全人類的預設常識。今天一切的「MB」「GB」「行動網路流量」，都是 1964 年那場會議的遺產。

### 3. 微碼（microcode）：讓小機器模仿大機器
家族中低階機型（如 Model 30）用較慢、較便宜的金屬氧化物電路，若直接實作整個 ISA 成本太高。Amdahl 與團隊（微碼部分由 Maurice Wilkes 1951 年的想法發揚）採用**微碼直譯**：

> 把複雜的 360 指令，用底層更簡單的微指令（microinstruction）一段小程式來「扮演」。

亦即低階機器的控制單元本質上是一台**硬體實作的直譯器**。若機器指令為 $I$、微指令集為 $\mu$，則：

$$\text{Execute}(I) = \text{interpret}_{\mu}(\text{Microprogram}(I))$$

高階機型（Model 75）則用硬體線路直接實作指令以追求速度。同一架構、不同實作層——這是「模擬/虛擬化」思想的硬體先聲。IBM 後來甚至在 System/370 上用微碼**模擬執行舊機器（1401、7090）的程式**，實現了「換機器不換軟體」的承諾。

### 4. Python 模擬 360 指令週期
System/360 的基本指令週期（fetch–decode–execute）可用 Python 概念性模擬：

```python
class System360:
    def __init__(self):
        self.reg = [0] * 16          # 16 個 32-bit 通用暫存器
        self.mem = {}                # 主記憶體（稀疏）
        self.psw = 0                 # 程式狀態字組（含 PC）

    def fetch(self):
        instr = self.mem.get(self.psw, 0)
        self.psw += 4                # 360 指令以 4 為定址單位
        return instr

    def decode(self, instr):
        op = (instr >> 24) & 0xFF    # 8-bit opcode：8-bit byte 的遺產
        r1 = (instr >> 20) & 0x0F
        r2 = instr & 0x0F
        return op, r1, r2

    def execute(self, op, r1, r2):
        if op == 0x1A:               # AR: 加法
            self.reg[r1] = (self.reg[r1] + self.reg[r2]) & 0xFFFFFFFF
        elif op == 0x05:             # BAL: 跳躍並儲存回返位址
            self.reg[r1], old = self.psw, self.reg[r1]
            self.ps = self.reg[r2] if False else old  # 簡化示意
        elif op == 0x00:
            return False             # 停機
        return True

    def run(self, entry):
        self.ps = entry
        while True:
            op, r1, r2 = self.decode(self.fetch())
            if not self.execute(op, r1, r2):
                break
```

這段模擬展示了 360 的三大遺產：8-bit opcode 定界、16 個 32-bit 通用暫存器、PSW 統一管理程式狀態（現代 CPU 的 flag register 與 interrupt 狀態字的祖先）。

## 結案 -- 後果與影響
- **豪賭成功**：System/360 大獲全勝，IBM 主宰主機市場數十年；Fortune 雜誌稱之為「IBM 的 50 億美元賭局」，事實上整個計畫（研發+生產線+行銷）耗資約 50 億美元，超過曼哈頓計畫。
- **IBM 主機至今仍在營運**：System/360 的 ISA 血脈經 370（1970）、390（1990）、zSeries（2000）一路延續到今天的 IBM z16（2022）——**60 年的 ISA 相容性**，史上最長壽的電腦架構。全球金融清算系統大量仍跑在 IBM Z 上。
- **相容機革命**：1970 年代 Amdahl 離開 IBM 創立 Amdahl Corporation 製造「插拔相容」主機，開啟主機相容機產業；此概念最終演化為 PC 相容機與 x86 生態。
- **軟體工業化**：360 的 OS/360 開發經歷催生了 Fred Brooks 的《人月神話》（The Mythical Man-Month, 1975），軟體工程學科由此誕生。
- **8-bit byte** 成為全球標準，影響至今一切數位基建。

## 關鍵人物與文獻
- **Gene Amdahl（1922–2015）**：System/360 主架構師，後創 Amdahl Corp（相容機）、提出 Amdahl's Law（並行加速比上限定理）：$$S = \frac{1}{(1-p) + \frac{p}{n}}$$
- **Fred Brooks（1931–2022）**：OS/360 專案經理，《人月神話》作者，1999 年圖靈獎。
- **Maurice Wilkes**：1949 年提出微程式設計概念，微碼的理論源頭。
- 文獻：*SPREAD Report*（IBM 內部, 1961）；G. Amdahl et al., "Architecture of the IBM System/360", *IBM Journal of R&D*, 1964；Fred Brooks, *The Mythical Man-Month*（1975）。
