# 2003 — QEMU 與 Xen：虛擬化的兩條道路合流

## 案件摘要
2003 年，兩位學界工程師各自發表了影響深遠的虛擬機系統：Fabrice Bellard 一人以一己之力寫出 QEMU，用動態二進位轉譯實現跨 ISA 的全系統模擬；劍橋大學的 Xen hypervisor 用半虛擬化繞過 x86 的虛擬化缺陷。兩條看似不同的路，在 2007 年與 KVM 合流，並隨 Intel VT-x（2005）抵達終極解法。

## 前因 -- 為什麼會有這個案子
- **VMware 的封閉與昂貴**：1999–2003 年 VMware 是 x86 虛擬化唯一成熟方案，閉源且商用授權昂貴；學界與開源社群需要自由的替代品。
- **跨 ISA 模擬的需求**：嵌入式開發（ARM/PowerPC）、作業系統研究、legacy 系統（Old Mac、SPARC）都需在 x86 上模擬其他架構——現有模擬器（Bochs 純直譯）慢到不可用。
- **Bellard 的前科**：Fabrice Bellard 曾贏得 FFmpeg（2000）的作者聲望；2003 年發表 QEMU 論文，其 TCG 動態二進位轉譯比 Bochos 快 $10\times$ 以上。
- **x86 仍不可虛擬化（2003）**：VT-x 尚未問世，敏感非特權指令的破口仍在；劍橋開發者選擇另一條路——**修改 Guest OS 原始碼**，讓它主動配合 hypervisor（paravirtualization）。

## 線索與推理 -- 數學式、程式、理論

### QEMU 的動態二進位轉譯（TCG）
QEMU 的執行模型：

1. **TB（Translation Block）**：guest 程式碼被切成 basic block（以分支/跳轉結尾）。
2. **TCG（Tiny Code Generator）**：把 guest TB 編譯成 host 機器碼，快取在 code cache。
3. **TB chaining**：轉譯後的 TB 直接跳到下一個已轉譯的 TB，避免回到執行迴圈：

$$
\text{TB}_1 \xrightarrow{\text{direct jump}} \text{TB}_2 \xrightarrow{\text{direct jump}} \text{TB}_3 \;\dots
$$

攤提後的效能模型：

$$
T_{\text{TCG}} \;=\; n \cdot c \cdot t_{\text{exec}} + \frac{C_{\text{gen}}}{k}, \qquad c \approx 1.1\text{–}2 \;(\text{相對原生})
$$

其中 $c$ 為 code quality factor，$k$ 為 TB 重複執行次數。對比純直譯的 $c \approx 10$，TCG 快一個數量級。

### 全系統模擬：跨 ISA 互模擬
QEMU 的核心設計是**guest 與 host ISA 解耦**：CPU 狀態（暫存器、PC、flags）用架構無關的 `CPUState` 結構表示，TCG 把 guest ISA 翻成 host ISA：

$$
\text{guest } (\text{ARM, PPC, SPARC, x86, \dots}) \;\xrightarrow{\;\text{TCG}\;}\; \text{host } (\text{x86, ARM, \dots})
$$

這使得**任意組合**的 $n \times m$ 模擬只需 $n + m$ 個前端/後端——與 1995 年 JVM 的 Write Once Run Anywhere 數學結構完全同構，只是這次模擬的是完整電腦（CPU + 裝置 + 中斷 + MMU）而非單一語言。

### Xen 的半虛擬化（paravirtualization）
Xen 的策略：**修改 Guest OS 原始碼**，把敏感指令改為**顯式的 hypercall**（類似系統呼叫但呼叫 hypervisor）：

$$
\text{trap-and-emulate:} \quad \text{敏感指令} \to \text{trap} \to \text{VMM 模擬}
$$

$$
\text{paravirtualization:} \quad \text{敏感操作} \to \text{hypercall（顯式呼叫）} \to \text{Xen}
$$

- **Ring compression**：x86 只有 ring 0–3，Xen 把自己放在 ring 0，Guest kernel 放在 ring 1，應用程式在 ring 3——壓縮了特權環的使用：

$$
\text{ring 0: Xen} \quad | \quad \text{ring 1: Guest kernel} \quad | \quad \text{ring 3: 應用}
$$

- **特權環壓縮的代價**：Guest kernel 的每次特權操作（頁表更新、中斷處理）都要經 ring 1 → ring 0 的切換，但由於是顯式呼叫，Xen 可以用批次（batch）與驗證（validate）最佳化。
- **Dom0/DomU 架構**：Xen 的特權域 Dom0 負責後端驅動（磁碟、網路），非特權域 DomU 透過前後端驅動與共享記憶體通訊。

### 硬體輔助虛擬化：Intel VT-x（2005）/ AMD-V 的終極解法
2005–2006 年，晶片廠在硬體中新增 **Guest 模式**（non-root mode）：

- **Intel VT-x**：新增 VMX root/non-root mode、VMCS（虛擬機控制結構）記錄 VM 狀態；`VMLAUNCH/VMRESUME` 進入 guest，敏感指令在 guest 模式自動 **VM-exit** trap 進 hypervisor。
- **AMD-V**：類似機制（SVM mode、VMCB）。

數學上，硬體輔助使 x86 恢復 Popek–Goldberg 條件：

$$
\text{non-root 模式下：} \quad \forall i \in S_{\text{sensitive}}: \; \text{exec}(i) \to \text{VM-exit} \;\Longrightarrow\; S_{\text{sensitive}} \subseteq S_{\text{privileged}}^{\text{(root)}}
$$

此後：Xen 的 HVM 模式（不需改 Guest OS）、KVM 直接用 VT-x、VMware 逐步棄用 binary translation——三條路殊途同歸。

### QEMU-KVM 合流（2007）
KVM（2006 併入 Linux kernel，2007 穩定）是 Linux 的 Type 1 hypervisor 模組，負責 CPU 與記憶體虛擬化（直接用 VT-x）；但它借用 QEMU 作為**裝置模型**（device model，模擬磁碟、網卡、顯示卡）：

$$
\text{Guest} \;\leftrightarrow\; \underbrace{\text{KVM（kernel：CPU/記憶體，VT-x 加速）}}_{\text{快}} + \underbrace{\text{QEMU（user：裝置模擬）}}_{\text{QEMU 遺產}}
$$

QEMU 從「轉譯者」轉型為「裝置模擬器 + 通用虛擬機框架」，TCG 退居「無 KVM 時的 fallback」與跨 ISA 模擬用途。

### Python 展示簡單二進位轉譯範例
以下用 Python 模擬「把 guest 指令碼轉譯為 Python 函式」的動態二進位轉譯：

```python
# Guest ISA：一個簡單的堆疊機指令集
# PUSH n / ADD / MUL / DUP / PRINT / HALT
GUEST_CODE = ['PUSH 2', 'PUSH 3', 'MUL', 'DUP', 'ADD', 'PRINT', 'HALT']

def translate(tb):
    """把 guest 指令轉譯為 Python 原始碼（模擬 TCG 生成 host 碼）"""
    lines, stack_depth = [], 0
    for ins in tb:
        op, *args = ins.split()
        if op == 'PUSH':
            lines.append(f"    st.append({args[0]})")
        elif op == 'ADD':
            lines.append("    st.append(st.pop() + st.pop())")
        elif op == 'MUL':
            lines.append("    st.append(st.pop() * st.pop())")
        elif op == 'DUP':
            lines.append("    st.append(st[-1])")
        elif op == 'PRINT':
            lines.append("    print(st.pop())")
        elif op == 'HALT':
            lines.append("    return")
    return "def host_code(st):\n" + "\n".join(lines)

# 動態「編譯」：exec 生成 host 函式（等同 TCG 生成機器碼並放入 code cache）
exec(translate(GUEST_CODE))
cache = {}                 # translation cache
cache[tuple(GUEST_CODE)] = host_code

# 執行：直接呼叫編譯後的「機器碼」，重複執行攤提編譯成本
st = []
for _ in range(3):         # 執行 3 次，只編譯 1 次
    cache[tuple(GUEST_CODE)](st)
# 輸出：12 12 12   （2*3=6, DUP 得 6,6, ADD 得 12）
```

（註：本例展示的是「編譯一次、執行多次」的攤提模型——真實 TCG 的本質相同：把 guest basic block 編成 host 機器碼、快取、並用 direct jump 串鏈（TB chaining）。）

## 結案 -- 後果與影響
- **QEMU** 成為開源虛擬化的基石：模擬幾乎所有 ISA（ARM、RISC-V、PowerPC、s390x），是作業系統教學、嵌入式開發、跨架構測試的標準工具；2008 年起與 KVM 合流成為 Linux 雲端生態的標準配備。
- **Xen** 成為 2006 年 Amazon EC2 的底座，撑起第一代公有雲；後來逐步讓位給 KVM（AWS 部分轉向 Nitro/KVM）。
- **VT-x/AMD-V** 使硬體輔助虛擬化成為所有現代 CPU 的標準配備，也催生了容器與 microVM（Firecracker 2018）。
- Bellard 的傳奇延續：FFmpeg、TCC、計算 $\pi$ 的世界紀錄——一人之力改寫多個領域。

## 關鍵人物與文獻
- **Fabrice Bellard**：QEMU、FFmpeg、TCC 的作者。
- **Keir Fraser & Ian Pratt**：劍橋 Xen 計畫主持人。
- **Avi Kivity**：KVM 的原作者（2006）。
- Bellard, F., *QEMU, a Fast and Portable Dynamic Translator*, USENIX ATC 2005 (FREENIX)。
- Barham et al., *Xen and the Art of Virtualization*, SOSP 2003。
- Kivity et al., *kvm: the Linux Virtual Machine Monitor*, Ottawa Linux Symposium 2007。
