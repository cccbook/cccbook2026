# 1981-IBMPC

## 案件摘要
1981 年 8 月 12 日，藍色巨人 IBM 推出 IBM PC（Model 5150）。真正的主角不是機器本身，而是一連串「開放」決策：第三方零組件、開放匯流排、可被複製的 BIOS、以及 Gates 那紙非買斷的 DOS 授權合約。這些決策催生了 PC 相容機產業與 Wintel 聯盟，改寫了此後 40 年的電腦史。

## 前因 -- 為什麼會有這個案子
- Apple II 證明個人電腦市場存在且暴利，IBM 的主流商用市場正被侵蝕。
- IBM 內部成立跳脫體制的「Entry Level Systems」小組（Florida Boca Raton），限期一年出貨，繞過 IBM 慢吞吞的標準流程。
- 當時 Apple II 的成功祕訣是「開放插槽 + 第三方擴充卡」，IBM 决定照抄這套哲學。
- 微軟的靠山：Altair BASIC 起家，已在業餘市場站穩，等著一躍而上。

## 線索與推理 -- 數學式、程式、理論
### 線索一：開放式設計的決策
IBM 做出三個違反自家傳統的決定：
1. **第三方零組件**：CPU 用 Intel 8088、作業系統向 Microsoft 授權 PC-DOS，而非自研。
2. **開放 ISA**：發布《IBM PC Technical Reference》手冊（含完整 BIOS 原始碼），任何人都知道如何插卡、如何呼叫系統。
3. **開放插槽**：5 個擴充槽，鼓勵第三方介面卡。

ISA（Industry Standard Architecture）匯流排的位址/資料空間定義：

$$\text{位址空間} = 2^{20} = 1\,\text{MB} \quad (\text{其中 RAM 通常僅 } 64\text{–}256\,\text{KB})$$

### 線索二：8088 CPU 4.77MHz
Intel 8088 是 8086 的「窮人版」：內部 16-bit、外部匯流排 8-bit。選它不是為了快，而是為了便宜——可用現成的 8-bit 週邊晶片。時脈 4.77 MHz 的來源也極為務實：NTSC 電視色副載波 $14.31818\,\text{MHz}$ 除以 3：

$$f_{CPU} = \frac{14.31818\,\text{MHz}}{3} = 4.7727\,\text{MHz}$$

8088 暫存器模型（Python 模擬，展示 16-bit 定址與 segment:offset）：

```python
MASK16 = 0xFFFF

class Regs8088:
    def __init__(self):
        self.ax = self.bx = self.cx = self.dx = 0   # 通用暫存器
        self.sp = self.bp = self.si = self.di = 0
        self.cs = self.ds = self.es = self.ss = 0  # 區段暫存器
        self.ip = 0                                 # 指令指標

    def set(self, name, value):
        assert 0 <= value <= MASK16, "16-bit 暫存器只有 0~65535"
        setattr(self, name, value)

    def physical(self, segment, offset):
        # 實體位址 = segment * 16 + offset（20-bit 定址的核心公式）
        return (segment << 4) + offset & 0xFFFFF

cpu = Regs8088()
cpu.set("cs", 0x1000)
cpu.set("ip", 0x0100)
print(hex(cpu.physical(cpu.cs, cpu.ip)))  # 0x10100
```

### 線索三：BIOS 與相容機（clone）產業
IBM 公布 BIOS 原始碼，卻忘了保護它。相容機廠商必須「乾淨室」（clean room）重寫功能相同、程式不同的 BIOS，以避開版權：

- 1982 年 Columbia、Compaq 推出相容機；Compaq 更做出可攜式 PC。
- 1984 年 Phoenix BIOS 授權給所有廠商，clone 產業全面爆發。
- 推理關鍵：**硬體可抄、BIOS 可重寫、但 DOS 的版權在 Microsoft 手上**——這是整個案件的樞紐。

### 線索四：Gates 的授權合約（非買斷！）
IBM 原本想買斷 DOS。Gates 拒絕，只授權、不賣斷，且合約允許微軟把 MS-DOS 授權給其他廠商。數學化的商業模型：

- 買斷：微軟收益 $= C$（一次性常數）。
- 授權：微軟收益 $= C' + r \cdot N(t)$，其中 $N(t)$ 為累計出貨台數，$r$ 為每台授權金。

當 $N(t)$ 隨 clone 產業指數成長時，$C' + rN(t) \gg C$。這紙合約讓微軟躺在每一台 PC 上收錢——**史上最值錢的一個「不」**。

### 線索五：Wintel 聯盟的誕生
IBM 想用 PS/2 與 OS/2（1987）奪回主導權，但 clone 廠商與微軟已強大到不受控制。最終標準的制定權落在 Intel（CPU）與 Microsoft（OS）手中，「Wintel」雙寡頭成形。

## 結案 -- 後果與影響
- IBM PC 成為事實標準，IBM 反而在 1990 年代退出自己發明的市場。
- PC 相容機產業造就 Compaq、Dell、Gateway，把電腦價格壓到蘋果難以招架。
- 微軟憑 MS-DOS/Windows 稱霸 30 年；Intel 憑 x86 持續迭代（286 → 386 → 486 → Pentium → x86-64）。
- 開放 ISA 生態（第三方介面卡、clone）成為後世 USB、PCIe 等開放標準的精神前身。
- 與 Mac 的封閉路線形成「開放 vs 封閉」世紀對決：短期開放贏（市占率），長期封閉在利潤與體驗上反撲（iPhone 時代）。

## 關鍵人物與文獻
- **Bill Gates / Paul Allen / Steve Ballmer**：微軟 DOS 授權談判與後續壟斷。
- **Don Estridge**：IBM PC 之父，Entry Level Systems 小組負責人。
- **Tim Paterson**：86-DOS（QDOS）作者，後被微軟買下改為 MS-DOS。
- 文獻：IBM PC Technical Reference (1981)；Gates, *The Road Ahead* (1995)；Chposky & Leonsis, *Blue Magic* (1988)。
