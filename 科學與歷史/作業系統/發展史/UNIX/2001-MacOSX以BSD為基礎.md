# 2001 - Mac OS X 以 BSD 為基礎（帝國的 Unix 化）

## 案件摘要
2001 年 3 月 24 日，Apple 發布 **Mac OS X 10.0**——核心 **Darwin** 建立在 **Mach 微核心 + FreeBSD** 之上，Unix 第一次被「消費性電腦帝國」收編。
$$\text{Mac OS X} = \text{Mach 微核心} + \text{BSD（FreeBSD）} + \text{Aqua 圖形介面}.$$
**今天每一台 Mac、iPhone（iOS 為其後裔）的底下，都跑著一套 Unix**。

## 前因 -- 為什麼會有這個案子
- **Classic Mac OS 的崩壞**：1990 年代的 Mac OS 9 是「協作式多工」（程式不讓出 CPU 全機卡死）、無記憶體保護（一個程式當掉全機當機）、無 POSIX——**彌補的缺陷：三項全缺**。Apple 決心重寫。
- **NeXTSTEP 的收購**：1996 年 Apple 買下 **NeXT**（Steve Jobs 1985 年創辦）——NeXTSTEP 的核心正是 **Mach + BSD**。**一場收購，把 Unix 帶進 Apple**。
- **Mach 的理論遺產**：Carnegie Mellon 大學的 Mach 微核心（1985，Rick Rashid）——記憶體物件、訊息傳遞；NeXT/Apple 採「混合核心」：Mach 抽象 + BSD 實用層——**理論（微核心）與務實（BSD 驅動）的合體**。

## 線索與推理 -- 數學式、程式、理論

### 第一條線索：混合核心（hybrid kernel）
$$\text{Darwin} = \text{Mach（微核心抽象：IPC、記憶體物件）} + \text{BSD（實用層：POSIX、檔案系統、網路）}.$$
- **彌補的缺陷**：純微核心的效能損耗（IPC 開銷）與純巨核心的隔離性差——混合核心取兩者折衷：Mach 層管抽象，BSD 層管實用。

### 第二條線索：記憶體保護與搶佔式多工
- Mac OS 9：協作式多工 + 無保護 → **OS X：搶佔式多工 + 每行程獨立位址空間**。
- **彌補的缺陷**：一個程式卡死/當掉拖垮全機——OS X 用硬體分頁（MMU）強制隔離。

### 第三條線索：Unix 的終端與圖形的合體
$$\text{Terminal（BSD shell）} \;+\; \text{Aqua（圖形介面）} = \text{Mac OS X}.$$
- 開發者第一次在消費性電腦上**同時擁有** Unix 命令列與精緻圖形介面——**工程師大舉遷移到 Mac**。

### Shell 範例：Mac 上的 Unix

```bash
# 2001 年之後：Mac 就是 Unix（POSIX 認證）
$ uname -a
Darwin mymac 24.0.0 ... arm64
$ ls /usr/bin | head -5      # BSD 使用者空間
$ brew install python        # Homebrew（2009）——macOS 的套件管理
```

### C 範例：Mach 訊息傳遞（Darwin 的微核心層）

```c
/* Mach IPC：Darwin 底層的訊息傳遞（1985 年 Mach 的遺產） */
#include <mach/mach.h>

mach_msg(&header,           /* 訊息頭 */
         MACH_SEND_MSG,     /* 傳送 */
         size, 0,
         MACH_PORT_NULL,
         MACH_MSG_TIMEOUT_NONE,
         MACH_PORT_NULL);
```

## 結案 -- 後果與影響
- **iOS（2007）**：iPhone 的作業系統就是 Mac OS X 的精簡版——今天逾十億台 iOS 裝置跑著 Darwin/BSD 的後裔。
- **工程師的遷移**：2000 年代後，開發者社群大舉從 Linux/Windows 遷移到 Mac——**Unix 命令列 + 精緻圖形**的組合至今無敵。
- **BSD 的商業勝利**：Apple 的 BSD 授權使用是「寬容授權」的最大商業成功案例——對照 GPL 的 Linux，兩種授權各自找到戰場。
- **Objective-C → Swift（2014）**：NeXT 的 Objective-C 遺產延續到今天的 Swift。
- 歷史教訓：**帝國可以買下 Unix（NeXT 收購），但 Unix 的思想（POSIX、一切皆檔案）早已不可替代**。

## 關鍵人物與文獻
- **S. Jobs**：NeXT (1985)、Apple 收購 NeXT (1996)、Mac OS X (2001)。
- **R. Rashid**：Mach 微核心 (1985, CMU)。
- **M. McKusick et al.**：《The Design and Implementation of the 4.3BSD OS》。
- 相關案件：`1983-BSD4.2TCP_IP與Sun.md`、`1987-MINIX微核心.md`。
