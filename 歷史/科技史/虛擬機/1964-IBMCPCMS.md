# 1964 — IBM CP-40 / CP-CMS 與完整系統虛擬化

## 案件摘要
1964 年前後，IBM Cambridge 科學中心在改良的 IBM 7094（CP-40）上開發 CP/CMS，首次實現「完整的系統虛擬化」：每個使用者都拿到一台**完整的虛擬機器**，擁有自己的 OS。這是 hypervisor 誕生的犯罪現場，也是半世紀後雲端運算的祖譜起點。

## 前因 -- 為什麼會有這個案子
- 1960 年代初，MIT 的 CTSS 證明了「時間共享（time-sharing）」可行：多人分時共用一台機器，每人分到時間片。
- 但時間共享是「OS 層面的共享」：所有使用者共用同一個作業系統，OS 一掛大家全掛，且無法各自執行不同 OS。
- IBM 與 MIT 合作 Project MAC 時需要一台能服務多位研究者的機器；Cambridge 科學中心則想驗證「機器共享（machine-sharing）」：直接把硬體切成多台完整的虛擬機器。
- 線索：能否寫一層軟體「扮演硬體」，讓每個 guest OS 都以為自己獨占整台機器？

## 線索與推理 -- 數學式、程式、理論

### 1. 時間共享 vs 機器共享
- **Time-sharing**：$N$ 個使用者 $\to$ 一個 OS $\to$ 硬體。共享的是 OS。
- **Machine-sharing（虛擬機）**：$N$ 個使用者 $\to$ $N$ 個 guest OS $\to$ hypervisor $\to$ 硬體。共享的是硬體。

後者的隔離性與彈性（各自可跑不同 OS、可快照、可遷移）是雲端架構的本質。

### 2. Hypervisor（VMM）的誕生
CP（Control Program）就是最早的 hypervisor/VMM（Virtual Machine Monitor）。定義（Goldberg 1973）：

> VMM 是一個軟體，它 (1) 提供一個與原始機器幾乎相同但隔離的程式執行環境（efficiency）；(2) 對此環境中執行的程式有完全的控制權（resource control）。

CP-CMS 的架構：

```
+---------+  +---------+  +---------+
| CMS #1  |  | CMS #2  |  |  ...    |   guest OS（單使用者互動式系統）
+---------+  +---------+  +---------+
|     CP (hypervisor)             |   提供虛擬機
+---------------------------------+
|        IBM 7094 / S/360 硬體     |
+---------------------------------+
```

### 3. Trap-and-emulate 原理
guest OS 執行特權指令（如 IO、改頁表）時必須陷入 hypervisor，由 hypervisor 模擬該指令的效果再返回：

```python
class Hypervisor:
    def __init__(self):
        self.devices = {"disk": "drum0"}

    def run(self, vm, code):
        pc = 0
        while pc < len(code):
            op, arg = code[pc]
            if op == "privileged":        # 特權指令 -> trap
                result = self.emulate(arg)  # VMM 模擬硬體效果
                vm.registers["R0"] = result
            else:
                vm.execute_user(op, arg)    # 非特權指令直接在硬體上跑
            pc += 1
```

效率關鍵：非特權指令**不經模擬**、直接在真實 CPU 上執行，只有特權指令陷入。

### 4. Popek–Goldberg 虛擬化定理（1974）
定理：對一個第三代電腦架構，若其**敏感指令（sensitive instructions）是特權指令的子集**，則該架構可虛擬化。

敏感指令三條件（改變系統組態或影響行為的指令）：
1. **Privileged**：使用者模式執行會陷入（trap）。
2. **Control-sensitive**：改變處理器模式或記憶體位址轉換（如 LPSW、設定頁表）。
3. **Behavior-sensitive**：執行結果依賴系統組態（如讀 timer、實際位址）。

形式化：$\text{sensitive} \subseteq \text{privileged} \Rightarrow \text{virtualizable}$。

IBM S/360 的問題恰恰是部分敏感指令（如 `LPSW`）**不陷入**，導致 S/360 早期無法完美虛擬化，IBM 得用 "hardware assist"（S/370 加了 V=R 模式）補救。x86 直到 2005 年 VT-x 才補齊。

### 5. 程式：檢查指令集可否虛擬化

```python
sensitive = {"LPSW", "STCTL", "SIO", "TIO", "SVC", "LRA"}
privileged = {"SIO", "TIO", "SVC"}          # S/360: LPSW 不陷入

def virtualizable():
    return sensitive <= privileged

print(virtualizable())   # False -> S/360 需要硬體輔助才能虛擬化
```

## 結案 -- 後果與影響
- CP-40 的經驗直接移植到 System/360 上成為 **CP-67**，再商品化為 **VM/370**（1972）。
- 證明了 hypervisor 概念可行，且「一機多用戶、各跑各的 OS」的模型被市場接受。
- Popek–Goldberg 定理成為虛擬化理論的基石，指導了 30 年硬體設計。
- VMware（1998）、Xen、KVM、乃至 AWS EC2 的虛擬機，概念血統都可追溯到 CP-CMS 的 trap-and-emulate。

## 關鍵人物與文獻
- **Robert Creasy、Richard Parmelee**：CP-40/CP-CMS 主要設計者。
- Creasy, *The Origin of the VM/370 Time-Sharing System*, IBM J. R&D, 1981.
- Parmelee et al., *Virtual Storage and Virtual Machine Concepts*, IBM Systems Journal, 1972.
- Popek & Goldberg, *Formal Requirements for Virtualizable Third Generation Architectures*, CACM 17(7), 1974.
