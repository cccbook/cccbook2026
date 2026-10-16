# 1987 - MINIX 微核心（教科書 Unix 與微核心思想）

## 案件摘要
1987 年，荷蘭 Vrije Universiteit 的 Andrew Tanenbaum 出版《Operating Systems: Design and Implementation》，
隨書附上 **MINIX**——一個為教學設計、可在 IBM PC 上執行的**完整 Unix 相容系統**，原始碼全書公開。
同時 MINIX 採用**微核心** (microkernel) 架構：
$$\text{核心只做最小的事（行程、記憶體、IPC）} \quad \text{驅動程式與檔案系統全部成為用戶程式}.$$
Unix 的宏核心傳統（見「1969-Unix誕生.md」）遭遇第一個系統性挑戰——
而 MINIX 的學生讀者中，有一位芬蘭人寫出了 Linux。

## 前因 -- 為什麼會有這個案子
- **Unix 源碼的封閉**：1984 年 AT&T 解體後開始**商業化 Unix**——大學不能再拿 Unix 原始碼教學（授權費昂貴）——**教學命案**：作業系統課程沒有可讀的原始碼。
- **Tanenbaum 的偵探手法**：與其買授權，不如**自己寫一個**——從零寫出 Unix 相容系統，原始碼印在書裡（約 12,000 行）——「教科書 + 原始碼 + 可執行」的三合一。
- **微核心的學術路線**：與 Multics/Unix 的宏核心（所有功能在核心態）相反——Tanenbaum 主張核心越小越好：
  $$\text{宏核心：失敗即當機} \quad \text{vs} \quad \text{微核心：驅動當機可重啟}.$$
- **Mach 的並行路線**：CMU 的 Mach（1985）同樣是微核心——成為 macOS (Darwin) 的基礎——微核心思想在學術界成為主流。

## 線索與推理 -- 數學式、程式、理論

### 第一條線索：微核心的架構
宏核心（Unix/Linux）：
$$\text{核心態} = \text{排程 + 記憶體 + 檔案系統 + 驅動 + 網路} \quad (\text{全部}).$$
微核心（MINIX）：
$$\text{核心態} = \text{排程 + IPC + 基本記憶體} \quad \text{（最小）},$$
$$\text{用戶態行程} = \text{檔案系統、驅動程式、網路伺服器} \quad (\text{各為獨立行程}).$$
- **訊息傳遞 (IPC)** 取代系統呼叫直達核心：
  $$\text{用戶行程} \xrightarrow{\text{message}} \text{FS 伺服器} \xrightarrow{\text{message}} \text{磁碟驅動}.$$
- **故障隔離**：驅動程式當機 → 只重啟該行程，核心不受影響——**可靠性的誕生**。

### 第二條線索：微核心的性能代價
訊息傳遞比系統呼叫直達多一次跨行程通訊：
$$\text{一次檔案讀取（微核心）} = 3\text{ 次行程切換} + 2\text{ 次訊息拷貝} \quad \text{vs（宏核心）} = 1\text{ 次系統呼叫}.$$
$$\text{微核心開銷} \approx 2\text{–}5\times \text{（當年的 IPC 成本）}.$$
這是宏核心 vs 微核心的百年辯論核心——**可靠性 vs 性能**。

### 第三條線索：教學的勝利
MINIX 原始碼 12,000 行、全書註解——**一個學生一學期可讀完**：
$$\text{Unix（數十萬行）} \quad \text{vs} \quad \text{MINIX（1.2 萬行，可讀）}.$$
1991 年，芬蘭學生 Linus Torvalds 用 MINIX 為開發平台寫出 Linux——見「1991-Linux誕生.md」。

### Python：微核心 vs 宏核心的 IPC 開銷模擬

```python
import numpy as np

ctx_switch, msg_copy = 1.0, 0.5      # 微秒級示意成本

def syscall_cost(microkernel):
    if microkernel:                   # user → FS → driver → user（3 切換 2 拷貝）
        return 3*ctx_switch + 2*msg_copy
    else:                             # 直達核心（1 次系統呼叫）
        return ctx_switch + msg_copy*0.2

print(f"宏核心讀檔成本: {syscall_cost(False):.2f} μs")
print(f"微核心讀檔成本: {syscall_cost(True):.2f} μs  (開銷 {syscall_cost(True)/syscall_cost(False):.1f}x)")
print("但驅動當機 → 微核心只重啟驅動，宏核心整機當機")
```
輸出：
```
宏核心讀檔成本: 1.10 μs
微核心讀檔成本: 4.00 μs  (開銷 3.6x)
但驅動當機 → 微核心只重啟驅動，宏核心整機當機
```

## 結案 -- 後果與影響
- **教學的革命**：OS 課程第一次有完整可讀原始碼；MINIX 3（2006）更進一步——驅動全在用戶態，朝「可自癒系統」邁進。
- **微核心的商業遺產**：Mach → **macOS/iOS 的 XNU 核心**（Mach + BSD 混合）、QNX（車用與工控）、L4 家族（嵌入式）——微核心思想統治了安全關鍵領域。
- **宏核心的勝利**：Linux（1991）選擇宏核心——性能與務實取勝，統治伺服器與 Android——Tanenbaum–Torvalds 辯論（1992）成為經典。
- **Tanenbaum–Torvalds 辯論**：Tanenbaum 批評 Linux「1991 年還寫宏核心是倒退」；Torvalds 回應「如果 GNU Hurd 準備好了，我就不會寫 Linux」——**學術的純粹 vs 工程的務實**，辯論至今仍是教科書案例。
- 歷史定位：MINIX 的最大貢獻不是它自己，而是**它的讀者**——教科書孵育了 Linux，一如 Multics（失敗者）孵育了 Unix。

## 關鍵人物與文獻
- **A. S. Tanenbaum**：《Operating Systems: Design and Implementation》(1987)；MINIX 3, CACM 49 (2006)。
- **R. Rashid**：Mach 微核心 (1985)——macOS 的祖先。
- **Torvalds–Tanenbaum 辯論**：comp.os.minix (1992)。
- 相關案件：`1969-Unix誕生.md`、`1991-Linux誕生.md`、`1983-GNU計畫.md`。
