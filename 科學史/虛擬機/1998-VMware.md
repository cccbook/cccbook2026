# 1998 — VMware 成立：x86 虛擬化的破案

## 案件摘要
1998 年，Mendel Rosenblum 與 Diane Greene 在史丹佛 DISCO 論文（1997）的基礎上成立 VMware。兇手是一個懸案二十年的難題：x86 指令集違反 Popek–Goldberg 虛擬化條件，理論上「不可虛擬化」。VMware 用二進位轉譯繞過了這個障礙，開啟了伺服器整合與雲端運算的前夜。

## 前因 -- 為什麼會有這個案子
- **1960 年代的輝煌**：IBM System/360-67 與 CP-67/VM 證明大型主機可以跑多個虛擬機，hypervisor 概念早已存在。
- **Popek–Goldberg 定理（1974）**：Formal Virtualizability Requirements 給出虛擬化的充分條件：所有**敏感指令**必須是**特權指令**。
- **x86 的缺陷（1998 年前）**：x86 的 ring 0/3 設計中，存在約 **17 條敏感但非特權**的指令（如 `SGDT`、`SIDT`、`POPF` 在 ring 3 靜默失敗而不觸發 trap），無法被 hypervisor 攔截——理論上 x86 不可虛擬化。
- **史丹佛 DISCO（1997）**：Rosenblum 等人為 NUMA 機器寫的 hypervisor，重燃學界對 VM 的興趣。Rosenblum 與妻子 Greene（當時為 Sun 副總）看到 x86 伺服器市場的機會，1998 年成立 VMware。

## 線索與推理 -- 數學式、程式、理論

### Popek–Goldberg 虛擬化條件
定義指令集的三類性質：
- **特權指令（privileged）**：僅在特權模式（ring 0）執行，否則 **trap**。
- **敏感指令（sensitive）**：行為取決於特權模式或影響系統組態（如修改頁表、中斷）。
- **良性指令（innocuous）**：其餘。

**定理**：一個 ISA 可虛擬化（存在高效 VMM），若且唯若其敏感指令集是特權指令集的子集：

$$
S_{\text{sensitive}} \;\subseteq\; S_{\text{privileged}}
$$

條件成立時，VMM 可用 **trap-and-emulate**：Guest OS 以非特權模式執行，任何越權操作 trap 進 VMM，由 VMM 模擬該效果。

### x86 的破口
x86 有 17 條指令在 ring 3 執行時**不 trap 而靜默失敗**或**洩漏系統狀態**，例如：

- `POPF`：ring 3 執行時不 trap，且**忽略**對 IF 旗標的修改 → Guest 無法透過 trap 讓 VMM 管理中斷。
- `SGDT/SIDT`：任何 ring 都可執行，洩漏真實的 GDT/IDT 位址 → Guest 發現自己不是在 ring 0。

形式化地：對敏感指令 $i \in S_{\text{sensitive}}$，若 $i \notin S_{\text{privileged}}$，則在非特權模式執行時

$$
\text{exec}(i) \not\to \text{trap} \quad\Longrightarrow\quad \text{VMM 無法攔截與模擬}
$$

傳統 trap-and-emulate 對這些指令失效——這就是 1998 年前「x86 不可虛擬化」的學界共識。

### 二進位轉譯（Binary Translation）
VMware 的解法：**不依賴 trap，而是在執行前掃描 guest 機器碼**，把問題指令替換或改寫：

1. 掃描 basic block，若發現會 trap 的控制流或問題指令，改寫為「跳進 VMM 的 emulation routine」。
2. 轉譯後的碼快取（translation cache, TC）中重複執行，攤提掃描成本：

$$
T_{\text{BT}} \;=\; k \cdot t_{\text{native}} + C_{\text{translate}} \quad\text{vs}\quad T_{\text{trap}} \;=\; k \cdot (t_{\text{trap}} + t_{\text{emulate}})
$$

當 $k$ 大時，BT 遠勝於反覆 trap。這與 JIT 的攤提邏輯完全同構——VMware 其實是對 x86 機器碼做了一次「JIT」。

### VMware Workstation（1999）與 ESX Server（2001）
- **Workstation（1999）**：Type 2 hypervisor，跑在 Windows/Linux 之上，讓開發者在一台 PC 上執行多個 OS。
- **ESX Server（2001）**：Type 1 hypervisor（bare-metal），直接跑在硬體上，以 binary translation + 直接執行混合策略， targeting 伺服器整合——把數十台利用率僅 10–15% 的實體伺服器合併為一台 ESX 主機上的多個 VM。

### Hypervisor Type 1 vs Type 2 對照表

| | Type 1（bare-metal） | Type 2（hosted） |
|---|---|---|
| 位置 | 直接跑在硬體上 | 跑在 host OS 之上 |
| 例子 | ESX Server、Xen、Hyper-V | VMware Workstation、VirtualBox、KVM（Linux 模組） |
| 開銷 | 低（無 host OS 中介） | 較高（經 host OS 的驅動/排程） |
| 用途 | 資料中心、雲端 | 桌面、開發測試 |

架構對照：

$$
\text{Type 1:} \quad \text{HW} \leftarrow \text{VMM} \leftarrow \text{VM}_1, \text{VM}_2, \dots
$$

$$
\text{Type 2:} \quad \text{HW} \leftarrow \text{Host OS} \leftarrow \text{VMM} \leftarrow \text{VM}_1, \text{VM}_2, \dots
$$

### 伺服器整合與雲端的前夜
VM 的經濟學：$n$ 台實體機（各利用率 $u \approx 0.1$）可整合為一台跑 $n$ 個 VM 的機器，硬體成本與耗電近似降為 $\lceil n \cdot u \rceil$ 台。2001 年 ESX 問世後，x86 伺服器平均利用率開始攀升；2006 年 Amazon EC2 以 Xen 為基礎推出——雲端運算的技術底座，正是這條破案線索的延伸。

## 結案 -- 後果與影響
- VMware 成為 2000 年代虛擬化霸主，2004 年被 EMC 以 6.35 億美元收購，2007 年 IPO。
- **binary translation 是過渡解法**：2005–2006 年 Intel VT-x / AMD-V 硬體輔助虛擬化問世後，trap-and-emulate 恢復可行，BT 逐漸退居次要角色。
- 虛擬機帶動 **IaaS 雲端**（EC2 2006）、**容器技術**（Docker 2013，是 VM 之後更輕量的隔離層）、**軟體定義資料中心**。
- 學界影響：虛擬化從冷門考古（1970s IBM）重新變成電腦系統的核心課題。

## 關鍵人物與文獻
- **Gerald Popek & Robert Goldberg**：1974 年虛擬化定理。
- **Mendel Rosenblum**：史丹佛教授、DISCO 作者、VMware 共同創辦人。
- **Diane Greene**：VMware 共同創辦人與首任 CEO。
- **Edouard Bugnion, Scott Devine, Edward Wang**：VMware 核心工程師。
- Popek & Goldberg, *Formal Requirements for Virtualizable Third Generation Architectures*, CACM 17(7), 1974。
- Bugnion et al., *DISCO: Running Commodity Operating Systems on Scalable Multiprocessors*, SOSP 1997。
- Adams & Agesen, *A Comparison of Software and Hardware Techniques for x86 Virtualization*, ASPLOS 2006。
